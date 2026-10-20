# AOS-W Version 1 release readiness decision packet

Presented October 20, 2026. RECOMMENDATION: DO NOT APPROVE STABLE V1 AT THIS STAGE.

## What is ready now

- Public development repo digzoman/aos-workflows, with standalone 0.7.0 preview downloadable and independently verified.
- 21 reusable marketing modules plus one compound template, manual file-first protocol, optional graph/state/governance/Git helper code, historical schemas and sanitized examples.
- 126 hosted tests passed and 13/13 local practical offline scenarios passed again on the real 0.7.0 ZIP.
- Real local file event persistence, retries, checkpoints, quality-control corrections, graph revisions, Git migration and nonpublishing marketing stage demonstration.
- A reproducible current-and-historical Git secret signature scanner. It passed high-confidence automated checks on its tested commit, though human privacy/rights audit remains outstanding.
- Reusable source traceability and immutable historical preservation for the tracked temp folder.
- Existing published preview artifact. No new stable v1.0.0 version or release was declared.

## Required original acceptance

T01 Ampgent complete real-world workflow, PARTIAL.
T02 independent agent/model platform handoff, NOT DEMONSTRATED.
T03 true exclusive collision control in hosted/shared mode, PARTIAL, hosted CAS REVIEW_REQUIRED, LFS BLOCKED.
T04 independent AI review failure/correction, PARTIAL, separate deterministic process only.
T05 revision preserves previous completed work, PASS local with mocked approval.
T06 move running Git work to second repo/remote, PASS local with limits.

All six were user-selected as mandatory success tests. Do not collapse them into a simple implementation checklist.

## Decisions requiring explicit owner approval or change

1. Whether to approve PRD 1.0-rc1 as written or approve a specific narrowed staged/manual first release. The PRD approval record is still PENDING, although scoped implementation instructions were given.
2. Whether T01 through T06 remain strict stable V1 entry criteria. Any deferral to V1.x must be a clearly documented change to original acceptance requirements, not inferred by the agent.
3. Whether Git ref CAS remains experimental-only, pending hosted test and Git LFS verification; no claim of production coordination without evidence.
4. Whether persistent cloud lifecycle testing, independent AI/human QA, schedule occurrence dedup and real Meta staging are in v1.0.0 scope or explicitly deferred. Do not silently alter existing requirements.
5. Open-source license choice. A public repository currently contains no selected license.
6. Privacy/source rights and external provider permissions, including retained historical source references and public research/creative examples. Pattern scanner PASS is not human signoff.
7. Whether the documented cross-instance join implementation gap is a blocking V1 defect. Recommended P0 since downstream work can otherwise appear ready ahead of accepted child QC.
8. Specific final release version/tag, change notes and authorization. AOS-W release approval is NOT authorization to publish marketing campaigns or spend.

## Current formal release state

Decision: PENDING OWNER REVIEW.
Recommended classification: RELEASE CANDIDATE REVIEW PACKAGE ONLY, v0.7.0 public preview remains current.
Stable Version 1 complete: NO.
New stable tag: NONE.
License: UNDECIDED.
Production marketing integrations: NOT AUTHORIZED.

## Review options

APPROVE WITH CHANGES. Specify exact deferred requirements, desired stable v1 scope, remaining hard blockers, license and ADR decisions. Then generate a revised PRD, acceptance gates and new reviewed release candidate.

REQUEST COMPLETION. Keep all six mandatory criteria and instruct testing of the missing real AI/cloud/Git/provider evidence before approving stable V1.

REJECT/DEFER. Preserve current v0.7.0 portable preview and continue V1.x development without changing formal PRD approval.

NO IMPLICIT APPROVAL. User should state the selected outcome explicitly. Any formal signoff must include date, PRD version, scope and remaining accepted risks.

## Evidence entrypoints

- docs/release/V1-REQUIREMENTS-MATRIX.md
- docs/release/V1-LIMITATIONS-AND-RISKS.md
- docs/release/V1-PROPOSED-RELEASE-NOTES.md
- docs/specs/prd/APPROVAL-REVIEW.md
- docs/specs/adrs/README.md
- docs/history/TEMP-ARCHIVE-INDEX.md
- docs/installation/QUICKSTART.md
- GitHub Actions audit 39499859355, marketing pilot 39498378421, collaboration 39428039269.
