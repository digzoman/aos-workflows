# Agreed Design Decisions, Baseline for AOS-W V1

Recorded 2026-10-20 from the 16-question interactive/conversational survey and follow-up design changes. These are **user-selected requirements**, not independently validated technical capabilities. Any proposed solution below labeled recommendation is not yet approved.

## Vision, initial scope, and distribution

- All three goals are equally important: a real Ampgent prototype, a reusable portable workflow standard, and reliable collaboration between swappable agents.
- V1 scope includes (1) research planning and keyword discovery, (2) repeatable research execution, (3) independent QC and corrections, (4) evidence synthesis and opportunity scoring, and (5) advertising creative and marketing implementation. Start with a bounded end-to-end pilot; do not treat a full production marketing system as already implemented.
- V1 supports reusable and compound workflows, sequential and parallel execution, dynamically generated research instances, results merging, and conditional paths.
- Public development from the start. Publish only sanitized examples and nonconfidential documentation; keep private project data out of this repo.
- Repository: **`digzoman/aos-workflows`**. Its installable, independently downloadable package is **`scaffold/aos-w/`**.
- The development repo may contain `docs/`, `examples/`, `scripts/`, `tools/`, and tracked `temp/` as necessary.
- Within an installed scaffold, **only `aos-w/agent-files/` may normally change**. Customized templates are also stored there. Include Markdown documentation explaining this boundary.

## Formats, environments, and Git

- Mixed plain-text formats: Markdown instructions and documentation, YAML workflow definitions, JSON or JSONL execution state and history.
- **Git is optional for AOS-W users.** The framework must work directly from a downloaded folder on a local computer or persistent cloud agent filesystem. No Git, dedicated MCP server, database, Python/runtime installation, dashboard, or always-on scheduler is a mandatory dependency.
- Both standalone single-agent use and shared collaborative multi-agent use must be possible; cloud storage and multi-agent execution are separate dimensions.
- Track configured Git synchronization or mirroring in `agent-files/` so agents know when to check/pull updates, verify current remote state, and commit/push completed work.
- Prototype **both Git LFS locking and atomic Git claims** and choose based on tests. Standard Git checkout is not a file lock. Agents sharing credentials require independent identity records.
- Optional helper scripts/tools are allowed so long as core operation remains possible through files and agent instructions.

## Prompt 01b addition, triggering and reusable skills

User-approved requirements added 2026-10-20, subsequent to the original survey.

### One-off and recurring workflow triggers

- **Default execution is non-repeating**, initiated when needed.
- Templates, including master and customized templates, may declare a configurable schedule for recurring launch of a workflow. A caller may override or remove the schedule when creating a workflow.
- A scheduled-capable template **must also support an ad hoc workflow launch**, even if a default schedule exists.
- Repeating is a trigger/execution property, **not the same thing as repeating research steps inside a single workflow**.
- AOS-W must not require its own daemon or scheduler for local standalone installation. The final design must distinguish storing a schedule from having a connected execution environment capable of actually launching work on that schedule.
- Recommended for review, not yet an approved schema: keep each scheduled occurrence as a distinguishable execution run with provenance and checkpoint history. Define scheduling, overlapping occurrences, missed events, timezone and deduplication rules in the PRD.

### Skill packages and just-in-time skill discovery

- **Skills may live within reusable workflow templates and within individual workflow instances themselves**, not only in a separate global library.
- A workflow or step identifies which skill(s) it needs, where they are found, and when agents should consult them.
- Skills may be locally bundled, referenced from previously installed agent skills, or referenced from Git repositories or other supported remote locations.
- Agent instructions should load **relevant skills just in time**, rather than all skills at every start.
- Custom template skills and workflow-instance skills must live inside `agent-files/` during normal installed operation. Approved base-template skills can ship inside standardized, read-only framework template packages.
- For external skills, design must address location, version/pinning, provenance, availability, trust and authorization before allowing any automatic fetch or execution. Referencing a skill never grants extra permissions.
- Specific manifest syntax and fallback/precedence rules are technical design work for PRD and implementation, not yet decided.

## Identity, coordination, and provenance

- Compatible with existing A Rep convention `[Agent | Platform | Role | Instance]`.
- Track identity in task claims, Git commits when used, handoffs, and independent QC and approval records. Tracking every file read is *not* a V1 requirement.
- Ownership is per task, with checkout/start timestamp, expected expiration, progress, recovery, and durable handoff.
- AOS-W is independent of A Rep but integrates and respects existing A Rep authority/skill/plan-work/data-ledger conventions.
- Any different agent should be able to reconstruct a workflow from persistent state and resume without losing history or repeating completed work.

## QC, autonomy, and revisions

- Support automated or objective checks, independent AI reviewer gates, human approval, and self-review for low-risk work.
- QC requirements and approval rules have defaults but are configurable by workflow/step. A future explicitly approved workflow might permit autonomous ad publication after satisfactory gates.
- Each workflow defines autonomy, permissions, and what actions require explicit human authorization. Default is bounded agent autonomy and human authorization for consequential external actions.
- A passed QC review alone does not create authorization to publish, spend money, or mutate production services.
- Dynamic workflow revisions configurable per workflow. Preserve history, completed work, rationale, and affected dependencies; material change policies are configurable.

## Required V1 demonstrations

1. Execute a realistic Ampgent marketing research workflow.
2. Demonstrate genuine handoff between AI platforms where access is available.
3. Prevent conflicting exclusive claims by two agents.
4. Show failed QC blocking dependent work and successful remediation unblocking it.
5. Revise an active workflow without losing historical work.
6. Move an active workflow to another Git repository and resume.

All tests must distinguish live demonstration from simulation or skipped coverage.

## Additional engineering ideas to evaluate, not preapproved implementation

The user specifically requested study of LangGraph ideas such as checkpoints, conditional routing, graph execution, retries, interruptions, and recovery. Research how to express these in portable files and what optional execution infrastructure would be needed. Do not imply unattended automatic retries exist without a running executor.

## Guardrails

- The public repo contains no secret/API key, customer information, private raw conversations, or unsanitized operational exports.
- Prompts 02–06 are historical and architectural research. Prompt 07 drafts the enhanced PRD; a **human approval checkpoint** precedes engine implementation.
- Specific file schemas, lock enforcement method, licensing, and cloud persistence guarantees remain open pending research and approval.

## Prompt 06 external architectural research, NOT new user decisions

The source and tradeoff analysis is in `temp/architecture/`, including eight **PROPOSED** ADRs. These are candidate decisions for Prompt 07 user review. The user-approved baseline above remains unchanged.

- Provisional technical preference, file-first workflow protocol with optional host execution and coordination; do not represent this as approved schema/runtime.
- Provisional technical preference, Git ref CAS claim trial for task-level exclusivity and Git LFS as the required alternative trial. **No winner selected; no two-agent tests performed.**
- Recorded current external-documentation discrepancy: public A Rep CURRENT says 1.5.0 while a-rep/SKILL says 1.5.1. No live Fred installed version verified.
- AOS-W may declare schedules, skills, QA, retries and ownership in files, but a plain text protocol cannot by itself enforce hard claims, run a timer or perform external provider actions.

Explicit owner approval of the enhanced PRD is required before technical implementation or marking any proposed ADR accepted.
