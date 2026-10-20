# Git LFS, atomic Git claims, worktrees and offline coordination

Prompt 06 **research and provisional recommendation, not a test report**. See W10–W12 in [SOURCES-06.md](SOURCES-06.md) for upstream documentation. The user's standing requirement is to **prototype both** and test two-agent races before selecting a winning implementation (Prompts 13 and 17).

## Candidates compared

| Dimension | Git LFS locks | Atomic Git task-ref claims | Git worktrees | Plain claim file without atomic host |
| --- | --- | --- | --- | --- |
| Enforced unit | Remote lock on a **path**, push restrictions for other Git LFS users when locks verification supported | Per-task branch/ref update representing expected revision and owner/lease token | Separate local checkout/branch; `worktree lock` prevents pruning, not task editing | Advisory serialized owner |
| Shared GitHub identity | **Weak fit**, both agents may appear as the same lock owner and lack exclusion | Can still arbitrate if each claimant uses atomic create/version-checked ref update; agent ID in claim payload separate | Same host may avoid same branch checkout conflicts, but cannot coordinate other hosts | Cannot guarantee unique claim |
| Concurrency | Server lock coordination by path | Remote ref creation/update race; only one competing update based on **same expected old ref** should commit when correct primitive is used | Local workspace separation only | Two agents can both write 'owned' |
| Arbitrary logical task | Must designate a concrete existing lockable file, potential lifecycle proliferation | Task ID maps naturally to one ref/claim record | Does not express task/approval | Can name task but not enforce |
| Offline behavior | Cannot acquire/check current server lock offline | Cannot acquire/renew remote claim offline | Independent local work possible, no shared remote arbitration | Best-effort/no remote exclusivity |
| Crash/abandoned | Lock remains until unlock/force unlock; built-in automatic task TTL not established | Lease expiration **recorded**, but takeover must use fresh remote CAS/compare and fencing | Stale worktree metadata can be pruned/repaired, not work lease | Manual reconciliation |
| Extra dependency | Git LFS executable/client/server and configured lock verification | Git+remote with suitable atomic ref behavior or connector/API implementing equivalent | Git | None, but no hard safety |
| Task output integration | Locking file path not separate QC/approval source | Can keep claims distinct from workflow main branch and merge results after review | Multiple branches/workspaces can help | Single-writer convention only |

**Key verified docs:** LFS lock is created on server for a path and push verification prevents *other users* changing locked files; it does not provide an agent-identity-aware lock when multiple agents authenticate as one user [W11]. `git worktree lock` prevents worktree administrative pruning/moving, not source file/task write conflicts [W10]. Git remote ref updates enforce fast-forward by default, but the generic GitHub REST PATCH ref interface has a `sha` and `force`, **not a documented expected_sha** [W12]. An available specific connector's `update_ref(expected_sha)` capability is **not** proof that GitHub REST itself exposes a standard CAS parameter.

## Important CAS and race nuance

**Proposed for later test**, not proof: represent each active logical task's authority as a dedicated remote ref and immutable claim commit recording `claim_id`, `actor` four-field identity, `run_id`, `task_id`, `acquired_at`, `expires_at`, `base_revision`, `fencing_epoch`, `status`, and `last_heartbeat`.

- For first claim, use **atomic create-if-absent** semantics on the task ref. Two agents racing to create the identical ref cannot both win if the Git server truly serializes ref creation.
- For renew/release/reclaim, require conditional update based on the **exact observed old ref** using a verified expected-SHA mechanism, e.g., Git `push --force-with-lease=<ref>:<expect>` or a connector explicitly supporting the expected old SHA. A generic ordinary fast-forward patch by itself may not implement task-level compare-and-swap when ref histories/commit ancestry are not designed carefully.
- Explicit `--force-with-lease` does **not** grant permission to replace arbitrary unrelated history. Work exclusively in reserved claim-ref namespaces, never rewrite workflow data or `main` to acquire a lock.
- A lease expiry timestamp alone is **not** atomic reclamation. Recovery must read latest ref, consult current claimant heartbeat/status, apply a conditional ownership change with new **fencing token/epoch**, and verify it persisted. A stale previous agent must not be allowed to commit final authoritative task output after a different claimant takes over. This requires an output-commit validation step.
- Shared credential is okay only if **logical agent identity in the claim** is separate and every writer honors the protocol. It is not proof of identity against a malicious agent.
- When network is absent/unknown, never silently assume the remote claim expired or remains owned. Suspend shared writes or switch to an explicitly consented single-agent offline fork that reconciles later. This is a **tradeoff** rather than offline multi-agent exclusivity.

## Why LFS may still be useful

LFS locking can protect nonmergeable external creative binaries or designated review artifacts when all participants use correct LFS clients, identities and server support. It is poorly matched as the **default task scheduler/owner registry**, because AOS-W tasks are logical graph nodes, not necessarily one LFS-tracked file. Locks left by crashed agents require active unlock/reconciliation; no automatic TTL guarantee is documented.

## Worktrees are orthogonal

Git worktrees help Fred/Muse or several coding agents keep independent branches and edits isolated while sharing repo data. They do **not** offer multi-host/task-exclusive checkout. Use optionally for parallel code/artifact branches, not for claim arbitration.

## Test plan, explicitly future

Prompt 13 prototype and Prompt 17 validation should run:
1. Two agents use **same GitHub account** to claim **same task** at the same instant; prove only one receives a valid claim token in each contender method.
2. Distinct-agent GitHub credentials, same-task race; repeat many times, record ref/lock response and remote read-back, not screenshots alone.
3. Two **different tasks** claim concurrently, verify both can progress without blocking.
4. Agent crashes after claim, after local task completion but before commit, and after external side effect but before verification.
5. Lease expires, stale owner tries to submit completion after takeover; require fencing or explicit rejection.
6. Network outage during lock acquire, renewal, release, and remote push; show conservative degraded behavior.
7. Two clones/worktrees and concurrent branch updates, including force/no-force behavior, expected SHA mismatch and task-claim ref misuse.
8. LFS locking of path with same credential, verify whether second client is treated as same owner; compare force unlock impact.
9. Lost/ambiguous update response, immediate read-back identifies real winner without generating duplicate claim or production side effect.
10. Portability: downloaded scaffold with no Git/LFS still runs human-guided one-agent tasks successfully.

**Provisional choice for PRD discussion:** reserve CAS-backed Git task refs as the preferred shared-Git strategy because they are task-centric and can distinguish logical agents even with common GitHub transport. Keep Git LFS as optional file-level protection and empirical competitor; don't mark either mechanism proven or reject the user's planned comparison. The protocol must remain meaningful in manual one-agent mode with **no hard mutex claim**.
