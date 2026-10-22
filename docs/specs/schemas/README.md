# AOS-W 1.0 Draft Record Schemas

**Design artifacts, not installed runtime code.** Each `*.schema.json` is a JSON Schema Draft 2020-12 document. YAML templates parse into the same object model. These are authoring contracts for Prompt 08, *not proof* that a future implementation or agent successfully enforces them. The original 16 documents (18 after Prompt 12) were syntax-parsed and their local `$ref` pointers reviewed as part of the design write-up; runtime schema validation and cross-file semantic checks belong to later tests.

| Schema file | Intended stored record |
| --- | --- |
| `common.schema.json` | Shared actor, artifact, permissions, step node, skill, trigger, predicate and quality gate definitions |
| `template.schema.json` | Published base YAML template and fully resolved graph revision |
| `custom-template.schema.json` | Custom overlay over explicitly version-pinned base, node patches and policy overrides |
| `compound-template.schema.json` | Composite template with child references, parameter bindings, authorization and join | 
| `retry-policy.schema.json` | Task-specific bounded retry policy |
| `instance.schema.json` | Instance config, effective policy, graph revision pointer |
| `template-lock.schema.json` | Immutable source version and local pinned template snapshot |
| `run.schema.json` | Manual/scheduled run identity, capabilities and mode |
| `state.schema.json` | Current **derived** state anchored to event prefix |
| `event.schema.json` | Single append-only JSONL event |
| `checkpoint.schema.json` | Durable resume anchor |
| `claim.schema.json` | Advisory or verified backend claim and fence evidence |
| `review.schema.json` | Gate, exact artifact set, verdict and reviewer |
| `approval.schema.json` | Scoped human/authorized external-action permission |
| `handoff.schema.json` | Optional handoff.json companion to handoff.md |
| `attempt.schema.json` | Per-attempt evidence, provider write ACK and readback |

## Contract and limitations

- All record roots use `schema_version: "1.0.0"`; this is a *draft design version*, not a released implementation. `aosw_version` belongs in the future installed `VERSION.json`.
- `$ref` is relative to the schema's location. A schema validator using a file-relative resolver MAY validate structure, but validation of graph cycles, cross-run IDs, user permissions, external truth, lease fencing, asset hashes and genuine independent reviews requires additional runtime/agent verification.
- Any `extensions` field is a namespaced escape hatch for future additive compatibility, **not** an authority expansion. Unknown hard permission fields cannot be ignored.
- Even correctly shaped JSON cannot prove actual remote synchronization, producer identity authentication, cryptographic hash or pixel-image QA.
- Some safe field defaults (recurrence DST, lease duration, claims winner, trusted remote skill resolution) remain open owner/empirical decisions. Presence of an enum is not policy approval of every option.
- No Git/Python/MCP or scheduler is needed to read the templates manually. Optional validators are future tooling, not core prerequisites.
- The future runtime must apply `GRAPH-AND-REVISIONS.md` and `EXECUTION-STATE.md` **in addition** to these structural schemas.

## Validation planned for Prompts 09–17

1. Parse all schema JSON and resolve all relative `$ref`.
2. Validate a bundled and customized YAML template after YAML-to-JSON conversion.
3. Negative tests for unknown critical fields, missing required IDs and malformed paths/ACL.
4. Validate events/checkpoints/handoff after simulated interrupted task and torn append.
5. Cross-file referential integrity, acyclic graph, protected-policy inheritance, reviewer independence and approval validity.
6. Template version pinning after published master changes.
7. Actual 2-agent claim race evidence and stale fencing where supported, never assumed from claim.schema.json.
8. Offline manual single-writer run with **no installed validator** remains usable and honestly advisory.

See [architecture specification](../architecture/README.md) and [PRD](../prd/PRD.md).

## Prompt 12 additions

`remediation.schema.json` and `governance-handoff.schema.json` document the two newly formalized record types. Claim, review, approval, event, state, handoff and common gate schemas gained compatible optional fields. Development and installed copies are byte-identical. This is shape validation guidance, not user authentication.

## Prompt 13 additions

`sync-config.schema.json` and `sync-state.schema.json` bring the installed/development schema set to **20**. They define optional Git modes, claim-backend choice and fail-closed shared offline policy. Actual remotely enforced guarantees require independent empirical validation.


## Version 0.8 visualization projection

The additive [visualization-snapshot.schema.json](visualization-snapshot.schema.json) describes an offline read-only snapshot, not a workflow engine state or event authority. It is shipped unmodified under scaffold/aos-w/spec/schemas and tested against the sanitized Bucket 9 demo.
