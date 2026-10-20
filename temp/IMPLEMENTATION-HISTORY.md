# Chronological Project History

## 2026-10-20. Prompt 01, initialization

- Confirmed requested repository name `digzoman/aos-workflows` and explicitly public visibility.
- Created GitHub repository and initial documentation.
- Set up tracked `temp/` workspace for plans, requirements, research, open questions, progress, and durable cross-session handoff.
- Defined the portable scaffold path and initially reserved `agent-files` as the only runtime-modifiable subtree.
- No engine, lock, Git synchronization, or operational workflow functionality implemented.
- Next task is research indexing, Prompt 02.

## 2026-10-20. Prompt 01b, requirements amendment

- User added non-repeating versus recurring workflows. Default is one-off; reusable templates can declare an overridable schedule and can still launch ad hoc.
- User added skills stored inside templates and workflow instances and referenced at the relevant step. Skills may also point to installed or repository-hosted skill packages.
- Recorded compatibility with no mandatory scheduler, Git, or agent daemon. Trigger execution infrastructure and detailed schema remain unresolved.
- Updated design baseline, scaffold documentation, work plan, open questions, progress, and handoff.
- No scheduling service, workflow engine, or skill resolver implemented. Next step still Prompt 02.

Future sessions should append substantive events with changed files, test evidence, commit references, and failures. Avoid copying raw private logs.

## 2026-10-20. Prompt 02, workflow history and source index

- Read the required tracked project context and confirmed the previous Prompt 01b commit as starting state.
- Inspected the restricted Max marketing repository and twenty targeted source documents spanning research planning, multiple-run execution, QC, creative production, peer review, staging, launch and web-development handoff.
- Directly viewed a Bucket 9 ChatGPT research conversation and consulted provided Ampgent project-context excerpts. Classified each title/source by observed access rather than inferring full transcript access.
- Created sanitized `temp/research/SOURCE-INDEX.md`, `WORKFLOW-PATTERNS.md` and `EVIDENCE-GAPS.md`.
- Recorded recoverability, cross-repo missing-artifact errors, partial QA, ambiguous external API retries and launch readback limits as observed failure/correction cases.
- Did not build an engine, modify external marketing infrastructure, or copy restricted source data into this public repo.
- Next task remains Prompt 03, detailed research workflow reverse engineering.

## 2026-10-20. Prompt 03, reverse engineering research workflow

- Read required AOS-W project state and the Prompt 02 sanitized research index.
- Directly inspected original Max research refresh queues, result logs, candidate ledger, scoring rubric, final report and source-match failures, plus October vertical methodology, trades discovery, independent 15-run portfolio and representative individual runs.
- Added restricted-source path addendum R21–R50, research workflow model, scoring/evidence/QC analysis, vertical and subvertical lineage, and 14 non-executable reusable template contracts with four composition sketches.
- Found distinct ad-persistence versus market-opportunity scoring and documented incomplete/blocked access without interpreting as verified absence.
- Recorded a source-of-truth discrepancy, Run 10 local progress started while portfolio index still said not started, without modifying the private source.
- No AOS-W workflow engine, schemas, live marketing actions or external system modifications.
- Next stage is Prompt 04 creative workflow research.

## 2026-10-20. Prompt 04, creative production history and candidate contracts

- Directly read restricted Max source documents for B1–B5 V3, B6/B7 Fred/Muse bakeoff and ChatGPT creative runs, B6.3 Ontario special cases, B8 VA variants, B9 offer/asset revisions, brand guidance and the existing logo-placement skill.
- Indexed 31 directly inspected source documents R51–R81 with evidence limitations.
- Built a staged production model, QA/approval matrix, version and skill design notes, corrective casebook, 14 proposed creative template contracts and four draft compositions.
- Preserved important chronology such as B9 logo-free owner selection and later branded approved variants. Differentiated documented historical QA from a new direct image inspection, which was not performed here.
- No executable engine, live creative generation, provider account modification or remote publish action.
- Next Prompt 05, reverse engineer Meta configuration, launch, CRM and monitoring.

## 2026-10-20. Prompt 05, historical Meta operations and tracking research

- Read source Max Meta staging, launch, age/geo targeting and message field docs, B8/B9 QA, website source/DEV handoff and HighLevel bot audit.
- Reviewed Fred issues 96,108,124,129,130,135,147 and relevant comments; read independent Oct 14 browser/server tracking analysis.
- Created 26-source indexed reference set R82–R107 and sanitized operational workflow, source-of-truth/failure, CRM/consent lessons, operations template catalog and PRD recommendations.
- Explicitly separated source-recorded historical provider actions from current live provider verification, which was not performed.
- No Meta, CRM, GHL, website or external account edits, and no engine implementation.
- Next Prompt 06 architecture/reliability research.

