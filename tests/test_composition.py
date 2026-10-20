"""Local-only conformance tests. PyYAML needed only to run these optional tests."""
import copy, json, tempfile, unittest, subprocess, sys, hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"/"composition"))
from composition import *
from cli import materialize
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'scaffold/aos-w'
FX=BASE/'examples/conformance/planning'
def j(n):return json.loads((FX/n).read_text())
def t(n):return read_yaml(ROOT/'templates'/n/'template.yaml')
class Conformance(unittest.TestCase):
    def test_graphs(self):
        for n in ['research-starter','periodic-review-example','competitor-investigation','research-portfolio-planner','research-portfolio-compound']:
            self.assertTrue(validate_graph(t(n)['graph'])['valid'])
    def test_cycle_and_missing_contract(self):
        a=copy.deepcopy(t('competitor-investigation')['graph'])
        a['nodes'][0]['needs']=['review-investigation']
        with self.assertRaises(InvalidWorkflow):validate_graph(a)
        b=copy.deepcopy(t('competitor-investigation')['graph']);del b['nodes'][0]['contract']
        with self.assertRaises(InvalidWorkflow):validate_graph(b)
    def test_custom_pin_and_permissions(self):
        child=t('competitor-investigation');overlay=read_yaml(ROOT/'agent-files/custom-templates/competitor-investigation-ontario/template.yaml')
        digest=sha256_bytes((ROOT/'templates/competitor-investigation/template.yaml').read_bytes())
        resolved=resolve(child,overlay,{'buyer':'Ontario roofers','focus':'interior repaint'},digest)
        self.assertEqual(resolved['template_id'],'competitor-investigation-ontario')
        self.assertIn('Ontario',resolved['graph']['nodes'][1]['instructions'])
        self.assertEqual(resolved['resolved_parameters']['market'],'US and Canada')
        with self.assertRaises(InvalidWorkflow):resolve(child,overlay,{'buyer':'Roofers','focus':'ads'},'BAD PIN')
        escalated=copy.deepcopy(overlay);escalated['policy_overrides']['allowed_actions'].append('activate_live')
        with self.assertRaises(InvalidWorkflow):resolve(child,escalated,{'buyer':'Roofers','focus':'ads'},digest)
    def test_parallel_and_conditional(self):
        plan=t('research-portfolio-planner')['graph']
        status=classify(plan,j('graph-state.json'),j('graph-context.json'))
        self.assertEqual(status['propose-investigations']['status'],'ready')
        self.assertEqual(status['synthesize']['status'],'waiting')
        self.assertIsNone(predicate({'op':'eq','path':'source.access','value':'yes'},{'source':{}}))
        self.assertFalse(predicate({'op':'and','args':[{'op':'eq','path':'x','value':1},{'op':'eq','path':'missing','value':2}]},{'x':0}))
    def test_synthesis_requires_every_independent_review(self):
        graph=t('research-portfolio-planner')['graph'];bundle=j('child-proposals.json');results=j('child-results-mock.json')
        state={'define-verticals':{'status':'COMPLETE'},'approve-plan':{'status':'COMPLETE'},'propose-investigations':{'status':'COMPLETE'},'synthesize':{'status':'WAIT_DEPENDENCY'}}
        ctx=j('graph-context.json');ctx['artifacts']['propose-investigations:child-proposals']={'verified':True};ctx['proposals']=bundle
        self.assertEqual(classify(graph,state,ctx)['synthesize']['status'],'blocked')
        ctx['synthesis_approval']={'valid':True}
        self.assertEqual(classify(graph,state,ctx)['synthesize']['status'],'waiting')
        ctx['children']=results
        self.assertEqual(classify(graph,state,ctx)['synthesize']['status'],'ready')
        ctx['children'][next(iter(results))]['review']['verdict']='REVISE'
        self.assertEqual(classify(graph,state,ctx)['synthesize']['status'],'waiting')

    def test_skill_capability_and_quality_escalation_are_blocked(self):
        graph=t('competitor-investigation')['graph'];ctx={'allowed_actions':['read','write_local']}
        graph['nodes'][0]['skills']=['not-installed']
        self.assertEqual(classify(graph,{},ctx)['scope']['status'],'blocked')
        del graph['nodes'][0]['skills']
        graph['nodes'][0]['required_capabilities']=['nonexistent-provider']
        self.assertEqual(classify(graph,{},ctx)['scope']['status'],'blocked')
        child=t('competitor-investigation');overlay=read_yaml(ROOT/'agent-files/custom-templates/competitor-investigation-ontario/template.yaml')
        digest=sha256_bytes((ROOT/'templates/competitor-investigation/template.yaml').read_bytes())
        unsafe=copy.deepcopy(overlay)
        unsafe['node_patches'][0]['node']['required_actions'].append('activate_live')
        with self.assertRaises(InvalidWorkflow):resolve(child,unsafe,{'buyer':'coaches','focus':'Meta'},digest)
        unsafe=copy.deepcopy(overlay)
        unsafe['node_patches'][0]['node']['quality']['gates']=[]
        # require a node-specific gate first, not merely template default
        base=copy.deepcopy(child);base['graph']['nodes'][1]['quality']['gates']=['evidence-qc']
        with self.assertRaises(InvalidWorkflow):resolve(base,unsafe,{'buyer':'coaches','focus':'Meta'},digest)

    def test_dynamic_children_are_stable_and_unstarted(self):
        plan=j('portfolio-plan.json');child=t('competitor-investigation');p1=proposals(plan,child);p2=proposals(plan,child)
        self.assertEqual(p1,p2)
        self.assertEqual(len(p1['proposals']),3)
        self.assertTrue(all(x['status']=='PROPOSED' and x['authorization_required'] and x['quality_requirements'] and all(n['done_when'] for n in x['execution_contracts']) for x in p1['proposals']))
        bad=copy.deepcopy(plan);bad['items'].append(copy.deepcopy(plan['items'][0]))
        with self.assertRaises(InvalidWorkflow):proposals(bad,child)
        bad=copy.deepcopy(plan);bad['approved_input']=False
        with self.assertRaises(InvalidWorkflow):proposals(bad,child)
    def test_review_gate_and_merge(self):
        p=j('child-proposals.json');result=j('child-results-mock.json');approval=j('synthesis-approval-mock.json')
        self.assertEqual(merge(p,result,approval)['status'],'READY_FOR_SYNTHESIS')
        bad=copy.deepcopy(result);bad[next(iter(bad))]['review']['verdict']='REVISE'
        with self.assertRaises(InvalidWorkflow):merge(p,bad,approval)
        with self.assertRaises(InvalidWorkflow):merge(p,result,{'decision':'DENIED'})
    def test_revision_preserves_siblings_and_history(self):
        g=t('competitor-investigation')['graph'];h=read_yaml(FX/'revised-child-graph.yaml')['graph']
        state={'scope':{'status':'COMPLETE'},'search-ads':{'status':'COMPLETE'}}
        with self.assertRaises(InvalidWorkflow):revision_impact(g,h,state)
        impacted=revision_impact(g,h,state,{'decision':'GRANTED','action':'revise_graph'})
        self.assertEqual(impacted['preserved'],['scope'])
        self.assertIn('review-investigation',impacted['invalidated'])
        self.assertNotIn('scope',impacted['invalidated'])
    def test_materialize_requires_exact_approval_and_pins_bytes(self):
        p=j('child-proposals.json');approval=j('approval-mock.json');child=ROOT/'templates/competitor-investigation/template.yaml'
        actor=j('actor.json')
        with tempfile.TemporaryDirectory() as d:
            home=Path(d)/'agent-files';home.mkdir()
            with self.assertRaises(InvalidWorkflow):materialize(p,dict(approval, decision='DENIED'),child,home,actor)
            self.assertEqual(list(home.iterdir()),[])
            with self.assertRaises(InvalidWorkflow):materialize(p,dict(approval, allowed_proposal_ids=[p['proposals'][0]['proposal_id']]),child,home,actor)
            outcome=materialize(p,approval,child,home,actor)
            self.assertEqual(outcome['count'],3)
            for row in p['proposals']:
                inst=home/'instances'/row['instance_id'];run=inst/'runs/run-001'
                self.assertEqual((inst/'graph-revisions/g0001.yaml').read_bytes(),child.read_bytes())
                events=[json.loads(x) for x in (run/'events.jsonl').read_text().splitlines()]
                self.assertEqual(len(events),1)
                self.assertEqual(events[0]['type'],'run_created')
                self.assertEqual(json.loads((run/'state.json').read_text())['run_status'],'CREATED')
                self.assertFalse(list((run/'artifacts').glob('evidence.md')))
            with self.assertRaises(InvalidWorkflow):materialize(p,approval,child,home,actor)
    def test_outside_agent_files_rejected(self):
        from cli import safe_path
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'agent-files';root.mkdir()
            with self.assertRaises(InvalidWorkflow):safe_path(root,'../external')
            with self.assertRaises(InvalidWorkflow):safe_path(root,'instances/../../external')
if __name__=='__main__':unittest.main(verbosity=2)
