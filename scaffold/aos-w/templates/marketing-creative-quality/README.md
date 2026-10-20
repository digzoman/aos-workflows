# Independent creative quality and revision

**Master template** `marketing-creative-quality` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Validate actual rendered artwork, spelling, semantic copy/offer match, safe zones and every supplied format; issue targeted fixes.

**Input parameters:** working_market, source_ref, creative_asset_manifest_ref, locked_copy_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `deterministic-export-check` (task): Verify exact file existence/hash/format/resolution and literal copy fields wherever editable. Outputs: artifacts/deterministic-export-check.md.
- `visual-semantic-inspection` (review): Independent reviewer views actual full-resolution variants for clipping, typography, realism, logo truth and CTA. Outputs: artifacts/visual-semantic-inspection.md.
- `revision-manifest` (task): List accepted variants and exact failed ones with correction, new hash and re-review requirement; no aggregate PASS if one required format failed. Outputs: artifacts/revision-manifest.md.

**Required QC:** image-pixel; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
