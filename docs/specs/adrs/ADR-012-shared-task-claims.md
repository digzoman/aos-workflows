# ADR-012: Separate advisory task ownership from proven exclusive coordination

**Status:** PROPOSED, Prompt 08 technical design; **not owner-accepted**. 2026-10-20. PRD review record remained pending when this document was written.

## Context
User selected per-task owner/expiry and comparison of Git LFS locking and atomic Git claims. Agents may share GitHub credentials, network may fail, stale claims persist.

## Proposed decision
Single agent uses an advisory claim file and one-writer assumption. Shared mode only declares enforced exclusivity if the actual backend demonstrates atomic creation/update and fencing. A remote outage or expired timestamp alone never grants takeover. Prototype Git LFS and Git ref CAS side by side; defer final backend choice.

## Consequences and alternatives
Optimistic local claims are portable but not a distributed mutex. Git LFS path/account semantics may not distinguish shared-login agents; CAS ref pushes need a proven expected-old-SHA mechanism, crash recovery and fencing. Worktrees isolate copies, do not lock tasks.

## Required validation and reconsideration
Prompt 13/17 real two-agent simultaneous collision, common login, stale submission after reclaim, ambiguous response and network partition. Mark untested until exercised.
