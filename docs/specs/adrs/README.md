# Architecture Decision Records under docs/specs

**Prompt 08 ADRs are PROPOSED, not adopted**. Original Prompt 06 ADR-001 through ADR-008 remain in `temp/architecture/adrs/`, also PROPOSED unless separately approved. This collection records concrete design choices for further owner review and testing, not implementation or external-action authority.

- [ADR-009](ADR-009-file-layout-and-compatibility.md), protected install root and pinned instance layout.
- [ADR-010](ADR-010-event-ledger-and-recovery.md), canonical validated event history and derived snapshots.
- [ADR-011](ADR-011-graph-and-policy-merge.md), DAG, conditional UNKNOWN, dynamic children and protected inheritance.
- [ADR-012](ADR-012-shared-task-claims.md), advisory local mode and optional empirically verified distributed claims.
- [ADR-013](ADR-013-skill-schedule-permission.md), just-in-time skill and recurring trigger separation from permissions.

Pending owner authorization is **not** satisfied by this repository commit. Git LFS vs atomic Git claim design is intentionally unresolved until Prompts 13/17 tests.

- [ADR-014](ADR-014-git-cas-provisional-selection.md), provisional preference for explicit expected-SHA Git ref CAS based on real *local* bare-Git tests; no real hosted GitHub/LFS server comparison yet.
