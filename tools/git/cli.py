"""Optional Git-backed coordination CLI. No server or Python requirement for standalone AOS-W."""
from __future__ import annotations
import argparse, json, sys, tempfile, os
from pathlib import Path
from coordination import GitClient, LFSLockPrototype, GitCoordinationError, now_utc, iso, valid_actor

def actor_value(value):
    if not value:return None
    if value.lstrip().startswith('{'):return json.loads(value)
    p=Path(value)
    return json.loads(p.read_text()) if p.is_file() else json.loads(value)

def record_sync(path, data):
    """Only write state inside an existing agent-files config directory; no credentials."""
    if not path:return
    dest=Path(path).resolve()
    if dest.name!='sync-state.json' or dest.parent.name!='config' or dest.parent.parent.name!='agent-files':
        raise GitCoordinationError('sync-state must be agent-files/config/sync-state.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    value={'schema_version':'1.0.0','checked_at':iso(now_utc()),**data}
    fd,tmp=tempfile.mkstemp(prefix='.sync-state-',dir=str(dest.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            json.dump(value,stream,indent=2,sort_keys=True);stream.write('\n');stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,dest)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def main(argv=None):
    p=argparse.ArgumentParser(description='Optional Git sync/CAS claim prototype (no provider writes)')
    p.add_argument('--repo',required=True,help='Existing Git checkout containing scaffold/aos-w/agent-files/')
    p.add_argument('--remote',default='origin')
    p.add_argument('--namespace',default='aosw-claims')
    p.add_argument('--sync-state',help='Optional <checkout>/scaffold/aos-w/agent-files/config/sync-state.json')
    p.add_argument('action',choices=['sync-status','sync-refresh','claim-status','claim','claim-verify','claim-release','lfs-probe','lfs-verify','lfs-lock','lfs-unlock'])
    p.add_argument('--run')
    p.add_argument('--task')
    p.add_argument('--actor',help='JSON literal or actor.json; exact [Agent | Platform | Role | Instance]')
    p.add_argument('--token')
    p.add_argument('--epoch',type=int)
    p.add_argument('--duration',type=int,default=1800)
    p.add_argument('--reclaim',action='store_true',help='Explicit stale claim reassignment; requires reason')
    p.add_argument('--reason')
    p.add_argument('--path',help='Repo-relative LFS lockable path (existing)')
    p.add_argument('--lock-id')
    p.add_argument('--branch',default='main')
    a=p.parse_args(argv)
    result=None
    try:
        client=GitClient(a.repo,a.remote,a.namespace)
        actor=actor_value(a.actor)
        if a.action in ('claim','claim-release','lfs-lock','lfs-unlock') and not valid_actor(actor):
            raise GitCoordinationError('Acting agent identity required')
        if a.action=='sync-status':result=client.sync_probe(a.branch)
        elif a.action=='sync-refresh':result=client.sync_refresh(a.branch)
        elif a.action=='claim-status':result=client.status(a.run,a.task)
        elif a.action=='claim':result=client.acquire(a.run,a.task,actor,lease_seconds=a.duration,explicit_reclaim=a.reclaim,reclaim_reason=a.reason)
        elif a.action=='claim-verify':result=client.verify(a.run,a.task,a.token,a.epoch)
        elif a.action=='claim-release':result=client.release(a.run,a.task,actor,a.token,a.epoch)
        elif a.action=='lfs-probe':result={'available':LFSLockPrototype(client).available(),'status':'NOT_TESTED_LIVE' if not LFSLockPrototype(client).available() else 'client_installed_server_not_yet_verified'}
        elif a.action=='lfs-verify':result=LFSLockPrototype(client).verify(a.path)
        elif a.action=='lfs-lock':result=LFSLockPrototype(client).lock(a.path,actor)
        elif a.action=='lfs-unlock':result=LFSLockPrototype(client).unlock(a.lock_id,actor)
        if a.sync_state and a.action.startswith(('sync-', 'claim-')):
            record_sync(a.sync_state,{'action':a.action,'status':'verified_remote_response','remote':a.remote,'branch':a.branch,'mode':'shared_coordinated' if a.action.startswith('claim-') else 'git_mirrored_single_writer',
              'last_verified_remote_sha':result.get('sha') or result.get('remote_tip'),'actor':actor,'note':'Git remote sync/claim observation; no provider authorization'})
        print(json.dumps(result,indent=2,default=str));return 0
    except (GitCoordinationError,OSError,ValueError) as exc:
        if a.sync_state:
            try:record_sync(a.sync_state,{'action':a.action,'status':'BLOCKED_OR_UNVERIFIED','reason':str(exc)[:300],'remote':a.remote,'mode':'shared_coordinated' if a.action.startswith('claim-') else 'git_mirrored_single_writer'})
            except Exception:pass
        print(json.dumps({'status':'BLOCKED','error':str(exc),'safe_action':'do_not_replay_or_overwrite; preserve work and reconcile remote when reachable'}),file=sys.stderr)
        return 2
if __name__=='__main__':raise SystemExit(main())
