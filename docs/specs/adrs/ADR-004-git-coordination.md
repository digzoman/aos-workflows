# ADR-004, Keep Git coordination optional; prototype CAS claims and LFS locks

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

User requires both approaches tested. Git LFS file locks are account/path oriented [W11]; worktree lock prevents pruning only [W10]. Git ref updates/push have fast-forward and explicit expected-ref lease semantics, but generic GitHub REST PATCH does NOT provide an expected_sha parameter [W12].

## Proposed decision

Provisional preference for per-task remote claim refs with **proven** atomic creation/update, logical agent ID, finite lease, unique fencing epoch and remote reconciliation. Keep LFS for experimental comparison/optional binary locks. No hard exclusive remote claim while offline. Do not commit to a winner before two-agent race tests.

## Alternatives and tradeoffs

LFS same-login agents may both be classified as the owner; locks can stick after crash and target files not tasks. CAS refs are more complex, require reliable expected-old value primitive, lease/fencing and reserved ref namespace, and cannot prevent bypass by a noncooperative agent. Worktrees isolate edits but do not arbitrate tasks.

## Validation and reconsideration

Prompt 13 prototype both; Prompt 17 simultaneous same-account claims, stale takeover, crashed owner, network loss and ambiguous push verification. If CAS unavailable through target connector, choose a different coordination primitive or limit to single writer.