## 2026-10-20. Prompt 06, architecture framework research

- Read AOS-W persistent operating context and confirmed prior Prompt 05 commit.
- Reviewed public A Rep framework, current primary skill and references, provenance, plans, ledgers, skills and recovery; reviewed private Fred and Max README and existing bounded Fred plan/events (without copying private content).
- Examined official LangGraph graph/checkpoint/interrupt/retry/subgraph and Agent Skills progressive disclosure docs; official Git worktree/LFS/ref-push behavior.
- Recorded a public A Rep version discrepancy and actual separate Fred-host / Max-manual execution models.
- Wrote sanitized `temp/architecture/` source index, A Rep compatibility, LangGraph mapping, minimal environment/core, Git claims/LFS/worktree tradeoffs, skills/scheduling/security, alternatives comparison and PRD inputs.
- Wrote eight **PROPOSED** ADRs, without representing them as owner-approved decisions. Git LFS versus atomic claims is deliberately **unresolved pending empirical trials**.
- No workflow runtime/code, provider action, lock test or scheduling service created.
- Next Prompt 07 enhanced PRD with human approval before implementation.

## 2026-10-20. Prompt 07, enhanced V1 PRD review package

- Re-read saved AOS-W user decisions, refinements and architectural comparisons, plus historical competitor research, creative QA and Meta/CRM setup/launch source-indexed models.
- Created a comprehensive 24-section DRAFT PRD and detailed requirements covering portable scaffold, agent-files-only normal writes, inheritance, graph semantics, checkpoint/replay, quality and human permission, task claims/Git, recurrence, skills, optional provider integrations and security.
- Explicitly mapped all 16 original survey answers, documented the six mandatory V1 success tests, and added research-derived negative/failure scenarios.
- Added ACCEPTANCE-TEST-MATRIX, DECISION-REGISTER and APPROVAL-REVIEW documents. Left LFS versus atomic claims and all eight ADRs unapproved.
- Retained fixed owner requirements rather than inventing exact schema, scheduler default or cloud guarantee; unresolved decisions remain clearly labeled.
- No implementation code or live account modifications. Next owner approval checkpoint, then Prompt 08 only after explicit approval.

## 2026-10-20. Prompt 08, technical architecture and file specifications

- Inspected PRD 1.0-rc1 and latest review decision register, approved baseline survey and Prompt 01b context; no independent approval/change record evidenced after Prompt 07. Treated user Prompt 08 as authorization to produce design documents only.
- Documented full future scaffold protected/mutable layout and compatible file responsibilities under `docs/specs/architecture`.
- Authored technical contracts for schema fields, graph eligibility/conditions, template pinning, conditional fan-out/joins, impact-limited graph revision, state/event audit, claims, reviews/permissions, checkpoints and manual zero-script operations.
- Authored 16 JSON Schema 2020-12 design files under docs/specs/schemas and proposed ADR-009 through ADR-013 under docs/specs/adrs.
- Corrected sample nested retry schema version and added optional structured handoff companion.
- No code engine, scripts, external provider operations, atomic Git lock tests, schedule daemon or permission changes.
- Next owner approval/checkpoint, then Prompt 09 scaffold implementation if expressly authorized.

## 2026-10-20. Prompt 09, portable standalone scaffold

- User explicitly directed implementation of Prompt 09 "using the approved PRD and technical specifications." Treated that instruction as owner authorization for the **initial file-based scaffold only**, not blanket acceptance of all ADRs or permission for live external systems. Formal PRD review form still lacked a separate submitted answer.
- Confirmed main HEAD at prior Prompt 08 commit. Inspected original scaffold placeholders, technical file map/manual protocol and current development rules before changes.
- Implemented actual `scaffold/aos-w/` README, PROTOCOL and version manifest, self-contained `spec/` with five technical reference documents and sixteen versioned draft JSON Schemas, and read-only reference guides.
- Implemented two master YAML templates: manually invoked `research-starter` with step-local bundled evidence-handling Agent Skill and safe self-review; `periodic-review-example` showing disabled weekly metadata without any scheduler.
- Implemented `agent-files/config/`, `custom-templates/`, `instances/`, `cache/`, `indexes/`, `coordination/` and an inert synthetic practice instance with physically present run-state, event-history, checkpoint, task-attempt, evidence, review, approval, claim, skill and handoff directories. The practice run explicitly has **zero executed tasks and no provider permissions**.
- Added optional `scripts/validate-scaffold.mjs` and `scripts/package-scaffold.sh` (not prerequisites for standalone users), plus sanitized example index and upgrade instructions.
- Performed staged Git tree validation: required paths present, 16 schema Git blobs match source, example template/snapshot/graph Git blob match and lock digest, two event sequence and state/checkpoint/handoff consistent, template graphs have no missing parsed dependencies or cycles. Detailed PASS/NOT-RUN evidence in `temp/tests/PROMPT-09-STRUCTURAL-VALIDATION.md`.
- Did **not** run a full YAML/JSON-Schema validator, actual optional scripts, cross-agent cold-start or create a prebuilt ZIP in this tool environment, and did not implement graph executor, Git locking, schedule host, provider writes or live marketing actions.
- Next Prompt 10, implement reusable template resolution, compound graph behavior and eligibility without violating no-runtime standalone mode.

