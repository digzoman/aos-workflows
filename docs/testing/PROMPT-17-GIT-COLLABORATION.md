# Prompt 17 — Git synchronized and cross-agent collaboration acceptance

Date: 2026-10-20. Base repository `digzoman/aos-workflows` at commit `d7f59cdd30959b2f2cee8a082c5545fe1d7fe82d`. Prompt 15 marketing library remains uncommitted at this baseline, so no false claim that this exercises its 0.7.0 distribution.

## Actual testing environment and trust levels

- **REAL LOCAL GIT:** Git 2.47.3, separate `git clone` working trees, ephemeral bare Git remote, Git commit/push/fetch/ref updates, separately spawned worker processes, real readback of accepted artifacts and event journals. The three process sessions are programmatic test workers (not separate language models or external services).
- **SIMULATED/CONTROLLED:** Research offers are fictional, reviewer is a deterministic separate OS process, interrupted worker is emulated by stopping task work (no kill of a persistent AI service), expiry advanced via a test-controlled remote claim commit, and any intended human approval is not authenticated.
- **BLOCKED/NOT RUN:** Actual ChatGPT ↔ Codex/Claude/Muse provider handoff, independent durable cloud agent sessions, provider-side Git claim fencing, and production ad/CRM activity. A hosted-GitHub ref-CAS and LFS experiment is separately run via Actions and must be evaluated from actual results; code or workflow presence alone does not count.

## Expected/observed acceptance matrix — real local bare Git

| ID | Expected and actual criterion | Classification |
| --- | --- | --- |
| P17-01 | Two distinct subprocesses independently discover eligible child research work from Git-cloned pinned records; use same Git email but distinct `[Agent, Platform, Role, Instance]`. | REAL LOCAL GIT |
| P17-02 | Simultaneous claims on one remote ref produce exactly one winner; stale clone owner cannot acquire already claimed task. | REAL LOCAL GIT |
| P17-03 | Worker-start refuses claim token supplied with a different four-part actor. | REAL LOCAL GIT + local guard |
| P17-03b | Wrong logical actor cannot release a current claim even with valid token/epoch (Prompt 17 implementation correction). | REAL LOCAL GIT + local guard |
| P17-04 | Claimed worker executes a real local research step, checkpoints/submits dated synthetic evidence, pushes a scoped `agent-files` commit, and remote readback matches. | REAL LOCAL GIT |
| P17-05 | Third fresh process/cloned filesystem inspects persisted handoff, produces a separate deterministic QC decision, original worker finishes after refreshing, receiving worker replays verified completed event chain. | REAL LOCAL GIT; NOT different AI model |
| P17-06 | Worker stops while holding a claim. Expiry does not automatically transfer ownership; explicit reviewed reclaim gets epoch+1; prior token cannot submit stale work. | REAL LOCAL GIT with SIMULATED expiry |
| P17-07 | Remote disconnect prevents claim revalidation and task mutation; disconnected worker cannot invent successful push. | TEST-INDUCED REMOTE FAILURE |
| P17-08 | Two clones make diverging commits; Git sync refuses automatic merge/reset and preserves local conflicted bytes. | REAL LOCAL GIT |
| P17-09 | Two workers complete *independent* child tasks in local parallel branches. Remote update while B has unfinished local draft blocks automatic refresh; operator preserves draft, explicitly reconciles, and publishes both child journals. Separate process checks evidence/QC, each producer completes and releases its claim; merged synthetic summary references exact artifact hashes and review IDs. No *live* marketing synthesis or human approval claimed. | REAL LOCAL GIT + manually reconciled test fixture |
| P17-10 | A partially executed workflow migrates to another local bare Git repository, cloned fresh; verified state survives. The new remote has no inherited claim ownership—reconfiguration/reclaim is explicit. | REAL LOCAL GIT |

All test case outcomes are verified by running `test_git_cross_agent.py`; any failure must remain FAIL until corrected. Do not extrapolate local results to hosted GitHub, production locks, independent human/AI identity authentication, or exactly-once provider effects.

## Known safety gap found and correction

The prior `GitClient.release()` verified only token/epoch, but accepted any syntactically valid four-part actor as the recorded releaser. On a shared Git credential, that misattributed the release when a different logical actor possessed the token. P17 adds an explicit equality check against current claim owner; P17-03b rejects the incorrect release. This is **cooperative provenance consistency**, not cryptographic authentication—someone controlling the token and arbitrary source files can still lie about actor identity.

## PRD acceptance comparison

- **T02 cross-platform handoff:** PARTIAL ONLY. Fresh process, clone and no in-memory conversation succeeded, but ChatGPT/Codex/Claude/Muse independent provider handoff not executed.
- **T03 exclusive collision prevention:** PASS for actual local bare Git ref-CAS and stale output rejection in tested client. Hosted GitHub server must be separately proved. External provider effects remain unfenced.
- **T04 review/correction:** Local deterministic separate reviewer and gate ordering tested, but independent AI review not exercised here (earlier P12/P16 tests cover mock QC remediation).
- **T05 immutable revision preservation:** Existing Prompt 16 cases exercised revisions; this test checks checkpoint transfer and branch merges but not cross-platform revision race.
- **T06 move Git repo and resume:** PASS for migration to a **different local bare Git remote** with explicit claim-reset caution, not a different hosted Git provider.
- **FR-401–FR-406, FR-501–FR-506, NFR-07/NFR-08:** Local snapshots, owner and trailer attribution, conservative sync, fail-closed offline, manual reclaim, separate child histories satisfy bounded local tests. Human identity verification, hosted CAS and distributed provider fencing remain open.

## Next actions

Examine hosted GitHub Actions P17 results and JSON evidence before upgrading ADR-014 from provisional. Exercise a true independent AI/provider agent handoff when platform tools and a persistent shared test workspace are authorized. Avoid treating Git account ownership or LFS lock ID as four-part agent authentication; keep Git optional for standalone use.

## Executed local results

**11 PASS, 0 FAIL.** Tests were actually executed in independent local Git worktrees: nine cases in a first unittest invocation (25.252 s) and the parallel merge plus migration cases in a second invocation (16.943 s). Each test created a fresh isolated bare remote and clean clones. The complete self-contained case evidence is in `temp/tests/PROMPT-17-LOCAL-RESULTS.json`; the reproducible test files provide the actual assertions and verification reads. This run was split for the tool execution window, not to omit failed cases. The final source tree will also be exercised by a separately tracked GitHub Actions job.

**One defect corrected:** `GitClient.release()` now requires the supplied actor to equal the current remote claim owner, in addition to a valid token and epoch. It does not authenticate that actor as a real human or distinct AI provider; it prevents accidental misattribution in the cooperative protocol.
