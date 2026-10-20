# Prompt 04, reconstructed Ampgent creative workflow

Definitions. **OBSERVED** is directly recorded by R51–R81 in [SOURCE-INDEX-04.md](SOURCE-INDEX-04.md). **PROPOSED** is a design candidate for AOS-W PRD, not an implemented feature. No live Meta account or image asset was modified.

## Historical execution sequence

1. **Source selection, R51/R56/R57.** Research shortlist and real competitor evidence became a source card with buyer, source problem, hook, offer/funnel, creative format and claim limitations.
2. **Commercial offer/claim contract, R56/R74–R79.** Determine truthful product, price, mechanism, capabilities, restricted claims and the intended customer action. B9 iterated from AI media-buyer concept into the owner-controlled $47 AI Digital Marketer story with explicit **ad creatives AND ad campaigns**.
3. **Semantic audit before image, R57–R58/R64.** Preserve buyer, triggering problem, source framing, mechanism, offer, outcome class and commercial path. Tier A source anchors must survive except approved removals, at least two on-image; deviations require reasons and approval before images.
4. **Structured Meta copy, R59/R74/R79.** Produce exact on-image hook/support/CTA, primary text, Meta headline, description, native CTA and relevant DM opener. Keep each field independently versioned and reviewed.
5. **Visual art direction, R52/R58/R72/R76.** 4:5 portrait often 1080×1350, mobile-readable hook, faithful hero image and mechanism visualization, premium dark/gold/blue Ampgent visual system, about 5% safe margins, no fake product/proof UI.
6. **Image/video/static composition, R53/R58/R63/R65.** Earlier files favored editable SVG and PNG; later direct composite imagery integrated human hero, workflow panels, text and CTA. Photo and foreground overlay are separable repair targets. Maintain no-imagery/imagery A/B options where requested.
7. **Deterministic branding, R63/R69/R72–R73.** Image generator does **not** draw logo. Canonical logo is placed from approved SVG/PNG using compositing, with face/headline protection. Explicit owner exception may permit a logo-free version. The logo skill is an **optional** external helper, not a mandatory AOS-W Python dependency.
8. **Format/placement derivation, R54/R66–R69/R76/R80.** Verify 1080×1350 feed portrait; separately compose or safely adapt square, in examples 1080×1080 and 1350×1350, using approved blur-fill where safe. Do not assume square feed art automatically passes 9:16 Stories/Reels.
9. **Technical and semantic visual QA, R52–R62/R69.** Check actual PNG pixel dimensions, mode, file integrity, text, legibility at native/mobile scale, margins, correct logo, copy coherence, claims and source semantic fidelity.
10. **Independent review and revisions, R56/R61–R62.** Fred/Muse first produced independent sets, submitted matrices and checkpoints, then reciprocally reviewed without editing original peer work. Comparisons included ICP, source hook, image overlay/copy alignment, native-CTA coherence and truthfulness.
11. **Owner selection and approval, R51–R53/R77–R80.** Approval is tied to a specific copy and asset variant, with explicit exceptions and archival version lineage. A rejected third creative or old logo does not mean all others should be rebuilt.
12. **GitHub commit/read-back and separately authorized Meta handoff, R53/R63/R66/R80–R81.** Uploaded bytes and real image visual checks are distinct from local export. Staging must read back copy, source-to-provider image association and placement/CTA. Creative and staging quality do not grant spend/launch permission.

## Dependency graph, proposed

```text
Approved competitor source + owner brief
           |
      Offer truth gate
           |
    Semantic plan and copy
           |
      Semantic gate
        /        \
    Hero media   Deterministic text + canonical brand assets
        \        /
       Portrait composition
           |
   Independent no-imagery/imagery variants
           |
   Export/format and image/brand QA
           |
   Square / placement adaptations
           |
   Variant-specific visual and source QA
           |
     Independent reviewer
           |
        Owner signoff
           |
      Artifact version freeze
           |
     Repo persistence check
           |
  **separate** Meta staging and preview gates
           |
  **separate** activation authorization
```

## Inputs/outputs, gate-specific proposed contract

- **Source package**. Input verified source-ad/format/screenshot and scope. Output creative assignment referencing source revision. Gate provenance or explicit evidence limit.
- **Offer strategy**. Input product truth/ICP/price/destination/approved claims. Output versioned source-to-offer adaptation and prohibited claims. Gate factual/policy/human approval when needed.
- **Semantic plan**. Input source spine + allowed transformations. Output `semantic-audit.md` and Tier A/B anchor map. Gate meaning before visuals.
- **Copy package**. Input strategy/offer. Output exact `copy.md` with Meta field identities plus image overlays. Gate claims, spelling, CTA/destination and owner copy lock.
- **Image generation**. Input approved visual brief and skill references. Output foreground/background candidate(s) with evidence of tool used and failures. Gate no text/proof invention or logo generation.
- **Brand composite**. Input actual source artwork and canonical logo/version. Output final editable and raster variants. Gate correct official brand geometry and visual margin.
- **Variant export**. Input locked artwork and placement recipe. Output portrait/square/other approved placement versions and hashes. Gate file format, dimensions, color space, correct text/logo.
- **Quality review**. Input exact artifact hashes, reference/approved copy and QA rubric. Output reviewer verdict + issue list. Gate no stale approval after changed copy/image.
- **Approval and handoff**. Input reviewed candidate set, versions and permission policy. Output owner-selected version(s), archived old versions and checked Git/provider mappings. Gate creator approval is not launch authority.

## Bucket-specific evidence

**B1–B5.** Ten top-two creative packs were upgraded and independently tracked through semantic, visual, export, upload and post-upload gates; source and copy locks prevented unnecessary rewrite. B5 CallRail imagery needed format correction and separate square export. [R51–R55, R69–R70]

**B6–B7.** Independent Fred/Muse work for eSoftware/JNT TEK and Global Teams/ProCoders exposed source semantic drift and established before-image Tier A checks and reciprocal critique. B6.1 wrong-logo/subline imagery was corrected without redoing source research. B6.3.1 and 6.3.2 involved Ontario eligibility wording that could not be treated as generic sales claims. [R56–R64, R67–R68]

**B8.** The Doers Way VA created three options with locked copy and mobile QA. Subsequent square-format and provider creative associations required additional attention; each variant had its own Meta mapping and approval status. [R65–R66]

**B9.** Offer/wording and artwork underwent V2 and V4 changes. A logo-free Oct 17 owner selection was documented and later superseded by Oct 18 branded, separately approved feed portrait/square assets, staged/read-back in Meta. Placement previews, 9:16 safe area and live messaging acceptance were tracked separately. [R74–R81]

## Central proposed principle

Creative state must be **per-artifact and per-gate**, not a single PASS Boolean. Independent branches can progress when their particular inputs are valid. Failed PNG dimensions should trigger a format-only correction, not redo research. Changed price/hook invalidates dependent text/image and provider staging verification, but not unrelated source records. A successful Meta write/read-back is not visual placement QA or actual delivery.
