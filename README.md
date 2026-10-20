# Agent OS Workflows (AOS-W)

AOS-W is a planned portable, file-based framework for repeatable, auditable AI-agent workflows. It is designed for one agent on a local or persistent cloud filesystem, with optional Git synchronization and multi-agent coordination. No Git installation, dedicated MCP server, database, Python runtime, or scheduler is required for the standalone design.

> **Status: first portable scaffold implemented (Prompt 09), manually operated only.** [Start with the self-contained scaffold](scaffold/aos-w/README.md). Templates, 16 draft schemas, instructions and a safe sample run are present. No automatic workflow engine, distributed lock or scheduler has been implemented.

## Planned distribution

The installable directory is [scaffold/aos-w/](scaffold/aos-w/). Copy it from the repository's ZIP into any persistent local/cloud folder, or use the optional packaging script to create a scaffold-only ZIP. It works manually without a Git checkout.

Only `scaffold/aos-w/agent-files/` is intended to change during ordinary installed-framework use. It will contain project-specific configuration, customized templates, active runs, evidence, reviews, state, and history. Framework maintainers may update the standardized scaffold outside this area through explicit releases.

## Development repository

- `docs/` — product and technical specifications as they are approved.
- `examples/` — sanitized reference examples.
- `scripts/` and `tools/` — optional utilities, not mandatory dependencies.
- `scaffold/` — future downloadable AOS-W distribution.
- `temp/` — **tracked**, public work-in-progress documentation, decisions, research, plans, progress, and cross-session handoffs.

Start with [temp/OPERATING-RULES.md](temp/OPERATING-RULES.md) and [temp/HANDOFF.md](temp/HANDOFF.md) when continuing the project. See [temp/DESIGN-DECISIONS.md](temp/DESIGN-DECISIONS.md) for the baseline requirements.

## Principles

1. Offline or cloud standalone first, Git optional.
2. Multi-agent execution optional, but supported when safe shared coordination is available.
3. Modular reusable templates, composed workflows, dependency gates, state, retries, recovery, evidence, and audit trails.
4. Non-repeating workflows by default, with optional schedule-triggered recurring instances. A template may provide a default schedule, while any permitted workflow can also be launched ad hoc. Scheduling must not require an always-on AOS-W runtime.
5. Skills can be bundled with templates and workflow instances or referenced from installed/local/repository skill locations. Steps identify needed skills and agents load them when relevant.
6. Explicit identity and permission boundaries. Quality review is not itself authorization for external side effects.
7. Model-agnostic interfaces. Integration with A Rep, not dependence on A Rep.
8. No credentials, customer secrets, private customer information, or unsanitized business records in this public repository.

## Roadmap

Prompts 02–06 researched Ampgent processes, A Rep, LangGraph and collaboration. Prompt 07 produced the PRD; Prompt 08 produced [technical specifications](docs/specs/architecture/) and [draft schemas](docs/specs/schemas/). **Prompt 09 is the initial file-based scaffold implementation.** Later prompts will implement graph execution, durable automated recovery, permissions, Git coordination and full Ampgent templates, followed by tests. The user explicitly directed Prompt 09 implementation; this does **not** approve production account actions or automatically accept all draft ADRs.

## Licensing

No open-source license has been selected yet. Public repository visibility does not itself grant reuse rights. Licensing is an unresolved decision to record during requirements review.