## 2026-10-20. Prompt 10, reusable workflow templates and composition

- Read persistent project state, architecture/schema decisions and existing Prompt 09 scaffold; verified GitHub main at prior commit before building.
- Extended read-only master library with `competitor-investigation`, `research-portfolio-planner`, and `research-portfolio-compound` (version 0.2.0), plus user-owned SHA-pinned custom Ontario overlay. Upgraded original master YAMLs to explicit step input/output/QC/dependency/contract fields, while preserving original practice run pinned to 0.1.0 bytes and adjusting optional legacy validation expectations.
- Documented file-only manual composition under `scaffold/aos-w/references/COMPOSITION.md`, revised template indexes, master/overlay READMEs and installed operating protocol.
- Added OPTIONAL PyYAML-based local helper and CLI in `tools/composition/` for schema-like graph shape validation, safe overlays, parameter resolution, readiness, stable dynamic child proposals, approved local materialization, strict reviewed synthesis and graph revision impact. Never made Python a mandatory runtime for downloaded file-only users.
- Added sanitized conformance JSON/YAML fixtures for coaches, agency owners and roofing research; mock approvals and PASS reviews exist **only as test fixtures** and do not prove actual work or owner authorization.
- Expanded `common.schema.json` (source and installed copy) for explicit node contracts and `state.schema.json` with FAILED for failure classification. Kept old schema fields optional to preserve 0.1.0 pinned run compatibility.
- Ran 11 local unittest methods and CLI smoke commands PASS; verified source Git blob SHA identity before commit. Log at `temp/tests/PROMPT-10-COMPOSITION-CONFORMANCE.md`.
- No provider/network actions, automatic workflow scheduling, live QA generation, concurrent task locking, event-backed revision application or crash-safe state engine implemented.
- Next Prompt 11 durable state, checkpoints, retry/recovery and controlled graph revision application.

## 2026-10-20. Prompt 11, durable state, retries and recovery

- Read persistent operating rules, Prompt 10 handoff, pinned graph/state/event/checkpoint contracts and current GitHub main before development.
- Implemented **optional** Python-local `tools/state/state.py` and `cli.py` with SHA-256-chained append-oriented JSONL, derived state with graph/version/actor/dependency/attempt/evidence/owner/pending operations, fsync and local snapshot replacement when supported, bounded retry and delay, explicit pause/resume/cancel/fail, and event-prefix checkpoints/handoffs.
- Protected external-effect replay using deterministic operation keys and intent-before-submit, ambiguous ACK readback requirements, explicit new-key retry only after verified NOT_APPLIED result; no provider APIs called and approval metadata remains cooperative, not cryptographically authenticated.
- Implemented authorized graph revision **application** to immutable graph file and graph_revised history with downstream invalidation, preserved completed evidence and stale-pointer recovery after crash. Existing older graphs remain pinned.
- Added torn-tail and stale-snapshot recovery, digest tampering rejection, current completed-artifact hash checks, checkpoint mismatch/orphan detection, partial child directory audit without duplication, and advisory compatibility with legacy unhashed run logs.
- Updated draft `state`, `event`, `run`, `handoff` and `retry-policy` schema definitions in **both** development and installable copies; added manual instructions `references/STATE-AND-RECOVERY.md` and synthetic recovery fixture descriptions.
- Ran **26 new local tests PASS**, plus **11 Prompt 10 regression tests PASS**, 37/37 overall, with one initial test-fixture copy setup correction documented. Only local synthetic tools, no live external accounts. Report: `temp/tests/PROMPT-11-STATE-CONFORMANCE.md`.
- No automatic execution scheduler, hard shared coordination, authenticated external-action authority or provider write/readback. Next Prompt 12 provenance/permissions/QC/skills.

## 2026-10-20. Prompt 13 — optional Git synchronization and task claims

