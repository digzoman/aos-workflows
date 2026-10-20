# Agent OS Workflows (AOS-W) — Version 1 Product Requirements Document

**Document status:** DRAFT FOR OWNER REVIEW — NOT APPROVED  
**Version:** PRD 1.0-rc1, 2026-10-20  
**Product:** Agent OS Workflows (AOS-W)  
**Repository:** https://github.com/digzoman/aos-workflows  
**Installable distribution:** scaffold/aos-w/  
**Approval gate:** No workflow engine or implementation work may begin until the owner explicitly approves this PRD. Proposed architectural choices and ADRs remain proposed unless separately accepted.

> **Reading convention.** **AGREED** means directly selected in the original survey or Prompt 01b refinements, as recorded in temp/DESIGN-DECISIONS.md. **RESEARCH** means documented by the historical Ampgent/A Rep studies in temp/research and temp/architecture; these files do not prove current live provider state. **PROPOSED** means a specific implementation-oriented recommendation requiring PRD/ADR review. **OPEN** means deliberately not decided. In requirements tables, **MUST** indicates a product-level obligation conditional on PRD approval; it does not imply a runtime already exists.

## 1. Executive overview

### 1.1 Product vision

AOS-W is a **portable, file-based, model-agnostic standard for multi-step agentic workflows**. A capable human-guided or autonomous AI agent can copy the standalone folder into a local or persistent cloud workspace, read an approved workflow template, execute or delegate authorized tasks, persist outputs and checkpoints, recover from interruption, request quality review, and hand off to another agent without relying on the original conversation or model process.

Three objectives have **equal priority** [AGREED]:
1. Deliver a genuine Ampgent advertising workflow prototype, grounded in completed competitor research, creative generation, ad configuration, and launch experiences.
2. Provide a reusable portable workflow format for unrelated use cases.
3. Enable reliable collaboration, bounded task ownership, independent quality control, and cross-platform handoffs among ChatGPT, Codex, Claude/Muse, Fred/Max, and other execution surfaces.

AOS-W is a **workflow layer**. It does not replace a capable AI model, A Rep's PRIMARY agent, a task-management application, a CRM, an ad network, or a scheduler. It does not magically execute YAML while no agent/host is running. Real-world tools and atomic coordination are optional capabilities with verifiable availability.

### 1.2 Problem to solve

Ampgent campaigns required many sessions to research Meta Ad Library keywords and competitors, preserve source evidence, generate precise visual/copy variants, conduct independent review, stage Meta campaigns, correct ages/geographies, activate specifically approved objects, and interpret performance. Durable tasks were often split across prompts and agents, while chat history, repository status, external provider state, and QA records could diverge. Observed issues included blocked/empty searches, old portfolio indexes, partial reviewer coverage, semantic drift, incorrect logos and image sizes, duplicate Meta objects after ambiguous API timeouts, incomplete CRM tests, and rate-limited readback [RESEARCH: Prompts 02–05].

AOS-W must capture **what was authorized, which agent did what, which exact artifact passed each gate, what the external system actually confirmed, what remains unknown, and what work is eligible next**. It must permit narrowly targeted correction without discarding unrelated successful work.

### 1.3 V1 success definition

Version 1 passes the **six original survey demonstrations**, supplemented by the Prompt 01b no-Git/schedule/skill tests. See Section 20 and supporting ACCEPTANCE-TEST-MATRIX.md. The deliverable must be downloadable and runnable by an agent using only the documented file protocol for single-writer use; more stringent exclusivity and scheduling capabilities must be tested in explicitly optional host modes.

### 1.4 Product principles

- **Files first; execution adapters optional.** No mandatory Python, programming runtime, Git, MCP server, database, dashboard, cloud platform, or daemon [AGREED Q15].
- **One format, multiple hosts.** Local versus cloud storage, Git mirroring, host scheduling, and concurrent agents are independent capabilities.
- **Only agent-files changes in normal use.** Standardized framework and base templates are read-mostly, project/custom/live data reside inside agent-files.
- **Authority is explicit.** A task plan, Git lock, producer provenance, skill, QC PASS, or provider access never creates business permission.
- **Observed truth versus workflow evidence.** The provider determines provider-owned facts; saved local history is evidence of what was done or observed.
- **Cold-start recovery.** Every phase can be resumed by a fresh session with appropriate access.
- **Version-accurate QC.** No stale approval can silently apply to an altered artifact or expanded required set.
- **No phantom guarantees.** Where an agent is only following instructions, the product labels concurrency, retries, privacy, scheduling, and validation as cooperative/manual, not technically enforced.

## 2. Users and personas

| Persona | Goal | Required behavior |
| --- | --- | --- |
| Workflow author/operator | Define repeatable tasks and defaults; select scope and permissions | Readable Markdown/YAML, template library, parameters, version tracking, approval gates |
| Owner/approver | Delegate bounded work while keeping control of publishing, spending and strategic decisions | Clear decision records, precise artifact/object scope, ability to approve/reject/waive only allowed gates |
| Standalone local AI agent | Execute a workflow in a copied folder without Git | Plain-file read/write, deterministic step order, manual checkpoint and handoff |
| Persistent cloud AI agent | Work from durable cloud files without necessarily being multi-agent | Storage durability check, source refs, crash/reconnect recovery |
| Parallel worker agent | Claim a permitted independent subtask, produce evidence and hand off | Explicit identity, dependency checks, task scope, exclusive claim where supported, separate outputs |
| Independent reviewer/Guardian | Review complete evidence and artifact revision without corrupting original submission | Reviewer independence, specific QC verdict and correction path, advisory scope where applicable |
| A Rep PRIMARY (Fred-like) | Coordinate strategic activity while delegating bounded workflows | Link a work Issue/plan to a workflow run, no duplicate global scheduler or competing authority |
| Manual agent repository (Max-like) | Persist a marketing workflow across ChatGPT/Codex/Claude sessions | No always-on runtime required, full handoff/recovery and optional Git sync |
| Maintainer/template publisher | Improve standard scaffolds safely | Explicit framework upgrades, package compatibility and non-destructive agent-files migration |

### 2.1 Primary jobs to be done

Plan competitor discovery; create and authorize vertical study children; score source advertisements independently from market opportunities; produce accurate copy and multiple creative formats; fix one failed logo/placement without restarting; prepare website/CRM/Meta configurations; pause-stage and verify provider objects; obtain specific launch approval; report results with provider/measurement distinctions; and reuse these patterns for unrelated business workflows.

## 3. Scope, boundaries, and releases

### 3.1 V1 required [AGREED Q1–Q3]

- Research plan and keyword discovery.
- Individually executable research batches and vertical runs.
- Automated/objective checks where tools are available, independent AI review, human approvals, and targeted revisions.
- Evidence synthesis, source-level and opportunity-level scoring with named rubrics.
- A **bounded** creative-to-marketing-implementation example, including prepared Meta/CRM/website artifacts, staged/mock provider integration and read-back behaviors where authorized.
- Reusable templates and composed workflows, sequential/parallel steps, conditional edges, dynamic run creation, join/merge.
- Cooperative standalone single-agent execution **and** tested shared-agent exclusivity through an optional coordination backend.
- Task/checkpoint/event/provenance files, explicit recovery and manual cross-agent handoffs.
- Optional Git sync, user-selected claim trials, default one-off triggers plus optional recurring declarations.
- Template/instance-embedded skills plus step-local installed/remote skill references.

### 3.2 Explicit nonrequirements [AGREED Q15]

Do **not** require a Python interpreter, LangGraph, cron daemon, persistent PRIMARY runtime, central database, dedicated MCP server, web dashboard, Git checkout or GitHub account. Those may be **optional integrations** only. Do not promise one-click fully autonomous ad buying, exact ROI measurement, a production CRM, browser access, live publishing, or guaranteed cloud storage when prerequisites are not present.

### 3.3 Bounded pilot interpretation [PROPOSED]

V1's real Ampgent pilot should complete a **sanitized end-to-end research and asset-production path**, with a controlled mocked/paused marketing handoff and explicit provider-readback examples. It must demonstrate a truthful research-to-creative-to-staging lifecycle and its authorization gates. It must **not** spend money, deploy production content, create actual campaigns, message real prospects, or emit conversion events without fresh task-specific authorization. The precise quantity of live integrations to require in V1 remains OPEN (D-09).

### 3.4 Non-goals

AOS-W does not itself replace A Rep's prioritization/heartbeat/Guardian, LangGraph runtime, Git source control, cloud synchronization, Meta Ads Manager, HighLevel CRM, website host, browser, editor or image generator. Reproducing all fifty-plus historical Ampgent templates as fully automated integrations is outside the smallest V1.

## 4. Operating environments and capability model

### 4.1 Orthogonal dimensions

**Storage location:** local persistent folder, persistent cloud folder, or shared workspace.  
**Version synchronization:** no Git, Git mirrored/synchronized, or host-managed non-Git cloud store.  
**Agent count:** one active writer, independent parallel branches, or shared coordinated multi-agent workers.  
**Execution trigger:** manual invocation, host-supplied event, host-supplied schedule, or existing A Rep wake.  
**Tool surface:** plain-files agent, optional scripting, Git connector, image/browser/provider connector and/or independent reviewer.

Do not encode a false binary notion that all cloud operation means collaborative execution or that all Git workflows have a scheduler.

