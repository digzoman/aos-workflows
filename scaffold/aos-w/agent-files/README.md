# agent-files — the ONLY normally writable installed area

**All runtime/user-specific changes go here.** The remainder of `aos-w/` is standardized framework content, intentionally replaceable during an explicit upgrade. Your agent must not modify `../templates/`, `../spec/`, `../references/`, `../VERSION.json` or `../PROTOCOL.md` during an ordinary run.

## Writable directories

| Path | Contains |
|---|---|
| `config/settings.json` | General local autonomy/single-writer settings and privacy hints |
| `config/capabilities.json` | Observed (or unverified) host capability status; not proof of itself |
| `config/sync.json` | Optional remote Git sync configuration; **disabled by default**, credentials never here |
| `custom-templates/<id>/` | User-owned templates/overlays, including skills, stored here rather than modifying master templates |
| `instances/<id>/` | Pinned effective template snapshots, graph revisions, instance config and individual run directories |
| `indexes/` | Rebuildable summaries; never current authority over a run |
| `cache/` | Rebuildable local cache without secrets |
| `coordination/` | Optional coordination metadata, not a lock merely because a file exists |

A pre-seeded **practice** instance `demo-local-research/` shows this layout with no work performed. New user instances are created **only when needed** and own `instance.json`, `template-lock.json`, `template-snapshots/`, `graph-revisions/`, `skills/`, and `runs/<run-id>/`. Each run owns `run.json`, `events.jsonl`, `state.json`, `checkpoints/`, `tasks/<task-id>/attempts/`, `claims/`, `reviews/`, `approvals/`, `artifacts/`, `skills/`, and `handoff.md`. Empty directories cannot be committed to Git; the agent **creates them at instantiation**, not by writing under protected framework folders.

See `instances/README.md` and `../references/INSTANCE-LAYOUT.md` for exact paths and examples.

## Manual operating rule

1. Look for previously saved work in `instances/` before creating a new run. Read handoff, event prefix, pinned graph revision and current state.
2. Use one active writer unless an actual, tested coordination backend is configured. A claim file alone is advisory.
3. Save the exact state and evidence before ending every session. If uncertain, record BLOCKED or RECONCILE_REQUIRED, not fabricated completion.
4. Keep secrets and sensitive provider/customer data out of **public Git**. This folder may be user-private locally; mirroring it into a public repository is a **separate privacy decision**.
5. A new installed framework release may replace standardized files **only after backing up this folder**. Never let an upgrade overwrite this directory.

## What counts as a working feature

An agent following `../PROTOCOL.md` can **manually** start a new instance, identify dependencies and save auditable files. Automatic task scheduling, enforced multi-agent leases, provider integrations, schema validation runtime and crash-atomic file transactions are **not implemented** by this folder.

## Version 0.3.0 state and recovery

Persist the actor-bound event journal and immutable graph revision under each run. Before resuming after interruption, reconcile `events.jsonl`, `state.json`, checkpoints, attempt records, actual artifacts and pending provider operation identities. The portable manual procedure is [STATE-AND-RECOVERY.md](../references/STATE-AND-RECOVERY.md). Local snapshot files may be regenerated; accepted history must not be silently rewritten. Only explicit repair quarantines a corrupt tail and retains all previously accepted event bytes. All such changes stay **inside agent-files**. There is no automatic timer or distributed mutex.

## Prompt 12 append-only governance records

Runs may create `claims/`, `reviews/`, `approvals/` and `handoffs/` records under this writable subtree. Append meaningful changes to `events.jsonl` and rebuild `state.json` from the verified event prefix. Owner/reviewer names are declared metadata, not authenticated permission; claims are advisory without a coordinator. Consult [the governance reference](../references/PROVENANCE-QUALITY-PERMISSIONS.md) and keep normal writes only under `agent-files`.

## Optional Git synchronization (0.5.0)

`config/sync.json` stores **configuration**, while `config/sync-state.json` stores the last actually observed sync attempt/result. Both belong to user-owned agent-files; no credentials are stored in either. If Git is not configured, mode remains standalone. In `shared_coordinated` mode, verified remote per-task claims must be obtained **before** modifying shared artifacts; no CAS connectivity means BLOCKED, not fallback to an expired local claim. Keep evidence and handoff records honest; remote commit and Git identity are separate from agent provenance and action approvals. See `../references/GIT-SYNC-AND-COORDINATION.md`.


## Version 0.8.0 user-owned visualizations

Use [visualizations/README.md](visualizations/README.md) to save generated offline read-only workflow pages. A view consists of visualizations/<view-id>/index.html plus an optional snapshot.json projection. It may show a template or a pinned graph with a saved run status. This is an **advisory snapshot**, not workflow authority or live provider truth. No generated file belongs outside agent-files; the protected HTML skeleton lives in ../references/visualization-viewer.html and normal agents must copy it rather than editing it. GitHub Pages is a separate public export requiring explicit permission and sanitization.
