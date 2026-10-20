# AOS-W Cross-Session Handoff

Updated: 2026-10-20
Completed: Prompt 08 technical architecture and file specifications (documentation only)
Repository: digzoman/aos-workflows, public main. **Verify current HEAD before any edit.**

## Required next-session reads

1. `temp/OPERATING-RULES.md` and `temp/DESIGN-DECISIONS.md`
2. `temp/CONCEPT-NOTES-01B.md`
3. `docs/specs/prd/PRD.md` and `docs/specs/prd/APPROVAL-REVIEW.md`
4. `docs/specs/architecture/README.md`
5. `docs/specs/architecture/ARCHITECTURE.md`
6. `docs/specs/architecture/FILE-SPECIFICATION.md`
7. `docs/specs/architecture/SCHEMA-CONTRACTS.md`
8. `docs/specs/architecture/GRAPH-AND-REVISIONS.md`
9. `docs/specs/architecture/EXECUTION-STATE.md`
10. `docs/specs/architecture/MANUAL-AGENT-PROTOCOL.md`
11. `docs/specs/architecture/OPEN-DECISIONS.md`
12. `docs/specs/schemas/README.md` and 16 draft JSON schemas
13. `docs/specs/adrs/README.md`, proposed ADR-009 through ADR-013, plus `temp/architecture/adrs/` 001–008

## Architectural contract

- Independent downloaded `scaffold/aos-w/` is read-mostly except `agent-files/`.
- Instance holds pinned resolved template snapshot and immutable graph revisions; master updates never modify active runs without an authorized revision event.
- Graph uses stable node IDs, explicit needs/conditions/join/fan-out with three-valued UNKNOWN; every READY task requires source, skills, permission and (if shared) verified claim.
- Validated chronological per-run events are audit authority, `state.json` derived snapshot, checkpoints immutable recovery anchors. Torn/ambiguous effects require honest reconciliation.
- QC binds exact rubric/artifact set/version; separate external action approval. Agent identity `[Agent | Platform | Role | Instance]` records producer only.
- Default manual one-off/standalone one-writer; recurring schedules stored as metadata unless optional host wake; Git mirror optional. Exclusive multi-agent claims must use a **tested** backend, not advisory file or worktree.
- Per-step skills can be bundled or pinned installed/remote; trust review, conflict fail-closed and no authorization escalation.

## Authorization and next action

The PRD approval checklist still says PENDING and no subsequent explicit recorded decision was found. The user specifically directed Prompt 08, authorizing this **design document work**; this did **not** automatically approve the PRD/ADRs or live actions. Before Prompt 09 implementation, obtain explicit owner approval of PRD/spec or direct authorization addressing the approval checkpoint. Record any owner decision and update ADR status only for specifically approved records.

Prompt 09 should build the actual protected scaffold under `scaffold/aos-w/` only after authority is established. It must not introduce mandatory Python, Git, MCP, database, always-on scheduler or cloud service. No live Meta/HighLevel/website changes without separate authorization.

## Evidence/limitations

- Sixteen schemas were authored and checked for valid JSON and relative reference links; actual validator execution and cross-model handoff tests remain future work.
- No runtime behavior, atomic claim or crash-safe file write demonstrated.
- References to Ampgent/Fred/Max are summarized/sanitized only; no private source copied.
- Update this handoff, progress and history and commit with verified SHA at each future stage.
