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
