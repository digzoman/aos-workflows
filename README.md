# Agent OS Workflows (AOS-W)

AOS-W is a planned portable, file-based framework for repeatable, auditable AI-agent workflows. It is designed for one agent on a local or persistent cloud filesystem, with optional Git synchronization and multi-agent coordination. No Git installation, dedicated MCP server, database, Python runtime, or scheduler is required for the standalone design.

> **Status: PRD drafted, awaiting owner approval.** The comprehensive [AOS-W Version 1 PRD](docs/specs/prd/PRD.md) and its [review documents](docs/specs/prd/README.md) are committed for human review. No workflow engine, lock mechanism or scheduler has been implemented or claimed to work yet.

## Planned distribution

The installable directory will live at `scaffold/aos-w/`. Users will be able to copy or download that directory into an arbitrary working folder.

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

Historical workflow and architecture research stages (Prompts 02–06) are complete, with sanitized results in tracked `temp/research/` and `temp/architecture/`. **The current step is owner review of the Prompt 07 enhanced PRD.** Prompt 08 implementation remains blocked until explicit approval. Draft architecture decision records are not yet approved.

## Licensing

No open-source license has been selected yet. Public repository visibility does not itself grant reuse rights. Licensing is an unresolved decision to record during requirements review.
