# Hypothetical offer positioning

**Master template** `marketing-offer-strategy` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Translate observed competitor offers into **proposed hypotheses**, not promises that the seller can actually fulfill.

**Input parameters:** working_market, source_ref, observed_competitor_matrix_ref, target_buyer. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `competitor-reference-map` (task): Tag each competitor observation OBSERVED_COMPETITOR with source/time; explicitly deny automatic equivalence to our product. Outputs: artifacts/competitor-reference-map.md.
- `hypothesize-our-offer` (task): Draft buyer outcome, pain, mechanism, differentiation, feasible pricing hypothesis, exclusions and commercial path. Outputs: artifacts/hypothesize-our-offer.md.
- `gap-and-assumption-audit` (review): Label every claim/feature/price as UNVERIFIED_HYPOTHESIS until a deliverability verification artifact is accepted. Outputs: artifacts/gap-and-assumption-audit.md.

**Required QC:** offer-claims; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
