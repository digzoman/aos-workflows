# V1 record schemas and cross-file constraints

**Status: draft technical design.** Formal shapes are in `docs/specs/schemas/*.schema.json` (JSON Schema 2020-12). YAML files must parse to the same JSON data model. Machine-readable shapes validate **structure only**, not permission, concurrency, semantic QC or external provider state.

## Schemas in this design

| Logical record | File | Principal fields | Cross-file constraints |
|---|---|---|---|
| Common definitions | `common.schema.json` | IDs, UTC datetimes, actor identity, artifact refs, predicates, policies | Reused via relative `$ref`; no secrets |
| Template | `template.schema.json` | template_id, version, graph, defaults, skills, trigger | Node IDs unique; no cycles; dependencies exist; no authority escalation |
| Custom template overlay | `custom-template.schema.json` | Base ID/version/digest, stable node patches, skill/policy/trigger overrides | Resolve only with protected authority, freeze effective snapshot |
| Compound template | `compound-template.schema.json` | Version-pinned child references, bindings, join and authorization mode | Distinct child IDs, graph acyclic, merge only reviewed output |
| Instance | `instance.schema.json` | instance_id, pinned template origin+snapshot, current graph revision, parameters, permissions | Pin exact version/content hash; no live master HEAD influence |
| Run | `run.schema.json` | run_id, instance, graph, trigger/occurrence, capability observations | One occurrence ID per due boundary; immutable source |
| State | `state.schema.json` | event_seq, event_digest, task map, gate status, active revisions | Derived from validated events, not provider authority |
| Event | `event.schema.json` | id, sequence, timestamp, actor, event type, task/attempt, revision, evidence | Event sequence single-writer or adapter-serialized, chronological |
| Checkpoint | `checkpoint.schema.json` | event prefix, hash, state digest, completed/blocked tasks and next steps | Stored before declaring durable; immutable checkpoint record |
| Claim | `claim.schema.json` | task owner, token, lease, fencing, coordination mode | Only backend-confirmed atomic claim is exclusive |
| Review | `review.schema.json` | exact artifact set, rubric, verdict, reviewer, findings | Complete required set, version-bound, reviewer independence |
| Approval | `approval.schema.json` | issuer, scope, exact versions, action class, limits/exclusions, expiry | Policy-protected human approval cannot be removed by child |
| Handoff | `handoff.schema.json` | run, last checkpoint, current blockers and next eligible nodes | `handoff.md` mirrors structured record without becoming source truth |
| Retry policy | `retry-policy.schema.json` | classes, attempts, backoff, reconcile/compensation | External ambiguous effect always reconcile before repeat |
| Resolved graph snapshot | same template schema with effective policy | template version, resolved defaults, child templates | Immutable per revision; located under writable agent-files |

## Example, master template YAML (descriptive and shape-compatible)

```yaml
schema_version: "1.0.0"
template_id: competitor-research
version: "1.0.0"
name: Competitor research with independent QC
description: Research a scoped buyer segment with evidence-based findings
parameters:
  buyer: {type: string, required: true}
trigger: {kind: manual}
policy:
  autonomy: bounded
  allowed_actions: [read, research, write_local, review]
  human_required_actions: [stage_paused, activate_live, change_budget, deploy_prod, send_message, emit_conversion]
  default_gates: [evidence-review]
  max_parallel_tasks: 1
  allow_dynamic_children: false
skills:
  - skill_id: research-standards
    source: bundled
    path: skills/research-standards/SKILL.md
    required: true
graph:
  nodes:
    - id: plan
      kind: task
      needs: []
      instructions: Define source queries and coverage boundaries
      outputs: [{artifact_id: research-plan, path: artifacts/plan.md}]
    - id: research
      kind: task
      needs: [plan]
      instructions: Collect dated source results, do not infer absence
      outputs: [{artifact_id: evidence-log, path: artifacts/evidence.md}]
      retry: {schema_version: "1.0.0", max_attempts: 2, on: [source_unavailable, rate_limited], backoff: manual}
    - id: review
      kind: review
      needs: [research]
      instructions: Independent source/coverage review
      review_gate: evidence-review
      outputs: [{artifact_id: review-report, path: reviews/research-review.md}]
```

A `review` node itself produces a review record that must pass a configured gate; it cannot automatically grant external authorization. This is one *illustrative* example, not an already bundled template.

## Example, event JSONL (each line a complete object)

```json
{"schema_version":"1.0.0","event_id":"evt-0001","seq":1,"run_id":"run-001","type":"task_started","at":"2026-10-20T16:00:00Z","actor":{"agent":"Max","platform":"ChatGPT","role":"worker","instance":"session-a"},"task_id":"plan","graph_revision":"g0001","attempt_id":"attempt-1","evidence":[]}
{"schema_version":"1.0.0","event_id":"evt-0002","seq":2,"run_id":"run-001","type":"task_completed","at":"2026-10-20T16:10:00Z","actor":{"agent":"Max","platform":"ChatGPT","role":"worker","instance":"session-a"},"task_id":"plan","graph_revision":"g0001","attempt_id":"attempt-1","evidence":[{"artifact_id":"research-plan","locator":"artifacts/plan.md","revision":"v1"}]}
```

The agent must not append a completion event if the declared artifact is missing or unverified.

## Cross-record invariants that JSON Schema alone cannot enforce

1. **Referential:** node ID uniqueness; every `needs`, `branch_target` and `join` child resolves to an actual node; all parent-child IDs and output contracts match.
2. **DAG:** no cycles in the expanded graph; bounded retries are attempts of a node, not directed cycles. Repeatable research batches use distinct stable item IDs/child executions, not a cyclic dependency.
3. **Policy:** effective actions are never a superset of inherited owner-protected authority; every nonlocal consequential action has valid separate approval bound to exact object/version and not revoked.
4. **Eligibility:** predecessors, predicates, required gate results, artifacts, skills and permissions must pass before claim. `UNKNOWN` is not false or true.
5. **Integrity:** snapshot event_seq matches verified event prefix and digest; review and approval artifact hashes match current versions; events preserve monotonic revision lineage.
6. **Uniqueness:** manual run and scheduled occurrence identity distinct; no two active exclusive owners with a verified CAS backend; if none, expose advisory state.
7. **Safety:** missing remote skill, provider readback, branch-target or claim strength yields blocked/pending and never a fabricated success.
8. **Storage:** outputs stay under agent-files, unless an explicit authorized external provider/output destination exists. No path traversal or symlink escape.
9. **Privacy:** no tokens/credentials in schema instance data or events; references to connector secrets only.
10. **Handoff:** current human summary derived from actual validated snapshot/events, not a separate arbitrary authority.

The JSON Schema documents intentionally do not validate complex temporal/runtime constraints. A future optional validator may provide strict checks, but a capable manually operating agent should follow the same invariants via the read-and-verify runbook.

## Compatibility and extension rules

All documents use `schema_version` separately from the software/scaffold `aosw_version`. V1 accepts compatible 1.x with only documented additive fields; unknown 2.x blocks. New fields MAY live in `extensions`, namespaced by vendor/source, and MUST NOT weaken approval or access gates. Unknown fields **outside** extension surfaces are errors in critical/security objects. Templates frozen into instances retain prior schema and template versions until explicit migration event.