| Environment | Minimum behavior | Limit of verified guarantee |
| --- | --- | --- |
| E1 local standalone | Unzip/copy scaffold, agent reads and writes only agent-files, manually executes graph | One cooperative writer; no exclusive concurrent claim without atomics |
| E2 cloud standalone | Same workflow from a host-proven persistent filesystem, one session or sequential fresh agents | Persistence must be established; ephemeral workspace is NOT sufficient |
| E3 Git-synchronized single writer | Read current Git remote status before work; record commit/push and conflicts afterward | Git sync alone does not lock tasks or verify external reality |
| E4 Git shared coordinated | Distinct logical task claims through **tested** optional coordination, parallel independent tasks | No exclusivity if remote claim/lease/fencing behavior not verified |
| E5 shared non-Git storage | Same graph with provider-native atomic compare/claim adapter if available | Otherwise manual serialized ownership only |
| E6 optional scheduled host | Reads declarative due tasks and starts authorized occurrence run | No unattended processing when the host/scheduler is absent or down |

**Capability declaration [PROPOSED]:** record actual observed availability for storage persistence, atomic writes, remote Git and compare/update, clock/timer, render/inspect, external API, provider readback and reviewer separation. A missing capability yields WAIT/BLOCKED/MANUAL_REVIEW, never fabricated PASS.

### 4.2 Installation and offline promise

