# Evidence consolidation and source lineage

**Master template** `marketing-evidence-consolidation` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Merge only accepted versioned research findings across runs; preserve contradictory claims and provenance.

**Input parameters:** working_market, source_ref, accepted_runs_ref. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `verify-child-acceptance` (task): Read each child latest artifact set and independent review, reject stale PASS or missing required runs. Outputs: artifacts/verify-child-acceptance.md.
- `merge-sellers` (task): Normalize advertiser identity, offer-family, observed offer, dates, links, market and duplicate identities. Outputs: artifacts/merge-sellers.md.
- `reconcile-contradictions` (task): Preserve evidence disagreement and source limits instead of silently choosing favorable results. Outputs: artifacts/reconcile-contradictions.md.
- `audit-consolidation` (review): Verify all required child references, confidence and source lineage with separate reviewer. Outputs: artifacts/audit-consolidation.md.

**Required QC:** consolidation; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
