#!/usr/bin/env python3
"""AOS-W P18, grounded-source, staged-only, three-child Bucket 9 execution.
Uses real public supplier page observations from a dated curated evidence input.
Neither actual Meta ad cards nor independent AI model or provider operations are claimed.
"""
import argparse,hashlib,json,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime, timezone
import yaml
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"tools/state"))
from state import RunStore
PRODUCER={"agent":"AmpgentResearch","platform":"github-actions","role":"producer","instance":"p18-a"}
PEER={"agent":"IndependentQC","platform":"separate-process","role":"reviewer","instance":"p18-b"}
RECOVERY={"agent":"ColdResume","platform":"file-replay","role":"worker","instance":"p18-c"}
EVENTS=[]
def check(name,ok):
    EVENTS.append({"case":name,"status":"PASS" if ok else "FAIL"})
    if not ok: raise AssertionError(name)
def hashfile(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def node(n,deps=(),qc=False,ext="md"):
    return {"id":n,"kind":"task","needs":list(deps),"instructions":"No external writes or account effects",
      "inputs":[],"outputs":[{"artifact_id":n+"-record","path":"artifacts/"+n+"."+ext,"required":True}],
      "quality":{"gates":["independent-check"] if qc else []},
      "contract":{"done_when":"Exact-hash artifact and scoped QC verified"},
      "required_actions":["read","write_local"]}
def new_run(instances,name,graph):
    i=instances/name
    (i/"graph-revisions").mkdir(parents=True,exist_ok=True)
    (i/"graph-revisions/g0001.yaml").write_text(yaml.safe_dump({"graph":graph}))
    return RunStore.create(i/"runs/run-001",graph,"run-001",PRODUCER)
def artifact(store,task,body,ext="md",version="v1"):
    p=store.root/"artifacts"/(task+"."+ext)
    p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(body,str): p.write_text(body)
    else:p.write_text(json.dumps(body,indent=2)+"\n")
    return [{"artifact_id":task+"-record","locator":"artifacts/"+task+"."+ext,"sha256":hashfile(p),"revision":version}]
def peer(kind,p,meta=None):
    command=[sys.executable,str(ROOT/"tests/acceptance/p18_verifier.py"),"--kind",kind,"--input",str(p)]
    if meta:command+=["--meta",str(meta)]
    proc=subprocess.run(command,capture_output=True,text=True,check=True)
    return json.loads(proc.stdout)
def accepted(store,task,refs,result,actor=PRODUCER):
    check(task+"-independent-gate",result["decision"]=="PASS" and result["sha256"]==refs[0]["sha256"])
    store.append("task_submitted_review",actor,task)
    store.append("review_accepted",PEER,task,payload={"verdict":"PASS","review_id":"p18-"+task+"-accepted",
     "artifacts":refs,"rubric_version":"p18-website-and-pixel-v1",
     "reviewer_kind":"separate_deterministic_process","review_pid":result["pid"]})
    store.complete(task,actor,refs)
def revise(store,task,old,new,result):
    check(task+"-reject-first",result["decision"]=="REVISE")
    store.append("task_submitted_review",PRODUCER,task)
    store.append("review_revise",PEER,task,payload={"verdict":"REVISE","review_id":"p18-"+task+"-rejected",
     "artifacts":old,"correction":",".join(result["issues"]),
     "retry":{"eligible":True,"next_eligible_at":None,"max_attempts":2,
       "attempts":1,"error_class":"review_revise","manual_approval_required":True}})
    check(task+"-blocked",store.verified()["tasks"][task]["status"]=="NEEDS_REWORK")
    store.retry(task,RECOVERY,approval=True)
    store.start(task,RECOVERY)
    return new
def finish(store,task,body):
    store.start(task,PRODUCER)
    refs=artifact(store,task,body)
    store.complete(task,PRODUCER,refs)
    store.checkpoint(PRODUCER)
def typeface(size,bold=False):
    f=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-"+("Bold" if bold else "Book")+".ttf")
    return ImageFont.truetype(str(f),size) if f.exists() else ImageFont.load_default()
def creative(path,with_cta):
    im=Image.new("RGB",(1080,1350),"#F7F5F1")
    d=ImageDraw.Draw(im)
    navy="#102D40";teal="#006D8F"
    d.text((76,80),"AMPGENT",fill=navy,font=typeface(37,True))
    d.text((76,220),"CREATE AD",fill=navy,font=typeface(93,True))
    d.text((76,330),"CREATIVES &",fill=navy,font=typeface(77,True))
    d.text((76,440),"CAMPAIGNS",fill=teal,font=typeface(90,True))
    d.text((76,550),"WITH AI",fill=teal,font=typeface(91,True))
    d.rounded_rectangle((76,715,1004,868),radius=40,fill=navy)
    d.text((112,754),"$47 STARTER TOOLKIT",fill="white",font=typeface(49,True))
    d.text((76,919),"For coaches and consultants",fill=navy,font=typeface(42,True))
    d.text((76,1009),"Plan. Create. Prepare.",fill=navy,font=typeface(43))
    if with_cta:
        d.rounded_rectangle((76,1133,1004,1241),radius=44,fill=teal)
        d.text((288,1157),"SEND MESSAGE",fill="white",font=typeface(49,True))
    im.save(path,optimize=True)
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    out=Path(args.out)
    check("fresh-output",not out.exists())
    out.mkdir(parents=True)
    data=json.loads((ROOT/"examples/conformance/marketing/p18-public-sources-20261020.json").read_text())
    check("three-research-children",len(data["segments"])==3)
    check("marketing-v07-present",(ROOT/"scaffold/aos-w/templates/marketing-lifecycle-compound/template.yaml").is_file())
    instances=out/"aos-w/agent-files/instances"
    parent_graph={"nodes":[node("plan"),node("fanout",["plan"]),node("synthesis",["fanout"]),
       node("offer",["synthesis"]),node("copy",["offer"]),node("creative",["copy"],True,"png"),
       node("crm",["offer"]),node("landing",["offer"]),node("tracking",["crm","landing"]),
       node("prelaunch",["creative","tracking"]),node("launch-permit",["prelaunch"])]}
    p=new_run(instances,"b9-parent",parent_graph)
    finish(p,"plan","# B9 research plan\nThree authorized research-only audience children, date 2026-10-20.\nNo provider changes. No unverified Meta ads.")
    manifest={"approved_scope":"research_only","template":"marketing-competitor-execution@0.7.0",
      "children":[{"run":s["id"],"buyer":s["buyer"]} for s in data["segments"]]}
    finish(p,"fanout","# Approved research proposals\n"+json.dumps(manifest,indent=2))
    children={}
    def all_reviewed(children):
        if len(children)!=len(data["segments"]): return False
        for run in children.values():
            v=run.verified()
            t=v["tasks"]["collect"]
            if t["status"]!="COMPLETE" or not t["review"] or t["review"]["verdict"]!="PASS":
                return False
            art=t["evidence"][0]
            if art["sha256"]!=hashfile(run.root/art["locator"]): return False
        return True
    check("join-blocked-before-child-reviews",not all_reviewed(children))
    for segment in data["segments"]:
        child=new_run(instances,"research-"+segment["id"],{"nodes":[node("collect",(),True,"json")]})
        children[segment["id"]]=child
        child.start("collect",PRODUCER)
        record={"buyer":segment["buyer"],"evidence":segment["evidence"],
            "evidence_class":"FIRST_PARTY_OFFER_PAGES_NOT_AD_CARDS","hypothesis":segment["hypothesis"]}
        if segment["id"]=="coaches":
            incomplete=json.loads(json.dumps(record))
            incomplete["evidence"][0].pop("url")
            before=artifact(child,"collect",incomplete,"json")
            fail=peer("research",child.root/"artifacts/collect.json")
            check("failed-child-not-accepted-for-synthesis",child.verified()["tasks"]["collect"]["status"]=="RUNNING")
            archived=child.root/"artifacts/collect-rejected-v1.json"
            shutil.copy2(child.root/"artifacts/collect.json",archived)
            check("failed-source-version-archived",hashfile(archived)==before[0]["sha256"])
            after_record=record
            # Correct the exact failing file and re-submit as revision v2.
            after=artifact(child,"collect",after_record,"json","v2")
            revise(child,"collect",before,after,fail)
            good=peer("research",child.root/"artifacts/collect.json")
            accepted(child,"collect",after,good,RECOVERY)
        else:
            refs=artifact(child,"collect",record,"json")
            accepted(child,"collect",refs,peer("research",child.root/"artifacts/collect.json"))
        child.checkpoint(PEER)
        child.handoff(PEER)
    check("all-child-runs-complete",all(x.verified()["run_status"]=="COMPLETED" for x in children.values()))
    check("join-allowed-only-on-reviewed-hashes",all_reviewed(children))
    evidence=[]
    for name,child in children.items():
        task=child.verified()["tasks"]["collect"]
        ref=task["evidence"][0]
        check(name+"-exact-hash",ref["sha256"]==hashfile(child.root/ref["locator"]))
        check(name+"-reviewed",task["review"]["verdict"]=="PASS")
        evidence.append({"child":name,"sha256":ref["sha256"],"review":task["review"]["review_id"]})
    # Manual cross-run join enforcement. Core graph READY is only an advisory
    # listing; this gate must be evaluated before synthesis.
    analysis=(
       "# Bucket 9 competitor evaluation, public websites as of 2026-10-20\\n\\n"
       "Coaches and consultants. Tadka advertises a self-serve creative system, "
       "Oak Marketing an AI assisted ads framework and The Ads Girl consulting and managed ads. "
       "This is the most direct pilot buyer for a beginner toolkit, but actual demand is unmeasured.\\n\\n"
       "Agency owners. Madgicx and AdCreative.ai sell established tools. "
       "Likely higher operator literacy and repeat volume, but the toolkit needs clear differentiation and workflow integration.\\n\\n"
       "Remodelers. V Easy, Syntex and NorthVale primarily offer done-for-you lead generation. "
       "High-value inquiries and available imagery are attractive, but a self-managed 47 dollar toolkit has unproven fit.\\n\\n"
       "Ranking is a test hypothesis, not statistical scoring. Evidence confidence is low to moderate. "
       "Eight first party supplier webpages were observed, zero active Meta ad cards were verified. "
       "Business results and independent customer demand are not proven.\\n"
    )
    (out/"OPPORTUNITY-EVALUATION.md").write_text(analysis)
    finish(p,"synthesis","# Accepted exact-hash child research\\n"+json.dumps(evidence,indent=2)+
      "\\n"+analysis)
    finish(p,"offer","# Ampgent proposed offer\n$47 AI starter toolkit from historical Bucket 9 concept.\nHypothesis only, deliverability and current price not owner reverified.")
    finish(p,"copy","# PROPOSED B9 C01 COPY\nPrimary. Put AI to work on your Facebook and Instagram ad creatives and campaign planning. Explore our guided toolkit for coaches and consultants. Message us for details.\nHeadline. AI Ad Creatives and Campaigns\nDescription. Plan and create with AI\nCTA. SEND MESSAGE.")
    p.start("crm",PRODUCER)
    p.start("landing",PRODUCER)
    p.checkpoint(PRODUCER)
    p.handoff(PRODUCER)
    p=RunStore(instances/"b9-parent/runs/run-001")
    check("cold-replay-parallel-branches",{"crm","landing"}.issubset(set(p.verified()["active_steps"])))
    for k,body in [("crm","# CRM MOCK PLAN\nHighLevel message routing, bot questions and Good Lead event unverified."),
                    ("landing","# LANDING MOCK PLAN\nOffer page, consent and messaging destination not deployed.")]:
        rr=artifact(p,k,body)
        p.complete(k,RECOVERY,rr)
    finish(p,"tracking","# TRACKING MOCK PLAN\nPixel, server-side CAPI, booking and Good Lead dedup not verified.")
    p.start("creative",PRODUCER)
    artwork=p.root/"artifacts/creative.png"
    artwork.parent.mkdir(parents=True,exist_ok=True)
    meta=artwork.with_suffix(".json")
    creative(artwork,False)
    meta.write_text(json.dumps({"safe_margin_px":76,"seller_logo":"UNVERIFIED_TEXT_PLACEHOLDER",
      "price_state":"PROVISIONAL_REQUIRES_OWNER_REVIEW"}))
    old=[{"artifact_id":"creative-record","locator":"artifacts/creative.png","sha256":hashfile(artwork),"revision":"v1"}]
    failed=peer("creative",artwork,meta)
    rejected_image=artwork.parent/"creative-rejected-v1.png"
    shutil.copy2(artwork,rejected_image)
    check("failed-creative-version-archived",hashfile(rejected_image)==old[0]["sha256"])
    creative(artwork,True)
    meta.write_text(json.dumps({"cta":"SEND MESSAGE","safe_margin_px":76,
      "seller_logo":"UNVERIFIED_TEXT_PLACEHOLDER","price_state":"PROVISIONAL_REQUIRES_OWNER_REVIEW"}))
    new=[{"artifact_id":"creative-record","locator":"artifacts/creative.png","sha256":hashfile(artwork),"revision":"v2"}]
    revise(p,"creative",old,new,failed)
    accepted(p,"creative",new,peer("creative",artwork,meta),RECOVERY)
    check("corrected-creative-digest-different",old[0]["sha256"]!=new[0]["sha256"])
    check("rejected-creative-remains-replayable",(artwork.parent/"creative-rejected-v1.png").is_file())
    finish(p,"prelaunch","# STAGED META AND CRM IMPLEMENTATION PACKAGE\nCampaign, ad set and ad objects not created. No budget active.\nUS/Canada ex Quebec proposed targeting requires confirmation.\nHighLevel/landing/CAPI/Good Lead provider state UNKNOWN.\nLogo and commercial offer require owner review.\nLaunch owner authorization NOT_GRANTED.")
    p.checkpoint(RECOVERY)
    p.handoff(RECOVERY)
    state=p.verified()
    check("final-live-approval-blocked",state["tasks"]["launch-permit"]["status"]!="COMPLETE")
    (out/"STAGED-IMPLEMENTATION.md").write_text("# Bucket 9 C01 staged campaign\n\n"+
      "Proposed Meta campaign with messages objective, coaches and consultants, US and Canada excluding Quebec, initial budget NOT AUTHORIZED.\n"+
      "Draft caption and ad creative at aos-w/agent-files/instances/b9-parent/runs/run-001/artifacts.\n"+
      "Campaign, ad set, ad, messaging, landing, pixel and CRM NOT CREATED or verified in provider.\n"+
      "Marketing claims and 47 dollar price require owner confirmation. Official Ampgent logo not sourced.\n"+
      "Final approval NO. External accounts UNTOUCHED.\n")
    summary={"as_of":datetime.now(timezone.utc).isoformat(),"checks":EVENTS,
      "total_checks":len(EVENTS),"parent_events":state["last_event_seq"],
      "child_events":{k:v.verified()["last_event_seq"] for k,v in children.items()},
      "sources":sum(len(s["evidence"]) for s in data["segments"]),
      "source_truth":"first_party_site_offers_not_verified_ad_cards","creative_sha256":hashfile(artwork),
      "QA":"separate_process_deterministic_not_AI","launch":"NOT_GRANTED",
      "real_meta_crm_effects":"NONE","conversion_readback":"NOT_RUN",
      "authentic_ai_creative_review":"NOT_RUN","manual_time_comparison":"NOT_MEASURED",
      "v1_T01":"PARTIAL_PUBLIC_EVIDENCE_STAGED_LOCAL"}
    (out/"SUMMARY.json").write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"result":"PASS_STAGED_SOURCE_GROUNDED","checks":len(EVENTS),
      "parent_events":state["last_event_seq"],"child_runs":len(children),"sources":summary["sources"],
      "launch":summary["launch"]}))
if __name__=="__main__":main()
