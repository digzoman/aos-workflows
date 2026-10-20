# CRM and messaging preparation

**Master template** `marketing-crm-preparation` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Prepare versioned conversational intent/routing, offer knowledge, appointment status and negative control tests without touching actual customer contacts.

**Input parameters:** working_market, source_ref, verified_offer_ref, crm_provider_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `crm-journey-map` (task): Specify messaging question (full question), blank Meta response, offer fingerprint, bot knowledge/route and contact permissions. Outputs: artifacts/crm-journey-map.md.
- `prepare-regression-matrix` (task): Separate actual Facebook Messenger and Instagram Direct tests from stored configuration; include unrelated-offer negative control. Outputs: artifacts/prepare-regression-matrix.md.
- `qa-crm-plan` (review): Peer verifies truth of route, consent/privacy boundaries and channel test plan; no live customer DMs. Outputs: artifacts/qa-crm-plan.md.

**Required QC:** crm-routing; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
