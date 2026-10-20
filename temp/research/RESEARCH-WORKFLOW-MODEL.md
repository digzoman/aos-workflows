# Competitor Advertising Research Workflow Model

Prompt 03, 2026-10-20. **O = directly observed in historical source documents. P = proposed AOS-W generalization, not yet approved or implemented.** See [SOURCE-ADDENDUM-03.md](SOURCE-ADDENDUM-03.md) for primary document IDs.

## Two complementary execution patterns

**O, queue-driven discovery.** The September refresh executed 34 advertiser checks in 6 batches and 96 keyword searches in 12 batches. It reconciled 131 deduplicated active offer families, ranked four per each of four buckets, and then selected one first choice and runner-up per bucket for creative work. Per-invocation prompts always read queues and progress, worked the next pending group, wrote evidence and committed a checkpoint. [R02–R05, R21–R28]

**O, separately authorized vertical portfolio.** The later B9.1 suite contained setup-only Prompt 00 plus 15 explicitly ordered audience prompts. Each research run had a dedicated progress file, source evidence log, scorecard and report, with an aggregate index and tracker. Preparing a prompt did not authorize the run, and finishing research did not authorize any Meta change. [R36–R50]

**P, compound workflow.** Support both an ordered queue worker and fan-out into independently tracked vertical children, then evidence validation, synthesis and optional downstream creative handoff.

```text
Scope and authority
       |
Environment + source preflight
       |
Research plan + versioned standards
       |
  +----+-------------------------------+
  |                                    |
Advertiser/keyword queues       Portfolio of verticals
  |                                    |
Batch workers and retries       Proposed child instances
  |                                    |
Candidate normalization         Explicit start authorization
  |                                    |
Coverage finalizer              One isolated run per vertical
  |                                    |
Source-ad rubric                Seven-axis vertical scoring
  |                                    |
Independent evidence QC         Independent run QC
  +----------------+-------------------+
                   |
             Cross-run synthesis
                   |
       Decision and bounded handoff
          (not launch permission)
```

## Reconstructed stage contracts

### 00. Context recovery and preflight

**O [R03, R41, R50].** Setup identifies branch/repo, authorized output paths, saved standards, browser and GitHub capabilities, canonical offer and prohibited actions. October Prompt 00 was setup-only and stopped before live competitor research.

**P input:** approved task/scope, source pointers, selected workflow template revision, environment requirements. **P output:** readiness and source-of-truth record, capabilities, limitations and allowed operations. **P gate:** required tools verified or explicit reduced-scope authorization; setup authority cannot mutate marketing production.

### 01. Define research question and buyer taxonomy

**O [R02, R32–R40].** Categories shifted from four broad AI-offer buckets, to added implementation/talent buckets, to separate paid versus organic B9/B10, then to specific businesses buying Meta-ad solutions. Broad trades were challenged with 30 specialty candidates. Owner preferences selected what to research rather than accepting numerical rank as authority.

**P input:** business question, existing approved offer, historical taxonomy, stakeholder priorities. **P output:** target buyers, included/excluded types, markets, hypotheses, finite scope and taxonomy version. **P gate:** audience is the *purchaser of the advertising solution*, not the seller's business or a consumer receiving the advertised service.

### 02. Build advertiser and keyword discovery queues

**O [R21, R23, R31–R33].** Bookmark evidence and prior keyword research seeded queues. Broad searches had a roughly 60-day active-ad filter, long-tail or advertiser checks 23 days; each queue row carried priority, family and status. New relevant keywords were deferred, not allowed to derail current batches.

**P input:** approved audience, search playbook, source bank. **P output:** stable prioritized tasks with exact keyword/advertiser, market, class-specific filters and source-level criteria. **P gate:** no duplicate query IDs, coverage standards explicit, scope expansion tracked and approved as required.

### 03. Process next advertiser batch

**O [R03, R21–R22].** Up to six next pending advertisers per prompt, confirm actual offer family, relevant active dates and creative format, search older same-family variants, record result and score; preserve FAIL_AGE, FAIL_RELEVANCE, NOT_FOUND and BLOCKED rather than deleting failures.

**P input:** claimed advertiser tasks, source policy, live-browser availability. **P output:** observation records, result statuses, deferred discovery leads, provisional candidates. **P gate:** source date, actual advertiser/page and justified status, without promoting too-new ads merely because hooks are attractive.

### 04. Process next keyword batch

**O [R03, R23–R24].** Eight next pending keywords per prompt. US active-ad search was the primary sample, with Canada/other filters used when relevant. Inspect beyond first card; capture rank context only when actually visible; dedupe IDs and advertiser/offer families; upgrade previous provisional scores only if ranking evidence is now available.

