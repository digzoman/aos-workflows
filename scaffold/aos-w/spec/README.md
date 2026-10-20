# Self-contained protocol and record specifications

Every file here is **read-mostly framework reference**, copied into the downloadable directory so an agent does not have to consult the development repo or an online chat.

- `SCHEMA-CONTRACTS.md`, record meanings, cross-record restrictions and a YAML example.
- `FILE-SPECIFICATION.md`, every important installed-path responsibility and version pinning.
- `GRAPH-AND-REVISIONS.md`, sequential/parallel/conditional/dynamic/merge semantics and eligibility.
- `EXECUTION-STATE.md`, statuses, reviews, retries, event history and safe recovery.
- `MANUAL-AGENT-PROTOCOL.md`, detailed no-helper-script procedure.
- `schemas/*.schema.json`, draft JSON Schema 2020-12 structural contracts for templates, custom templates, compound graphs, instance/run/state/event/claim/review/approval/checkpoint etc.

Version `1.0.0` is the **schema-design contract version**, not a claim of a finished engine. A reader should refuse unknown major versions and treat unverified capabilities/unknown side effects as blocked. JSON Schema alone does not enforce side effects, true reviewer independence, cross-file DAG integrity or distributed mutexes.
