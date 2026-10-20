# Advertising visual strategy and creative brief

**Master template** `marketing-creative-brief` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Create a source-faithful truthful design brief for portrait/square and placement constraints from locked ad copy.

**Input parameters:** working_market, source_ref, copy_revision_ref, brand_guidelines_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `source-brief` (task): Map strategy, audience, visual hook and reference evidence, avoiding imitation or invented competitor claims. Outputs: artifacts/source-brief.md.
- `layout-plan` (task): Specify hierarchy, exact frozen text blocks, logo/CTA safe zone (default 5%), imagery/no-image alternatives, placement-specific crops. Outputs: artifacts/layout-plan.md.
- `brief-peer-review` (review): Verify semantic alignment, image guidance, margins and feasibility before generating any image. Outputs: artifacts/brief-peer-review.md.

**Required QC:** brief-visual; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
