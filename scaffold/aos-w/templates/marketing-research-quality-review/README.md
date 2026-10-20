# Independent research quality and remediation

**Master template** `marketing-research-quality-review` / `0.7.0`, manual trigger, non-repeating by default. This is a **definition**, not an executed workflow or evidence of actual campaign state.

Evaluate exact current submitted research evidence with independent reviewer, scoped correction and resubmission; do not erase failed attempts.

**Input parameters:** working_market, source_ref, submitted_run_ref, rubric_version. All source references must be resolved to real versioned evidence before a relevant PASS. No real customer data or secrets are bundled.

**Run process:**

- `freeze-submission` (task): Record complete submitted artifact IDs/hashes/graph revision and producer identity; reject missing evidence. Outputs: artifacts/freeze-submission.md.
- `peer-audit` (review): Independent reviewer inspects real primary sources, search breadth, dedupe and contradictions; decide PASS/REVISE/BLOCKED/INSUFFICIENT_EVIDENCE. Outputs: artifacts/peer-audit.md.
- `remediation-route` (task): For REVISE create exact failed-artifact fixes, bounded new attempt and invalidate affected downstream QC; do not approve failed content. Outputs: artifacts/remediation-route.md.

**Required QC:** qc-independent; see `template.yaml` for exact gate types, reviewer independence and permissions. **Quality PASS does not grant external-action permission.**

This module can be instantiated independently. A compound workflow pins this template's source digest, binds parameters and validates its output contract; every external action requires separate actual host/provider authority.
