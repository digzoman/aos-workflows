# Prompt 04, evidence-backed correction cases and minimal retry policy

**OBSERVED** refers to historical Max records in [SOURCE-INDEX-04.md](SOURCE-INDEX-04.md). **PROPOSED** is an unimplemented AOS-W design response.

1. **Semantic drift behind a valid image.** Earlier source audit found changed buyer/problem framing despite format-valid imagery [R29–R30/R57]. **PROPOSED:** send to strategy/copy remediation before generating again, invalidate semantic and downstream copy/image approvals while keeping verified source research.
2. **Wrong or generated pseudo-logo.** B6.1 eSoftware imagery had a logo with an unwanted subline; original archived, official no-subline version recomposited and GitHub image re-inspected [R63/R72–R73]. **PROPOSED:** retry brand composite, export and visual QA only, not hero generation or research.
3. **Mislabeled dimensions.** B5 CallRail manual imagery measured 1198×1313 instead of the expected 1080×1350 [R69]. Corrected portrait and square were separately verified. **PROPOSED:** use actual file metadata and repair just transformation plus related QA, never trust filenames or stale notes.
4. **Square crop loses content.** Blurred-background fill preserved entire portrait for 1:1 while other briefs called for independent square layout [R66/R69/R73/R76]. **PROPOSED:** explicit variant recipe and format-specific safety/legibility review; 9:16 remains separate if enabled.
5. **Generated image edit unavailable in a specific harness.** A B1 SalesAPE upgrade stalled when the GitHub image was not available as an editable image input for ImageGen; later direct-composite generation resolved the issue [R53]. **PROPOSED:** preserve checkpoint and offer an authorized regenerate/composite fallback, don't mark the edit successful.
6. **Metadata upload versus actual pixels.** V3 and B8/B9 records verified file/payload status while some placement crops and live messaging remained unverified [R54/R66/R80–R81]. **PROPOSED:** independent native and mobile viewing, post-upload check, and later provider placement QA.
7. **Copy-image disagreement.** Fred's critique specifically called for checking embedded headline versus `copy.md` [R61]. **PROPOSED:** compare exact deterministic source strings where possible; raster text needs actual visual/OCR-like review without pretending file bytes alone prove readability.
8. **Eligibility/claim change.** Ontario funding creatives required updated figure and clarification that advertising audience language was not the official eligibility threshold [R67–R68]. **PROPOSED:** invalidate related factual claims, copy, embedded artwork and staging fields, seek human authorization for high-stakes claim changes.
9. **Independent A/B variants.** B8 produced no-imagery and imagery V1/V2 with separate Meta image associations [R65–R66]. **PROPOSED:** a sibling variant failure does not automatically invalidate approved siblings unless parent policy says all variants required.
10. **Overwritten/changed owner selection.** B9 Oct 17 logo-free instruction was superseded by subsequent branded approvals, and both histories persist [R77–R81]. **PROPOSED:** append-only approval/supersession events with exact hashes, explicit exception scope, no assumption latest-edited file is approved.
11. **Creative source or destination missing.** V3 had incomplete reference packs and destination assumptions; work was held before unsafe staging/launch [R54–R55]. **PROPOSED:** missing source -> evidence gate, missing landing destination -> stage/launch gate, not a generic global workflow failure.
12. **New quality standard does not retroactively validate old work.** Ten older B1–B5 creatives were upgraded against new B6/B7 quality bar, with multiple gates and preserved prior versions [R52–R53]. **PROPOSED:** version the QA rubric, re-review affected archived assets rather than silently marking them compliant.

## Minimal correction decision tree, proposed

- `UNSUPPORTED_CLAIM` or `SEMANTIC_DRIFT` -> offer/copy/semantic gate, then affected images and approvals.
- `SPELLING`, `TEXT_MISMATCH` -> typography/overlay composition and affected image variants, semantic check if meaning changed.
- `MISSING_LOGO`, `WRONG_LOGO` -> deterministic logo composite, output variants, visual/brand/repository QA.
- `WRONG_DIMENSION`, `COLOR_MODE`, `CORRUPT_FILE` -> transform/export and pixel QA, no source research replay.
- `UNSAFE_CROP`, `POOR_MOBILE_LEGIBILITY` -> format-specific layout and review, leave sibling layouts alone.
- `ASSET_NOT_EDITABLE`, `CONNECTOR_UNAVAILABLE` -> checkpoint, retry another permitted method or request real source access.
- `UPLOAD_HASH_MISMATCH` -> retry upload/read-back and revalidate actual remote bytes.
- `PLACEMENT_PREVIEW_UNKNOWN` -> downstream provider preview gate, not local-artifact failure.
- `OWNER_REJECTED` -> revise only explicitly rejected branch or stop; don't auto-regenerate locked approved work.

**PROPOSED recovery rule.** Record failed artifact hash, gate, reviewer and attempted repair. Preserve prior source and creative versions, redo only the transitive downstream checks that depend on the changed content, request owner approval for material claims/offer deviations, and never infer launch authority from a creative QA PASS.
