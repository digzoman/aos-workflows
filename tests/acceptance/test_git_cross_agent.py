"""P17 real Git bare-remote two-clone, multi-process, file-based collaboration.
This suite does NOT claim live GitHub, external cloud agents, or independently run AI models.
"""
from __future__ import annotations
import concurrent.futures,datetime as dt,hashlib,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
import yaml
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/git'))
sys.path.insert(0,str(ROOT/'tools/state'))
from coordination import GitClient,Conflict,Offline,Unauthorized,iso,now_utc
from state import RunStore,digest
ACTORS={'alpha':{'agent':'Alpha','platform':'local-subprocess','role':'researcher','instance':'worker-001'},'beta':{'agent':'Beta','platform':'local-subprocess','role':'researcher','instance':'worker-002'},'qa':{'agent':'QAGate','platform':'local-subprocess','role':'deterministic-reviewer','instance':'reviewer-003'},'handoff':{'agent':'Receiver','platform':'local-subprocess','role':'research-lead','instance':'receiver-004'}}
PREFIX='scaffold/aos-w/agent-files/'

# Test-fixture isolation: Git 2.55 runner may launch auto-GC/maintenance while
# TemporaryDirectory cleanup is removing bare remote packfiles. This is not
# part of the AOS-W claim protocol. Keep test repositories deterministic.
os.environ['GIT_CONFIG_COUNT']='2'
os.environ['GIT_CONFIG_KEY_0']='gc.auto'
os.environ['GIT_CONFIG_VALUE_0']='0'
os.environ['GIT_CONFIG_KEY_1']='maintenance.auto'
os.environ['GIT_CONFIG_VALUE_1']='false'

def git(cwd,*args,check=True):
 p=subprocess.run(['git',*args],cwd=cwd,text=True,capture_output=True,timeout=30)
 if check and p.returncode:raise AssertionError({'git':args,'stderr':p.stderr,'stdout':p.stdout})
 return p.stdout.strip() if check else p

def seed_run(seed,child,actor):
 instance=seed/PREFIX/'instances'/('child-'+child);(instance/'graph-revisions').mkdir(parents=True)
 graph={'schema_version':'1.0.0','template_id':'fake-competitor-research','version':'0.1.0','trigger':{'kind':'manual'},'policy':{'autonomy':'bounded'},'graph':{'nodes':[{'id':'research','kind':'task','needs':[],'inputs':[],'outputs':[{'artifact_id':'evidence','path':'artifacts/evidence.md'}],'quality':{'gates':['source-check']},'contract':{'done_when':'A verified evidence file, PASS review and checkpoint exist'},'instructions':'Write source-labelled fictional evidence and receive deterministic separate-process review'}]}}
 (instance/'graph-revisions'/'g0001.yaml').write_text(yaml.safe_dump(graph,sort_keys=False))
 (instance/'template-snapshots').mkdir()
 run=instance/'runs'/'run-001';RunStore.create(run,graph['graph'],'run-001',actor).checkpoint(actor)

