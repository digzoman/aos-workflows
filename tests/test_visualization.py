"""AOS-W 0.8 read-only visualization conformance, no browser/provider writes."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("aosw_visualizer",ROOT/"scripts/aosw-visualize.py")
viz=importlib.util.module_from_spec(spec)
spec.loader.exec_module(viz)
HTML=(ROOT/"scaffold/aos-w/references/visualization-viewer.html").read_text()
EXAMPLE=json.loads((ROOT/"examples/visualization/bucket9-stage.json").read_text())
SCHEMA=json.loads((ROOT/"scaffold/aos-w/spec/schemas/visualization-snapshot.schema.json").read_text())

class VisualizationAcceptance(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.addCleanup(self.temp.cleanup)
  self.out=Path(self.temp.name)/"aos-w/agent-files/visualizations/demo/index.html"

 def test_01_offline_viewer_no_network(self):
  self.assertIn('<svg aria-hidden="true" id="links">',HTML)
  self.assertIn('const NS="http://www.w3.org/2000/svg";',HTML)
  self.assertIn('textContent',HTML)
  self.assertNotIn('https://cdn',HTML)
  self.assertNotIn('fetch(',HTML)
  self.assertNotIn('XMLHttpRequest',HTML)

 def test_02_demo_contract_valid(self):
  from jsonschema import Draft202012Validator,FormatChecker
  Draft202012Validator(SCHEMA,format_checker=FormatChecker()).validate(EXAMPLE)
  self.assertEqual(len(EXAMPLE["nodes"]),11)
  self.assertEqual(EXAMPLE["nodes"][-1]["status"],"WAIT_APPROVAL")

 def test_03_prompt_drilldown_and_gate_fields(self):
  for name in ['"Prompt / agent instructions"','"Quality controls and approval gates"','"Execution rules and retry policy"','"Artifacts and evidence references"']:
   self.assertIn(name,HTML)
  self.assertIn("n.prompt||n.instructions",HTML)

 def test_04_safe_html_json_embedding(self):
  attack='</script><script>window.attacker=1</script>&\u2028'
  data=dict(EXAMPLE)
  data["nodes"]=list(EXAMPLE["nodes"])
  data["nodes"][0]=dict(data["nodes"][0],prompt=attack)
  out=viz.render(data,HTML)
  self.assertNotIn('</script><script>window.attacker',out)
  self.assertIn("\\u003c/script\\u003e",out)
  self.assertNotIn(attack,out)
  self.assertEqual(out.count(TOKEN:=viz.TOKEN),0)

 def test_05_yml_template_converts_real_graph(self):
  path=ROOT/"scaffold/aos-w/templates/research-starter/template.yaml"
  data=viz.source_to_snapshot(viz.load_yaml(path),None,str(path),None)
  self.assertEqual(data["mode"],"TEMPLATE")
  self.assertEqual(len(data["nodes"]),3)
  self.assertTrue(all(n["status"]=="NOT_STARTED" for n in data["nodes"]))
  self.assertIn("Record dated sources",data["nodes"][1]["prompt"])

 def test_06_compound_visualizes_real_fanout_and_join(self):
  path=ROOT/"scaffold/aos-w/templates/marketing-lifecycle-compound/template.yaml"
  data=viz.source_to_snapshot(viz.load_yaml(path),None,str(path),None)
  self.assertGreater(len(data["nodes"]),10)
  self.assertTrue(any(n["kind"]=="child_generator" for n in data["nodes"]))
  self.assertTrue(any(len(n["needs"] or [])>1 for n in data["nodes"]))

 def test_07_run_state_overlay_unverified(self):
  path=ROOT/"scaffold/aos-w/templates/research-starter/template.yaml"
  st={"run_id":"r1","graph_revision":"g0001","last_event_seq":6,
   "tasks":{"define-scope":{"status":"COMPLETE","attempts":1},"collect-evidence":{"status":"NEEDS_REWORK","attempts":2}}}
  d=viz.source_to_snapshot(viz.load_yaml(path),st,str(path),None)
  self.assertEqual(d["mode"],"RUN")
  self.assertEqual(d["verification"],"SOURCE_SNAPSHOT_UNVERIFIED")
  self.assertEqual(d["nodes"][0]["status"],"COMPLETE")
  self.assertEqual(d["nodes"][1]["status"],"NEEDS_REWORK")
  self.assertEqual(d["nodes"][2]["status"],"UNKNOWN")

 def test_08_unknown_dependency_rejected(self):
  data={"graph":{"nodes":[{"id":"a","needs":["missing"]}]}}
  with self.assertRaisesRegex(viz.ViewError,"Missing graph dependencies"):
   viz.source_to_snapshot(data,None,"a.yaml",None)

 def test_09_cycle_rejected(self):
  data={"graph":{"nodes":[{"id":"a","needs":["b"]},{"id":"b","needs":["a"]}]}}
  with self.assertRaisesRegex(viz.ViewError,"Cycle detected"):
   viz.source_to_snapshot(data,None,"a.yaml",None)

 def test_10_duplicate_id_rejected(self):
  data={"graph":{"nodes":[{"id":"a","needs":[]},{"id":"a","needs":[]}]}}
  with self.assertRaisesRegex(viz.ViewError,"duplicated"):
   viz.source_to_snapshot(data,None,"a.yaml",None)

 def test_11_reject_output_outside_writable_root(self):
  with self.assertRaises(viz.ViewError):
   viz.ensure_safe_output(Path(self.temp.name)/"index.html")

 def test_12_reject_output_symlink(self):
  root=Path(self.temp.name)/"aos-w/agent-files/visualizations"
  root.mkdir(parents=True)
  (root/"demo").symlink_to(Path(self.temp.name),target_is_directory=True)
  with self.assertRaisesRegex(viz.ViewError,"Symlink"):
   viz.ensure_safe_output(root/"demo/index.html")

 def test_13_save_local_snapshot_and_read_only_page(self):
  html=viz.render(EXAMPLE,HTML)
  viz.save(html,self.out,EXAMPLE)
  self.assertTrue(self.out.is_file())
  self.assertTrue((self.out.parent/"snapshot.json").is_file())
  self.assertIn("Human launch approval",self.out.read_text())
  self.assertEqual(json.loads((self.out.parent/"snapshot.json").read_text())["nodes"][-1]["status"],"WAIT_APPROVAL")

 def test_14_package_writable_seed_and_protected_viewer_allowlisted(self):
  mod=importlib.util.spec_from_file_location("aosw_distribution",ROOT/"scripts/aosw-distribution.py")
  pkg=importlib.util.module_from_spec(mod);mod.loader.exec_module(pkg)
  self.assertTrue(pkg.permitted("references/visualization-viewer.html"))
  self.assertTrue(pkg.permitted("references/VISUALIZATION.md"))
  self.assertTrue(pkg.permitted("agent-files/visualizations/README.md"))
  self.assertFalse(pkg.permitted("agent-files/visualizations/demo/index.html"))
  self.assertIn("visualizations",pkg.USER_DIRS)

 def test_15_no_automatic_pages_or_execution(self):
  import subprocess
  code=(ROOT/"scripts/aosw-visualize.py").read_text()
  self.assertNotIn("gh pages",code)
  self.assertNotIn("requests.post",code)
  self.assertNotIn("subprocess.run",code)
  self.assertIn("GENERATED_READ_ONLY",code)


 def test_16_prepared_snapshot_rejects_duplicate_ids(self):
  d=json.loads(json.dumps(EXAMPLE))
  d["nodes"].append(dict(d["nodes"][0]))
  with self.assertRaisesRegex(viz.ViewError,"Duplicate snapshot"):
   viz.render(d,HTML)

 def test_17_prepared_snapshot_rejects_cycles(self):
  d=json.loads(json.dumps(EXAMPLE))
  d["nodes"][0]["needs"]=["launch"]
  with self.assertRaisesRegex(viz.ViewError,"Cycle detected"):
   viz.render(d,HTML)

 def test_18_exact_long_prompt_rejected_not_truncated(self):
  d={"graph":{"nodes":[{"id":"a","needs":[],"instructions":"x"*18001}]}}
  with self.assertRaisesRegex(viz.ViewError,"not silently truncated"):
   viz.source_to_snapshot(d,None,"example.yaml",None)

 def test_19_prepared_snapshot_rejects_missing_dependency(self):
  d=json.loads(json.dumps(EXAMPLE))
  d["nodes"][0]["needs"]=["no-such-node"]
  with self.assertRaisesRegex(viz.ViewError,"Unknown snapshot dependency"):
   viz.render(d,HTML)


 def test_20_real_p18_run_loads_and_reconciles_saved_events(self):
  run=ROOT/"docs/testing/evidence/p18-grounded-39498378421/aos-w/agent-files/instances/b9-parent/runs/run-001"
  d=viz.run_dir_snapshot(run)
  self.assertEqual(d["mode"],"RUN")
  self.assertEqual(d["run_id"],"run-001")
  self.assertEqual(d["instance_id"],"b9-parent")
  self.assertEqual(d["verification"],"EVENTS_RECONCILED")
  self.assertGreaterEqual(d["event_seq_observed"],40)
  self.assertEqual(len(d["nodes"]),11)
  by_id={n["id"]:n for n in d["nodes"]}
  self.assertEqual(by_id["creative"]["status"],"COMPLETE")
  self.assertNotEqual(by_id["launch-permit"]["status"],"COMPLETE")
  self.assertTrue(by_id["creative"]["activity"])

 def test_21_runner_auto_output_path_matches_writable_folder(self):
  run=ROOT/"docs/testing/evidence/p18-grounded-39498378421/aos-w/agent-files/instances/b9-parent/runs/run-001"
  d=viz.run_dir_snapshot(run)
  default=run.absolute().parents[3]/"visualizations"/(
      d["instance_id"]+"--"+d["run_id"]+"--"+d["graph_revision"])/"index.html"
  self.assertTrue(str(default).endswith("agent-files/visualizations/b9-parent--run-001--g0001/index.html"))
  viz.ensure_safe_output(default)

 def test_22_event_integrity_tamper_blocks_verified_visual(self):
  import shutil
  from pathlib import Path
  source=ROOT/"docs/testing/evidence/p18-grounded-39498378421/aos-w/agent-files/instances/b9-parent"
  target=Path(self.temp.name)/"aos-w/agent-files/instances/b9-parent"
  shutil.copytree(source,target)
  run=target/"runs/run-001"
  events=run/"events.jsonl"
  lines=events.read_text().splitlines()
  entry=json.loads(lines[0])
  entry["type"]="forged_workflow_event"
  lines[0]=json.dumps(entry)
  events.write_text("\n".join(lines)+"\n")
  with self.assertRaisesRegex(viz.ViewError,"Event verification failed"):
   viz.run_dir_snapshot(run)

 def test_23_unverified_run_is_clearly_labeled(self):
  run=ROOT/"docs/testing/evidence/p18-grounded-39498378421/aos-w/agent-files/instances/b9-parent/runs/run-001"
  d=viz.run_dir_snapshot(run,verify_events=False)
  self.assertEqual(d["verification"],"SOURCE_SNAPSHOT_UNVERIFIED")
  self.assertIn("advisory",d["warning"])
  self.assertNotEqual(d["nodes"][-1]["status"],"COMPLETE")

 def test_24_visualization_run_metadata_schema(self):
  from jsonschema import Draft202012Validator,FormatChecker
  run=ROOT/"docs/testing/evidence/p18-grounded-39498378421/aos-w/agent-files/instances/b9-parent/runs/run-001"
  data=viz.run_dir_snapshot(run)
  Draft202012Validator(SCHEMA,format_checker=FormatChecker()).validate(data)

if __name__=="__main__":unittest.main()
