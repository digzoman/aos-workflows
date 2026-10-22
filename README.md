## v0.9.1 — human-first workflow coordination (preview)

Current release: [AOS-W v0.9.1 portable preview](https://github.com/digzoman/aos-workflows/releases/tag/v0.9.1-portable-preview). Agents should use the included AGENTS.md entry point and the new human-first workflow viewer, status-aware review counts, portable step briefs, and capability-recovery guidance. A declared missing tool is not a reason to refuse, invent an owner approval gate, or stop safe parallel work. Private production snapshots must not be published automatically to public GitHub Pages; an opt-in **fictional** sanitized demo is prepared. Original stable V1 acceptance T01–T04 remains open.

# AOS-W v0.8.2 Workflow Visualization

**Current preview:** [v0.8.2 portable release](https://github.com/digzoman/aos-workflows/releases/tag/v0.8.2-portable-preview). This additive release includes a protected offline interactive HTML/SVG viewer, an optional generator, visualization snapshot schema, safe agent-files/visualizations output location, a sanitized sample and a new design spec. It is **not stable Version 1**. Previous four original V1 acceptance demonstrations remain pending. See [v0.8 visualization specification](docs/specs/visualization/V0.8-SPEC.md), [portable viewer guide](scaffold/aos-w/references/VISUALIZATION.md) and [Bucket 9 example](examples/visualization/bucket9-stage.json).

# Agent OS Workflows, AOS-W

AOS-W is a **portable, file-based workflow standard** for AI agents. It provides repeatable tasks, reusable template contracts, evidence tracking, checkpoints, handoffs and manual protocols. Its downloaded core does not require Git, Python, an MCP server, a database or a scheduler. Optional helper tooling adds local deterministic validation, file state management and experimental Git synchronization.

**Earlier release status, October 20, 2026.** The [0.7.0 portable preview](https://github.com/digzoman/aos-workflows/releases/tag/v0.7.0-portable-preview) is available and tested. **The original six Version 1 success criteria are not all demonstrated, and stable Version 1 is not approved or published.** See the [release approval packet](docs/release/V1-RELEASE-APPROVAL-PACKET.md), [full requirement traceability](docs/release/V1-REQUIREMENTS-MATRIX.md), and [limitations](docs/release/V1-LIMITATIONS-AND-RISKS.md).

## Download and start

Follow the [0.7.0 quick start](docs/installation/QUICKSTART.md). Download the clean aos-w-portable-0.7.0.zip from its [GitHub prerelease](https://github.com/digzoman/aos-workflows/releases/tag/v0.7.0-portable-preview), confirm the published SHA-256 and extract the single aos-w folder into persistent storage. Read aos-w/README.md and PROTOCOL.md, choose a template, then create a pinned instance under aos-w/agent-files.

Ordinary operation may write only within **aos-w/agent-files**. The protected file protocol includes templates, specification schemas, skills and reference instructions. Only the optional maintainer upgrade changes the protected standardized part while preserving the user data subtree.

## Available templates and optional tools

The portable preview includes 21 standalone marketing modules plus one compound research-through-staged-campaign workflow. See scaffold/aos-w/templates/MARKETING-LIBRARY.md and scaffold/aos-w/references/MARKETING-WORKFLOWS.md. The development repository also includes optional tools/composition, tools/state, tools/governance and tools/git, plus audited packaging and installation utilities under scripts.

Its task graph, quality gates, autonomy and external-action approvals are documented, but plain files do not themselves enforce a live scheduler, hard cross-process mutex, authenticated human approval or external provider side effects. Git CAS remains a prototype, and unattended Meta/GHL publication is not part of the release.

## Tests and documented evidence

- [Hosted V1 release audit](https://github.com/digzoman/aos-workflows/actions/runs/39499859355), 126 unit/conformance tests and 13 standalone practical checks passed on the actual clean 0.7.0 ZIP. A selected current/historical repository secret-pattern and archive-allowlist audit passed. This does not certify all privacy/legal requirements.
- [Prompt 18 source-backed staged marketing pilot](docs/testing/PROMPT-18-END-TO-END-RESULTS.md), 27 passing assertions, three separately persisted children, eight public supplier offer descriptions, rejected/corrected research and a 1080x1350 PNG, blocked publication gate. Not an independently AI-reviewed or actual Meta staging acceptance.
- [Prompt 17 Git collaboration acceptance](docs/testing/PROMPT-17-GIT-COLLABORATION.md), genuine local bare Git and process races passed; the separate hosted GitHub CAS probe was REVIEW_REQUIRED and Git LFS server test BLOCKED.
- [Prompt 16 standalone local acceptance](docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md) includes 13 file-based scenarios. The separate durable cloud filesystem scenario was not run.

Original test requirements and acceptance conditions are in docs/specs/prd/ACCEPTANCE-TEST-MATRIX.md. The original PRD remains formally unapproved, despite later bounded implementation instructions. No live marketing permission is granted by a PRD or file-based approval.

## Repository map

- docs/specs for the original surveyed requirements, PRD, schemas and proposed architecture decisions.
- docs/testing for reproducible test reports, historical conformance and real run evidence.
- docs/release for release assessments, missing evidence, risk and pending owner approval.
- docs/installation for current and historically versioned install/upgrade instructions.
- scaffold/aos-w for the clean installable framework and templates.
- tools and scripts for **optional** developer or host helpers, not inside the minimal ZIP.
- examples for sanitized demonstrations and test fixtures.
- temp for tracked, preserved historical notes, source indexes and handoffs, indexed by docs/history/TEMP-ARCHIVE-INDEX.md.

## Licensing and safety

**No open-source license has been selected.** Public GitHub visibility does not automatically grant reuse rights. Approval to publish an AOS-W release is separate from approval to publish marketing advertisements, spend funds or access customer systems. Live external actions require explicit, authenticated, scoped authority and read-back at the provider boundary.

For current work, read [the release approval packet](docs/release/V1-RELEASE-APPROVAL-PACKET.md) and temp/HANDOFF.md. Verify the current main commit and actual CI results before making changes.


## HTML-first workflow viewing

Agents should display an interactive HTML diagram directly in an available browser/HTML preview or give the individual index.html link/attachment. Do not make users download a ZIP to inspect a workflow if direct HTML is possible. The AOS-W **framework** remains a multi-file ZIP installation. See [HTML-first visualization spec](docs/specs/visualization/V0.8-SPEC.md).

## Working visualization implementation and browser evidence

The [v0.8.1 code and test report](docs/testing/V08-WORKFLOW-VISUALIZATION.md) documents the real browser smoke, one-command verified run visualization, nested SHA-pinned child prompts and interactive HTML. [Open desktop/mobile browser test screenshots](https://github.com/digzoman/aos-workflows/actions/runs/39747505741/artifacts/12411797423). The [0.8.1 preview release](https://github.com/digzoman/aos-workflows/releases/tag/v0.8.1-portable-preview) is the current distribution. Stable V1 acceptance remains pending.
