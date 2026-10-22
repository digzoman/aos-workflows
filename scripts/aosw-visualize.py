#!/usr/bin/env python3
"""Optional AOS-W 0.8 self-contained offline workflow visualizer.

Agent-only/manual use requires no Python. This convenience renderer reads the
original YAML template or a pinned graph and optional derived run state, then
writes a READ-ONLY standalone HTML snapshot under agent-files/visualizations.
Never uploads to GitHub Pages, never edits workflow state or authorizations.
"""
from __future__ import annotations
import argparse, json, os, re, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

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
        nodes.append({
            "id": node_id,
            "label": sanitized_text(entry.get("name") or entry.get("title") or node_id, 180),
            "kind": sanitized_text(entry.get("kind"), 70),
            "needs": sanitized_text(entry.get("needs", [])),
            "status": status,
            "prompt": sanitized_text(entry.get("instructions") or entry.get("prompt"), 16000),
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
            "source": "Pinned graph source, not current mutable master" if mode != "TEMPLATE" else "Published template definition"
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
    return {
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

def encode_json(data):
    # This embedding never executes untrusted labels as HTML, JS, or a URL.
    return (json.dumps(data, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
            .replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("&", "\\u0026").replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))

def render(data: dict, html_template: str):
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
        raise ViewError("Snapshot requires nodes array")
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
    parser.add_argument("--state",type=Path,help="optional derived run state.json")
    parser.add_argument("--out",required=True,type=Path,help="agent-files/visualizations/<id>/index.html")
    parser.add_argument("--title",help="optional display title")
    args=parser.parse_args()
    try:
        if args.snapshot:
            if args.state:raise ViewError("--snapshot cannot be combined with --state")
            data=json.loads(args.snapshot.read_text(encoding="utf-8"))
        else:
            path=args.template or args.graph
            tpl=load_yaml(path)
            state=json.loads(args.state.read_text(encoding="utf-8")) if args.state else None
            data=source_to_snapshot(tpl,state,str(path),args.title)
        html=render(data,VIEWER.read_text(encoding="utf-8"))
        location=save(html,args.out,data)
        print(json.dumps({"result":"GENERATED_READ_ONLY","html":str(location),
                          "snapshot":str(location.parent/"snapshot.json"),
                          "nodes":len(data["nodes"]),"mode":data.get("mode"),
                          "verification":data.get("verification")}))
    except (ViewError,OSError,ValueError,TypeError) as exc:
        print("Visualize: "+str(exc),file=sys.stderr)
        raise SystemExit(2)
if __name__=="__main__":
    main()
