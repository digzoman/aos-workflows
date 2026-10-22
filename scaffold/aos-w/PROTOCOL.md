# AOS-W portable agent protocol (0.1)

**Use these instructions even with no Git or helper scripts.** This document is a concise standalone procedure. Detailed frozen design guidance is shipped in `spec/`.

## Entry and authority

1. Read `README.md`, `VERSION.json`, `agent-files/README.md` and `agent-files/config/settings.json`. Confirm the folder is actually persistent. Inspect current capability evidence; absent or unverified tools remain UNVERIFIED.
2. Check `agent-files/instances/` for saved instances and each `runs/<run-id>/handoff.md`. Never rely on previous chat context alone.
3. Treat user-authorized work scope and approvals as **separate** from a quality PASS, role, Git access or skill. Read the current approved state of any external provider before making a consequential authorized change.
4. **Only write inside `agent-files/` during normal work.** Path traversal, symlink escape, credentials in public examples, and unreviewed remote script execution are forbidden.

## Start a new run

1. Choose a template under `templates/` or `agent-files/custom-templates/`.
2. Validate the declared source, required parameters, skills, policy, outputs and dependencies. Pin the **resolved template bytes and version**, inherited effective policy and graph revision into a **new** `agent-files/instances/<instance-id>/`. Do not edit the master template.
3. Create `runs/<run-id>/` with `run.json`, `events.jsonl`, `state.json`, `checkpoints/`, `tasks/`, `claims/`, `reviews/`, `approvals/`, `artifacts/`, `skills/`, and `handoff.md`. Paths and schema files are documented in `references/START-A-RUN.md` and `spec/schemas/`.
4. Record run_created as event sequence 1 with four-field provenance `[Agent | Platform | Role | Instance]`. A one-off/manual run never implies further recurrence.

## Pick the next eligible node

A node is eligible only if it exists in the *pinned current graph revision*, its required predecessor outputs are accepted/current, its condition is TRUE (not UNKNOWN), no dependency is blocked or stale, and all required skills/capabilities and **before-execution** action approvals are present. An unresolved provider operation blocks replay. If an exclusive task is requested in shared mode, acquire a **verified** backend claim before mutation; otherwise use single-writer manual mode.

Read relevant skills just in time. Mark missing/untrusted remote skills BLOCKED or use an explicitly permitted pinned offline fallback. Do not execute unknown code merely because a skill mentions it.

## Work, review, checkpoint and handoff

- Record task attempt/start before work and bound retries. Store source and evidence inside the run. External writes require explicit approved operation scope plus before/after provider readback; request ACK is not provider success.
- Validate outputs and exact artifact revisions. If quality review is needed, save review and wait. A failed gate only blocks dependent steps; unrelated approved work may continue.
- Append a complete single-line JSON event with unique event_id and increasing seq. Update derived `state.json`, create a checkpoint anchored to the last **validated** event, then update `handoff.md` with exact next step and blockers. Mark unavailable hashes/integrity tools as advisory or unverified; never invent PASS.
- On restart, inspect event log in sequence and compare its last verified event with state/checkpoint. Preserve suspect partial writes, reconcile external effects before retry, and do not re-create children or provider objects merely because the previous response timed out.
- A material revision produces a **new immutable graph revision** under the instance, preserving prior completed artifacts and invalidating only affected descendants/reviews.

## Git, schedules, and collaboration

Git sync is optional and off by default. If deliberately enabled, inspect remote status **before** changes and verify push/readback afterward. No network means sync remains pending; never assume remote lock ownership.

Default triggers are manual. A scheduled declaration does not run itself. Each true scheduled invocation uses a unique occurrence key; unattended wake requires an external authorized host.

Claims written in `claims/` are advisory in plain-file mode; they are NOT distributed locks. A second writer must not proceed with a colliding task absent a tested coordination backend. Git LFS vs atomic task-claim selection is still a future empirical decision.

## Stop criteria

If data, required reviewer, permission, skill, claim, source or provider readback is missing, record the precise blocker and handoff instead of guessing. Do not declare an external task done based on a local note, Git commit, plan or QC alone.

See `spec/MANUAL-AGENT-PROTOCOL.md` for the longer reference procedure.

## Reusable composition and dynamic child workflows (0.2.0)

