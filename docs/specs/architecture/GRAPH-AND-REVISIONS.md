# Workflow graph, eligibility, composition and versioned revisions

## Definition and graph invariants

A template graph contains nodes with **stable IDs**, task kinds `task`, `review`, `approval`, `join` and optional `child_generator`. Each has `needs` dependencies, output contracts, optional skills, retry and QC policies, optional deterministic `when` predicates and downstream implications. A compound workflow can include child template references pinned to exact version or content digest. A graph is a DAG after expansion, and every generated node/child ID must be unique within its run.

Graph edges express **eligibility** and desired data flow, not an automatically running thread or a message bus. An executor or manually following agent advances READY tasks, while durable events specify accepted outcomes.

## Predicate semantics

Conditions are declarative expressions `{"op":"eq","path":"tasks.research.result","value":"complete"}` or `and/or/not`, `exists`, `in`, `gte` and `lte` over previously verified local run data only. Missing data or stale/unverified source resolves to **UNKNOWN**. No embedded JS/Python/eval/shell execution as predicate. `when` TRUE enables, FALSE skips branch only when all incoming alternatives are conclusively closed; UNKNOWN blocks/WAIT rather than treating missing evidence as false. Exact operator set is a technical design candidate to test and may be narrowed before engine release.

## Formal next-eligible task rule

A node is READY when, for the **current graph revision**, all of the following are true:

1. Node is instantiated, not CANCELLED/SUPERSEDED and has no completed valid result for the exact current input versions.
2. All required `needs` are COMPLETE or ACCEPTED with appropriate current QC, with artifact versions matching the node's declared required inputs.
3. Its edge and node predicate evaluates TRUE; FALSE means SKIPPED only if no other incoming path can make it eligible; UNKNOWN means WAIT_CONDITION.
4. All hard prerequisites (required skill resolvable, policy/context, declared hosting capabilities, source access) are verified; otherwise BLOCKED or MANUAL_REQUIRED.
5. Any required **before-execution** authorization exists for the precise action scope and is unexpired/unrevoked. Post-task QC/owner approvals do not preauthorize earlier side effects.
6. Existing external operation attempts that could have had side effects have been reconciled; UNKNOWN effect blocks retry.
7. If exclusive coordination is requested, verified backend claim can be obtained before mutating output. Otherwise only single-writer/manual cooperative mode may proceed.
8. Retry attempts do not exceed declared ceiling and any next-eligible-after time or required human escalation is satisfied.
9. A ready task is not already claimed/running by another valid owner; stale claims require audited reclaim.

An agent may **list** candidate READY tasks before claim, but only a verified atomic claim grants exclusive right in shared mode. Claim does **not** confer external-action permission.

## Node completion and downstream propagation

A task COMPLETED means required local outputs and completion predicates verified for a pinned artifact set, not that QA or authorization automatically passed. REVIEW_WAIT means independent evaluation pending. ACCEPTED is a gate verdict allowing dependents under relevant policy. A failed gate produces NEEDS_REWORK and blocks only dependents. Untouched independent sibling tasks stay eligible if they do not need the failed result.

For conditional branches, path selection event persists value/evidence/predicate revision. On a changed input/predicate the branch decision becomes STALE and dependent outcomes need impact analysis; retain original choice as audit. Do not erase skipped branches, retain `SKIPPED_BY_CONDITION` with decision reference.

## Composition cases

**Sequential:** `A -> B -> C` with each `needs` depending on accepted predecessors.

**Parallel:** after `plan`, tasks `research-a` and `research-b` have no dependency between them and write separate output directories. An agent may run sequentially under standalone mode; a verified claim adapter supports real concurrent workers.

**Conditional:** `source-check` yields `verified`, `blocked`, `unknown`. Verified enters `analyze`; blocked triggers `retry-source` under bounded policy; unknown waits/human authorization. No inference of “no competition” from blocked source.

**Dynamic fan-out:** parent `plan-approved` can create a `child_generation_proposed` event with specs for 15 verticals (stable IDs computed from parent, slug, source revision). Each starts PROPOSED, authorization according to preapproved scope; child gets its own run and origin. No duplicate child if proposed again after crash. `fanout_revision` stores identities.

