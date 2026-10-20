# Persistent execution state and recovery (file-only protocol, 0.3.0)

**This page is a normative agent-readable procedure; it does not require Python, Git, MCP, a cloud service, a database or an unattended scheduler.** A compatible agent can follow it using plain text/YAML/JSON files. All user/runtime writes go under the installed `aos-w/agent-files/` root. `tools/state/` is an optional developer helper outside the downloadable scaffold.

## 1. Authoritative records

Open the instance's `template-lock.json`, immutable `graph-revisions/<id>.yaml`, `runs/<id>/run.json`, `events.jsonl`, `state.json`, latest `checkpoints/<id>.json`, attempt records and `handoff.md`. If `run.json` points to a different revision than the latest **valid** `graph_revised` event, reconcile the pointer with the verified immutable graph bytes. Do not follow the latest master-template revision.

- `events.jsonl`: **append-only accepted history**; use a new event to correct an older statement, never silently replace a successful past event. One JSON object per complete LF-terminated line with monotonically increasing `seq`, actor identity, timestamp, pinned graph revision, evidence and previous-event hash when available.
- `state.json`: **materialized view** (run ID, graph revision, task status, attempts, owner, evidence, pending actions, retry conditions, last event sequence/digest and eligible task candidates). This is rebuildable from events, never more authoritative than them.
- `checkpoints/<id>.json`: immutable event-prefix anchor with current graph, completed/blocked tasks, pending operations and output references. A checkpoint is *not* a guarantee of remote synchronization.
- `tasks/<task-id>/attempts/<attempt-id>.json`: derived attempt evidence. The original event trail survives future attempt updates and corrections.
- `handoff.json` and `handoff.md`: concise next action, blockers and uncertainties for a **different agent in a new conversation**. Handoff is an index, not proof of provider-side success.

Read the **actual file** and confirm its artifact version/digest, not a stale report. If hashing is unavailable, use `integrity_level: advisory` and do not claim cryptographic verification.

## 2. State transition checks

| Current state | Event | Allowed next state and obligations |
| --- | --- | --- |
| WAIT_DEPENDENCY | task_ready | READY only if predecessor results/required quality are current and needed policy/skills/permissions are available |
| READY | task_claimed | CLAIMED, record `[Agent \| Platform \| Role \| Instance]`; advisory only without tested backend |
| CLAIMED | task_started | RUNNING; new `attempt_id`, increment attempt count, preserve past attempts |
| RUNNING | task_completed | COMPLETE only if declared artifacts exist, evidence is current, and gate verdict matches exact artifact revision |
| RUNNING | task_submitted_review | WAIT_REVIEW; exact artifact set/rubric and reviewer required |
| WAIT_REVIEW | review_revise | NEEDS_REWORK with corrective instructions; no downstream eligibility |
| RUNNING/WAIT_REVIEW | task_failed | BLOCKED or FAILED with error class, retry budget and next eligible time |
| BLOCKED/NEEDS_REWORK | task_requeued | READY after permitted correction, bounds, delay and side-effect reconciliation |
| Any active nonterminal | task_paused / task_resumed | PAUSED, then only explicitly authorized continuation; a formerly running task starts a fresh attempt |
| Run ACTIVE | run_paused / run_resumed | PAUSED / ACTIVE; no new work while paused |
| Run nonterminal | run_cancelled / run_failed | CANCELLED / FAILED; preserve artifacts and prior events |
| State at old revision | graph_revised | New immutable graph; preserve prior results, invalidate changed and downstream branches only |

`UNKNOWN`, `RECONCILE_REQUIRED`, missing required skill, missing reviewer or missing action authorization must **block**, not be interpreted as true or success. Conditional and composed tasks still use `references/COMPOSITION.md` to determine eligibility.

## 3. Manual commit and checkpoint protocol

1. **Before** task work: verify dependencies, approved scope, exact pinned graph, required skills and any necessary claim. Inspect prior attempt and operation ledger. Choose a unique attempt ID, append `task_started` and save its actor/time.
2. Perform only the permitted bounded work. Put outputs under `runs/<id>/artifacts/`; provide media type, source, locator, revision and hash where possible. Never write to protected framework directories.
3. On success, verify files really exist. If QC is required, record `task_submitted_review`, obtain a review on the **exact versioned artifact set**, then record acceptance or corrective verdict. Append `task_completed` only after all required checks pass.
4. On failure, append `task_failed`/`review_revise` with error category, actual attempt count, **correction instructions**, retry limit, next eligible time and human intervention requirement. No automatic future wake is implied. Never repeat unknown external writes.
5. Before ending the session, append final meaningful event, update `state.json` anchored at that event, persist a checkpoint for that exact *earlier verified event prefix* and then append `checkpoint_created`. Update both handoffs with blockers, pending provider operations and next candidates. In optional helpers, file snapshots use temp-file/replace and fsync where supported; this is **not** a cross-host transaction guarantee.
6. If an optional Git mirror is enabled, confirm remote sync separately. A local checkpoint never implies successful Git push.

