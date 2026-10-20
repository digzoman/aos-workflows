# Prompt 10 conformance report — reusable templates and composition

**Date:** 2026-10-20. **Mode:** real local process execution with synthetic inputs, no external provider access. **Scope:** optional Python/PyYAML helper (not a standalone prerequisite), versioned YAML template fixtures and files under temporary `agent-files`. The repository's file-only manual protocol is separately documented and remains operational without this helper.

## Validation executed — PASS

Executed in the isolated local container using **byte-for-byte identical** copies of the committed candidate `tools/composition/composition.py`, `tools/composition/cli.py`, `tests/test_composition.py`, the new YAML masters, overlay and JSON fixtures. Checked Git blob SHA-1 correspondence for key code/template/fixture sources against GitHub's staged tree before publishing.

```sh
cd /path/to/aos-workflows
python -m unittest discover -s tests -p 'test_composition.py' -q
# Ran 11 tests in approximately 0.24 seconds
# OK
```

11 test methods exercised the following positive and negative cases:

1. All five bundled master graphs validate with explicit task inputs, outputs, QA and done-when execution contracts.
2. A DAG cycle and a node missing its execution contract are rejected.
3. A custom regional overlay resolves only against the exact base SHA-256 and version; bad pin or expanded allowed actions fail.
4. Parallel readiness and three-valued conditional UNKNOWN semantics are deterministic.
5. Stable per-item child proposal IDs, explicit input/output/QC contracts; duplicate slug and unapproved parent planning input blocked.
6. A synthesis merge requires exact separate authorization and **every child's current PASS review**. Unreviewed child blocks merge.
7. A material graph revision requires separate approval; changed node and transitive descendants invalidated, unaffected completed work preserved.
8. Scoped child instantiation creates three independent local instance/run directories with copied pinned template, initial event, state and handoff. Wrong approval or mismatched child set blocked; rerun with existing IDs refused.
9. Path traversal outside `agent-files` refused.
10. The dynamic synthesis readiness node stays blocked for missing approval, waiting for missing child results, READY only when all accepted, and waiting again if any review changes to REVISE.
11. Added external-action permissions, removed step QA gates, missing skill or unavailable host capability are blocked.

## CLI smoke tests — PASS

Directly invoked the optional `tools/composition/cli.py` commands `validate`, `classify`, `propose`, `materialize`, `merge`, and `revision-impact` against the sanitized fixtures. The status assessment returned `propose-investigations: ready` and `synthesize: waiting`. The approved fixture instantiation created exactly:

- `bucket9-research-coaches-r0001`
- `bucket9-research-agencies-r0001`
- `bucket9-research-roofing-r0001`

The resulting local instances began CREATED with no completed research and no external provider operations. The synthetic all-PASS fixture returned `READY_FOR_SYNTHESIS`. Revision impact of a changed `search-ads` instruction marked `search-ads`, `extract-offers`, `verify-evidence`, and `review-investigation` invalid, while preserving the earlier scope step.

## Existing pinned run preservation

The 0.1.0 practice instance under `agent-files/instances/demo-local-research/` remains pinned to its original immutable 0.1.0 source and g0001 snapshot, even though the protected master `research-starter` has advanced to 0.2.0. The optional `scripts/validate-scaffold.mjs` was updated to compare the historic snapshot to its own graph and digest instead of assuming it must equal the latest master. This is a **documented compatibility update**, not a claim that the optional Node validator was executed in this test run.

## NOT RUN / NOT PROVEN

- Full JSON Schema Draft 2020-12 validation against every YAML document using a remote-installed schema validator; structural fields were added to both `common.schema.json` copies and YAML graphs were validated by the optional Python helper.
- Actual second-platform, cross-session handoff or a real multi-agent collision race.
- Cryptographic authentication of owner approvals. File-only mode is cooperative; the fixture `approval-mock.json` is test-only, not real delegated authority.
- Distributed/transactional child creation or crash-atomic event append. The optional local materializer prevents known duplicate IDs and stops on errors; a crash during multi-child write requires manual recovery.
- Automatic graph task dispatch, scheduled triggering, automatic review model calls, Meta/HighLevel/website changes or live advertisements.
- Actual application of a graph revision to live run history; the helper produces the impact plan and manual protocol describes event-backed application. Prompt 11 implements durable state/recovery.

**Result:** Initial Prompt 10 reusable composition mechanism, local child instantiation, policy checks and conformance fixtures PASS at the stated local/testing scope. More stringent implementation and release tests remain future work.
