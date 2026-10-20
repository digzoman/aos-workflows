# Research Evolution, Fan-Out and Subverticals

Prompt 03. Source facts marked **O**, design generalizations **P**.

## Observed timeline

- **September 21–24, earlier advertiser evidence:** Fred and Max separately held historic research. Source index required union, not replacement. [R01, R31]
- **September 24, broad four-bucket research:** six advertiser loops and twelve keyword loops with persistence gates, later 16 finalists and eight selected creatives. [R02–R05, R21–R29]
- **October 3–4, new buckets and independent review:** research/creative handoffs across Fred and Muse showed parallel independent work with later reconciliation rather than erasing dissent. [Previous R06–R09]
- **October 16, paid/organic split:** provisional broad social AI work divided into paid B9 and organic B10; historical source records preserved. [Previous R14]
- **October 19, sector expansion:** initial pool of many industries, ten qualitative vertical scores, admitted incomplete census and new research candidates. [R32–R35]
- **October 19, owner-prioritized studies:** owner business priorities, not only numeric ranking, determined which sectors to investigate. Trades discovery compared 30 subcategories, proposed several challengers and explicitly rejected the idea that five placeholder folders were preapproved. [R37–R40]
- **October 19–20, 15-run research portfolio:** setup-only Prompt 00 followed by separately authorized numbered audience runs, starting general SMBs, agency owners, experienced advertisers, general trades, then narrower verticals/trades. Each run had isolated work files and one portfolio tracker. [R41–R49]

## Critical interpretation

**O.** A portfolio folder can exist before a run is started. Each historical numbered run required its own user request and wrote checkpoints before and after browsing. No automatic background job started the next run. [R41, R43, R48]

**O.** Broad trade or gym research can produce a narrower owner hypothesis; a planned specialty follow-up remains *proposed* until authorized. A previously scored category can receive a different result after more-specific source checks, without invalidating historical evidence. [R34, R37–R40, R44, R47]

**O.** At inspection Run 10 had an active `PROGRESS.md` while its portfolio index still said NOT STARTED. That is summary lag, **not evidence of Run 10 completion**. [R48–R49]

## Proposed dynamic child-run generation

**P input:** approved research plan and allowed scope, versioned parent template, owner priority, candidate list, source standards, budget/coverage rules and shared skills.

1. Produce **suggested** run records with stable ID/slug, buyer, research question, inclusion/exclusion criteria, dependencies, source type and expected outputs.
2. Deduplicate against known completed/active runs; link to prior evidence and declare whether a new run is refresh, expansion or genuinely distinct.
3. Store generated runs separately within `agent-files/`. Distinguish suggested/planned from authorized/claimed/running/completed.
4. Apply configured authorization policy to each child or the whole batch. Historical 15-run behavior required separate messages, but V1 can support preauthorized multi-run parallelism where explicitly configured.
5. Claim each eligible child independently, preserve task-agent identity, and enforce external-browser rate/cost limits.
6. Each child emits progress, evidence, a seven-criterion score, independent confidence, limitations and QC verdict; final parent synthesis consumes only authorized accepted outputs.
7. Refresh a **derived** portfolio view from the source-of-truth child states. Warn when a cached/indexed summary is stale.
8. Propose new conditional subvertical children from evidence, requiring the correct approval before starting them.

**P state distinction:** lifecycle (PLANNED/WAITING_APPROVAL/RUNNING/WAITING_QC/COMPLETE/etc.), finding (PASS/FAIL_AGE/RETRY_REQUIRED/etc.), evidence quality, strategic disposition (LAUNCH CANDIDATE/RESEARCH MORE/DEFER), and authorization must be separate dimensions.

## Parallel and conditional execution

**P:** When an owner authorizes an entire portfolio, independent child runs can fan out across multiple agents while deduping shared source edits through explicit locking/claim coordination. Evidence synthesis waits for required QC, not simply the number of created folders. A missing source may route to retry/fallback; weak market evidence may route to narrower segment discovery; a policy concern may trigger extra specialist review. Unrelated approved runs can continue.

Research batches repeated manually in historical conversations. That does **not** prove a recurring scheduler. Schedule metadata and step-local skills requested in AOS-W Prompt 01b are new framework requirements to be designed separately from the observed history.
