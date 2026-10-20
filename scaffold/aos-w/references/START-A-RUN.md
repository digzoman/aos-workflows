# Start or resume a workflow without scripts

**For a capable AI agent or human following the file protocol.** Use `../README.md`, `../PROTOCOL.md`, `../agent-files/README.md` first. This is the full no-runtime procedure for the 0.1.0 scaffold; it does not start anything automatically.

## A. Discover and choose

Read the read-only index `../templates/README.md`; look inside each template's `template.yaml`. Also inspect `../agent-files/custom-templates/` and `../agent-files/instances/` for existing user templates/runs. Prefer **resuming** an existing run when its handoff refers to the task; do not duplicate work because the chat started over.

For a new low-risk walkthrough, choose `research-starter` with question **"Which evidence sources might help us compare three hypothetical software services?"** and no account access. Confirm bounds, needed skills and owner scope. Its output paths are relative to the **run root**, not the master template folder.

## B. Pin the original definition before work

Choose unique lowercase-safe `instance-id` and `run-id` (such as `example-research-001` and `run-001`). Under **`agent-files/instances/example-research-001/`**, create:

- `template-snapshots/<content-id>/template.yaml` — exact frozen resolved YAML; a hash is recommended if the host can calculate it.
- `template-lock.json` — template ID/version, source path, snapshot path, digest/integrity confidence, graph revision and timestamp. Do not claim verified SHA if you cannot compute it.
- `graph-revisions/g0001.yaml` — immutable resolved graph for this instance.
- `instance.json` — parameters, effective policy, current graph revision, creator and timestamp.
- `runs/run-001/run.json` — manual trigger, run identity, actual host capabilities and timezone-aware created_at.
- `runs/run-001/events.jsonl` — initial `run_created` event, seq 1, actual actor identity/time.
- `runs/run-001/state.json` — current run/task status and anchor `last_event_seq: 1`, integrity level advisory unless proven.
- `runs/run-001/handoff.md` — current eligible task, blockers and precise next action.
- Empty supporting folders `runs/run-001/checkpoints/`, `tasks/`, `claims/`, `reviews/`, `approvals/`, `artifacts/`, and `skills/`, creating task attempts as tasks start.

Use `../spec/schemas/` to check structural fields. Do not assume its presence means a validator is installed. See [INSTANCE-LAYOUT.md](INSTANCE-LAYOUT.md) for full example paths and [EVIDENCE-AND-PERMISSIONS.md](EVIDENCE-AND-PERMISSIONS.md) for what approval actually means.

## C. Select only eligible work

The starter DAG is:

```text
define-scope -> collect-evidence -> review-evidence
```

For `define-scope`, confirm no source dependency, manual trigger and read/local-writing authority. Write `runs/run-001/artifacts/scope.md`, including evidence criteria and boundaries. Then append `task_started` and `task_completed` events **after** verifying actual output, update state, checkpoint and handoff. Only then does `collect-evidence` become eligible.

The `collect-evidence` step references the bundled `skills/evidence-handling/SKILL.md`; load it **then**, not at agent startup for unrelated tasks. Record observed source versus inference and return blocked/retry when source unavailable.

Before `review-evidence`, ensure the evidence file exists and version is current. The starter uses `self_review` for a harmless local example; record actual reviewer, complete output set, rubric, result and (if valid) summary. A PASS on research does **not** confer permission to publish or spend.

## D. Record resumable history, then stop

At each bounded task boundary:

1. Append one complete UTF-8 JSON event with unique event_id, increasing `seq`, precise task and agent identity.
2. Verify the event was saved, then refresh materialized `state.json` anchored to the same event prefix.
3. Store checkpoint if a verified resume boundary exists, or honestly label the integrity level advisory.
4. Update `handoff.md` with run/graph version, completed tasks, next eligible tasks, unavailable evidence and any required human decision.
5. If Git mirror **is configured**, verify remote status before/after and record actual results. Otherwise stop with local file work only.

The next agent starts by comparing the latest checkpoint with `events.jsonl`, `state.json`, and actual artifact files. A file called COMPLETE is never enough; inspect the evidence. External operations of unknown outcome require live **readback before replay**.

## E. Sample event and state shapes (illustrative, not already executed)

```json
{"schema_version":"1.0.0","event_id":"evt-0001","seq":1,"run_id":"run-001","type":"run_created","at":"2026-10-20T12:00:00Z","actor":{"agent":"sample-agent","platform":"local-manual","role":"worker","instance":"demo-a"},"graph_revision":"g0001","evidence":[]}
```

```json
{"schema_version":"1.0.0","run_id":"run-001","graph_revision":"g0001","state_revision":1,"updated_at":"2026-10-20T12:00:00Z","last_event_seq":1,"integrity_level":"advisory","run_status":"CREATED","tasks":{"define-scope":{"status":"READY","attempts":0,"graph_revision":"g0001"},"collect-evidence":{"status":"WAIT_DEPENDENCY","attempts":0,"graph_revision":"g0001"},"review-evidence":{"status":"WAIT_DEPENDENCY","attempts":0,"graph_revision":"g0001"}},"eligible_tasks":["define-scope"]}
```

The first step is shown READY after recomputing the pinned graph's dependencies, but **not running or completed**. On actual work, append new task events under the user's current actor identity rather than copying the sample actor.

## F. Do not do these things

- Modify `../templates/` or `../spec/` to store run results.
- Use a template file's latest version instead of the pinned graph to resume an old run.
- Invent SHA, peer review, Git push, provider write, scheduler wake or lease ownership.
- Treat missing source as proven absence, failed QC as permanent whole-run failure, or a self-review as independent review.
- Start the workflow just because an old scheduled timestamp has passed and no scheduler was present.
