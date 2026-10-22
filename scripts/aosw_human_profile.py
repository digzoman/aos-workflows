"""AOS-W v0.9 human presentation profile: safe, non-authoritative projections.

A projection never edits graph IDs, checkpoint history, approval records or tools.
If the source graph lacks required information, it says that clearly while
encouraging resourceful completion using authorized alternatives.
"""
from __future__ import annotations
import re
from pathlib import Path

LANES = {
    "hvac-installation-owners": "HVAC business owners",
    "planned-general-trades": "General trades",
    "experienced-meta-marketers": "Experienced Meta advertisers",
    "agency-owners": "Agency owners",
    "licensed-life-insurance-agents": "Licensed life insurance agents",
    "general-smb-owners": "Small business owners",
}
PHASES = {
    "research": ("research", "Research competitors"),
    "qc-research": ("research-review", "Check the research"),
    "image-customize": ("creative", "Prepare ad creatives"),
    "qc-image": ("creative-review", "Review ad creatives"),
    "copy-message": ("ad-copy", "Write ad copy"),
    "qc-copy": ("copy-review", "Review ad copy"),
    "manager-setup": ("campaign-setup", "Prepare ad campaign"),
    "qc-setup": ("campaign-review", "Check campaign setup"),
}
WORDS = {"hvac": "HVAC", "smb": "small business", "qc": "quality", "meta": "Meta", "crm": "CRM",
         "ai": "AI", "ghl": "HighLevel", "ap": "accounts payable", "capi": "Conversions API"}
META_AD_LIBRARY = {
    "name": "Meta Ad Library",
    "url": "https://www.facebook.com/ads/library/",
    "purpose": "Inspect dated public Facebook and Instagram advertising examples",
    "status": "SUGGESTED_NOT_VERIFIED",
    "note": "An internal 'Ads Gallery' may be different; confirm its exact identity and access instead of assuming these services are identical."
}
RECOVERY = (
    "Use available connected tools, browser, approved skills or authorized alternate sources. "
    "Do not stop or invent a human gate after one failure; continue independent work. "
    "Record only a genuine unmet requirement after documenting attempted methods. "
    "Never fabricate evidence, independent review or provider authorization."
)

def words(value):
    tokens = re.sub(r"[_-]+", " ", str(value or "")).split()
    return " ".join(WORDS.get(t.lower(), t.lower()) for t in tokens)

def source_title(entry):
    # Explicit editorial titles have precedence over generated guesses.
    candidate = entry.get("title") or entry.get("name")
    if isinstance(candidate, str) and candidate.strip() and "--" not in candidate and not re.fullmatch(r"[a-z0-9_-]+", candidate.strip()):
        return candidate.strip()[:110], "AUTHOR_DEFINED"
    if isinstance(candidate, str) and " " in candidate and "--" not in candidate and len(candidate)<110:
        return candidate.strip(), "AUTHOR_DEFINED"
    node_id = entry.get("id", "")
    suffix = node_id.split("--")[-1]
    prefix = node_id.rsplit("--", 1)[0] if "--" in node_id else ""
    audience = LANES.get(prefix)
    target = audience or words(prefix)
    actions = {
        "research": "Research", "qc-research": "Review",
        "image-customize": "Prepare creative for", "qc-image": "Review images for",
        "copy-message": "Write ad copy for", "qc-copy": "Review ad copy for",
        "manager-setup": "Set up ads for", "qc-setup": "Check ad setup for"
    }
    if audience and suffix in actions:
        action = actions[suffix]
        subject = audience if audience.startswith(("HVAC","CRM","AI")) else audience[0].lower()+audience[1:] if audience else ""
        if suffix == "qc-research":return "Review "+subject+" research", "GENERATED_FROM_ID"
        if suffix == "research":return "Research ads for "+subject, "GENERATED_FROM_ID"
        if action.endswith("for"):return action+" "+subject, "GENERATED_FROM_ID"
        return action+" "+subject, "GENERATED_FROM_ID"
    if node_id.startswith("human-"):
        return "Approve "+words(node_id[6:]), "GENERATED_FROM_ID"
    if "launch" in node_id:
        return "Launch approved advertising" if "launch" in node_id else words(node_id).capitalize(), "GENERATED_FROM_ID"
    if entry.get("kind")=="review":
        return "Review "+words(suffix), "GENERATED_FROM_ID"
    title=words(node_id)
    return (title[0].upper()+title[1:] if title else "Unnamed workflow task"), "GENERATED_FROM_ID"

def lane_phase(entry):
    node_id = entry.get("id","")
    suffix = node_id.split("--")[-1]
    lane_id = entry.get("lane_id") or (node_id.rsplit("--",1)[0] if "--" in node_id else "shared")
    lane_title = entry.get("lane_title") or LANES.get(lane_id) or ("Shared campaign" if lane_id=="shared" else words(lane_id).capitalize())
    phase_id = entry.get("phase_id")
    phase_title = entry.get("phase_title")
    if not phase_id or not phase_title:
        phase = PHASES.get(suffix)
        if not phase:
            if entry.get("kind")=="approval":phase=("approvals","Owner approvals")
            elif "launch" in node_id:phase=("launch","Launch and verify")
            elif entry.get("kind")=="review":phase=("review","Quality review")
            elif "meta" in node_id or "adset" in node_id:phase=("campaign-setup","Prepare campaigns")
            elif "copy" in node_id:phase=("ad-copy","Write ad copy")
            else:phase=("preparation","Prepare workflow")
        phase_id = phase_id or phase[0]
        phase_title = phase_title or phase[1]
    return {"lane_id":lane_id,"lane_title":lane_title,"phase_id":phase_id,"phase_title":phase_title}

