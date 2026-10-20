# Marketing opportunity and confidence scoring

**Master template** `marketing-opportunity-scoring` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Score buyers and offer niches using evidence-based transparent axis rubrics, uncertainty and cost-to-test caveats.

**Input parameters:** working_market, source_ref, scorecard_ref, scoring_rubric. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `select-rubric` (task): Pin seven-axis or custom rubric and weights, missing-data policy and distinction between opportunity and source-ad persistence. Outputs: artifacts/select-rubric.md.
- `score-verticals` (task): Score buyer pain, value, competition, ability to evidence results, DIY/tool fit, conversion and audience reach using cited rows. Outputs: artifacts/score-verticals.md.
- `confidence-and-cost` (task): Separate evidence confidence and research gaps from weighted opportunity scores; estimate incremental creative and adset cost only as assumptions. Outputs: artifacts/confidence-and-cost.md.
- `independent-score-review` (review): Verify arithmetic, source specificity and unexplained rankings before proposing test priority. Outputs: artifacts/independent-score-review.md.

**Required QC:** scoring; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
