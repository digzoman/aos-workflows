# Competitor investigation, reusable child workflow (0.2.0)

A five-step, file-native workflow for dated competitor Meta advertising research. This **does not** automatically browse Meta or make production changes.

- `scope` captures buyer, focus, geography and sourcing boundaries.
- `search-ads` gathers dated observed advertiser/ad evidence or explicitly flags inaccessible sources.
- `extract-offers` deduplicates advertisers, offer families, tools and agency services.
- `verify-evidence` compares seller claims with traceable sources and preserved gaps.
- `review-investigation` requires **independent** `evidence-qc` against exact artifact versions.

Each node has stable ID, inputs, outputs, `quality.gates`, `contract.done_when` and `needs`. The template accepts `buyer`, `focus` and optional `market`; a new instance pins this file's bytes and exact template version. Candidate children from a portfolio plan remain PROPOSED until approved by an owner. Only real inspected evidence and version-accurate reviewer PASS allow a parent to synthesize. Output paths are run-root-relative under agent-files.

See `../../references/COMPOSITION.md` for how to resolve, start or retry a child using just files. This master is protected; create any custom version under `../../agent-files/custom-templates/`.
