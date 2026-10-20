# Reusable templates and composition, portable procedure (0.2.0)

AOS-W's **authoritative template is YAML**. These procedures are sufficient for a capable agent with ordinary file reading/writing. The optional `tools/composition/` helper uses Python + optional PyYAML, but neither Python nor Git nor a scheduler is required by the downloaded scaffold.

## 1. Master, custom and resolved instances

* Read-only masters are in `templates/<id>/template.yaml`. Each node must have a stable `id`, `kind`, `needs`, explicit `inputs`, `outputs`, `quality.gates`, `contract.done_when`, `instructions` and intended `required_actions`. Changes to these protected files are framework releases, not ordinary workflow writes.
* Custom overlays belong in `agent-files/custom-templates/<id>/template.yaml`. They declare the exact base template `template_id`, `version`, **SHA-256 of its original YAML bytes**, and a bounded set of node patches (`add`, `replace`, `remove`) each with a reason. Custom policy can narrow allowed actions and concurrency, not increase them or remove protected gates.
* At instantiation, resolve base + accepted overlay + parameter values; save a **copied fully resolved source** to `agent-files/instances/<id>/template-snapshots/<content-id>/template.yaml`, pin the source revision/digest in `template-lock.json`, and create immutable `graph-revisions/g0001.yaml`. Never follow master HEAD to resume an existing instance. On framework upgrade, retain pinned snapshots and all `agent-files`.
* Parameter types are strings, numbers, booleans, arrays or objects with `required`/`default` fields. Reject unknown parameters, missing required values and incompatible type. Store actual resolved values in `instance.json`. Recompute digest when source changes.

## 2. Sequential, parallel and conditional routing

`needs` is the sequence/dependency contract. Independent nodes sharing only a completed predecessor may be processed sequentially by one agent or in parallel **only if** a tested coordination mechanism prevents conflicting writes. Each step writes its own files, never a common output without a declared join/reconciliation policy.

A predicate uses declarative operators `eq`, `neq`, `in`, `exists`, `gte`, `lte`, `and`, `or`, `not`. Values come only from verified run context. Resolve to TRUE, FALSE, **UNKNOWN**. Unknown never becomes false merely because a source is inaccessible; wait or follow an explicitly approved UNKNOWN branch. No executable expressions are loaded from a template.

A task's computed status:

* `completed` if a recorded current exact-version completion exists, with any required downstream review handled separately.
* `failed` if its task record is FAILED/NEEDS_REWORK, preserving the attempt and allowing a bounded correction.
* `blocked` for BLOCKED, RECONCILE_REQUIRED, canceled, missing permissions/capability, unknown external effects or an unverified exclusive claim in shared mode.
* `waiting` when a predecessor is incomplete, version-bound review is absent, input evidence is missing, condition UNKNOWN/FALSE, join children pending, another actor currently owns the claim, or task is already in progress.
* `ready` only when all required predecessor status/reviews, verified input artifacts, condition TRUE, relevant skills/capabilities, pre-execution action permission and ownership checks pass.

Readiness is **computed**, not an implicit permission to execute. Before performing an external account action, check a separate current owner authorization for that exact action, objects, budget, version and exclusions. A completed or PASS result never itself authorizes publishing.

## 3. Planning → distinct child proposals → approved child instances

The parent master `research-portfolio-planner` runs `define-verticals -> approve-plan -> propose-investigations -> synthesize`.

1. Save a versioned `portfolio-plan.json` from research planning. Each proposed vertical has a stable slug, buyer, research focus and market. `approve-plan` must genuinely record owner/reviewer permission and source revision. The conformance fixture's `approved_input:true` is **simulated test evidence** only.
2. Convert approved plan items to **deterministic proposals** using `plan_id` + slug + plan revision; reject duplicate slugs. Each child proposal includes a distinct instance/run ID, exact child template/version, explicit parameters, inputs, outputs, quality gates, per-step dependencies and execution contracts. Re-running the same plan yields the same proposal IDs. **Proposed does not mean authorized or started.**
3. Obtain an independent scoped instantiation approval with `decision: GRANTED`, `scope: instantiate_children`, exact `plan_id`, revision, proposed IDs, source YAML SHA-256 and issuer. Under a manually trusted owner, create the child instance/run directories inside `agent-files/` with pinned template bytes, immutable graph, initial CREATED state, a run_created event and handoff. Duplicate existing IDs are a hard stop, not overwritten.
4. Work on the independent child workflows. Each must produce real dated competitor evidence and undergo independent `evidence-qc` with a review of its **current artifact versions and full required set**. A provisional or unverified source, timeout or merely saved research file does not count as PASS.
5. The parent `synthesize` join remains waiting until every required child is COMPLETE with a current passing review. A separate scoped `synthesize` approval is required. A read-only result merge references accepted child artifacts and exact revisions, preserving contradictory evidence; it never erases or replaces child history.

The `research-portfolio-compound` master also illustrates **static reusable children** with pinned `content_digest`, explicit parameter bindings, dependency and `all_accepted` merge. The dynamic planner uses a fan-out proposal artifact; child IDs become known only after approved planning. A parent must not assume generated children exist because a `child_generator` node was completed.

## 4. Revisions and invalidation

A material change to an executed node, authority, claim or source contract requires a separately granted graph-revision approval. Create `graph-revisions/g0002.yaml`, record an old/new diff, append `graph_revision_requested` and `graph_revised` events, update the current pointer and checkpoint in `agent-files/` **after** validation. Old graph files, history, outputs and reviews remain immutable. Recompute descendant closure for changed nodes. Mark affected results SUPERSEDED or STALE for new revision; preserve unaffected accepted branches. A new buyer/problem/price claim invalidates downstream creative; a single square-logo correction should not erase approved research or portrait assets.

The optional helper's `revision-impact` command is **analysis only**, not a mutation or approval engine. The automated event-append and crash-atomic revision transaction remain Prompt 11 work.

## 5. What is actually implemented now

* File-native master/overlay/compound/dynamic-planner templates and this manual protocol.
* Optional PyYAML-based deterministic helper for validation, inheritance/parameters, readiness, child proposal generation, **approval-gated local instantiation**, reviewed synthesis and revision impact; conformance tests include negative cases.
* **Not implemented:** automatic workflow dispatch, live parallel task claiming, durable crash-atomic event store, remote claim fencing, external provider writes, autonomous background recurrence or automatic quality review. The helper does not authenticate owner identity; manual-mode approvals are cooperative local file records.

See `examples/conformance/planning/` (in the **development repository**, not a live account) for synthetic fixture data. The standalone downloaded folder has all master instructions; optional examples/tests can be copied into `agent-files/` when needed, not into protected master folders.
