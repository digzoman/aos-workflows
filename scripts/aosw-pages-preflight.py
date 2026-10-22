#!/usr/bin/env python3
"""Narrow v0.9 GitHub Pages safety check for an allowlisted FICTIONAL example.

This is not a general-purpose private data sanitizer or approval verifier.
Never feed a live customer, marketing workflow or agent-files directory here.
"""
import hashlib,json,re,sys
from pathlib import Path
class ExportError(ValueError):pass
CREDENTIALS=re.compile(r"(?i)(api[_-]?key\s*[:=]|bearer\s+\S+|password\s*[:=]|secret\s*[:=])")
def validate(snapshot,html):
    if snapshot.get("public_export") is not True:raise ExportError("Source not public-export")
    if snapshot.get("template_id")!="synthetic-v09-six-lane" or snapshot.get("run_id")!="example-not-production":
        raise ExportError("Only the public fictional demo is permitted")
    if not str(snapshot.get("warning","")).startswith("Fictional synthetic example"):
        raise ExportError("Fictional disclaimer missing")
    if snapshot.get("mode")!="RUN" or len(snapshot.get("nodes",[]))!=56:
        raise ExportError("Incorrect public fixture")
    if "__AOSW_SNAPSHOT_JSON__" in html:raise ExportError("Unrendered HTML")
    if CREDENTIALS.search(html) or CREDENTIALS.search(json.dumps(snapshot)):
        raise ExportError("Potential credential")
    return True
def main():
    if len(sys.argv)!=4:raise SystemExit("usage: preflight snapshot.json index.html public/index.html")
    source=Path(sys.argv[1]);src=Path(sys.argv[2]);dest=Path(sys.argv[3])
    payload=json.loads(source.read_text(encoding="utf-8"));html=src.read_text(encoding="utf-8")
    validate(payload,html)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html,encoding="utf-8")
    print(json.dumps({"result":"ALLOWLISTED_FICTIONAL_HTML","html":str(dest),"sha256":hashlib.sha256(html.encode()).hexdigest()}))
if __name__=="__main__":
    try:main()
    except (ExportError,ValueError,OSError) as exc:
        print("REJECTED: "+str(exc),file=sys.stderr);raise SystemExit(2)