A user can directly download only **scaffold/aos-w/** from the public repository (or a release packaging that extracts to that folder), move it to any working directory, open README/START-HERE, choose a base template or create an instance under agent-files, and begin by asking a capable agent to follow the instructions. An agent must never assume that a machine already has Git or internet access. In offline mode, already bundled and installed trusted skills remain usable; remote-only assets are unresolved until connectivity or a verified offline snapshot exists.

## 5. Terminology and semantic distinctions

| Term | Meaning |
| --- | --- |
| Framework scaffold | Immutable/read-mostly distributed AOS-W instructions, base templates, specifications and supporting skills |
| Agent-files | Only normally writable subtree under an installed scaffold, containing custom templates, runs, artifacts, reviews, sync config and logs |
| Template | Reusable versioned workflow definition, instructions, input/output contracts, QC and autonomy defaults, optional trigger and skills |
| Custom template | User-created or overridden template saved under agent-files, not an in-place modification of the standard template |
| Workflow definition | Versioned composed directed graph with stable step IDs, conditions, joins and possibly child templates |
| Workflow instance | Project-scoped instantiated definition and its metadata/parameters/permissions; may have one or several execution runs |
| Run / occurrence | One concrete execution attempt of an instance; a schedule occurrence gets distinct identity and history; a manual trigger also creates a run |
| Task / node | Smallest independently claimable executable or reviewable unit with stable ID and contract |
| Attempt | One invocation of a task that may succeed, fail, time out or require reconciliation |
| Child workflow | Dynamic or declared nested workflow with own run state and explicit parent relation |
| Claim / lease | Recorded task owner and validity window; **exclusive** only where supported by tested atomic coordination |
| Checkpoint | Durable, revision-specific state+evidence boundary from which another agent can resume |
| Event log | Chronological history of changes, attempts, QA, authorizations and reconciliations |
| Gate | A validation/approval condition; QC assesses quality, authorization grants bounded permission |
| Artifact | Output or evidence file/object addressed by locator and revision/hash, potentially stored outside AOS-W |
| Skill | Instructions/resources for how to do a step; can include optional tool/code; **never** creates permission |
| Provider truth | Verified facts that external system owns, e.g., Meta campaign status, CRM booking |
| Evidence confidence | Assessment of support for a claim; distinct from task status, score or business outcome |
| Autonomy policy | Explicit scope of decisions/actions permitted without interrupting the owner |
| Sync mode | Whether/how Git or other storage is used, separate from agent concurrency |
| Fencing | Conditional protection preventing a former task owner from committing authoritative output after lease takeover |
| Handoff | Durable source/versions/state/next-action package for a fresh session or different agent |

Workflow lifecycle, domain research result, external object status, QA verdict, human authorization and business/measurement outcome **MUST NOT** be conflated into one status.

## 6. Portable distribution and protected-file specification

### 6.1 Repository layout [AGREED]

Public development repository: README.md, docs/, examples/, scripts/, tools/, **scaffold/aos-w/**, and tracked **temp/**. The temp directory records development decisions/research/handoffs and is **not** a writable end-user runtime scratch space. The root can publish optional scripts and helper apps without adding them to the minimum installed folder.

### 6.2 Proposed downloadable scaffold directory contract

The following is the **PRD-required logical layout, proposed directory spelling** for technical design in Prompt 08:

- **scaffold/aos-w/README.md**: beginner start, capabilities/limitations, one-agent runbook, upgrade rules.
- **scaffold/aos-w/FRAMEWORK.md** (or equivalent): canonical protocol, safety/identity/recovery specification.
- **scaffold/aos-w/spec/**: versioned human-readable schemas/state/compatibility definitions.
- **scaffold/aos-w/templates/**: approved read-mostly base workflows and their step-specific skills/assets.
- **scaffold/aos-w/references/**: approved instructions and example patterns referenced just in time.
- **scaffold/aos-w/agent-files/README.md**: **only normally writable location** and recovery/sync explanation.
- **scaffold/aos-w/agent-files/config/**: local execution policy, observed capabilities, optional Git remote mapping and sync mode; never plaintext secrets.
- **scaffold/aos-w/agent-files/custom-templates/**: custom/inherited templates and bundled user skills.
- **scaffold/aos-w/agent-files/workflows/**: instantiated definitions, configuration, run history and parent/child relationships.
- **scaffold/aos-w/agent-files/runs/** (if separate from workflows): run-specific state/events, claims, proofs, reviews, approvals, outputs, handoff and skill snapshots.
- **scaffold/aos-w/agent-files/cache/** and/or **indexes/**: optional rebuildable nonauthoritative convenience files within writable zone.

The chosen workflow versus run path hierarchy and names are **OPEN D-01**, but the hard boundary is not open: in ordinary use every mutable record, even custom templates, skill snapshots, local Git sync metadata, and runtime logs, is stored in agent-files. No required active-state writes are allowed into framework templates, docs or reference skills. Explicit installer/version upgrade of standard files is a governed exception.

### 6.3 Upgrade and isolation contract

Upgrade MUST never silently overwrite agent-files. A framework distribution release carries its own version and a migration note; an installed run pins the template/scaffold revision it started from and must remain recoverable after framework files change. Framework upgrade MAY require explicit migration, backup and human review where schemas or approval semantics change. A broken/incompatible run MUST report incompatibility and remain recoverable from its last valid snapshot, not be converted in place without a record.

### 6.4 Download package quality

An independent folder copy must contain every mandatory base instruction/template/skill needed for the standalone example, excluding optional external dependencies and project secrets. Distribution documentation must explain how to use it **without cloning the entire repository**, where to write run files, and how to check for (but not assume) optional connected Git sync.


## 7. Templates, parameters, inheritance and composition

### 7.1 Template model

**FR-101:** Each template MUST declare stable identifier, human purpose, semantic version, source and trust classification, parameter/inputs/output contracts, graph steps, default autonomy/approval policy, retry/quality defaults, optional trigger, referenced skills and artifact destinations. It SHOULD include a minimal usage example and preflight prerequisites.

**FR-102:** Instantiate a versioned copy/reference without mutating the source template. A user can select standard templates and create customized variants under agent-files. Resolve effective settings into a **pinned run manifest** so later changes to a master template do not silently alter an active run.

**FR-103:** Support configuration inheritance/overrides from framework defaults → base template → custom template → instance → allowed run/step override. **PROPOSED guardrails:** more-specific settings may change allowed values but cannot expand authority above a protected owner/organization policy; mandatory compliance or explicitly human-only gates cannot be removed without independently approved authority. The precise merge syntax, conflicting skill precedence and override whitelist are **OPEN D-02**.

**FR-104:** Every effective field SHOULD record its source layer and revision, or expose a reproducible resolved manifest. On conflicts, ambiguous inheritance MUST fail with a diagnostic instead of choosing a silently permissive value.

**FR-105:** Template evolution uses explicit versioning; deprecation and migration require traceable changes. A copy of a custom template remains project-owned in agent-files; its linkage to upstream version may be retained for comparison without mandatory automatic update.

### 7.2 Composition primitives [AGREED]

- **Sequence:** a node is eligible only when predecessor gates and required outputs are satisfied.
- **Parallel branch:** independent nodes may be claimed and executed concurrently if the host has safe coordination; in one-agent mode an agent may process them one at a time with identical graph meaning.
- **Conditional edge:** route from an evaluated predicate to named branches, including UNKNOWN/UNVERIFIED and failure cases. Do not coerce absence of evidence to FALSE.
- **Dynamic fan-out:** a planner proposes zero or more child tasks/workflows from approved input inventory. Stable IDs and explicit run-level authorizations prevent accidental duplicates.
- **Join/merge:** aggregate required accepted child outputs, preserve dissent, gaps, version and scoring rubric; the template defines ALL/QUORUM/SELECTED behavior or a documented equivalent. Exact quorum semantics are proposed, not user-approved.
- **Nested composition:** one template can invoke/reuse another as a child with scoped inputs/outputs, permissions and lifecycle.
- **Repeat inside one run:** loops over queues, batch sizes or retry work are distinct from a scheduled recurring *new* run.

**FR-106:** A composite instance MUST preserve stable parent-child links, data dependencies, source rubric and owner permission boundaries. A child created dynamically begins PROPOSED/PLANNED, never automatically AUTHORIZED unless a preexisting policy explicitly authorizes that class and scope. Historical 15-run vertical research required individual human prompts; V1 MAY support batch authorization, but must not retroactively infer it from that historical program.

**FR-107:** Independent parallel branches MUST use separate output/evidence locations or enforce safe merge strategy, avoiding unsynchronized edits to one shared Markdown or JSON file. Parent consolidation occurs only after configured accepted child versions and quality gates.

**FR-108:** Graph revisions may add, remove, split, reorder or reparameterize future steps according to each workflow's **configurable change policy**. Preserve completed results and previous graph version; examine changed dependencies, affected input hashes and reviewer gates. A routine low-risk change may be auto-approved where policy permits. Material change MUST wait for the required approver.

### 7.3 Conditions and loop safeguards

**FR-109:** Condition evaluation MUST produce TRUE, FALSE or UNKNOWN, with reasons and evidence. On UNKNOWN, default safe behavior is WAIT/BLOCKED or follow a specifically configured UNKNOWN path, never assume success. An execution adapter must not evaluate arbitrary untrusted expressions or scripts merely because YAML contains them. Exact portable predicate vocabulary is **OPEN D-03**.

**FR-110:** Loops MUST have bounded, observable iteration/queue progress and termination conditions, stable per-item IDs and retry budgets. A user can interrupt or stop without losing completed batches. A plan with 15 child prompts does not constitute a command to launch all 15 at once.

## 8. Run state, events, checkpoints and recovery

### 8.1 State dimensions

**FR-201:** A run has stable identity, template/effective-manifest revision, parent relation, trigger/occurrence identity, created/updated times, current eligible tasks, tasks' state, latest verified checkpoint, current owner, permissions, blockers, QC/approval pointers and optional sync state. Task status, artifact review, domain outcome and provider activity MUST remain distinct.

**PROPOSED V1 task lifecycle:** PROPOSED → PLANNED/WAITING_AUTHORIZATION → READY → CLAIMED/RUNNING → WAIT_EXTERNAL/WAIT_HUMAN/WAIT_QC or NEEDS_REWORK → COMPLETE; alternate BLOCKED, CANCELLED and SUPERSEDED. Recovery-specific UNKNOWN/RECONCILE_REQUIRED can interrupt a task. This is a candidate canonical vocabulary; the exact enum is **OPEN D-04**.

**FR-202:** Preserve domain-specific findings, for example source-ad PASS/FAIL_AGE/RETRY_REQUIRED, market LAUNCH_CANDIDATE/RESEARCH_MORE/DEFER, FULL versus PROVISIONAL scores and HIGH/MEDIUM/LOW confidence in separate named fields, with rubric/version and cited evidence. They cannot replace lifecycle states.

**FR-203:** Live Meta state has separate intended, request accepted, configured, effective/review and observed delivery/insights fields; CRM event provenance and business outcome are separate still. A local file's last status or a campaign label is not live provider authority.

### 8.2 Current snapshot, events and audit

**FR-204:** Persist resumable machine-readable run/task state (proposed JSON), a chronological logical event trail (proposed JSONL), human-readable progress/handoff (Markdown), and artifact/evidence references. Required event fields, proposed: stable event_id, run/task/attempt, event type, actor four-field identity, timestamp with timezone, prior/next state, manifest/revision, claim/approval link, source/evidence and result. JSON/JSONL choice follows user preference; exact source-of-truth precedence during corruption is **OPEN D-05**.

**FR-205:** Event logging MUST be monotonic in meaning. Correcting an old finding appends a superseding/correction event rather than silently erasing history. Derived portfolio indexes, queue dashboards and aggregated progress files are **rebuildable views**; when their timestamps conflict with an inspected per-run current state, flag STALE_INDEX and reconcile without falsely declaring the run unstarted or completed.

**FR-206:** Checkpoints MUST describe confirmed completed work, the next eligible action, pending permission/review, evidence and precise changed artifact version. A checkpoint MUST NOT assert Git push, external provider write or QC pass before independently observing the result. A fresh authorized agent can resume from stored state without earlier chat context.

**FR-207:** A writing failure, interrupted JSONL event, missing snapshot or mismatched versions MUST be detected and handled conservatively. The recovery policy must retain the last verifiably consistent boundary, preserve suspect files for inspection and avoid guessing that an external action did or did not happen. **Do not claim crash-atomic file updates** in a plain text editing environment; an optional host may supply temp-file rename/fsync/transactional behavior once tested.

### 8.3 Retry, wait and interruption

**FR-208:** Each task may declare retriable failures, bounded attempts, delay/backoff advice, fallback source, compensation and escalation. The protocol distinguishes RETRY_REQUIRED, EMPTY_VERIFIED, SOURCE_UNAVAILABLE, RATE_LIMITED, FAILED_VALIDATION and uncertain side-effect outcome. In file-only mode an agent records next_due/WAIT; no unattended timer is implied.

**FR-209:** A retry after an ambiguous external create/update MUST first read the provider/operation state when available. Store a stable logical operation key and attempt trail to prevent duplicates. If provider readback is unavailable, remain RECONCILE_REQUIRED and require human/authorized recovery; do not assume failed request means no side effect.

**FR-210:** Interruption by human review pauses only dependent work. Independent authorized branches MAY continue. A resumed agent must check whether outputs and side effects from the interrupted attempt already exist before replaying. Side effects are *at-least-once possible* unless underlying adapter/provider offers a proven stronger guarantee.

**FR-211:** Repair MUST target the smallest affected upstream node plus transitive dependent artifacts/gates. Incorrect square dimension must not force repeated competitor discovery; wrong logo must not invalidate an unaffected caption; changed price or buyer/problem premise must invalidate downstream claims/copy/images and provider mapping as applicable.

## 9. Quality gates, reviewer roles and approvals

### 9.1 Separate verification and permission

**FR-301:** Support objective/deterministic checks, semantic and visual agent evaluation, independent AI reviewer and explicit human approval, as configurable workflow defaults and per-step gates [AGREED Q11]. Self-review is allowed for low-risk work when template policy permits. A passed QC gate **never** grants permission to publish, send, spend or deploy; that requires an independently scoped authorization record.

**FR-302:** Every QC verdict MUST identify gate, reviewer identity, exact evaluated artifact IDs/hashes and set membership, rubric/version, criteria, evidence, result and timestamp. If a previously approved 2-item set grows to 8 required items, the old approval remains valid **only for its original set**, not the new full deliverable.

**FR-303:** Independent review MUST record a distinct reviewer from the producer when configured, retain first-pass submissions and make peer critiques append-only. In manual text-only mode independence is a process rule, not tamper-proof access control; a host with access isolation MAY enforce it and document the guarantee.

**FR-304:** Verdicts SHOULD distinguish PASS, REVISE/NEEDS_REWORK, INSUFFICIENT_EVIDENCE, PENDING_VERIFICATION, BLOCKED, and WAIVED_BY_AUTHORIZED_OWNER. A waiver must specify scope, rationale, expiry and affected risk; it is not silently equivalent to evidence PASS. Exact vocabulary is **OPEN D-04**.

**FR-305:** Approval MUST have subject/action class, allowable resources/objects, affected artifacts+versions, authority/source, time/expiry where applicable, budget/exposure limit if relevant, conditions, negative exclusions and actor identity. Editing significant claims, audience/eligibility, spending, production deployments, or publishing follows configurable policy. Optional future trusted automation may publish after QC **only if a separately valid permission policy explicitly grants that operation**.

### 9.2 Workflow autonomy and dynamic changes

**FR-306:** Provide at least bounded default autonomy (plan, research, draft, propose, checkpoint, perform permitted reversible mechanics) and workflow-specific configurable policy, with allowance for autonomous low-risk execution or higher delegated action when explicitly authorized [AGREED Q12]. Conditions/permission sources are inherited transparently without letting weaker layers override protected policy.

**FR-307:** Per-workflow revision policy chooses permitted minor changes, required review for material edits, which upstream decisions are immutable, and which completed branches need re-verification. Historical work is not deleted. Effective policy and revocation MUST be visible at each run.

**FR-308:** Independent branches that have passed the appropriate gates may proceed despite an unrelated failing branch, unless the parent explicitly requires ALL siblings before join or owner approval says otherwise. A fully accepted compound result needs configured join evidence and current gates, not just child file presence.

### 9.3 Domain-specific quality examples

**Research gates:** source access works; dated source/advertiser/keyword evidence; genuine commercial paid-Meta relevance; buyer matches target; observed ad-ID versus result card versus landing/snippet/inference classification; seller/offer-family dedup; age threshold by query type; no invented prominence; coverage reconciles all pending/retry rows; correct named ad-persistence score versus seven-axis vertical-opportunity rubric.

**Creative gates:** accepted semantic spine (buyer, trigger, hook, mechanism, offer, outcome, commercial path) before image generation; exact primary text/headline/description/on-image words; truthful approved claims; official logo asset (not AI fake), source revision, readable safe margins; actual image dimensions and square/portrait/9:16 placement preview; separate deterministic export, visual QC, Git blob read-back and owner selection.

**Marketing gates:** exact configured Meta campaign/adset/ad and paused state; correct geography/age **hard versus suggested** controls and exclusions; actual media association; selectable full-text Questions and empty Response fields; saved GHL bot knowledge versus real FB/IG DM behavior; website DEV/PROD release and consent; Pixel/CAPI dedup/qualified milestone proof; separate scoped activation and actual provider/delivery verification.

## 10. Identity, ownership, claims, and multi-agent handoff

**FR-401:** Persist agent provenance using the A Rep-compatible four-part convention **[Agent | Platform | Role | Instance]** on task claims, significant events, reviews, human-facing handoffs and Git commits when available. An optional agent-run correlation ID helps distinguish fresh sessions using one GitHub login. Native GitHub author/transport is not proof of agent identity.

**FR-402:** An exclusive task may be marked CLAIMED only with owner identity, acquired/last-seen times, lease/expiry hint, task/revision, and shared-claim verification result. In single-agent manual mode, ownership is cooperative/advisory. AOS-W MUST NOT promise mutual exclusion for uncontrolled simultaneous file writers.

**FR-403:** A shared mode claiming **enforced exclusivity** requires a tested atomic claim primitive and stale-owner fencing/revision checks. Without one, shared tasks are blocked, queued for manual arbitration, or explicitly single-writer; two independent agents must not both be told they own the same exclusive task.

**FR-404:** A lease may expire on paper, but takeover and output acceptance require fresh observation and atomic/revision-checked new ownership in enforced mode; after network failure a previous owner must not assume it still possesses the remote lease. Recovery MUST preserve ambiguous claim state and prevent stale completions where enforcement is supported.

**FR-405:** Handoff packages MUST include exact repository/local/storage locator, template and run ID/version, owner/claim, completed tasks/evidence, failing gates, source-of-truth boundaries, all outstanding permissions, next authorized action and timing, unresolved sync/provider effects, and known tool/skill limitations. New agent checks live artifacts and remote state before performing work.

**FR-406:** One agent platform can pick up a run from another without converting to a provider-specific engine schema. Fred/Max/A Rep integration is optional. A Rep retains strategic PRIMARY/Issue/plan authority; AOS-W holds bounded graph/run state. The same business obligation must not become two inconsistent "authoritative" plans.

## 11. Optional Git synchronization and locking

### 11.1 Git synchronization contract

**FR-501:** Configuration in agent-files records whether Git synchronization is enabled, remote/repo identifier, branch/mirroring strategy, base revision, expected read-before-work and write-after-checkpoint behavior, credentials *by external reference only*, and conflict policy. In no-Git mode, these are absent/disabled with no functional penalty.

**FR-502:** When enabled, the agent MUST inspect sync status or latest remote revision before modifying shared work and validate local/remote changes before pushing. Checkpointing locally is not proof of remote persistence. Conflicts must be reported and reconciled, never silently overwritten. No automatic force push of framework history.

**FR-503:** Git commits SHOULD carry Agent-Provenance (and Agent-Run when available), reference run/task and meaningful change intent. Sensitive credentials or customer data must be filtered before Git transmission, especially to this **public** development repo.

### 11.2 Locking study and decision gate

**FR-504:** Prototype **both Git LFS locking and atomic Git-based task claims**. Record actual two-agent races under shared and distinct GitHub identities, collisions on same/different tasks, crash/lease expiration, lost network and ambiguous updates. Before tests, neither is declared proven or the final selected protocol [AGREED Q7].

**PROPOSED candidate A:** Git LFS path locks for binary or designated files. Limitation: file-level scope, installed Git LFS and server support, same-account lock ownership ambiguity, stale lock cleanup and no guaranteed task lease.

**PROPOSED candidate B:** A task-specific Git ref/commit claim with version-checked creation/update and fencing. Limitation: not all API paths provide compare-and-swap; ordinary GitHub REST PATCH refs lack a documented expected-old-SHA parameter. A compatible Git push/connector with actual expected-SHA lease semantics must be tested. Expiry alone does not fence stale agents.

**FR-505:** Worktrees MAY isolate local branches/working copies, but Git worktree lock is administrative protection against pruning, **not** an exclusive edit/task claim. Git checkout similarly is not a lock.

**FR-506:** Offline mode MUST never pretend to hold or renew a cloud-exclusive lease. It may process isolated private drafts, record an offline fork for later reconciliation, or remain single-writer, following approved policy. Reconnection must reconcile remote task ownership **before** accepting previously unsynchronized outputs as authoritative.

**Decision:** final claim strategy, exact Git ref layout, lease duration, fencing token and force-with-lease behavior are **OPEN D-06** until implementation-stage research and tests.


## 12. Manual, scheduled and recurring triggers

**AGREED Prompt 01b:** Workflows are **non-repeating by default**. A standard/custom template may declare an editable recurring schedule. Any scheduled-capable template can also be launched ad hoc, and an instance can override/disable its template's default schedule. Recurrence starts new occurrences; queue loops and retries within one run are different.

**FR-601:** The workflow trigger contract MUST represent manual versus scheduled invocation distinctly, with template default, instance override, enabled/disabled state, owning time zone, intended recurrence expression, next due/check timestamp, invocation provenance, missed event and overlap policy. The exact RRULE/cron/syntax selection is **OPEN D-07**.

**FR-602:** Every occurrence has a stable uniqueness key derived from template/instance identity, schedule revision and intended occurrence boundary, plus an independent run ID; manually invoked runs are identified as manual even if the template has a schedule. Duplicate host wakeups must not produce duplicate accepted occurrences when verified coordination/idempotency is available.

**FR-603:** A purely standalone agent may read schedule metadata, calculate or check due occurrences using its host's observed clock, and report the next action when invoked. It MUST NOT claim background timers ran while no executor was present. Optional Fred/A Rep wake, OS cron, cloud host, GitHub Action or other scheduler can trigger the same file protocol if explicitly configured. No such integration is a base requirement.

**FR-604:** Recurrence policies MUST be able to express or explicitly defer handling of missed windows, daylight-saving transitions, time-zone changes, clock uncertainty, catch-up/skip/coalesce, overlapping active occurrences, retries of one occurrence, pause/resume, and cancellation. Default values are proposed for PRD review rather than silently assumed (see D-07). A manual agent must surface the unresolved choice when it affects a due run.

**FR-605:** A recurring research or read-only monitoring task does not confer standing authorization to publish ads, change budget, send outreach or trigger irreversible CRM conversions. Any inherited permission must identify action class, scope, conditions and expiry, and be checked on each occurrence.

**Edge cases:** two schedulers signal the same 9 AM occurrence; host is offline for three days; daylight saving fall-back repeats a local clock time; DST spring-forward omits a local time; an old recurrence version triggers after changed schedule; an active run overlaps the next scheduled one; user manually starts a scheduled template in between. Each must have an explicit event/response and never silently duplicate external side effects.

## 13. Skills as just-in-time workflow resources

**AGREED Prompt 01b:** Skills live in base templates, custom templates, or workflow instances, and may reference installed local skills or pinned remote Git/repository content. Steps identify precisely which ones to load and when. This is compatible with Agent Skills packages and A Rep's experimental versus approved procedure lifecycle.

**FR-701:** A workflow/template/run MUST be able to bundle its own skill package and bind that package to one or more task nodes. AOS-W SHOULD recognize Agent Skills-style directory containing a SKILL.md plus optional references, examples, scripts and assets. A run MAY capture the exact skill snapshot/revision used to allow reproduction even if upstream evolves.

**FR-702:** Skill reference resolution MUST support (a) read-mostly built-in skills, (b) custom template/run skills inside agent-files, (c) already-installed host skills, and (d) local or remote repository locations with version pin/hash and expected trust classification. Exact source identifiers and resolution precedence are **OPEN D-08**. Conflicting names/trust states are errors or explicit reviewer choices, never silent untrusted shadowing.

**FR-703:** Load only metadata needed to discover a skill, then the relevant SKILL.md when the node is eligible, then supporting files only when the instructions actually require them. Do not inject all unrelated skills into every agent context. The task event log records resolved skill ID, origin, revision and availability.

**FR-704:** A remote skill MUST be treated as untrusted content until source/revision/integrity and applicable approval are checked. Referencing an executable script cannot bypass tool permissions or launch arbitrary code; a script requires a compatible installed executor and separately appropriate authorization. A skill cannot supersede owner policy, escalate roles or override framework security.

**FR-705:** Offline lookup of a required remote-only skill MUST yield MISSING_SKILL/BLOCKED or use a previously verified local pinned copy if the workflow expressly permits it. Absence must not be represented as successful loading. The existing Ampgent logo-placement skill illustrates a useful **optional** Python/Pillow helper, not a mandatory Python dependency.

**FR-706:** AOS-W skill trust and A Rep's scratch-versus-procedures distinction SHOULD interoperate. AOS-W custom or run-specific skills do not automatically count as human-approved A Rep procedures, and sharing a GitHub identity does not prove a skill's author/reviewer.

## 14. External integrations, provider truth and side-effect safety

### 14.1 Optional adapters and permissions

**FR-801:** External tools are optional by design. Define adapter capabilities for Meta Ads Manager, website/host, HighLevel CRM, browser/image generation, Git, task/schedule host and other services. A workflow can prepare a proposed action offline; it may only report it as **executed** when the authorized host actually called the provider and verified applicable result.

**FR-802:** Distinguish permission classes including READ, RESEARCH, WRITE_LOCAL, STAGE_PAUSED, EDIT_CRM_CONFIGURATION, DEPLOY_DEV, DEPLOY_PROD, ACTIVATE_LIVE, MODIFY_BUDGET, SEND_MESSAGE and EMIT_CONVERSION. Permissions have owner/revision, intended objects, exclusions and explicit constraints. Environments with no provider access do not promote local intent to a provider operation.

**FR-803:** Before a consequential external mutation, preserve target identity, expected pre-state, desired diff, idempotency key, authority record and potential impact on siblings. After the action, record request attempt, provider acknowledgement and independent readback where available. A timeout or account rate-limit leaves an explicitly uncertain state.

### 14.2 External authority matrix

| Domain question | Truth source | Local workflow evidence |
| --- | --- | --- |
| Selected source ad, source audit and internal copy | Historical evidence and owner-approved version/decision | Cited source IDs, exact copy and artifact hash; historical facts may go stale |
| Current campaign/adset/ad existence, audience, budget, status | Meta Ads Manager/Graph readback | Desired manifest and timestamped last observed provider state |
| Live delivery/spend/CTR/CPC | Meta insights with exact period, filters and attribution | Source query, measured/estimated flag, denominators and time |
| Real Messenger/IG arrival and Max reply | Actual channel and HighLevel conversation state | Saved prompt/Question, Response null and test evidence |
| Booking, qualification and won state | HighLevel confirmed appointment/pipeline rules | Mapping and event audit, not a substitute for CRM business truth |
| Pixel/CAPI acceptance/dedup | Meta Events diagnostics plus transmitted event IDs | Consent and trigger logic, before/after test evidence |
| Website actually serving DEV or PROD revision | Hosting/deployment provider and rendered site | Source/deployed build SHA, release approval and smoke-test evidence |
| Agent task completion and permission | AOS-W versioned run events plus actual human authority | Run audit, handoff and gate status; cannot overwrite provider truth |

**FR-804:** AOS-W must not treat local plan, AI claim, README status, stale derived index or a campaign name such as an outdated paused prefix as current external reality.

### 14.3 Idempotency, compensations and controls

**FR-805:** New campaign/adset/ad creation needs preflight list/look-up for existing matching operation identity. On ambiguous create response, read before retry; do not blindly duplicate. Failed creative customization should route to a bounded, supported alternate approved by the owner, rather than repeat an invalid payload.

**FR-806:** A Meta activation workflow MUST explicitly enumerate campaign, adset and ad objects, approved variants and held siblings, verify fresh budget/geography and user scope, then perform only permitted changes. Historic child-first activation is a useful candidate procedure, not a universally proven Meta requirement. Actual serving and first impressions remain separate.

**FR-807:** Website source commit, DEV host deployment and PROD release require separate evidence and release permissions; production includes backup/rollback plan. A provider mutation is not assumed to be atomic with a Git commit or CRM change.

**FR-808:** CRM saved knowledge differs from an actual channel response. Pixel PageView, button click, confirmed Schedule, QualifiedLead and Purchase are different milestones. Browser/server event duplication must be tested with stable event identity and consent before claiming dedup. A published GHL workflow listing is not evidence its trigger/filters are correct.

**FR-809:** Rollback/compensation is a separate controlled operation with before snapshot, authority and after readback. Some effects such as customer messages, spend and conversion events cannot truly be undone. Handle ambiguous outcomes without false exactly-once guarantees.

**FR-810:** Monitoring must include measurement window, attribution settings, denominators and provider timestamp. No-click CPC may be reported as undefined and **separately labeled estimated** if calculated from explicitly stated assumptions. Do not present model-imputed conversions as observed performance. Automatically applying a suggested optimization needs authorization under its workflow policy.

## 15. Security, privacy and public distribution

**FR-901:** AOS-W development repository is fully public from the start [AGREED Q4]. Only sanitized generalized research/candidate templates, mock assets, policies and nonconfidential examples may be committed. Private project conversations, production credentials, raw ad account data, direct messaging details, CRM contacts, customer records, original internal screenshots and private repo artifacts must not be published by accident.

**FR-902:** Credential material stays in host-managed secrets/connector configuration, not template YAML, JSON state, logs, events, skill files or Git history. Local config MAY contain credential *references* that are safe for its intended visibility. Any sensitive run should store outputs in an appropriately controlled location rather than syncing private data into the public AOS-W repo.

**FR-903:** Paths supplied by templates and skills MUST be treated as untrusted until allowed-root and access policy checks; normal file writes stay under agent-files. Remote skill code, executable hooks, scripts and unknown URLs require supply-chain/trust review and separately scoped tool permission.

**FR-904:** Producer identity/role fields support accountability but are not authentication. Only actual host permission and verified owner approval can enforce external-effect boundaries. Shared GitHub credential agents need separately recorded logical IDs, but hostile actors bypassing the convention cannot be excluded by text files.

**FR-905:** Public example templates must use fictitious/sanitized customers, generic provider object IDs, safe destination placeholders, neutral screenshots or synthetic creative content with legitimate usage rights. Any actual user project/provider data must be managed with data-minimization and access controls external to the public distribution.

**FR-906:** Support explicit retention/redaction/export/delete instructions per run with audit treatment appropriate to its host, while avoiding a misleading promise of irreversible erase from existing Git history or external systems. Do not store untrusted private blobs merely to support a demo.

**FR-907:** Third-party text, scraped advertising evidence, competitor images and external skills are **data**, not higher-level instructions. AOS-W agents must not execute embedded instructions to override owner scope, reveal secrets or change external accounts.

**FR-908:** Before release, decide an open-source **license** explicitly; public repository visibility is not itself a grant of reuse permissions. License selection remains **OPEN D-10**.


## 16. Consolidated functional requirements and implementation contracts

This section is an implementation checklist. The more detailed clauses in Sections 6–15 remain normative within the **draft** PRD. Every identifier refers to a testable capability, not a claim it already exists.

| ID group | Required capability | Minimum acceptance evidence |
| --- | --- | --- |
| FR-001–FR-006 | Portable installation and modes | Copyable scaffold without required Git/runtime; writable agent-files boundary; documented capability fallback |
| FR-101–FR-110 | Templates, inheritance, graph, conditional, dynamic fan-out and merge | Versioned manifest and effective settings, deterministic eligible-task list and traceable child run |
| FR-201–FR-211 | State, checkpoint, events, resumption and targeted retry | Interrupted work recovered with exact evidence; stale index/corrupt-state warnings; no ambiguous external replay |
| FR-301–FR-308 | Objective/AI/human QC, scoped approval, autonomy and revisions | Wrong artifact or incomplete output fails; correct review and distinct permission gate unblock only eligible steps |
| FR-401–FR-406 | Provenance, task claims and handoff | Distinct agent IDs recorded; cross-platform cold start; optional tested exclusive mode blocks second claimant |
| FR-501–FR-506 | Optional Git sync and competitive locking trials | No-Git mode succeeds; mirrored conflicts detected; LFS/CAS experiments recorded, no invented winner |
| FR-601–FR-605 | Manual default and optional recurring schedules | Template override and ad hoc invocation, occurrence identity and no phantom background execution |
| FR-701–FR-706 | Template/run/installed/remote skills loaded at task time | Correct pinned skill loaded only for relevant task; missing/untrusted skill safely blocked |
| FR-801–FR-810 | Provider authority and side-effect safety | PAUSED staging vs activation separated, ambiguous timeout reconciled, actual readback and business truth distinguished |
| FR-901–FR-908 | Public distribution, secrets, path safety, trust and license gate | Sanitized release, no key/private data, tested boundary and honest licensing decision |

**Additional minimum installer requirements:**
- **FR-001:** From downloaded scaffold alone, explain to a compatible agent how to select/create a run and persist state, without network services or additional installed executables. A pure agent-read/write procedure is acceptable for single-agent use.
- **FR-002:** Include a source-controlled, versioned and readable minimal workflow example whose required skills are bundled. Test after copying **only** scaffold/aos-w to an unrelated directory.
- **FR-003:** All ordinary instance artifacts, including optional sync and agent-created custom templates, are written under agent-files. A test should attempt an outside-root write and verify prevention when a host validator exists, or a clear safe refusal under cooperative-only mode.
- **FR-004:** Supported hosts expose a way to report real capability status and evidence with UNKNOWN when unverified, without requiring every possible capability.
- **FR-005:** A human can inspect/revise/restart an instance after an interruption with no original model session, and keep previous results and approvals.
- **FR-006:** Every live-facing example uses mock/paused actions by default and requires a separate explicit permission gate for any production mutation.

### 16.1 Minimum data contracts for technical design [PROPOSED]

To be considered implementation-ready as requirements, the eventual Prompt 08 schemas must provide at least these properties:

| Record type | Required logical fields |
| --- | --- |
| Framework manifest | schema version, framework version, file-root/writability constraints, compatible protocol versions, optional adapter references |
| Template manifest | immutable template ID/version, author/trust, input schema, graph nodes, defaults, permissions/QC policy, trigger default, skills and output contract |
| Instance manifest | instance ID, template provenance/version, resolved config, scope, allowed permissions, current workflow graph revision, origin/creator and optional parent |
| Run/occurrence | unique run ID, manual/scheduled source, schedule revision/intended fire boundary when relevant, created/last update, run state, source of truth, parent/child links |
| Task/attempt | stable node ID, dependencies, eligibility/outcome, attempt ID, actor, timestamps, lease/owner, inputs/outputs, retry budget, verification status |
| Event | stable event ID, type, entity IDs, timestamp, actor/authority, previous/next state, artifact refs, evidence, correlation/revision and note |
| Artifact | stable ID, relative/supported external locator, media/type, version/hash, producer/source time, confidentiality/trust classification |
| Review/QC | reviewer, independence requirement, exact artifact hash/set, rubric/version, gate, evidence, verdict, remediation and scope |
| Authorization | who/what approved, action class, exact allowed objects/resources and exclusions, scope/version, prerequisites, budget/expiry and revocation |
| Claim | task ID, run ID, actor four-part identity, claim token, acquired/heartbeat/expiry, coordination capability, base version/fencing where enforced |
| Sync | enabled/disabled, remote/branch/ref, last verified local/remote revision, change status and unresolved conflicts, credential ref only |
| Skill resolution | skill ID, location/type, pin/hash, trust/source, required task, availability/cache, approved fallback and executed-tool permission |
| Provider operation | adapter, provider object IDs outside public sample, desired diff, operation key, authorization, attempt/response, actual readback, uncertainty/compensation |
| Handoff | run/task IDs, current state and timestamp, verified artifacts, blockers, approvals, expected next action, source and runtime limitations |

The exact serialization grammar, order of authority among snapshot/events, schema validation library and path names remain open for Prompt 08; a proposed schema cannot silently relax the above evidence/permission needs.

### 16.2 Required operational commands or equivalent agent actions

An implementation may use documented agent instructions **instead of a CLI**. It must define consistent ways to: inspect current run, create from template, resolve effective config, see next eligible tasks, claim/start/record attempt, attach evidence, submit quality review, approve/reject, checkpoint, recover, propose a revision, reconcile external state, handoff, and optionally sync/trigger a scheduled occurrence. Optional CLI/helper aliases should map to the same logical operations and never create a second independent state store.

## 17. Nonfunctional requirements and observable service quality

| ID | Requirement | V1 acceptance target and evidence |
| --- | --- | --- |
| NFR-01 Portability | One copied scaffold folder plus compatible agent is sufficient for offline single-agent walkthrough; no mandatory installer, internet, Git or Python |
| NFR-02 Persistence | A run resumes after a fresh agent session using only retained files and current external evidence; no reliance on prior conversation text |
| NFR-03 Readability | Human can inspect template, task states, gate results, approvals, event trail and next action without a specialized dashboard |
| NFR-04 Isolation | Ordinary framework files remain unmodified across a run; custom templates, data and working skills stay in agent-files |
| NFR-05 Audit | Every material attempt, approval, revision, skip/waiver and ambiguous external action has actor, time, scope and evidence pointers; no silent retroactive edits |
| NFR-06 Compatibility | Same logical workflow definition runs through manual local and optionally connected cloud/Git hosts; capability differences are recorded, not encoded as forks |
| NFR-07 Safe recovery | Interrupted work either resumes at verifiable checkpoint or fails closed with a useful handoff; never invent success or replay ambiguous side effect |
| NFR-08 Coordination | With a verified shared-claim adapter, two competing agents cannot both acquire the same still-current exclusive task; without one, system explicitly refuses that guarantee |
| NFR-09 Security | No production secrets/raw customer data in public assets; remote skills cannot override permissions; normal writes restricted as far as the host can enforce |
| NFR-10 Version stability | Manifest and artifact versions make approvals reproducible; altered required output invalidates only dependent gates; old results remain available |
| NFR-11 Extensibility | Optional Git, scheduler, image, CRM, Meta and reviewer adapters do not alter base schemas or require extra services for unrelated tasks |
| NFR-12 Resilience | Rate limit, missing browser, stale metadata, missing skill, network interruption and torn-write cases yield explicit actionable status rather than lost work |
| NFR-13 Observability | Every test record declares LIVE/REAL, MOCKED, MANUAL/COOPERATIVE or NOT_RUN and reports evidence plus remaining unknowns |
| NFR-14 Determinism boundary | Deterministic checks (size/hash/schema/IDs) are enforced only when capabilities exist; semantic/visual judgements document reviewer and confidence |
| NFR-15 Cross-platform | A second agent platform can continue an independent saved instance without requiring the first platform's proprietary session runtime |
| NFR-16 Resource discipline | Avoid forcing expensive providers/models or loading all skill packages for every step; bound retries, parallelism and remote request budgets |
| NFR-17 Upgrade safety | A framework/template upgrade cannot overwrite agent-files; incompatible schema requires explicit migration/review and backup |
| NFR-18 Documentation | A novice can locate start, example, next task, expected outputs, blocked status and how to request a human approval from the installed folder |

**Quantitative targets [PROPOSED/OPEN]:** The original survey did not specify a startup latency, operations-per-minute throughput, event-count scale, storage quota, outage SLO, memory footprint or exact concurrency limit. No invented performance guarantee is part of V1. Prompt 08 SHOULD identify realistic sample-size bounds and measure them in Prompts 16–18.

## 18. Evidence-based example workflow specifications

### Example A. Meta Ads Library discovery queue

**Source model:** September 2026 broad research in Max. Thirty-four advertiser checks and ninety-six keyword queries were actually organized as six- and eight-item batches, respectively, with 23-day/specific versus roughly 60-day/broad source age conditions. These numbers are **historical example configuration**, not fixed framework limits.

**Graph:** preflight and source verification → select buyer/buckets → build advertiser and keyword queues → repeat eligible advertiser batches → keyword batches → reconcile/dedupe advertiser+offer family and ad ID variants → retry only blocked/high-value searches → source persistence rubric → coverage QC → shortlist and handoff. Evidence fields include observed ad ID or result card, query/market, active dates, rank *if observed*, source tier, verified emptiness versus RETRY_REQUIRED and producer.

**Acceptance:** all planned rows accounted for or exceptions explicitly accepted; scoring has a named ad-level rubric/version, no implied ad profitability; reviewers assess the correct artifact set. An inaccessible gallery never becomes a fabricated “no competition” conclusion.

### Example B. Fifteen vertical/subvertical investigations

**Source model:** Bucket 9 program with Prompt 00 setup-only and prompts for fifteen independently authorized audience studies, with general SMB/agency/experienced marketers, general trades, other industries and five specialist trades.

**Graph:** owner/offer question → portfolio candidate plan → generate self-contained proposed children with distinct IDs, buy-side role, search plan, outputs, exclusions and dependencies → per-child authorization (or explicitly approved batch autonomy) → research/evidence → seven-component vertical-opportunity score + separate HIGH/MEDIUM/LOW evidence confidence → independent review → portfolio reconciliation → conditional follow-up subvertical suggestions → human decision. Dynamic proposals do not automatically become active work.

**Acceptance:** scored seller evidence counts independently, differentiates DFY agency, DWY education, DIY tool and AI tool, confirms actual business-owner paid-Meta demand where possible, and preserves unresolved depth. The stale Run 10 portfolio index case demonstrates that child state must win over an unverified aggregate report, while being careful not to infer completion from “started.”

### Example C. Research-to-approved creative with failed square/brand correction

**Source model:** B1–B8 advertising creatives, source semantic audits, independent Fred/Muse critiques, official logo placement and multiple image variants.

**Graph:** source and exact offer claims → approved semantic spine → copy fields and copy lock → art direction → generated imagery and/or editable text-safe composite → canonical logo overlay → portrait and square branches → deterministic file/dimension/hash test → visual AI/independent reviewer check → owner-selected variant approval → repo readback/handoff.

**Test variation:** produce one approved portrait, deliberately introduce wrong logo on square, fail brand QC, repair composite/export/visual/owner-version gates for square only. Preserve original source research, copy and approved portrait; reject stale approval against a changed logo version. Another variation changes a grant/price number, which **does** invalidate copied text and related image/staging gates.

### Example D. PAUSED Meta campaign configuration, authorization and readback

**Source model:** selected B1–B9 campaign setup, geography and age corrections, specific held campaigns, square placement API failure, Oct 15 and Oct 18 controlled activations.

**Graph:** approved image/copy/buyer → Meta account baseline and current object inventory → scoped desired campaign/adset/ad graph → geo/age/standard versus suggested audience QA → media hash and messaging Question/blank Response mapping → website/GHL/tracking readiness gates → separate STAGE_PAUSED authorization → provider write/read-back → placement and end-to-end channel verification → independent prelaunch QA → explicit object/budget-specific activation approval → children then parents only if enabled → per-level configured/effective status and observed delivery → read-only metrics.

**Acceptance:** run cannot claim success from provider request ACK alone, cannot activate a held sibling, cannot duplicate objects after ambiguous timeout, and does not count a PageView as Schedule or a booking as qualified revenue. Any real external work must be separately authorized; staged/mocked pilot must say so.

### Example E. Recurring read-only monitoring and ad hoc override

**Source model:** user requirement Prompt 01b, plus historical requests for post-launch CPC/CTR and errors.

**Graph:** recurring-capable template with schedule metadata → optional host fires a unique occurrence or user manually starts a run → read permission and provider preflight → fetch date-scoped insights → independently compare measured and estimated results → classify issues → prepare recommendations → human review before any live optimization → checkpoint/report. When no scheduler exists, no run silently starts; when provider missing, record unavailable metrics.

**Acceptance:** a manually invoked run from a recurring template is distinguishable from its scheduled occurrences; two duplicate due signals cannot be accepted twice in tested coordinated mode; a monitoring summary never automatically changes spend.

## 19. Failure scenarios and edge cases

| Scenario | Required safe outcome |
| --- | --- |
| Browser returns empty/blocked Meta gallery while other searches work | RETRY_REQUIRED/SOURCE_UNAVAILABLE with attempt evidence, not EMPTY_VERIFIED or asserted market absence |
| Duplicate competitor variants and seller brands | Normalization by ad-ID, advertiser and offer-family; preserve independent supplier count |
| Child run started but portfolio index stale | Flag derived index stale, read exact child checkpoint, reconcile without inferring completion |
| Partial QC review of only two of eight required items | Preserve narrow review; parent gate stays incomplete until required artifact set reviewed |
| Semantic buyer/problem mismatch despite attractive creative | Reject source-meaning gate; return to upstream strategy/copy before visual work |
| Wrong logo or export size in one square | Recompose/re-export/review only affected variant plus dependent gates |
| Superseded owner-selected B9 logo-free and later logo-branded version | Preserve both timed approvals, supersession and exception; don't assume newest draft approved |
| Two agents claim one task without atomic coordination | Refuse “exclusive ownership” guarantee; serialize manually, or require adapter before parallel execution |
| Same GitHub login on two workers | Separate four-field logical agent identity; real test proves claim protocol, not account login alone |
| LFS stale lock after crash | Recovery/escalation record; only authorized unlock, compare to CAS alternative in tests |
| CAS ref expired; disconnected old worker resumes | Conditional takeover and fencing validation; stale completion rejected where enforced |
| Git remote unavailable during sync | Local checkpoint preserved; remote sync unknown/blocked, no claim it reached GitHub |
| JSONL torn write or current JSON snapshot mismatch | Keep last verifiable checkpoint, quarantine suspect event, no silent event loss |
| Missing remote skill while offline | Approved pinned local fallback or BLOCKED; never pretend it loaded |
| Changed custom template while run active | Keep previous effective revision, propose explicit upgrade/revision and gate invalidation |
| Changed recurring template schedule during pending occurrence | Occurrence identity and schedule revision prevent accidental duplicate |
| DST overlap or missed run after host outage | Apply configured missed/overlap policy and record decision; no implicit catch-up side effect |
| Provider Meta create times out after actually creating object | GET/list reconcile operation signature, not duplicate create |
| Unsupported per-placement Meta creative rule | Record terminal validation failure, propose authorized safe-square fallback |
| Meta activation succeeds but readback rate-limited | WRITE_ACCEPTED + VERIFY_PENDING; retry read, not write; delivery unknown |
| Parent campaign active but sibling adsets held | Inspect subtree and verify held siblings still PAUSED |
| CRM bot knowledge saved but real IG/Messenger not tested | CONFIG_VERIFIED, BEHAVIOR_UNVERIFIED, no claim that leads are routed |
| Browser and server Schedule possible duplication | Dedup test via stable event identity, consent and source; probable/unknown until proven |
| Website source committed but DEV/PROD absent | Deploy gate PENDING, no claim site is live |
| “Launch candidate” appears in research report | Treat as strategic recommendation; never activation authorization |
| Agent reports Git commit but push not checked | Local completion separate from REMOTE_VERIFIED; verify branch head and blob |
| Sensitive record accidentally included in pending public commit | Block release; sanitize and revalidate working tree/history impact |
| Reviewer shares producer account | Log logical identity, apply independent process and separate review artifact; don't claim identity cryptographically proven |
| User revokes approval after planned publication | Stop future dependent mutation; record revocation and reconcile already-performed effects |

## 20. Version 1 success tests and completion gates

The **six exact user-approved demonstrations** are mandatory. Supporting ACCEPTANCE-TEST-MATRIX.md contains specific setup, steps, expected evidence and failure assertions. A test is PASS only with an actual run record and inspected artifacts. Declare LIVE/REAL, MOCKED, MANUAL/COOPERATIVE or NOT_RUN for every required capability, not an undifferentiated green check.

| Test | Original survey criterion | Required observation |
| --- | --- | --- |
| **T01** | Real-world Ampgent workflow | Complete bounded real research (with dated actual source evidence where available), QC, synthesis and creative/marketing handoff, without unauthorized publishing |
| **T02** | Cross-platform handoff | One platform starts, another resumes from files only, accurately identifies completed/pending work and makes next authorized verified progress |
| **T03** | Collision prevention | Two workers race for same task with **enforced coordination adapter**; exactly one valid task owner and stale output rejected; standalone mode honestly cooperative |
| **T04** | Quality enforcement and correction | Deliberate failed gate blocks dependent node; targeted fix and revised QC resumes only affected branch |
| **T05** | Dynamic revisions | Update active graph, preserve completed work/old versions and event history, invalidate affected dependencies, resume correctly |
| **T06** | Move Git repository and resume | Migrate active run and source pointers to a different test Git repo/clone, explicitly reconfigure remote, verify no lost state and continue |

**Prompt 01b additional mandatory tests:**
- **T07** no-Git copied folder and single-agent restart with bundled master and custom/run skills.
- **T08** recurring-capable template launched ad hoc, distinct manual versus scheduled occurrence identity and an honest no-scheduler test.
- **T09** scheduled duplicate/overlap/missed trigger handling when a host trigger is available or controlled mock (label MOCKED if so).
- **T10** just-in-time skill resolution, pinned external reference if access exists, untrusted/missing skill blocked, no authority escalation.

**Research-derived resilience tests:**
- **T11** ambiguous external create/provider timeout reconciliation without duplicate (mock or explicitly approved test account).
- **T12** rate-limited readback after accepted write never triggers a duplicate write.
- **T13** two independent creative versions, only one failed square/logo; preserved successful portrait and version-specific approvals.
- **T14** stale summary/partial QC and torn-state recovery are detected, not silently considered complete.
- **T15** staged PAUSED versus authorized live activation with held siblings and actual readback distinctions.
- **T16** Pixel/CAPI/CRM simulated or safely authorized consent, event idempotency and real milestone classification, with unknown preserved if not testable.

**Release gating [PROPOSED]:** T01–T08 and T10 must pass at the appropriate actual capability level; T03 requires real two-client coordination (a mock by itself is insufficient). Scheduled host tests may be MOCKED when no optional scheduler host is part of the release, but product copy must not claim unattended scheduling works. T09 and T11–T16 need at least controlled scenario evidence and honest scope; marketing providers' real account operations remain optional and require owner permission. A failure in a core six survey test blocks V1 acceptance.

### 20.1 Evidence record for each acceptance test

Required test log fields: test ID, PRD revision, software/framework revision, environment/mode and capabilities, source/template/run revisions, actor, actual steps, expected versus observed result, artifact/commit references, LIVE/MOCKED/MANUAL/NOT_RUN classification, PASS/FAIL/BLOCKED, caveats, reviewer and unresolved corrective action. For T03 collect racing request timings and authoritative remote claim outcomes; for T06 collect old/new repository refs and post-move handoff. For external provider tests, store only sanitized or private references as appropriate, never publish real customer or account data.


## 21. Dependency-ordered implementation roadmap

**Status:** Implementation has **not** begun. These milestones become eligible only if the owner approves this PRD, including any requested modifications. Prompts 08–19 are the existing agreed implementation/test plan, not work authorized by merely reading this section.

| Milestone | Planned prompt | Depends on | Deliverable and exit evidence |
| --- | --- | --- | --- |
| **M0 Requirements approval** | 07 | Prompts 01–06 research | Owner reviews PRD, survey trace, decisions and acceptance contract; explicit approval or change request. **Stop here now.** |
| **M1 Architecture and schemas** | 08 | Approved M0 | Accepted protocol terms, folder schema, task graph, event/snapshot consistency, identity, authorization, schedules and skills resolution with migration/version contract |
| **M2 Minimum portable folder** | 09 | M1 | Downloadable scaffold/aos-w with protected/read-mostly base and writable agent-files, start guide, manual single-writer walkthrough |
| **M3 Template/graph execution protocol** | 10 | M2 | Composition, parameters, inheritance, loop/conditional/parallel eligibility, dynamic child proposals and join, manual/scheduled occurrence metadata |
| **M4 Durable state and recovery** | 11 | M2–M3 | Versioned events/state/handoff, intentional interruption tests, bounded retry and explicit unknown external action |
| **M5 Identity, permissions, QC and skills** | 12 | M3–M4 | Task ownership, four-field provenance, reviewer gates, artifact-specific approval, permission matrix and step-local skill resolution |
| **M6 Optional Git and coordination trials** | 13 | M4–M5 | Git sync workflow and actual LFS versus atomic Git claims prototype, documented same-account races and stale-lease limitations |
| **M7 Optional tool adapters and packaging** | 14 | M2–M6 | Optional deterministic validator/packager, tested independent folder archive; no new mandatory runtime requirement |
| **M8 Sanitized Ampgent examples** | 15 | M3–M7 | Verified research queue, vertical portfolio, creative QC and staged/mock marketing templates, no private account data |
| **M9 Offline single-agent acceptance** | 16 | M8 | T01 as applicable, T04–T05, T07–T08, T10 and recovery cases with honest cooperative-mode labels |
| **M10 Git and cross-platform coordination acceptance** | 17 | M6/M9 | T02/T03/T06 and recurring duplicate-trigger test; real race evidence, failure recovery, no unproven exclusive guarantee |
| **M11 End-to-end marketing pilot** | 18 | M8–M10 | Bounded sanitized research → approved creative → simulated/authorized paused Meta+CRM handoff and discrepancy handling |
| **M12 Release audit and owner review** | 19 | All prior milestones | Requirement trace PASS/FAIL, security/sanitization and license decision, compatibility and migration docs, explicit acceptance of any limitations |

**Critical path:** PRD owner approval → schemas → installable core → reusable graph/state → QC/permissions/skills → optional coordination adapter → examples and tests → release review. Parallelize independent documents/examples only after stable contracts, not at the cost of incompatible schema forks.

### 21.1 Stage-specific constraints

- M1 must resolve or explicitly defer D-01 through D-08 without violating the approved baseline. A change requiring owner policy approval goes back through review.
- M2 can function manually with no Git, database, Python, Node, cloud service, scheduler or MCP server.
- M3/M4 must distinguish declaration from actual task dispatch. Do not claim auto retries or parallel execution without a running agent/host.
- M6 must prototype **both** contested locking approaches, and cannot select a winner merely by reading documentation.
- M8 uses generalized examples; raw Ampgent internal assets, accounts and transcripts do not enter this public repo.
- M11 may use mocks/PAUSED staging depending on separate owner permissions. Live production ad activation and spend are never inherited from approval of this PRD.
- At every stage, maintain temp/PROGRESS.md, temp/HANDOFF.md, implementation history and committed verification; exact branch SHA must be observed.

## 22. Architecture alternatives and consequences

The following alternatives were studied in Prompt 06. None is a silently accepted final implementation decision. The original no-mandatory-runtime constraint eliminates some as V1 foundations.

| Approach | Benefit | Disadvantage | PRD disposition |
| --- | --- | --- | --- |
| Plain Markdown-only checklist | Minimal installation, easy for any model | Inadequate machine state, dependency integrity and collision detection | Not sufficient alone |
| **File-first workflow graph with optional adapters** | One portable spec; readable, recoverable, environment-neutral | Manual agents cannot enforce atomicity or timing on their own | **Preferred PROPOSED basis** |
| Mandatory LangGraph runtime | Real graph scheduling, checkpoints, interrupts, reducers, retries | Requires installed software/execution environment and checkpointer configuration | Borrow patterns only, optionally integrate in future |
| Mandatory A Rep PRIMARY | Mature agent goals, notifications, heartbeat, provenance | Duplicates/depends on agent-specific lifecycle, excludes dormant Max and generic standalone users | Optional integration only |
| Mandatory database/MCP coordinator | Stronger possible concurrency/transactions with a service | Violates lightweight offline standalone requirement | Defer, not required |
| Git-only state and locks | Existing versioning and widely available collaboration | Network/account/Git dependency, lock limits, offline inaccessible | Optional sync/coordination |
| Git worktrees alone | Separate code/artifact branches per agent | No task-exclusivity guarantee across hosts | Optional isolation tool |
| Git LFS locking | File-level remote locks, useful for binaries | Path/account identity, stale unlock, client/remote dependencies | Prototype and compare, not preselected |
| Atomic Git claims | Logical per-task remote refs, supports shared transport plus logical identity | Correct CAS/fencing/lease recovery is nontrivial and backend-specific | Provisional research preference only until actual tests |

### 22.1 Chosen constraints versus proposed decisions

**Already agreed:** public repo, folder distribution, agent-files-only ordinary writes, mixed Markdown/YAML/JSON(L), optional Git, all five prototype modules, six V1 demonstrations, four-field agent identity, QC/approval policy variety, workflow-specific autonomy and revision policy, default non-repeating plus optional schedule, per-template/run skill bundles and remote refs.

**Proposed ADRs requiring review:** ADR-001 file-first single spec, ADR-002 run snapshot/events, ADR-003 capability layers, ADR-004 Git claim trials, ADR-005 skill trust, ADR-006 recurring trigger separation, ADR-007 A Rep boundary, ADR-008 side-effect guardrails. See temp/architecture/adrs/. The mere fact that they are written in this PRD does not set their status to ACCEPTED.

### 22.2 LangGraph and A Rep alignment

Borrow LangGraph's graph terminology, thread/run-like identity, checkpoint boundaries, conditional edges, parallel branch join, interrupt/approval gates, bounded RetryPolicy mindset and replay/side-effect caution, while being explicit that these are file protocol descriptions in standalone mode. A Rep's optional plan-work remains an agent-level planning aid; AOS-W's instance is a bounded workflow, not a rival global priority queue. Max needs no scheduler, Fred can optionally trigger a workflow from its existing PRIMARY/Issue mechanism. Both remain governed by current human instructions and source-of-truth providers.

## 23. Decisions requiring owner review, and items deliberately unresolved

This register is normative for **what remains undecided**. Recommendations below are not defaults to be silently implemented. A decision may be assigned to Prompt 08 schema design when it does not change owner-facing product scope; changes to authority, default autonomy, cloud/external services or licensing require explicit owner review.

| Decision | Question and proposed direction | Owner/action milestone |
| --- | --- | --- |
| **D-01 Folder details** | Keep agent-files the sole mutable zone; decide workflows versus runs nesting, names, cache and manifest layout | Prompt 08 schema, owner review if semantics change |
| **D-02 Inheritance precedence** | Base → custom → instance → step, never override a protected human gate; exact precedence/conflict/merge language undecided | Prompt 08, approve policy rules |
| **D-03 Predicate grammar** | Prefer finite declarative comparisons and UNKNOWN branch, no arbitrary executable YAML | Prompt 08 technical decision |
| **D-04 Lifecycle/QC enum** | Distinguish status domains and UNKNOWN, exact names/transitions/waiver semantics TBD | Prompt 08 schema |
| **D-05 Snapshot/event authority** | Current JSON + chronological JSONL, define torn-write recovery and what dominates a mismatch | Prompt 08 schema and test |
| **D-06 Multi-agent lock winner** | Must prototype Git LFS **and** atomic Git CAS under same credentials, stale leases and outages; neither proven | Prompts 13/17 empirical selection |
| **D-07 Schedule rules** | RRULE versus cron/portable notation, timezone/DST, missed/overlap policies, dedup and host adapters | Prompt 08, owner acceptance of defaults |
| **D-08 Skill resolution** | Exact installed/bundled/remote precedence, pin/trust and code execution permissions | Prompt 08, owner approval for privilege implications |
| **D-09 V1 external integration depth** | Bounded marketing pilot with mock/paused side effects; decide whether any real Meta/GHL test account integration is required for acceptance | Owner before Prompt 18 |
| **D-10 Open-source license** | No license yet; decide before release | Owner before Prompt 19 |
| **D-11 Cloud durability guarantee** | Define minimum host persistent storage/atomic write capability and fallback under ephemeral cloud agents | Prompt 08 then Prompt 16/17 test |
| **D-12 Claim lease/reclaim** | Fencing token, timeout, abandoned owner reassignment and offline conflict policy | Prompt 13/17 proof and owner policy |
| **D-13 QC waiver / autonomy** | Default human approvals for consequential actions agreed, but exact waiver powers and level-dependent automatic repair privileges remain to be settled | Owner before implementation affecting permissions |
| **D-14 Dynamic child authorization** | Historical 15 runs separately approved; configure when generated children may auto-start under explicit prior scope | Owner/Prompt 08 |
| **D-15 Artifact hashes and migration** | Required hash types for text/images/provider mappings, run version pin/upgrade process | Prompt 08 technical design |
| **D-16 A Rep compatibility release** | Public A Rep CURRENT says 1.5.0, main SKILL.md says 1.5.1; Fred installed host version unverified | Check actual host at integration test, no false assumption |
| **D-17 Source data model** | Ad offer-family ledger and seller/vertical scoring need distinct rubrics, can share provenance envelope | Prompt 08 template schema |
| **D-18 Review independence strength** | Cooperative distinct reviewer in standalone mode; host-enforced access isolation optional | Owner accepts guarantee wording, technical host support later |
| **D-19 Measurable performance targets** | No owner-defined latency, storage or concurrency SLO; propose testing useful small pilot rather than inventing target | Owner/Prompt 08 |
| **D-20 Public release boundaries** | Example data rights, sanitized assets and limits on retaining local sensitive runs in Git mirrors | Owner policy and pre-release audit |

**Decisions from the user must not be reopened silently.** This includes repository identity, no mandatory tool/runtime, protected framework folder, workflows configured per use case, public sanitized distribution, and all six success demonstrations.

## 24. Source, traceability and document governance

### 24.1 Primary decisions

- **Original 16-question survey** consolidated in temp/DESIGN-DECISIONS.md; supporting per-question audit in docs/specs/prd/SURVEY-TRACEABILITY.md.
- **Prompt 01b user refinements**, temp/CONCEPT-NOTES-01B.md, requiring optional scheduled recurrence and per-template/run skill bundles with lazy loading.
- **Project work plan and handoff**, temp/WORK-PLAN.md, temp/HANDOFF.md, temp/PROGRESS.md, with research before PRD and an explicit owner approval checkpoint.

### 24.2 Historical Ampgent primary research

- Prompt 02 sanitized evidence index: temp/research/SOURCE-INDEX.md and WORKFLOW-PATTERNS.md.
- Prompt 03 research queue, 15-run vertical studies and source/evidence rubric: temp/research/RESEARCH-WORKFLOW-MODEL.md, RESEARCH-EVIDENCE-QA.md, VERTICAL-RESEARCH-LINEAGE.md and candidate-templates/CATALOG.md.
- Prompt 04 image/copy/creative and independent QC: temp/research/creative-production/CREATIVE-PRODUCTION-MODEL.md, QA-GATES-AND-APPROVALS.md and candidate-templates/CREATIVE-CATALOG.md.
- Prompt 05 Meta/website/HighLevel launch and conversion state: temp/research/campaign-operations/WORKFLOW-MODEL.md, FAILURES-AND-AUTHORITY.md, CRM-TRACKING-LESSONS.md and PRD-RECOMMENDATIONS-05.md.

These summarize private source materials and must not be interpreted as freshly verified live Meta, GHL, website or customer data. The public PRD intentionally uses process and mock examples, not confidential artifacts.

### 24.3 Technical research and proposed ADRs

- Prompt 06 source register: temp/architecture/SOURCES-06.md, including A Rep/Fred/Max source inspection and LangGraph, Agent Skills and official Git references.
- Alternatives and modes: temp/architecture/ALTERNATIVES-COMPARISON.md and ENVIRONMENTS-AND-MINIMAL-CORE.md.
- Git coordination limitations: temp/architecture/COORDINATION-AND-LOCKING.md.
- Skills and scheduling: temp/architecture/SKILLS-SCHEDULING-AND-SECURITY.md.
- Proposed ADR-001 through ADR-008 in temp/architecture/adrs/.

### 24.4 Related PRD review artifacts

- **SURVEY-TRACEABILITY.md** traces all sixteen user answers, subsequent changes and PRD coverage.
- **ACCEPTANCE-TEST-MATRIX.md** provides reproducible expected behavior, positive/negative tests and live-versus-mock documentation.
- **DECISION-REGISTER.md** organizes agreed, proposed, unresolved and deferred decisions.
- **APPROVAL-REVIEW.md** gives the owner a focused approval checklist and identifies the exact implementation stop condition.

### 24.5 Document lifecycle and approval

- Current PRD status: **DRAFT FOR OWNER REVIEW**.
- Approved baseline decisions remain in temp/DESIGN-DECISIONS.md. Research findings and draft ADRs do not override them.
- Owner may approve, reject, or request changes to PRD. Any revisions must keep a version history and note material differences.
- **No implementation begins from this draft, no ADR becomes ACCEPTED automatically, and no live account actions are authorized.**
- On explicit owner approval, change PRD status and selected ADR statuses using a recorded owner decision/commit, then begin Prompt 08 technical architecture within approved scope. If the owner requests changes, revise this document and present it again for approval.

---

**End of PRD v1.0-rc1.** Further implementation is blocked pending explicit owner approval.
