#!/usr/bin/env python3
"""Advisory Agent Skills conformance checker. Never gates agent task execution.

Checks name/description YAML frontmatter and local safe paths; reports repairs
without changing user-owned skill contents or inventing approvals.
No external dependencies or network needed.
"""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
NAME=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_SKILLS=600

def analyze(path:Path,root:Path):
    issues=[]
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        return {"path":str(path),"status":"UNSAFE_PATH","issues":["Outside safe local skill root or symlink"]}
    text=path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        issues.append("Missing YAML frontmatter opening marker")
        head=""
    else:
        match=re.search(r"(?m)^---\s*$",text[4:])
        if match is None:
            issues.append("Missing YAML frontmatter closing marker");head=""
        else:head=text[4:4+match.start()]
    attrs={}
    for line in head.splitlines():
        if not line.strip() or line.startswith((" ","\t","#")):continue
        if ":" not in line:
            issues.append("Invalid frontmatter line");continue
        k,v=line.split(":",1)
        attrs[k.strip()]=v.strip().strip('"').strip("'")
    name=attrs.get("name","")
    description=attrs.get("description","")
    if not NAME.fullmatch(name):issues.append("name must use lower-case hyphenated slug")
    if name!=path.parent.name:issues.append("name must match parent skill directory")
    if not description:issues.append("description is required")
    if len(description)>1024:issues.append("description exceeds 1024 characters")
    if not text[4:].strip():issues.append("Empty skill body")
    if not path.name=="SKILL.md":issues.append("Expected SKILL.md")
    return {"path":str(path.relative_to(root)),"name":name,
            "status":"REVIEW_RECOMMENDED" if issues else "CONFORMS",
            "issues":issues,"action":"Improve skill metadata using an authorized framework/skill edit; do not block unrelated agent tasks." if issues else "Use normally within existing permissions."}

def scan(root:Path):
    root=root.resolve()
    if not root.is_dir():raise ValueError("Missing skill root")
    paths=sorted(root.rglob("SKILL.md"))
    if len(paths)>MAX_SKILLS:raise ValueError("Too many skill files")
    result=[analyze(p,root) for p in paths]
    return {"result":"ADVISORY_NON_GATING",
            "total":len(result),"conformant":sum(x["status"]=="CONFORMS" for x in result),
            "review_recommended":sum(x["status"]!="CONFORMS" for x in result),
            "skills":result}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("root",type=Path)
    args=p.parse_args()
    try:print(json.dumps(scan(args.root),indent=2))
    except (OSError,ValueError) as err:print(str(err),file=sys.stderr);raise SystemExit(2)
if __name__=="__main__":main()
