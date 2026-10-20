# Installation and upgrade: standalone AOS-W 0.6.0

The **complete** standalone AOS-W release archive contains an `aos-w/` folder. Unzip and copy `aos-w/` into any persistent directory. A capable agent can read `README.md`, `PROTOCOL.md`, this document and `references/START-A-RUN.md` to begin work without Git, Python, scripts, a server or a scheduler.

## Clean installation

1. Choose a persistent local/cloud directory (confirm data survives between sessions).
2. Extract the separately downloadable `aos-w-portable-0.6.0.zip`, retaining the `aos-w/` directory. It includes standardized guides, master templates, bundled skills, schemas, integrity manifest and an empty, writable `agent-files/` starter tree.
3. Read `aos-w/README.md` and `aos-w/PROTOCOL.md` before starting.
4. Instruct your agent: **"Read AOS-W rules and saved work; list available master and custom templates; start a one-off manual instance of research-starter with my question, and show me the next eligible step. Do not perform external actions."**
5. New user work goes only in `agent-files/instances/` or `agent-files/custom-templates/`. Never edit protected master templates during a normal run. Do not infer human approval from a skill or local JSON.

The release ZIP intentionally **does not bundle** the development repository, development scripts, tests, temp research, prior active workflows or private records. The development repo's pre-seeded practice instance is also intentionally excluded from the **clean distribution**; this is not a missing workflow engine.

## Upgrading an existing installation

Never blindly unzip a new distribution over `aos-w/` because it might overwrite `agent-files/`. Take a complete backup, then replace protected standardized files/directories only: root README/PROTOCOL/VERSION, `spec/`, `references/` and `templates/`. Retain all existing `agent-files/` content **unchanged**: config, custom templates, pinned instances, run history, reviews, approvals, skills and checkpoints. Verify compatibility of pinned templates and schema major version before resuming. Keep a rollback copy of the old installation until satisfied.

If a host has optional Python, the developer repository provides `scripts/aosw-distribution.py install|upgrade` to verify SHA256 manifest and stage an upgrade with a backup. Python is **not installed in or required by this ZIP**; this is only an optional convenience. The upgrade cannot guarantee durability on arbitrary networked filesystems and is not a distributed transaction.

## Equivalent manual operating procedure

- **Find templates:** read `templates/README.md`, `templates/<id>/template.yaml` and `agent-files/custom-templates/`.
- **Start a workflow:** create a new instance ID and pin resolved template bytes in `agent-files/instances/<id>/template-snapshots/`, copy a graph revision, write `instance.json`, `template-lock.json`, and create a run with initial `run.json`, `events.jsonl`, derived `state.json`, task folders and `handoff.md`. See `references/START-A-RUN.md`.
- **Resume safely:** read saved events, pinned graph and last checkpoint. Reconcile stale snapshots, current evidence, retries, ownership and any unknown provider effects. Do not blindly replay external operations.
- **Claim, review and approve:** follow `references/PROVENANCE-QUALITY-PERMISSIONS.md`. A local claim is advisory; a QC PASS does not grant external permission.
- **Checkpoint/recover:** follow `references/STATE-AND-RECOVERY.md` with an agent; record uncertainty rather than fabricating hashes or observed provider status.
- **Optional Git:** follow `references/GIT-SYNC-AND-COORDINATION.md`; no Git is needed for standalone one-agent work.

Neither copying nor the optional init helper automatically dispatches tasks, schedules workflows, authenticates a human reviewer, or publishes ads. Shared Git ref CAS remains provisional pending hosted remote tests.
