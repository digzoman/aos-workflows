# Initial Candidate Reusable Workflow Templates

**Design candidates, not runnable templates.** Prompt 03, 2026-10-20. Each uses the historical evidence IDs described in [../SOURCE-ADDENDUM-03.md](../SOURCE-ADDENDUM-03.md). Proposed interfaces and gates are hypotheses for Prompt 07 PRD and Prompt 08 technical architecture, not approved schemas. Default trigger is **ad hoc/non-repeating**, with optional future schedule declaration and manual override.

| ID | Candidate template | Historical support | Suggested gate |
| --- | --- | --- | --- |
| T01 | Environment & authority preflight | R03, R41, R50 | G0/G1 |
| T02 | Research portfolio/segment planner | R32–R41 | G0/G5 |
| T03 | Keyword & advertiser discovery planner | R21, R23, R31–R33 | G2 |
| T04 | Advertiser verification worker | R03, R21–R22 | G2/G3 |
| T05 | Keyword sweep worker | R03, R23–R24 | G2/G3 |
| T06 | Evidence normalization & seller dedupe | R25–R27, R36 | G4 |
| T07 | Source/coverage finalizer | R03–R04, R34 | G5 |
| T08 | Source-ad persistence scoring | R25–R28 | G6 |
| T09 | Vertical opportunity research | R36, R43–R47 | G3/G6 |
| T10 | Independent research QC/rework | R06–R09, R29–R30 | G7 |
| T11 | Cross-run synthesis and decision | R27, R34–R39, R42 | G8 |
| T12 | Targeted retry/revalidation | R24, R34, R48 | G2/G5 |
| T13 | Dynamic subvertical proposal generator | R37–R40 | G0/G8 |
| T14 | Cross-agent checkpoint/handoff | R03, R41–R50 | G9 |

## T01, Environment & authority preflight

Input: user task, allowed sources and writes, hosting capability list, repo or local workspace, prerequisite skills. Output: verified tool access, read-source snapshot, allowed mutation list, blockers, next-task handoff. Acceptance: actual read/write tests where authorized, no invented VM view or API availability. Retry: bounded source-specific check, fail closed if essential access unavailable. Dependency: none. Historical support R41 and R50.

## T02, Research portfolio/segment planner

Input: parent objective, canonical offering, previous evidence, segment universe, owner priorities. Output: candidate audiences, buyer definitions, ranked rationale, per-run proposal IDs, independent scope and coverage expectations. Acceptance: planned is explicitly different from started; no child starts without configured authorization. Dependency: T01. Gate: owner approval if required. Historic R33–R41.

## T03, Keyword and advertiser discovery planner

Input: defined segment and historical research, keyword bank, source/market filters and budget. Output: finite ordered queues with stable IDs, broad vs specific category, threshold and priority. Acceptance: no duplicated items, representative synonyms, adequate geography and search families, deferred expansion list. Dependency: T02/T01. Historic R21/R23/R31/R32.

## T04, Advertiser verification worker

Input: one claimed advertiser queue item, history, evidence contract. Output: observed advertiser+offer-family record, variant evidence, source class, status, provisional score if appropriate, new search-term suggestions. Acceptance: live source/date/format or honest failure, no unsupported current status or invented older variant. Dependency: T03 and access gate. Retry: legitimate first-party alternate then BLOCKED/NOT_FOUND. Historical R03/R21/R22.

## T05, Keyword sweep worker

Input: claimed query row, date threshold, market and existing ledger. Output: query-level observation and deduplicated candidate changes, observed sample/rank context, retries. Acceptance: inspect beyond first relevant card, distinguish EMPTY_VERIFIED from RETRY_REQUIRED; no fabricated Meta rank or targeting. Dependency: T03. Historical R03/R23/R24.

## T06, Evidence normalization and independent-seller dedupe

Input: T04/T05 observations plus existing sources and version. Output: stable ad IDs, offer-family entities, seller identities, source links and contradictions. Acceptance: one seller does not become multiple competitors through variants; prior/source lineage retained; ambiguous duplicates flagged. Dependency: one or more evidence workers. Historical R25–R27/R36/R47.

## T07, Source and coverage finalizer

Input: current queues, result records, candidate ledger, targets and outstanding blockers. Output: coverage verdict, target-specific minimal retries, accepted documented exceptions. Acceptance: each planned row accounted for, no material missing item silently passed, historic observations never considered fresh without re-verification. Dependency: T04–T06. Historical R03/R04/R34.

## T08, Source-ad persistence and shortlist scorer

