# Agent OS Workflows — portable starter (0.6.0)

**Status:** Initial **file-based scaffold**, not a workflow execution engine. It is usable as an instruction-driven, **single-writer, manually operated** workflow folder. Automatic graph execution, distributed locks, time-triggered runs, provider integration and validators are later milestones.

## Start here (no installed software required)

1. Place this entire `aos-w/` folder in any **persistent** local or cloud working directory. Copying only this directory is sufficient; the outer development repository is not needed.
2. Give your AI agent the instruction: **"Read aos-w/README.md, PROTOCOL.md and agent-files/README.md. Show the built-in templates and any saved instances, then recommend the next safe eligible step. Follow the no-scripts manual protocol."**
3. Open [templates/README.md](templates/README.md) and select [research-starter](templates/research-starter/README.md) for a safe, non-commercial practice workflow.
4. The agent creates a **new** `agent-files/instances/<id>/` directory, pins a copy of the selected template and the graph revision, then creates a unique run under `runs/<run-id>/`. See [references/START-A-RUN.md](references/START-A-RUN.md).
5. Work from the **pinned graph**, not a potentially changed master template. Choose a READY step only after checking dependencies, current scope, skills, quality gates and any pending provider uncertainty.
6. Record each attempt and result under the run. At each checkpoint, update `events.jsonl`, `state.json`, checkpoint and `handoff.md`. On restart, inspect those records before continuing.

Only `agent-files/` may normally be modified. The installed `README.md`, `PROTOCOL.md`, `VERSION.json`, `spec/`, `templates/` and `references/` are protected **by convention**; without optional host-enforced filesystem permissions this is not a technical sandbox.

## Composition and reusable research workflows

See [references/COMPOSITION.md](references/COMPOSITION.md) for the portable conventions for master and custom templates, dependency/condition eligibility, approved child-generation, independent investigation reviews, all-accepted merging, and revision impact. New protected templates include `competitor-investigation`, `research-portfolio-planner` and `research-portfolio-compound`. An **optional**, separately installed PyYAML helper under the development repository's `tools/composition/` can check graphs and create approved local child instances. This helper is not included as a dependency of the downloadable scaffold.

The original synthetic `demo-local-research` run stays pinned to the **0.1.0** master snapshot; the current `research-starter` master is **0.2.0**. Do not rewrite an existing pinned workflow when the master changes.

## Durable state and recovery (0.3.0)

Use [references/STATE-AND-RECOVERY.md](references/STATE-AND-RECOVERY.md) to persist event history, task attempts, owners, evidence, checkpoints, bounded retries, pauses/cancellations, interrupted-work handoffs, controlled graph revisions and external operation uncertainty. A second agent can resume using the pinned graph and validated files without previous conversation memory. The development repo's **optional** [tools/state/](../../tools/state/) Python helper demonstrates deterministic local replay/checkpoints/corrupt-tail quarantine; **no Python is required** for the installed file-only protocol. It never calls Meta, GHL, websites or any provider, and it does not enforce shared distributed claims.

## Agent provenance, QC and permissions (0.4.0)

Read [the manual governance protocol](references/PROVENANCE-QUALITY-PERMISSIONS.md) for four-field actor identity, advisory claims and handoffs, configurable workflow/step quality gates, remediation, waiver, and separate time/resource/version-limited approvals. The [optional local governance checker](../../tools/governance/README.md) validates those records and event history, but **does not authenticate owners, enforce shared locks or perform external provider actions**. File-only operation still needs no Python.

## Optional Git synchronization and shared work (0.5.0)

Standalone use remains Git-free. If your workspace explicitly configures Git, follow [GIT-SYNC-AND-COORDINATION.md](references/GIT-SYNC-AND-COORDINATION.md) for remote checks, fast-forward-only refresh, commit/push verification, and per-task claims. The optional [developer Git helper](../../tools/git/README.md) implements explicit expected-old-SHA remote ref CAS and a Git LFS lock prototype. Git CAS won **local bare-remote** competition tests with separate agents using the same Git login; hosted GitHub transport and live Git LFS locking are **not yet verified**. Shared mode **fails closed** if the remote is unreachable. Git is never mandatory, and claims do not grant external action authority.

## Download and safe upgrade (0.6.0)

[Installation guide](references/INSTALL.md): extract the standalone `aos-w/` ZIP into any persistent work folder. It contains only protected framework files plus **clean starter** `agent-files/` configuration and empty runtime folders. Unlike the public development repository, **the ZIP excludes the synthetic practice instance and any private user data**. For an upgrade **back up and preserve the entire existing `agent-files/`** while replacing only protected paths. The optional, separately hosted distribution checker verifies the ZIP's SHA-256 manifest and stages upgrades with rollback backups. It is not a runtime requirement.

## What comes in this directory

| Path | Use | May an executing agent normally edit it? |
|---|---|---|
| `PROTOCOL.md` | Operational instructions, eligibility, checkpoint and handoff | **No** |
| `VERSION.json` | Framework/protocol compatibility | **No** |
| `spec/` | Self-contained human specifications and 16 draft JSON Schemas | **No** |
| `templates/` | Discoverable read-only master templates and bundled skills | **No** |
| `references/` | Walkthroughs and safe usage examples | **No** |
| `agent-files/` | Config, custom templates, instances/runs, logs, evidence and reviews | **Yes**, within owner policy |

## Trust and execution limits

- A workflow definition is **instructions and declared dependencies**, not self-executing software. A capable agent follows it when asked.
- Without a proven coordination adapter, task ownership is **advisory**. Use **one active writer**. Do not promise multi-agent collision prevention from claim files.
- Git, Git LFS, Python, Node, a database, cloud server and MCP are **not required**. Optional Git is configured in `agent-files/config/sync.json`; it is disabled by default.
- Schedules are **declarative**. A recurring-capable template can be invoked manually; no background schedule is included.
- Skills are loaded **only when relevant** and can never create new access privileges.
- Quality approval and permission to publish, spend, send, deploy, or write external systems are **separate**. The starter template operates only on local, nonconfidential test data.
- A successful file edit is **not proof** that a live external service was changed. Do not place secrets or customer data in the public development repository.

## Upgrading without losing work

Treat an installed release's `agent-files/` as user-owned. To upgrade, **back up the whole folder**, replace only standardized files from a newer `aos-w/` distribution, and keep the existing `agent-files/` unchanged. Verify version/schema compatibility and old pinned snapshots before resuming. Do **not** copy a fresh distribution over `agent-files/` or delete it with the old framework directory. Detailed procedure: [references/UPGRADE-AND-PORTABILITY.md](references/UPGRADE-AND-PORTABILITY.md).

## Restart prompt for a new AI session

> Read `aos-w/README.md`, `aos-w/PROTOCOL.md`, `aos-w/agent-files/README.md`, and saved `handoff.md`. Discover instances under `agent-files/instances/`. Validate the selected run's pinned template, `events.jsonl` and `state.json`; report any inconsistencies, blockers, approval requirements or unknown external effects. Identify the **next eligible bounded step** and ask before actions requiring approval. Never infer completion from chat memory or merely from a plan.

This is a foundation for future Prompts 15–19, not the fully tested Version 1 release.
