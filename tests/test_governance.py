"""Synthetic single-writer governance tests: no trusted users/provider APIs/distributed mutex."""
from __future__ import annotations
import copy, datetime as dt, hashlib, json, sys, tempfile, unittest
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/governance'))
sys.path.insert(0,str(ROOT/'tools/state'))
from governance import Governance, Unauthorized, identity_string
from state import RunStore, StateError, digest, utcnow

WORKER={'agent':'Max','platform':'ChatGPT','role':'worker','instance':'s1'}
REVIEWER={'agent':'Fred','platform':'Codex','role':'reviewer','instance':'s2'}
VALIDATOR={'agent':'schema','platform':'local','role':'validator','instance':'v1'}
HUMAN={'agent':'Owner','platform':'human','role':'owner','instance':'approval-ui'}
OTHER={'agent':'Claude','platform':'Claude','role':'worker','instance':'s3'}


def node(name,needs=(),gates=(),actions=None):
    return {'id':name,'kind':'task','needs':list(needs),'inputs':[],
            'outputs':[{'artifact_id':name+'-out','path':'artifacts/'+name+'.md','required':True}],
            'quality':{'gates':list(gates)},'instructions':'Draft evidence for '+name,
            'contract':{'done_when':'Verified artifact + current quality gates'},
            'required_actions':actions or ['write_local'],
            'retry':{'max_attempts':3,'on':['review_revise','incomplete_evidence'],'backoff':'manual'}}

