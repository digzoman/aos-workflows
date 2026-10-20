# Architecture alternatives and smallest reliable V1

Date 2026-10-20. **Proposals** informed by the user baseline in `temp/DESIGN-DECISIONS.md`, source index [SOURCES-06.md](SOURCES-06.md), LangGraph mapping and existing A Rep design. No alternative was implemented/tested under Prompt 06.

## Execution and persistence strategy

| Architecture | Manual download/no tools | Enforced automated DAG/interrupts | Multi-agent remote arbitration | Maintenance/portability | Decision status |
|---|---|---|---|---|---|
| **A. File protocol + cooperative agent** | Yes, agent needs basic file read/write | Instructions/checkpoints only; enforcement not guaranteed | No exclusive claims without optional adapter | Lowest, easiest to audit | **Recommended minimum core** |
| B. File protocol + optional provider adapters | Yes if adapters omitted | When installed host supports scripts/automation | Possible with selected adapter | Moderate; one spec across modes | **Recommended extension** |
| C. Mandatory LangGraph runtime + checkpointer | No; requires programming runtime and integration | Stronger configured graph execution | Needs durable shared checkpointer/service & concurrency design | Significant dependency and coupling | Reject as mandatory, study concepts |
| D. Mandatory A Rep runtime and GitHub Issues | No; requires specific agent host/wake and repository | Nondeterministic PRIMARY, not same as enforced graph | One PRIMARY runtime lock; no multi-agent task guarantee | Redundant agent orchestration | Reject as dependency, allow integration |
| E. Required DB/central MCP orchestrator | No | Can enforce transactions and scheduler with well-engineered service | Potentially strongest if centralized | Violates first-install lightweight goal | Defer outside V1 |
| F. Markdown instructions only, no machine state | Yes | None | None | Lowest complexity but poor reliable restart | Insufficient for V1 acceptance |

**Recommendation:** A+B. First write a clear portable declarative contract and cold-start runbook. Allow optional deterministic host adapters for file operations, Git claims, provider tools, linting, actual timers and QC rendering. If a claimed guarantee cannot be enforced in the current environment, show a degraded state rather than claiming success.

## Major design comparisons

| Concern | Option 1 | Option 2 | Proposed direction |
| --- | --- | --- | --- |
| Core workflow graph | Flat imperative checklist | Versioned stable task graph with conditions and child runs | Task graph, but plain instructions readable first |
| Checkpoint representation | Markdown-only | JSON current state + JSONL events, Markdown human notes | Separate machine and human views; exact schema at Prompt 08 |
| Recovery | Resume past chat | Resume durable state plus observed provider truth | Durable run is source of truth for run progress |
| Automation | Mandatory daemon | Optional host wake / manually invoked | Optional host; schedule declarative |
| Skills | Global injected skill catalog | Step-local pinned skill packages and resources | Just-in-time Agent Skills; trust/version controls |
| Git sync | Required for all | Optional mirror mode configured in agent-files | Optional, no Git for standalone |
| Concurrent claim | File name says CLAIMED | Verified atomic primitive + fencing/lease | Exclusive claims only where host can enforce |
| Cross-agent review | Any agent says PASS | Named reviewer, exact artifact/hash, rubric and scope | Version-bound QC independent from permissions |
| Provider updates | Script assumes write worked | Submitted response + external readback + recovery | Provider readback authoritative |
| A Rep integration | Replace existing plans/PRIMARY | Link authorized Issues and workflow runs | Independent but interoperable |
| Indexes | Manually authoritative tracker | Derived from per-run facts/events | Derived with stale warning |
| Background recurring tasks | Schedule string implies execution | Due schedule plus optional host trigger | Do not claim unattended action offline |

## Minimum 8-step agent protocol to specify later

1. **Recover** exact installed scaffold/template/revisions and per-run state, ownership, permissions and unresolved errors.
2. **Observe** current host capabilities and external truth required by the next step; log inability to verify.
3. **Select** next eligible authorized task, dependency and review gates, not the next arbitrary paragraph.
4. **Claim** task if multi-agent mode and a tested coordination adapter are configured; otherwise confirm local single-writer assumption.
5. **Execute** bounded work, with necessary step-local trusted skills, and record attempted external operation key before side effect.
6. **Verify** outputs, exact artifact versions, expected provider readback and QC reviewer requirement.
7. **Checkpoint** canonical state/events/handoff durably, with optional Git sync if configured.
8. **Release/stop** task claim, report blockers and next authorized action; don't automatically start unapproved downstream work.

Each step is a **proposed future procedure**, not evidence that a current runtime can perform it.

## Product positioning

AOS-W is a repeatable workflow standard and durable collaboration layer; A Rep is a persistent agent operating system; LangGraph is an executable graph orchestration library. Borrow specific properties where useful but don't conflate these product layers.

The practical smallest V1 needs enough recorded state to support the six agreed user demonstrations while clearly separating advisory/manual from strongly-enforced concurrent operation. Eight ADRs remain proposed until owner review.