def resource_list(entry):
    resources=[]
    for raw in (entry.get("resources") or []):
        if isinstance(raw,dict):
            d={k:raw[k] for k in ("name","url","path","purpose","status","access","note") if k in raw}
            if d.get("name"):resources.append(d)
    text=(entry.get("instructions") or entry.get("prompt") or "").lower()
    node_id=entry.get("id","").lower()
    if ("research" in node_id or "competitor" in text or "ad library" in text) and not any(r.get("name")=="Meta Ad Library" for r in resources):
        resources.append(dict(META_AD_LIBRARY))
    if "ads gallery" in text and not any(r.get("name","").lower()=="ads gallery" for r in resources):
        resources.append({"name":"Ads Gallery", "status":"IDENTITY_UNVERIFIED",
                          "purpose":"Resolve the exact gallery named by the source instructions",
                          "note":"Check the original saved tool/source reference or connected apps; never invent a URL or silently conflate with Meta Ad Library."})
    return resources

def human_brief(entry, template=None, run=None):
    title,origin=source_title(entry)
    names=lane_phase(entry)
    prompt=entry.get("instructions") or entry.get("prompt") or ""
    policy=template.get("policy",{}) if isinstance(template,dict) else {}
    if not isinstance(policy,dict):policy={}
    capabilities=[]
    nid=entry.get("id","").lower()
    if "image" in nid or "creative" in nid:capabilities.append("inspect original image pixels and typography")
    if entry.get("kind")=="review" or "qc-" in nid:capabilities.append("independent review only if required by the saved quality gate")
    if "research" in nid:capabilities.append("access dated primary sources or truthfully labeled historical records")
    params=template.get("parameters",{}) if isinstance(template,dict) else {}
    source_refs={}
    if isinstance(params,dict):
        for key in ("source_research_portfolio","base_ad_copy_ref","portrait_ref","square_ref"):
            value=params.get(key)
            if isinstance(value,dict) and isinstance(value.get("default"),str):
                source_refs[key]=value["default"]
    context={"pinned_graph":run.get("graph_revision") if isinstance(run,dict) else None,
             "run_id":run.get("run_id") if isinstance(run,dict) else None,
             "workspace_or_template_source":run.get("source") if isinstance(run,dict) else None,
             "declared_source_refs":source_refs}
    summary=entry.get("summary") or title+"."
    resources=resource_list(entry)
    purpose=entry.get("purpose") or summary
    status=run.get("status") if isinstance(run,dict) else None
    if status == "READY" and entry.get("kind")=="review":next_action="Perform the saved quality review using an independent agent if required; record the exact-artifact verdict."
    elif status == "NEEDS_REWORK":next_action="Read the reviewer findings, correct the affected artifact and re-run required quality checks."
    elif status == "WAIT_DEPENDENCY":next_action="Continue independent authorized work; do not bypass unfinished predecessor checks."
    elif status == "WAIT_APPROVAL":next_action="Prepare the complete approval package and retain the existing owner authorization gate."
    elif status == "COMPLETE":next_action="Preserve completed evidence; inspect the next eligible dependent task."
    else:next_action="Use the saved procedure and inputs; check the current run before claiming this step."
    missing=[]
    if not prompt:missing.append("Original source step instructions are not recorded")
    if not entry.get("outputs") and not entry.get("contract"):missing.append("Expected output or completion contract not specified")
    # Advisory metadata must never add new approval restrictions.
    return {
        "title":title,"title_origin":origin,"summary":str(summary)[:500],
        "purpose":str(purpose)[:500],"phase":names["phase_title"],"phase_id":names["phase_id"],
        "lane":names["lane_title"],"lane_id":names["lane_id"],"next_action":next_action,
        "resources":resources,"inputs":entry.get("inputs") or [],
        "outputs":entry.get("outputs") or [],"source_context":context,
        "required_capabilities":capabilities,
        "allowed_actions":entry.get("required_actions") or policy.get("allowed_actions") or [],
        "human_required_actions_existing_policy":policy.get("human_required_actions") or [],
        "acceptance":entry.get("contract") or {},
        "quality":entry.get("quality") or {},
        "missing_references":missing,"recovery_guidance":RECOVERY,
        "source_status":"PINNED_INSTRUCTIONS_PROJECTION" if prompt else "INCOMPLETE_SOURCE",
        "original_instructions":prompt,
    }

def add_human_profile(data, template=None):
    nodes=data.get("nodes",[])
    if not isinstance(nodes,list):return data
    for n in nodes:
        original={"id":n.get("id"),"title":n.get("title"),"name":n.get("label"),
                  "kind":n.get("kind"),"instructions":n.get("prompt"),
                  "inputs":n.get("inputs"),"outputs":n.get("outputs"),"quality":n.get("quality"),
                  "contract":n.get("contract"),"required_actions":n.get("required_actions"),
                  "resources":n.get("resources"),"summary":n.get("summary"),"purpose":n.get("purpose"),
                  "phase_id":n.get("phase_id"),"phase_title":n.get("phase_title"),
                  "lane_id":n.get("lane_id"),"lane_title":n.get("lane_title")}
        run={"status":n.get("status"),"graph_revision":data.get("graph_revision"),
             "run_id":data.get("run_id"),"source":n.get("source_path") or n.get("source")}
        n["human"]=human_brief(original,template,run)
    return data
