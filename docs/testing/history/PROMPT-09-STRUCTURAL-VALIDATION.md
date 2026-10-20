# Prompt 09 staged structural validation — 2026-10-20

**Scope:** Public `digzoman/aos-workflows` Git tree for initial `scaffold/aos-w/` before commit. Checks were performed through read-only repository Git tree and blob inspection and lightweight graph-shape logic; they are **not** real agent task execution, a Node script test run, full YAML/JSON-Schema validation or distributed coordination test.

## Results — PASS (staged structural inspection)

1. Required protected files and writable initial folders exist in staged tree: README, PROTOCOL, VERSION, self-contained spec, references, master templates, agent-files config/custom/instances/indexes/cache/coordination.
2. **16** draft JSON Schema documents copied into scaffold from `docs/specs/schemas/` with **matching Git blob SHAs**. Prior Prompt 08 reference-check found no broken local references; this Prompt 09 copy inspection verified byte-for-byte identity. No separate installed runtime validator executed.
3. Master `research-starter` template, pinned `demo-local-research` snapshot and `g0001.yaml` **share the same Git blob SHA** `6dfc95e637498dd9cb14cfb592a261e81f06b4ce`. Template lock contains that exact Git-blob digest and version 0.1.0.
4. Two synthetic events in example `events.jsonl` have monotonically increasing sequence numbers 1 and 2; `state.json`, initial checkpoint and structured handoff all anchor sequence 2 and graph revision g0001. The run state is CREATED, next eligible task `define-scope`, **zero executed task attempts**, no granted external approvals.
5. Both master YAML files passed lightweight **static graph shape checks**: `research-starter` has `define-scope -> collect-evidence -> review-evidence`; `periodic-review-example` has `inspect -> summarize`. Every parsed dependency resolves to a node in the same graph, and no cycle was detected in these samples.
6. Sync configuration defaults to **disabled** and the manual one-writer mode requires no Git, Python, Node, MCP server, database or daemon.
7. Standardized docs distinguish file status from provider truth, and user-owned `agent-files/` is the only normal write target.
8. A read-only optional developer script `scripts/validate-scaffold.mjs` and optional ZIP packaging helper `scripts/package-scaffold.sh` were authored as support tools, not mandatory runtime dependencies.

## Checks NOT RUN / not proven

- Full YAML parser + JSON Schema validator invocation against all examples. The JSON Schemas and example records were checked structurally/read as JSON, but validator-library execution is still a follow-up.
- Execution of the actual Node optional validator or shell packaging script in a checked-out repository. This session's local container could not reach github.com to clone the staged files.
- Real agent cold-start completing `define-scope`, persisting new attempts, reviewing evidence and resuming another session.
- Atomic writes/crash durability across hosts, multi-agent claim races, schedule wake, idempotent external provider calls or any real Meta/GHL/website operation.
- Producing an actual prebuilt scaffold-only ZIP asset from this environment; the optional packaging script and GitHub whole-repository ZIP are documented distribution paths.

## Next phase

Prompt 10 should implement/test actual template reuse, inheritance, dependency/graph operations, conditional/dynamic execution and schedule metadata behavior. Prompt 11–13 tackle durable state automation, QC/permissions/skills, and empirical Git coordination, respectively. Keep the standalone manual/no-Git route intact.
