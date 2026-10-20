# Marketing research planning

**Master template** `marketing-research-plan` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Define target buyers, vertical/subvertical boundaries, scope and independently reviewable research portfolio. Proposes child work only after approved scope.

**Input parameters:** working_market, source_ref, research_question, max_verticals. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `define-buyers` (task): Separate owner/buyer from end consumer; map verticals and service class, market, seasonality and inclusion/exclusion rules. Outputs: artifacts/define-buyers.md.
- `draft-plan` (task): Provide stable slug per vertical, ranked questions, coverage matrix, estimate access limitations, per-child evidence contract. Outputs: artifacts/draft-plan.md.
- `approve-scope` (approval): Obtain actual owner approval for research scope and any child creation; do not invent reviewer identity. Outputs: artifacts/approve-scope.md.

**Required QC:** plan-scope; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
