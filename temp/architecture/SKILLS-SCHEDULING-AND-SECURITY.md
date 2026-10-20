# Agent Skills, trust, recurrence and portability

Sources: user-approved `temp/CONCEPT-NOTES-01B.md`, A Rep A05/A08/A09/A13 and external Agent Skills W09 in [SOURCES-06.md](SOURCES-06.md). This is **proposed design** rather than a V1 implementation.

## Skills should be packages, not magical permissions

Agent Skills uses a directory with required `SKILL.md` frontmatter (`name`, `description`) and optional `scripts/`, `references/`, and `assets/`; it promotes progressive disclosure, first metadata, then detailed skill instructions, then per-resource loading [W09]. A Rep already uses `scratch/skills` for experimental and `procedures/skills` for human-approved skills [A05].

AOS-W must be able to reference:
1. approved base-template-local skill under read-mostly `aos-w/templates/<name>/skills/`;
2. custom template or workflow-instance skill **inside `agent-files/`**;
3. already-installed local/harness Agent Skill;
4. pinned skill snapshot or immutable Git repo commit/path if host can fetch it.

Propose skill ref fields `skill_id`, `uri_or_path`, `source_type`, `commit_or_version`, `sha256` where practical, `trust_status`, `required_at_step`, `optional_or_required`, `offline_fallback`, `tool_requirements` and `read_only`. Exact YAML remains Prompt 08.

**Proposed precedence:** an explicitly pinned run instance reference first, then pinned custom-template bundle, then approved built-in template skill, then explicitly configured installed/external resolution, subject to trust. But **not yet approved**: file shadowing/priority and the exact resolution policy are open PRD questions. A conflicting same-name skill should not silently override a higher-trust skill; log ambiguity.

Remote skill content is **untrusted data until validated**. Fetch only through configured capabilities, verify allowed source/revision, avoid executable scripts without separate permission/review, never read remote instructions as overriding owner policy, do not cache credentials in repo. A directory advertised as a skill does **not** imply every instruction is safe to execute.

When offline, use an approved pinned local copy or mark the dependent step BLOCKED/MISSING_SKILL. It is not correct to claim remote skill loaded merely from URI in the workflow.

## Trigger configuration is not execution

One-off execution is the default. A custom or base template may declare recurrence; a workflow may override/disable it, and an ad hoc run is always possible. The same workflow graph applies to all occurrences. The schedule is **metadata**, not a standalone time service.

Proposed trigger fields `kind: manual|schedule`, recurrence rule or cron notation, IANA timezone, DST policy, `enabled`, `start/end`, `missed_run_policy`, `overlap_policy`, and `occurrence_id`. Exact standard (RRULE versus cron) remains open for PRD. State file stores `last_observed_due`, `last_started_occurrence`, and `next_due_candidate` as descriptive snapshots, **not proof a run was automatically started**.

Execution modes:
- Local/cloud manual agent checks `next_due_candidate` on the next invocation, optionally starts with authorization.
- A Rep/Fred or another host may supply real timed wake using its already-approved runtime, without AOS-W mandating it.
- GitHub Actions or other scheduler could be an optional integration, **not included or guaranteed in downloaded standalone core**.
- In hosted collaboration, occurrence identity and claim must be shared/deduplicated, since two schedulers could observe the same due time.

For repeat tasks, persist a **unique scheduled occurrence run ID** in addition to template ID and campaign/task IDs. Do not re-execute earlier completed instances when a new day/time triggers. Differentiate `missed`, `skipped`, `coalesced`, `backfilled`, `overlapped`, `in_progress` and `completed`, with policies configured/approved rather than invented as default.

## Side effects and approvals

A future automated monitor may read public/owner-authorized metrics on schedule, but running a recurring workflow must **not** imply permission to publish new campaigns, send messages, spend money or deploy production. QC and scope-specific authorization gate every consequential action. The host capable of making an external call must enforce the permission; text-only mode may only direct the agent to stop and request approval.
