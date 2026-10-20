# Ampgent Workflow History, Source Index

Prepared 2026-10-20 as **Prompt 02 research evidence**, not a workflow template or technical design approval.

## Scope and responsible disclosure

- Period examined: primarily September 19 through October 20, 2026, with a few earlier project references when relevant.
- Primary directly inspected evidence: **private** `digzoman/a-rep-Max` repository documents read via the authenticated GitHub connector, plus directly viewed text from the open Ampgent B9.1 ChatGPT conversation. The user-provided project conversation history and the prior AOS-W discussion also provide context.
- **Public-repo safety:** this file records source *titles, relative paths, approximate dates, sanitized process summaries, and access status*. It does not copy internal messages, customer records, advertising account identifiers, Meta Library IDs, campaign payloads, raw research evidence logs, credentials, or personal conversation URLs.
- The private source repository path prefix **MAX** below means `digzoman/a-rep-Max`, branch `main`. Authorized readers may open `https://github.com/digzoman/a-rep-Max/blob/main/<relative-path>` while signed in. These are restricted-source pointers, not public copies.
- **Citations in this index are pointers for authorized reviewers**, not a claim that ordinary public visitors can open private material.
- Do not import private source documents wholesale into this public repo. Recheck sources when the workflow is adapted because current execution state can change.

### Evidence tiers

- **R, directly read:** authenticated GitHub file inspected in this research run. Strong for what that document *records*; not independent verification of a third-party service's current live state.
- **C, directly viewed:** authenticated ChatGPT browser tab text inspected. Strong for what the chat says; assistant claims within it are not independently verified unless corroborated by a persisted artifact.
- **P, project context:** titles/excerpts supplied in this project's context or accessible earlier transcript, but full original chat was **not** opened in this run.
- **L, located only:** directory or title confirmed, but body not examined. Treat conclusions as tentative until inspected.
- **I, analyst interpretation:** potential generalizable system requirement. Not itself historical evidence.

## A. Ampgent project conversation index

ChatGPT conversation links are deliberately not reproduced in this **public** GitHub repository. The source title and project name are the locator within the user's private Ampgent ChatGPT project.

| ID | Chat title, approx date | Workflow category | Accessible evidence and limitation |
| --- | --- | --- | --- |
| C01 | `x AOS-Workflows 1`, Oct 16–20 | Framework concept, lifecycle retrospective | **P**. Prior conversation transcript was provided in the current project context and included the original ad-research-to-launch workflow description, framework conventions, handoffs, and QC. Full live chat not opened here. |
| C02 | `AOS-Workflows 2`, Oct 20 | V1 survey, architecture, Prompt 01/01b/02 | **C/current conversation**. User decisions directly available; canonical sanitized decisions are in this repository's `temp/DESIGN-DECISIONS.md`. |
| C03 | `B9: Paid Social Media Mktg Ai 1`, about Oct 15–17 | B9 offer, ad copy, creative creation, publishing claims | **P/L**. Title/link confirmed in project sidebar and relevant excerpts available in current project context. Original message body was not opened in this run. |
| C04 | `B9: Paid Social Media Mktg Ai 2`, about Oct 17–19 | New verticals, 15-run plan, prompts and handoff | **P/L**. Title confirmed in project sidebar and earlier excerpts in context. Corroborated by MAX portfolio prompt sequence and run index. Full live chat not opened. |
| C05 | `B9: Paid Social Media Mktg Ai 3`, Oct 19–20 | Separately authorized vertical research runs, evidence/QC and Git commits | **C**. Directly viewed current browser tab, including completed-run messages through Run 09 and an in-progress Run 10. Completeness assertions checked against the MAX run index; do not report Run 10 complete. |
| C06 | `B9: Social Media Mktg Ai 1b Deep Research`, about Oct 16 | Paid-versus-organic positioning and market assessment | **P**. Excerpts in project conversation context only; full source not opened. |
| C07 | `B1-7: Ads Management 2 - Ampgent Meta Launch Review`, about Oct 14–16 | Preflight, targeting corrections, launch and post-launch monitoring | **P**. Project context shows launch authorization, pausing a weak creative, CPC/CTR requests, geography corrections. Direct activation record is MAX R11 below. Full original chat not opened. |
| C08 | `Audit Ad Geographies`, about Oct 9–15 | Account-wide geographic and age targeting reviews | **P**. Excerpts available; corroborated by MAX audience-targeting revision files. Full source not opened. |
| C09 | `Ampgent Blogs Case Studies 2`, about Oct 15 | Case study writing, cross-agent marketing system narrative and editorial cover | **P**. Project excerpts show article/cover work. Publication state not verified. |
| C10 | `B1-7 Ads Management` and predecessor creative preparation chats, Sep–Oct | Source matching, selected offers, creative revision and Meta staging | **P**, exact individual conversation URLs/titles not fully established here. MAX creative/research artifacts provide stronger evidence. |
| C11 | `Check HighLevel Access` and `HighLevel Overview Access Failure`, about Oct 9 | CRM connector access and tool limitations | **P**. Prompt excerpts show access checks and a failure report; neither proves full working CRM integration. |
| C12 | Ampgent website redesign and implementation conversations, about Oct 8–16 | Landing pages, site QA, dev-to-production handoff | **P**. Specific full chat title not verified in this run. MAX website design/handoff files are directly inspected. |

