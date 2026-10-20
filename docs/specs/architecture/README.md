# AOS-W V1 technical specification package

**Status: TECHNICAL DESIGN DRAFT, not a working implementation.** Prepared October 20, 2026 for Prompt 08. PRD 1.0-rc1 remains recorded as DRAFT/PENDING in `docs/specs/prd/APPROVAL-REVIEW.md`. The user's Prompt 08 request authorizes this documentation work, **not** engine implementation or production actions. No intervening owner change requests were evidenced at inspection.

Normative reading order:

1. [ARCHITECTURE.md](ARCHITECTURE.md), system responsibilities, modes, constraints, authority.
2. [FILE-SPECIFICATION.md](FILE-SPECIFICATION.md), full protected/read-only and writable runtime layout, compatibility and version pinning.
3. [SCHEMA-CONTRACTS.md](SCHEMA-CONTRACTS.md), schema catalog, normative cross-file invariants and record examples.
4. [GRAPH-AND-REVISIONS.md](GRAPH-AND-REVISIONS.md), dependency semantics, eligibility, fan-out, joins and safe evolution.
5. [EXECUTION-STATE.md](EXECUTION-STATE.md), lifecycle, attempt ledger, checkpoint, recovery and gate transition rules.
6. [MANUAL-AGENT-PROTOCOL.md](MANUAL-AGENT-PROTOCOL.md), no-scripts procedure, cold starts, handoffs and optional adapters.
7. [OPEN-DECISIONS.md](OPEN-DECISIONS.md), explicitly provisional decisions, tests and deferred conflicts.
8. [../schemas/README.md](../schemas/README.md), actual versioned draft JSON Schema documents, intended for YAML/JSON records.
9. [../adrs/README.md](../adrs/README.md), Prompt 08 new PROPOSED ADRs 009–013, without auto-accepting Prompt 06 ADRs.

**Normative vocabulary:** MUST and MUST NOT denote design requirements proposed for V1; SHOULD preferred compatible behavior; MAY optional. This is an implementation-ready *specification*, not a claim any behavior is already enforced. **Host-enforced** guarantees must be separately demonstrated; plain-file operation is cooperative, single-writer and manual.

**References:** approved user requirements recorded in `temp/DESIGN-DECISIONS.md` including Prompt 01b, detailed draft PRD `docs/specs/prd/PRD.md`, research `temp/research/`, technical comparison `temp/architecture/`.

Change discipline: update schema examples and references together; never silently modify the user-approved baseline or give draft ADRs ACCEPTED status without explicit owner decision. Keep `agent-files/` only as the *future* install runtime mutable root.
