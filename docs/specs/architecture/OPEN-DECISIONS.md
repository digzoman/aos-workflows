# Prompt 08 proposed choices and unresolved engineering gates

Prompt 08 is documentation-only and takes the 16 survey answers and Prompt 01b as fixed. The PRD's approval record was still **PENDING** at inspection; the user's explicit Prompt 08 instruction authorizes this design drafting but is not separately recorded as unqualified PRD approval. Do not silently change `docs/specs/prd/PRD.md` or earlier ADR status to ACCEPTED.

## Technical decisions specified here as proposals

| Topic | Prompt 08 choice | Status |
| --- | --- | --- |
| Directory hierarchy | `agent-files/instances/<id>/runs/<id>`, custom templates/config inside same zone | Proposed, schema-level concrete |
| Template freeze | Resolve then pin copy and content revision, never chase upstream HEAD for existing run | Follows approved requirement |
| History | Events audit authority, state.json materialized current view, checkpoints anchors; stale indexes derived | Proposed clarification of PRD D-05 |
| Graph | DAG with typed node kinds, dependency lists, 3-valued conditions; bounded retry not graph cycle | Proposed technical definition |
| Gate model | exact artifact-set QC distinct from separate action authorization | Follows agreed requirement |
| Claims | logical file advisory by default; only tested adapter can enforce exclusive ownership and fencing | Follows agreed baseline; backend winner open |
| Inheritance | keyed merge, protected permission intersection and no silent human-gate weakening | Proposed D-02 policy |
| Skill resolution | exact pinned ref, no silent shadowing, missing remote blocks or approved fallback | Proposed D-08 policy |
| Recurrence | manual default, explicit host wake, stable schedule occurrence IDs; syntax adapter may support cron/RRULE | Requirement fixed, expression choice open |

These choices are described enough for implementers to create a compatible first implementation, but choices that affect permissions, trust, scheduling, or coordination remain subject to explicit owner review and empirical validation.

## Unresolved details that MUST NOT be invented as passed/approved

1. **PRD owner approval record** remains pending in repository; user is directing this spec phase, but owner signoff for engine build still has to be recorded before Prompt 09.
2. **Git LFS vs atomic Git CAS** must be compared in real races with shared GitHub login, stale leases, crashes and offline network cases (Prompts 13/17). REST GitHub PATCH does not itself establish expected-old-SHA CAS.
3. **Durability and claims** on arbitrary cloud agents: persistent volume and proven atomic write/compare semantics are host-specific; no guarantees from a path name.
4. **Recurrence expression syntax** RRULE vs cron, DST missing/repeated times, overlap and missed policy defaults require explicit decision; no automatic waking without host.
5. **Skill name conflict, remote trust**, and execution of bundled scripts may require additional host permissions; a referenced repository is not authority.
6. **Actual schema validation** of the draft JSON Schemas across a YAML/JSON parser/validator remains future test work; structural contracts are authored, not runtime tested.
7. **Schema field naming/compatibility migration** needs acceptance against real cross-model handoffs and exact pinned local copy before freezing `1.0.0` for release.
8. **Agent identity authentication** is not supplied by the four-field producer header or shared GitHub login.
9. **Owner policy/waiver defaults**, lease reclamation and emergency pause authority must not be broadened by this documentation.
10. **Git public data hygiene and license** remain pre-release decisions; examples stay sanitized.

## Next steps

Prompt 09 may implement the downloadable protected scaffold only after explicit owner PRD/spec approval (or a clear direction that authorizes that implementation). Prompt 10–12 implement graph/state/QC/skill behavior under approved schema. Prompt 13 experiments compare real coordination backends rather than treating this paper design as proof. Prompt 16–18 run actual tests. Every stage records what is LIVE, MOCKED, MANUAL or NOT_RUN and does not mark hypothetical acceptance tests PASS.
