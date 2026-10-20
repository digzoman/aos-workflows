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


## 2026-10-20 verified continuation audit

Prompt 15 was subsequently published in commit 3512cb7, schema repair a7b7e8a. Hosted 0.7.0 CI run 39434478250 PASSED 126 tests and published a clean preview ZIP. Previous P15-uncommitted notices above are historical, no longer current. Prompt 17 hosted CI run 39428039269 concluded success, but its OWN output states CAS REVIEW_REQUIRED and LFS BLOCKED. Prompt 18 pilot NOT RUN. Prompt 19 release assessment initiated and status HOLD; see docs/release/V1-READINESS-2026-10-20.md. Formal PRD-wide approval, independent AI cross-platform handoff and cloud persistent acceptance are still unfulfilled. No stable V1 release authorized.


## Prompt 18 synthetic executable pilot, verified 2026-10-20

CI run 39495294275 SUCCESS. Actual optional RunStore executed 77 on-disk event transitions in a mock three-vertical marketing scenario, including incomplete research QC -> correction, SVG fixture QC -> correction, parallel CRM/landing prep, cold reopening, checkpoint/handoff and deliberately NOT_GRANTED live permit. Report docs/testing/PROMPT-18-SYNTHETIC-PILOT-REPORT.md. This does NOT satisfy T01 real Ampgent pilot, independent model QA or provider state verification. Hosted portable CI 39495294210 also SUCCESS. Prompt 19 remains release HOLD pending original criteria and owner approval.


## Prompt 18 latest source-grounded execution, 2026-10-20

GitHub Actions run 39498378421 SUCCESS, 27/27 assertions, three separate research child run instances, eight real public supplier-offer pages, rejected and preserved v1 research and creative, deterministic reviewer subprocess, corrected 1080x1350 PNG, 57 parent events, 13+8+8 child events, exact-hash child join, cold reopened state and blocked launch. Evidence automatically committed under docs/testing/evidence/p18-grounded-39498378421, with formal report docs/testing/PROMPT-18-END-TO-END-RESULTS.md. This is partial original T01/T04 proof. No active Meta Ad Library cards verified, no independent AI review, no provider action or owner budget authorization. Prior synthetic pilot entries are historical, latest source-grounded evidence supersedes for staged scope.