class GitCollaborativeAcceptance(unittest.TestCase):
 def setUp(self):
  t=tempfile.TemporaryDirectory(prefix='aosw-p17-');self.addCleanup(t.cleanup);self.root=Path(t.name)
  self.remote=self.root/'server.git';git(self.root,'init','--bare',str(self.remote))
  seed=self.root/'seed';git(self.root,'init','-b','main',str(seed))
  git(seed,'config','user.name','Shared Bot Credential');git(seed,'config','user.email','same-account@example.invalid')
  for task in ('coaches','agencies'):seed_run(seed,task,ACTORS['alpha'])
  (seed/PREFIX/'portfolio-plan.json').write_text(json.dumps({'plan_id':'portfolio','tasks':['coaches','agencies'],'join':'all_reviewed','synthesis_authority':'required'},indent=2)+'\n')
  git(seed,'add','.');git(seed,'commit','-m','sanitized portfolio seed');git(seed,'remote','add','origin',str(self.remote));git(seed,'push','-u','origin','main');git(self.remote,'symbolic-ref','HEAD','refs/heads/main')
  self.a=self.root/'worker-alpha';self.b=self.root/'worker-beta';self.c=self.root/'worker-qa'
  for d in (self.a,self.b,self.c):
   git(self.root,'clone',str(self.remote),str(d));git(d,'config','user.name','Shared Bot Credential');git(d,'config','user.email','same-account@example.invalid')
  self.ca=GitClient(self.a);self.cb=GitClient(self.b);self.cc=GitClient(self.c)
  self.audit=[]
 def worker(self,d,mode,task,who,claim=None,note=None,expect_ok=True):
  cmd=[sys.executable,str(HERE/'git_collab_worker.py'),mode,'--repo',str(d),'--task',task,'--actor',json.dumps(ACTORS[who])]
  if claim:cmd+=['--token',claim['record']['token'],'--epoch',str(claim['record']['epoch'])]
  if note:cmd+=['--note',note]
  p=subprocess.run(cmd,text=True,capture_output=True,timeout=30)
  if expect_ok:self.assertEqual(p.returncode,0,p.stderr+'\n'+p.stdout)
  return json.loads(p.stdout) if p.returncode==0 else p.stderr
 def runpath(self,d,task):return d/PREFIX/'instances'/('child-'+task)/'runs'/'run-001'
 def publish(self,client,d,task,actor):
  rel=PREFIX+'instances/child-'+task+'/runs/run-001'
  return client.sync_commit([rel],actor,branch='main',message='Accepted '+task+' checkpoint')
 def test_01_two_separate_os_processes_discover_from_file_records(self):
  a=self.worker(self.a,'discover','coaches','alpha');b=self.worker(self.b,'discover','coaches','beta')
  self.assertEqual(a['found'][0]['eligible'],['research']);self.assertEqual(b['found'][1]['eligible'],['research'])
  self.assertNotEqual(a['actor'],b['actor'])
  self.assertEqual(git(self.a,'config','user.email'),git(self.b,'config','user.email'))
 def test_02_parallel_cas_and_stale_clone_claim_rejected(self):
  def attempt(i):
   c=self.ca if i==0 else self.cb
   try:return ('WIN',c.acquire('portfolio','coaches',ACTORS['alpha' if i==0 else 'beta']))
   except Conflict as e:return ('CONFLICT',str(e))
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:r=list(pool.map(attempt,(0,1)))
  self.assertEqual(sum(x[0]=='WIN' for x in r),1,r)
  self.assertEqual(sum(x[0]=='CONFLICT' for x in r),1,r)
  winner=next(x[1] for x in r if x[0]=='WIN')
  loser_client=self.cb if winner['record']['actor']==ACTORS['alpha'] else self.ca
  with self.assertRaises(Conflict):loser_client.acquire('portfolio','coaches',ACTORS['beta' if loser_client==self.cb else 'alpha'])
  self.assertEqual(self.ca.status('portfolio','coaches')['sha'],winner['sha'])
 def test_03_owner_identity_and_claim_required_at_worker_start(self):
  claim=self.ca.acquire('portfolio','coaches',ACTORS['alpha']);result=self.worker(self.b,'start','coaches','beta',claim,expect_ok=False)
  self.assertIn('Actor does not match remote ownership',result)
  good=self.worker(self.a,'start','coaches','alpha',claim);self.assertEqual(good['status'],'RUNNING')
 def test_03b_release_rejects_different_actor_even_with_valid_token(self):
  claim=self.ca.acquire('portfolio','coaches',ACTORS['alpha'])
  with self.assertRaises(Unauthorized):
   self.cb.release('portfolio','coaches',ACTORS['beta'],claim['record']['token'],claim['record']['epoch'])
  self.assertEqual(self.ca.status('portfolio','coaches')['record']['state'],'active')
 def test_04_task_output_checkpoint_handoff_and_real_remote_commit(self):
  claim=self.ca.acquire('portfolio','coaches',ACTORS['alpha'])
  self.worker(self.a,'start','coaches','alpha',claim)
  result=self.worker(self.a,'submit','coaches','alpha',claim,note='Source: synthetic-catalog-01\nObserved: one fictional ad offer, dated 2026-10-20.\n')
  self.assertEqual(result['status'],'WAIT_REVIEW')
  self.publish(self.ca,self.a,'coaches',ACTORS['alpha'])
  remote=git(self.remote,'show','main:'+PREFIX+'instances/child-coaches/runs/run-001/artifacts/evidence.md')
  self.assertIn('Observed:',remote)
  hist=git(self.a,'log','-1','--format=%B');self.assertIn('Agent-Provenance: [Alpha | local-subprocess | researcher | worker-001]',hist)
  self.assertEqual(RunStore(self.runpath(self.a,'coaches')).verified()['tasks']['research']['status'],'WAIT_REVIEW')
 def test_05_receiver_cold_resume_from_separate_clone_and_QC(self):
  claim=self.ca.acquire('portfolio','coaches',ACTORS['alpha'])
  self.worker(self.a,'start','coaches','alpha',claim)
  self.worker(self.a,'submit','coaches','alpha',claim,note='Source: fictional-record-1\nObserved: a hypothetical offer only.\n')
  self.publish(self.ca,self.a,'coaches',ACTORS['alpha'])
  self.assertEqual(self.cc.sync_refresh()['status'],'SYNCED')
  cold=self.worker(self.c,'handoff','coaches','handoff')
  self.assertGreater(cold['last_event_seq'],2);self.assertNotIn('research',cold['completed'])
  review=self.worker(self.c,'review','coaches','qa');self.assertEqual(review['status'],'WAIT_REVIEW')
  self.publish(self.cc,self.c,'coaches',ACTORS['qa'])
  self.assertEqual(self.ca.sync_refresh()['status'],'SYNCED')
  finished=self.worker(self.a,'finish','coaches','alpha',claim)
  self.assertEqual(finished['status'],'COMPLETE');self.publish(self.ca,self.a,'coaches',ACTORS['alpha'])
  self.assertEqual(self.cb.sync_refresh()['status'],'SYNCED')
  s=RunStore(self.runpath(self.b,'coaches')).verified();self.assertEqual(s['tasks']['research']['status'],'COMPLETE')
  self.assertEqual(s['tasks']['research']['last_attempt_owner'],ACTORS['alpha'])
  self.assertEqual(s['tasks']['research']['review']['verdict'],'PASS')
 def test_06_crashed_owner_expiry_and_no_automatic_reclaim(self):
  first=self.ca.acquire('portfolio','coaches',ACTORS['alpha'])
  self.worker(self.a,'start','coaches','alpha',first)
  # Simulate operator-detected loss of session and objectively expired lease via remote CAS.
  stale={**first['record'],'expires_at':iso(now_utc()-dt.timedelta(minutes=10))}
  newer=self.ca._commit(stale,first['sha']);self.ca._push(newer,first['ref'],first['sha'])
  with self.assertRaises(Conflict):self.cb.acquire('portfolio','coaches',ACTORS['beta'])
  with self.assertRaises(Unauthorized):self.cb.acquire('portfolio','coaches',ACTORS['beta'],explicit_reclaim=True,reclaim_reason='short')
  second=self.cb.acquire('portfolio','coaches',ACTORS['beta'],explicit_reclaim=True,reclaim_reason='Operator reviewed hung process, checked no provider effects, approved manual takeover')
  self.assertEqual(second['record']['epoch'],2)
  old=self.worker(self.a,'submit','coaches','alpha',first,note='Source: old\nObserved: old work\n',expect_ok=False)
  self.assertTrue('token/epoch' in old or 'no longer current' in old)
 def test_07_partition_blocks_shared_mutations_and_preserves_drafts(self):
  first=self.ca.acquire('portfolio','coaches',ACTORS['alpha'])
  self.worker(self.a,'start','coaches','alpha',first)
  git(self.a,'remote','set-url','origin',str(self.root/'unreachable.git'))
  with self.assertRaises(Offline):self.ca.verify('portfolio','coaches',first['record']['token'],first['record']['epoch'])
  out=self.worker(self.a,'submit','coaches','alpha',first,note='Source: pending\nObserved: not applied\n',expect_ok=False)
  self.assertIn('Offline',out)
  self.assertFalse((self.runpath(self.a,'coaches')/'artifacts/evidence.md').exists())
 def test_08_real_divergent_commit_conflict_preserves_local_outputs(self):
  a=self.a/PREFIX/'portfolio-plan.json';b=self.b/PREFIX/'portfolio-plan.json'
  a.write_text('{"notes":"from A"}\n');self.ca.sync_commit([PREFIX+'portfolio-plan.json'],ACTORS['alpha'])
  b.write_text('{"notes":"from B, preserve"}\n');git(self.b,'add',PREFIX+'portfolio-plan.json');git(self.b,'commit','-m','local plan B')
  self.assertEqual(self.cb.sync_probe()['status'],'DIVERGED')
  with self.assertRaises(Conflict):self.cb.sync_refresh()
  self.assertIn('preserve',b.read_text())
 def test_09_parallel_branches_explicit_reconciliation_and_reviewed_merge(self):
  c1=self.ca.acquire('portfolio','coaches',ACTORS['alpha']);c2=self.cb.acquire('portfolio','agencies',ACTORS['beta'])
  for client,d,task,who,claim in ((self.ca,self.a,'coaches','alpha',c1),(self.cb,self.b,'agencies','beta',c2)):
   self.worker(d,'start',task,who,claim)
   self.worker(d,'submit',task,who,claim,note=f'Source: fictional-{task}\nObserved: synthetic {task} candidate with no real customer data.\n')
  # Alice publishes branch A; Bob's completed draft is not discarded/overwritten.
  self.publish(self.ca,self.a,'coaches',ACTORS['alpha'])
  with self.assertRaises(Conflict):self.cb.sync_refresh() # has dirty, behind status
  p=self.runpath(self.b,'agencies');scratch=self.root/'safe-backup';shutil.copytree(p,scratch)
  # Explicit operator reconciliation after preserving the full B draft and checking remote state.
  git(self.b,'reset','--hard','HEAD');git(self.b,'clean','-fd')
  self.assertEqual(self.cb.sync_refresh()['status'],'SYNCED')
  shutil.copytree(scratch,p,dirs_exist_ok=True)
  self.publish(self.cb,self.b,'agencies',ACTORS['beta'])
  # Two separate review/checkpoint rounds, no self-reviews.
  for client,d,task in ((self.ca,self.a,'coaches'),(self.cb,self.b,'agencies')):
   self.assertEqual(client.sync_refresh()['status'],'SYNCED')
   self.worker(d,'review',task,'qa')
   self.publish(client,d,task,ACTORS['qa'])
  # Finish with producer after re-read, verifying the same claims are still current.
  for client,d,task,who,claim in ((self.ca,self.a,'coaches','alpha',c1),(self.cb,self.b,'agencies','beta',c2)):
   self.assertEqual(client.sync_refresh()['status'],'SYNCED')
   self.worker(d,'finish',task,who,claim)
   self.publish(client,d,task,ACTORS[who])
   client.release('portfolio',task,ACTORS[who],claim['record']['token'],claim['record']['epoch'])
  self.cb.sync_refresh()
  synth=[]
  for task in ('coaches','agencies'):
   s=RunStore(self.runpath(self.b,task)).verified();q=s['tasks']['research'];self.assertEqual(q['status'],'COMPLETE');self.assertEqual(q['review']['verdict'],'PASS')
   f=self.runpath(self.b,task)/'artifacts/evidence.md';self.assertEqual(q['evidence'][0]['sha256'],digest(f.read_bytes()))
   synth.append({'task':task,'evidence_sha256':q['evidence'][0]['sha256'],'review_id':q['review']['review_id']})
  manifest=self.b/PREFIX/'synthesis-reviewed.json';manifest.write_text(json.dumps({'status':'MOCK_READY_FOR_HUMAN_SYNTHESIS','children':synth,'source':'reviewed_local_git_evidence_only'},indent=2)+'\n')
  self.cb.sync_commit([PREFIX+'synthesis-reviewed.json'],ACTORS['beta'])
  self.ca.sync_refresh()
  self.assertEqual(json.loads((self.a/PREFIX/'synthesis-reviewed.json').read_text())['children'],synth)
 def test_10_move_to_different_git_remote_preserves_checked_run(self):
  c=self.ca.acquire('portfolio','coaches',ACTORS['alpha']);self.worker(self.a,'start','coaches','alpha',c);self.worker(self.a,'submit','coaches','alpha',c,note='Source: synthetic\nObserved: saved work\n');self.publish(self.ca,self.a,'coaches',ACTORS['alpha'])
  migrated=self.root/'new-remote.git';git(self.root,'init','--bare',str(migrated));git(self.a,'remote','add','migration',str(migrated));git(self.a,'push','migration','main')
  git(migrated,'symbolic-ref','HEAD','refs/heads/main');dest=self.root/'new-repo-clone';git(self.root,'clone',str(migrated),str(dest));new=GitClient(dest)
  self.assertEqual(new.sync_probe()['status'],'SYNCED');self.assertEqual(RunStore(self.runpath(dest,'coaches')).verified()['tasks']['research']['status'],'WAIT_REVIEW')
  self.assertIsNone(new.status('portfolio','coaches')['record']) # claim namespace NOT migrated implicitly
  self.assertNotEqual(str(self.remote),str(migrated))
