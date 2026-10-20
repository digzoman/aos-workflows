# Installed draft JSON Schemas

This directory ships the sixteen JSON Schema Draft 2020-12 design files **inside the standalone distribution**. They match the repository's `docs/specs/schemas/` at scaffold packaging time. No network access is required to read them.

These documents cover common types; master/custom/compound templates; retry; instance and pinned template lock; run; state; event; checkpoint; claim; review; approval; handoff and attempt. Source references use relative `$ref` paths inside this directory.

**Important:** these files specify record shapes; they are **not a schema-validator installation**. The current 0.1.0 release includes no automatic graph executor, nor independent proofs of permissions, evidence truth, claims, event atomicity or a scheduler. A capable single agent can follow the instructions manually.

For full schema field details see `../SCHEMA-CONTRACTS.md`, `../GRAPH-AND-REVISIONS.md` and `../EXECUTION-STATE.md`.
