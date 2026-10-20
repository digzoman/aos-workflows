# Optional AOS-W composition helper

The downloadable AOS-W scaffold operates through instructions and files; **no Python or packages are required** for a capable agent to follow the manual protocol. This optional helper is for maintainers/agents whose host already supplies Python 3 and PyYAML (`pip install pyyaml` if they choose to use it). It does not fetch provider data, send messages, run ads, schedule jobs, or supply hard multi-agent locks.

From the development repository root:

```sh
python tools/composition/cli.py validate scaffold/aos-w/templates/competitor-investigation/template.yaml
python tools/composition/cli.py classify scaffold/aos-w/templates/research-portfolio-planner/template.yaml examples/conformance/planning/graph-state.json --context examples/conformance/planning/graph-context.json
python tools/composition/cli.py propose examples/conformance/planning/portfolio-plan.json scaffold/aos-w/templates/competitor-investigation/template.yaml --output scaffold/aos-w/agent-files/cache/child-proposals.json
python -m unittest discover -s tests -p 'test_composition.py' -v
```

**Only agent-files is writable in normal operation.** The CLI refuses any `--output` outside a directory named `agent-files`. The `materialize` command checks the named proposal IDs, owner approval fixture, plan revision and exact child template SHA-256 before writing new child instances; it stops rather than overwriting existing instance IDs. It is not an atomic distributed transaction. In a real workflow, replace simulated fixture approvals with actual owner-issued approvals with checked authority. CLI commands are demonstrations, not proof that a user independently reviewed the result.

`revision-impact` merely reports changed/invalidated/preserved step IDs; it does **not** edit history or apply any graph revision. True event-backed revisions are Prompt 11. JSON Schema library validation and later race tests are separate from this optional helper.

To run the tests with no real external account: copy the fixture data from `examples/conformance/planning/` or use the `tests/` suite. All fixtures refer to fictional/sanitized example categories and are not live Meta campaign data.
