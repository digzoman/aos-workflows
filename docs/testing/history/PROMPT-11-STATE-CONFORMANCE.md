# Prompt 11 — Persistent state, recovery and retry conformance

**Executed:** 2026-10-20. **Test scope:** local isolated Python 3/PyYAML fixtures; no network APIs, Meta/GHL credentials, cloud schedulers, authenticated human approvals or concurrent agents. **Assessment:** 26 new tests PASS, 11 previous Prompt 10 tests PASS, 37 combined PASS. This report does not assert the full V1 six mandatory cross-agent demonstrations are passed.

## Executed commands and observed results

```sh
cd /path/to/aos-workflows
python -m unittest discover -s tests -p 'test_state*.py' -q
# Ran 26 tests — OK
python -m unittest discover -s tests -p 'test_*.py' -q
# Ran 37 tests — OK
```

The optional state CLI was also invoked as a subprocess in `test_state_cli.py`, using a real temporary instance, pinned YAML graph, actor identity, checkpoint and recovery readback. It returned CREATED state and a consistent event sequence after checkpoint/recover. All outputs are synthetic local files.

One initial combined run reported two errors because the pre-existing Prompt 10 Ontario custom-overlay test fixture had **not been copied into the isolated workspace**. After restoring the exact existing fixture (without changing implementation), all 37 combined tests passed. Those initial errors were test-environment setup failures, not ignored test results.

## Positive and negative coverage, actually exercised

1. **Fresh agent/session:** independent `RunStore` object with a different four-field actor recovered current run identity, accepted completed step, owner, evidence and newly eligible successor from persisted files only. This is NOT a real different AI platform.
2. **Bounded transient retry:** source-unavailable failure recorded correction, attempts, 60-second fixed delay, attempt-2 on permitted invocation and separate attempt-history files. Immediate retry blocked.
3. **Exhaustion and explicit fail:** max-attempt policy produced terminal task failure, disallowed requeue and recorded explicit `run_failed`.
4. **Incomplete evidence:** missing artifact or wrong SHA-256 could not complete; correction required acknowledgement and a new bounded attempt.
5. **QC revision:** a failed review persisted REVISE/correction; old review could not count as PASS; a second attempt with a new output hash and current exact PASS review completed. This was a mocked local reviewer decision, not external reviewer independence.
6. **Pause/resume/cancel:** run PAUSED blocked starts, task PAUSED resumed through a new attempt, and explicit cancellation prevented further task execution.
7. **External operation ambiguity:** operation key recorded before submission, repeated intent rejected, ambiguous ACK marked RECONCILE_REQUIRED; no completion or replay before a supplied readback reference. No real provider contacted.
8. **NOT_APPLIED reconciliation:** only after explicit readback and `task_unblocked` could a fresh attempt use a new operation key referencing the original; a false prior reference was rejected.
9. **Torn JSONL:** half-written trailing line caused fail-closed load, no automatic deletion; explicit recovery quarantined original tail bytes and kept the accepted event prefix unmodified.
10. **Digest tampering:** mutated event line was rejected, preserved for authorized manual repair and never counted as valid historic completion.
11. **Stale derived snapshot:** invalid event sequence or task data was preserved in `recovery/`, state rebuilt from the accepted journal, and recovery event appended.
12. **Checkpoint validation:** mismatched event digest and orphan checkpoint detected. Neither replaced validated event history.
13. **Graph revision application:** approval-scoped g0002 file and graph-revised event preserved unchanged completed work; changed/descendant results invalidated with old evidence in `superseded_results` and previous completion events retained.
14. **Crash after graph event:** stale run current-revision pointer recovered only after checking saved immutable g0002 digest; prior graph remained available.
15. **Changed/missing prior artifact:** historic COMPLETE event kept, but current derived state blocked descendants after detecting output SHA mismatch.
16. **Direct-state bypass:** `task_ready` or `task_claimed` on dependent node before predecessor completion refused.
17. **Pinned graph integrity:** mutation of original immutable graph bytes detected on a fresh session.
18. **Legacy compatibility:** older 0.1/0.2 journal records lacking digests remained readable with integrity level ADVISORY; subsequent hashed events did not silently promote legacy history to fully verified.
19. **Unsafe shared mode:** optional helper refused mutation under `shared_coordinated` without a verified adapter.
20. **Partial generated-child batch:** read-only audit identified PARTIAL and MISSING child directories without creating/overwriting work; unsafe child ID blocked.
21. **CLI smoke:** inspected, checkpointed and recovered a real temporary local run from a new subprocess.
22. **Prompt 10 regressions:** all original 11 graph/template/composition tests passed after restoring their test fixture.

## Data model and durability actually supported

- SHA-256 chained append-oriented JSONL events, actor identity, task transition validation, attempt counters, recorded owner, artifact hashes, provider operation records, revision IDs, and precise next-eligible local candidates.
- Rebuildable `state.json`; checkpoint anchored to a saved verified event prefix; optional fsync and atomic replace on compatible local filesystems. Handoff JSON/Markdown written under the run directory.
- Explicit `recovery_checked` event, stale snapshot backups and quarantine of suspect log tails **only on authorized repair**. No automatic elimination of unverified history.
- Retry after review, incomplete evidence and manual intervention requires explicit acknowledgement, and future delay time is checked only when an agent/host invokes the workflow.
- No external provider mutation is performed by the optional state CLI; provider ACK/readback fields are supplied, and externally authenticated truth is not attested by these local tests.

## NOT EXECUTED / NOT PROVEN

- Hard multi-writer mutual exclusion, distributed Git atomic claims, real cloud-persistence durability or crash-atomic multi-file transaction. Host fsync/rename cannot guarantee uninterrupted work across all storage providers.
- Real external provider readback or idempotent Meta/CRM mutations; readback records were mocks or operator-supplied references.
- Actual independent AI review, authenticated owner approval, multi-platform handoff or live operational grants. Local tests use simulated reviewer/approval identities.
- Unattended retry timer, scheduled wake, automatic workflow dispatcher, programmatic selection of every conditional/compound step, or safe automated provider replay.
- Full JSON Schema Draft 2020-12 validation of all bundled schemas with a separate validator; schema records were updated in this commit and need full validation in a subsequent hardening step.
- Actual remote Git checkout/release ZIP build from this offline test environment.

**Next:** Prompt 12: agent provenance, stronger approval/QC mechanics, reviewer independence and just-in-time skill resolution. Then Prompt 13: Git synchronization and experimental real two-agent exclusive claims. Preserve the file-only/no-runtime minimum.
