#!/usr/bin/env python3
"""Cold process agent simulation: reads ONLY persisted installed AOS-W files.

This is an acceptance *harness*, not a production AOS-W agent or a model.
No Git, network, external provider, or previous conversation context is accessed.
"""
import argparse, hashlib, json, sys
from pathlib import Path
import yaml

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
sys.path.insert(0,str(PROJECT/'tools'/'state'))
from state import RunStore

ACTOR={'agent':'Offline Research Agent','platform':'standalone-fresh-process','role':'research-worker','instance':'p16-cold-resume'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(root,aid,relative,rev='v1'):
 p=root/relative
 return {'artifact_id':aid,'locator':relative,'sha256':sha(p),'revision':rev}
def main():
 a=argparse.ArgumentParser();a.add_argument('--install',required=True);a.add_argument('--instance',required=True);a.add_argument('--run',default='run-001');opts=a.parse_args()
 install=Path(opts.install).resolve();assert not (install/'.git').exists()
 assert (install/'PROTOCOL.md').is_file() and (install/'references/STATE-AND-RECOVERY.md').is_file()
 i=install/'agent-files/instances'/opts.instance;run=i/'runs'/opts.run
 saved=json.loads((run/'handoff.json').read_text());assert saved['run_id']==opts.run
 graph=yaml.safe_load((i/'graph-revisions'/f"{saved['graph_revision']}.yaml").read_text())['graph']
 assert [n['id'] for n in graph['nodes']]==['define-scope','collect-evidence','review-evidence']
 source=json.loads((run/'artifacts/offline-sources.json').read_text());assert source['scenario']=='fictional_offline_fixture'
 skill=(install/'templates/research-starter/skills/evidence-handling/SKILL.md').read_text()
 assert 'Evidence handling' in skill and 'observed' in skill.lower()
 store=RunStore(run)
 pre=store.verified();assert pre['tasks']['define-scope']['status']=='COMPLETE'
 # Interrupted/unfinished task from prior process must NEVER be silently counted as finished.
 status=pre['tasks']['collect-evidence']['status']
 if status=='RUNNING':
  store.append('task_paused',ACTOR,'collect-evidence',payload={'reason':'Prior process interrupted; no completed evidence; re-evaluate before restart'})
  store.append('task_resumed',ACTOR,'collect-evidence',payload={'reason':'Cold-start inspected saved state and owner; new bounded attempt'})
  status='READY'
 assert status in ('READY','WAIT_DEPENDENCY'),status
 store.start('collect-evidence',ACTOR,context_checked=True)
 lines=['# Offline evidence log','',f"Research question: {source['question']}",'','**Source class:** deliberately fictional local fixture; NO external factual claim.','',
 '## Directly observed fixture records','','| Source ID | Fictional product | Quoted fixture capability | Price class |','|---|---|---|---|']
 for row in source['records']:
  lines.append(f"| {row['id']} | {row['product']} | {row['capability']} | {row['tier']} |")
 lines+=['','## Inferences (not observed claims)','',
 'The local fixture suggests two distinct capability families: automated appointments and draft advertising copy. This is only a hypothesis for comparison, not a verified market outcome.','',
 '## Source limitations','',
 '- Fixture is synthetic and offline. No provider websites, Meta Ads Library or real advertisers were accessed.',
 '- Tier descriptions are fictional and cannot be treated as market prices.',
 '- Independent checking requires actual sources outside this acceptance scenario.','']
 (run/'artifacts/evidence.md').write_text('\n'.join(lines),encoding='utf-8')
 store.complete('collect-evidence',ACTOR,[ref(run,'evidence-log','artifacts/evidence.md')]);store.checkpoint(ACTOR)
 assert store.verified()['eligible_tasks']==['review-evidence']
 store.start('review-evidence',ACTOR)
 text=(run/'artifacts/evidence.md').read_text();pass_checks=all(x in text for x in ['Directly observed fixture records','Inferences (not observed claims)','Source limitations']+ [v['id'] for v in source['records']])
 assert pass_checks
 summary=['# Reviewed offline research summary','','**Verdict:** PASS (permitted low-risk self-review on fictional local evidence).','',
 f"Question: {source['question']}",'',
 '**Observed:** Three explicitly fictional source rows were inspected from a local fixture.','',
 '**Interpretation:** Two potential capability families, not proof of product-market fit.','',
 '**Unverified:** Real competitors, advertising evidence, actual prices, deliverability, and business outcomes.','',
 'QC rubric: evidence-self-check v1; agent reviewed actual current source records and separations of observations/inference/limits.','']
 (run/'artifacts/summary.md').write_text('\n'.join(summary),encoding='utf-8')
 summary_ref=ref(run,'reviewed-summary','artifacts/summary.md')
 store.append('task_submitted_review',ACTOR,'review-evidence')
 store.append('review_accepted',ACTOR,'review-evidence',payload={'verdict':'PASS','review_id':'p16-self-review-001','artifacts':[summary_ref], 'rubric_version':'evidence-self-check-v1', 'reviewer_kind':'self_review', 'subject':'fictional only'})
 store.complete('review-evidence',ACTOR,[summary_ref]);cp=store.checkpoint(ACTOR);handoff=store.handoff(ACTOR);result=store.verified()
 assert result['run_status']=='COMPLETED' and set(result['completed_steps'])=={'define-scope','collect-evidence','review-evidence'}
 print(json.dumps({'result':'PASS','resumed_from_handoff_seq':saved['last_event_seq'],
  'new_process_actor':ACTOR,'final_seq':result['last_event_seq'],'final_status':result['run_status'],
  'completed':result['completed_steps'],'first_checkpoint':cp['checkpoint_id'],'integrity':result['integrity_level'],
  'handoff_seq':handoff['last_event_seq'],'quality':'self_review_pass_on_fictional_fixture'},sort_keys=True))
if __name__=='__main__':main()