Input: normalized ad family, age/rank/variant evidence, named `source-ad-persistence` rubric and categories. Output: FULL or PROVISIONAL score, transparent components, candidate decision, diverse shortlists. Acceptance: correct 50/30/20 or documented 60/40 missing-rank model; no profitability inference. Dependency: T06/T07 as configured. Historical R25–R28.

## T09, Vertical buyer/opportunity research

Input: authorized vertical ID, buyer roles, baseline evidence, source/offer classes, constraints, seven-axis rubric. Output: dated evidence log, independent seller counts, seven-axis scorecard, separate confidence, research report, process checkpoints. Acceptance: owner buying paid-Meta marketing is not consumer seeing niche ads; observe US/CA separately; distinguish AI tool/DIY/DWY/DFY and features absent from toolkit; score reasons justified. Dependency: T01/T02 plus explicit run authority. Historical R36/R41–R47.

## T10, Independent research QC and remediation

Input: immutable submitted run/evidence version, approved rubric, source pointers and reviewer identity. Output: PASS/REVISE/BLOCKED/INSUFFICIENT_EVIDENCE, detailed issues and rework target. Acceptance: reviewer independent when specified, exact artifact set known, no automatic approval on changed files. Dependency: T07/T08/T09; can conditionally re-enter only failed workers. Historical R06–R09/R29–R30.

## T11, Cross-run synthesis and opportunity decision

Input: reviewed research runs, stakeholder priorities, historical baselines and current limitations. Output: versioned ranked decision and source matrix, LAUNCH CANDIDATE/RESEARCH MORE/DEFER, explicit follow-on proposal. Acceptance: observed facts separate from interpretation; no ad-creation or publication authority inferred. Dependency: T10 pass or explicit documented exception for every required child. Historical R27/R34–R39/R42.

## T12, Targeted retry and revalidation

Input: source-access error or stale/high-value evidence, attempt history, allowed browsers, maximum budget. Output: new verified observation or honest failure, current state update and preserved previous evidence. Acceptance: bounded attempts, no access bypass, no duplicate candidates or side effects, reliable empty versus unavailable classification. Dependency: triggered by failed T04/T05/T07/T09. Historical R24/R34/R48.

## T13, Dynamic subvertical proposal generator

Input: reviewed umbrella research, gaps, owner priorities, available candidate roles and subtrade evidence. Output: zero or more distinct child proposals with IDs, rationale, dependencies, evidence quality, approval state and priority. Acceptance: placeholders are not automatically selected winners; no surprise new live research or external actions. Dependency: T11, then configured authorization. Historical R37–R40.

## T14, Cross-agent checkpoint/handoff

Input: current run state, last submitted artifacts, exact paths/versions, reviewer/owner, next eligible action, unresolved blockers. Output: durable resumption packet and optional Git commit/remote state after verification. Acceptance: another agent can identify what is done and what is *not*; cross-repo source location explicit; failed sync recorded, not concealed. Dependency: called at meaningful transitions. Historical R03/R41–R50.

## Common candidate conventions for later design

Every proposed template should eventually declare accepted inputs, required skills/resources and their locations, source-of-truth pointers, stable task identifiers, read/write permissions, artifacts, dependencies, QC/approval policy, retry budget, state and event recording, and a non-Git standalone procedure. Subtemplates may bundle relevant `SKILL.md` instructions in the standardized template or inside a custom template/run under `agent-files/`; external references must not expand authority. None of these manifests has been implemented.

## Prompt 04 creative modules

Fourteen additional **design-only** creative templates C01–C14 are detailed in [CREATIVE-CATALOG.md](CREATIVE-CATALOG.md). These cover source assignment, offer truth, semantic pre-image approval, Meta copy, art direction, generation, deterministic branding, placement variants, export checks, independent visual/semantic QA, peer bakeoff, targeted correction, owner selection and provider handoff. See [CREATIVE-COMPOSITION-EXAMPLES.md](CREATIVE-COMPOSITION-EXAMPLES.md).

No template implementation or workflow engine was created during Prompt 04.

## Prompt 05 implementation modules

Fifteen further **design-only** modules M01–M15 now appear in [OPERATIONS-CATALOG.md](OPERATIONS-CATALOG.md), with five [operations workflow composition sketches](OPERATIONS-COMPOSITIONS.md). They cover Meta preflight, graph planning, audience, creatives, messaging, CRM, website, tracking, paused staging, independent QA, separate launch permission, provider reconciliation, insights, controlled iteration and cross-provider recovery. They remain proposals pending Prompt 07 PRD approval.
