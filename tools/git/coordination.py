"""OPTIONAL Git-synchronised AOS-W task coordination.
Requires Git installed and a configured, reachable remote; NOT part of standalone AOS-W.
Claim refs use Git push --force-with-lease=<ref>:<explicit-old-sha>, never implicit leases.
This does NOT authenticate actors, fence external APIs, or guarantee distributed exactly-once effects.
"""
from __future__ import annotations
import datetime as dt
import json, os, re, subprocess, uuid
from pathlib import Path

SAFE=re.compile(r'^[a-z0-9][a-z0-9._-]{0,79}$')
class GitCoordinationError(RuntimeError): pass
class Conflict(GitCoordinationError): pass
class Offline(GitCoordinationError): pass
class Unauthorized(GitCoordinationError): pass

def valid_actor(actor):
    return isinstance(actor,dict) and all(isinstance(actor.get(k),str) and actor[k].strip() for k in ('agent','platform','role','instance'))

def now_utc():return dt.datetime.now(dt.timezone.utc)
def at(value):return dt.datetime.fromisoformat(value.replace('Z','+00:00'))
def iso(value):return value.isoformat(timespec='seconds').replace('+00:00','Z')
def safe_id(v):return isinstance(v,str) and bool(SAFE.fullmatch(v)) and '..' not in v and not v.endswith('.lock') and not v.startswith('.')
def canonical(data):return json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)

