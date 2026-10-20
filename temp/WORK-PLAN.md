# AOS-W V1 Work Plan

Updated: 2026-10-20
Current phase: Prompt 14 distribution/optional helper implementation complete, release ZIP published and hosted smoke tests verified
Next phase: Prompt 15 sanitized Ampgent marketing reusable workflow templates
Implementation phases 09–13 were explicitly directed by the owner; live external operations remain separately approval-gated. Full V1 production/release approval is not implied.

## Research and design stages

- [x] Prompt 01. Create public repository and tracked decision and handoff workspace, without implementing the engine.
- [x] Prompt 01b. Add one-off versus scheduled recurring workflow triggering and per-template/per-instance just-in-time skills to the agreed design scope.
- [x] Prompt 02. Indexed accessible Ampgent conversations and inspected restricted research, creative, collaboration, staging, launch, and website artifacts, with sanitization and evidence limitations documented.
- [x] Prompt 03. Reconstructed 34-advertiser / 96-keyword queue workflow and 15-run vertical portfolio, scoring, source evidence, retry and independent QC; candidate research template specifications committed.
- [x] Prompt 04. Reconstructed B1–B9 creative strategy, copy, semantic gates, image generation and repair, exact logo placement, format variants, QA, Fred/Muse critique and owner selection; 14 candidate creative templates documented.
- [x] Prompt 05. Reconstructed Meta campaign/adset/ad architecture and targeted updates, provider state, paused staging, cross-system CRM/website/Pixel/CAPI gating, owner-controlled launch, rate limits, dedup/consent risks, and reporting; 15 candidate operations modules and composition designs documented.
- [x] Prompt 06. Inspected A Rep/Fred/Max source conventions; researched current LangGraph, Agent Skills, Git LFS locks, Git worktrees and version-checked Git refs; documented portable versus host-enforced behavior, environments, architecture alternatives and eight proposed ADRs. Git locking winner deferred to empirical tests.
- [ ] Prompt 07. **Draft and survey audit complete; owner approval PENDING.** Enhanced PRD at `docs/specs/prd/PRD.md`, supporting 16-question trace, decision register, acceptance matrix and approval checklist committed. Check this item only after explicit owner approval. No engine development yet.

## Implementation stages, conditional on PRD approval (Prompt 08 docs expressly requested; coding still conditional)

- [x] Prompt 08. Technical design completed as documentation: protected scaffold layout, 16 JSON Schema designs, graph eligibility/composition/revisions, lifecycle/event/checkpoint/recovery, manual protocol, and five new PROPOSED ADRs under docs/specs/. No engine built and pending PRD approval record not altered.
- [x] Prompt 09. Implemented self-contained `scaffold/aos-w/` with protected docs, 16 copied draft schemas, two master templates, bundled evidence skill, user-owned `agent-files`, inert practice instance and handoffs, optional structural validator/ZIP packager, documented manual startup/recovery and staged structural check results.
- [x] Prompt 10. Implemented 0.2.0 reusable template contracts, policy-constrained custom overlays, static/dynamic compound research workflows, optional local PyYAML composition/approval-gated instance helper, conditional/QA/permission-aware eligibility, revision impact planning, 11 passing conformance tests and sanitized multi-investigation fixtures. Automatic dispatch/event-safe revision application remain Prompt 11.
- [x] Prompt 11. Implemented optional local append-oriented SHA-256 event/state helper, immutable checkpoint anchors, attempt/retry records, pause/resume/cancel/fail, exact-scope provider operation identity/reconciliation, graph revision application, corrupted-tail and stale-snapshot recovery; updated 5 schema pairs and file-only manual protocol. 26 new + 11 prior tests PASS. No provider calls, automatic scheduler or distributed mutual exclusion.
- [x] Prompt 12. Implemented four-field agent provenance, advisory claims, configurable QC, expiry/revocation approvals and handoffs. 38 new tests passed. Remote trusted skill loading remains future work.
- [x] Prompt 13. Implemented optional Git sync, explicit old-SHA CAS task claims, Git LFS client prototype, fail-closed offline modes, and 15 local Git conformance tests (90 total); provisional preference for CAS, hosted GitHub/LFS server tests still pending.
- [x] Prompt 14. Authored optional clean ZIP builder/installer/upgrade, quick-start initialization/status helper, manifest integrity and archive safety, portable docs and GitHub Actions standalone ZIP workflow. 18 new tests + 90 prior = 108 local PASS. Verify hosted artifact and preview release status separately.
- [ ] Prompt 15. Sanitized Ampgent marketing template library.

## Validation and release stages

- [ ] Prompt 16. Standalone offline and single-agent tests, including manually launched one-off/recurring-template instances and bundled/local skills.
- [ ] Prompt 17. Git and cross-agent collaboration tests, including scheduled occurrence identity and safe shared skill references where supported.
- [ ] Prompt 18. Staged end-to-end marketing workflow pilot, no live publishing without new authorization.
- [ ] Prompt 19. Requirements audit, release readiness and human review.

## Definition of done for a stage

Deliverables committed with actual SHA, evidence read back or tests reported honestly, `PROGRESS.md` and `HANDOFF.md` updated, unresolved questions explicitly registered. Do not mark tests as passed without executions.
