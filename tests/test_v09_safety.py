"""AOS-W v0.9 HTML-first hosting and capable-agent safeguards."""
from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class V09Safety(unittest.TestCase):
 def test_fictional_only_pages_export(self):
  spec=importlib.util.spec_from_file_location("aosw_public_check",ROOT/"scripts/aosw-pages-preflight.py")
  mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
  demo=json.loads((ROOT/"examples/visualization/synthetic-six-audience.json").read_text())
  self.assertTrue(mod.validate(demo,"<html>Fictional safe page</html>"))
  for changes in [
    {"public_export":False},
    {"template_id":"b9-six-vertical-launch"},
    {"run_id":"run-001"},
    {"warning":"Private current marketing workflow"}]:
   unsafe=dict(demo,**changes)
   with self.assertRaises(mod.ExportError):mod.validate(unsafe,"<html>unsafe</html>")
  with self.assertRaises(mod.ExportError):
   mod.validate(demo,"<html>api_key=abc</html>")

 def test_pages_is_explicit_opt_in(self):
  content=(ROOT/".github/workflows/aosw-v09-pages.yml").read_text()
  self.assertIn("workflow_dispatch:",content)
  self.assertNotIn("\n  push:",content)
  self.assertIn("aosw-pages-preflight.py",content)
  self.assertIn("steps.deployment.outputs.page_url",content)
  self.assertIn("environment:",content)

 def test_autonomy_requires_recovery_not_fake_gates(self):
  source=(ROOT/"scaffold/aos-w/references/CAPABILITY-RECOVERY.md").read_text()
  protocol=(ROOT/"scaffold/aos-w/PROTOCOL.md").read_text()
  self.assertIn("zero new human approval gates",source)
  self.assertIn("approved skills",source)
  self.assertIn("Continue",source)
  self.assertIn("do not invent gates",protocol.lower())

 def test_release_is_portable_without_pages_dependency(self):
  version=json.loads((ROOT/"scaffold/aos-w/VERSION.json").read_text())
  self.assertEqual(version["aosw_version"],"0.9.0")
  self.assertFalse(version["mandatory_programming_runtime"])
  self.assertFalse(version["mandatory_git"])
  self.assertEqual(version["agent_discovery"]["a2a"],"not_implemented")
  self.assertNotIn("pages",version.get("minimum_requirements",[]))

if __name__=="__main__":unittest.main()
