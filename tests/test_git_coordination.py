"""Prompt 13 experiments: real local Git bare remote; no GitHub/network, no LFS server."""
from __future__ import annotations
import concurrent.futures, datetime as dt, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/git'))
from coordination import GitClient, LFSLockPrototype, Conflict, Offline, Unauthorized, GitCoordinationError, iso, now_utc

A={'agent':'Max','platform':'ChatGPT','role':'worker','instance':'process-a'}
B={'agent':'Fred','platform':'Codex','role':'worker','instance':'process-b'}

def cmd(cwd,*args):
    p=subprocess.run(['git',*args],cwd=cwd,text=True,capture_output=True)
    if p.returncode:raise AssertionError((args,p.stdout,p.stderr))
    return p.stdout.strip()

class LocalRemoteTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.base=Path(self.t.name)
        self.remote=self.base/'server.git';cmd(self.base,'init','--bare',str(self.remote))
        self.seed=self.base/'seed';cmd(self.base,'init','-b','main',str(self.seed))
        cmd(self.seed,'config','user.name','Shared Git Login');cmd(self.seed,'config','user.email','shared@example.invalid')
        f=self.seed/'scaffold/aos-w/agent-files/README.md';f.parent.mkdir(parents=True);f.write_text('# user data\n')
        cmd(self.seed,'add','.');cmd(self.seed,'commit','-m','seed');cmd(self.seed,'remote','add','origin',str(self.remote));cmd(self.seed,'push','-u','origin','main')
        cmd(self.remote,'symbolic-ref','HEAD','refs/heads/main')
        self.a=self.base/'a';self.b=self.base/'b'
        for path in (self.a,self.b):
            cmd(self.base,'clone',str(self.remote),str(path));cmd(path,'config','user.name','Shared Git Login');cmd(path,'config','user.email','shared@example.invalid')
        self.ca=GitClient(self.a);self.cb=GitClient(self.b)
    def test_unique_claim_winner_and_shared_authentication(self):
        x=self.ca.acquire('run-001','step-001',A)
        self.assertEqual(x['record']['actor'],A)
        with self.assertRaises(Conflict):self.cb.acquire('run-001','step-001',B)
        self.assertEqual(self.cb.status('run-001','step-001')['record']['actor'],A)
        self.assertEqual(cmd(self.a,'config','user.email'),cmd(self.b,'config','user.email'))
    def test_simultaneous_competing_pushes_across_distinct_clones(self):
        def go(i):
            client=self.ca if i==0 else self.cb
            try:return 'WIN',client.acquire('run-001','race-001',A if i==0 else B)
            except Conflict as exc:return 'CONFLICT',str(exc)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(go,[0,1]))
        self.assertEqual([r[0] for r in results].count('WIN'),1,results)
        self.assertEqual([r[0] for r in results].count('CONFLICT'),1,results)
        winner=next(x[1] for x in results if x[0]=='WIN')
        self.assertEqual(self.ca.status('run-001','race-001')['sha'],winner['sha'])
    def test_multiple_races_retain_exactly_one_ref_winner(self):
        for n in range(6):
            def attempt(i):
                c=self.ca if i==0 else self.cb
                try:return c.acquire('run-001','race-%02d'%n,A if i==0 else B)
                except Conflict:return None
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:v=list(pool.map(attempt,[0,1]))
            self.assertEqual(sum(x is not None for x in v),1,v)
    def test_stale_claim_fails_if_owner_releases_and_new_owner_claims(self):
        first=self.ca.acquire('run-001','step-001',A)
        self.ca.release('run-001','step-001',A,first['record']['token'],first['record']['epoch'])
        second=self.cb.acquire('run-001','step-001',B)
        self.assertEqual(second['record']['epoch'],first['record']['epoch']+1)
        with self.assertRaises(Conflict):self.ca.verify('run-001','step-001',first['record']['token'],first['record']['epoch'])
        with self.assertRaises(Conflict):self.ca.release('run-001','step-001',A,first['record']['token'],first['record']['epoch'])
    def test_expiration_does_not_silently_grant_takeover(self):
        claim=self.ca.acquire('run-001','step-001',A)
        ref=claim['ref'];sha=claim['sha']
        expired=dict(claim['record'],expires_at=iso(now_utc()-dt.timedelta(minutes=60)))
        ext=self.ca._commit(expired,sha);self.ca._push(ext,ref,sha)
        with self.assertRaises(Conflict):self.cb.acquire('run-001','step-001',B)
        with self.assertRaises(Unauthorized):self.cb.acquire('run-001','step-001',B,explicit_reclaim=True)
        new=self.cb.acquire('run-001','step-001',B,explicit_reclaim=True,reclaim_reason='Owner checked remote audit and explicitly authorized stale claim reassignment')
        self.assertEqual(new['record']['epoch'],2)
        self.assertEqual(new['record']['reclaim_reason'][:5],'Owner')
        with self.assertRaises(Conflict):self.ca.verify('run-001','step-001',claim['record']['token'],1)
    def test_offline_partition_blocks_claim_and_verification(self):
        x=self.ca.acquire('run-001','step-001',A)
        cmd(self.b,'remote','set-url','origin',str(self.base/'missing_remote.git'))
        with self.assertRaises(Offline):self.cb.acquire('run-001','other-001',B)
        with self.assertRaises(Offline):self.cb.verify('run-001','step-001',x['record']['token'],x['record']['epoch'])
        with self.assertRaises(Offline):self.cb.release('run-001','step-001',B,x['record']['token'],x['record']['epoch'])
    def test_sync_fast_forward_and_divergence_fail_closed(self):
        p=self.a/'scaffold/aos-w/agent-files/sample.json';p.write_text('1\n')
        ack=self.ca.sync_commit(['scaffold/aos-w/agent-files/sample.json'],A)
        self.assertEqual(ack['status'],'SYNCED')
        self.assertEqual(self.cb.sync_probe()['status'],'BEHIND')
        self.assertEqual(self.cb.sync_refresh()['status'],'SYNCED')
        # two editors independently create conflicting local commits
        p.write_text('changed by A\n');cmd(self.a,'add','scaffold/aos-w/agent-files/sample.json');cmd(self.a,'commit','-m','edit A')
        p2=self.b/'scaffold/aos-w/agent-files/sample.json';p2.write_text('changed by B\n')
        cmd(self.b,'add','scaffold/aos-w/agent-files/sample.json');cmd(self.b,'commit','-m','edit B')
        cmd(self.a,'push','origin','main')
        self.assertEqual(self.cb.sync_probe()['status'],'DIVERGED')
        with self.assertRaises(Conflict):self.cb.sync_refresh()
        self.assertEqual(p2.read_text(),'changed by B\n')
    def test_dirty_workspace_refuses_auto_refresh(self):
        f=self.a/'scaffold/aos-w/agent-files/fresh.json';f.write_text('from A\n')
        self.ca.sync_commit(['scaffold/aos-w/agent-files/fresh.json'],A)
        dirty=self.b/'scaffold/aos-w/agent-files/README.md';dirty.write_text('unsaved local changes\n')
        with self.assertRaises(Conflict):self.cb.sync_refresh()
        self.assertEqual(dirty.read_text(),'unsaved local changes\n')
    def test_unaudited_local_ahead_history_is_not_silently_pushed(self):
        other=self.a/'README.md';other.write_text('unexpected framework edit\n')
        cmd(self.a,'add','README.md');cmd(self.a,'commit','-m','out of scope change')
        sample=self.a/'scaffold/aos-w/agent-files/fresh.json';sample.write_text('value\n')
        with self.assertRaises(Conflict):self.ca.sync_commit(['scaffold/aos-w/agent-files/fresh.json'],A)
        self.assertNotIn('README.md',self.ca.run('ls-remote','origin','refs/heads/main').stdout)
    def test_no_unscoped_git_staging(self):
        with self.assertRaises(Unauthorized):self.ca.sync_commit(['README.md'],A)
        with self.assertRaises(Unauthorized):self.ca.sync_commit(['../../secret'],A)
        with self.assertRaises(Unauthorized):self.ca.sync_commit(['scaffold/aos-w/agent-files/../../PROTOCOL.md'],A)
    def test_lfs_not_installed_and_no_false_success(self):
        # Explicitly simulate missing LFS, independent of the host's installed packages.
        # GitHub Actions runners may include git-lfs even if the developer VM does not.
        import subprocess
        class NoLFSClient:
            def __init__(self,repo): self.repo=repo
            def run(self,*args,allow_failure=False):
                return subprocess.CompletedProcess(args,1,stdout='',stderr='git-lfs not installed')
        proto=LFSLockPrototype(NoLFSClient(self.a))
        self.assertFalse(proto.available(),'Simulated client must remain unavailable')
        p=self.a/'scaffold/aos-w/agent-files/README.md'
        with self.assertRaises(Offline):proto.lock(str(p.relative_to(self.a)),A)
    def test_mocked_lfs_result_uses_git_account_not_agent(self):
        class Fake:
            repo=Path('/tmp')
            def run(self,*args,allow_failure=False):
                class P:
                    returncode=0
                    stdout=json.dumps({'ours':[{'id':'lfs-001','owner':{'name':'Shared Git Login'},'path':'same-file'}],'theirs':[]})
                return P()
        ans=LFSLockPrototype(Fake()).verify('same-file')
        self.assertEqual(ans['ours'][0]['owner']['name'],'Shared Git Login')
        self.assertNotIn('instance',ans['ours'][0]['owner'])
    def test_cli_smoke_records_remote_observation_inside_agent_files(self):
        import sys
        target=self.a/'scaffold/aos-w/agent-files/config/sync-state.json'
        program=Path(__file__).resolve().parents[1]/'tools/git/cli.py'
        result=subprocess.run([sys.executable,str(program),'--repo',str(self.a),'--sync-state',str(target),
                               'sync-status'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        state=json.loads(target.read_text())
        self.assertEqual(state['status'],'verified_remote_response')
        self.assertEqual(state['mode'],'git_mirrored_single_writer')
        self.assertTrue(json.loads(result.stdout)['status'] in ('SYNCED','DIRTY'))
        self.assertNotIn('password',state)
    def test_read_only_claim_probe_does_not_create_remote_refs(self):
        self.assertIsNone(self.ca.status('run-001','unknown')['sha'])
        refs=cmd(self.remote,'for-each-ref','--format=%(refname)','refs/heads/aosw-claims')
        self.assertEqual(refs,'')
    def test_invalid_actor_ref_and_no_auto_reclaim(self):
        with self.assertRaises(Unauthorized):self.ca.acquire('run-001','step-001',{'agent':'same'})
        with self.assertRaises(GitCoordinationError):self.ca.acquire('../oops','step-001',A)
        with self.assertRaises(GitCoordinationError):self.ca.acquire('run-001','step-001',A,lease_seconds=1)

if __name__=='__main__':unittest.main()
