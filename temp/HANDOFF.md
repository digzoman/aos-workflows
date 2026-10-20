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
