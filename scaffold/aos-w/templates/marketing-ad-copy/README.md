# Advertising copy and messaging package

**Master template** `marketing-ad-copy` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Produce exact on-image ad text, primary Meta text, headline, description, CTA and optional messaging questions from the **approved deliverable offer** only.

**Input parameters:** working_market, source_ref, verified_offer_ref, buyer. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `semantic-spine` (task): Pin buyer, problem, hook, mechanism, promised outcome, deliverable features, offer and next step to owner-approved source. Outputs: artifacts/semantic-spine.md.
- `draft-fields` (task): Generate separate image-overlay, primary, headline, description, CTA, full selectable question and blank reply-response where relevant. Outputs: artifacts/draft-fields.md.
- `claims-copy-qa` (review): Peer check each literal field, punctuation, product truth and semantic alignment; feedback targets only failed copy fields. Outputs: artifacts/claims-copy-qa.md.

**Required QC:** copy-semantic; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
