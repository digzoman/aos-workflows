# Prompt 13 — Git synchronization and multi-agent coordination experiments

**Date:** 2026-10-20. **Host:** Git 2.47.3; Python 3 stdlib test harness, local temporary Git bare repositories; no user credentials/remote cloud service. Full earlier AOS-W source fixtures included after an initial isolated-workspace setup correction. **Live Git LFS and hosted GitHub push tests: NOT RUN.**

## Tests actually executed

- `python -m unittest discover -s tests -p test_git_coordination.py -q` → **15 PASS**.
- `python -m unittest discover -s tests -p 'test_*.py' -q` → **90 PASS** (15 new + 38 governance + 26 state/recovery + 11 composition).
- Two clones of one bare Git remote used identical Git `user.name` and `user.email` while declaring distinct four-part agent identities.
- Explicit initial expected-absent ref CAS yielded one winner and one loser in simultaneous competition. Repeated six distinct task races yielded exactly one ref winner each.
- Stale worker could not verify or release a newer epoch after original release and re-claim.
- Expired claims did **not** auto-transfer: manual reviewed rationale + expected-old SHA CAS were required for reclaim, and old token invalidated.
- Remote disconnect caused acquisition, verification and release to block instead of relying on stale caches.
- Sync preflight/refresh allowed clean fast-forward; divergent local commits or dirty worktrees were not overwritten/auto-merged.
- Only requested paths under `scaffold/aos-w/agent-files/` were accepted for commit staging; agent provenance commit trailer recorded separately from shared Git user.
- Optional CLI read-only remote status wrote a sync-state file inside agent-files/config, without credentials.
- Git LFS binary not available; candidate correctly returned unavailable rather than fabricating a live lock. Mock JSON fixture demonstrated LFS server owner represented the shared Git account, not individual AOS-W agent.

## Test classification

| Capability | Classification | Result |
| --- | --- | --- |
| Git CAS new ref competition, same authenticated account, one winner | REAL LOCAL GIT | PASS |
| Concurrent CAS race repeated with two clones | REAL LOCAL GIT | PASS, 6/6 single winner |
| Stale ownership, explicit expired reclaim, epochs | REAL LOCAL GIT + simulated older timestamp | PASS |
| Network unavailable | TEST-INDUCED local remote failure | PASS, fail closed |
| Divergent branch + dirty worktree sync preservation | REAL LOCAL GIT | PASS |
| Optional LFS binary detection | REAL ENVIRONMENT | git-lfs not installed |
| LFS lock JSON behavior | MOCKED | Parsed, not real server test |
| Two remote GitHub workers race or GitHub branch creation rules | NOT RUN | Git transport DNS lookup failed |
| True multi-agent provider-side fencing/exactly-once effects | NOT IMPLEMENTED | Block external effects absent other authority |

## Comparative recommendation

**Preferred optional coordinator: explicit Git-ref CAS**, provisionally, because atomic expected-old-SHA behavior was observed on a real local bare Git server, it exposes distinct logical actor fields despite identical Git account credentials, and it does not require Git LFS. **Do not claim a validated GitHub-hosted lock**; GitHub protected branches, named refs, transport authentication and Git LFS actual server behavior require separate tests. No fallback to advisory multi-agent claims is acceptable when a remote is unavailable.

## Operational limitations

Git itself is an **optional** sync/coordination dependency; base file-only operation remains unchanged. Claim ref CAS serializes **one ref**, not an arbitrary file write or API effect. One authenticated user can deliberately bypass logical actor metadata. A claimant crash/lease expiry requires manual reclaim and investigation of pending provider actions. There is no shared transaction across claim ref, workflow event journal, remote branch and provider side effect. Public claims must not include secrets or sensitive customer information.

## Test environment note

The initial combined regression run returned missing-file errors because the isolated test folder lacked pre-existing Prompt 10 planning YAML and JSON fixtures. These were restored unchanged from the prior test workspace, and all 90 tests then passed. The failure was an environment setup omission, not a behavioral test passed by assertion.

## Follow-up before production capability status

1. Verify Git CAS refs and branch protection on the actual chosen GitHub host using disposable test branches and two distinct harnesses sharing a GitHub authentication identity.
2. Install Git LFS in a separate test environment and test true server lock/verify/unlock, same account actors, stale ownership and push enforcement.
3. Exercise live remote disappearance/reconnection, conflict queues and independent owner escalation; add a provider-side fencing/idempotency layer before any consequential external action.
4. Add explicit mode validation/release tests and containerized installer cold-start to Prompt 14–17. Do not mark T01–T16 complete here.
