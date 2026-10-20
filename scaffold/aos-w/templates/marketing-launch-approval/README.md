# Human authorization for live ad publication

**Master template** `marketing-launch-approval` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Prepare exact launch manifest and request real, separately authenticated HUMAN approval. This module **does not activate ads**.

**Input parameters:** working_market, source_ref, integration_qc_ref, meta_snapshot_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `freeze-launch-manifest` (task): Define exact campaign/adset/ad IDs, creative revisions/hashes, budgets and max exposure, geography/holds, permission scope and expiry. Outputs: artifacts/freeze-launch-manifest.md.
- `check-current-provider-state` (task): Read actual provider snapshot if authorized; if absent or inconsistent STOP and request reconciliation. Outputs: artifacts/check-current-provider-state.md.
- `request-owner-launch-permit` (approval): Owner must explicitly approve exact live activation and budget/exclusions with expiry; passing creative QC or paused staging is NOT authorization. Outputs: artifacts/request-owner-launch-permit.md.
- `prepare-activation-handoff` (task): Write a NON-EXECUTING launch handoff listing permitted target IDs, dependency readback, provider operation keys and independent verification sequence; no activation. Outputs: artifacts/prepare-activation-handoff.md.

**Required QC:** launch-permit; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
