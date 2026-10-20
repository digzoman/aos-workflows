# Installed draft JSON Schemas

This directory ships the eighteen JSON Schema Draft 2020-12 design files **inside the standalone distribution**. They match the repository's `docs/specs/schemas/` at scaffold packaging time. No network access is required to read them.

These documents cover common types; master/custom/compound templates; retry; instance and pinned template lock; run; state; event; checkpoint; claim; review; approval; handoff and attempt. Source references use relative `$ref` paths inside this directory.

**Important:** these files specify record shapes; they are **not a schema-validator installation**. The current 0.1.0 release includes no automatic graph executor, nor independent proofs of permissions, evidence truth, claims, event atomicity or a scheduler. A capable single agent can follow the instructions manually.

For full schema field details see `../SCHEMA-CONTRACTS.md`, `../GRAPH-AND-REVISIONS.md` and `../EXECUTION-STATE.md`.

## Prompt 11 additive fields

The draft `state`, `event`, `run`, `handoff` and `retry-policy` schemas now describe local owner/attempt/review references, hashed event predecessors, pausing/failing, operation uncertainty and active/revised graph identity. These are **structural contracts**; without optional host validation they are readable instructions only, not enforced permissions or proof of external provider success. Legacy 0.1/0.2 records remain valid by omission of newly optional fields.

## Governance record additions

The 0.4.0 distribution includes **18** draft JSON Schemas: the original 16 plus `remediation.schema.json` and `governance-handoff.schema.json`. Claim/review/approval/state/event/handoff fields support additional actor, graph, expiry/revocation and waiver metadata. Schema-valid records do not prove owner identity or real provider authority.
