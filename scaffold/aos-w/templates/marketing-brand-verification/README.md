# Canonical brand and logo verification

**Master template** `marketing-brand-verification` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Use genuine approved logo provenance and pixel-level appearance checks; never trust a generator to recreate a brand mark accurately.

**Input parameters:** working_market, source_ref, artwork_ref, canonical_brand_asset_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `pin-brand-source` (task): Record approved logo/hash/version and any explicitly owner-approved logo-free exception. Outputs: artifacts/pin-brand-source.md.
- `check-application` (task): Inspect actual pixels of all variants for size, 5% safe regions, distortion, false logos, contrast and top-right placement where specified. Outputs: artifacts/check-application.md.
- `brand-independent-review` (review): Separate reviewer verifies canonical asset and every intended placement, issues precise correction if not PASS. Outputs: artifacts/brand-independent-review.md.

**Required QC:** brand-integrity; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
