# AOS-W execution environments and minimum reliable design

**Proposed architecture**, not implementation. User requirements are in `temp/DESIGN-DECISIONS.md`; A Rep and external primary docs listed in [SOURCES-06.md](SOURCES-06.md).

## One workflow specification, orthogonal capabilities

Do not create separate offline versus online **workflow languages**. The same template/instance describes tasks, identity, dependencies, conditions, QC/approval, source-of-truth, retry bounds, provenance, skills and triggers. Environment-specific capabilities are recorded in project-local `agent-files/` configuration.

| Scenario | Files and persistence | How work advances | Concurrency guarantee |
| --- | --- | --- | --- |
| Local standalone, one agent | Ordinary downloaded folder | Manually invoked agent reads/writes snapshots and evidence | No multi-agent guarantee; safe under single active writer assumption |
| Cloud standalone, one agent | Persistent hosted filesystem or workspace | Manually invoked/cloud agent, optional host-triggered wake | Needs proven file durability; no Git required; don't assume ephemeral VM survives |
| Git-synchronized, single agent | Local/cloud files plus remote Git mirror | Before work inspect configured sync state, after work sync verified changes | Optimistic conflict detection for sync, **not** an exclusive task lock unless claim protocol enabled |
| Shared multi-agent on one filesystem | Same `agent-files/` visible to workers | Agents independently claim eligible tasks via host-supported atomic mechanism | Exclusive claim only if filesystem lock/create/compare semantics proved; plain text alone advisory |
| Shared multi-agent on Git remote | Separate local working copies plus shared task coordination refs | Sync and claim through optional Git adapter | Mutually exclusive claims only with tested remote atomic compare/claim and fencing |
| Other shared cloud storage | Provider-native shared directory or documents | Agent interacts through available connector | Version-precondition/transaction necessary; if absent, collaborative mode must degrade to single writer/manual arbitration |

Cloud-hosted does not imply multi-agent, and Git-synchronized does not imply full collaboration. The first two are storage and execution **location**; the third is sync; the last two describe verified coordination ability.

## Smallest useful persistent file contract, proposal

- **Framework read-mostly** `scaffold/aos-w/`: README/runbook, template(s), lightweight format spec, common skill instructions and optional tools references.
- **Only writable runtime zone** `scaffold/aos-w/agent-files/`: `settings`, custom templates/skills, active workflow instances, run snapshots, append-style events, artifacts/evidence, claims, reviewers/approvals, handoffs and optional Git metadata. Exact naming/schema deferred to Prompt 08.
- Markdown describes human-friendly intent, instructions, approvals and why; YAML describes task graph and conditional/approval structure; JSON stores canonical per-run/task machine state; JSONL can store chronological events. A self-contained instance references immutable template/revision and its own declared skills.
- **Logical event and snapshot authority:** propose versioned state snapshot for cheap recovery, plus durable event log for audit and incremental rebuild. If disagreement/corruption occurs, reconcile from verified events/artifacts and stop rather than guessing. Don't claim full event sourcing or transactional atomicity without tested host semantics.
- Generated portfolio index and status summaries are views, not primary authoritative state. One complete workflow run should have its own stable ID even when a template is recurring.

## Portable protocol vs necessary execution environment

| Portable files can describe | Can't enforce absent host capabilities |
| --- | --- |
| Graph nodes, conditions and next-eligible task instructions | Invoke agent automatically, evaluate arbitrary code or ensure agent obeys |
| Artifact paths, expected hashes, QA gate and reviewer policy | Compute hashes/image pixel metrics unless agent/host provides tools |
| Leases with owner and expiry hints | Block conflicting writer, fence stale owner or atomically reclaim |
| `WAIT_HUMAN` and approved-scope rules | Guarantee a malicious/misconfigured agent cannot write externally |
| Retry strategy and after-time timestamps | Wake, backoff, send one external request exactly once |
| Schedule expression, timezone and default ad hoc behavior | Time-trigger runs while everything is off |
| Git remote setting and sync instructions | Ensure network/repo access, avoid Git race without lock protocol |
| Remote skill locator, trust state and version pin | Authenticate/read/evaluate/execute skill securely |
| Human and peer approval instructions | Enforce reviewer independence if all agents share uncontrolled reads |
| External write plan and provider preconditions | Execute safe Meta/CRM actions and verify actual business outcome |

Call the file-only mode **cooperative/manual**, not a strongly enforced orchestration engine. It can still be useful and auditable if agents obey instructions.

## Minimal V1 choice for Prompt 07 review

1. Launch one human-readable `WORKFLOW.md`/YAML task set and append task outcome/checkpoint into `agent-files/`.
2. No mandatory interpreter, Git, host service, LangGraph, database, scheduler, external API or Python.
3. Agent follows an explicit startup/claim/check/action/verify/checkpoint/handoff/stop runbook.
4. One authoritative run state and event trail; all generated indexes derived, not competing.
5. Explicit `capability_status` so a missing network/browser/clock/file tool causes BLOCKED or PENDING rather than fabricated success.
6. For shared collaboration, **opt in only to a verified coordination adapter**. Without one, allow parallel *planning* but warn exclusive tasks are cooperative and require manual serialized ownership.
7. Stable component IDs, parent-child, revision and artifact hashes enable minimal retry/review invalidation.
8. Optional scripts/adapters can later perform real atomic claims, linting, scheduling, Git sync and external provider actions. Do not move their dependencies into the minimum standalone package.

This approach satisfies portability first without representing untested constraints as guarantees.
