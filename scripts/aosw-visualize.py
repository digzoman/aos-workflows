#!/usr/bin/env python3
"""Optional AOS-W 0.8 self-contained offline workflow visualizer.

Agent-only/manual use requires no Python. This convenience renderer reads the
original YAML template or a pinned graph and optional derived run state, then
writes a READ-ONLY standalone HTML snapshot under agent-files/visualizations.
Never uploads to GitHub Pages, never edits workflow state or authorizations.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

# Optional developer convenience; the installed core remains manual/file-only.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aosw_human_profile import add_human_profile

ROOT = Path(__file__).resolve().parents[1]
VIEWER = ROOT / "scaffold/aos-w/references/visualization-viewer.html"
TOKEN = "__AOSW_SNAPSHOT_JSON__"
SAFE = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
ALLOWED_STATUSES = {
    "NOT_STARTED", "READY", "RUNNING", "COMPLETE", "ACCEPTED",
    "WAIT_DEPENDENCY", "WAIT_CONDITION", "WAIT_APPROVAL", "REVIEW_WAIT",
    "NEEDS_REWORK", "BLOCKED", "RECONCILE_REQUIRED", "CANCELLED",
    "FAILED", "SKIPPED", "SKIPPED_BY_CONDITION", "SUPERSEDED", "STALE",
    "UNKNOWN", "CREATED", "PAUSED", "PENDING"
}

class ViewError(ValueError):
    pass

def ensure_safe_output(path: Path):
    path = path.absolute()
    parts = path.parts
    if "agent-files" not in parts or "visualizations" not in parts:
        raise ViewError("Output must be under <aos-w>/agent-files/visualizations/")
    idx = parts.index("agent-files")
    if idx + 1 >= len(parts) or parts[idx + 1] != "visualizations":
        raise ViewError("Output must be in agent-files/visualizations/")
    if idx < 1 or parts[idx - 1] != "aos-w":
        raise ViewError("Parent of agent-files must be aos-w")
    if path.name != "index.html" or len(parts) < idx + 4:
        raise ViewError("Output must be agent-files/visualizations/<safe-id>/index.html")
    if not SAFE.fullmatch(parts[idx + 2]):
        raise ViewError("Unsafe visualization ID")
    if len(parts) != idx + 4:
        raise ViewError("One visualization ID directory only")
    # Refuse symlink redirects in any existing path element.
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise ViewError("Symlink output path forbidden")
    if path.exists() and not path.is_file():
        raise ViewError("Output path is not a file")
    return path

def load_yaml(path: Path):
    try:
        import yaml
    except ImportError as e:
        raise ViewError("PyYAML is optional but required for --template or --graph; use --snapshot JSON without it") from e
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ViewError("Expected YAML object")
    return data

def sanitized_text(value, max_len=18000):
    if value is None:
        return None
    if isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value[:max_len]
    if isinstance(value, list):
        return [sanitized_text(v, max_len) for v in value[:200]]
    if isinstance(value, dict):
        return {str(k)[:100]: sanitized_text(v, max_len)
                for k,v in list(value.items())[:120]}
    return str(value)[:max_len]

def source_to_snapshot(template: dict, state: dict | None, source: str, title: str | None):
    graph = template.get("graph")
    if not isinstance(graph, dict) or not isinstance(graph.get("nodes"), list):
        raise ViewError("Graph.nodes missing")
    if len(graph["nodes"]) > 240:
        raise ViewError("Graph exceeds 240 nodes, split or collapse children")
    mode = "RUN" if state is not None else ("INSTANCE" if source.endswith(".yaml") and "graph-revisions" in source else "TEMPLATE")
    tasks = state.get("tasks", {}) if isinstance(state, dict) else {}
    nodes = []
    seen = set()
    for entry in graph["nodes"]:
        if not isinstance(entry, dict):
            raise ViewError("Node must be an object")
        node_id = entry.get("id")
        if not isinstance(node_id, str) or not SAFE.fullmatch(node_id) or node_id in seen:
            raise ViewError("Node ID missing, duplicated or unsafe")
        seen.add(node_id)
        task = tasks.get(node_id, {}) if isinstance(tasks, dict) else {}
        if not isinstance(task, dict):
            task = {}
        raw_status = task.get("status") if state is not None else "NOT_STARTED"
        status = raw_status if raw_status in ALLOWED_STATUSES else "UNKNOWN"
        child = entry.get("child_template_ref")
        full_prompt = entry.get("instructions") or entry.get("prompt")
        if full_prompt is not None and (not isinstance(full_prompt, str) or len(full_prompt) > 18000):
            raise ViewError("Step "+node_id+" prompt must be full text of at most 18000 chars, not silently truncated")
        nodes.append({
            "id": node_id,
            "label": sanitized_text(entry.get("title") or entry.get("name") or node_id, 180),
            "title": sanitized_text(entry.get("title"), 140),
            "summary": sanitized_text(entry.get("summary"), 500),
            "purpose": sanitized_text(entry.get("purpose"), 500),
            "phase_id": sanitized_text(entry.get("phase_id"), 120),
            "phase_title": sanitized_text(entry.get("phase_title"), 120),
            "lane_id": sanitized_text(entry.get("lane_id"), 120),
            "lane_title": sanitized_text(entry.get("lane_title"), 120),
            "required_actions": sanitized_text(entry.get("required_actions")),
            "resources": sanitized_text(entry.get("resources")),

            "kind": sanitized_text(entry.get("kind"), 70),
            "needs": sanitized_text(entry.get("needs", [])),
            "status": status,
            "prompt": full_prompt,
            "inputs": sanitized_text(entry.get("inputs")),
            "outputs": sanitized_text(entry.get("outputs")),
            "quality": sanitized_text(entry.get("quality")),
            "contract": sanitized_text(entry.get("contract")),
            "when": sanitized_text(entry.get("when")),
            "retry": sanitized_text(entry.get("retry")),
            "child_template": sanitized_text(child.get("template_id") if isinstance(child, dict) else child, 200),
            "owner": sanitized_text(task.get("owner") or task.get("claimed_by"), 200),
            "attempts": sanitized_text(task.get("attempts")),
            "review": sanitized_text(task.get("review")),
            "evidence": sanitized_text(task.get("evidence")),
            "notes": sanitized_text(task.get("error") or task.get("blocked_reason")),
            "source": "Pinned graph source, not current mutable master" if mode != "TEMPLATE" else "Published template definition",
            "policy": sanitized_text(template.get("policy",{})),
            "child_ref": sanitized_text(child)
        })
    missing = sorted({dep for n in nodes for dep in (n["needs"] or [])
                      if isinstance(dep, str) and dep not in seen})
    if missing:
        raise ViewError("Missing graph dependencies: " + ", ".join(missing[:12]))
    # Reject cyclic dependencies, rather than draw false DAG ordering.
    lookup = {n["id"]: n for n in nodes}
    visiting, visited = set(), set()
    def check_acyclic(node_id):
        if node_id in visiting:
            raise ViewError("Cycle detected at " + node_id)
        if node_id in visited:
            return
        visiting.add(node_id)
        for predecessor in lookup[node_id]["needs"] or []:
            check_acyclic(predecessor)
        visiting.remove(node_id)
        visited.add(node_id)
    for node_id in lookup:
        check_acyclic(node_id)
    if state is not None and state.get("graph_revision") and "graph-revisions" not in source:
        warning = "State overlay used on nonpinned template path; verify graph revision manually."
    else:
        warning = "Run status is derived from state.json and has NOT been reconciled against events, providers or reviewer signatures." if state is not None else "Template-only structure; no live progress is implied."
    result = {
        "visualization_schema": "1.0.0",
        "mode": mode,
        "title": title or template.get("name") or "AOS-W workflow",
        "template_id": template.get("template_id", "pinned-instance-graph"),
        "run_id": state.get("run_id") if state is not None else None,
        "graph_revision": state.get("graph_revision") if state is not None else None,
        "event_seq_observed": state.get("last_event_seq") if state is not None else None,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verification": "SOURCE_SNAPSHOT_UNVERIFIED",
        "public_export": False,
        "warning": warning,
        "nodes": nodes
    }
    return add_human_profile(result, template)

def run_dir_snapshot(folder: Path, title: str | None = None, verify_events: bool = True):
    """Read a saved run and its pinned graph without mutating the run.

    With the optional development RunStore, scan exact event hashes, detect
    torn tails and reject a conflicting snapshot. No reviewer/provider
    authentication can be inferred from valid local event bytes alone.
    """
    folder = folder.absolute()
    if folder.is_symlink() or any(p.is_symlink() for p in folder.parents):
        raise ViewError("Symlink source run folder not allowed")
    if not folder.is_dir() or folder.parent.name != "runs":
        raise ViewError("Expected agent-files/instances/<id>/runs/<run-id>")
    instance = folder.parent.parent
    if instance.parent.name != "instances" or instance.parent.parent.name != "agent-files":
        raise ViewError("Run is not in an AOS-W instance")
    data = json.loads((folder/"run.json").read_text(encoding="utf-8"))
    state = json.loads((folder/"state.json").read_text(encoding="utf-8"))
    if data.get("run_id") != folder.name or state.get("run_id") != folder.name:
        raise ViewError("Run identity conflicts with saved file path")
    revision = state.get("graph_revision")
    if not isinstance(revision,str) or not SAFE.fullmatch(revision):
        raise ViewError("Invalid pinned graph revision")
    graph_path = instance/"graph-revisions"/(revision+".yaml")
    if not graph_path.is_file() or graph_path.is_symlink():
        raise ViewError("Pinned graph revision missing/unsafe")
    graph = load_yaml(graph_path)
    if verify_events:
        sys.path.insert(0,str(ROOT/"tools/state"))
        try:
            from state import RunStore, StateError
            result = RunStore(folder).verified()
        except (OSError, ValueError, KeyError) as exc:
            raise ViewError("Event verification failed, visualization blocked: "+str(exc)) from exc
        if result.get("graph_revision") != revision or result.get("last_event_seq") != state.get("last_event_seq"):
            raise ViewError("Saved state differs from event-verified graph/sequence")
        if result.get("last_event_digest") != state.get("last_event_digest"):
            raise ViewError("Saved state digest disagrees with event stream")
        # Use the recomputed state as the display source of truth, not a
        # potentially older standalone state.json overlay.
        state = result
    doc=source_to_snapshot(graph,state,str(graph_path),title)
    doc["verification"] = ("EVENTS_RECONCILED"
                           if verify_events and state.get("integrity_level")=="verified"
                           else "SOURCE_SNAPSHOT_UNVERIFIED")
    doc["warning"] = (
        "Event chain reconciled against local journal; actor/reviewer claims and external provider state are NOT authenticated."
        if doc["verification"]=="EVENTS_RECONCILED"
        else "Saved state is advisory or legacy; no proof of external provider truth or authenticated review.")
    doc["source_graph"] = revision
    doc["instance_id"] = instance.name
    # Bounded activity metadata only. Avoid opaque event payloads that may hold
    # tokens, customer data or private source content.
    if (folder/"events.jsonl").is_file():
        activity={}
        for line in (folder/"events.jsonl").read_text(encoding="utf-8").splitlines():
            if not line.strip(): continue
            event=json.loads(line)
            task_id=event.get("task_id")
            if task_id and isinstance(task_id,str):
                log=activity.setdefault(task_id,[])
                actor=event.get("actor") or {}
                log.append({"seq":event.get("seq"),"type":event.get("type"),
                            "at":event.get("at"),"actor": actor.get("agent") if isinstance(actor,dict) else None})
                if len(log)>8: del log[:-8]
        for node in doc["nodes"]:
            node["activity"]=activity.get(node["id"],[])
    return add_human_profile(doc, graph)

def resolve_local_children(snapshot: dict, template_path: Path):
    """Show actual subworkflow prompts only when the local module matches
    the compound template's pinned content SHA-256. Never fetch remotely.
    """
    template_path=Path(template_path).absolute()
    if template_path.name!="template.yaml" or template_path.parent.parent.name!="templates":
        return snapshot
    library=template_path.parent.parent
    for n in snapshot["nodes"]:
        ref=n.get("child_ref")
        if not isinstance(ref,dict): continue
        name=ref.get("template_id")
        pin=ref.get("content_digest")
        n["child_resolution"]="UNRESOLVED"
        if not isinstance(name,str) or not SAFE.fullmatch(name):
            n["child_resolution"]="INVALID_ID";continue
        if not isinstance(pin,str) or not re.fullmatch(r"sha256:[a-f0-9]{64}",pin):
            n["child_resolution"]="NO_VERIFIABLE_PIN";continue
        target=library/name/"template.yaml"
        if target.is_symlink() or not target.is_file():
            n["child_resolution"]="PINNED_MODULE_NOT_FOUND";continue
        actual="sha256:"+hashlib.sha256(target.read_bytes()).hexdigest()
        if actual!=pin:
            n["child_resolution"]="PIN_DIGEST_MISMATCH";continue
        child=load_yaml(target)
        if child.get("template_id")!=name or child.get("version")!=ref.get("version"):
            n["child_resolution"]="PIN_VERSION_MISMATCH";continue
        steps=child.get("graph",{}).get("nodes",[])
        if not isinstance(steps,list) or len(steps)>60:
            n["child_resolution"]="INVALID_SUBGRAPH";continue
        listed=[]
        for step in steps:
            prompt=step.get("instructions") or step.get("prompt")
            if not isinstance(prompt,str) or len(prompt)>18000:
                n["child_resolution"]="INVALID_PROMPT";listed=[];break
            listed.append({"id":step.get("id"),"kind":step.get("kind"),"prompt":prompt,
                "needs":step.get("needs",[]),"inputs":step.get("inputs",[]),
                "outputs":step.get("outputs",[]),"quality":step.get("quality",{}),
                "contract":step.get("contract",{})})
        if listed:
            n["child_resolution"]="PINNED_LOCAL_MODULE_VERIFIED"
            n["child_steps"]=listed
    return snapshot

def encode_json(data):
    # This embedding never executes untrusted labels as HTML, JS, or a URL.
    return (json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026").replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))

def validate_snapshot(data: dict):
    if not isinstance(data, dict) or data.get("visualization_schema") != "1.0.0":
        raise ViewError("Visualization schema must be 1.0.0")
    if data.get("mode") not in ("TEMPLATE", "INSTANCE", "RUN"):
        raise ViewError("Invalid visualization mode")
    if not isinstance(data.get("title"), str) or not data["title"]:
        raise ViewError("Missing visualization title")
    if data.get("verification") not in ("SOURCE_SNAPSHOT_UNVERIFIED", "EVENTS_RECONCILED", "HOST_VALIDATED"):
        raise ViewError("Invalid verification tier")
    nodes=data.get("nodes")
    if not isinstance(nodes, list) or not 1<=len(nodes)<=240:
        raise ViewError("Expected 1..240 nodes")
    names=set()
    for n in nodes:
        if not isinstance(n, dict) or not isinstance(n.get("id"), str) or not SAFE.fullmatch(n["id"]):
            raise ViewError("Invalid snapshot step ID")
        if n["id"] in names:
            raise ViewError("Duplicate snapshot step ID")
        names.add(n["id"])
        if n.get("status") not in ALLOWED_STATUSES:
            raise ViewError("Invalid snapshot task status")
        if not isinstance(n.get("needs"), list) or any(not isinstance(x,str) or not SAFE.fullmatch(x) for x in n["needs"]):
            raise ViewError("Invalid snapshot dependencies")
        if n.get("prompt") is not None and (not isinstance(n["prompt"],str) or len(n["prompt"])>18000):
            raise ViewError("Prompt too long for exact display")
    byid={n["id"]:n for n in nodes}
    visiting=set()
    visited=set()
    def visit(node):
        if node in visiting:raise ViewError("Cycle detected in snapshot at "+node)
        if node in visited:return
        visiting.add(node)
        for dep in byid[node]["needs"]:
            if dep not in byid:raise ViewError("Unknown snapshot dependency "+dep)
            visit(dep)
        visiting.remove(node)
        visited.add(node)
    for n in byid:
        visit(n)

def render(data: dict, html_template: str):
    validate_snapshot(data)
    if html_template.count(TOKEN) != 1:
        raise ViewError("Viewer template placeholder missing or duplicated")
    if len(data["nodes"]) > 240:
        raise ViewError("Too many diagram nodes")
    return html_template.replace(TOKEN, encode_json(data))

def save(html: str, dest: Path, snapshot: dict):
    dest = ensure_safe_output(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # atomic best effort, single-writer. No claim of durable crash atomicity.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=dest.parent,
                                      prefix=".view-", suffix=".html", delete=False) as stream:
        stream.write(html)
        tmp = Path(stream.name)
    try:
        os.replace(tmp, dest)
    finally:
        if tmp.exists():
            tmp.unlink()
    snap = dest.parent / "snapshot.json"
    if snap.is_symlink():
        raise ViewError("Refuse symlink snapshot path")
    snap.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--template",type=Path,help="source template.yaml")
    group.add_argument("--graph",type=Path,help="pinned graph-revisions/g*.yaml")
    group.add_argument("--snapshot",type=Path,help="prepared visualization snapshot.json")
    group.add_argument("--run-dir",type=Path,help="existing run folder, auto-loads pinned graph and verifies events")
    parser.add_argument("--state",type=Path,help="optional derived run state.json")
    parser.add_argument("--out",type=Path,help="agent-files/visualizations/<id>/index.html (automatic for --run-dir)")
    parser.add_argument("--unverified",action="store_true",help="skip event verification, label source as UNVERIFIED")
    parser.add_argument("--title",help="optional display title")
    args=parser.parse_args()
    try:
        if args.unverified and not args.run_dir:raise ViewError("--unverified applies only to --run-dir")
        if args.run_dir:
            data=run_dir_snapshot(args.run_dir,args.title,verify_events=not args.unverified)
        elif args.snapshot:
            if args.state:raise ViewError("--snapshot cannot be combined with --state")
            data=json.loads(args.snapshot.read_text(encoding="utf-8"))
        else:
            path=args.template or args.graph
            tpl=load_yaml(path)
            state=json.loads(args.state.read_text(encoding="utf-8")) if args.state else None
            data=source_to_snapshot(tpl,state,str(path),args.title)
            # Only master/template mode can securely load sibling child modules.
            # Pinned run revisions must never resolve changing template HEAD.
            if args.template:
                data=resolve_local_children(data,path)
        # Prepared v0.8 JSON remains compatible; generate advisory human-facing
        # labels/briefs without rewriting pinned canonical workflow sources.
        if any(not isinstance(n.get("human"), dict) for n in data.get("nodes",[])):
            data=add_human_profile(data)
        html=render(data,VIEWER.read_text(encoding="utf-8"))
        if args.out:
            destination=args.out
        elif args.run_dir:
            destination=args.run_dir.absolute().parents[3]/"visualizations"/(
                data["instance_id"]+"--"+data["run_id"]+"--"+data["graph_revision"])/"index.html"
        else:
            raise ViewError("--out required for template, graph and JSON snapshot inputs")
        location=save(html,destination,data)
        print(json.dumps({"result":"GENERATED_READ_ONLY","html":str(location),
                          "snapshot":str(location.parent/"snapshot.json"),
                          "nodes":len(data["nodes"]),"mode":data.get("mode"),
                          "verification":data.get("verification")}))
    except (ViewError,OSError,ValueError,TypeError) as exc:
        print("Visualize: "+str(exc),file=sys.stderr)
        raise SystemExit(2)
if __name__=="__main__":
    main()
