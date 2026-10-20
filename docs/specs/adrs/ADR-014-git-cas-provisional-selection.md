# ADR-014: Prefer explicit Git-ref CAS for optional multi-agent claims (provisional)

**Status: PROVISIONALLY SELECTED FOR OPTIONAL PROTOTYPE ONLY — not accepted as production-hardened.** October 20, 2026. Does not supersede all prior PROPOSED ADRs or make Git mandatory.

## Context

AOS-W must support standalone file-only operation and optional Git synchronization. Some agents (including ChatGPT, Codex, Claude or custom harnesses) may share one GitHub credential. Agent identity `[Agent | Platform | Role | Instance]` must remain independent of Git login. Git checkout and worktrees do not provide exclusive task locks. Network loss, crash, stale leases and concurrent writers cannot be handled safely by a local `claim.json` alone.

## Alternatives and observed evidence

| Criterion | Git LFS path lock | Explicit remote Git ref CAS |
| --- | --- | --- |
| Resource | Existing file path with LFS lockable attributes | Per-task claim ref/branch and JSON state in ref commit |
| Extra requirement | Git LFS binary + lock-supporting server + hook/verification | Git executable + remote that permits namespaced branches / explicit leases |
| Actual local execution | Git LFS binary **absent**; wrapper and a simulated API parsing test only | Real local bare Git remote; competing workers, reclaims, partitions, conflict tests **PASS** |
| Same Git authentication | Server owner is Git user; not sufficient to distinguish agents | Ref content includes separate four-part agent ID, random token and increasing epoch; one CAS winner independent of shared account |
| Concurrency boundary | Server path lock if host enforces and push verifies (not tested here) | Server atomically accepts/rejects one ref update against explicit old SHA (tested on local bare remote) |
| Crash/stale claim | Requires lock listing, manual force unlock/risk of someone else's working copy | Expiry alone never grants takeover; explicit reviewed reclaim reason and new CAS epoch; stale token rejected |
| Offline | Lock verification impossible; cached locks stale | Remote ref check impossible; shared mutations fail closed |
| External APIs | Cannot fence Meta/GHL side effects | Cannot fence Meta/GHL side effects; separate idempotency/provider approval required |
| Portability | Requires LFS installed in all participating hosts | Basic Git feature in optional Git mode, no extra LFS install |

References: <https://git-scm.com/docs/git-push> (explicit expected-old SHA lease), <https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-lock.adoc>, <https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-locks.adoc>, <https://github.com/git-lfs/git-lfs/blob/main/docs/api/locking.md>, <https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-config.adoc>.

## Decision

Use **explicit old-value ref CAS** as the *preferred experimental* claim mechanism **only in configured `shared_coordinated` mode** when the selected remote is reachable and the actual ref namespace is confirmed supported. Store owner, separate agent provenance, token, epoch, lease and prior ref in each claim commit. For any missing remote capability or failed compare-and-swap, stop shared work rather than downgrade silently to advisory claims.

Keep a Git LFS wrapper as an alternative test adapter for teams that already use server-managed file locks, but do **not** select it as the primary AOS-W per-task lock based on a Git user alone.

## Decision limitations and validation required

1. **No hosted GitHub push test**: this environment cannot resolve `github.com` for Git transport; public GitHub tool access was used for repository changes, not actual competing remote Git push experiments. Test remote branch namespace permission, protected branch rules, consistent CAS and GitHub API view before declaring hosted mode reliable.
2. **No real Git LFS lock-server test**: `git-lfs` is not installed. The LFS comparison is based on protocol/docs plus a mocked parser. Need live install/server tests including same credential and server-side enforcement on pushes.
3. Local bare Git experiments are real concurrency and Git transport tests, **not** provider-side fencing or exactly-once execution guarantees.
4. Logical actor fields and claim tokens are **not authenticated**, and an agent with remote push permission could bypass the protocol. Enforced outside actions require provider-side authority; token/epoch checks constrain *cooperative clients* only.
5. No atomic transaction spans Git claim refs, workflow data files, local checkpoints and provider writes. Recovery must reconcile all authorities individually.
6. Explicit lease checks use local UTC clocks; significant clock skew can alter expiry/reclaim decisions. Never auto-steal based on time alone.
7. Dedicated branch refs may be visible in public repositories and accumulate. No automatic sweeping/deletion; future admin cleanup must preserve an auditable history and avoid leaking private task titles.

**Next acceptance gate:** Run two independent hosted workers with shared authentication against a temporary protected-test repo, verify one winner, interrupt/reclaim, force a network failure and recover, then compare with actual Git LFS server locking. Until then, mark Git CAS as **PROVISIONAL** and default AOS-W to standalone single-writer.

## Prompt 17 local acceptance update (2026-10-20)

The existing local ref CAS approach passed 11 additional real local Git/multi-process integration scenarios covering task discovery/ownership, separate child runs, checkpoint and handoff provenance, divergent history, reviewed synthetic merge, suspended worker, stale token and transfer to a second remote. The claim release implementation was tightened to check the exact four-field owner actor. This improves audit consistency but not authentication. A dedicated hosted GitHub CAS/LFS probe is provided in Actions and must be **observed** before upgrading this ADR from provisional. No real Codex, Claude, Muse or other independent AI provider was tested.
