# AOS-W Project Progress

Updated: 2026-10-20
Current: **Prompt 17 local Git collaboration acceptance passed 11/11. Hosted GitHub CAS/LFS probe pending separate readback.**
Prior: Prompt 16 v0.6 local standalone/offline practical 13 PASS, 0 FAIL, independent persistent cloud FS NOT RUN; GitHub CI 108 previous regressions + 13 acceptance PASS.

## Baseline truth

- Main at test start `d7f59cdd30959b2f2cee8a082c5545fe1d7fe82d` (AOS-W 0.6.0). Earlier Prompt 15 marketing library remained prepared but **uncommitted**, so cannot count it as released tested material.
- PRD T02/T03/T06 and FR-401–406/FR-501–506/NFR-07/08 defined acceptance targets; full V1 release approval still unresolved.

## Prompt 17 executed

- **11 PASS / 0 FAIL** in local bare-Git remote experiment with two separately cloned task workers, third reviewer clone and fourth fresh subprocess handoff reader.
- Both independent worker processes discovered actual eligible workflow tasks and read/wrote real local AOS-W `RunStore` event history, output artifacts, reviews, checkpoint and handoff records.
- Both Git clones use same Git username/email while AOS-W events, claim ref records and commit trailers identify distinct actors `[Agent | Platform | Role | Instance]`.
- Remote ref CAS simultaneous acquisition admitted one winner; stale local claims blocked. A new regression detects and rejects different logical actor attempting to release a task with valid token/epoch.
- Human-reviewed stale takeover **simulated** (expiry moved by controlled remote test commit); no automatic takeover. Old claimant could not write after remote epoch changed.
- Induced offline Git remote blocked shared task writes; divergent Git history was not auto reset/overwritten.
- Two parallel child research runs with separate output/event journals were manually reconciled without discarded evidence; process-isolated deterministic QC recorded and exact-hash checked before a synthetic merged portfolio file.
- An active child run was moved to a different local bare Git remote/clone, reloaded from event history; claims were correctly NOT inherited.
- No live ad/CRM/website/provider operations. These are separate OS processes, NOT actual independent AI provider platforms; reviewer was deterministic, not a second model.

## Discovered defect and correction

`tools/git/coordination.py:GitClient.release` previously accepted any 4-field actor so long as token+epoch matched. With shared Git credentials, this could incorrectly attribute release to another agent if the token leaked. New code validates exact current owner actor before recording release. Added regression P17-03b PASS. File-declared identities remain cooperative and not cryptographic authorization.

## Evidence and open items

- `tests/acceptance/test_git_cross_agent.py`, `git_collab_worker.py` and `temp/tests/PROMPT-17-LOCAL-RESULTS.json`: executable tests and actual case-level PASS ledger.
- `docs/testing/PROMPT-17-GIT-COLLABORATION.md`: classification/PRD comparison and limitations.
- Hosted GitHub Actions experiment in `.github/workflows/aosw-p17-git-collaboration.yml`; GitHub-hosted CAS/LFS results MUST be checked after publication, never assumed.
- Live GitHub refs may have permission/ruleset limitations, and LFS server locking may be unavailable. In such cases report BLOCKED.
- Separate ChatGPT/Codex/Claude/Muse agent-surface handoff, persistent multi-session cloud volume, signed approvals, provider fencing and scheduled occurrence remains NOT RUN.

Next: hosted experiment readback; complete separate P15 library commit and repeat acceptance; Prompt 18 staged marketing pilot, no external live operations.