class GovernanceConformance(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.inst=Path(self.temp.name)/'aos-w/agent-files/instances/example'
        self.run=self.inst/'runs/run-001';(self.inst/'graph-revisions').mkdir(parents=True)
        self.graph={'nodes':[node('draft',gates=['auto','independent']),node('dependent',['draft']),
                             node('parallel'),node('send',['draft'],actions=['send_message']),
                             node('human-review',gates=['owner-gate'])]}
        self.policy={'autonomy':'bounded','allowed_actions':['read','write_local','review','send_message'],
            'human_required_actions':['send_message'],'default_gates':[],
            'max_parallel_tasks':1,'allow_dynamic_children':False}
        self.gates=[{'gate_id':'auto','kind':'deterministic','required':True,'rubric_id':'file-hash'},
                    {'gate_id':'independent','kind':'ai_independent','required':True,'rubric_id':'source-evidence'},
                    {'gate_id':'owner-gate','kind':'human','required':True,'rubric_id':'owner-choice'}]
        (self.inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':self.graph,'policy':self.policy,'gates':self.gates}))
        self.store=RunStore.create(self.run,self.graph,'run-001',WORKER)
        self.gov=Governance(self.run)
    def expiry(self,seconds=3600):
        return (dt.datetime.now(dt.timezone.utc)+dt.timedelta(seconds=seconds)).isoformat()
    def out(self,task,content=None,revision='v1'):
        s=content or 'Actual bounded evidence for '+task
        target=self.run/'artifacts'/(task+'.md');target.parent.mkdir(exist_ok=True)
        target.write_text(s)
        return [{'artifact_id':task+'-out','locator':'artifacts/'+task+'.md',
                 'revision':revision,'sha256':digest(s.encode())}]
    def claim_begin(self,task,who=WORKER,resources=None):
        self.gov.claim('claim-'+task+'-'+str(self.store.verified()['tasks'][task]['attempts']),task,who,self.expiry(),resources=resources)
        self.gov.begin(task,who)
    def complete_draft(self):
        self.claim_begin('draft');out=self.out('draft')
        self.gov.submit_review('draft',WORKER)
        self.gov.review('r-auto','draft',WORKER,VALIDATOR,'auto',out,'PASS')
        self.gov.review('r-independent','draft',WORKER,REVIEWER,'independent',out,'PASS')
        self.gov.finalize('draft',WORKER,out)
        return out

    def test_four_field_identity_and_commit_trailer(self):
        self.assertEqual(identity_string(WORKER),'[Max | ChatGPT | worker | s1]')
        with self.assertRaises(Unauthorized):identity_string({'agent':'Max','role':'worker'})

    def test_claim_identity_and_handoff_provenance(self):
        rec=self.gov.claim('claim-draft-0','draft',WORKER,self.expiry())
        self.assertEqual(rec['mode'],'advisory')
        self.assertEqual(rec['actor']['instance'],'s1')
        with self.assertRaises(Unauthorized):self.gov.begin('draft',OTHER)
        self.gov.begin('draft',WORKER)
        h=self.gov.handoff(WORKER,'Request independent review after drafting','Evidence drafting in progress')
        self.assertEqual(h['actor']['platform'],'ChatGPT')
        self.assertIn('claim-draft-0',str(h['claims']))
        self.assertIn('Next: Request independent review', (self.run/'handoff.md').read_text())
        es=[json.loads(x) for x in (self.run/'events.jsonl').read_text().splitlines()]
        self.assertIn('governance_handoff',[e['type'] for e in es])

    def test_claim_conflicts_and_expiry_not_hard_lock(self):
        self.gov.claim('claim-draft-0','draft',WORKER,self.expiry())
        with self.assertRaises(Unauthorized):self.gov.claim('claim-other','draft',OTHER,self.expiry())
        with self.assertRaises(Unauthorized):self.gov.begin('draft',OTHER)
        rec=json.loads((self.run/'claims/claim-draft-0.json').read_text())
        self.assertEqual(rec['extensions']['lease_guarantee'],'none')
        self.gov.release('claim-draft-0','release-draft',WORKER,'Manual stop')
        self.gov.claim('claim-draft-1','draft',OTHER,self.expiry())
        self.assertEqual(self.store.verified()['tasks']['draft']['status'],'CLAIMED')

    def test_dependency_blocked_while_parallel_ready(self):
        with self.assertRaises(Unauthorized):self.gov.claim('premature','dependent',WORKER,self.expiry())
        self.claim_begin('parallel')
        self.gov.finalize('parallel',WORKER,self.out('parallel'))
        self.assertEqual(self.store.verified()['tasks']['parallel']['status'],'COMPLETE')
        self.assertEqual(self.store.verified()['tasks']['dependent']['status'],'WAIT_DEPENDENCY')

    def test_deterministic_independent_and_all_gates_required(self):
        self.claim_begin('draft');out=self.out('draft');self.gov.submit_review('draft',WORKER)
        self.gov.review('r1','draft',WORKER,VALIDATOR,'auto',out,'PASS')
        with self.assertRaises(Unauthorized):self.gov.finalize('draft',WORKER,out)
        with self.assertRaises(Unauthorized):self.gov.review('r-self-fake','draft',WORKER,{**WORKER,'role':'reviewer'},'independent',out,'PASS')
        self.gov.review('r2','draft',WORKER,REVIEWER,'independent',out,'PASS')
        self.gov.finalize('draft',WORKER,out)
        self.assertEqual(self.store.verified()['tasks']['draft']['status'],'COMPLETE')
        self.assertEqual(self.store.verified()['tasks']['dependent']['status'],'WAIT_DEPENDENCY')
        self.assertIn('dependent',self.store.verified()['eligible_tasks'])

    def test_review_fails_and_remediation_then_resubmission(self):
        self.claim_begin('draft');old=self.out('draft',content='Initial ambiguous findings')
        self.gov.submit_review('draft',WORKER)
        self.gov.review('qc-fail','draft',WORKER,REVIEWER,'independent',old,'REVISE',correction='Add source citations')
        self.assertEqual(self.store.verified()['tasks']['draft']['status'],'NEEDS_REWORK')
        self.assertNotIn('dependent',self.store.verified()['eligible_tasks'])
        self.assertIn('parallel',self.store.verified()['eligible_tasks'])
        with self.assertRaises(Unauthorized):self.gov.resubmit('draft',WORKER,'qc-fail','')
        self.gov.resubmit('draft',WORKER,'qc-fail','Added independent source citations')
        self.gov.release('claim-draft-0','release-old',WORKER,'Failed QC; new attempt')
        self.gov.claim('claim-draft-1','draft',WORKER,self.expiry())
        self.gov.begin('draft',WORKER)
        revised=self.out('draft',content='Cited and corrected findings',revision='v2')
        self.gov.submit_review('draft',WORKER)
        self.gov.review('qc-pass-auto','draft',WORKER,VALIDATOR,'auto',revised,'PASS')
        self.gov.review('qc-pass-peer','draft',WORKER,REVIEWER,'independent',revised,'PASS')
        self.gov.finalize('draft',WORKER,revised)
        self.assertEqual(self.store.verified()['tasks']['draft']['attempts'],2)
        self.assertEqual(self.store.verified()['tasks']['draft']['status'],'COMPLETE')
        self.assertEqual(json.loads((self.run/'reviews/qc-fail.json').read_text())['verdict'],'REVISE')

    def test_wrong_artifact_revision_cannot_reuse_old_pass(self):
        self.claim_begin('draft');out=self.out('draft');self.gov.submit_review('draft',WORKER)
        self.gov.review('review-a','draft',WORKER,VALIDATOR,'auto',out,'PASS')
        self.gov.review('review-b','draft',WORKER,REVIEWER,'independent',out,'PASS')
        changed=self.out('draft',content='Different bytes',revision='v2')
        with self.assertRaises(Unauthorized):self.gov.finalize('draft',WORKER,changed)
        self.assertEqual(self.store.verified()['tasks']['draft']['status'],'WAIT_REVIEW')

    def test_human_gate_and_self_review_not_inferred(self):
        self.claim_begin('human-review');out=self.out('human-review');self.gov.submit_review('human-review',WORKER)
        with self.assertRaises(Unauthorized):self.gov.review('fake-human','human-review',WORKER,REVIEWER,'owner-gate',out,'PASS')
        self.gov.review('actual-human-declared','human-review',WORKER,HUMAN,'owner-gate',out,'PASS')
        self.gov.finalize('human-review',WORKER,out)
        self.assertEqual(self.store.verified()['tasks']['human-review']['status'],'COMPLETE')

    def test_action_denied_before_scope_grant_and_no_wildcard(self):
        self.complete_draft()
        with self.assertRaises(Unauthorized):self.gov.claim('claim-send','send',WORKER,self.expiry(),resources=['thread-1'])
        with self.assertRaises(Unauthorized):self.gov.grant('g-wildcard',HUMAN,['send_message'],['*'])
        self.gov.grant('g1',HUMAN,['send_message'],['thread-1'],task_id='send')
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'send_message',['thread-2'],'send')
        self.assertEqual(self.gov.authorize(WORKER,'send_message',['thread-1'],'send')['approval_id'],'g1')
        self.gov.claim('claim-send','send',WORKER,self.expiry(),resources=['thread-1'])
        self.gov.begin('send',WORKER)
        self.gov.operation_intent('send',WORKER,'send_message',['thread-1'],'mock-provider','thread-1',{'body':'draft-only'})
        self.assertEqual(len(self.store.verified()['pending_provider_operations']),1)
        # DOES NOT SEND anything. The operation is only an intentional local record.

    def test_permission_rechecked_after_claim_before_start(self):
        self.complete_draft()
        self.gov.grant('timebound',HUMAN,['send_message'],['thread-1'],task_id='send',expires_at=self.expiry(120))
        self.gov.claim('claim-send','send',WORKER,self.expiry(120),resources=['thread-1'])
        self.gov.revoke('timebound','timebound-revoke',HUMAN,'Do not proceed')
        with self.assertRaises(Unauthorized):self.gov.begin('send',WORKER)
        self.assertEqual(self.store.verified()['tasks']['send']['status'],'CLAIMED')

    def test_grant_expiry_revocation_and_version(self):
        self.complete_draft()
        self.gov.grant('p1',HUMAN,['send_message'],['thread-1'],task_id='send',expires_at=self.expiry(60))
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'send_message',['thread-1'],'send',now=self.expiry(120))
        self.assertEqual(self.gov.authorize(WORKER,'send_message',['thread-1'],'send')['approval_id'],'p1')
        self.gov.revoke('p1','p1-revoke',HUMAN,'Owner withdrew approval')
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'send_message',['thread-1'],'send')
        self.gov.grant('p2',HUMAN,['send_message'],['thread-1'],task_id='send')
        # Simulate revision invalidation in a separate pinned run: contract expects matching current graph.
        self.store.run_data['current_graph_revision']='g0001'  # no real rewrite
        self.assertEqual(self.gov.authorize(WORKER,'send_message',['thread-1'],'send')['approval_id'],'p2')
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'deploy_prod',['thread-1'],'send')

    def test_tampered_permission_file_is_rejected_against_event_history(self):
        self.complete_draft()
        self.gov.grant('grant-integrity',HUMAN,['send_message'],['thread-1'],task_id='send')
        file=self.run/'approvals/grant-integrity.json'
        record=json.loads(file.read_text());record['resource_ids'].append('thread-999')
        file.write_text(json.dumps(record))
        with self.assertRaises(Unauthorized):
            self.gov.authorize(WORKER,'send_message',['thread-999'],'send')

    def test_graph_revision_invalidates_old_permission_record(self):
        self.gov.grant('old-grant',HUMAN,['send_message'],['thread-1'],task_id='send')
        self.assertEqual(self.gov.authorize(WORKER,'send_message',['thread-1'],'send')['approval_id'],'old-grant')
        # Separate approved graph revision, old grants pinned to g0001 become unusable for g0002.
        proposed=copy.deepcopy(self.graph)
        proposed['nodes'][0]['instructions']='Different bounded research scope'
        self.store.revise('g0002',yaml.safe_dump({'graph':proposed,'policy':self.policy,'gates':self.gates}).encode(),
                          WORKER,{'decision':'GRANTED','action':'revise_graph','base_revision':'g0001','approval_id':'mock-revision'})
        with self.assertRaises(Unauthorized):
            self.gov.authorize(WORKER,'send_message',['thread-1'],'send')

    def test_budget_amount_required_and_bounded(self):
        self.gov.policy['allowed_actions'].append('change_budget')
        self.gov.grant('budget-approval',HUMAN,['change_budget'],['campaign-x'],limits={'max_amount':25})
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'change_budget',['campaign-x'],amount=None)
        with self.assertRaises(Unauthorized):self.gov.authorize(WORKER,'change_budget',['campaign-x'],amount=50)
        self.assertEqual(self.gov.authorize(WORKER,'change_budget',['campaign-x'],amount=20)['approval_id'],'budget-approval')

    def test_unauthorized_approval_issuer(self):
        with self.assertRaises(Unauthorized):self.gov.grant('bad-owner',WORKER,['send_message'],['thread-1'])
        with self.assertRaises(Unauthorized):self.gov.grant('bad-privilege',HUMAN,['deploy_prod'],['site-x'])

    def test_history_and_provenance_of_every_governance_record(self):
        self.complete_draft()
        events=[json.loads(x) for x in (self.run/'events.jsonl').read_text().splitlines()]
        self.assertTrue(all(set(('agent','platform','role','instance'))<=e['actor'].keys() for e in events))
        types=[e['type'] for e in events]
        self.assertIn('claim_recorded',types)
        self.assertEqual(types.count('quality_recorded'),2)
        self.assertIn('task_completed',types)
        governance=self.store.verified()['governance']
        self.assertEqual(len(governance['reviews']),2)
        self.assertEqual(len(governance['claims']),1)

    def test_policy_parallel_limit_is_not_ignored(self):
        self.gov.claim('claim-draft-0','draft',WORKER,self.expiry())
        with self.assertRaises(Unauthorized):
            self.gov.claim('claim-parallel','parallel',OTHER,self.expiry())
        self.gov.release('claim-draft-0','release-draft',WORKER,'Capacity change')
        self.gov.claim('claim-parallel','parallel',OTHER,self.expiry())

    def test_self_review_only_for_configured_gate(self):
        self.gates.append({'gate_id':'self-local','kind':'self_review','required':True,'rubric_id':'local'})
        self.gov.gates['self-local']=self.gates[-1]
        self.graph['nodes'].append(node('self-task',gates=['self-local']))
        # To create an expanded graph, make a *new independent instance*, not secretly edit the active graph.
        inst=Path(self.temp.name)/'aos-w/agent-files/instances/only-self'
        (inst/'graph-revisions').mkdir(parents=True)
        g={'nodes':[node('self-task',gates=['self-local'])]}
        (inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':g,'policy':self.policy,'gates':[self.gates[-1]]}))
        run=inst/'runs/run-002'
        RunStore.create(run,g,'run-002',WORKER)
        a=Governance(run)
        a.claim('self-claim','self-task',WORKER,self.expiry())
        a.begin('self-task',WORKER)
        file=run/'artifacts/self-task.md';file.parent.mkdir(exist_ok=True);file.write_text('checked locally')
        refs=[{'artifact_id':'self-task-out','locator':'artifacts/self-task.md','revision':'v1',
               'sha256':digest(b'checked locally')}]
        a.submit_review('self-task',WORKER)
        with self.assertRaises(Unauthorized):a.review('wrong-review','self-task',WORKER,REVIEWER,'self-local',refs,'PASS')
        a.review('self-ok','self-task',WORKER,WORKER,'self-local',refs,'PASS')
        a.finalize('self-task',WORKER,refs)
        self.assertEqual(a.store.verified()['tasks']['self-task']['status'],'COMPLETE')

if __name__=='__main__':unittest.main()
# Waiver test stays outside main test class to keep the core fixture unchanged.
class WaiverConformance(unittest.TestCase):
    def setUp(self): GovernanceConformance.setUp(self)
    claim_begin=GovernanceConformance.claim_begin
    expiry=GovernanceConformance.expiry
    out=GovernanceConformance.out
    def test_owner_waiver_preserved_not_passed(self):
        self.gates[1]['waivable']=True
        self.gov.gates['independent']['waivable']=True
        self.claim_begin('draft');out=self.out('draft');self.gov.submit_review('draft',WORKER)
        self.gov.review('pass-auto','draft',WORKER,VALIDATOR,'auto',out,'PASS')
        with self.assertRaises(Unauthorized):self.gov.waive_review('wrong-waiver','draft',WORKER,HUMAN,'auto',out,'Owner requests omission')
        self.gov.waive_review('waiver-peer','draft',WORKER,HUMAN,'independent',out,'Limited source access, approved bounded exception')
        self.gov.finalize('draft',WORKER,out)
        state=self.store.verified()
        self.assertIn('independent',state['tasks']['draft']['review']['waived_gate_ids'])
        self.assertEqual(state['tasks']['draft']['review']['quality_outcome'],'ACCEPTED_WITH_WAIVER')
        self.assertEqual(json.loads((self.run/'reviews/waiver-peer.json').read_text())['verdict'],'WAIVED_BY_OWNER')