- Built on the published Prompt 12 foundation and verified prior local regression tests.
- Implemented Git-optional remote check/fetch, clean fast-forward, no silent auto-merge/reset/force-push, explicit agent-files-only commit and remote readback with four-part Agent-Provenance commit trailer.
- Prototyped CAS task refs with explicit old SHA lease, logical actor separate from Git user, UUID token and monotonic epoch, explicit expired-claim reclaim, release and fail-closed offline behavior.
- Git LFS lock/verify/unlock wrapper is present, but git-lfs binary and supporting server were unavailable; no real Git LFS experiment conducted.
- Real local bare Git remote tested with separate clones using same Git user identity. 15 new tests passed, 90 regression tests total; six concurrent races each yielded one winner.
- Added three-mode configuration, observed sync-state, two Draft 2020-12 JSON schemas (20 total), portable manual rules, ADR-014, sanitized fixtures and test evidence.
- Provisional preferred coordinator is Git ref CAS, subject to hosted GitHub branch/ref, race and network testing; no real GitHub Git transport (DNS unresolved) or provider side effects.
- Next Prompt 14: packaging and upgrade preservation, schema validation and optional-host readiness testing.

## 2026-10-20. Prompt 14 — optional helpers, standalone distribution and safe upgrades

- Re-read durable Prompt 13 Git/agent-files implementation, preserved 0.5.0 manual portability and current GitHub main.
- Replaced the old unrestricted `zip -r` packaging behavior with optional, stdlib-only `scripts/aosw-distribution.py`: strict source allowlist, nonsecret clean agent-files seed, deterministic ZIP, SHA-256 manifest, zip-slip/duplicate/symlink and size checks, staged install and rollback-preserving upgrade. Updated shell wrapper to call safe builder; no silent raw user-folder ZIP.
- Added optional `scripts/aosw-ops.py` for template/instance discovery, advisory status, one-off safe run creation from a pinned master YAML with optional PyYAML, four-field provenance, initial SHA256-chained event and clean handoff. The tool never executes tasks/Meta/CRM actions and cannot authenticate owners.
- Added independent `.github/workflows/aosw-portable.yml` to execute regression suite, produce/verify `aos-w-portable-0.6.0.zip`, install into arbitrary working folder, create an initialized workflow and upgrade preserving its user artifact, upload Actions artifact and attempt optional preview release asset. Hosted execution and asset status must be independently verified after commit.
- Shipped `scaffold/aos-w/references/INSTALL.md` plus development quickstart and updated README/version/docs. The clean ZIP omits the repository's synthetic demo run and custom overlay, but retains empty config/instance directories and protected docs/schema/master/skill definitions.
- **18** new local tests and **90** existing regression tests PASS (**108/108**). Also created an instance from the actual previous `research-starter` YAML and replayed with Prompt 11 `RunStore.verified()` without any prior chat context.
- No automatic scheduler, always-on engine, external provider actions or production distributed claim/authorization system; retain Git ref CAS as provisional for hosted verification. Prompt 15 marketing templates next.

## 2026-10-20. Prompt 16 — practical standalone/offline acceptance

- Detected Prompt 15 marketing templates were not committed to `main`; selected the proven public 0.6.0 release ZIP with exact known SHA-256 to avoid silently testing a nonexistent 0.7 release.
- Extracted a genuinely fresh local `aos-w/` working folder without Git and used optional developer helpers from **outside the installed folder**. Executed fictional offline research, generated scope/evidence/summary artifacts, checked hashes and submitted a self-review gate. Deliberately interrupted a running task and had a **new OS process** recover and complete it from saved handoff, pinned graph, just-in-time skill and event history, without prior conversation state.
- Exercised real local custom template, output, transient failure/bounded retry, QC revise/resubmit, exact revision invalidation and nondestructive history, pause/resume/cancel, corrupt JSONL repair with quarantined tail, mock provider operation dedup/reconciliation guard and normal writes confined to `agent-files`.
- Initial harness assertions expected a skill-dependent node to be unconditionally READY, contrary to defined behavior. Corrected assertions to verify context gate and reran: 13 PASS, 0 FAIL, 1 NOT RUN (separate persistent cloud filesystem), with every expected/observed result in `docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md` and synthetic evidence under `tests/acceptance/evidence/`.
- Added reproducible scripts to `tests/acceptance/` and a GitHub Actions offline acceptance step; hosted result must be checked separately. No framework code was changed for test harness corrections. These local tests do not establish separate AI harness, authenticated approval, scriptless manual execution or persistent cloud-host operation.

- Post-commit independent GitHub Actions run `39423403366` SUCCESS. Its logs show 108 previously existing tests PASS and practical tests P16-01 through P16-13 PASS; ZIP digest equals v0.6.0. Uploaded separate acceptance evidence artifact ID `12264942466`. This is a separate hosted *ephemeral* CI runner, **not** the unperformed durable cloud filesystem acceptance case.