class GitClient:
    """Operates in a Git working tree. Claims are refs, independent of HEAD/working tree."""
    def __init__(self,repo,remote='origin',claim_namespace='aosw-claims'):
        self.repo=Path(repo).resolve();self.remote=remote;self.namespace=claim_namespace
        if not safe_id(remote) or not safe_id(claim_namespace):raise GitCoordinationError('Unsafe Git remote/namespace')
        self.run('rev-parse','--show-toplevel')
    def run(self,*args,input_text=None,allow_failure=False):
        p=subprocess.run(['git',*args],cwd=self.repo,input=input_text,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30,
                         env={**os.environ,'GIT_TERMINAL_PROMPT':'0','GIT_AUTHOR_NAME':'AOS-W Claim Ref','GIT_AUTHOR_EMAIL':'aosw@invalid.example',
                         'GIT_COMMITTER_NAME':'AOS-W Claim Ref','GIT_COMMITTER_EMAIL':'aosw@invalid.example'})
        if p.returncode and not allow_failure:
            err=(p.stderr or p.stdout).strip()
            if any(s in err.lower() for s in ['could not resolve host','unable to access','connection refused','connection timed out','does not appear to be a git repository','no such device','could not read from remote']):raise Offline(err)
            raise GitCoordinationError(f'git {args[0]} failed: {err[:350]}')
        return p
    def ref(self,run,task):
        if not safe_id(run) or not safe_id(task):raise GitCoordinationError('Invalid run/task identifier')
        return f'refs/heads/{self.namespace}/{run}/{task}'
    def remote_tip(self,ref):
        p=self.run('ls-remote',self.remote,ref)
        lines=[s for s in p.stdout.splitlines() if s.endswith('\t'+ref)]
        if len(lines)>1:raise GitCoordinationError('Ambiguous ref')
        return lines[0].split('\t')[0] if lines else None
    def read_claim(self,ref,sha):
        if not sha:return None
        self.run('fetch','--no-tags',self.remote,ref)
        v=self.run('show',f'{sha}:claim.json').stdout
        try: record=json.loads(v)
        except json.JSONDecodeError as e:raise GitCoordinationError('Remote claim record invalid') from e
        if record.get('ref')!=ref:raise GitCoordinationError('Remote ref/claim mismatch')
        return record
    def status(self,run,task):
        ref=self.ref(run,task);sha=self.remote_tip(ref)
        return {'ref':ref,'sha':sha,'record':self.read_claim(ref,sha)}
    def _commit(self,record,parent):
        blob=self.run('hash-object','-w','--stdin',input_text=canonical(record)+'\n').stdout.strip()
        tree=self.run('mktree',input_text=f'100644 blob {blob}\tclaim.json\n').stdout.strip()
        args=['commit-tree',tree]
        if parent:args.extend(['-p',parent])
        return self.run(*args,input_text=f"AOS-W {record['state']} {record['run_id']}/{record['task_id']}\n\nAgent-Provenance: [{record['actor']['agent']} | {record['actor']['platform']} | {record['actor']['role']} | {record['actor']['instance']}]\n").stdout.strip()
    def _push(self,new,ref,old):
        # Explicit empty <expect> means ref MUST not exist. Explicit old SHA ensures CAS on updates.
        p=self.run('push',f'--force-with-lease={ref}:{old or ""}',self.remote,f'{new}:{ref}',allow_failure=True)
        if p.returncode:
            try: current=self.remote_tip(ref)
            except Offline:raise Offline('Push outcome uncertain and remote cannot be read. STOP: do not retry blindly.')
            if current==new:return new # accepted push, acknowledgment may have been lost
            raise Conflict(f'Remote claim changed (expected {old or "ABSENT"}, observed {current or "ABSENT"}); do not overwrite')
        check=self.remote_tip(ref)
        if check!=new:raise GitCoordinationError('Push returned success but new ref is unverified')
        return new
    def acquire(self,run,task,actor,lease_seconds=1800,explicit_reclaim=False,reclaim_reason=None):
        if not valid_actor(actor):raise Unauthorized('Complete logical four-part actor required')
        if not isinstance(lease_seconds,int) or not 60<=lease_seconds<=86400:raise GitCoordinationError('Lease must be 60..86400 seconds')
        st=self.status(run,task);old=st['record']
        if old and old['state']=='active':
            if not explicit_reclaim:raise Conflict('Task already claimed, including when agents share the same Git identity')
            if at(old['expires_at'])>now_utc():raise Unauthorized('Cannot reclaim an unexpired task claim')
            if not reclaim_reason or len(reclaim_reason)<12:raise Unauthorized('Explicit stale-claim reconciliation/approval reason needed')
        elif explicit_reclaim:raise Unauthorized('Reclaim only for an expired active claim')
        if old and old['state'] not in ('released','active'):raise Conflict('Unknown prior claim state')
        epoch=(old.get('epoch',0)+1) if old else 1
        stamp=now_utc();ref=st['ref']
        record={'schema_version':'1.0.0','run_id':run,'task_id':task,'ref':ref,'state':'active',
             'actor':actor,'git_authenticated_user':'unverified_not_equivalent_to_actor',
             'token':uuid.uuid4().hex,'epoch':epoch,'acquired_at':iso(stamp),
             'expires_at':iso(stamp+dt.timedelta(seconds=lease_seconds)),
             'prior_tip':st['sha'],'reclaim_reason':reclaim_reason if explicit_reclaim else None,
             'guarantee':'git_ref_cas_only_external_actions_not_fenced'}
        new=self._commit(record,st['sha']);self._push(new,ref,st['sha'])
        return {'ref':ref,'sha':new,'record':record,'mode':'enforced_git_ref_cas_local_or_verified_remote'}
    def verify(self,run,task,token,epoch):
        st=self.status(run,task);rec=st['record']
        if not rec or rec.get('state')!='active' or rec.get('token')!=token or rec.get('epoch')!=epoch:
            raise Conflict('Claim token/epoch no longer current: do not write or perform external actions')
        if at(rec['expires_at'])<=now_utc():raise Conflict('Claim expired: stop and reconcile, no automatic takeover')
        return st
    def release(self,run,task,actor,token,epoch):
        if not valid_actor(actor):raise Unauthorized('Four-part actor required')
        st=self.verify(run,task,token,epoch)
        rec={**st['record'],'state':'released','released_at':iso(now_utc()),'released_by':actor}
        new=self._commit(rec,st['sha']);self._push(new,st['ref'],st['sha'])
        return {'ref':st['ref'],'sha':new,'record':rec}
    def sync_probe(self,branch='main'):
        if not safe_id(branch):raise GitCoordinationError('Unsafe branch')
        # Always fetch before using remote-tracking state; cannot silently auto-merge conflicts.
        status=self.run('status','--porcelain').stdout
        tip=self.remote_tip('refs/heads/'+branch)
        if not tip:return {'status':'BLOCKED','reason':'Branch missing on remote'}
        self.run('fetch','--no-tags',self.remote,'refs/heads/'+branch)
        head=self.run('rev-parse','HEAD').stdout.strip()
        clean=not status.strip()
        if head==tip:return {'status':'SYNCED' if clean else 'DIRTY','remote_tip':tip,'local_tip':head,'clean':clean}
        ahead=self.run('merge-base','--is-ancestor',head,tip,allow_failure=True).returncode==0
        behind=self.run('merge-base','--is-ancestor',tip,head,allow_failure=True).returncode==0
        return {'status':'BEHIND' if ahead else 'AHEAD' if behind else 'DIVERGED','remote_tip':tip,'local_tip':head,'clean':clean,
                'next_action':'Fast-forward only when clean' if ahead else 'Stop; do not force push or auto-resolve'}
    def sync_refresh(self,branch='main'):
        scan=self.sync_probe(branch)
        if scan['status']=='SYNCED':return scan
        if scan['status']=='BEHIND' and scan['clean']:
            self.run('merge','--ff-only','FETCH_HEAD');return self.sync_probe(branch)
        raise Conflict('Remote/local mismatch or dirty worktree; preserve local changes, reconcile manually')
    def sync_commit(self,paths,actor,branch='main',message='AOS-W run checkpoint'):
        if not valid_actor(actor):raise Unauthorized('Actor required')
        pre=self.sync_probe(branch)
        if pre['status'] not in ('SYNCED','DIRTY'):raise Conflict('Check remote updates before committing; no automatic conflict merge')
        if not paths or any(not isinstance(p,str) or not p.startswith('scaffold/aos-w/agent-files/') or '..' in Path(p).parts or Path(p).is_absolute() for p in paths):
            raise Unauthorized('Only explicit agent-files paths may be staged by this adapter')
        self.run('add','--',*paths)
        changes=self.run('diff','--cached','--name-only').stdout.splitlines()
        if not changes:raise GitCoordinationError('No staged changes')
        if any(not p.startswith('scaffold/aos-w/agent-files/') for p in changes):raise Unauthorized('Other staged changes present; unstage manually before sync')
        trailer=f"Agent-Provenance: [{actor['agent']} | {actor['platform']} | {actor['role']} | {actor['instance']}]"
        self.run('commit','-m',message+'\n\n'+trailer)
        p=self.run('push',self.remote,f'HEAD:refs/heads/{branch}',allow_failure=True)
        if p.returncode:raise Conflict('Git push rejected/unknown: fetch and inspect remote before retry or merge')
        remote=self.remote_tip('refs/heads/'+branch)
        local=self.run('rev-parse','HEAD').stdout.strip()
        if remote!=local:raise GitCoordinationError('Remote push not verified')
        return {'status':'SYNCED','sha':local,'actor':actor}