**Merge/join:** policies `all_accepted`, `any_accepted` or `quorum` with explicit threshold and missing/failed handling. The merge includes source IDs, revisions, QC decisions, contradictory evidence, rubric versions and confidence; it does not overwrite child reports. `quorum` and `any` must have documented authorized acceptance, never default as a workaround for missing research.

**Compound/subworkflow:** parent passes immutable scoped parameters and allowed actions to pinned child instance; child cannot expand capabilities/permissions above parent. A parent with durable handoff can resume independent children in another session.

## Template inheritance and version freeze

Inheritance resolves **base template -> custom template overlay -> instance override -> permitted run-specific overrides**. All resolved values and origin revisions stored in a `template-lock.json` and immutable graph-revision file under the instance. Rules:

- Scalars can override only if field is marked overridable in parent.
- Object maps merge by named key with explicit deletions, with protected fields non-overridable without owner approval.
- Arrays `nodes`, `skills`, `default_gates`, `allowed_actions` are keyed collections. Merge by stable IDs rather than numeric positions.
- Permission sets are **intersection** with protected owner ceiling; adding an action requires explicit separate owner approval. Human-required actions remain protected.
- Gate strengthening is allowed; weakening independent/human hard gate needs separate authorized policy change and graph revision.
- Retry budget cannot silently increase beyond protected ceiling or call external providers more often than approved.
- A missing/ambiguous override rule blocks resolution, not silently uses permissive default.

Resolved snapshot is copied to `agent-files/instances/<id>/template-snapshots/`; **never read a changing master template HEAD as the active run's graph**.

## Active graph revision transaction

1. Propose `graph_revision_requested` with base graph revision and reason/actor.
2. Build candidate new pinned graph; calculate node change/diff (new, removed, changed params/skills/permissions/inputs/outputs).
3. Derive impact closure, starting with changed nodes and all downstream nodes depending on stale output/changed gate. Record unchanged completed nodes as reused with exact hashes.
4. Check workflow's autonomy revision policy; material claims/pricing, protected gates, live actions, budget, child scope need required human permission. A reviewer cannot waive policy just because it is convenient.
5. Acquire a verified graph-update claim if shared mode; otherwise single-writer. Verify base revision unchanged at commit.
6. Persist new immutable graph revision and `graph_revised` event; update instance pointer and state snapshot only after verification. Preserve old events and artifacts.
7. Mark impacted completed results as STALE/SUPERSEDED for the *new* revision, not retroactively FAILED; invalidate old QC/approval use on changed resource versions. Keep unaffected work valid.
8. Re-evaluate conditions, task eligibility and joins. Preserve explicit rationale/decision in handoff.
9. On conflict/power loss, reconcile expected base revision and event state; do not silently apply two competing graph edits.

## Examples

- **Wrong logo** on one square: invalidate square branding/export/visual review/selected approval plus downstream Meta mapping, but not research, original copy or accepted portrait.
- **Changed $47 price**: invalidates offer claim/copy and text-containing images; related creative QC and provider ad mapping must be revisited. Unaffected competitor source evidence remains.
- **Stale portfolio index**: recompute index from child run events; don't mark child NOT STARTED if it has verified started event.
- **Interrupted dynamic generator**: reloading same proposal IDs results in no new duplicate children; queued proposals remain distinct from authorized/started runs.

This is a specification. Exact implementation mechanics and automated validator behavior remain Prompt 09–12 and test work, not achievements of Prompt 08.

## Prompt 10 implementation status (2026-10-20)

The 0.2.0 file-native scaffold now includes a planning-to-independent-research composition example and optional local PyYAML helper, as documented in `scaffold/aos-w/references/COMPOSITION.md`. Eleven local conformance tests cover stable child proposals, exact mocked instantiation scope, current independent review-before-merge, permission-constrained overlays, conditional readiness and downstream revision impact. Automated dispatch, real multi-agent coordination and **application** of immutable graph-revision events remain subsequent work. Python is optional; the manual protocol remains the required portable baseline.
