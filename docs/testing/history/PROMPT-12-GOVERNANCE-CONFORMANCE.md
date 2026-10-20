# Prompt 12 governance conformance — 2026-10-20

**Execution mode:** Real local Python 3/PyYAML filesystem tests using temporary synthetic `agent-files` instances; **no actual external provider, authenticated identity, unattended worker, shared Git locking or real human approval performed**.

## Verified test results

```sh
cd /path/to/aos-workflows
python -m unittest discover -s tests -p 'test_governance*.py' -q
# Ran 38 tests — OK
python -m unittest discover -s tests -p 'test_state*.py' -q
# Ran 26 tests — OK
python -m unittest discover -s tests -p 'test_composition.py' -q
# Ran 11 tests — OK
python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 75 tests — OK
```

The new optional governance adapter is in `tools/governance/governance.py`; its CLI subprocess test was included. Earlier state and composition suites also passed without modifications to their fixture definitions. The Prompt 11 state reducer was extended with additive governance event types, and its optional context gate now allows the governance adapter to run authorized local tasks which previously had to be manually gated. Existing non-governance callers retain prior conservative behavior and all 37 older tests pass.

## Positive and negative cases exercised

1. Four-part agent provenance, invalid/missing identity rejected, claims and transition records contain actor fields and timestamps.
2. Single-writer advisory claims, denial of concurrent different-owner claim, release and controlled reassignment, no hard-lock claim.
3. Parallel task capacity and dependency blocking: sibling `parallel` can complete when `draft` fails independent QC; dependent remains ineligible until current PASS/allowed waiver.
4. Deterministic artifact digests, independent AI reviewer distinct from producer even when role label changes, human-declared reviewer and explicitly permitted self-review.
5. Task-specific default gate conjunction: passing only one of two required gates cannot finalize; full currently hashed artifact set and current attempt+graph revision required.
6. REVISE with source-specific remediation record, explicit correction evidence, bounded requeue, new attempt and revised artifact ID/revision/hash, old reviewer history retained.
7. Missing, changed, or mismatched artifacts fail closed; old PASS cannot be reused for new bytes or new attempt.
8. Action classes and task/workflow ceilings: ungranted send blocked, wildcard resource approval rejected, incorrect resource or action blocked, declared human approver required.
9. Grant expiry, revocation via new audit record and graph-revision invalidation (old grant not reused).
10. Budget action requires actual limit/amount and denies over-limit attempt. No API action occurs.
11. Operation-intent wrapper performs scope check before recording mock provider intent; it never sends a message. Existing state helper retains ambiguous-operation no-duplicate protections.
12. Same event history hashes and append-only files preserve approvals, reviews, release, remediation, handoffs and full actor provenance; altering the approval JSON without a matching validated event record is rejected.
13. Explicit owner waiver only for a gate declared `waivable: true`, not the deterministic protected gate without opt-in. Aggregate result `ACCEPTED_WITH_WAIVER` is distinct from underlying evidence PASS.
14. CLI `inspect` works against a local run; unauthorized `authorize` command fails with a nonzero exit code.

## Implementation security limitations

- The local helper **does not authenticate** owner/reviewer identities, implement cryptographic signatures, enforce OS filesystem isolation or create hard distributed task claims. It checks declarations within records and journal consistency. A malicious actor with filesystem access can modify records/code or bypass the optional helper. Only actual host/provider authorization can enforce actions.
- `context_checked` in the optional state helper is a caller-asserted local gate; it must not be described as a trusted proof. File-only agents follow `references/PROVENANCE-QUALITY-PERMISSIONS.md` instead of installing Python.
- Review PASS for semantic criteria is a **recorded evaluator assertion**, not proof the AI model actually inspected images/source; deterministic hashing proves only byte identity. A `role=owner` label is not an authenticated human click.
- The helper stores record before appending its immutable event; a crash between those writes can leave an orphan JSON record. The event-ledger cross-check fails closed until manual reconciliation. Multi-file atomic commit requires a supported host/transaction layer and remains unimplemented.
- The optional helper does **not** contact Meta Ads, GHL, Git, websites, inboxes, social accounts, or any third-party service; `operation_intent` remains local only.
- Real multi-agent collision prevention and shared Git identity tests are planned for Prompt 13, not demonstrated here. Cross-platform test T02, collision test T03 and the other V1 acceptance demonstrations are still not completed by these unit tests.

## Next phase

Prompt 13: optional Git mirroring, test both Git LFS and atomic Git task-claim approaches with real simultaneous workers, same GitHub identity, crash/lease reclamation, ambiguous network results, and stale-owner fencing. Retain standalone no-Git file workflow.
