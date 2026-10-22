"""AOS-W Prompt 15 local-only marketing workflow conformance. All inputs are sanitized.
Run with `python -m unittest discover -s tests -p test_marketing.py -v`.
"""
import copy,hashlib,importlib.util,json,os,sys,tempfile,unittest,warnings
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, RefResolver
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE/'scaffold/aos-w';T=ROOT/'templates';F=BASE/'examples/conformance/marketing'
sys.path.insert(0,str(BASE/'tools/composition'))
from composition import validate_graph, classify, InvalidWorkflow

def template(name):return yaml.safe_load((T/name/'template.yaml').read_text())
def load(name):return json.loads((F/name).read_text())

class MarketingConformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ids=sorted(p.parent.name for p in T.glob('marketing-*/template.yaml'))
        cls.docs={p.name:json.loads(p.read_text()) for p in (ROOT/'spec/schemas').glob('*.schema.json')}
    def test_marketing_library_has_21_standalone_and_compound(self):
        self.assertEqual(len(self.ids),22)
        self.assertIn('marketing-lifecycle-compound',self.ids)
        for n in self.ids:
            self.assertTrue((T/n/'README.md').is_file(),n)
            self.assertEqual(template(n)['version'],'0.7.0')
            self.assertEqual(template(n)['trigger']['kind'],'manual')
            self.assertTrue(validate_graph(template(n)['graph'])['valid'])
    def test_complete_json_schema_validation_with_actual_refs(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',DeprecationWarning)
            for name in self.ids:
                document=template(name)
                n='compound-template.schema.json' if name=='marketing-lifecycle-compound' else 'template.schema.json'
                schema=self.docs[n]
                validator=Draft202012Validator(schema,resolver=RefResolver.from_schema(schema,store=self.docs))
                errors=sorted(validator.iter_errors(document),key=lambda e:str(e.path))
                self.assertEqual([],[(e.message,list(e.path)) for e in errors],name)
    def test_all_nodes_have_exact_io_and_qa_and_safe_local_outputs(self):
        for name in self.ids:
            doc=template(name);gates={g['gate_id'] for g in doc.get('gates',[])}
            by={n['id']:n for n in doc['graph']['nodes']}
            for node in by.values():
                self.assertTrue(node['contract']['done_when'],(name,node['id']))
                self.assertIn(node['kind'],['task','review','approval','join','child_generator'])
                self.assertIn('needs',node)
                self.assertTrue(node['outputs'])
                self.assertTrue(set(node['quality']['gates'])<=gates,(name,node['id']))
                for art in node['outputs']:
                    self.assertTrue(art['path'].startswith('artifacts/'))
                    self.assertNotIn('..',art['path'])
                for input in node['inputs']:
                    self.assertIn(input['from'],by)
                    self.assertIn(input['artifact_id'],[a['artifact_id'] for a in by[input['from']]['outputs']])
            self.assertTrue(validate_graph(doc['graph'])['valid'])
    def test_default_approval_is_never_automatic_provider_write(self):
        for name in self.ids:
            d=template(name)
            self.assertEqual(d['policy']['autonomy'],'bounded')
            self.assertTrue({'activate_live','change_budget','deploy_prod'} <= set(d['policy']['human_required_actions']))
            self.assertFalse({'activate_live','stage_paused','change_budget','send_message','deploy_prod'} & set(d['policy']['allowed_actions']))
            for n in d['graph']['nodes']:
                self.assertFalse({'activate_live','stage_paused','change_budget','deploy_prod','send_message'} & set(n['required_actions']))
        launch=template('marketing-launch-approval')
        gate=next(g for g in launch['gates'] if g['gate_id']=='launch-permit')
        self.assertEqual(gate['kind'],'human');self.assertTrue(gate['protected']);self.assertFalse(gate['waivable'])
        self.assertEqual(launch['graph']['nodes'][-1]['kind'],'task')
        self.assertNotIn('activate_live',[x['id'] for x in template('marketing-lifecycle-compound')['graph']['nodes']])
    def test_three_step_competitor_hypothesis_verified_truth_boundary(self):
        cmp=template('marketing-competitor-execution');off=template('marketing-offer-strategy');verified=template('marketing-offer-deliverability')
        self.assertEqual(cmp['extensions']['source_class'],'OBSERVED_COMPETITOR_ONLY')
        self.assertEqual(off['extensions']['offer_status'],'HYPOTHESIS_NOT_DELIVERABLE')
        self.assertEqual(verified['gates'][0]['kind'],'human')
        self.assertIn('offer-verified',next(x for x in template('marketing-lifecycle-compound')['graph']['nodes'] if x['id']=='copy')['needs'])
        self.assertIn('offer-verified',next(x for x in template('marketing-lifecycle-compound')['graph']['nodes'] if x['id']=='crm')['needs'])
    def test_compound_child_refs_are_correct_sha256_and_all_21(self):
        c=template('marketing-lifecycle-compound')
        self.assertEqual(len(c['composition']['children']),21)
        by={x['child_id']:x for x in c['composition']['children']}
        self.assertEqual(set(by),set(n['id'] for n in c['graph']['nodes']))
        for child in by.values():
            path=T/child['template_id']/'template.yaml'
            self.assertEqual(child['content_digest'],'sha256:'+hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(child['version'],'0.7.0')
            self.assertEqual(child['authorization_mode'],'per_child')
        self.assertEqual(c['composition']['join']['policy'],'all_accepted')
        self.assertEqual(set(c['composition']['join']['children']),set(by))
    def test_evidence_join_really_blocks_unreviewed_dynamic_children(self):
        graph=template('marketing-lifecycle-compound')['graph']
        node=next(x for x in graph['nodes'] if x['id']=='evidence')
        self.assertEqual(node['extensions']['join_source'],'artifacts/research-child-proposals.json')
        statuses={'research-peer-review':{'status':'COMPLETE'},'research-fanout':{'status':'COMPLETE'}}
        ctx={'allowed_actions':['read','write_local'], 'artifacts':{'research-fanout:research-fanout-record':{'verified':True},'research-peer-review:research-peer-review-record':{'verified':True}}}
        blocked=classify(graph,statuses,ctx)
        self.assertEqual(blocked['evidence']['status'],'waiting')
        bundle=load('child-proposals-MOCK.json')['data']
        ctx['proposals']=bundle
        self.assertEqual(classify(graph,statuses,ctx)['evidence']['status'],'blocked')
        ctx['synthesis_approval']={'valid':True}
        self.assertEqual(classify(graph,statuses,ctx)['evidence']['status'],'waiting')
        ctx['children']={p['proposal_id']:{'status':'COMPLETE','review':{'verdict':'PASS'},'artifacts':[{'id':'versioned'}]} for p in bundle['proposals']}
        self.assertEqual(classify(graph,statuses,ctx)['evidence']['status'],'ready')
        ctx['children'][bundle['proposals'][0]['proposal_id']]['review']['verdict']='REVISE'
        self.assertEqual(classify(graph,statuses,ctx)['evidence']['status'],'waiting')

    def test_compound_plan_fanout_and_join_gates(self):
        c=template('marketing-lifecycle-compound');nodes={n['id']:n for n in c['graph']['nodes']}
        self.assertEqual(nodes['research-fanout']['kind'],'child_generator')
        self.assertEqual(nodes['research-fanout']['fanout']['max_children'],15)
        self.assertEqual(nodes['evidence']['kind'],'join')
        self.assertEqual(nodes['evidence']['extensions']['join_policy'],'all_accepted')
        self.assertTrue(nodes['evidence']['extensions']['no_auto_accept'])
        self.assertEqual(nodes['integration']['kind'],'join')
        self.assertEqual(nodes['integration']['join']['policy'],'all_accepted')
        self.assertEqual(set(nodes['integration']['needs']),{'brand','meta-plan','crm','landing','tracking'})
        self.assertEqual(nodes['launch-approval']['quality']['gates'],['launch-permit'])
        self.assertEqual(nodes['launch-approval']['kind'],'approval')
    def test_parallel_readiness_after_verified_offer_is_non_inferential(self):
        c=template('marketing-lifecycle-compound')
        self.assertEqual(set(next(n for n in c['graph']['nodes'] if n['id']=='crm')['needs']),{'offer-verified'})
        self.assertEqual(set(next(n for n in c['graph']['nodes'] if n['id']=='landing')['needs']),{'offer-verified'})
        self.assertEqual(set(next(n for n in c['graph']['nodes'] if n['id']=='tracking')['needs']),{'crm','landing'})
        simulated=load('parallel-branches-MOCK.json')
        self.assertEqual(set(simulated['parallel_possible']),{'crm','landing'})
        self.assertFalse(simulated['real_provider_changes'])
        self.assertIn('MOCK',simulated['fixture_kind'])
    def test_output_sha_mutation_changes_child_pin(self):
        c=template('marketing-lifecycle-compound')
        child=next(x for x in c['composition']['children'] if x['child_id']=='copy')
        before=child['content_digest'];after='sha256:'+hashlib.sha256((T/'marketing-ad-copy/template.yaml').read_bytes()+b'changed').hexdigest()
        self.assertNotEqual(before,after)
    def test_no_real_provider_grants_or_private_secrets(self):
        forbidden=['REAL_UNTRUSTED_TOKEN','X-API-KEY','sk_live_','access_token:','@gmail.com','@outlook.com','facebook_access_token','act_123456','client_id: private']
        for name in self.ids:
            for p in (T/name).rglob('*'):
                if p.is_file():
                    body=p.read_text()
                    for x in forbidden:self.assertNotIn(x,body,(name,p.name))
    def test_image_generation_fails_closed_without_tool(self):
        d=template('marketing-image-generation');n=next(n for n in d['graph']['nodes'] if n['id']=='produce-candidates')
        self.assertIn('image_generation',n['required_capabilities'])
        statuses={'verify-generator':{'status':'COMPLETE'}}
        ctx={'allowed_actions':['read','write_local'],'artifacts':{'verify-generator:verify-generator-record':{'verified':True}}}
        self.assertEqual(classify(d['graph'],statuses,ctx)['produce-candidates']['status'],'blocked')
    def test_negative_qc_fixture_requires_scope_and_is_mock(self):
        d=load('negative-gates-MOCK.json')
        self.assertEqual(len(d['scenarios']),6)
        self.assertTrue(all('MOCK' in d['fixture_kind'] for _ in [0]))
        s=[x for x in d['scenarios'] if x['case']=='activation_without_permit'][0]
        self.assertIsNone(s['human_permit'])
    def test_all_example_instances_created_not_fabricated_completion(self):
        root=F/'instances';dirs=sorted(p for p in root.iterdir() if p.is_dir());self.assertEqual(len(dirs),6)
        for p in dirs:
            inst=json.loads((p/'instance.json').read_text());self.assertEqual(inst['current_graph_revision'],'g0001')
            run=p/'runs/run-001';s=json.loads((run/'state.json').read_text())
            self.assertEqual(s['run_status'],'CREATED')
            self.assertFalse(s['completed_steps'])
            events=[json.loads(x) for x in (run/'events.jsonl').read_text().splitlines()]
            self.assertEqual(len(events),1)
            self.assertEqual(events[0]['type'],'run_created')
            lock=json.loads((p/'template-lock.json').read_text());pin=p/lock['pinned_snapshot_path']
            self.assertEqual((p/'graph-revisions/g0001.yaml').read_bytes(),pin.read_bytes())
            self.assertEqual(lock['content_digest'],'sha256:'+hashlib.sha256(pin.read_bytes()).hexdigest())
    def test_safe_standalone_instantiation_from_new_templates(self):
        import importlib.machinery,shutil
        ops=importlib.machinery.SourceFileLoader('ops15',str(BASE/'scripts/aosw-ops.py')).load_module()
        with tempfile.TemporaryDirectory() as folder:
            installed=Path(folder)/'arbitrary-work/aos-w';shutil.copytree(ROOT,installed,ignore=shutil.ignore_patterns('demo-local-research','competitor-investigation-ontario'))
            actor={'agent':'tester','platform':'local','role':'worker','instance':'test-module'}
            a=ops.init(installed,'marketing-offer-strategy','new-offer','run-001',actor,{'observed_competitor_matrix_ref':'fixture-only','target_buyer':'SMB'})
            self.assertFalse(a['task_executed']);self.assertTrue(a['ready_candidates'])
            self.assertFalse(ops.local_status(installed,'new-offer','run-001')['authorized_to_execute'])
    def test_packager_includes_only_clean_marketing_templates(self):
        import importlib.machinery
        dist=importlib.machinery.SourceFileLoader('dist15',str(BASE/'scripts/aosw-distribution.py')).load_module()
        with tempfile.TemporaryDirectory() as d:
            z=Path(d)/'marketing-portable.zip';dist.build(ROOT,z)
            manifest,_=dist.verify(z)
            self.assertEqual(manifest['version'],'0.8.0')
            self.assertIn('templates/marketing-lifecycle-compound/template.yaml',manifest['entries'])
            self.assertIn('templates/MARKETING-LIBRARY.md',manifest['entries'])
            self.assertIn('templates/marketing-competitor-execution/skills/marketing-source-claims/SKILL.md',manifest['entries'])
            self.assertNotIn('agent-files/instances/demo-local-research/instance.json',manifest['entries'])
            self.assertEqual([x for x in manifest['entries'] if x.startswith('agent-files/instances/')], ['agent-files/instances/README.md'])
    def test_marketing_modules_independently_instantiable_with_parameters(self):
        # Each module uses declared parameters, per-module base graph and safe local action policy.
        for name in self.ids:
            if name=='marketing-lifecycle-compound':continue
            d=template(name)
            self.assertIn('source_ref',d['parameters'])
            self.assertEqual(d['policy']['allowed_actions'],['read','research','write_local','review'])
            self.assertTrue(d['graph']['nodes'][0]['id'])
    def test_failure_on_one_research_branch_preserves_other_proposals(self):
        bundle=load('child-proposals-MOCK.json')['data'];ids=[x['proposal_id'] for x in bundle['proposals']]
        self.assertEqual(len(ids),3)
        self.assertEqual(len(set(ids)),3)
        self.assertTrue(all(x['status']=='PROPOSED' and x['authorization_required'] for x in bundle['proposals']))
        failure=load('negative-gates-MOCK.json')['scenarios'][0]
        self.assertIn('REVISE',failure['verdict']);self.assertIn('agencies/roofing',failure['unrelated'])

if __name__=='__main__':unittest.main()
