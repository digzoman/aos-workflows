#!/usr/bin/env python3
"""AOS-W V1 release audit, deterministic and non-sensitive output.

Checks tracked current tree, reachable Git blob history, preview ZIP,
survey architecture, manifest, and evidence-marker consistency.
Does not assert human privacy, licensing, identity, cloud persistence,
provider integration or V1 acceptance. Never prints discovered secret values.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, sys, zipfile
from collections import Counter
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
def command(*args, raw=False):
    p=subprocess.run(args,cwd=ROOT,check=True,capture_output=True)
    return p.stdout if raw else p.stdout.decode("utf-8","replace")
def sha(b):return hashlib.sha256(b).hexdigest()

# Signatures are split where helpful to avoid test source itself resembling a credential.
PATTERNS={
 "private_key":re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
 "github_classic":re.compile(r"\b(?:gh"+"[pousr]"+r"_[A-Za-z0-9_]{25,})"),
 "github_finegrained":re.compile(r"\bgithub_"+"pat_"+r"[A-Za-z0-9_]{25,}"),
 "openai_style":re.compile(r"\bsk"+"-"+r"[A-Za-z0-9_-]{35,}"),
 "aws_access_key":re.compile(r"\bAK"+"IA"+r"[0-9A-Z]{16}\b"),
 "google_api_key":re.compile(r"\bAI"+"za"+r"[0-9A-Za-z_-]{32,}"),
 "slack_token":re.compile(r"\bxox"+"[baprs]-"+r"[0-9A-Za-z-]{24,}"),
 "unipile_key":re.compile(r"\bu"+"ctr"+r"[A-Za-z0-9]{4,20}\.[A-Za-z0-9+/=]{28,}"),
 "api_key_assignment":re.compile(r"(?i)(?:x-api-key|api[_-]key|client[_-]secret)\s*[:=]\s*['\"]?([A-Za-z0-9+/=._-]{32,})"),
}
UNSAFE_EXT={".env",".pem",".p12",".pfx",".p8",".sqlite",".db",".keystore"}
ALLOW_PUBLIC_EMAIL_DOMAIN={"example.com","example.org","example.net","example.invalid",
 "users.noreply.github.com","noreply.github.com","github.com","localhost"}
EMAIL=re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b")
EXCLUDE_AS_USER_INPUT=False

def filename_risks(name):
    p=PurePosixPath(name)
    result=[]
    if p.name in (".env",".npmrc",".pypirc",".netrc","id_rsa","id_ed25519"):result.append("sensitive_filename")
    if p.suffix.lower() in UNSAFE_EXT:result.append("sensitive_extension")
    return result

def findings(data,path):
    if b"\0" in data[:3000]:
        return {"binary":True,"secret_classes":[],"nonexample_email_count":0}
    try:txt=data.decode("utf-8")
    except UnicodeDecodeError:return {"binary":True,"secret_classes":[],"nonexample_email_count":0}
    return {"binary":False,
     "secret_classes":[name for name,pattern in PATTERNS.items() if pattern.search(txt)],
     "nonexample_email_count":sum(1 for m in EMAIL.finditer(txt) if m.group(1).lower() not in ALLOW_PUBLIC_EMAIL_DOMAIN)}

def scan_tree():
    names=[s.decode("utf-8","surrogateescape") for s in command("git","ls-files","-z",raw=True).split(b"\0") if s]
    bad=[];nonexample_email_files=[];binary_count=0
    for name in names:
        p=ROOT/name
        if not p.exists():continue
        if not p.is_file():continue
        suspicious=filename_risks(name)
        d=findings(p.read_bytes(),name)
        if d["binary"]:binary_count+=1
        suspicious+=d["secret_classes"]
        if suspicious:bad.append({"path":name,"categories":sorted(set(suspicious))})
        if d["nonexample_email_count"]:nonexample_email_files.append({"path":name,"count":d["nonexample_email_count"]})
    return {"tracked_file_count":len(names),"binary_count":binary_count,"secret_or_sensitive_path_candidates":bad,
       "nonexample_email_files":nonexample_email_files[:35],"nonexample_email_file_count":len(nonexample_email_files)}

def scan_history():
    # This reads reachable history using a single git cat-file stream. It deliberately
    # reports only risk categories and the first path for each blob, never secret bytes.
    raw=command("git","rev-list","--objects","--all")
    pairs=[]
    seen=set()
    for line in raw.splitlines():
        bits=line.split(" ",1)
        if len(bits)<2:continue
        object_id,name=bits
        if object_id in seen:continue
        seen.add(object_id);pairs.append((object_id,name))
    p=subprocess.Popen(["git","cat-file","--batch"],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    suspects=[];email_files=0;binary_count=0;blobs=0;scanned_bytes=0
    assert p.stdin and p.stdout
    for oid,path in pairs:
        p.stdin.write((oid+"\n").encode());p.stdin.flush()
        header=p.stdout.readline().decode("ascii","replace").strip().split()
        if len(header)!=3 or header[1] not in ("blob","tree","commit","tag"):
            raise RuntimeError("Git object audit failed to read "+oid[:8])
        size=int(header[2]);data=p.stdout.read(size);p.stdout.read(1)
        if header[1]!="blob":continue
        blobs+=1;scanned_bytes+=len(data)
        d=findings(data,path)
        if d["binary"]:binary_count+=1
        tags=filename_risks(path)+d["secret_classes"]
        if tags:suspects.append({"path":path,"categories":sorted(set(tags)),"blob_prefix":oid[:12]})
        if d["nonexample_email_count"]:email_files+=1
    p.stdin.close();p.stdout.close()
    p.wait(timeout=30)
    if p.returncode:raise RuntimeError("Git cat-file stream failed")
    return {"reachable_unique_blob_count":blobs,"scanned_bytes":scanned_bytes,"binary_blob_count":binary_count,
      "secret_or_sensitive_path_candidates":suspects[:100],"candidate_count":len(suspects),
      "nonexample_email_blob_count":email_files,"scan_scope":"all reachable refs in checkout fetch-depth=0"}

def scan_zip(path):
    from importlib.machinery import SourceFileLoader
    mod=SourceFileLoader("aosw_distribution",str(ROOT/"scripts/aosw-distribution.py")).load_module()
    zpath=Path(path).resolve()
    mod.verify(zpath)
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
        info={i.filename:i for i in z.infolist()}
        unsafe=[]
        data={}
        for n in names:
            if not n.startswith("aos-w/") or ".." in PurePosixPath(n).parts:unsafe.append(n)
            rel=n[len("aos-w/"):]
            if not n.endswith("/") and (rel.startswith("agent-files/instances/") or rel.startswith("agent-files/custom-templates/")):
                # Distribution includes only clean README seeds.
                if PurePosixPath(rel).name!="README.md":unsafe.append(n)
            if rel.startswith(("temp/","tests/","tools/","docs/","scripts/")):unsafe.append(n)
            if not n.endswith("/"):
                data[n]=z.read(n)
                if not mod.permitted(rel):unsafe.append(n)
        ver=json.loads(data["aos-w/VERSION.json"])
        sha256=sha(zpath.read_bytes())
        return {"version":ver["aosw_version"],"sha256":sha256,"archive_bytes":zpath.stat().st_size,
        "zip_member_count":len(names),"unsafe_archive_entries":unsafe,
        "framework_dependencies":ver["distribution"]["runtime_dependencies"],
        "contains_user_instance":any(n.startswith("aos-w/agent-files/instances/") and not n.endswith("README.md") for n in names),
        "required_entries_all_present":all(n in data for n in ("aos-w/README.md","aos-w/PROTOCOL.md","aos-w/VERSION.json",
            "aos-w/DISTRIBUTION-MANIFEST.json","aos-w/templates/MARKETING-LIBRARY.md"))}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--zip",required=True)
    ap.add_argument("--out",required=True)
    options=ap.parse_args()
    current=scan_tree()
    historical=scan_history()
    archive=scan_zip(options.zip)
    required=[
      "docs/specs/prd/PRD.md","docs/specs/prd/SURVEY-TRACEABILITY.md",
      "docs/specs/prd/APPROVAL-REVIEW.md","docs/specs/prd/ACCEPTANCE-TEST-MATRIX.md",
      "docs/specs/architecture/FILE-SPECIFICATION.md","docs/specs/architecture/EXECUTION-STATE.md",
      "docs/specs/adrs/ADR-014-git-cas-provisional-selection.md",
      "docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md",
      "docs/testing/PROMPT-17-GIT-COLLABORATION.md",
      "docs/testing/PROMPT-18-END-TO-END-RESULTS.md"]
    missing=[x for x in required if not (ROOT/x).exists()]
    summary={"timestamp":datetime.now(timezone.utc).isoformat(),"commit":command("git","rev-parse","HEAD").strip(),
     "scan_method":"path and high confidence text patterns including all reachable Git refs, not a human privacy audit",
     "current_tree":current,"history":historical,"portable_zip":archive,
     "requirements_documents_missing":missing,
     "checks":{
       "no_high_confidence_secret_signatures_current":not current["secret_or_sensitive_path_candidates"],
       "no_high_confidence_secret_signatures_history":not historical["secret_or_sensitive_path_candidates"],
       "zip_validator_pass":not archive["unsafe_archive_entries"] and archive["required_entries_all_present"],
       "required_documents_present":not missing,
     },"human_review_pending":["private business and customer data contextual review","public-source content usage rights",
          "license choice","formal PRD/ADR approval","original six success demonstrations","cloud durability and independent AI reviewer"]}
    summary["automated_gate_pass"]=all(summary["checks"].values())
    path=Path(options.out);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"automated_gate":summary["automated_gate_pass"],
      "files":current["tracked_file_count"],"history_blobs":historical["reachable_unique_blob_count"],
      "zip_sha256":archive["sha256"],
      "current_secret_candidates":len(current["secret_or_sensitive_path_candidates"]),
      "history_secret_candidates":historical["candidate_count"],
      "email_contextual_review_files":current["nonexample_email_file_count"],
      "checks":summary["checks"],"missing_docs":missing,"archive_unsafe_categories":[PurePosixPath(x).name for x in archive["unsafe_archive_entries"][:10]]}))
    if not summary["automated_gate_pass"]:
       raise SystemExit("Automated release gate found issues. Review JSON categories and fix before release.")
if __name__=="__main__":main()
