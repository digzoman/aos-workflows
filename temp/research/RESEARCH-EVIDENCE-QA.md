# Evidence, Scoring and Failure Modes

Prompt 03. **O** marks directly inspected source record; **P** marks a proposal for AOS-W. See [SOURCE-ADDENDUM-03.md](SOURCE-ADDENDUM-03.md).

## Two different score types that must not be conflated

### A. Advertisement / offer-family persistence score

**O [R25].** Candidate requires an active relevant Meta commercial ad and sufficiently specific, modelable hook, with historical age rule of ~60 days for broad queries and >=23 days for narrower terms/advertiser lookups.

`Full = 0.50 × prominence + 0.30 × longevity + 0.20 × variant strength`.

Longevity = `min(days_active / 180, 1) × 100`. Variant strength = `min((variant_count - 1)/6, 1) × 100`. Prominence uses observed rank in the accessible query sample with breadth qualification. When keyword prominence is not available, advertiser lookup uses `PROVISIONAL = 0.60 × longevity + 0.40 × variant strength`.

Historical output [R26–R27] included 131 families, across four buckets. **O:** duration, frequency of creative variants and estimated search position are proxies for persistent advertising, never direct financial performance.

**P:** template rubric `source-ad-persistence`, individually versioned. FULL only with actual observed ranking basis. Source age policy is configurable by query/class, not globally fixed.

### B. Business vertical opportunity score

**O [R36, R44, R47].** Seven criteria, with written rationale for each, total 100.

1. Independent, directly relevant Meta competitor evidence, 25.
2. Fit with the actual $47 owner-controlled creative and campaign toolkit, 20.
3. Paid-Meta suitability and plausible buyer economics, 20.
4. Self-service urgency and motivation, 15.
5. US/Canada market breadth, 10.
6. Truthful vertical-specific creative adaptability, 5.
7. Advertising and professional-policy compatibility, 5.

Separate **HIGH/MEDIUM/LOW evidence confidence** based on freshness, directness, depth and seller independence. Even 89/100 with MEDIUM confidence is a qualitative research prioritization, **not an estimated chance of commercial success**.

**P:** rubric `vertical-opportunity`, independent of ad-level persistence and parameterized to specific approved product promises.

## Evidence hierarchy and deduplication

**O [R24, R32, R36, R43, R46–R47].** Source classes include directly reopened live Meta ID; active search-result ad card; niche landing page without source ad; seller-brand identity; search snippet; analyst inference; excluded adjacent consumer-facing advertising. Historic specificity labels include `EXPLICIT_IN_AD`, `LANDING_PAGE_ONLY`, `BRAND_ONLY`, `INFERRED`, `ADJACENT_EXCLUDED`.

The research treats seller independence, ad-ID identity, ad variants, and offer-family identity separately. One brand's several variants are not several independent sellers. A seller claiming a result is not measured Meta campaign performance; a country search filter is not proof of actual delivery country.

**P:** every observation retains source locator, market/filter, observed time, source class, buyer-role quote/reference, offer type (AI TOOL, DIY/COURSE, DWY, DFY), verification tier, limitations and uploader/agent identity. Prefer stable IDs with source pointers, and exclude confidential raw evidence from public distributions.

## Observed exceptions and lessons

**Unreliable empty search [R24, R04].** The very broad `ai` query and a close alternate gave no cards despite functioning related queries. It was marked RETRY_REQUIRED rather than falsely EMPTY_VERIFIED; later a fresh legitimate search resolved it. **P:** use bounded retries, context-specific `SOURCE_UNAVAILABLE` and verified emptiness only after credible checks. Persist search variants and attempt count.

**Insufficient first-pass scope [R34].** Forty observed cards (including adjacent and repeats) were short of original 60–100 relevant cards and >=25 independent relevant suppliers; Canada evidence and direct-ID reopen depth were thin. The report declared its limitations. **P:** distinguish REPORT_DELIVERED from COVERAGE_COMPLETE and allow explicit, documented owner acceptance of limited evidence.

**Partial QA [R04, R29–R30].** An earlier QC attempt reviewed only the initial two assets of a later eight-asset set. Later source-match auditing revealed semantic buyer/problem drift that required copy and offer corrections. **P:** approval attaches to **exact artifact set, hashes, version and rubric**, invalidated by material changes. A format-valid file is not automatically semantically valid research.

**Cross-repository false absence [R01, R31, previous R10].** Research existed in another agent repository; a previous handoff misclassified it as missing. **P:** store full workspace locator, authority, revision, path, access error type and fallback. `not found in repo A` is not `not found anywhere`.

**Independent work and source disagreement [previous R06–R07].** Fred/Muse had distinct research outputs, independently assessed before peer comparison, with later source corrections. **P:** preserve independent submissions and explicit conflicting conclusions, not consensus-by-copying.

**Portfolio index behind individual run [R48–R49].** Run 10 `PROGRESS.md` shows explicit authorization, start and research checkpoints; the portfolio `RUN-INDEX.md` still lists it NOT STARTED. We did not modify its restricted records or assume it finished. **P:** per-run state/events win over derived portfolio summary if verified; mark aggregate `STALE` and recompute.

**Ambiguous external write [previous R11].** Meta staging suffered a timeout and duplicate objects, subsequently cleaned up. **P:** before retrying an external create, reconcile provider state with operation identity; do not assume timed-out action failed.

## Proposed non-implementation QC checklist for research templates

- **G0 Scope**. Explicit research-only authority, paths, buyer and truth source.
- **G1 Access**. Browser and storage actually tested, no invented VM or unavailable API.
- **G2 Query evidence**. Stable task, exact query/advertiser, date rule, market, attempt result.
- **G3 Eligibility**. Correct business buyer, directly relevant paid Meta offering, eligible source evidence.
- **G4 Identity**. Deduped advertisers, offer families and ad variants without inflating supplier count.
- **G5 Coverage**. Count remaining PENDING, BLOCKED, RETRY_REQUIRED and confidence shortfalls.
- **G6 Scoring**. Correct named rubric/version, components, rationale and evidence confidence.
- **G7 Independent QC**. Reviewer different from producer if required, exact artifact set/version, reasoned verdict.
- **G8 Synthesis**. Facts, seller claims, inference and recommendations separately; unfinished evidence visible.
- **G9 Next-stage handoff**. Fresh-session source pointers, unresolved issues, permissions and required approval.

**P failure policy:** remediation repeats the smallest affected work unit plus dependent gates. Unrelated authorized parallel branches continue. A QC result never grants Meta publishing or spending permission.
