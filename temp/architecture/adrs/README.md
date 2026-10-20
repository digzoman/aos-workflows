# Draft architecture decision records

These are **initial proposals**, not a record of owner approval. Do not mark ACCEPTED or begin implementing from them before Prompt 07 enhanced PRD review. Each ADR links to primary research in [../SOURCES-06.md](../SOURCES-06.md), [../COORDINATION-AND-LOCKING.md](../COORDINATION-AND-LOCKING.md), and the earlier marketing workflow studies.

- [ADR-001](ADR-001-portable-single-spec.md) portable file-first graph, no mandatory runtime.
- [ADR-002](ADR-002-state-and-checkpoints.md) durable per-run state, event trail and deterministic recovery.
- [ADR-003](ADR-003-optional-capabilities.md) orthogonal local/cloud, standalone/sync, shared coordination.
- [ADR-004](ADR-004-git-coordination.md) trial CAS Git claims versus LFS, no winner until tests.
- [ADR-005](ADR-005-skills-and-trust.md) step-local Agent Skills and trust rules.
- [ADR-006](ADR-006-scheduling.md) manual default, optional recurring triggers, host wake only.
- [ADR-007](ADR-007-a-rep-boundary.md) integrate with A Rep but avoid second PRIMARY and plan authority.
- [ADR-008](ADR-008-authority-and-side-effects.md) explicit approvals, QC binding, compensation and provider truth.

Decision record lifecycle: PROPOSED -> user REVIEWED -> ACCEPTED/REJECTED/DEFERRED after explicit approval. Any alternative should record evidence, risks and tests, not overwrite the first decision's history.