Read `references/COMPOSITION.md` for the authoritative no-helper procedure. Every new master/custom node must declare inputs, outputs, quality gates, dependencies and a `contract.done_when`. A `child_generator` creates **PROPOSED** stable-ID children only; separate exact-scope approval is needed before creating their run directories. The parent synthesis node must wait for **every required child's passing current quality review** and a separate synthesis authorization. The optional developer helper can perform deterministic local checks/instantiation, but is not required to follow the file contract. Revision changes append a new graph file and affected state events; never edit prior completed history.

## Persistent state, retries and interrupted-work recovery (0.3.0)

**Read [references/STATE-AND-RECOVERY.md](references/STATE-AND-RECOVERY.md)** before writing task history, recovery, reviews or external operation records. Preserve an append-oriented JSONL event ledger (actor, graph revision, attempt, evidence and optional predecessor digest); treat state.json and handoff as rebuilt views. Verify exact pinned graph and completed artifact hashes on fresh start. A torn last line must be explicitly quarantined/authorized for repair, not silently accepted or deleted. For unknown provider operation effects record intent and RECONCILE_REQUIRED, read actual provider truth separately and never blindly repeat. Bounded retries require correction/limits/optional delay; delay metadata alone does not create a timer. Explicitly pause/resume/cancel/fail rather than infer completion. The optional `tools/state/` developer helper implements these local checks in a compatible filesystem; manual agents need no script. No distributed mutex or production action authority is conferred.

## Provenance and governance gates (0.4.0)

Follow [references/PROVENANCE-QUALITY-PERMISSIONS.md](references/PROVENANCE-QUALITY-PERMISSIONS.md) before claiming, reviewing or authorizing a task. Record [Agent | Platform | Role | Instance] in claims, transitions, reviews, handoffs and Git commit trailers when Git is enabled. Use complete exact-version artifact QC, and distinct permission-to-act records. Failed QC creates structured remediation and blocks dependents, not unrelated siblings. Every external consequential action requires an authenticated host/provider authority **in addition** to cooperative JSON approval. A file declaring `role=owner` or a caller-set `context_checked` flag is never a hard security mechanism.

## Optional remote sync and multi-agent coordination (0.5.0)

Only when Git is enabled: read `agent-files/config/sync.json`, confirm actual remote reachability, check/fetch at session start, before shared-task claims and writes, after checkpoints/pushes, and at handoff. Allow clean fast-forward only; on dirty/diverged history preserve both versions and stop. Shared task work requires a verified claim on its own remote ref using an **explicit expected-old-SHA Git CAS lease**, with separate `[Agent | Platform | Role | Instance]` ownership, token and epoch. Never infer exclusivity from checkout, a worktree, Git user, unverified LFS lock, local claim timestamp or an expired lease. If remote is unavailable, record `sync_pending`/BLOCKED; halt shared mutations and external effects. For the full no-helper procedure read `references/GIT-SYNC-AND-COORDINATION.md`. No Git is needed in standalone mode.


## Optional workflow visualization, version 0.8.0

On a user request or at an authorized checkpoint, an agent may derive a visual **read-only** snapshot from a template or exact pinned graph plus selected run state. Read references/VISUALIZATION.md and spec/schemas/visualization-snapshot.schema.json. Generate agent-files/visualizations/<safe-view-id>/index.html by inserting correctly escaped snapshot JSON in protected references/visualization-viewer.html. Show each graph dependency arrow, exact step instructions, saved QA, retries and evidence; distinguish real event-derived progress from an advisory state snapshot and never claim provider readback. Visualization generation is not a workflow task execution, reviewer approval or permission to act. If local browser rendering is unsupported, provide the file; suggest public GitHub Pages only on user opt-in with separately sanitized export, never expose raw agent-files.


### Visualization delivery rule (v0.8.2)

**HTML FIRST.** Once the agent creates a visualization, prioritize showing its self-contained index.html directly in the host's HTML/browser preview, or give a verified link/attachment to the individual HTML page. Do not lead with a ZIP archive of a single diagram. Only use ZIP when platform-forced, specifically requested or genuinely multi-file, with instructions to open index.html. Public hosting via GitHub Pages is optional and needs explicit approval and sanitization. This does not alter the ZIP required to install the multi-file AOS-W framework.
