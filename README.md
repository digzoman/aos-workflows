# Agent OS Workflows (AOS-W)

AOS-W is a planned portable, file-based framework for repeatable, auditable AI-agent workflows. It is designed for one agent on a local or persistent cloud filesystem, with optional Git synchronization and multi-agent coordination. No Git installation, dedicated MCP server, database, Python runtime, or scheduler is required for the standalone design.

> **Status: portable AOS-W 0.6.0 scaffold and optional helper tooling.** [Read the standalone quick start](docs/installation/QUICKSTART.md) or [explore the scaffold](scaffold/aos-w/README.md). The portable release ships **20 draft schemas**, instructions, templates and clean starter data; automatic workflow dispatch, a live scheduler and production distributed locking are not implemented.

## Downloadable distribution and optional tools

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

## Prompt 10, reusable composition (0.2.0)

The [composition protocol](scaffold/aos-w/references/COMPOSITION.md) and [planning/competitor templates](scaffold/aos-w/templates/README.md) now support explicit task contracts, dependency routing, custom overlays, stable child proposals, independent research QC and reviewed portfolio merging. An [optional PyYAML helper](tools/composition/README.md) implements local checks and approval-gated child instantiation, with [sanitized fixtures](examples/conformance/README.md) and unit tests. **No Python or Git is mandatory for file-only operation.** Automatic task dispatch, enforced multi-agent claims and external provider APIs are not implemented.

## Prompt 11 — durable run state (0.3.0)

The [manual state/recovery protocol](scaffold/aos-w/references/STATE-AND-RECOVERY.md) now specifies append-oriented event history, checkpoints, retries, paused/failed runs, evidence integrity, provider-action intent reconciliation and fresh-agent recovery. The [optional deterministic helper](tools/state/README.md) implements and locally tests these operations under a **single-writer** assumption; 26 new tests and 11 composition regressions passed. Real provider writes, hard distributed locks, unattended timers and cryptographic human authorization are **not implemented**. All ordinary installed-workflow modifications remain under `agent-files/`.

## Prompt 12 — governance (0.4.0)

The [portable manual governance protocol](scaffold/aos-w/references/PROVENANCE-QUALITY-PERMISSIONS.md) and [optional local checker](tools/governance/README.md) now support four-field provenance, advisory claims/handoffs, deterministic/independent AI/human/permitted self-review, structured corrections, explicit resource and budget permissions, expiry and revocation. **File records are not authenticated host permission; no provider operations occur.** [Conformance report](temp/tests/PROMPT-12-GOVERNANCE-CONFORMANCE.md).

## Prompt 14: tested clean ZIP and upgrades (0.6.0)

The [installation guide](docs/installation/QUICKSTART.md) and [standalone manual guide](scaffold/aos-w/references/INSTALL.md) describe the clean downloadable `aos-w-portable-0.6.0.zip`. [GitHub Actions](.github/workflows/aosw-portable.yml) builds, verifies and uploads an independent ZIP; the [verified v0.6.0 preview release](https://github.com/digzoman/aos-workflows/releases/tag/v0.6.0-portable-preview) is now publicly available. The [optional maintainer packager](scripts/aosw-distribution.py) creates SHA-256-verified allowlisted ZIPs, installs into arbitrary working directories and stages upgrades that preserve existing `agent-files/` byte for byte, with a rollback backup. The [optional workflow quickstarter](scripts/aosw-ops.py) discovers templates, inspects saved work (advisory) and initializes a pinned, CREATED run with zero provider effects. **108 local tests passed (18 new + 90 regression)**. This is still a file-based/manual core with no mandatory scripting runtime or Git. See [conformance report](temp/tests/PROMPT-14-DISTRIBUTION.md).

**Verified direct download:** [aos-w-portable-0.6.0.zip](https://github.com/digzoman/aos-workflows/releases/download/v0.6.0-portable-preview/aos-w-portable-0.6.0.zip) · SHA256 `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`. Hosted [CI run](https://github.com/digzoman/aos-workflows/actions/runs/39415147383) passed 108 tests, clean installation, workflow initialization and agent-files-preserving upgrade.

## Prompt 16 — practical offline acceptance on standalone v0.6.0

Thirteen [real local file-based acceptance scenarios](docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md) passed against the verified 0.6.0 download. These include a research run deliberately interrupted mid-step, then completed by a new OS process using only persisted files; local custom templates, failed QC with correction, retries, revision, cancel, corrupt-tail recovery and no changes outside `agent-files`. One separate persistent cloud filesystem test remains **NOT RUN**. This is not evidence of real cross-platform AI model handoff, live provider integration, or production shared locking. The prior Prompt 15 marketing library was unpublished at the start of this acceptance run and needs a distinct commit/test.
