# Conversion and consent tracking verification

**Master template** `marketing-tracking-verification` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Create evidence-backed tracking plan distinguishing clicks, actual booked appointments, qualified leads and purchases, with consent and stable deduplication keys.

**Input parameters:** working_market, source_ref, funnel_contract_ref, actual_provider_events_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `milestone-taxonomy` (task): Define PageView consent, CTA/DM, appointment-confirmed Schedule, verified Good Lead, and actual paid Purchase; exclude tests/cancellations. Outputs: artifacts/milestone-taxonomy.md.
- `source-of-truth-map` (task): Map browser events, server CAPI, CRM confirmations, consent/revoke, event ID dedup, attribution windows and reliability of observed event counts. Outputs: artifacts/source-of-truth-map.md.
- `test-matrix` (task): Specify rejection/acceptance, browser/server duplicate prevention, booking versus click, chatbot negative controls; actual provider tests marked UNVERIFIED unless performed. Outputs: artifacts/test-matrix.md.
- `independent-tracking-review` (review): Peer verifies provider evidence and flags unknown dedup/attribution; no invented Schedule, qualified lead or Purchase. Outputs: artifacts/independent-tracking-review.md.

**Required QC:** conversion-truth; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
