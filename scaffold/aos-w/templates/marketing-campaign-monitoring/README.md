# Read-only campaign performance monitoring

**Master template** `marketing-campaign-monitoring` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Summarize dated real provider delivery and downstream CRM outcomes, not merely API-accepted writes, with observed and estimated metrics clearly labeled.

**Input parameters:** working_market, source_ref, reporting_period, provider_readback_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `observe-status` (task): Record actual configured/effective/review/delivery state separately; distinguish held/paused and unverified status. Outputs: artifacts/observe-status.md.
- `measure-results` (task): Compute CTR/CPC from actual impressions/clicks/spend; when no clicks use explicitly labeled estimate or N/A; never invent conversations. Outputs: artifacts/measure-results.md.
- `crm-attribution` (task): Compare confirmed booking/Good Lead status using actual CRM and consent evidence, not Meta events alone. Outputs: artifacts/crm-attribution.md.
- `report-independent-review` (review): Check timestamps, denominators, estimated labels, rate-limit/attribution caveats and safe recommended watchlist. Outputs: artifacts/report-independent-review.md.

**Required QC:** monitoring-evidence; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
