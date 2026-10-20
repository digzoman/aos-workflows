# V1 Acceptance Test Matrix and Evidence Protocol

**Status:** DRAFT; not executed. PRD source: [PRD.md](PRD.md) §§16–20. The six original survey tests are T01–T06, plus Prompt 01b and research-derived coverage. **Do not mark any test as passed merely because a requirement, test plan or source observation exists.**

## Standard test report contract

Each run produces a test ID, UTC execution time, framework/PRD/template/run revisions, host and mode (local single-writer, persistent cloud, Git synced or verified shared), actual capabilities, preconditions, actor role, steps, expected behavior, actual evidence references/hashes, PASS/FAIL/BLOCKED/NOT_RUN, limitations, fix or handoff, and reviewer identity where relevant.

Evidence levels are **LIVE/REAL**, **MOCKED/CONTROLLED**, **MANUAL/COOPERATIVE**, **NOT_RUN**. LIVE requires a real host/provider/agent action actually observed; an event in old repository research is not a test execution. MOCKED must identify the simulated boundary. Manual can show protocol behavior but not enforced cross-process mutual exclusion.

## Six survey-mandated acceptance demonstrations

### T01. Real Ampgent workflow execution

- **Setup:** sanitize a real-ish owner-authorized competitive research question and portfolio for Bucket 9 or other approved Ampgent offering. Establish source/buyer relevance and approved research-only boundaries. Do not copy secrets or private raw ad content to the public repo.
- **Steps:** instantiate workflow; preflight actual accessible sources; generate a keyword/advertiser queue; execute bounded run(s) with checkpoints; log qualifying/blocked source evidence; dedupe; apply named appropriate scoring rubric; independent review; synthesize opportunities; create creative/Meta handoff proposal with separate authorization.
- **Positive:** next-task eligibility, all output references, source dates, evidence confidence, score version, review, committed/verified handoff work; no phantom Meta activation.
- **Negative:** inaccessible Meta card not accepted as observed absence; missing source-ad ranking yields PROVISIONAL, not invented FULL; unsupported consumer ad excluded from B2B tool supplier count.
- **Evidence:** dated run events, query/advertiser evidence tier, independent review, output report/handoff. Record whether source browsing LIVE or controlled/mock.

### T02. Cross-platform handoff

- **Setup:** agent platform A starts an authorized run and intentionally stops mid-work after durable checkpoint; platform B uses a separate session/context and the same retained folder.
- **Steps:** B reads scaffold rules and run state, verifies exact output hashes/revisions and permission, identifies next eligible node, produces a bounded artifact, commits/syncs if configured, leaves updated handoff.
- **Positive:** completed tasks not repeated; source/approvals still respected; meaningful work performed by a genuinely different platform.
- **Negative:** stale summary says NOT STARTED while child event says RUNNING; B detects inconsistency and does not erase child work.
- **Evidence:** distinct four-field producer identities, artifact before/after and separate platform timestamps; a mock second agent is **not** sufficient to claim real cross-platform success.

### T03. Exclusive two-agent claim collision prevention

- **Setup:** shared Git test repository, same task/run ID, two independently executing agents; at least one run under same GitHub login and another distinct credentials if available. Test both LFS and CAS proposals before selection.
- **Steps:** simultaneous claim request; inspect authoritative server claim/lock and both client responses; complete with winner and attempt stale owner submit; repeat across many races; exercise lease expiration, reclaim, crash, lost result and network restoration.
- **Positive:** no two valid active exclusive owners for one task at a time; new fenced owner rejects stale outputs; different task IDs may proceed concurrently; clear mechanism/version documented.
- **Negative:** Git worktree or bare claim Markdown considered a task mutex, REST PATCH assumed to support expected-old SHA without proof, same-login LFS allowed both clients to mutate.
- **Evidence:** remote refs/server locks, exact replies and server timestamps, claimant identities, conditional update results, stale output test. A protocol mock alone is insufficient for this core criterion.

### T04. Failed independent quality gate and targeted repair

- **Setup:** two branches with approved inputs, reviewer gate requiring independent agent on branch B, one intentionally wrong image/logo or insufficient source evidence.
- **Steps:** attempt join, receive REVISE/INSUFFICIENT; dependent node blocked while unrelated branch remains eligible; correct failing artifact only, resubmit reviewer on new hash; join.
- **Positive:** old FAIL and new PASS both retained; modified artifact hash invalidates old approvals, unaffected siblings remain valid.
- **Negative:** reviewer has not inspected new required asset but parent marked PASS; QC PASS automatically confers permission to publish.
- **Evidence:** gate evaluation snapshots, hashes, named reviewer identity, after-repair dependency graph.

### T05. Revise active workflow without erasing history

- **Setup:** active multi-step workflow with completed and pending nodes and at least one accepted review.
- **Steps:** propose a new conditional node, change one downstream dependency and approval rule under workflow's revision policy, apply with owner decision if required, recompute eligibility and review invalidation.
- **Positive:** old graph, events and completed artifact preserved, new graph version recorded, stale downstream gate invalidated, correct next step, no unauthorized run.
- **Negative:** retrospective edits destroy old reviewer verdict or silently repeat completed external operation.
- **Evidence:** graph before/after, revision event, unchanged completed hashes, approval history.

### T06. Portability to another Git repository

