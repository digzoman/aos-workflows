"""P17 optional live GitHub CAS/LFS experiment on isolated ephemeral refs.
No Git credential is written into AOS-W files. This is not part of the file-only core.
Run exclusively on Actions main when contents:write is explicitly allowed.
Results distinguish PASS/BLOCKED/NOT_RUN; failures are not silently converted to PASS.
"""
from __future__ import annotations
import base64,concurrent.futures,json,os,subprocess,sys,tempfile,uuid
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/git'))
from coordination import GitClient,Conflict,Offline,Unauthorized,LFSLockPrototype
A={'agent':'HostedAlpha','platform':'github-actions-separate-process','role':'claimant','instance':'worker-a'}
B={'agent':'HostedBeta','platform':'github-actions-separate-process','role':'claimant','instance':'worker-b'}

def git(cwd,*args):
 p=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True,timeout=50)
 if p.returncode:raise RuntimeError(f'Git command failed (no credential details): {args[0]} exit {p.returncode}; {p.stderr[:160]}')
 return p.stdout.strip()

def main():
 out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
 res={'classification':'REAL_HOSTED_GITHUB_GIT_IF_VERIFIED','status':'NOT_RUN','repo':os.getenv('GITHUB_REPOSITORY'),'cas':{},'lfs':{'status':'NOT_RUN'},'limitations':['Same hosted runner; two OS subprocesses, not two separate AI provider platforms','Provider effects are not fenced by Git claims']}
 token=os.getenv('GITHUB_TOKEN')
 if not token or not os.getenv('GITHUB_REPOSITORY'):
  res.update(status='BLOCKED',reason='No GitHub credential/repository environment');out.write_text(json.dumps(res,indent=2)+'\n');return
 nonce='p17-'+str(os.getenv('GITHUB_RUN_ID','local'))+'-'+str(os.getenv('GITHUB_RUN_ATTEMPT','1'))+'-'+uuid.uuid4().hex[:8]
 namespace='aosw-acceptance-'+nonce
 ghurl='https://github.com/'+os.environ['GITHUB_REPOSITORY']+'.git'
 auth=base64.b64encode(('x-access-token:'+token).encode()).decode()
 os.environ['GIT_CONFIG_COUNT']='1';os.environ['GIT_CONFIG_KEY_0']='http.https://github.com/.extraheader';os.environ['GIT_CONFIG_VALUE_0']='AUTHORIZATION: basic '+auth
 os.environ['GIT_TERMINAL_PROMPT']='0'
 created=[]
 try:
  with tempfile.TemporaryDirectory(prefix='aosw-live-hosted-') as temp:
   tmp=Path(temp);a=tmp/'a';b=tmp/'b'
   for folder in (a,b):
    git(tmp,'clone','--quiet','--no-hardlinks',str(ROOT),str(folder))
    git(folder,'remote','set-url','origin',ghurl)
    git(folder,'config','user.name','Shared GitHub App Credential')
    git(folder,'config','user.email','same-transport@example.invalid')
   ca=GitClient(a,claim_namespace=namespace);cb=GitClient(b,claim_namespace=namespace)
   try:
    sha=ca.remote_tip('refs/heads/main')
    if not sha:raise RuntimeError('GitHub remote branch not visible')
    res['cas']['hosted_main_tip_verified']=True
   except Exception as e:
    res.update(status='BLOCKED',reason='Could not authenticate/read GitHub remote main: '+type(e).__name__)
    out.write_text(json.dumps(res,indent=2)+'\n');return
   def attempt(i):
    actor=A if i==0 else B
    cmd=[sys.executable,str(HERE/'git_collab_worker.py'),'claim','--repo',str(a if i==0 else b),'--task','same-task','--actor',json.dumps(actor)]
    # Worker has default namespace; hosted test uses unique namespace via optional env for isolation.
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=45,env={**os.environ,'AOSW_TEST_CLAIM_NAMESPACE':namespace})
    if p.returncode==0:return {'status':'WIN','data':json.loads(p.stdout)}
    if 'Conflict' in p.stderr or 'already claimed' in p.stderr or 'Remote claim changed' in p.stderr:return {'status':'CONFLICT','detail':'ref CAS rejected competing claimant'}
    return {'status':'BLOCKED','detail':p.stderr[-250:]}
   with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(attempt,(0,1)))
   res['cas']['competing_processes']=[z['status'] for z in results]
   st=ca.status('portfolio','same-task');ref=st['ref'];created.append(ref)
   if any(z['status']=='BLOCKED' for z in results):
    res.update(status='BLOCKED',reason='Hosted Git transport/permission prevented completing a reliable competing-claim result')
   elif sorted(z['status'] for z in results)!=['CONFLICT','WIN'] or not st['record']:
    res.update(status='FAIL',reason='Hosted competing Git ref updates did not establish exactly one owner')
   else:
    winner=st['record'];res['cas']['winning_agent']=winner['actor']
    res['cas']['claim_tip']=st['sha'];res['cas']['same_git_auth_account']=git(a,'config','user.email')==git(b,'config','user.email')
    loser=cb if winner['actor']==A else ca
    try:loser.acquire('portfolio','same-task',B if winner['actor']==A else A)
    except Conflict:res['cas']['stale_claim_blocked']=True
    res['status']='PASS' if res['cas'].get('stale_claim_blocked') else 'FAIL'
   # Lock comparison is separate and never converts a missing LFS service to PASS.
   protoA=LFSLockPrototype(ca);protoB=LFSLockPrototype(cb)
   if not protoA.available():res['lfs']={'status':'BLOCKED','reason':'Git LFS binary unavailable'}
   else:
    lockfile='scaffold/aos-w/agent-files/'+nonce+'-lfs.txt'
    for clone in (a,b):
     fp=clone/lockfile;fp.parent.mkdir(parents=True,exist_ok=True);fp.write_text('synthetic acceptance lock only\n')
    lock=None
    try:
     lock=protoA.lock(lockfile,A)
     res['lfs']={'status':'PASS_LOCK_ACQUIRED','owner_from_server':lock['lock'].get('owner'), 'same_credential_distinguishes_agent_instances':False}
     try:
      protoB.lock(lockfile,B)
      res['lfs']['second_lock']='granted_or_same_owner_response';res['lfs']['status']='REVIEW_REQUIRED'
     except Exception as e:res['lfs']['second_lock']='refused_'+type(e).__name__
    except Exception as e:res['lfs']={'status':'BLOCKED','reason':'Live Git LFS lock API '+type(e).__name__}
    finally:
     if lock:
      try:protoA.unlock(lock['lock']['id'],A);res['lfs']['unlock']='verified_request_succeeded'
      except Exception as e:res['lfs']['unlock']='FAILED_'+type(e).__name__
 finally:
  for ref in created:
   # No unscoped history refs, and never force-delete a ref after someone else changed it.
   try:
    p=subprocess.run(['git','push',f'--force-with-lease={ref}:{st["sha"]}',ghurl,':'+ref],cwd=ROOT,capture_output=True,text=True,timeout=45)
    res.setdefault('cleanup',{})[ref]='DELETED' if p.returncode==0 else 'FAILED_SAFE_STOP'
    if p.returncode:res['status']='REVIEW_REQUIRED'
   except Exception as e:res.setdefault('cleanup',{})[ref]='FAILED_'+type(e).__name__;res['status']='REVIEW_REQUIRED'
  res.pop('credential',None);out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'hosted_cas':res['status'],'lfs':res['lfs']['status'],'results_path':str(out)}))
if __name__=='__main__':main()
