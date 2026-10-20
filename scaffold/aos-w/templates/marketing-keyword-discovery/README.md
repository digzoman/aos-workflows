# Keyword and advertiser search discovery

**Master template** `marketing-keyword-discovery` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Prepare prioritized Meta Ads Library search terms and advertiser candidates, deduplicated and coverage-aware, without claiming search results.

**Input parameters:** working_market, source_ref, vertical, buyer. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `seed-families` (task): List buyer-language, direct problem, trade niches, category synonyms, offer mechanism, competitor brand and local variants with stable keyword IDs. Outputs: artifacts/seed-families.md.
- `normalize-queue` (task): Deduplicate terms, rank by relevance, add country/time/search source and explicit exclusions and retry limits. Outputs: artifacts/normalize-queue.md.
- `audit-coverage` (review): Independently examine important omitted synonyms, discovery breadth, bias and source availability; record deferred queue. Outputs: artifacts/audit-coverage.md.

**Required QC:** keyword-coverage; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
