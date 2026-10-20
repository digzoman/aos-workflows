# Prompt 04, creative QA and approval model

This is a **proposed model**, grounded in R51–R81, for Prompt 07 PRD evaluation. It is not a working AOS-W workflow engine. Each gate references exact copy/artwork/rubric revision and evidence artifacts.

## Gate classes and appropriate verification methods

| Gate | What must be checked | Method | Authority / invalidation |
| --- | --- | --- | --- |
| G-C0 source | Source identity, observed creative format, offer-family source and evidence reliability | Document/source verification with human or AI if uncertain | New source or material correction reopens source/spine |
| G-C1 product/claims | What Ampgent can actually deliver, price, product limits, unsupported promises and sector rules | Human/qualified AI semantic review and factual references | Material promise/price/eligibility requires human review |
| G-C2 semantic spine | Same buyer, problem, hook, mechanism, offer/next step, outcome and commercial path, Tier A/B anchors | Semantic AI + independent reviewer on cited source | Must PASS **before** final visual generation, invalidate on strategic drift |
| G-C3 copy | Exact on-image text, primary caption, Meta headline, description, CTA, destination, questions | Deterministic field presence and literal comparison, then semantic/claims review | Lock and version exact content, editing invalidates impacted images |
| G-C4 visual brief | Source-connected hero, no fake metrics, appropriate hierarchy, projected text and safe margins | AI/human design judgment | Approved brief used to generate exact candidate versions |
| G-C5 logo | Canonical logo file, version (with or without subline), geometry, placement and margin | Deterministic provenance plus **pixel inspection** | No generated pseudo-logos, except explicit owner-approved logo-free artifact |
| G-C6 export | Actual dimensions, image format, RGB, image integrity, source/editable file and file hash | Deterministic file/image validators when available | Any failed format remains failed even if prior version passed |
| G-C7 visual | Typography/spelling/readability, photos/subjects, overlay/copy consistency, clipping, mobile view, 5% safe region | Render actual pixels and independent AI/human visual review | Re-check every changed format/variant, even after deterministic PASS |
| G-C8 variation | Each portrait/square/Story option looks correct for the **intended placement** | Actual per-format viewing; Meta preview when staging | A 1:1 file does not automatically pass 9:16 preview |
| G-C9 independent peer | Review actual source adaptation, truthful claims, CTA and visual/spelling accuracy, with reviewer's identity | Independent agent, preserving producer work | QC verdict tied to source/copy/image hashes and rubric version |
| G-C10 owner selection | Which version, logo exception, alternatives and scope are approved | Explicit human approval by default | Owner selection is variant-specific and not spending permission |
| G-C11 repository artifact | Committed GitHub payload exactly matches approved source, and post-upload display is intact | Blob/hash/read-back plus rendered remote image inspection | Requires recheck after upload or replacement |
| G-C12 Meta stage | Ad creative copy, media hash, native CTA, message questions, status, and intended placement mapping | Provider API read-back plus previews where accessible | Even PASS here does not mean campaign activation authorized |
| G-C13 publication | External action, budget, owner permissions and launch disposition | Separate authorization policy, provider read-back | Never infer from G-C9/C10 creative approval |

**Observed basis.** Historical V3 quality reports separately checked SVG/PNG and visual spot-checks, while Meta launch/destination were still open [R54]. Upgrade progress had separate semantic/visual/export/upload/post-upload columns [R53]. B9 Meta provider hashes/fields passed, but placement, Stories/Reels and live DM tests remained pending [R80–R81]. Independent critique addressed misleading source replacements and mismatched copy [R61–R62].

## Deterministic versus judgment-based checks

**Best deterministic candidates**, actual pixel dimensions and ratios, PNG/JPEG encoding readability, RGB and alpha where specified, existence of files, SHA/hash integrity, filename/expected asset mapping, exact string comparison in editable SVG or structured copy, required keys/paths and state transition prerequisites.

**AI visual or semantic reviewer candidates**, actual logo appearance, spelling baked into generated pixels, headline visibility, color contrast, hierarchy, realism, no awkward faces, semantic spine fidelity, clarity of offer and mismatch between image and caption. Generic image model output often contains text that cannot be reliably validated by only checking PNG metadata.

**Human review candidates**, substantial commercial claim changes, source-to-offer transformation beyond permitted drift, unproven capabilities/industry funding claims, choosing one of several credible designs, exceptions to brand rules, final consequential publishing/budget authorization.

### Approval semantics, proposed

- Review contains producer identity, reviewer identity, artifact hash(es), rubric version, method, decision, date/time and issue list.
- A `PASS` must name **which** gate, scope and exact variants it covers.
- `NEEDS_REVISION`, `BLOCKED`, `WAIVED_BY_OWNER` and `PENDING_VERIFICATION` must remain separate from `PASS`.
- A specific creative may be approved for **internal testing**, **GitHub artifact**, **Meta PAUSED staging**, or **external publication** separately.
- Post-approval material changes invalidate only dependent checks. The prior decision remains in history as valid for its old version.
- Different reviewer independence rules can be configured by template and human override. An agent's self-review alone cannot silently replace independent QC when specified.
- Source claims and eligibility require external/source confirmation, not only a confident model opinion.

## Acceptance demonstration for V1

Use a staged test where one approved B8-like portrait stays unchanged while square fails a safe-zone test. Redo only square layout and its export/visual/post-upload gates, confirm portrait/source/copy remain PASS. Separately introduce semantic misalignment and show it blocks image work until corrected. For grant/price edits require explicit owner approval and invalidate both copy and images containing changed values. These are **proposed tests**, not yet run.
