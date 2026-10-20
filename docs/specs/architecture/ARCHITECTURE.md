# System architecture and responsibilities

**Document revision:** architecture-proposal 0.1, October 20, 2026. Source: PRD §§1–17/21–23; user survey Q01–Q16 + Prompt 01b. This document does not mark the PRD approved.

## Invariants

1. `scaffold/aos-w/` is independently downloadable; **no mandatory** Git, Python, JavaScript runtime, database, MCP server, daemon, cloud provider, scheduler or web dashboard.
2. Normal installed workflow work changes **only** `aos-w/agent-files/`; base template and framework changes require an explicit versioned upgrade operation.
3. One workflow vocabulary is shared across local standalone, persistent-cloud standalone, optional Git mirroring and verified multi-agent coordination.
4. The framework stores *intended work*, *observed events*, *QC evidence* and *authorization*. Actual Meta, GHL, website, Git remote and other provider state is authoritative for provider-owned facts.
5. Producer identity uses `[Agent | Platform | Role | Instance]` and never confers permission. AOS-W task orchestration does not replace A Rep PRIMARY, issue radar, plan-work or Guardian authority.
6. QC verification and permission to perform consequential actions are **independent gates**. A workflow may autonomously publish only if a separately scoped standing authority expressly permits it, is current, and all configured QC gates pass.
7. No workflow graph is executed merely because a YAML file exists. A capable agent follows the manual protocol. Automation, hard access checks, atomic claims, clocks and outside service writes require explicitly present optional host capabilities.
8. Read/propose/approve/stage paused/activate/change budget/deploy production/send messages/emit CAPI events are separate action scopes; no implicit escalation.
9. Source content and external skill instructions are untrusted data; only approved policy and tool host authority can authorize execution.
10. Public repo artifacts contain sanitized process examples, not private ad account data, secrets, customer messages or original internal marketing assets.

## Conceptual layers

| Layer | Responsibility | Authority and outputs |
| --- | --- | --- |
| **A. Distribution** | README, protocol and versioned base templates, optional skills/docs | Read-mostly installed scaffold; not active project state |
| **B. Definition** | Reusable base/custom template, fields, DAG, policies, trigger, skills | Template source revision and trust, immutable pin for instance |
| **C. Instance** | Owner's fixed configuration, selected template lineage and graph revision | Resolved template snapshot and immutable selection history |
| **D. Run/occurrence** | One concrete manual/scheduled execution, task attempts, local events/checkpoints, artifacts, reviews, authorization, handoff | Local run evidence; lifecycle reconstructed from validated events |
| **E. Agent host** | Human-guided model or optional adapter that chooses eligible work, verifies tool capabilities, writes files, waits/starts tasks | **Cooperative** in no-adapter mode; host must prove stronger execution properties |
| **F. Coordination adapter** | Optional local filesystem CAS or Git remote atomic claim/lease/fencing | Enforced task exclusivity only after tests; Git LFS vs Git CAS still unresolved |
| **G. Provider adapter** | Optional actual Meta, HighLevel, browser, website, Git and analytics reads/writes | Provider readback authoritative; local ACK not provider-effect truth |
| **H. Reviewer/approver** | Independent QC and human/scoped authorization, dynamic graph approval | QC/PERMISSION separately version-bound; default human gate for consequential external actions |

## Environment capability declaration

A run's `capabilities` maps each feature to `available`, `unavailable` or `unverified`, with `mechanism`, `verified_at` and evidence. Required categories: `persistent_files`, `atomic_single_file_write`, `cryptographic_hash`, `exclusive_claim`, `remote_sync`, `clock`, `schedule_wake`, `external_provider`, `pixel_visual_review` and `independent_reviewer`. Capabilities do **not** derive from mere presence of a URL, skill, dependency declaration or cloud environment. Their verification is environment-specific and expirable.

Host-missing capability causes `BLOCKED`, `PENDING_VERIFICATION`, or explicitly authorized manual cooperative fallback. A run that requires exclusive multi-agent coordination MUST NOT start parallel exclusive tasks under an unverified claim backend.

## Authoritative state and sources

Use **validated per-run events as the audit authority**. `state.json` is a derived materialized current snapshot with the last included event sequence/hash; `checkpoints/` are validated resume anchors. A snapshot is fast to read but cannot rewrite history. If events/snapshot disagree, stop, preserve the conflict, and rebuild from the last validated sequence. A run `INDEX` is always derived and can be stale.

Domain provider reality is resolved separately using explicit readback before consequential external actions. Meta configured ACTIVE is not evidence of actual delivery, and a saved GHL bot setting is not proof of a real Messenger/Instagram reply.

## Allowed operation classes

`read`, `research`, `write_local`, `review`, `stage_paused`, `edit_crm`, `deploy_dev`, `deploy_prod`, `activate_live`, `change_budget`, `send_message`, `emit_conversion`. Defaults permit read/research/local draft/checkpoint within approved file root, and demand explicit owner authority for consequential nonlocal actions. A run claim, producer role and skill never add an operation class.

## V1 execution distinction

- **Portable minimum:** a capable agent reads Markdown/YAML/JSON, records dated JSONL events, keeps snapshot/checkpoint/handoff, validates dependencies and operates under a single-writer assumption.
- **Optional stronger modes:** host supplies schema validator, atomic file writes, Git sync and multi-agent claim adapter, scheduler or actual external APIs. Each adapter advertises and tests only its own guarantees.
- **Not in V1 minimum:** mandatory LangGraph runtime or A Rep PRIMARY; these are integrations, not dependencies.

## Compatibility

Protocol schemas use `schema_version: "1.0.0"` and `aosw_version` separately. Compatible readers MUST reject unknown **major** schema versions, ignore unknown extension fields only in designated `extensions` objects, and retain opaque original records when migrating. Additive optional fields under the same major version are permitted only when a missing field has a documented safe meaning. Never treat missing permission, requirement, review or skill as implied PASS.

Detailed transitions and rewrite rules live in the other architecture docs. The actual JSON Schemas are design artifacts, **not** an implemented engine or verified enforcement.