class LFSLockPrototype:
    """Git-LFS file lock candidate, unavailable unless actual git-lfs and server exist."""
    def __init__(self,client:GitClient):self.git=client
    def available(self):return self.git.run('lfs','version',allow_failure=True).returncode==0
    def lock(self,file,actor):
        if not valid_actor(actor):raise Unauthorized('Agent provenance required')
        p=Path(file)
        if p.is_absolute() or '..' in p.parts or not str(p).startswith('scaffold/aos-w/agent-files/'):
            raise Unauthorized('LFS prototype only locks agent-files paths')
        if not (self.git.repo/p).is_file():raise GitCoordinationError('Git LFS locking requires an existing worktree file')
        if not self.available():raise Offline('Git LFS executable unavailable, cannot claim tested live lock')
        result=self.git.run('lfs','lock','--json',str(p))
        try: lock=json.loads(result.stdout)['lock']
        except (KeyError,ValueError) as e:raise GitCoordinationError('Unrecognized LFS lock response') from e
        return {'lock':lock,'actor':actor,'warning':'Git LFS server owner is Git account, not logical agent; no same-account isolation'}
    def verify(self,path):
        if not self.available():raise Offline('Git LFS unavailable')
        p=self.git.run('lfs','locks','--verify','--json')
        try:return json.loads(p.stdout)
        except ValueError as e:raise GitCoordinationError('Bad locks verification') from e
    def unlock(self,lock_id,actor):
        if not valid_actor(actor):raise Unauthorized('Actor required')
        if not self.available():raise Offline('Git LFS unavailable')
        if not lock_id:raise GitCoordinationError('Lock ID required')
        return json.loads(self.git.run('lfs','unlock','--json','--id='+lock_id).stdout)
