"""CLI subprocess tests deliberately use only a local file-only synthetic run."""
import json,subprocess,sys,unittest
from pathlib import Path
from test_governance import GovernanceConformance,WORKER,HUMAN
ROOT=Path(__file__).resolve().parents[1]
class GovernanceCLIConformance(unittest.TestCase):
    def setUp(self): GovernanceConformance.setUp(self)
    def test_cli_inspect_and_no_permission(self):
        tool=ROOT/'tools/governance/cli.py'
        base=[sys.executable,str(tool),str(self.run)]
        result=subprocess.run(base+['inspect'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['state']['run_status'],'CREATED')
        deny=subprocess.run(base+['authorize','--actor',json.dumps(WORKER),'--payload',json.dumps({
            'action':'send_message','resources':['thread-1'],'task_id':'send'})],capture_output=True,text=True)
        self.assertEqual(deny.returncode,2)
        self.assertIn('DENIED_OR_BLOCKED',deny.stderr)
