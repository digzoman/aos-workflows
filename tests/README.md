# Optional executable conformance tests

Run from the repository root in a developer environment with Python 3 and **PyYAML** installed:

```sh
python -m unittest discover -s tests -p 'test_composition.py' -v
```

The tests exercise pure local-file composition semantics, deterministic child proposals, approval-gated materialization into a temporary `agent-files` directory, independent review-before-merge, protected policy inheritance, three-valued conditions, explicit revision invalidation and path confinement. All fixtures are synthetic and no network, Meta, CRM or actual multi-agent coordination is used.

These tests do **not** make Python/PyYAML a prerequisite for ordinary standalone AOS-W, and do not prove a working always-on graph engine, real external account permissions, distributed locking or full JSON Schema validation.

## Prompt 11 state/recovery suite

Run `python -m unittest discover -s tests -p 'test_state*.py' -v` for the **26** local state/recovery/CLI tests, or `python -m unittest discover -s tests -p 'test_*.py' -q` for **37** total (including the 11 composition tests). Python/PyYAML are optional maintainer tools, not installed scaffold requirements. The new tests cover historic event preservation, SHA-256 integrity, torn-tail quarantine, checkpoint recovery, bounded retries, QC correction, uncertain provider intent dedup, explicit pause/resume/cancel/fail, stale artifact blocking, graph revision recovery, and no duplicate child creation. See `temp/tests/PROMPT-11-STATE-CONFORMANCE.md` for actual scope and limitations. No real external accounts were used.

## Prompt 12 governance tests

`python -m unittest discover -s tests -p 'test_governance*.py' -q` executes **38** new local tests. `python -m unittest discover -s tests -p 'test_*.py' -q` executes **75 total**, including Prompt 11's 26 and Prompt 10's 11. These run entirely against synthetic files and self-declared actors, not real providers, signed approvals or enforced distributed locks.

## Prompt 14 optional ZIP and installation tests

`python -m unittest discover -s tests -p 'test_distribution.py' -q` runs **18** new synthetic ZIP/install/upgrade, malicious archive and clean cold-start checks. `python -m unittest discover -s tests -p 'test_*.py' -q` runs **108 total** with all previous Git, governance, state and composition tests. The optional tool uses Python stdlib only for ZIP/upgrade; optional `aosw-ops.py init` needs PyYAML but the downloaded folder works manually without any Python. A separate GitHub Actions workflow builds the release from the **complete** scaffold and tests installation/upgrade; report that hosted result separately from local fixture tests.
