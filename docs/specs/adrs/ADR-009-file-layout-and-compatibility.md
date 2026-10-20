# ADR-009: Protected scaffold and per-instance immutable template snapshots

**Status:** PROPOSED, Prompt 08 technical design; **not owner-accepted**. 2026-10-20. PRD review record remained pending when this document was written.

## Context
User Q05/Q06/Q16 require downloadable scaffold and agent-files-only ordinary writes. The PRD also requires compatibility and no mandatory Git/runtime.

## Proposed decision
Standard definitions live read-mostly in scaffold/aos-w. All custom templates, resolved source snapshots, instance manifests, immutable graph revisions, runs/attempts/checkpoints/claims/reviews/approvals/handoffs live under agent-files. A run pins resolved template bytes/content revision and never rereads an upstream mutable template as its current graph.

## Consequences and alternatives
Separate active data from release upgrades. More files create small manual overhead but make cold start and preservation reliable. An all-in-one mutable template risks silent status drift and contaminated framework upgrades.

## Required validation and reconsideration
Copy folder with no Git, edit upstream master without changing active run, migrate schema major with explicit boundary and ensure no writes outside agent-files.
