# Historical Workflow Patterns and Evidence-Based Cases

Prepared under Prompt 02. These are **sanitized analytical summaries of prior work**, not new AOS-W design approvals. The source IDs refer to [SOURCE-INDEX.md](SOURCE-INDEX.md). The restricted source files should be consulted for the full evidence.

## Observed end-to-end pattern

1. **Scope/authorization**: specify task limits, owner approvals and source of truth, sometimes in a setup-only prompt. Evidence R02, R03, R17.
2. **Plan and decompose**: assemble keyword/advertiser queues or a numbered vertical run index with stable work IDs and output contracts. R03, R16–R18.
3. **Execute independent work**: take the next pending batch or separately authorized numbered run and record observations, with source/confidence. R03–R04, R18 and C05.
4. **Checkpoint**: write results, status and evidence to GitHub; on retry resume at the first not-yet-verified item, not the next presumed item. R04 and R17.
5. **Assess/QC**: independent evidence checks, mandatory thresholds, truthfulness, source-match and creative validation. R05, R07–R10.
6. **Correct/replan**: retry inaccessible searches, revise deficient creative assets, update targeting conclusions, or split research categories while keeping historical provenance. R04, R07, R10, R12, R14.
7. **Integrate and stage**: create approved external configurations in paused/preproduction state and read back actual provider objects. R11, R19–R20.
8. **Authorize and activate**: human directive distinguishes staging from spending/publishing; launch parent/child objects in a controlled order. R13.
9. **Verify live state and monitor**: distinguish accepted API writes, persisted effective status and actual delivery/performance. R13 and project-context C07.

## Case 1. Research planning, sequential batches, and restart after browser failure

**Direct evidence:** R02–R04. The research refresh used a startup prompt, six advertiser verification loops, twelve keyword-sweep loops, and separate creative loops. Agents read authoritative queue/progress files at each iteration instead of trusting chat memory. Progress recorded completed loops and statuses separately.

**Observed failure/recovery:** Several keyword lookups were marked `RETRY_REQUIRED` when browser access was unreliable, then revisited with a fresh legitimate session. They were not counted as "no ad evidence" merely because a lookup failed. The source's later progress document recorded completion after retries and reconciliation.

**Generalizable lesson (I):** distinguish `PENDING`, `IN_PROGRESS`, `RETRY_REQUIRED`, `BLOCKED`, `NO_EVIDENCE_VERIFIED`, and `COMPLETE`; a transient tool failure must not mutate the substantive research conclusion.

**Candidate template (I):** research-plan -> batch runner -> checkpoint -> evidence integrity reviewer -> finalizer, with configurable queue selection and retries.

## Case 2. QC that detects meaningful weakness rather than mere file presence

**Direct evidence:** R04, R05, R09–R10. Source-match criteria covered buyer, problem, hook, vocabulary, visual grammar, captions and truthful representation. The progress file records an earlier QC attempt that only reviewed part of a subsequently expanded creative set, as well as revision cycles that later passed the mandatory criteria.

**Observed correction:** Creative QA prompted a layout adjustment to move a CTA/disclosure away from unsafe feed margins, and source-matching revisions addressed weaker adaptations before final acceptance.

**Generalizable lesson (I):** a quality gate needs the input version or artifact set it reviewed. A passed gate for an earlier 2-item set must not automatically approve the later 8-item set.

**Candidate template (I):** source-brief -> copy QA -> asset generation -> visual + technical QA -> independent semantic QA -> remediation -> approval.

## Case 3. Cross-repository handoff falsely interpreted as missing work

**Direct evidence:** R01 and R10. A staging/creative handoff incorrectly treated existing source/ranking files as unavailable because they were stored in another agent repository. The work documentation later corrected the source location.

**Generalizable lesson (I):** every handoff should carry absolute repository identity, branch/revision, relative artifact paths, authority/source-of-truth, and a verification procedure. "File missing in this repository" is different from "no file exists."

**Candidate template (I):** handoff preflight that checks all dependency locations and records failures with exact repository and path.

## Case 4. Independent agent research and peer review without copy-forward contamination

**Direct evidence:** R06–R08. Fred and Muse had separate research artifacts and reciprocal review roles. When a planned collaborator became unavailable, Fred was assigned as an independent counterpart. The handoff required independent evidence before reading the other agent's rankings; later synthesis corrected an incorrectly categorized candidate rather than averaging away a disagreement.

**Generalizable lesson (I):** preserve independent reviewer inputs, role changes, separation of duties, and rejected findings. QC should distinguish factual contradiction from harmless differences in opinion.

**Candidate template (I):** independent parallel branches -> locked submissions -> peer-review -> reconciliation -> final synthesis with dissent/evidence.

## Case 5. API timeout caused duplicate external objects during staging

**Direct evidence:** R11. Paused-only Meta staging contained a failed attempt and timeout-recovery episode that left an unwanted duplicate ad set/ad and unused creative. The work record describes cleanup and identifies the intended retained objects. The external system, rather than a local plan file, was authoritative for created objects.

