# Campaign optimization proposals and authorized changes

**Master template** `marketing-optimization` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Propose bounded changes from verified insights; any live budget, targeting, creative or status edits require a new, exact-scoped authenticated human permit.

**Input parameters:** working_market, source_ref, verified_metrics_ref, current_provider_state_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `diagnose-opportunity` (task): Separate actual performance anomalies and tracking limitations from hypotheses; rank fixes with evidence. Outputs: artifacts/diagnose-opportunity.md.
- `draft-diff` (task): Specify exact before/after campaign/adset/ad/asset changes, objective, budget exposure, rollback/compensation, stable operation IDs. Outputs: artifacts/draft-diff.md.
- `owner-change-permit` (approval): Request exact human approval for each consequential provider write or spend change; no silent auto-optimization. Outputs: artifacts/owner-change-permit.md.
- `reconciliation-handoff` (task): Document approved change and required post-write provider readback; without authorized connector, STOP before any action. Outputs: artifacts/reconciliation-handoff.md.

**Required QC:** optimization-authorization; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
