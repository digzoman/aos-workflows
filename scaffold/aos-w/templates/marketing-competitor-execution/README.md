# Competitor research execution

**Master template** `marketing-competitor-execution` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Investigate actual advertisers and buyer-specific offers; every claim requires dated source evidence, not invented ad status or targeting.

**Input parameters:** working_market, source_ref, vertical, buyer, queue_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `verify-access` (task): Record actual access, research mode, date, market, query queue, retry budget; unavailable is not a verified zero. Outputs: artifacts/verify-access.md.
- `sweep-queue` (task): Inspect bounded keyword/search advertiser queue; preserve URL, source date, active/inactive observation and source reliability. Outputs: artifacts/sweep-queue.md.
- `seller-offer-families` (task): Dedupe seller/advertiser identity, variations and service-versus-software offer family; preserve conflicts. Outputs: artifacts/seller-offer-families.md.
- `coverage-ledger` (task): Account for every authorized keyword and advertiser entry, include unavailable/verified empty/retry needed distinctly. Outputs: artifacts/coverage-ledger.md.
- `source-evidence-review` (review): Have separate reviewer verify exact observation artifacts, evidence completeness and all outstanding gaps. Outputs: artifacts/source-evidence-review.md.

**Required QC:** evidence-integrity; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
