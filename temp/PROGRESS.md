# AOS-W Development Progress

Date: 2026-10-20
Phase: **Prompt 10 reusable workflow composition implemented and locally tested**
Status: FILE-FIRST MANUAL STANDARD + OPTIONAL COMPOSITION HELPER. NOT A BACKGROUND ENGINE.
Next: Prompt 11 durable execution state, checkpoints, retries, recovery and interrupted-work semantics.

## Prior phases
- Prompts 01–08: requirements, historical Ampgent evidence, A Rep/LangGraph/Git research, PRD, technical specifications and proposed ADRs.
- Prompt 09: installable standalone 0.1.0 scaffold with protected master definitions, user-owned agent-files, 16 schema copies, two starter templates, practice run and optional structural helpers.

## What Prompt 10 actually added
- Updated standardized scaffold version to **0.2.0**. Original synthetic 0.1.0 `demo-local-research` run remains pinned to its previous immutable source/graph (no silent template upgrade).
- Master `competitor-investigation` template with five tasks, independent `evidence-qc`, explicit input/output/quality/dependency/contract fields.
- Master `research-portfolio-planner` with define-plan, owner approval, deterministic child proposals and all-reviewed synthesis gate.
- Master `research-portfolio-compound` showing three version-and-SHA256-pinned static children, scoped bindings and all-accepted join.
- Existing `research-starter` and `periodic-review-example` master definitions upgraded to explicit 0.2.0 contracts without changing existing run history.
- Sanitized `agent-files/custom-templates/competitor-investigation-ontario/` overlay with exact base source SHA and permission-constrained node patch.
- Portable human/agent `references/COMPOSITION.md`, template READMEs and updated protocol.
- **Optional** `tools/composition/composition.py` + `cli.py`: validate acyclic graph contracts, resolve bounded policy overlays/parameters, classify ready/waiting/blocked/failed/completed work, evaluate three-valued conditions, propose stable child IDs, locally create approved children, merge only reviewed children with explicit synthesis authorization, analyze authorized graph revision impact.
- Expanded both authoritative and installed `common.schema.json` node definitions with `inputs`, `quality`, `contract`, `extensions`; added FAILED status in both state schema copies, preserving backwards-compatible optional node fields.
- Conformance fixtures in `examples/conformance/planning/` for three buyer verticals, simulated approval and review, proposals, context and revised graph.

## Actual validation performed
- **11 unittest methods PASS** with PyYAML in local development runtime.
- Optional helper CLI smoke tests of validate, classify, propose, materialize, merge, and revision-impact PASS against synthetic fixtures.
- Verified local test source/blob identity against staged GitHub tree SHA for key tool, test, fixture and template files before commit.
- Scoped simulated approval creates three CREATED child instance folders under a temporary `agent-files`; no real research, Meta, CRM, messages, website or spend.
- Report: `temp/tests/PROMPT-10-COMPOSITION-CONFORMANCE.md`.

## Deliberate limits
- No mandatory Python/PyYAML to use the **downloadable** file-and-instructions framework. Helper is development/host-optional.
- No network provider calls, automatic background dispatch/schedule, authenticated approvals, truly exclusive concurrent claims, or crash-atomic multi-child transaction.
- Graph revisions: impact and safety check **implemented**, event-backed application not implemented yet. Prompt 11 handles state/retries/recovery.
- JSON Schema validator-library invocation on complete remote schema bundle not claimed; node shape validation is by the tested helper.
- User's explicitly scoped Prompt 10 instruction authorizes these project files, **not** production account changes or blanket ADR acceptance.
- Full V1 T01–T16 cross-platform/production/scheduling acceptance remains future work.

## Next step
Prompt 11 implements persistent event/state/checkpoint reconciliation, bounded retry mechanics, safe interrupted work and explicit revision transactions, staying compatible with manual single-agent mode and preserving only `agent-files/` normal writes.