No agent needs to audit every file read. Record meaningful state transitions, owner changes, artifacts, reviews, approvals, external intents and recovery decisions.

## 4. Failure categories and bounded retries

Configure per-node `retry.max_attempts`, `retry.on`, `retry.backoff` and, if fixed/exponential, `delay_seconds`. Errors include transient source unavailability, rate limits, incomplete evidence, failed QC, unknown provider result and human intervention. A manual agent does not wake automatically after a delay; it checks the clock **on invocation** and records the observed time.

A failed review retains its original review record. On correction, use a new attempt and new review bound to the changed version; old history remains inspectable. Exceeding `max_attempts` blocks or fails the task with escalation, rather than secretly resetting the counter. A delayed retry with time in the future is WAITING, not READY. Additional permissions are never implied by having retry attempts left.

## 5. External operation reconciliation before retry

Before any **authorized** external mutation, form an operation key from run ID, task ID, provider, exact resource and canonical desired change. Write `operation_intent` to durable history **before** calling provider, with approval ID, pre-state/source and desired payload digest. Then write `operation_submitted`, followed by provider acknowledgement if observed. **An ACK alone is not proof of deployed effect.** If a timeout or crash could have happened after submission, mark `RECONCILE_REQUIRED`.

Use an authorized provider **read-only** lookup of the actual resource and attach provider identity, observed time, provider object/ref and result (`APPLIED`, `NOT_APPLIED`, or `MISMATCH`). Record `operation_reconciled`. An explicitly verified `NOT_APPLIED` result may permit a **new separately authorized attempt** after `task_unblocked`, using a new operation key that refers to the previous reconciled operation; `APPLIED` cannot be replayed. Do not automatically replay an ambiguous write merely because a task or process restarted. A local claim, approval ID string, or API request body does not prove permission; it must be checked against actual owner/host authorization. The optional state helper **never contacts a provider**.

## 6. Interrupted or inconsistent state

1. Verify run identity and pinned graph bytes before accepting a new writer. Reconstruct the longest **valid** complete JSONL event prefix, checking sequence and digest if present. Ignore unverified or torn event tails as evidence of success.
2. If the latest JSONL line is corrupt/truncated, **stop** and quarantine the exact bytes to `runs/<id>/recovery/`. Only with explicit authorized repair may the helper rewrite the file to the **unchanged valid prefix** and append `recovery_checked`. Preserve original suspect bytes. Never silently rewrite accepted historical events.
3. If `state.json` disagrees, save the older snapshot as evidence and rebuild from accepted events. A checkpoint claiming a missing or mismatched event digest is flagged; the checkpoint is not used to overwrite the event ledger.
4. Verify completed artifacts are still present and match recorded hashes; a changed or missing file is a **current integrity blocker**, not erasure of the historical completion event. Reevaluate descendants and reviews.
5. Detect partly created child instance directories: mark MISSING, PARTIAL, INITIALIZED or CONFLICT. Do not recreate/overwrite an existing child without explicit reconciliation and authorization.
6. For a graph revision interruption, verify `graph-revisions/<id>.yaml` content digest from the event before repairing a stale `run.json` current revision pointer. Preserve earlier graph files, accepted results and revision history.
7. Leave `handoff.md` and optional `handoff.json` showing exact last valid sequence, current task/owner, remaining approvals, recovery blockers, provider uncertainties and next eligible candidate. A fresh agent must be able to continue using **only persisted files**.

## 7. Optional helper, guarantees and limits

The development repository includes `tools/state/state.py` and `cli.py`. **Python is never installed or required inside the downloadable `aos-w` folder.** The helper can replay/check SHA-256-chained events, fsync local append, atomically replace derived JSON snapshots where supported, calculate bounded retries, quarantine corrupt tails, detect stale artifacts, and verify revision content and run pointers. Loading YAML requires optional PyYAML. The helper supports **only single-writer/local** mode, with no remote claim enforcement. Shared coordinated mutations are explicitly refused.

File-only agents can follow the same protocol without helpers, but must honestly mark hashes, exclusivity, persistence and clocks as UNVERIFIED when not actually checked. Automated timers, provider reads/writes, authenticated approval, exactly-once external effects, and real distributed collision prevention **are not implemented**. Reference examples are fictional and do not authorize real customer data or ads.
