# Prompt 16 — Standalone Offline Practical Acceptance

Date: 2026-10-20T12:26:15.598290+00:00
Baseline: verified aos-w-portable-0.6.0.zip
ZIP SHA-256: `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`

**Environment:** Actual extracted local ZIP in a fresh non-Git working directory. The optional development-only state and init helpers were called OUTSIDE the installed scaffold. A second Python process loaded only pinned files/hand-off and offline fixture input. Research and reviewers operate on fictional sources; no real advertisers or customer data. **No separate hosted persistent cloud filesystem was available/tested.**

**Results:** 13 PASS / 0 FAIL / 1 NOT RUN

| Case | Expected behavior | Actual outcome | Evidence |
|---|---|---|---|
| P16-01-fresh-zip-no-git | Install verified standalone ZIP in arbitrary persistent local folder, with no Git and no existing runs. | **PASS** — version=0.6.0, archive_bytes=97648, protected_files=54, git_repo_in_install=False, existing_workflow_instances=0 | protected-baseline.json |
| P16-02-initialize-real-research-workflow | Create pinned CREATED run with exactly one initially eligible unconditioned task. | **PASS** — created=offline-research, pin=sha256:1e7eb336acfd9489ea3c8f465c08575e3c169e, ready=['define-scope'], fixture_rows=3 | initial-handoff.json, offline-working-directory/aos-w/agent-files/instances/offline-research/instance.json |
| P16-03-real-step-and-deliberate-midtask-interruption | Write scope artifact, complete and checkpoint step; persist an incomplete running evidence attempt. | **PASS** — completed=['define-scope'], interrupted=['collect-evidence'], events=10, cp_before_interruption=checkpoint-000005, cp_during_interruption=checkpoint-000009 | interrupted-state.json, offline-working-directory/aos-w/agent-files/instances/offline-research/runs/run-001/artifacts/scope.md |
| P16-04-cold-process-recovery-and-real-research-completion | New process discovers handoff, correctly restarts incomplete task, writes fictional research, reviews artifacts, completes and checkpoints. | **PASS** — separate_process=True, start_from_persisted_handoff_seq=10, final_event_seq=23, status=COMPLETED, all_steps=['define-scope', 'collect-evidence', 'review-, resumed_task_attempts=2, qc=self_review_pass_on_fictional_fixture | cold-agent-output.txt, offline-working-directory/aos-w/agent-files/instances/offline-research/runs/run-001/events.jsonl, offline-working-directory/aos-w/agent-files/instances/offline-research/runs/run-001/artifacts/evidence.md |
| P16-05-protected-file-write-boundary | Protected framework hashes unchanged; event history and outputs under agent-files. | **PASS** — protected_hashes_match=True, protected_count=54, all_runtime_records_under_agent_files=True, no_git=True, review_event_present=True | protected-baseline.json, acceptance-results.json |
| P16-06-custom-template-and-manual-instance | Custom source, graph revision, snapshot and actual executed step saved only under agent-files. | **PASS** — user_custom_source=agent-files/custom-templates/local-custom-res, custom_pinned=True, actual_step_executed=define-scope, next=collect-evidence | offline-working-directory/aos-w/agent-files/custom-templates/local-custom-research/template.yaml |
| P16-07-transient-failure-bounded-retry-correction | Explicit attempt-1 failure and correction, new attempt, validated output; no silent completion. | **PASS** — retry_attempts=2, failure_logged=True, correction_logged=True, next=['review-evidence'] | offline-working-directory/aos-w/agent-files/instances/custom-instance/runs/run-001/events.jsonl |
| P16-08-qa-failure-remediation-resubmission | Rejected review blocks completion; unauthorized retry denied; corrected revision accepted after explicit approval. | **PASS** — first_verdict=REVISE, second_verdict=PASS, explicit_retry_approval_required=True, status=COMPLETED | offline-working-directory/aos-w/agent-files/instances/custom-instance/runs/run-001/artifacts/summary.md |
| P16-09-versioned-graph-revision-nondestructive | Unapproved revision denied; scoped mock-approved revision retains original graph/history and invalidates descendants. | **PASS** — revision=g0002, preserved=['define-scope'], invalidated=['collect-evidence', 'review-evidence'], history_preserved=True, approval_is_mocked=True | offline-working-directory/aos-w/agent-files/instances/custom-instance/graph-revisions/g0001.yaml, offline-working-directory/aos-w/agent-files/instances/custom-instance/graph-revisions/g0002.yaml |
| P16-10-pause-resume-cancel | Paused run refuses task start; explicit resume works; canceled run refuses task start. | **PASS** — paused_blocked=True, resumed=True, cancelled_blocked=True, checkpoint=checkpoint-000004 | offline-working-directory/aos-w/agent-files/instances/cancellation/runs/run-001/events.jsonl |
| P16-11-partial-journal-recovery | Torn JSONL detected, cannot auto-repair, authorized repair preserves valid prefix and quarantines tail. | **PASS** — corrupt_detected=True, repair_explicit=True, tail_quarantined=True, previous_running_state_retained=True | offline-working-directory/aos-w/agent-files/instances/corrupt-test/runs/run-001/events.jsonl |
| P16-12-ambiguous-external-operation-idempotency | Mock provider operation uses stable key; duplicate intent and unreconciled completion blocked. | **PASS** — duplicate_blocked=True, reconcile_required=True, mock_provider_only=True, no_real_provider_call=True | offline-working-directory/aos-w/agent-files/instances/provider-ambiguity/runs/run-001/events.jsonl |
| P16-13-final-root-immutability | All framework bytes untouched after entire suite; install still contains no .git. | **PASS** — protected_files_unchanged=54, runs_with_event_journals=5, no_git=True | protected-baseline.json |
| P16-14-separate-persistent-cloud-filesystem | Install on separate genuinely persistent cloud filesystem with an independent lifecycle and rerun offline cold start. | **NOT_RUN** — A separate persistent cloud filesystem accessible through an authorized execution environment was not available. The isolated local folder is not a cloud substitute. | None |

## Actual execution evidence

- `offline-working-directory/aos-w/agent-files/instances/offline-research/runs/run-001/events.jsonl` — verified event chain with real scope and evidence artifacts, attempts, QC and final checkpoint.
- `initial-handoff.json`, `interrupted-state.json` and `cold-agent-output.txt` — source interruption state and cold independent-process resume.
- `protected-baseline.json` — all standardized file SHA-256 values; compared after workflow completion and failure scenarios.
- `acceptance-results.json` — individual assertions and outcomes.

## Corrections and rerun evidence

- Two initial harness assertions incorrectly expected `collect-evidence` to appear as automatically READY; because it requires a step-local skill, AOS-W reports a context/skill check blocker until the agent explicitly verifies it. Corrected the assertions, kept `context_checked=True` at the actual attempt, and reran the complete suite: 13/13 PASS. This is a **test harness correction**, not a framework defect.

## Scope and deviations

- Offline sources are deliberately fictional so this proves workflow execution/state integrity, **not** factual competitor research quality or external-provider integration.
- Python was used as an **optional local deterministic test harness**; the installed folder contains neither the helper code nor Git. No assertion is made that an AI model independently initiated tool actions in a foreign harness.
- Separate persistent cloud filesystem/second cloud host was **not available**. Local second-directory tests cannot count as cloud acceptance.
- A graph revision uses a **mocked owner approval**; manual run records cannot authenticate the owner and cannot authorize real effects.
- Background scheduling, concurrent shared agents, hosted Git CAS/LFS, and real Meta/CRM calls are out of scope.
