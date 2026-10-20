# AOS-W tracked historical workspace review

Inventory date 2026-10-20. The directory temp/ is tracked, public and historically important. All 60 current files are preserved. This is an index and a proposed future cleanup plan, not authorization to delete or rewrite the source.

## Promoted durable reference material

- temp/DESIGN-DECISIONS.md was copied without rewriting into docs/specs/requirements/USER-AGREED-BASELINE.md. This preserves the user-selected original requirements.
- temp/CONCEPT-NOTES-01B.md was copied into docs/specs/requirements/PROMPT-01B-REFINEMENTS.md. The original scheduling and skills decisions are preserved.
- temp/architecture/adrs/ADR-001 through ADR-008 were copied to docs/specs/adrs/. All remain explicitly PROPOSED, not accepted.
- temp/tests/PROMPT-09 through PROMPT-15 reports and P17 local results were copied to docs/testing/history/. Original historical results stay in temp.
- Durable product/design specifications already reside in docs/specs/prd, docs/specs/architecture and docs/specs/schemas. None is retroactively approved.
- Current acceptance evidence remains under docs/testing, full released preview documentation under docs/release and installation under docs/installation.

## Tracked archive inventory, no files deleted

- temp/CONCEPT-NOTES-01B.md
- temp/DESIGN-DECISIONS.md
- temp/HANDOFF.md
- temp/IMPLEMENTATION-HISTORY.md
- temp/OPEN-QUESTIONS.md
- temp/OPERATING-RULES.md
- temp/PROGRESS.md
- temp/README.md
- temp/RESEARCH-NOTES.md
- temp/WORK-PLAN.md
- temp/architecture/A-REP-COMPATIBILITY.md
- temp/architecture/ALTERNATIVES-COMPARISON.md
- temp/architecture/COORDINATION-AND-LOCKING.md
- temp/architecture/ENVIRONMENTS-AND-MINIMAL-CORE.md
- temp/architecture/LANGGRAPH-PATTERN-MAPPING.md
- temp/architecture/PRD-INPUTS-06.md
- temp/architecture/README.md
- temp/architecture/SKILLS-SCHEDULING-AND-SECURITY.md
- temp/architecture/SOURCES-06.md
- temp/architecture/adrs/ADR-001-portable-single-spec.md
- temp/architecture/adrs/ADR-002-state-and-checkpoints.md
- temp/architecture/adrs/ADR-003-optional-capabilities.md
- temp/architecture/adrs/ADR-004-git-coordination.md
- temp/architecture/adrs/ADR-005-skills-and-trust.md
- temp/architecture/adrs/ADR-006-scheduling.md
- temp/architecture/adrs/ADR-007-a-rep-boundary.md
- temp/architecture/adrs/ADR-008-authority-and-side-effects.md
- temp/architecture/adrs/README.md
- temp/research/EVIDENCE-GAPS.md
- temp/research/README.md
- temp/research/RESEARCH-EVIDENCE-QA.md
- temp/research/RESEARCH-WORKFLOW-MODEL.md
- temp/research/SOURCE-ADDENDUM-03.md
- temp/research/SOURCE-INDEX.md
- temp/research/VERTICAL-RESEARCH-LINEAGE.md
- temp/research/WORKFLOW-PATTERNS.md
- temp/research/campaign-operations/CRM-TRACKING-LESSONS.md
- temp/research/campaign-operations/FAILURES-AND-AUTHORITY.md
- temp/research/campaign-operations/PRD-RECOMMENDATIONS-05.md
- temp/research/campaign-operations/SOURCE-INDEX-05.md
- temp/research/campaign-operations/WORKFLOW-MODEL.md
- temp/research/candidate-templates/CATALOG.md
- temp/research/candidate-templates/COMPOSITION-EXAMPLES.md
- temp/research/candidate-templates/CREATIVE-CATALOG.md
- temp/research/candidate-templates/CREATIVE-COMPOSITION-EXAMPLES.md
- temp/research/candidate-templates/OPERATIONS-CATALOG.md
- temp/research/candidate-templates/OPERATIONS-COMPOSITIONS.md
- temp/research/creative-production/ASSET-LINEAGE-AND-SKILLS.md
- temp/research/creative-production/CREATIVE-PRODUCTION-MODEL.md
- temp/research/creative-production/FAILURES-REVISIONS-04.md
- temp/research/creative-production/QA-GATES-AND-APPROVALS.md
- temp/research/creative-production/SOURCE-INDEX-04.md
- temp/tests/PROMPT-09-STRUCTURAL-VALIDATION.md
- temp/tests/PROMPT-10-COMPOSITION-CONFORMANCE.md
- temp/tests/PROMPT-11-STATE-CONFORMANCE.md
- temp/tests/PROMPT-12-GOVERNANCE-CONFORMANCE.md
- temp/tests/PROMPT-13-GIT-COORDINATION.md
- temp/tests/PROMPT-14-DISTRIBUTION.md
- temp/tests/PROMPT-15-MARKETING-CONFORMANCE.md
- temp/tests/PROMPT-17-LOCAL-RESULTS.json

## Preserved historical groups

The source indexes and research models in temp/research cover historic Ampgent research, creative production and campaign workflows, with explicit limits on private-source access. temp/architecture captures alternatives, vendor research, reference provenance and the original proposed ADRs. temp/IMPLEMENTATION-HISTORY.md records the chronological implementation and corrections. temp/OPEN-QUESTIONS.md is historical and includes matters later partially resolved. temp/WORK-PLAN.md, temp/PROGRESS.md and temp/HANDOFF.md preserve active-session and prior-session state, including old claims subsequently superseded by newer dated addenda.

## Proposed cleanup, DO NOT PERFORM YET

1. Retain original source files until the owner reviews an exact file-by-file cleanup diff. Promoted copies are not a license to erase research or historical evidence.
2. Later, optionally group old temp notes under docs/history/snapshots by stage, preserving their bytes and Git history. Record original path, replacement link, SHA and reviewer approval for every migration.
3. Never mark original proposed ADR decisions ACCEPTED by moving them. Their governance status remains explicitly documented in docs/specs/adrs/README.md.
4. Use docs/release/V1-REQUIREMENTS-MATRIX.md and current test results for current truth, and retain dated old reports as historical evidence rather than altering them to match newer tests.
5. Perform human privacy and publication rights review before any additional sharing of research artifacts or copied private third-party content. Automated token scanning alone cannot certify source rights or absence of contextual customer details.

## Continuing the project

Read docs/release/V1-RELEASE-APPROVAL-PACKET.md and docs/release/V1-REQUIREMENTS-MATRIX.md, then temp/HANDOFF.md for session continuity, and the exact current commit/CI run for execution evidence. No confidential account actions or stable release approvals are granted by this archive migration.
