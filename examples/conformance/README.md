# AOS-W 0.2 composition conformance fixtures

`planning/` contains synthetic, **MOCKED** portfolio research inputs, proposed child investigations and deliberately simulated approvals/reviews. They are not real ads, proof of published work, credentials, or authorizations for any external system.

Included:

- `portfolio-plan.json`, a versioned plan for coaches, agencies and roofing businesses.
- `child-proposals.json`, deterministic proposals only, not started instances.
- `approval-mock.json`, simulated instantiation permission for test-only temporary `agent-files` directory.
- `child-results-mock.json`, all current PASS outcomes **simulated** so that merge conditions can be tested.
- `synthesis-approval-mock.json`, simulated permission to consolidate, not permission to publish.
- `graph-state.json` and `graph-context.json`, evidence-aware parent run eligibility inputs.
- `revised-child-graph.yaml`, changed investigation requiring downstream impact analysis.
- `expected-negative.json`, safety expectations.

Use `python -m unittest discover -s tests -p 'test_composition.py' -v` if optional PyYAML is installed. The tests perform **local filesystem operations only** and create/delete temporary `agent-files` directories. They neither scrape current advertisements nor alter live accounts.
