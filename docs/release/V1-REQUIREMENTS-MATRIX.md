# AOS-W Version 1 requirements traceability and acceptance matrix

Review date: October 20, 2026. Classification is explicitly evidence-tiered.
Sources: docs/specs/requirements/USER-AGREED-BASELINE.md, docs/specs/requirements/PROMPT-01B-REFINEMENTS.md, docs/specs/prd/SURVEY-TRACEABILITY.md, PRD.md, ACCEPTANCE-TEST-MATRIX.md, proposed ADR-001 through ADR-014, architecture specs, implementation and hosted tests.
The original PRD still says DRAFT FOR OWNER REVIEW, not formally approved. Direct scoped implementation instructions are acknowledged, but do not rewrite the PRD approval record.

## Evidence tier vocabulary

CONFIRMED HOSTED means GitHub Actions actually executed a check, not that a separate long-lived cloud filesystem was proven.
CONFIRMED LOCAL means real test files, processes or local Git remote were exercised with controlled/synthetic data.
MANUAL DOCUMENTED means file-only behavior is specified for a capable agent, not enforced by a runtime.
PARTIAL means a subset works but original acceptance coverage is missing.
BLOCKED or NOT RUN means that evidence was not produced. A CI green status does not override a warning within its evidence log.

## Six mandatory original V1 demonstrations

**T01, real Ampgent research-to-advertising execution. PARTIAL, original success criterion NOT MET.**
Evidence: docs/testing/PROMPT-18-END-TO-END-RESULTS.md; GitHub Actions 39498378421; 27 passing local staged assertions, three separate child research runs and eight first-party vendor offering-page descriptions, one reviewed/changed PNG, CRM/landing plans, no external publication.
Gaps: actual Meta Ad Library ad card observations/source-ad tracking, evidence-based full approved audience rubric, independent AI model research and visual review, authentic seller delivery/price approval, actual verified provider staging/integration, running the full pinned compound template instead of a bounded purpose-built test graph. T01 cannot be called a complete real-world demonstration.

**T02, independent AI platform handoff. NOT MET.**
Evidence: Prompt 16 cold separate OS process from file state, Prompt 17 separate Git clones/processes and reviewer. These prove resumable state but not ChatGPT-to-Codex/Claude/Muse or another genuinely different AI executor. No separate persistent cross-provider handoff with artifacts and reviewer identity has been demonstrated.

**T03, exclusive two-agent collision control. PARTIAL, original full criterion NOT MET.**
Evidence: temp/tests/PROMPT-13-GIT-COORDINATION.md, docs/testing/PROMPT-17-GIT-COLLABORATION.md. Local bare Git CAS test used same Git email and actual parallel competing processes, stale epochs, manual takeover, conflict and network interruption. Hosted P17 Actions 39428039269 finished with workflow SUCCESS, but experiment explicitly reported GitHub CAS REVIEW_REQUIRED and live Git LFS BLOCKED. User/agent authentication and external provider fencing absent. ADR-014 must remain provisional.

**T04, independent QA failure, targeted correction, unaffected branches. PARTIAL, original independent-AI criterion NOT MET.**
Evidence: 0.7.0 grounded pilot 39498378421 deliberately failed missing research source and CTA-less PNG quality reviews. Each was corrected, rejected versions preserved, and exact-hash PASS recorded by a separate deterministic subprocess. Three child branches and parallel CRM/landing steps were exercised. Reviewer was not a separately executing AI model or independently inspected human visual reviewer. The generic core does not enforce a cross-instance all-reviewed join automatically, so pilot code used a separate guard.

**T05, revise active workflow without erasing history. LOCAL PASS subject to mocked authority.**
Evidence: Prompt 16 P16-09 graph revision g0001 to g0002 preserved prior graph and completed task artifacts, invalidated affected downstream work, rejected unauthorized/mock-unapproved application. Ownership approval was simulated, not authenticated. Meets a narrower local functional case, not a live multi-host concurrency revision scenario.

**T06, migrate active work to a different Git remote and resume. LOCAL PASS with limitations.**
Evidence: Prompt 17 P17-10 moved a partly executed pinned run to a different local bare Git remote, reopened run/event history, did not inherit old remote claims. This confirms real local Git portability; not a second hosted Git service or AI platform.

## Original 16 survey decisions, current implementation and remaining proof

Q01. All three goals equally weighted, real Ampgent pilot, portable standard, cross-agent work. PORTABLE LOCAL PROVED, pilot PARTIAL, cross-platform AI NOT RUN. Tests T01/T02/T07.

Q02. All five modules, research/keywords, repeatable research, QC correction, synthesis/scoring, creative/marketing staging. TEMPLATES PRESENT, synthetic or bounded tests; full source-ad evidence and live provider readback missing. Tests P15, P18.

Q03. Sequential/parallel, compound composition, dynamic child creation, conditional paths, all-reviewed merge. CONTRACTS AND OPTIONAL HELPERS PASS LOCAL. Independent child creation and guarded merge in P18, but automatic native parent-child enforcement incomplete. See tests/test_composition.py and P18 report.

Q04. Entirely PUBLIC repository using nonconfidential examples. REPO PUBLIC VERIFIED. Current tree and reachable-history secret signature scans passed at host baseline, but confidential-context, image rights and historical binary manual review remain open. Do not treat passing patterns as a complete data-protection certification.

