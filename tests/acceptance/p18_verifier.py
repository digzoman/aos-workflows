#!/usr/bin/env python3
"""Independent-process, deterministic P18 evidence verifier. Not an AI reviewer."""
import argparse,hashlib,json,os
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser()
p.add_argument("--kind",choices=["research","creative"],required=True)
p.add_argument("--input",required=True)
p.add_argument("--meta")
args=p.parse_args()
f=Path(args.input)
fail=[]
if args.kind=="research":
    evidence=json.loads(f.read_text())
    rows=evidence.get("evidence",[])
    if len(rows)<2: fail.append("insufficient_sources")
    for row in rows:
        if not row.get("url"): fail.append("missing_url")
        if not row.get("observed"): fail.append("missing_observation")
        if not row.get("seller"): fail.append("missing_seller")
    if evidence.get("evidence_class")!="FIRST_PARTY_OFFER_PAGES_NOT_AD_CARDS":
        fail.append("source_kind_unverified")
else:
    meta=json.loads(Path(args.meta).read_text())
    with Image.open(f) as image:
        if image.size != (1080,1350): fail.append("wrong_size")
        if image.mode not in ("RGB","RGBA"): fail.append("wrong_color_mode")
    if meta.get("cta")!="SEND MESSAGE": fail.append("missing_correct_CTA")
    if meta.get("safe_margin_px",0)<54: fail.append("insufficient_margin")
    if meta.get("seller_logo")!="UNVERIFIED_TEXT_PLACEHOLDER": fail.append("logo_provenance")
    if meta.get("price_state")!="PROVISIONAL_REQUIRES_OWNER_REVIEW": fail.append("unverified_price")
print(json.dumps({"decision":"REVISE" if fail else "PASS","issues":fail,"method":"independent_process_rules","pid":os.getpid(),"sha256":hashlib.sha256(f.read_bytes()).hexdigest()}))