- **Setup:** running instance in Git-enabled test repository A, copied to a different repository B and remote/ref reconfigured intentionally.
- **Steps:** verify local run state, move file tree with full agent-files and essential template/snapshot references, change mirror settings without touching framework base, synchronize to repo B, fresh agent resumes.
- **Positive:** stable logical run identity and task dependency state, remote-specific refs clearly reconfigured, no lost event/approval; generated indexes rebuildable.
- **Negative:** hardwired original GitHub URL/branch prevents standalone recovery; old remote treated as current authority without reconfiguration.
- **Evidence:** both sanitized test repo SHAs, old/new references, successful continuation artifact.

## Prompt 01b and baseline portability tests

### T07. No-Git local standalone and writable boundary

- Copy only scaffold/aos-w into a clean directory with no Git/Node/Python required; run a one-off bundled example by agent instructions, checkpoint, close session, resume.
- Create a custom template and instance skill inside agent-files; framework files unchanged. Attempt writing to templates/ during normal execution, agent/validator rejects it.
- Optional host code may run if present, but test result MUST establish no mandatory dependency.
- Evidence: complete copied directory tree, run state, before/after framework hash or file list, distinct resumed session.

### T08. One-off and manual invocation from recurring template

- Launch a template with no schedule; verify non-repeating default and no automatic subsequent occurrence.
- Instantiate a template with a schedule; override/disable schedule for one instance and manually launch another run without losing schedule metadata.
- Verify manual run ID different from any schedule occurrence, and no background execution while no scheduler host is present.
- Evidence: trigger declarations, run/occurrence IDs, event timestamps and disabled-host observation.

### T09. Recurring occurrence identity and duplicate wake policy

- In optional host or controlled simulation, fire the same intended scheduled occurrence twice; only one accepted execution identity with verified coordination.
- Exercise pending previous occurrence, missed three daily windows, daylight-saving repeated and skipped local wall clock, timezone change and schedule edit.
- Observe behavior according to **approved** configured policy. If the policy has not been decided, mark BLOCKED rather than silently inventing a default.
- Evidence: occurrence keys, scheduler events/claims, explicit LIVE or MOCKED labels.

### T10. Skills resolution, provenance, and safe fallbacks

- Bind a bundled skill to one eligible step and verify it loads then (not at startup for every step).
- Resolve custom-template skill and approved run-local skill, preserve source/revision, then intentionally present conflicting/untrusted remote skill content.
- Reject unauthorized override/privilege expansion, mark missing remote-only skill BLOCKED offline or use explicitly approved pinned snapshot.
- Evidence: resolution log, source hash, trust decision, capability check, no external side effect from skill instructions.

## Research-derived robustness and integration tests

### T11. Ambiguous provider create outcome

- Mock or isolated test account returns timeout **after** accepting a create. Resume agent reads actual object inventory using stable operation identity.
- Positive: reuse/reconcile original object; no duplicate adset/ad. Unknown remains UNKNOWN if no readback.
- Negative: a retry blindly creates a second object.

### T12. Rate-limited provider read-back

- Operation accepted; immediate GET returns rate limit. Resume with allowed safe GET/reconciliation once possible.
- Positive: WRITE_ACCEPTED separate from VERIFY_PENDING and later CONFIRMED; no duplicate activation requests, no guessed actual delivery.
- Negative: status printed "live delivering" solely from initial PATCH response.

### T13. Creative sub-branch repair

- One valid portrait image and one square with wrong official logo or clipping. Independent semantic/visual QA flags square.
- Positive: redo only composite/export/visual and affected review/approval; original copy/research/portrait hashes unchanged.
- Negative: all assets re-generated or old reviewer verdict passed to replacement square.

### T14. Stale derived index and torn state

- A child run is started while aggregate index remains stale; inject partially written event and inconsistent state snapshot in a copy.
- Positive: detect stale and torn write, recover last verifiable checkpoint, preserve corrupt evidence for analysis and stop if exact outcome uncertain.
- Negative: summary overwrites verified child progress or corrupt event silently skipped as valid.

### T15. Staged Meta config versus authorized activation and held siblings

- Prepare three-level campaign graph with shared parent containing one approved and four held sibling adsets; stage PAUSED and separately request launch subset.
- Positive: exact authorized subtree eligible, held siblings remain PAUSED, per-level configured/effective state and observed delivery distinguished.
- Negative: user approves creative but all campaign children activate; a stale P-prefix name treated as current provider status.

### T16. GHL/website/Pixel/CAPI and lead truth

- Consent/website and mock or safe provider tests for PageView, booking CTA, confirmed booking, Good Lead qualification and actual messages; repeat same webhook event_id.
- Positive: click isn't Schedule; booking is not automatically QualifiedLead; browser/server events dedup or explicitly unresolved; bot saved config vs delivered FB/IG conversation separately verified.
- Negative: synthetic test lead published as customer conversion, double-counted appointment, no-consent transmission or GHL published-workflow list claimed to prove internal trigger.

## Release-gate summary

- All six original tests T01–T06 are mandatory as user-selected success demonstrations; T03 must contain a **real shared-claim race**, not just a hypothetical diagram.
- T07, T08 and T10 mandatory from the no-runtime/skills/trigger requirements.
- T09 and T11–T16 require at least controlled failure-scenario validation with appropriately labeled tool coverage; no accidental production ad actions.
- Missing required environment capability can yield BLOCKED/NOT_RUN with a meaningful explanation, but **does not count as passing a mandatory V1 test**.
- QA reviewer and owner approve release only after test evidence is inspected; Git commit alone does not prove tests occurred.
