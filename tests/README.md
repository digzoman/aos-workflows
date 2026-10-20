# Optional executable conformance tests

Run from the repository root in a developer environment with Python 3 and **PyYAML** installed:

```sh
python -m unittest discover -s tests -p 'test_composition.py' -v
```

The tests exercise pure local-file composition semantics, deterministic child proposals, approval-gated materialization into a temporary `agent-files` directory, independent review-before-merge, protected policy inheritance, three-valued conditions, explicit revision invalidation and path confinement. All fixtures are synthetic and no network, Meta, CRM or actual multi-agent coordination is used.

These tests do **not** make Python/PyYAML a prerequisite for ordinary standalone AOS-W, and do not prove a working always-on graph engine, real external account permissions, distributed locking or full JSON Schema validation.

## Prompt 11 state/recovery suite

Run `python -m unittest discover -s tests -p 'test_state*.py' -v` for the **26** local state/recovery/CLI tests, or `python -m unittest discover -s tests -p 'test_*.py' -q` for **37** total (including the 11 composition tests). Python/PyYAML are optional maintainer tools, not installed scaffold requirements. The new tests cover historic event preservation, SHA-256 integrity, torn-tail quarantine, checkpoint recovery, bounded retries, QC correction, uncertain provider intent dedup, explicit pause/resume/cancel/fail, stale artifact blocking, graph revision recovery, and no duplicate child creation. See `temp/tests/PROMPT-11-STATE-CONFORMANCE.md` for actual scope and limitations. No real external accounts were used.
