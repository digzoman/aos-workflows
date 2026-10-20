# Meta campaign, adset and ad preparation

**Master template** `marketing-meta-campaign-preparation` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Draft desired Meta campaign/adset/ad graph, targeting, budgets, holds, creative hashes and CTA; no default provider writes or activation.

**Input parameters:** working_market, source_ref, verified_offer_ref, approved_creatives_ref, account_readback_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `baseline-readback` (task): Record whether real Meta provider access and current account budget/object inventories were actually read; UNKNOWN if unavailable. Outputs: artifacts/baseline-readback.md.
- `campaign-structure` (task): Document exact parent/adset/ad desired state, objective, budget/currency, location/age and exclusions, sibling HOLDs, placement media IDs. Outputs: artifacts/campaign-structure.md.
- `paused-staging-plan` (task): Produce idempotent proposed operations, provider-object identity reconciliation and PENDING provider readback plan; do not claim PAUSED exists. Outputs: artifacts/paused-staging-plan.md.
- `owner-scope-approval` (approval): Human reviews exact spend exposure, location and identities for a possible future PAUSED staging; this is NOT activation approval. Outputs: artifacts/owner-scope-approval.md.

**Required QC:** campaign-plan; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
