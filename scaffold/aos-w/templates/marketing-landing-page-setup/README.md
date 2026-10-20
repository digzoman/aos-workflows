# Landing page and website preparation

**Master template** `marketing-landing-page-setup` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Prepare offer pages, CTAs, UTMs, consent and DEV smoke tests. Drafts and repository commits never prove production deployment.

**Input parameters:** working_market, source_ref, verified_offer_ref, site_source_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `page-contract` (task): Plan truthful site claim/destination, navigation, responsive views, privacy/cookie consent and UTMs. Outputs: artifacts/page-contract.md.
- `dev-preview-plan` (task): Draft DEV-only content and rollback map; log whether hosted preview actually exists or remains NOT_TESTED. Outputs: artifacts/dev-preview-plan.md.
- `page-peer-review` (review): Check page/CTA/accessibility/consent and actual preview as available; do not claim PROD without separate owner grant and readback. Outputs: artifacts/page-peer-review.md.

**Required QC:** landing-readiness; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
