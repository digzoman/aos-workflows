#!/usr/bin/env python3
"""Controlled Prompt 18 pilot. Real file events, MOCK research and deterministic QC only."""
import argparse,hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
import yaml
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/"tools/state"))
from state import RunStore
A={"agent":"P18Worker","platform":"local-actions","role":"worker","instance":"p18-a"}
B={"agent":"P18Reviewer","platform":"local-actions","role":"mock-reviewer","instance":"p18-b"}
C={"agent":"P18Resumer","platform":"local-fresh-store","role":"worker","instance":"p18-c"}
def node(name,deps=(),review=False,ext="md"):
 return {"id":name,"kind":"task","needs":list(deps),"inputs":[],"instructions":"Sanitized mock, no provider effects",
 "outputs":[{"artifact_id":name+"-output","path":"artifacts/"+name+"."+ext,"required":True}],
 "quality":{"gates":["mock-independent-review"] if review else []},
 "contract":{"done_when":"Exact artifact digest checked"},
 "required_actions":["read","write_local"]}
def write(store,task,body,ext="md",rev="v1"):
 p=store.root/"artifacts"/(task+"."+ext);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
 return [{"artifact_id":task+"-output","locator":"artifacts/"+task+"."+ext,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"revision":rev}]
def pass_review(s,task,refs,actor=A):
 s.append("task_submitted_review",actor,task)
 s.append("review_accepted",B,task,payload={"verdict":"PASS","review_id":"p18-pass-"+task,"artifacts":refs,
 "rubric_version":"synthetic-qa-v1","reviewer_kind":"deterministic-test","subject":"MOCK only"})
def done(s,task,body,review=False,ext="md"):
 s.start(task,A)
 ref=write(s,task,body,ext)
 if review:pass_review(s,task,ref)
 s.complete(task,A,ref)
def bad_then_repair(s,task,bad,good,ext="md"):
 s.start(task,A);ref=write(s,task,bad,ext)
 s.append("task_submitted_review",A,task)
 s.append("review_revise",B,task,payload={"verdict":"REVISE","review_id":"p18-revise-"+task,
 "artifacts":ref,"correction":"Intentional missing quality requirement",
 "retry":{"eligible":True,"next_eligible_at":None,"max_attempts":2,"attempts":1,
 "error_class":"review_revise","manual_approval_required":True}})
 assert s.verified()["tasks"][task]["status"]=="NEEDS_REWORK"
 s.retry(task,C,approval=True)
 s.start(task,C);fixed=write(s,task,good,ext,rev="v2")
 pass_review(s,task,fixed,actor=C);s.complete(task,C,fixed)
 assert fixed[0]["sha256"]!=ref[0]["sha256"]
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--evidence",required=True);o=ap.parse_args()
 out=Path(o.evidence).resolve();out.mkdir(parents=True,exist_ok=True)
 assert (BASE/"scaffold/aos-w/templates/marketing-lifecycle-compound/template.yaml").is_file()
 i=out/"aos-w/agent-files/instances/bucket9-mock"
 (i/"graph-revisions").mkdir(parents=True,exist_ok=True)
 g={"nodes":[node("plan"),node("keywords",["plan"]),
 node("coaches",["keywords"],True),node("agencies",["keywords"],True),node("renovations",["keywords"],True),
 node("synthesis",["coaches","agencies","renovations"]),node("offer",["synthesis"]),
 node("copy",["offer"]),node("creative",["copy"],True,"svg"),
 node("crm",["offer"]),node("landing",["offer"]),node("tracking",["crm","landing"]),
 node("prelaunch",["creative","tracking"]),node("launch-permit",["prelaunch"])]}
 (i/"graph-revisions/g0001.yaml").write_text(yaml.safe_dump({"graph":g}))
 s=RunStore.create(i/"runs/run-001",g,"run-001",A)
 done(s,"plan","# MOCK scope\nThree fictional audiences")
 done(s,"keywords","# MOCK queue\ncoaches, agencies, renovations")
 assert {"coaches","agencies","renovations"}.issubset(set(s.verified()["eligible_tasks"]))
 bad_then_repair(s,"coaches","# INCOMPLETE fixture","# MOCK coaches\nSynthetic record with limitations")
 assert "synthesis" not in s.verified()["eligible_tasks"]
 done(s,"agencies","# MOCK agency source and limitations",True)
 s.start("renovations",A);s.checkpoint(A);s.handoff(A)
 s=RunStore(i/"runs/run-001")
 assert s.verified()["tasks"]["renovations"]["status"]=="RUNNING"
 s.append("task_paused",C,"renovations",payload={"reason":"Interrupted for cold resume"})
 s.append("task_resumed",C,"renovations",payload={"reason":"Recovered persisted event history"})
 s.start("renovations",C);rr=write(s,"renovations","# MOCK remodeling source and limitations")
 pass_review(s,"renovations",rr,actor=C);s.complete("renovations",C,rr)
 assert "synthesis" in s.verified()["eligible_tasks"]
 done(s,"synthesis","# MOCK synthesis\nThree reviewed fictional branches")
 done(s,"offer","# HYPOTHESIS ONLY\nNot a verified deliverable")
 done(s,"copy","# PROPOSED COPY\nNo real ad or product claims")
 s.start("crm",A);s.start("landing",A)
 assert {"crm","landing"}.issubset(set(s.verified()["active_steps"]))
 s.complete("crm",A,write(s,"crm","# MOCK CRM plan, unverified"))
 s.complete("landing",A,write(s,"landing","# MOCK landing plan, unverified"))
 done(s,"tracking","# MOCK Pixel CAPI verification UNKNOWN")
 before='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350"></svg>'
 after='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350"><text x="90" y="220">MOCK CREATIVE, NOT APPROVED</text></svg>'
 bad_then_repair(s,"creative",before,after,"svg")
 done(s,"prelaunch","# STAGED PLAN ONLY\nNo Meta changes. No approval to launch.")
 s.checkpoint(C);s.handoff(C);f=s.verified()
 assert all(v["status"]=="COMPLETE" for k,v in f["tasks"].items() if k!="launch-permit")
 assert f["tasks"]["launch-permit"]["status"]!="COMPLETE"
 lines=(s.root/"events.jsonl").read_text().splitlines()
 assert len(lines)>35
 d={"classification":"REAL_LOCAL_AOSW_FILE_EVENTS_WITH_MOCK_DATA",
 "when":datetime.now(timezone.utc).isoformat(),"events":len(lines),
 "completed":f["completed_steps"],"pending":"launch-permit",
 "research_qc_correction":"PASS_DETERMINISTIC","creative_qc_correction":"PASS_DETERMINISTIC",
 "parallel_branches":"PASS","cold_file_reopen":"PASS","real_ads_library":"NOT_RUN",
 "independent_ai_review":"NOT_RUN","real_image_generation_visual_qa":"NOT_RUN",
 "external_meta_crm_actions":"NOT_RUN","owner_live_authorization":"NOT_GRANTED",
 "V1_T01":"NOT_DEMONSTRATED"}
 (out/"p18-results.json").write_text(json.dumps(d,indent=2)+"\n")
 print("P18 staged synthetic file pilot PASS",len(lines),"events; launch NOT_GRANTED")
if __name__=="__main__":main()