## B. Directly inspected repository evidence

All paths are relative to the restricted MAX repository root unless otherwise stated. File dates below come from the file title or recorded header, not independent Git commit chronology.

| ID | Approx period | Restricted-source pointer | Primary workflow evidence |
| --- | --- | --- | --- |
| R01 | Sep 24 and Oct 16 | `work/ampgent-adaptive-offer-testing/README.md` | Ownership of marketing records moved from Fred to Max; keyword research, shortlists, creative recreations and later paid/organic bucket split. **R** |
| R02 | Sep 24–Oct | `work/ampgent-adaptive-offer-testing/meta-ad-research-refresh-2026-09-24/README.md` | Objective, four-bucket classification, two longevity thresholds, evidence contract, live-source and access-failure rules. **R** |
| R03 | Sep 24–Oct | `work/ampgent-adaptive-offer-testing/meta-ad-research-refresh-2026-09-24/PROMPT-PACK.md` | Startup prompt, six advertiser batches, twelve keyword batches and per-bucket creative loops. Each iteration reloads queues and persists progress. **R** |
| R04 | Sep 24–Oct | `work/ampgent-adaptive-offer-testing/meta-ad-research-refresh-2026-09-24/PROGRESS.md` | Actual batch checkpoints, retry-required browser rows, multi-pass independent source-match QA, errors corrected and final states. **R** |
| R05 | Sep–Oct | `work/ampgent-adaptive-offer-testing/meta-ad-research-refresh-2026-09-24/SOURCE-MATCH-RUBRIC.md` | Multi-criterion quality scoring and mandatory pass floors, including truthfulness. **R** |
| R06 | Oct 3 | `work/ampgent-adaptive-offer-testing/meta-ad-bakeoff-2026-10-03/HANDOFF-FRED-MUSE.md` | Cross-agent replacement of an unavailable collaborator, independent evidence before reciprocal comparison, explicit coordination surfaces. **R** |
| R07 | Oct 3 | `work/ampgent-adaptive-offer-testing/meta-ad-bakeoff-2026-10-03/FINAL-SYNTHESIS.md` | Independent agent evidence was merged, discrepancies corrected, false source categorization rejected. **R** |
| R08 | Oct 4 | `work/ampgent-adaptive-offer-testing/meta-ad-creative-bakeoff-2026-10-04/BRIEF.md` | Fred and Muse independent visual production, separate artifacts, reciprocal critiques and preservation of original work. **R** |
| R09 | Oct 4 | `work/ampgent-adaptive-offer-testing/meta-ad-creative-bakeoff-2026-10-04/SEMANTIC-MATCHING-SPEC.md` | Quality gates on buyer, painful problem, hooks and truthful offers before visual production. **R** |
| R10 | Sep 26–Oct 15 | `work/ampgent-adaptive-offer-testing/meta-ad-creatives-v3-five-buckets-2026-09-26/PROGRESS.md` | Approved set, cross-repo false-unavailable incident, creative packs, QA and staged Meta preparation. **R** |
| R11 | Sep 28–Oct | `work/ampgent-adaptive-offer-testing/meta-ad-creatives-v3-five-buckets-2026-09-26/META-STAGING-2026-09-28.md` | Paused-only campaign staging, external object read-back and recovery from a timeout-related duplicate creation. **R** |
| R12 | Oct 15 | `work/ampgent-adaptive-offer-testing/meta-ad-creatives-v3-five-buckets-2026-09-26/META-AUDIENCE-TARGETING-2026-10-15.md` | Applied targeting revision that explicitly supersedes an earlier version; hypotheses distinguished from actual conversion results. **R** |
| R13 | Oct 15 | `work/ampgent-adaptive-offer-testing/meta-launch-2026-10-15.md` | Recorded owner authorization, controlled hierarchical activation, early API rate-limit/read-back gap and later partial confirmation. **R** |
| R14 | Oct 16 | `work/ampgent-adaptive-offer-testing/meta-ads-buckets-9-10-2026-10-16/README.md` | Revised taxonomy into paid and organic categories, source evidence tables and explicit research-only authority. **R** |
| R15 | Oct 16 | `work/ampgent-adaptive-offer-testing/meta-ad-bucket-9-2026-10-16/muse/MUSE-B9-STATUS.md` | Long GitHub-access/tool delay, alternate connector recovery, missing live Meta ad IDs honestly marked unknown. **R** |
| R16 | Oct 19–20 | `work/ampgent-adaptive-offer-testing/meta-ads-buckets-9-10-2026-10-16/bucket-9-paid-marketing/ampgent-9.1-ai-media-buyer/vertical-expansion-research-2026-10-19/portfolio-15-sequential-research-2026-10-19/README.md` | Separate setup prompt, fifteen individually authorized runs, cross-vertical tracker, no premature folder creation. **R** |
| R17 | Oct 19–20 | `work/ampgent-adaptive-offer-testing/meta-ads-buckets-9-10-2026-10-16/bucket-9-paid-marketing/ampgent-9.1-ai-media-buyer/vertical-expansion-research-2026-10-19/portfolio-15-sequential-research-2026-10-19/SETUP-ACCESS-CHECK.md` | Setup-only browser and GitHub verification, truthful limitation on user-visible VM, prohibition on expanding setup scope. **R** |
| R18 | Oct 20 | `work/ampgent-adaptive-offer-testing/meta-ads-buckets-9-10-2026-10-16/bucket-9-paid-marketing/ampgent-9.1-ai-media-buyer/vertical-expansion-research-2026-10-19/portfolio-15-sequential-research-2026-10-19/RUN-INDEX.md` | Nine runs recorded completed, remaining runs unstarted at inspected revision; per-run progress, evidence, scorecard and report contract. **R** |
| R19 | Oct 8 | `work/ampgent-website-redesign-2026-10-08/README.md` | Separate website content/design/source/QA and deployment handoff; staged work clearly marked not production authorized. **R** |
| R20 | Oct 8 | `work/ampgent-website-redesign-2026-10-08/PROMPT.md` | Detailed website scope, source ownership, planned QA, isolated handoff to technical operator and explicit deployment authority. **R** |