**Generalizable lesson (I):** after ambiguous external API success or timeout, read back by stable operation identity before retrying creation. Detect and reconcile orphaned/duplicate objects. A local "completed" flag must not substitute for a live read-back.

**Candidate template (I):** external-action preflight -> request with idempotency/reconciliation key -> provider read-back -> duplicate check -> corrective action -> checkpoint.

## Case 6. Successful launch calls were not the same as full delivery verification

**Direct evidence:** R13. The activation record documented explicit owner authorization, constrained campaign selection and a hierarchical activation order. The immediate provider read-back hit an API rate limit. A later call confirmed the selected campaigns at campaign level, while full ad-set and individual-ad effective serving remained incompletely verified in that record.

**Generalizable lesson (I):** model authorization, accepted write, persisted configured state, effective delivery and measurable business outcomes as **different evidence states**. A rate-limited readback becomes a follow-up action, not an unsupported "everything live" assertion.

**Candidate template (I):** human-authorized launch -> child/parent activation -> layered provider verification -> review-status check -> spend/impressions/lead monitoring.

## Case 7. Dynamic category revision preserved historical evidence

**Direct evidence:** R01, R14. A provisional social-media AI category was later split into paid and organic research categories. Earlier Fred/Muse records remained historical; the newer source index adopted the revised taxonomy instead of retroactively treating the old classification as though it never existed.

**Generalizable lesson (I):** record taxonomy/revision migrations, source mappings, rationale, unchanged archived evidence, and whether dependent tasks must be rescored or rerun.

**Candidate template (I):** evidence-driven replan proposal -> revision gate -> migration map -> selective recomputation -> audit log.

## Case 8. Fifteen-run vertical research with a separate setup authority boundary

**Direct evidence:** R16–R18 and directly viewed C05. The project created a setup-only Prompt 00, a stable 15-run portfolio and a separately authorized prompt for each audience. Each run used its own progress, evidence, scorecard and final report, plus a cross-run tracker. At the inspected GitHub revision, runs 01–09 were completed, 10–15 not started; the directly viewed chat showed Run 10 in progress, **not completed**.

**Generalizable lesson (I):** a planned run is not an authorized or started run. An in-progress chat may be ahead of a persisted index. Reconcile updates before reporting the authoritative latest state. Keep per-run artifacts isolated, and defer aggregation until required QC.

**Candidate template (I):** setup access gate -> plan-and-generate N runs -> authorize individual run -> evidence -> independent QC -> update portfolio summary.

## Case 9. Research tool capability differences and verification uncertainty

**Direct evidence:** R15, R17. One research session recorded slow/failed GitHub issue access and switched to a confirmed available connector; incomplete direct Meta source evidence was marked unknown. A later setup verification confirmed that headless browser access existed but a user-visible live browser link was unavailable.

**Generalizable lesson (I):** capability detection should be source- and session-specific. An alternative connector does not make the original tool's limitations disappear. Every evidence record needs verification status and the last actually observed source.

**Candidate template (I):** environment preflight -> declared capabilities -> evidence collection with fallback -> explicit unknown/unavailable states.

## Case 10. Website handoff between design and deployment roles

**Direct evidence:** R19–R20. The Max workspace separated content, design, page inventory, source files, QA and deployment handoff. The recorded source package was staged, while technical deployment and production authorization were separate steps for a different role.

**Generalizable lesson (I):** artifact readiness, development deployment, production release and authorization are distinct gates. Multi-agent handoffs should include source location, tested build state, environment, outstanding checks, and prohibited actions.

**Candidate template (I):** content/design -> build -> static tests -> handoff -> DEV deploy -> browser QA -> production approval -> prod read-back.

## CRM and monitoring coverage is thinner

Project-context conversations refer to HighLevel access, chatbots, Meta lead tracking, Good Lead signals, booking events, website routing, and CPC/CTR follow-up. This run did **not** independently inspect a current authoritative HighLevel workflow or Meta insights report. No current integration pass or performance figures are asserted. Prompt 05 must inspect direct integration/QA artifacts and provider readbacks before classifying those modules as demonstrated end-to-end.

## Provisional template candidate list for Prompts 03–05

1. Environment and source access preflight.
2. Research plan and keyword/advertiser discovery.
3. Next-pending research batch / numbered vertical run.
4. Evidence capture, classification and source-confidence QA.
5. Independent peer review and remediation.
6. Cross-run synthesis and evidence-scored opportunity comparison.
7. Offer strategy and truthful competitive adaptation.
8. Creative copy, image, branding, visual QA and revision.
9. Meta configuration preflight, paused staging and read-back.
10. CRM/landing-page/tracking preparation and integration QA.
11. Explicit prelaunch authorization, activation and verification.
12. Metrics monitoring, diagnostics and controlled iteration.
13. Cross-agent handoff, interrupted recovery and dynamic replan.

These are **research-derived candidates**, not implemented files or an approved technical schema.
