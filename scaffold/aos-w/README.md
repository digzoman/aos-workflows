# Agent OS Workflows — portable starter (0.2.0)

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

This is a foundation for future Prompts 11–19, not the fully tested Version 1 release.
