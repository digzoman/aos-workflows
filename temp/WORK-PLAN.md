# AOS-W V1 Work Plan

Updated: 2026-10-20
Current phase: Prompt 03, competitor Meta research reverse engineering completed
Next phase: Prompt 04, ad creative production workflow research
No workflow engine implementation authorized before PRD approval.

## Research and design stages

- [x] Prompt 01. Create public repository and tracked decision and handoff workspace, without implementing the engine.
- [x] Prompt 01b. Add one-off versus scheduled recurring workflow triggering and per-template/per-instance just-in-time skills to the agreed design scope.
- [x] Prompt 02. Indexed accessible Ampgent conversations and inspected restricted research, creative, collaboration, staging, launch, and website artifacts, with sanitization and evidence limitations documented.
- [x] Prompt 03. Reconstructed 34-advertiser / 96-keyword queue workflow and 15-run vertical portfolio, scoring, source evidence, retry and independent QC; candidate research template specifications committed.
- [ ] Prompt 04. Reverse engineer ad copy and creative/image production and revision loops.
- [ ] Prompt 05. Reverse engineer Meta campaign setup, tracking, CRM, prelaunch QA, activation, and optimization.
- [ ] Prompt 06. Review A Rep, LangGraph, Agent Skills, locking and portability tradeoffs; include scheduling backend interfaces, due-trigger behavior, skill packaging and skill resolution/trust.
- [ ] Prompt 07. Produce enhanced PRD at `docs/specs/prd/PRD.md`, explicitly covering non-repeating vs recurring schedules, on-demand launch, missed/overlapping schedules, optional schedule triggering, template/instance skill bundles, lazy skill resolution, and remote skill security; obtain explicit human review and approval.

## Implementation stages, conditional on PRD approval

- [ ] Prompt 08. Formal technical architecture and schemas, including trigger/schedule and skill reference/bundling definitions.
- [ ] Prompt 09. Build downloadable scaffold, protected framework files, writable `agent-files`.
- [ ] Prompt 10. Template reuse, composition, dependencies, dynamic runs, non-repeating/scheduled trigger metadata, and ad hoc launch overrides.
- [ ] Prompt 11. State, checkpoints, retries, recovery, and interruption semantics.
- [ ] Prompt 12. Agent provenance, autonomy, permissions, QC, handoffs, and just-in-time skill loading/resolution without implicit authority expansion.
- [ ] Prompt 13. Optional Git syncing; compare LFS and atomic Git coordination.
- [ ] Prompt 14. Optional helper tooling and independent download package.
- [ ] Prompt 15. Sanitized Ampgent marketing template library.

## Validation and release stages

- [ ] Prompt 16. Standalone offline and single-agent tests, including manually launched one-off/recurring-template instances and bundled/local skills.
- [ ] Prompt 17. Git and cross-agent collaboration tests, including scheduled occurrence identity and safe shared skill references where supported.
- [ ] Prompt 18. Staged end-to-end marketing workflow pilot, no live publishing without new authorization.
- [ ] Prompt 19. Requirements audit, release readiness and human review.

## Definition of done for a stage

Deliverables committed with actual SHA, evidence read back or tests reported honestly, `PROGRESS.md` and `HANDOFF.md` updated, unresolved questions explicitly registered. Do not mark tests as passed without executions.
