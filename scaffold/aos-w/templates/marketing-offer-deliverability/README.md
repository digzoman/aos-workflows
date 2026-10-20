# Verified deliverable offer and capabilities

**Master template** `marketing-offer-deliverability` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Have actual owner or authorized product authority verify specific product/service scope, price, deliverability, limits and support; blocks downstream claims until confirmed.

**Input parameters:** working_market, source_ref, offer_hypothesis_ref, actual_product_evidence_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `inventory-capabilities` (task): Check real product/tool/service features, staff capacity, fulfillment path, geography and exclusions against authoritative documents. Outputs: artifacts/inventory-capabilities.md.
- `verify-commercial-terms` (task): Cross-check live price, billing, support promises, refund and compliance constraints; unsupported claims remain blocked. Outputs: artifacts/verify-commercial-terms.md.
- `owner-confirm-deliverability` (approval): Obtain version-scoped human acceptance of exactly deliverable offer terms and limitations; a hypothetical marketing plan is not evidence. Outputs: artifacts/owner-confirm-deliverability.md.

**Required QC:** deliverability; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