**P input:** claimed query, age threshold, market/source. **P output:** query record, sampled cards, source links, deduplicated candidate updates and retry notes. **P gate:** no invented rank, age, creative, full ad counts or market absence. An unexplained blank gallery becomes RETRY_REQUIRED or BLOCKED, not EMPTY_VERIFIED.

### 05. Normalize candidates and source confidence

**O [R25–R27, R31–R36, R47].** Candidate identity was advertiser+material hook/offer family, with direct ad ID and variants retained separately; vendor brands and underlying shared platforms were considered before independent seller counting. Old Fred evidence and newer Max results were unioned rather than overwritten.

**P input:** batch observations plus provenance of older work. **P output:** normalized entity ledger, deduplication map, observed evidence class, source freshness, seller independence, unknown fields. **P gate:** direct verified Meta ad evidence distinct from landing-page descriptions and from inference.

### 06. Finalize research coverage and handle exceptions

**O [R03–R04, R27, R34].** Section 1B reconciled terminal advertiser statuses. Section 2B retried the highest-value blocked keyword searches and compared legacy candidates. The initial vertical study was delivered despite failing its aspirational coverage target, and explicitly recorded limitations.

**P input:** queue state and evidence completeness report. **P output:** finalizer verdict, outstanding high-value searches and gaps. **P gate:** no unfinished query silently counted done; bounded fallback attempts; insufficient coverage may produce DELIVERED_WITH_LIMITATIONS or require another pass.

### 07. Score source advertisements

**O [R25–R28].** Full ad score combined observed search prominence, active duration and related variant strength. Advertiser-only observations received PROVISIONAL scores without meaningful prominence data. Selection of four per bucket also respected buyer fit, offer fidelity, diversity and practical creative adaptation.

**P input:** qualifying ad-family ledger, source-ad rubric revision. **P output:** full or provisional score, component evidence, shortlist and explicit rejection rationale. **P gate:** do not infer profitability, conversion, true targeting or Meta advertiser spend.

### 08. Score business verticals and narrow subsegments

**O [R33–R39, R43–R47].** The later vertical work scored seven weighted criteria, reported confidence separately and often recommended a qualified owner subsegment rather than an overly broad audience. DFY agency demand was not considered direct proof of DIY AI software willingness.

**P input:** qualified owner-facing supplier evidence, canonical product feature boundaries, seven-axis rubric revision. **P output:** component scores with explanations, evidence confidence, buyer/market shortlisting, compliance caveats and recommended decision. **P gate:** scores not presented as measured leads, CAC, ROAS or conversion, and prior scores not silently promoted to fresh evidence.

### 09. Independent QC and targeted corrections

**O [R04–R05, R06–R09, R29–R30].** Separate Fred/Muse work preceded reciprocal peer comparison; source-match audit later found semantic drift and demanded revisions. One earlier QA examined only a subset of a larger final creative collection.

**P input:** exact artifact set/version, rubric and independent reviewer identity. **P output:** pass, revise, insufficient evidence or blocked, with precise failing items and correction path. **P gate:** gate approval covers only submitted artifact set; revisions trigger selective re-review without repeating unrelated branches.

### 10. Synthesize and hand off

**O [R27–R28, R34–R39, R41–R49].** Research reports separated observation, inference and recommendations. Strategic dispositions included LAUNCH CANDIDATE, RESEARCH MORE and DEFER. Runs ended with persisted status and next explicitly authorized prompt. Proposed future creatives/ad sets were outside research authority.

**P input:** QC-accepted candidate/vertical results, stakeholder priority and unresolved evidence. **P output:** sourced synthesis, ranked portfolio, dissent and gaps, requested next stage and approval requirements. **P gate:** no claimed launch approval merely because research completed or recommendation says LAUNCH CANDIDATE.

## Observed historical status vocabularies

- Advertiser results, PENDING, PASS, FAIL_AGE, FAIL_RELEVANCE, NOT_FOUND, BLOCKED. [R21–R22]
- Keyword results, PENDING, DONE, EMPTY_VERIFIED, RETRY_REQUIRED, BLOCKED. [R23–R24]
- Scoring, FULL versus PROVISIONAL, HIGH/MEDIUM/LOW *confidence* for vertical opportunity research. [R25–R26, R36]
- Portfolio, NOT STARTED, IN PROGRESS, COMPLETED. Strategic recommendation is a **separate** LAUNCH CANDIDATE, RESEARCH MORE, DEFER. [R41–R49]

**P.** Store generic lifecycle status, domain research outcome, evidence-quality status, market recommendation and execution approval as separate fields. One universal `status` cannot capture all five correctly.

## Portability and authority

Historical work depended on GitHub and browser connectors, but AOS-W must not require Git. **P:** use per-run files as standalone authority and treat Git portfolio indexes as rebuildable views when configured. Multi-agent parallelism is optional and must use independently authorized child tasks and safe coordination. Skills and recurrence metadata are newer AOS-W requirements from Prompt 01b, not capabilities established by historical runs.
