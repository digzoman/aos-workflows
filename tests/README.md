# Optional executable conformance tests

Run from the repository root in a developer environment with Python 3 and **PyYAML** installed:

```sh
python -m unittest discover -s tests -p 'test_composition.py' -v
```

The tests exercise pure local-file composition semantics, deterministic child proposals, approval-gated materialization into a temporary `agent-files` directory, independent review-before-merge, protected policy inheritance, three-valued conditions, explicit revision invalidation and path confinement. All fixtures are synthetic and no network, Meta, CRM or actual multi-agent coordination is used.

These tests do **not** make Python/PyYAML a prerequisite for ordinary standalone AOS-W, and do not prove a working always-on graph engine, real external account permissions, distributed locking or full JSON Schema validation.
