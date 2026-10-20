"""AOS-W P17: ephemeral *separate OS process* Git workflow worker.
All file operations are synthetic and local; no external marketing services.
"""
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/git'))
sys.path.insert(0,str(ROOT/'tools/state'))
from coordination import GitClient, Conflict
from state import RunStore, digest

def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['discover','claim','start','submit','review','finish','handoff']);p.add_argument('--repo',required=True);p.add_argument('--run',default='portfolio');p.add_argument('--task',default='coaches');p.add_argument('--actor',required=True);p.add_argument('--token');p.add_argument('--epoch',type=int);p.add_argument('--note');p.add_argument('--reviewer')
 a=p.parse_args();repo=Path(a.repo);actor=json.loads(a.actor);client=GitClient(repo,claim_namespace=__import__('os').environ.get('AOSW_TEST_CLAIM_NAMESPACE','aosw-claims'))
 base=repo/'scaffold/aos-w/agent-files/instances'
 def runpath(task):return base/('child-'+task)/'runs'/'run-001'
 if a.action=='claim':
  claimed=client.acquire('portfolio',a.task,actor)
  print(json.dumps({'actor':actor,'status':'CLAIM_GRANTED','ref':claimed['ref'],'sha':claimed['sha'],'epoch':claimed['record']['epoch']},sort_keys=True));return
 if a.action=='discover':
  found=[]
  for task in ('coaches','agencies'):
   state=RunStore(runpath(task)).verified();st=client.status('portfolio',task)
   found.append({'task':task,'run_status':state['run_status'],'completed':state['completed_steps'],'eligible':state['eligible_tasks'],'claim_actor':st['record']['actor'] if st['record'] and st['record'].get('state')=='active' else None})
  print(json.dumps({'actor':actor,'found':found},sort_keys=True));return
 if a.action=='handoff':
  s=RunStore(runpath(a.task));v=s.verified();h=s.handoff(actor)
  print(json.dumps({'actor':actor,'last_event_seq':v['last_event_seq'],'completed':v['completed_steps'],'next':h['next_action'],'graph_revision':v['graph_revision']},sort_keys=True));return
 if a.action!='review':
  if not a.token or a.epoch is None:raise RuntimeError('Worker needs exact remote claim token and epoch')
  st=client.verify('portfolio',a.task,a.token,a.epoch)
  if st['record']['actor']!=actor:raise RuntimeError('Actor does not match remote ownership (four-field identity)')
 store=RunStore(runpath(a.task));task='research'
 if a.action=='start':
  store.start(task,actor);store.checkpoint(actor)
 elif a.action=='submit':
  if not a.note:raise RuntimeError('Evidence text required')
  artifact=runpath(a.task)/'artifacts'/'evidence.md';artifact.parent.mkdir(parents=True,exist_ok=True)
  artifact.write_text(a.note,encoding='utf-8')
  store.append('task_submitted_review',actor,task_id=task)
  store.checkpoint(actor)
 elif a.action=='review':
  # Deterministic review from a separate process; NOT an independent AI reviewer.
  item=store.verified()['tasks'][task]
  if item['status']!='WAIT_REVIEW':raise RuntimeError('Review not eligible')
  if item.get('owner')==actor:raise RuntimeError('Review cannot self-certify')
  f=runpath(a.task)/'artifacts'/'evidence.md';text=f.read_text()
  if 'Observed:' not in text or 'Source:' not in text:raise RuntimeError('Evidence missing source/observation labels')
  evidence={'artifact_id':'evidence','locator':'artifacts/evidence.md','sha256':digest(f.read_bytes()),'revision':'v1'}
  store.append('review_accepted',actor,task_id=task,payload={'verdict':'PASS','review_id':'qa-'+a.task,'rubric_version':'1','artifacts':[evidence],'review_kind':'deterministic_separate_process'})
  store.checkpoint(actor)
 elif a.action=='finish':
  f=runpath(a.task)/'artifacts'/'evidence.md';e={'artifact_id':'evidence','locator':'artifacts/evidence.md','sha256':digest(f.read_bytes()),'revision':'v1'}
  store.complete(task,actor,[e]);store.checkpoint(actor)
 else:raise RuntimeError('unsupported action')
 v=store.verified()
 print(json.dumps({'actor':actor,'action':a.action,'task':a.task,'status':v['tasks'][task]['status'],'seq':v['last_event_seq'],'digest':v['last_event_digest']},sort_keys=True))
if __name__=='__main__':main()