## C. Additional located primary artifacts, to deepen during Prompts 03–05

These were listed in directories, but not all individual bodies were read. **L** unless linked from an R document.

- `meta-ad-research-refresh-2026-09-24/KEYWORD-QUEUE.md`, `KEYWORD-RESULTS.md`, `ADVERTISER-QUEUE.md`, `ADVERTISER-RESULTS.md`, `FINAL-REPORT.md`, `SOURCE-MATCH-AUDIT.md`, `CREATIVE-MATRIX.md`.
- `meta-ad-creatives-v3-five-buckets-2026-09-26/` candidate folders, `SOURCE-MATCH-QA-2026-09-26.md`, `META-MESSAGING-TEMPLATE-RULES.md`.
- `meta-ad-creative-bakeoff-2026-10-04/` agent-specific folders and independent critique files.
- `meta-ads-buckets-9-10-2026-10-16/` evidence ledgers and the newer individual research report/scorecard/evidence files under `runs/`.
- `work/ampgent-website-redesign-2026-10-08/qa/`, `handoff/FRED-DEPLOYMENT-HANDOFF.md`, `design/`, `research/`.
- A Rep `procedures/skills/plan-work/SKILL.md` and `data-ledger/SKILL.md`, and Max's `scratch/skills/add-ampgent-logo/` as follow-up reusable-skill candidates.

## D. Coverage statement

This index establishes concrete historical workflows for search planning, batch research, evidence/QC, creative production, revision, paused staging, launch and its verification limitations. It **does not** independently verify today's live Meta campaign delivery, performance metrics, HighLevel functionality, production site status, or final completion of research Run 10. No proprietary project transcripts were exported.

Next: use R02–R05/R16–R18 for Prompt 03 research; R08–R10 for Prompt 04 creative research; R11–R13/R19–R20 for Prompt 05 implementation/deployment research.

## E. Prompt 03 source expansion

Thirty further directly inspected Max repository documents, R21–R50, are registered with exact restricted relative locators and evidence purposes in [SOURCE-ADDENDUM-03.md](SOURCE-ADDENDUM-03.md). The new research interpretation and candidate template specifications are in [RESEARCH-WORKFLOW-MODEL.md](RESEARCH-WORKFLOW-MODEL.md) and [candidate-templates/CATALOG.md](candidate-templates/CATALOG.md). **This does not imply updated independent live Meta verification.**

## F. Prompt 04 creative production source expansion

Thirty-one additional restricted Max documentation sources, R51–R81, are indexed in [creative-production/SOURCE-INDEX-04.md](creative-production/SOURCE-INDEX-04.md). New files document B1–B9 creative production, the canonical logo skill, image generation and correction, QA, approvals, asset versions and Meta staging boundaries. These notes do **not** imply current independent pixel inspection or production delivery verification.

## G. Prompt 05 Meta operations, CRM, launch and tracking evidence

Twenty-six additional directly inspected private repository/issue records R82–R107 are catalogued in [campaign-operations/SOURCE-INDEX-05.md](campaign-operations/SOURCE-INDEX-05.md). Staged and activated Meta state, rejected operations, adset geo/age revisions, HighLevel bot configuration/behavior distinction, Pixel/CAPI dedup uncertainty and website DEV/PROD release authority are described. These are historical document reads, not current live provider checks.
