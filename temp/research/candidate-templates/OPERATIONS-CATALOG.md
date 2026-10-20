# Prompt 05 candidate reusable campaign operations templates

**Design-only**, not runnable or approved workflow files. Historical source grounding R82–R107 in [../campaign-operations/SOURCE-INDEX-05.md](../campaign-operations/SOURCE-INDEX-05.md). Common contract for every template: scope/permissions, exact provider/local source identities, input versions, output artifacts, deterministic/AI/human quality gates, owner/provenance, retry budget, compensation, provider read-back and optional just-in-time skill references. Default launch is **non-repeating/ad hoc**; scheduled monitoring is optional host-triggered work and must never imply always-on AOS-W.

| ID | Candidate template | Key inputs -> durable outputs and acceptance gate |
| --- | --- | --- |
| M01 | Meta access and baseline readback | Account access/approved scope -> real campaign tree snapshot, cap/budgets, required permissions; fail closed if no provider access. |
| M02 | Campaign/adset/ad specification | Approved stable offer/media/copy -> desired parent/adset/creative/placement graph, account cost exposure and exact exclusions; owner approves. |
| M03 | Targeting/geo/age review | Current Meta readback + approved buyer/regions -> explicit before/after targeting plan with standard/Advantage+ semantics; no accidental exclusion loss. |
| M04 | Image/creative/media binding | Approved copy/media hashes -> uploaded image IDs and actual attached ad creative/CTA mapping; verify every variant and original source. |
| M05 | Selectable questions and fingerprint | Exact messaging intent + offer routing -> full Meta Question, null Response, fingerprint; provider readback and route tests. |
| M06 | HighLevel bot/CRM preparation | Canonical offer and regression set -> scoped knowledge + expected chat/booking behavior; saved config and actual behavior separate gates. |
| M07 | Website landing/CTA and DEV staging | Offer paths, original site sources, consent policy -> site build + hosted DEV/preview QA and rollback details; no implicit PROD deploy. |
| M08 | Tracking taxonomy and Pixel/CAPI QA | Funnel milestones + privacy/consent + source truth -> actual event/trigger/dedup/attribution contract, safely verified in provider; block unknown GHL logic. |
| M09 | Meta PAUSED staging | Approved graph and STAGE_PAUSED authorization -> existing-object reconciliation, idempotent create/update, paused final readback. |
| M10 | Independent prelaunch QA | Actual Meta config, image previews, routing, CRM, tracking, holds -> granular PASS/PENDING/FAIL with issue-specific remediation; separate launch authorization required. |
| M11 | Explicit launch authorization | Human direction, selected object tree, budget, holds -> immutable launch permit limited to exact campaigns/adsets/ads and approved versions. |
| M12 | Controlled activation and reconciliation | Launch permit + fresh snapshot -> child-first activation attempt log, provider readback, held-sibling check, deferred rate-limit verification. |
| M13 | Read-only campaign insights and attribution | Meta reporting window + CRM state -> CPC/CTR/cost and message outcomes, observed vs estimated labels, source/time and tracking caveats. |
| M14 | Targeted optimization and correction | Verified findings + authority -> scoped changes, before/after provider reconciliation, compensation plan and new QA for affected descendants. |
| M15 | Cross-provider handoff and incident recovery | Exact source/deploy revisions, prior state, failures and authorized permission -> resumable handoff with source-of-truth and next eligible action. |

## Gate category examples

G-M0 approved stable source/offer and permissions. G-M1 provider access and baseline inventory. G-M2 exact campaign structure, currency, objective, budget and scope. G-M3 hard targeting and exclusions. G-M4 image/copy/CTA message field and preview. G-M5 GHL saved knowledge and separately tested real channel behavior. G-M6 website hosted/consent/UTM links. G-M7 truthful booked/qualified conversion definitions, source and dedup. G-M8 independent PAUSED provider readback. G-M9 explicit live launch approval. G-M10 post-write configured/effective status plus review/delivery evidence. G-M11 real insights and source-qualified metrics. G-M12 exact documented compensation and revision history.

These gates have different reviewers: deterministic comparison for exact hashes/field presence/targeting; AI/visual reviewer for preview crops/semantic message consistency; real browser/CRM tester for end-to-end flows; user for new spend/production authorization. A file-only workflow can *record* these checks but cannot claim technically enforced provider operations without host access.

## Narrow remediation examples

- **Invalid placement rule** -> revise creative mapping or generate an approved square, do not recreate campaigns or redo research.
- **Wrong geo** -> apply exact targeting diff, preserve budget/ad IDs/other interests, readback the corrected adset.
- **Meta activation read rate limit** -> retry GET after appropriate delay (if a host executor exists), never replay successful writes solely due to read failure.
- **Bad GHL offer routing** -> fix knowledge/test rules, preserve other offers, rerun only GHL and linked chat QA; don't rewrite approved image.
- **Double Schedule risk** -> investigate browser/server IDs and consent/dedup; leave actual ad campaign objective unchanged unless separately approved.
- **Bad website link** -> fix the specific page/CTA and recheck hosted DEV, obtain separate PROD release permission.

## V1 minimum pilot

Use mock/staged Meta objects and sanitized one-offer configurations, with simulated rate-limit and rejected creative rule, a paused preflight, exact image association, failed CRM integration, a separate owner authorization, accepted activation responses and later readback. An internal AOS-W test must explicitly distinguish mocked provider state from real Meta API execution.
