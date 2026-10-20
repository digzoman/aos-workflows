"""Stdlib test suite for optional ZIP distribution & installed user-data preservation.
Tests use synthetic framework sources, never customer data or network.
"""
import importlib.util, json, tempfile, unittest, zipfile, hashlib, shutil, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def mod(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    return m
D=mod(ROOT/'scripts'/'aosw-distribution.py','aosw_distributor')
O=mod(ROOT/'scripts'/'aosw-ops.py','aosw_ops')

class TestDistribution(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.source=self.root/'repo'/'scaffold'/'aos-w';self.source.mkdir(parents=True)
        for rel,content in {'README.md':'# Framework','PROTOCOL.md':'Run manually',
          'VERSION.json':json.dumps({'aosw_version':'0.5.0','schema_version':'1.0.0','mandatory_git':False,'mandatory_programming_runtime':False}),
          'spec/README.md':'Schemas','spec/schemas/common.schema.json':'{}',
          'references/README.md':'Manual', 'templates/README.md':'Index',
          'agent-files/README.md':'Writable', 'agent-files/config/settings.json':'{}',
          'agent-files/config/sync.json':'{"enabled":false}',
          'agent-files/instances/README.md':'Instances',
          'templates/research-starter/template.yaml':'schema_version: "1.0.0"\ntemplate_id: research-starter\nversion: "0.5.0"\nparameters:\n  question: {type: string, required: true}\npolicy: {allowed_actions: [read, write_local], max_parallel_tasks: 1}\ngraph:\n  nodes:\n    - id: define-scope\n      needs: []\n      kind: task\n      instructions: Write a local scope\n      outputs: [{artifact_id: scope, path: artifacts/scope.md}]\n'} .items():
            p=self.source/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
        # intentionally PRIVATE source files must not leak into ZIP
        p=self.source/'agent-files'/'instances'/'customer-instance'/'secret.txt';p.parent.mkdir(parents=True);p.write_text('PRIVATE CUSTOMER DATA - SHOULD NOT APPEAR')
        p=self.source/'agent-files'/'config'/'private-key.json';p.write_text('not-the-real-key')
        p=self.source/'agent-files'/'custom-templates'/'user-secret'/'template.yaml';p.parent.mkdir(parents=True);p.write_text('PRIVATE')
        self.zip=self.root/'aos-w.zip'

    def build(self):return D.build(self.source,self.zip)
    def test_build_verify_manifest(self):
        result=self.build();self.assertEqual(result['version'],'0.5.0');m,files=D.verify(self.zip)
        self.assertEqual(result['files'],len(files)+1)
        self.assertIn('templates/research-starter/template.yaml',files)
        self.assertEqual(len(m['entries']),len(files))
    def test_excludes_all_user_private_data(self):
        self.build();raw=self.zip.read_bytes()
        self.assertNotIn(b'PRIVATE CUSTOMER DATA',raw)
        with zipfile.ZipFile(self.zip) as z:
            names=z.namelist();self.assertFalse(any('/customer-instance/' in n for n in names))
            self.assertFalse(any('/user-secret/' in n for n in names))
            self.assertFalse(any('private-key.json' in n for n in names))
            self.assertIn('aos-w/agent-files/instances/',names)
    def test_deterministic_archive(self):
        a=self.build()['sha256'];self.assertEqual(a,self.build()['sha256'])
    def test_install_into_arbitrary_directory(self):
        self.build();dest=self.root/'workspaces'/'random-folder'/'aos-w'
        r=D.install(self.zip,dest);self.assertFalse(r['upgraded']);self.assertTrue((dest/'agent-files'/'instances').is_dir())
        self.assertEqual(O.list_work(dest)['templates'][0]['id'],'research-starter')
        self.assertFalse((dest/'agent-files'/'instances'/'customer-instance').exists())
    def test_upgrade_preserves_run_and_custom_bytes(self):
        self.build();dest=self.root/'work'/'aos-w';D.install(self.zip,dest)
        user=dest/'agent-files';inst=user/'instances'/'live-job'/'runs'/'run-001';inst.mkdir(parents=True)
        (inst/'events.jsonl').write_bytes(b'{"event":1}\n');(inst/'handoff.md').write_bytes(b'Unfinished on purpose')
        c=user/'custom-templates'/'custom'/ 'template.yaml';c.parent.mkdir(parents=True);c.write_bytes(b'Custom YAML: keep\n')
        (user/'config'/'sync.json').write_bytes(b'{"enabled":true,"branch":"private"}')
        before={str(p.relative_to(user)):hashlib.sha256(p.read_bytes()).hexdigest() for p in user.rglob('*') if p.is_file()}
        (self.source/'PROTOCOL.md').write_text('Updated standard protocol')
        (self.source/'VERSION.json').write_text('{"aosw_version":"0.6.0","schema_version":"1.0.0"}')
        D.build(self.source,self.zip)
        x=D.install(self.zip,dest,upgrade=True)
        self.assertEqual(x['version'],'0.6.0');self.assertTrue(Path(x['backup']).is_dir())
        self.assertEqual((dest/'PROTOCOL.md').read_text(),'Updated standard protocol')
        after={str(p.relative_to(user)):hashlib.sha256(p.read_bytes()).hexdigest() for p in user.rglob('*') if p.is_file()}
        self.assertEqual(before,after);self.assertEqual((inst/'handoff.md').read_bytes(),b'Unfinished on purpose')
    def test_cannot_install_over_existing_or_upgrade_missing(self):
        self.build();d=self.root/'foo'/'aos-w';D.install(self.zip,d)
        with self.assertRaises(D.DistributionError):D.install(self.zip,d)
        with self.assertRaises(D.DistributionError):D.install(self.zip,self.root/'none'/'aos-w',upgrade=True)
    def test_manifest_tampering_rejected(self):
        self.build();p=self.root/'tampered.zip'
        with zipfile.ZipFile(self.zip) as a,zipfile.ZipFile(p,'w') as b:
            for n in a.namelist():b.writestr(n,b'STOLE CONTENT' if n=='aos-w/PROTOCOL.md' else a.read(n))
        with self.assertRaises(D.DistributionError):D.verify(p)
    def test_zip_slip_rejected(self):
        self.build();p=self.root/'evil.zip'
        with zipfile.ZipFile(self.zip) as a,zipfile.ZipFile(p,'w') as b:
            for n in a.namelist():b.writestr(n,a.read(n))
            b.writestr('aos-w/../evil.txt','x')
        with self.assertRaises(D.DistributionError):D.verify(p)
    def test_unknown_extra_file_rejected(self):
        self.build();p=self.root/'extra.zip'
        with zipfile.ZipFile(self.zip) as a,zipfile.ZipFile(p,'w') as b:
            for n in a.namelist():b.writestr(n,a.read(n))
            b.writestr('aos-w/temp/internal.md','wrong')
        with self.assertRaises(D.DistributionError):D.verify(p)
    def test_duplicate_names_rejected(self):
        self.build();p=self.root/'duplicate.zip'
        with zipfile.ZipFile(self.zip) as a,zipfile.ZipFile(p,'w') as b:
            for n in a.namelist():b.writestr(n,a.read(n))
            b.writestr('aos-w/readme.md','different case')
        with self.assertRaises(D.DistributionError):D.verify(p)
    def test_user_symlink_blocks_upgrade(self):
        self.build();d=self.root/'d'/'aos-w';D.install(self.zip,d)
        (d/'agent-files'/'unsafe').symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(D.DistributionError):D.install(self.zip,d,upgrade=True)
        self.assertTrue((d/'README.md').exists())
    def test_source_symlink_fails_closed(self):
        (self.source/'references'/'links.md').symlink_to(self.root/'missing')
        with self.assertRaises(D.DistributionError):D.build(self.source,self.zip)
    def test_schema_major_upgrade_blocked(self):
        self.build();d=self.root/'d'/'aos-w';D.install(self.zip,d)
        (d/'VERSION.json').write_text('{"schema_version":"2.0.0","aosw_version":"1.0"}')
        with self.assertRaises(D.DistributionError):D.install(self.zip,d,upgrade=True)
    def test_manual_no_python_git_declared(self):
        self.build();m,files=D.verify(self.zip)
        self.assertIn(b'mandatory_git',files['VERSION.json'])
        self.assertFalse(any(k.startswith('tools/') or k.startswith('tests/') or k.startswith('temp/') for k in files))

class TestOps(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'aos-w';(self.root/'agent-files'/'instances').mkdir(parents=True)
        (self.root/'VERSION.json').write_text('{"aosw_version":"0.5.0"}')
        t=self.root/'templates'/'research-starter'/'template.yaml';t.parent.mkdir(parents=True)
        t.write_text('schema_version: "1.0.0"\ntemplate_id: research-starter\nversion: "0.5.0"\nparameters:\n  question: {type: string, required: true}\npolicy: {autonomy: bounded, allowed_actions: [read, write_local], human_required_actions: [], default_gates: [], max_parallel_tasks: 1, allow_dynamic_children: false}\ngraph:\n  nodes:\n    - id: scope\n      kind: task\n      needs: []\n      instructions: Write a scope\n      outputs: [{artifact_id: scope, path: artifacts/scope.md}]\n    - id: collect\n      kind: task\n      needs: [scope]\n      instructions: Research\n      outputs: [{artifact_id: evidence, path: artifacts/evidence.md}]\n')
        self.actor={'agent':'fixture','platform':'test','role':'worker','instance':'session-001'}
    def test_discovery_and_required_input(self):
        self.assertEqual(O.list_work(self.root)['templates'][0]['id'],'research-starter')
        with self.assertRaises(O.OpsError):O.init(self.root,'research-starter','job1','run-1',self.actor,{})
    def test_init_and_resume_no_memory(self):
        try:import yaml
        except ImportError:self.skipTest('Optional PyYAML not installed')
        result=O.init(self.root,'research-starter','job1','run-1',self.actor,{'question':'Fictional products'})
        self.assertEqual(result['ready_candidates'],['scope'])
        state=O.local_status(self.root,'job1','run-1');self.assertTrue(state['event_prefix_consistent'])
        self.assertEqual(state['observed_valid_event_seq'],1)
        self.assertEqual(state['run_status'],'CREATED')
        path=self.root/'agent-files'/'instances'/'job1'
        self.assertEqual((path/'graph-revisions'/'g0001.yaml').read_bytes(),(self.root/'templates'/'research-starter'/'template.yaml').read_bytes())
        self.assertEqual(len(list((path/'runs'/'run-1'/'tasks').glob('*/attempts'))),2)
        # Explicitly no previous chat needed to find initial work.
        self.assertEqual(O.list_work(self.root)['instances'][0]['runs'],['run-1'])
        with self.assertRaises(O.OpsError):O.init(self.root,'research-starter','job1','run-1',self.actor,{'question':'again'})
    def test_status_detects_event_corruption(self):
        try:import yaml
        except ImportError:self.skipTest('Optional PyYAML not installed')
        O.init(self.root,'research-starter','job1','run-1',self.actor,{'question':'Q'})
        events=self.root/'agent-files'/'instances'/'job1'/'runs'/'run-1'/'events.jsonl'
        with events.open('ab') as f:f.write(b'{ incomplete')
        check=O.local_status(self.root,'job1','run-1');self.assertFalse(check['event_prefix_consistent']);self.assertTrue(check['issues'])
    def test_unsafe_ids_rejected(self):
        with self.assertRaises(O.OpsError):O.init(self.root,'research-starter','../escape','run-1',self.actor,{})
