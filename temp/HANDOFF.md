# AOS-W Cross-Session Handoff — Prompt 17

Updated: 2026-10-20
Status: **Local real Git multi-process collaboration PASS 11/11; hosted GitHub CAS/LFS experimental run requires verification.** No other AI-model-provider handoff executed.
Repository: public digzoman/aos-workflows. Check actual HEAD before editing.

## Starting reads
1. `temp/OPERATING-RULES.md`, `temp/DESIGN-DECISIONS.md`, `temp/WORK-PLAN.md`, `temp/PROGRESS.md`.
2. `docs/testing/PROMPT-17-GIT-COLLABORATION.md`, `temp/tests/PROMPT-17-LOCAL-RESULTS.json`.
3. `tests/acceptance/test_git_cross_agent.py`, `tests/acceptance/git_collab_worker.py`, `tests/acceptance/hosted_github_claims.py`.
4. `tools/git/coordination.py`, `tools/git/README.md`, ADR-014.
5. `.github/workflows/aosw-p17-git-collaboration.yml` and actual GitHub Actions run logs/results/artifact, if available.
6. Prior Prompt 16 standalone acceptance and PRD T02/T03/T06 and FR-401–406/FR-501–506.

## Actual tested functionality
- Separate process workers in three independent clones of one **local bare Git remote**, same Git email, independent declared agent identities and separate task execution history.
- Multiple CAS tests: one winner per task, owner identity verified at worker-start, stale epochs rejected, no auto lease stealing, explicit reviewed stale-claim takeover under simulated expiry.
- Full local artifact submission/remote commit/readback, separate-process deterministic QC, new clone cold resume, checkpoint/event chain and accepted completion.
- Parallel branches: failure to refresh dirty/behind, explicit backup and human-style reconciliation, reviewed child evidence and merge into mock synthesis artifact.
- Divergent local commits preserved; remote partition fails closed; incomplete run migrated to a new Git bare remote and resumed; old claim refs not implicitly carried over.
- **Code fix:** `GitClient.release` now requires exact actor match alongside token and epoch to prevent accidental provenance misattribution. This is not identity authentication.

## Verification limits
- 11/11 local tests passed, no actual advertising research or provider effects.
- Worker subprocess names reflect **local-subprocess**, not fake Codex/Claude/Muse sessions. Reviewer is a separate deterministic process only.
- Hosted GitHub LFS/CAS probe separately scheduled in new Actions workflow, must be read back and classified accurately before removing ADR-014 provisional status.
- Git remains optional; standalone 0.6.0 unaffected. Claim ref CAS does not fence external API actions, authorize ad spend, or verify human roles.
- Prompt 15 marketing library is not yet on main; do not present 0.7.0 templates as published.

## Next
Inspect hosted Actions outcome, record PASS/BLOCKED/FAIL and any leaked claim ref cleanup; complete P15 publication; then stage Prompt 18 marketing pilot. For real cross-model platform coverage, acquire actual separate connected AI sessions and durable shared volume before marking T02 pass.


## Verified handoff amendment after latest main review, 2026-10-20

Read docs/release/V1-READINESS-2026-10-20.md, docs/release/V1-TRACEABILITY-2026-10-20.md, docs/release/V1X-BACKLOG.md and docs/testing/PROMPT-18-PILOT-PLAN.md before proceeding. Prompt 15 is now ON MAIN as version 0.7.0 and hosted 126 tests PASS, superseding older notes above. Prompt 17 hosted workflow success does NOT clear its CAS REVIEW_REQUIRED and LFS BLOCKED outcomes. Next actual work is to RUN Prompt 18 and save execution evidence, not to present its preparation as execution. Prompt 19 only prepared readiness documentation and release gate HOLD. Do not declare V1 complete until evidence gaps and owner approval are resolved. Do not modify live marketing accounts.


## Prompt 18 actual pilot execution amendment, 2026-10-20

Hosted synthetic file pilot executed successfully in run 39495294275, 77 events, no actual provider changes, no real research and no independent AI review. Read docs/testing/PROMPT-18-SYNTHETIC-PILOT-REPORT.md for what genuinely ran. Continue the REAL research/image/independent QC segment of P18, then re-audit stable V1. Do not mark T01 PASS or treat CI green as hosted Git CAS acceptance.


## Prompt 18 completed staged pilot handoff, 2026-10-20

Newest executable source-grounded P18 run is GitHub Actions 39498378421. Read docs/testing/PROMPT-18-END-TO-END-RESULTS.md and docs/testing/evidence/p18-grounded-39498378421/SUMMARY.json. Three separate child instances with 8 observed first-party seller sites, real 1080x1350 pilot PNG, independent deterministic subprocess QA, preserved rejected artifacts, 27 passing checks, 57 parent events, no external operations. Launch NOT_GRANTED. Pending full T01 are verified Ad Library ad cards, true independent AI review, verified product/price and official logo, real full compound workflow execution and any authorized provider staging. Preserve current evidence, update V1 readiness only when acceptance improves.
