# A Rep, Fred and Max compatibility analysis

All references A01–A15 in [SOURCES-06.md](SOURCES-06.md). **Source-derived** facts are labelled S; **proposals** labelled P.

## Existing roles and mechanisms

**S.** A Rep describes a persistent goal-driven **PRIMARY** with judgment, not an enforced deterministic task graph. Cold-start recovery reads current authority/context/work/issues, approved skills, runtime and real external evidence. Agent source can change among Codex/OpenCode/Claude without continuity resting in one model session. The existing A Rep event/heartbeat watcher and local flock belong to that host runtime only. [A01/A03/A04]

**S.** Fred is a live/private A Rep PRIMARY using GitHub Issues and the local runtime. Max intentionally has no runtime/watcher/heartbeat and is invoked manually while retaining marketing decisions and artifacts. **This difference proves a portable workflow should not presume always-running PRIMARY or a certain cloud provider.** [A10/A14]

**S.** A Rep permits only one mutating PRIMARY of its authoritative *agent-level* state. Workers may perform bounded delegated activity with documented handoffs; Guardian review is advisory, not another PRIMARY. Producer provenance `[Agent | Platform | Role | Instance]` and `Agent-Run` distinguish agents despite shared GitHub credentials and identify **producer, not approver**. [A04/A06]

**S.** Experimental skills are under `scratch/skills`, while promoted approved skills live in `procedures/skills` after review and human approval. Skill instructions are not new authority; specialized tools/helpers are optional. [A05/A10/A14]

**S.** A Rep V1.5 optional `plan-work` uses `work/plans/<id>/PLAN.md` (current authoritative header) and `EVENTS.md` (chronological record), with derived/rebuildable `INDEX.md`. States `READY`, `RUNNING`, `WAIT_UNTIL`, `WAIT_EVENT`, `WAIT_HUMAN`, `WAIT_GUARDIAN`, `BLOCKED`, `COMPLETE`, `CANCELLED` are recovery vocabulary, not graph execution. [A02/A08]

**S.** `data-ledger` has provider truth, business truth and agent working/audit state. It uses `snapshot.csv`, `events.csv` with `event_id` de-dup, and derived index. Neither the plan nor ledger permits external actions beyond existing authority. [A02/A09]

**S.** Fred issue 90 is an actual plan/example. It preserved blind first-pass scoring, fresh source recheck and a later completed follow-up without retroactively modifying original ranking. This resembles scoped AOS-W versioned QC and resumable steps. [A11]

## Avoid two competing agents or plans

**P.** AOS-W should own only **workflow template, instance, task dependency, step-gate and workflow state**. A Rep owns **persistent agent identity, prioritization, global work issue radar, wake and authority context**. If an A Rep work item launches an AOS-W workflow, put an optional lightweight pointer from A Rep Issue/plan to AOS-W run; do not double-maintain an authoritative plan with copied statuses. AOS-W provides a derived summary/backlink and events; plan-work remains useful for goals outside formal workflows.

**P.** The A Rep full repo is **not** an AOS-W installation prerequisite. A manually running Max/ChatGPT, a local agent on a laptop or a cloud agent may read standalone `aos-w/` and checkpoint work directly. An A Rep-driven host may additionally wake a task, apply protected business rules and link its work Issue.

**P.** Task-level exclusive claims within AOS-W do not conflict with A Rep's one PRIMARY rule, provided agent-level authority remains with PRIMARY and bounded worker claims never create new rights. An A Rep Guardian may serve as independent reviewer where permitted without becoming workflow owner.

**P.** Treat existing A Rep and AOS-W statuses as **different layers**, map only explicit limited states and never assume `PLAN.md` or `EVENTS.md` can be machine-enforced in an unmodified agent harness.

## Compatibility requirements for PRD

1. Four-field producer identity, run correlation, source/rubric/artifact revisions and human approval recorded distinctly.
2. `source_of_truth` must identify external provider and optional A Rep issue/plan references; current provider facts outrank workflow cache for provider-owned fields.
3. Fresh-agent recovery instructions, no dependency on prior chat context, current read-only artifact indexes reconstructable from base per-run events.
4. Skills may use the Agent Skills `SKILL.md` convention, with trust/approved/exploratory state and read-on-demand behavior. Promotion remains governed by owning environment.
5. No automatic A Rep scheduler or Fred runtime dependency. AOS-W can be driven by Max manually or Fred/other host when explicitly configured.
6. Preserve existing A Rep authority hierarchy, never infer external account permission from a task claim, lock, QC pass, skill, GitHub write access or review.
