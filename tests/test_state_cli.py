"""Smoke test optional CLI with real temporary files and no providers."""
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
ACTOR={'agent':'smoke','platform':'test-cli','role':'worker','instance':'new-session'}
class CliSmoke(unittest.TestCase):
    def test_inspect_recover_checkpoint(self):
        sys.path.insert(0,str(ROOT/'tools/state'))
        from state import RunStore
        with tempfile.TemporaryDirectory() as d:
            inst=Path(d)/'aos-w/agent-files/instances/test-1';(inst/'graph-revisions').mkdir(parents=True)
            graph={'nodes':[{'id':'scope','needs':[],'kind':'task','instructions':'Write scope',
                    'inputs':[],'outputs':[{'artifact_id':'scope','path':'artifacts/scope.md'}],
                    'quality':{'gates':[]},'contract':{'done_when':'Write scope'},'required_actions':['write_local']}]}
            (inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':graph}))
            run=inst/'runs/run-001';RunStore.create(run,graph,'run-001',ACTOR)
            def cli(action,*args):
                z=subprocess.run([sys.executable,str(ROOT/'tools/state/cli.py'),str(run),action,*args],text=True,capture_output=True)
                self.assertEqual(z.returncode,0,z.stderr)
                return json.loads(z.stdout)
            self.assertEqual(cli('inspect')['run_status'],'CREATED')
            self.assertEqual(cli('checkpoint','--actor',json.dumps(ACTOR))['event_seq'],1)
            self.assertEqual(cli('recover','--actor',json.dumps(ACTOR))['issues'],[])
            self.assertEqual(cli('inspect')['last_event_seq'],3)
if __name__=='__main__':unittest.main()
