# AOS-W Cross-Session Handoff

Date: 2026-10-20
Completed: **Prompt 10 reusable templates, compound workflow conventions, optional local helper and conformance tests**
Repository: `digzoman/aos-workflows`, public main. **Check HEAD and project rules before the next change.**

## Priority reads for Prompt 11
1. `temp/OPERATING-RULES.md`, `temp/DESIGN-DECISIONS.md`, `temp/CONCEPT-NOTES-01B.md`
2. `temp/WORK-PLAN.md`, `temp/PROGRESS.md`, this handoff
3. `scaffold/aos-w/README.md`, `PROTOCOL.md`, `VERSION.json`
4. `scaffold/aos-w/references/COMPOSITION.md`, `START-A-RUN.md`
5. `tools/composition/composition.py`, `cli.py`, `README.md`
6. `tests/test_composition.py`, `temp/tests/PROMPT-10-COMPOSITION-CONFORMANCE.md`
7. `scaffold/aos-w/templates/competitor-investigation/template.yaml`
8. `scaffold/aos-w/templates/research-portfolio-planner/template.yaml`
9. `scaffold/aos-w/templates/research-portfolio-compound/template.yaml`
10. `examples/conformance/planning/` synthetic planning/approval/review fixtures
11. `docs/specs/architecture/EXECUTION-STATE.md`, `GRAPH-AND-REVISIONS.md`, `MANUAL-AGENT-PROTOCOL.md`

## Implemented contract
- Master/custom reusable YAML templates; custom overlay pinned to exact base version + SHA256, cannot expand owner actions/parallel allowance or drop inherited QC.
- New nodes explicitly declare inputs, outputs, expected quality gates, stable ID, needs and done_when contract. New 0.2 masters validate; old synthetic 0.1 practice instance remains **pinned** to old snapshot.
- Approved plan produces deterministic proposed child IDs `plan_id-slug-revision`. A **separate exact-scope simulated approval** was exercised to locally create three independent run directories in tests, each CREATED and not yet executed.
- Readiness categories: ready/waiting/blocked/failed/completed, preserving UNKNOWN conditions; explicit all-reviewed current children and separate approval before synthesis. Parallel branches are data-level independent, not automatically dispatched.
- Proposed material revision impact preserves unaffected completed work, requires separate authorization for changes to executed/sensitive nodes. No durable graph-revision application/actual events yet.
- Conformance: 11 local unit tests passed, CLI smoke tests passed, source SHA identities matched staged repository content.

## Next Prompt 11 tasks
- Formalize durable event append and materialized state with consistency and torn-write handling, checkpoint recovery, bounded retries and provider ambiguity tracking.
- Implement protected graph-revision **application** without overwriting historical events/accepted artifacts, using the Prompt 10 revision impact reports and explicit version-scoped approval.
- Address interrupted child instantiation or partial file-write reconciliation. Do not claim atomicity in plain-file mode.
- Add negative tests for retry duplication, stale gate revisions, corrupted JSONL and crash recovery. Preserve 0.1 pinned fixtures and user-owned directories.
- Keep provider state authoritative; no live Meta/GHL operations unless separately authorized.

## Guardrails
No mandatory Git, Python, database, MCP, cloud, dashboard or scheduler for file-native standalone users. Optional PyYAML requires explicit host choice. No tested Git LFS/CAS concurrency, no real unattended tasks, no production ad publishing. Programmatic helper writes only to user-owned `agent-files`; permissions in fixture are MOCKED and not authenticated authority.