Q05. One portable self-contained folder; agent-files only normally writable, including custom templates. PASS in standalone P16 protected-hash and 0.7.0 re-execution. AOS-W core is instructions and versioned files, not a mandatory executor.

Q06. Markdown instructions, YAML graph/template, JSON/JSONL state and handoffs. PASS in 126 hosted conformance tests and 13 practical standalone 0.7.0 acceptance tests.

Q07. Prototype Git LFS and task-ref CAS fairly before deciding. PARTIAL, local Git ref CAS race PASS; GitHub-hosted CAS REVIEW_REQUIRED, server LFS BLOCKED. See ADR-014 and Prompt 17.

Q08. Independent A Rep integration, not dependence. Design and provenance compatible; downloaded core standalone without A Rep. A Rep interoperability integration test with independently installed live host NOT RUN.

Q09. Four-field logical actor identity, owner/time/trailers/handoffs. LOCAL PASS, identity is cooperative metadata, not cryptographically authenticated; no exhaustive read-access audit required.

Q10. Step-level exclusive ownership and independent simultaneous agents where safely supported. LOCAL BARE GIT PASS, hosted shared coordination not certified. Plain manual single-writer mode is not exclusive.

Q11. Automated, independent AI, human and self QC configurable at workflow/step. LOCAL DETERMINISTIC AND DECLARED GATES PASS. Genuine independent AI review and authenticated human authority remain unproven. Tests P12, P16, P18.

Q12. Configurable bounded autonomy and consequence-specific permissions. Represented in template policy and optional governance checks. Strong actual provider-side authorization NOT IMPLEMENTED. No live publishing permission inferred.

Q13. Configurable dynamic revision preserving exact completed work and history. LOCAL PASS via test P16-09 with mocked approval; shared concurrent revision conflicts need more testing.

Q14. All six V1 success demonstrations are mandatory. NOT MET. Only T05/T06 have bounded local PASS, while T01/T02/T03/T04 are incomplete.

Q15. No mandatory Python, Git, server, MCP, DB, dashboard or daemon. PASS for installable file-only manual core. Optional tools use Python/Git/PyYAML for more ambitious guarantees.

Q16. Public digzoman/aos-workflows and downloadable scaffold/aos-w; Git optional. PASS. Verified versioned v0.7.0 preview with clean ZIP and manifest SHA-256.

## Additional Prompt 01b criteria

T07 local standalone without Git, protected-file boundary and custom instance. PASS on actual 0.7.0 archive after P16 harness generalization, 13 of 13 local practical scenarios.

T08 manual one-off launch and ad hoc launch from a recurring template. Declaration/manual behavior supported; dedicated end-to-end acceptance NOT RUN.

T09 scheduling occurrence duplicate wake, DST, missed and overlap policies. NOT RUN, host scheduler absent and policy defaults unresolved. Must not claim recurring runtime.

T10 just-in-time bundled/local/remote skill resolution. BUNDLED and local skill context tested; authenticated untrusted remote source handling NOT RUN.

T11/T12 ambiguous provider create/readback/rate limits. Synthetic intent/reconciliation guards PASS local, REAL PROVIDER READBACK NOT RUN.

T13/T14 source and visual reviews. Deterministic separate subprocess QA executed; independent AI and genuine image/official logo visual review NOT RUN.

T15 marketing campaign configuration, CRM and tracking staged/verified. Local text specification staged; real Meta and GHL configured-state verification NOT RUN.

## Core implementation coverage

Scaffold, schemas and template lifecycle: implemented.
Writable/protected boundaries: local PASS with hash checks.
Local no-Git run, checkpoint, error recovery: 0.7.0 actual ZIP PASS.
Persistent cloud volume surviving terminated host: NOT RUN, ephemeral Actions runner is not proof.
Optional Git mirror: local Git tested, hosted P17 uncertain.
Shared claim coordination: prototype only.
Graph conditional/parallel/dynamic children: contracts/helpers locally tested, host dispatch manual.
Cross-instance joins: external exact-hash validator needed, framework defect/improvement pending.
State event SHA chain, retries and corrupt-tail recovery: local PASS.
QA/provenance/handoff: locally tested, host authentication absent.
Remote skills/scheduling: not implemented end-to-end.
Live Meta, CRM, provider updates: not implemented/authorized.
Distribution/upgrade preservation: confirmed in hosted tests.
Version policy and licensing: open owner decisions.
Authenticated human release approval: pending.

## Reproducible evidence and verification

- GitHub Actions 39499859355, 126 PASS regression/conformance and 13 PASS practical standalone 0.7.0, plus repository historical/current automated screening and ZIP validation.
- GitHub Actions 39498378421, 27/27 bounded source-grounded marketing pilot checks.
- GitHub Actions 39428039269, hosted P17 Git coordination completed but CAS REVIEW_REQUIRED and LFS BLOCKED.
- docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md, historical v0.6.0 actual portable checks.
- docs/testing/PROMPT-17-GIT-COLLABORATION.md.
- docs/testing/PROMPT-18-END-TO-END-RESULTS.md.
- docs/specs/prd/ACCEPTANCE-TEST-MATRIX.md describes the originally required outcomes and must not be confused with execution.

The test status is conservative by design. Full Version 1 is not yet demonstrated under the originally selected success definition.
