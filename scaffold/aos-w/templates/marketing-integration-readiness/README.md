# Final cross-system prelaunch integration QA

**Master template** `marketing-integration-readiness` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Bring approved creative, Meta desired-versus-actual readback, CRM, landing and tracking findings into a single honest READY/BLOCKED status.

**Input parameters:** working_market, source_ref, creatives_ref, campaign_ref, crm_ref, landing_ref, tracking_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `collect-current-versions` (task): Pin exact outputs, PASS reviews, current hashes, owner approvals, external provider readbacks and unresolved sources. Outputs: artifacts/collect-current-versions.md.
- `verify-dependent-gates` (task): Check selected assets and placement previews, paused account status if staged, delivery routing, hosted page and conversion consent/dedup; NOT_RUN cannot become PASS. Outputs: artifacts/verify-dependent-gates.md.
- `integration-peer-review` (review): Independent reviewer identifies gaps by system and precise remediation; no blanket PASS, no permission to launch. Outputs: artifacts/integration-peer-review.md.

**Required QC:** integration-readiness; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
