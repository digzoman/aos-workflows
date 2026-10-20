# AOS-W Cross-Session Handoff

Date: 2026-10-20
Completed: **Prompt 09 initial portable scaffold**
Repository: `digzoman/aos-workflows`, public `main`. **Check latest HEAD before any next modifications.**

## First reads for next session

1. `temp/OPERATING-RULES.md`
2. `temp/DESIGN-DECISIONS.md`, `temp/CONCEPT-NOTES-01B.md`
3. `temp/WORK-PLAN.md`, `temp/PROGRESS.md`
4. `docs/specs/prd/PRD.md`, `docs/specs/architecture/README.md`
5. `scaffold/aos-w/README.md`, `scaffold/aos-w/PROTOCOL.md`, `scaffold/aos-w/VERSION.json`
6. `scaffold/aos-w/agent-files/README.md` and `scaffold/aos-w/agent-files/instances/README.md`
7. `scaffold/aos-w/references/START-A-RUN.md`, `INSTANCE-LAYOUT.md`, `UPGRADE-AND-PORTABILITY.md`
8. `scaffold/aos-w/templates/research-starter/template.yaml`, `periodic-review-example/template.yaml`
9. `scaffold/aos-w/agent-files/instances/demo-local-research/runs/run-001/handoff.md`
10. `temp/tests/PROMPT-09-STRUCTURAL-VALIDATION.md`, `docs/specs/schemas/README.md`

## Exact current implementation

- Protected/read-mostly `scaffold/aos-w` framework docs/templates/skills/specs and `VERSION.json` tagged 0.1.0.
- Sixteen JSON Schema drafts copied byte-for-byte into installed `spec/schemas/`.
- Manual low-risk research-starter template with 3 valid graph nodes and bundled step-local skill; optional periodic-review template with disabled schedule declaration.
- Only `agent-files/` is normal writable root; subdirectories for config, custom template, instances/runs, evidence/artifacts, attempts/history, claims, reviews, approvals and indexes/cache/coordination are physically represented by user-owned config and **synthetic practice instance**.
- Practice `demo-local-research/run-001` has **created, not executed** state, 2 init events, no completed tasks/real research/authority, matching g0001 template pin and a safe next task `define-scope`.
- No Git requirement for a downloaded folder. Git/scheduler/provider capabilities default disabled/unverified and live remote actions require separately established permission.

## Tests and verification limits

- Staged tree structural existence, Git blob pinning, schema-source copy identity, demo run event/state/checkpoint/handoff coherence, and both built-in graph shape checks PASSED. See test report.
- Node validator and shell packager are **optional and authored but NOT RUN**; full YAML parser/JSON Schema validation NOT RUN, no real cross-platform handoff, no working auto engine/Git claims/provider API integration.
- No actual scaffold-only ZIP release asset created by this ChatGPT tool session; using GitHub's repo ZIP plus copying the folder is documented.

## Next assignment, Prompt 10

Implement template resolution/inheritance, compound and conditional workflow semantics, dependency-aware eligibility, dynamic child proposals and merge logic according to current technical design. Keep manually readable portable specification and no mandatory Git/runtime; if adding optional tools, verify they are not a dependency. Exercise new workflow behavior with real local fixture files and explicitly label MOCKED versus LIVE.

Avoid changes to live Meta, GHL, websites or real customer systems. Agent claims remain advisory unless a tested adapter is introduced. Update plan/progress/handoff/history and commit actual artifacts, not unverified reports.

## Scoped approval

User explicitly directed Prompt 09 implementation under the described approved PRD, recorded as authorization for **this scaffold**. Earlier form fields were pending, and no blanket ADR acceptance or provider publishing permissions are claimed.
