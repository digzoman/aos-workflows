# AOS-W V1 requirements and evidence traceability

Date: 2026-10-20. Evidence baseline: main a7b7e8ac. This is a readiness snapshot, not an assertion of full coverage.

## Survey and architecture requirement groups

- Original 16-question survey, product scope and all five workflow module families: design traced by docs/specs/prd/SURVEY-TRACEABILITY.md, implementation exists in 0.7 marketing library. Full demonstrated end-to-end execution remains missing.
- Public digzoman/aos-workflows with standalone scaffold/aos-w: implemented, published preview.
- Self-contained scaffold with agent-files normally the only writable directory: implemented and tested in Prompt 16 locally.
- Markdown instructions, YAML templates, JSON/JSONL state: implemented, optional helper support.
- No mandatory Git, Python, database, MCP server, dashboard or scheduler: verified distribution and local standalone use, no-host cloud separately untested.
- Local cloud and Git operating modes independently of agent count: designed. Local and Git mock modes demonstrated. Separate durable cloud filesystem NOT RUN.
- Sequential, parallel, conditional, compound, dynamic fanout and merges: implemented in contracts/optional helpers, local test coverage. Full marketing life cycle orchestration is still manual/host-dependent.
- Template pins, custom overlay policies and historical revisions: specified and locally tested; mock-approved graph revisions only.
- Four-field agent provenance and handoffs: locally tested, not cryptographically authenticated.
- Git LFS and Git-CAS experiments: prototypes provided. Real local CAS one-winner test passed. Hosted CAS REVIEW_REQUIRED, live LFS BLOCKED. No production certification.
- Automated QA, independent AI, human and permitted self-review: declared and deterministic/local policies tested; genuinely independent AI and verified human authority remain open.
- Configurable autonomy and human external-action gates: represented by templates and helper checks. Host enforcement of external-provider permissions absent.
- Checkpoints, append-oriented history, retries, idempotency, interrupts and recovery: implemented in optional helper and real local tests, real provider effect reconciliation untested.
- One-off default and optionally scheduled repeating workflows: declared in templates. Unattended scheduler and recurrence identity/dedup execution absent.
- Bundled, custom and remote skill references: bundled and file-local skill context checks demonstrated; trusted remote resolution not established.
- A Rep compatibility: design convention matched, not yet a verified interoperability acceptance case.
- Downloadable install and safe user-data-preserving upgrades: 0.7.0 preview CI passed. Full existing-data migration and major version upgrade tests remain open.

## Six acceptance demonstrations

T01: NOT RUN as requested; see PROMPT-18-PILOT-PLAN.md.
T02: PARTIAL process/clone handoff only; real second AI platform not run.
T03: PARTIAL local Git CAS pass; hosted GitHub result REVIEW_REQUIRED; Git LFS blocked.
T04: PARTIAL deterministic QC and correction; independent AI creative gate missing.
T05: LOCAL PASS with mock authority; historical preservation proven within local fixture.
T06: LOCAL PASS to second bare Git remote; hosted provider transfer not run.

Evidence entrypoints:
- docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md
- docs/testing/PROMPT-17-GIT-COLLABORATION.md
- temp/tests/PROMPT-15-MARKETING-CONFORMANCE.md
- GitHub Actions run 39434478250, 126 conformance tests PASS and 0.7.0 package
- GitHub Actions run 39428039269, P17 workflow success but hosted CAS REVIEW_REQUIRED, LFS BLOCKED

Classification is intentionally conservative. Contract compliance, local simulation, test harness runs and real independent agent execution are different evidence tiers.


## Same-day post-audit pilot evidence

T01 has a new PARTIAL SYNTHETIC execution record, run 39495294275 with 77 persisted events and explicit NOT_GRANTED publication gate. It does not demonstrate the original real-world T01 criterion. T04 likewise has additional deterministic mock research and SVG artifact review failure/recovery evidence, but independent AI reviewer verification is still not executed. See docs/testing/PROMPT-18-SYNTHETIC-PILOT-REPORT.md. All other classifications remain unchanged.
