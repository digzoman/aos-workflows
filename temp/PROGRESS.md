# AOS-W Development Progress

Date: 2026-10-20
Phase: **Prompt 09 initial portable scaffold IMPLEMENTED; staged structural validation PASSED.**
Next: Prompt 10 template resolution, compound graphs, conditional eligibility and dynamic instance behavior.

## Previous work

- Prompts 01–01b: user requirements, 16 survey answers, one-off/recurrence and step-local skills, public repo.
- Prompts 02–05: sanitized evidence from Ampgent advertiser research, B1–B9 creative production, Meta/website/CRM staging, launch and monitoring.
- Prompt 06: architectural comparisons and proposed ADRs 001–008.
- Prompt 07: comprehensive PRD with user requirements trace, acceptance matrix and unresolved decisions.
- Prompt 08: 16 draft JSON Schemas, detailed architecture, graph/revision/state/recovery/manual agent protocol, proposed ADRs 009–013.

## Prompt 09 working foundation

- Download/copy `scaffold/aos-w/` alone to a persistent local/cloud directory. README, PROTOCOL, VERSION and five bundled detailed specifications plus **16 copied draft JSON Schemas** are installed; no external docs required for manual reading.
- Master templates `research-starter` (3 nodes, manual, local-only, bundled evidence-handling SKILL) and `periodic-review-example` (2 nodes, disabled weekly trigger, no automatic wake).
- Writable `agent-files/` includes config with Git/scheduler/provider unavailable by default, custom templates, instances, indexes, cache, coordination notes.
- **Inert practice instance** `agent-files/instances/demo-local-research/`: pinned version and content blob, immutable g0001 snapshot, run-001 with run_created and initial checkpoint events, derived state READY only for define-scope, checkpoint/handoff, task attempts and audit/evidence/review/approval directories. This is a structural initial state **not performed work**.
- Protected standard content versus writable user data clearly documented; safe manual upgrade must preserve agent-files without overwriting it.
- Optional nonrequired maintainer scripts: `scripts/validate-scaffold.mjs` (Node.js structural checks) and `scripts/package-scaffold.sh` (zip helper). These were authored but **not executed in this environment**.
- Updated root/scaffold/example documentation for directly downloadable repository-folder layout and honest capability limits.

## Verification actually performed

Repository staged-tree reads confirmed:
1. Required runtime/config/sample paths exist; 16 schema copies match original design blob SHAs.
2. Master research template, saved snapshot and current g0001 graph match the exact same Git blob SHA, and template-lock digest matches.
3. JSON sample records parse, events seq 1–2 align with state/checkpoint/handoff at seq 2; run state CREATED, no attempts completed or grants claimed.
4. The two master templates passed simple static node/dependency resolution and no detected cycle.
5. `temp/tests/PROMPT-09-STRUCTURAL-VALIDATION.md` distinguishes PASS from NOT_RUN tests.

## Still NOT implemented or demonstrated

- Full JSON Schema/YAML validation through an actual parser/validator in the installed distribution or even the optional Node script's execution.
- A real end-to-end standalone run resumed across separate AI sessions.
- Automated graph executor, durable crash-atomic filesystem writes, conditional/dynamic execution runtime, parallel scheduling, verified Git CAS/LFS locking, provider integration, external publishing, Meta/CRM actions.
- Prebuilt ZIP uploaded as release; installation instructions use repository ZIP (copy only folder) or optional packager script.
- All 16 V1 acceptance tests remain NOT RUN.

## Owner authorization and limits

The user explicitly requested Prompt 09 **implementation using the approved PRD**, which constitutes scoped authorization for this scaffold step. The prior dedicated PRD approval form did not separately record a broad decision; proposed ADRs are not all accepted by inference. No permission for live marketing operations or spending was given.

Next Prompt 10 should implement and test actual template inheritance/composition/graph step eligibility while retaining the zero-mandatory-runtime manual protocol. **Do not oversell the 0.1.0 scaffold as a working execution engine.**
