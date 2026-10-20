# AOS-W Cross-Session Handoff — Prompt 16

Updated: 2026-10-20
Current stage: **Standalone/offline practical local acceptance PASSED 13/13; cloud persistent filesystem NOT RUN.** Formal Version 1 acceptance incomplete.
Repo: public digzoman/aos-workflows main. Verify current HEAD and Actions run before working.

## Required reads
1. `temp/OPERATING-RULES.md`, `temp/DESIGN-DECISIONS.md`, `temp/WORK-PLAN.md` and this handoff.
2. `docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md` and `tests/acceptance/README.md`.
3. `tests/acceptance/run_standalone_acceptance.py`, `resume_agent.py`, `evidence/acceptance-results.json` and selected real event journals.
4. `scaffold/aos-w/README.md`, `PROTOCOL.md`, `references/STATE-AND-RECOVERY.md`, `tools/state/state.py`, `scripts/aosw-ops.py`.
5. `.github/workflows/aosw-portable.yml` for the hosted local-filesystem ZIP acceptance job.
6. Prompt 15 design files must be checked for an actual commit; as of Prompt 16 start they were uncommitted.

## Confirmed local capabilities
- Verified release v0.6.0 ZIP SHA-256 `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`, actual extracted installation with no Git.
- Three research steps genuinely executed on a **fictional offline fixture**. Scope and evidence hashes verified; one incomplete running attempt deliberately interrupted and resumed from saved event/handoff/graph/skill by a new independent OS process.
- Completed run has a verified event chain, QC submission/PASS, checkpoint and saved handoff. Legacy master and installed framework 54 protected files unchanged.
- A user custom template was created under agent-files, initialized and executed; test also covered bounded failure/retry, QC rejection/correction, approved graph revision with preserved history, pause/resume/cancel, corrupt-tail recovery and ambiguous-effect dedup.
- 13 acceptance cases PASS; cloud persistent filesystem case explicitly NOT RUN; real cross-platform AI harness/remote provider actions not tested.

## Test harness correction
The first test wrongly expected a skill-bound node in the automatic eligible list. The implementation correctly demands an explicit context/skill check. Tests were fixed and rerun; no production framework bug established.

## Next steps
- GitHub Actions run 39423403366 **completed SUCCESS**, with 108 regressions and 13 standalone acceptance cases PASS; artifact ID 12264942466 holds acceptance report/results/interruption/cold-resume evidence. Persistent cloud FS test still NOT RUN.
- Finish previously prepared but unpublished Prompt 15 marketing templates. Do not conflate the GitHub v0.6.0 release with an unreleased v0.7.0.
- Future separate cloud-host persisted install, actual other-agent platform cold resume, scheduled occurrence tests and independent approval enforcement are pending.
- No live Meta/HighLevel/site operations, and mock approvals cannot be used for them.
