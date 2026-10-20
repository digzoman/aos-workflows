"""Local-only tests, no external APIs, no scheduler, no real user approvals."""
from __future__ import annotations
import copy, hashlib, json, tempfile, unittest, sys
from pathlib import Path
import yaml
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools/state'))
from state import RunStore, StateError, CorruptLog, digest, utcnow

ACTOR={'agent':'tester','platform':'local-tests','role':'worker','instance':'process-1'}
NEXT={'agent':'another','platform':'another-harness','role':'recovery','instance':'fresh-process'}

def node(ident,needs=(),gates=(),retry=None):
    n={'id':ident,'kind':'task' if not gates else 'review','needs':list(needs),'instructions':'Create output',
      'inputs':[],'outputs':[{'artifact_id':ident+'-result','path':'artifacts/'+ident+'.md','required':True}],
      'quality':{'gates':list(gates)},'contract':{'done_when':'Output verified'},'required_actions':['write_local']}
    if retry:n['retry']=retry
    return n

class PersistentStateConformance(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.inst=Path(self.temp.name)/'aos-w/agent-files/instances/fixture'
        self.root=self.inst/'runs/run-001'
        self.graph={'nodes':[node('a',retry={'max_attempts':2,'on':['source_unavailable','incomplete_evidence','transient_io'],'backoff':'fixed','delay_seconds':60}),node('b',['a'])]}
        (self.inst/'graph-revisions').mkdir(parents=True)
        (self.inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':self.graph}),encoding='utf-8')
        self.store=RunStore.create(self.root,self.graph,'run-001',ACTOR)
    def out(self,task='a',content='a result'):
        rel='artifacts/'+task+'.md';path=self.root/rel;path.parent.mkdir(exist_ok=True)
        path.write_text(content)
        return [{'artifact_id':task+'-result','locator':rel,'sha256':digest(content.encode()),'revision':'v1'}]
    def test_resume_across_clean_sessions(self):
        self.store.start('a',ACTOR)
        self.store.complete('a',ACTOR,self.out())
        cp=self.store.checkpoint(ACTOR)
        fresh=RunStore(self.root)
        s=fresh.verified()
        self.assertEqual(s['completed_steps'],['a']);self.assertEqual(s['eligible_tasks'],['b'])
        self.assertEqual(cp['event_seq'],5)
        fresh.start('b',NEXT);fresh.complete('b',NEXT,self.out('b'))
        self.assertEqual(fresh.verified()['run_status'],'COMPLETED')
        self.assertEqual(len(list((self.root/'tasks/a/attempts').glob('*.json'))),1)
        fresh.checkpoint(NEXT)
        self.assertIn('b',fresh.verified()['completed_steps'])

    def test_transient_retry_delay_attempt_history(self):
        self.store.start('a',ACTOR)
        self.store.fail('a',ACTOR,'source_unavailable','Try a different source')
        s=self.store.verified();self.assertEqual(s['tasks']['a']['status'],'BLOCKED')
        self.assertTrue(s['tasks']['a']['retry']['next_eligible_at'])
        with self.assertRaises(StateError):self.store.retry('a',ACTOR)
        self.store.retry('a',ACTOR,now='2099-01-01T00:00:00Z')
        self.store.start('a',NEXT)
        self.assertEqual(self.store.verified()['tasks']['a']['attempts'],2)
        self.store.complete('a',NEXT,self.out())
        self.assertEqual(len(list((self.root/'tasks/a/attempts').glob('*.json'))),2)

    def test_retry_cap_and_explicit_run_failure(self):
        self.store.start('a',ACTOR)
        self.store.fail('a',ACTOR,'source_unavailable','Try again',policy={'max_attempts':1,'on':['source_unavailable'],'backoff':'manual'})
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'FAILED')
        with self.assertRaises(StateError):self.store.retry('a',ACTOR)
        self.store.append('run_failed',ACTOR,payload={'reason':'User explicitly terminated after exhausted attempt'})
        self.assertEqual(self.store.verified()['run_status'],'FAILED')

    def test_missing_evidence_never_completes_and_requires_correction(self):
        self.store.start('a',ACTOR)
        with self.assertRaises(StateError):self.store.complete('a',ACTOR,[])
        with self.assertRaises(StateError):self.store.complete('a',ACTOR,[{'artifact_id':'a-result','locator':'artifacts/a.md','sha256':'bad','revision':'v1'}])
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'RUNNING')
        self.store.fail('a',ACTOR,'incomplete_evidence','Recheck date and source')
        with self.assertRaises(StateError):self.store.retry('a',ACTOR,now='2099-01-01T00:00:00Z')
        self.store.retry('a',ACTOR,approval=True,now='2099-01-01T00:00:00Z')
        self.store.start('a',ACTOR)
        self.store.complete('a',ACTOR,self.out())

    def test_quality_rejection_then_version_bound_review(self):
        g={'nodes':[node('review',gates=['human-qc'])]}
        (self.inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':g}))
        # Fresh created run in separate instance
        inst=Path(self.temp.name)/'aos-w/agent-files/instances/qc';(inst/'graph-revisions').mkdir(parents=True)
        (inst/'graph-revisions/g0001.yaml').write_text(yaml.safe_dump({'graph':g}))
        x=RunStore.create(inst/'runs/run-002',g,'run-002',ACTOR)
        x.start('review',ACTOR);out=inst/'runs/run-002/artifacts/review.md';out.parent.mkdir();out.write_text('weak')
        x.append('task_submitted_review',ACTOR,'review')
        x.append('review_revise',NEXT,'review',payload={'verdict':'REVISE','correction':'Verify actual sources','retry':{'eligible':True,'max_attempts':2,'attempts':1,'manual_approval_required':True,'next_eligible_at':None}})
        self.assertEqual(x.verified()['tasks']['review']['status'],'NEEDS_REWORK')
        with self.assertRaises(StateError):x.retry('review',ACTOR)
        x.retry('review',ACTOR,approval=True);x.start('review',ACTOR)
        x.append('task_submitted_review',ACTOR,'review')
        with self.assertRaises(StateError):x.complete('review',ACTOR,[{'artifact_id':'review-result','locator':'artifacts/review.md','sha256':digest(b'weak'),'revision':'v1'}])
        out.write_text('corrected')
        x.append('review_accepted',NEXT,'review',payload={'verdict':'PASS','review_id':'r-002','artifacts':[{'artifact_id':'review-result','revision':'v2','sha256':digest(b'corrected')}], 'rubric_version':'1.0'})
        x.complete('review',ACTOR,[{'artifact_id':'review-result','locator':'artifacts/review.md','sha256':digest(b'corrected'),'revision':'v2'}])
        self.assertEqual(x.verified()['run_status'],'COMPLETED')
        self.assertTrue(any(e['type']=='review_revise' for e in self.journal(x.root)))

    def journal(self,root=None):return [json.loads(x) for x in ((root or self.root)/'events.jsonl').read_text().splitlines()]

    def test_run_pause_resume_task_pause_cancel(self):
        self.store.append('run_paused',ACTOR,payload={'reason':'Owner interruption'})
        with self.assertRaises(StateError):self.store.start('a',ACTOR)
        self.store.append('run_resumed',NEXT,payload={'reason':'Owner resumed'})
        self.store.append('task_ready',NEXT,'a')
        self.store.append('task_paused',NEXT,'a',payload={'reason':'Waiting source'})
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'PAUSED')
        self.store.append('task_resumed',NEXT,'a')
        self.store.start('a',NEXT)
        self.store.append('task_cancelled',NEXT,'a',payload={'reason':'No longer needed'})
        self.store.append('run_cancelled',NEXT,payload={'reason':'Owner canceled'})
        self.assertEqual(self.store.verified()['run_status'],'CANCELLED')
        with self.assertRaises(StateError):self.store.start('b',ACTOR)

    def test_ambiguous_external_intent_blocks_duplicates_and_completion(self):
        self.store.start('a',ACTOR)
        req={'object':'test-obj','desired':'PAUSED'}
        key=self.store.operation_key('a','synthetic-meta','object-1',req)
        self.store.operation_intent('a',ACTOR,'synthetic-meta','object-1',req,'mock-approval-001')
        with self.assertRaises(StateError):self.store.operation_intent('a',ACTOR,'synthetic-meta','object-1',req,'mock-approval-001')
        self.store.append('operation_submitted',ACTOR,'a',payload={'operation_key':key})
        self.store.append('operation_ack',ACTOR,'a',payload={'operation_key':key,'ack':'ambiguous'})
        with self.assertRaises(StateError):self.store.complete('a',ACTOR,self.out())
        s=self.store.verified();self.assertEqual(s['tasks']['a']['status'],'RECONCILE_REQUIRED')
        self.assertIn(key,s['pending_provider_operations'])
        self.assertEqual(RunStore(self.root).verified()['operations'][key]['status'],'RECONCILE_REQUIRED')
        with self.assertRaises(StateError):self.store.append('operation_reconciled',NEXT,'a',payload={'operation_key':key,'result':'APPLIED'})
        self.store.append('operation_reconciled',NEXT,'a',payload={'operation_key':key,'result':'APPLIED','readback_source':'mock-provider','observed_at':utcnow(),'readback_ref':'synthetic:test-response-1'})
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'BLOCKED')
        self.assertEqual(self.store.verified()['operations'][key]['status'],'APPLIED')

    def test_corrupt_partial_tail_is_quarantined_with_explicit_repair(self):
        self.store.start('a',ACTOR)
        with (self.root/'events.jsonl').open('ab') as f:f.write(b'{"seq":')
        with self.assertRaises(CorruptLog):self.store.verified()
        with self.assertRaises(CorruptLog):self.store.recover(NEXT)
        prior=(self.root/'events.jsonl').read_bytes()
        issues=self.store.recover(NEXT,repair_tail=True)
        self.assertTrue(any('partial' in x for x in issues))
        self.assertTrue(list((self.root/'recovery').glob('corrupt-tail-*.bin')))
        self.assertEqual((self.root/'events.jsonl').read_bytes()[:len(prior)-len(b'{"seq":')],prior[:-len(b'{"seq":')])
        self.assertEqual(self.journal()[-1]['type'],'recovery_checked')

    def test_inconsistent_derived_state_is_preserved_and_rebuilt(self):
        self.store.start('a',ACTOR)
        x=json.loads((self.root/'state.json').read_text());x['last_event_seq']=9000
        (self.root/'state.json').write_text(json.dumps(x))
        self.store.recover(NEXT)
        self.assertEqual(self.store.verified()['last_event_seq'],len(self.journal()))
        self.assertTrue(list((self.root/'recovery').glob('snapshot-before-*')))

    def test_hash_chain_tamper_detected(self):
        self.store.start('a',ACTOR)
        raw=(self.root/'events.jsonl').read_text();(self.root/'events.jsonl').write_text(raw.replace('task_started','task_completed',1))
        with self.assertRaises(CorruptLog):self.store.verified()
        self.store.recover(NEXT,repair_tail=True)
        self.assertTrue((self.root/'recovery').exists())
        self.assertEqual(self.journal()[-1]['type'],'recovery_checked')

    def test_graph_revision_preserves_prior_results_and_replays(self):
        self.store.start('a',ACTOR);self.store.complete('a',ACTOR,self.out())
        modified=copy.deepcopy(self.graph)
        modified['nodes'][1]['instructions']='Changed downstream b'
        revised=yaml.safe_dump({'graph':modified}).encode()
        with self.assertRaises(StateError):self.store.revise('g0002',revised,NEXT,{'decision':'DENIED'})
        change=self.store.revise('g0002',revised,NEXT,{'decision':'GRANTED','action':'revise_graph','base_revision':'g0001','approval_id':'mock-owner-review-1'})
        self.assertEqual(change['preserved'],['a'])
        stored=RunStore(self.root).verified()
        self.assertEqual(stored['graph_revision'],'g0002')
        self.assertEqual(stored['tasks']['a']['status'],'COMPLETE')
        self.assertEqual(stored['tasks']['b']['status'],'WAIT_DEPENDENCY')
        self.assertTrue((self.inst/'graph-revisions/g0001.yaml').exists())
        self.assertEqual(self.store.handoff(NEXT)['graph_revision'],'g0002')

    def test_revision_of_completed_step_invalidates_dependents_without_erasing(self):
        self.store.start('a',ACTOR);self.store.complete('a',ACTOR,self.out())
        self.store.start('b',ACTOR);self.store.complete('b',ACTOR,self.out('b'))
        changed=copy.deepcopy(self.graph);changed['nodes'][0]['instructions']='New input evidence contract'
        new=yaml.safe_dump({'graph':changed}).encode()
        change=self.store.revise('g0002',new,NEXT,{'decision':'GRANTED','action':'revise_graph','base_revision':'g0001','approval_id':'mock-owner-review-2'})
        self.assertEqual(set(change['invalidated']),{'a','b'})
        state=RunStore(self.root).verified()
        self.assertEqual(state['tasks']['a']['status'],'WAIT_DEPENDENCY')
        self.assertEqual(len(state['superseded_results']),2)
        self.assertTrue(any(e['type']=='task_completed' for e in self.journal()))

    def test_stale_checkpoint_does_not_override_event_history(self):
        self.store.start('a',ACTOR);cp=self.store.checkpoint(ACTOR)
        s=json.loads((self.root/'state.json').read_text());s['last_event_seq']=0
        (self.root/'state.json').write_text(json.dumps(s))
        self.store.recover(NEXT)
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'RUNNING')
        self.assertEqual(cp['checkpoint_id'],'checkpoint-000004')

    def test_crash_after_graph_revision_event_before_run_pointer_update(self):
        self.store.start('a',ACTOR);self.store.complete('a',ACTOR,self.out())
        changed=copy.deepcopy(self.graph);changed['nodes'][1]['instructions']='New revision after crash'
        self.store.revise('g0002',yaml.safe_dump({'graph':changed}).encode(),NEXT,
            {'decision':'GRANTED','action':'revise_graph','base_revision':'g0001','approval_id':'test-only-approval'})
        data=json.loads((self.root/'run.json').read_text());data.pop('current_graph_revision')
        (self.root/'run.json').write_text(json.dumps(data))
        fresh=RunStore(self.root)
        issues=fresh.recover(NEXT)
        self.assertIn('reconciled_graph_pointer_from_verified_event',issues)
        self.assertEqual(json.loads((self.root/'run.json').read_text())['current_graph_revision'],'g0002')
        self.assertEqual(fresh.verified()['tasks']['a']['status'],'COMPLETE')

    def test_corrupted_checkpoint_does_not_override_events(self):
        self.store.start('a',ACTOR);cp=self.store.checkpoint(ACTOR)
        path=self.root/'checkpoints'/(cp['checkpoint_id']+'.json')
        body=json.loads(path.read_text());body['event_digest']='f'*64;path.write_text(json.dumps(body))
        issues=self.store.recover(NEXT)
        self.assertTrue(any('invalid_checkpoint_anchor' in x for x in issues))
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'RUNNING')

    def test_completing_task_cannot_bypass_dependencies_via_direct_event(self):
        with self.assertRaises(StateError):self.store.append('task_ready',ACTOR,task_id='b')
        with self.assertRaises(StateError):self.store.append('task_claimed',ACTOR,task_id='b')
        self.assertEqual(self.store.verified()['tasks']['b']['attempts'],0)

    def test_completed_evidence_is_revalidated_on_new_session(self):
        self.store.start('a',ACTOR);self.store.complete('a',ACTOR,self.out())
        (self.root/'artifacts/a.md').write_text('altered without revision')
        fresh=RunStore(self.root)
        state=fresh.verified()
        self.assertEqual(state['tasks']['a']['status'],'BLOCKED')
        self.assertEqual(state['eligible_tasks'],[])
        self.assertTrue(any('stale_evidence' in x for x in state['audit_warnings']))
        issue=fresh.recover(NEXT)
        self.assertTrue(any('stale_evidence' in x for x in issue))
        self.assertTrue(any(e['type']=='task_completed' for e in self.journal()))

    def test_no_shared_claim_guarantee_is_inferred(self):
        data=json.loads((self.root/'run.json').read_text());data['mode']='shared_coordinated'
        (self.root/'run.json').write_text(json.dumps(data))
        shared=RunStore(self.root)
        with self.assertRaises(StateError):shared.append('task_ready',ACTOR,'a')

    def test_original_pinned_graph_modification_is_detected(self):
        (self.inst/'graph-revisions/g0001.yaml').write_text('graph: {nodes: []}')
        with self.assertRaises(StateError):RunStore(self.root)

    def test_ack_is_not_provider_readback_and_retries_are_blocked(self):
        self.store.start('a',ACTOR)
        request={'action':'stage_paused'}
        key=self.store.operation_key('a','mock','object-1',request)
        self.store.operation_intent('a',ACTOR,'mock','object-1',request,'test-only-approval')
        self.store.append('operation_submitted',ACTOR,'a',payload={'operation_key':key})
        self.store.append('operation_ack',ACTOR,'a',payload={'operation_key':key,'ack':'accepted','evidence':'mock ack'})
        self.assertIn(key,self.store.verified()['pending_provider_operations'])
        with self.assertRaises(StateError):self.store.complete('a',ACTOR,self.out())
        self.store.append('operation_unknown',NEXT,'a',payload={'operation_key':key})
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'RECONCILE_REQUIRED')

    def test_resuming_paused_running_task_requires_new_attempt(self):
        self.store.start('a',ACTOR)
        self.store.append('task_paused',ACTOR,'a',payload={'reason':'Manual pause'})
        self.store.append('task_resumed',NEXT,'a')
        self.assertEqual(self.store.verified()['tasks']['a']['status'],'READY')
        self.store.start('a',NEXT)
        self.assertEqual(self.store.verified()['tasks']['a']['attempts'],2)

    def test_orphan_checkpoint_is_reported_not_used_as_truth(self):
        self.store.start('a',ACTOR)
        cp=self.store.checkpoint(ACTOR)
        # simulate a file stored just before checkpoint_created went to the journal
        duplicate=self.root/'checkpoints/checkpoint-orphan.json'
        body=dict(cp,checkpoint_id='checkpoint-orphan');duplicate.write_text(json.dumps(body))
        issues=self.store.recover(NEXT)
        self.assertTrue(any('orphan_checkpoint' in x for x in issues))

    def test_incomplete_child_fanout_audit_does_not_duplicate_or_mutate(self):
        from state import inspect_child_batch
        agent=Path(self.temp.name)/'aos-w/agent-files'
        rows={'plan_id':'fictional','proposals':[{'instance_id':'child-a','run_id':'run-001'},
              {'instance_id':'child-b','run_id':'run-001'}]}
        partial=agent/'instances/child-a';partial.mkdir();(partial/'instance.json').write_text('{}')
        found=inspect_child_batch(agent,rows)
        self.assertEqual([x['status'] for x in found['results']],['PARTIAL','MISSING'])
        self.assertFalse(found['all_initialized'])
        self.assertFalse((agent/'instances/child-b').exists())
        with self.assertRaises(StateError):inspect_child_batch(agent,{'proposals':[{'instance_id':'../escape','run_id':'run-001'}]})

    def test_verified_not_applied_provider_result_requires_explicit_new_attempt(self):
        self.store.start('a',ACTOR)
        request={'desired':'PAUSED'}
        key=self.store.operation_key('a','synthetic-meta','object-4',request)
        self.store.operation_intent('a',ACTOR,'synthetic-meta','object-4',request,'test-owner-scope')
        self.store.append('operation_submitted',ACTOR,'a',payload={'operation_key':key})
        self.store.append('operation_unknown',NEXT,'a',payload={'operation_key':key})
        self.store.append('operation_reconciled',NEXT,'a',payload={'operation_key':key,'result':'NOT_APPLIED',
            'observed_at':utcnow(),'readback_source':'mock-provider','readback_ref':'mock:lookup-42'})
        with self.assertRaises(StateError):self.store.operation_intent('a',ACTOR,'synthetic-meta','object-4',request,'test-owner-scope')
        self.store.append('task_unblocked',NEXT,'a',payload={'reason':'Verified NOT_APPLIED; new authorized attempt required'})
        self.store.start('a',NEXT)
        newer=self.store.operation_key('a','synthetic-meta','object-4',request,retry_reference=key)
        self.assertNotEqual(newer,key)
        self.store.operation_intent('a',NEXT,'synthetic-meta','object-4',request,'test-owner-scope',retry_reference=key)
        self.assertIn(newer,self.store.verified()['pending_provider_operations'])
        with self.assertRaises(StateError):self.store.operation_intent('a',NEXT,'synthetic-meta','object-4',request,'test-owner-scope',retry_reference='nonexistent')

    def test_read_only_resume_legacy_advisory_journal(self):
        # old 0.1.0 logs didn't have digests; they must not be misrepresented as verified.
        event=json.loads((self.root/'events.jsonl').read_text().splitlines()[0]);event.pop('digest');event.pop('prev_digest')
        (self.root/'events.jsonl').write_text(json.dumps(event)+'\n')
        s=self.store.verified()
        self.assertEqual(s['integrity_level'],'advisory')
        self.store.append('recovery_checked',NEXT,payload={'legacy_event_source':'0.1'})
        self.assertEqual(self.store.verified()['integrity_level'],'advisory')

if __name__=='__main__':unittest.main(verbosity=2)
