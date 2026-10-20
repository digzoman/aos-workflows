# Advertising image and variant generation

**Master template** `marketing-image-generation` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Generate actual image assets only if an authorized image-capable host is available; store file hashes, generator/source and dimensions; never assume text in images is correct.

**Input parameters:** working_market, source_ref, approved_brief_ref, image_tool_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `verify-generator` (task): Check actual image tool availability, user scope, format and access. If unavailable, set BLOCKED without inventing output. Outputs: artifacts/verify-generator.md.
- `produce-candidates` (task): Produce traceable image candidates (e.g. portrait 1080x1350, square 1080x1080) using approved brief; distinguish generated draft from approved asset. Outputs: artifacts/produce-candidates.md.
- `record-image-integrity` (task): Inspect real file headers, RGB, pixel dimensions, exact copy text visibility and SHA256; reject blank/pseudo-logo output. Outputs: artifacts/record-image-integrity.md.
- `pixel-peer-review` (review): Independently inspect the actual pixels and per-placement crop/text hierarchy, not only image metadata. Outputs: artifacts/pixel-peer-review.md.

**Required QC:** image-pixel; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
