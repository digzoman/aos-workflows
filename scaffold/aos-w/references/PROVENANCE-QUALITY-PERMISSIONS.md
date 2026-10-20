# Prompt 12 — Provenance, task claims, QC gates and permissions

This is the **normative file-only/manual protocol**, usable by a capable agent without any helper scripts. The optional `tools/governance/` adapter in the development repository verifies some of the same rules locally; it is **not an authentication system**.

## 1. Identify every actor

Record four nonempty fields `[Agent | Platform | Role | Instance]` in task claims, task transitions, reviews, approval decisions, significant handoffs and, where Git is enabled, commit trailers (`Agent-Provenance: [Agent | Platform | Role | Instance]`). Use a different instance for a fresh session. Changing a role label alone does **not** establish independence or prove identity. Host-side authentication and independent reviewer isolation remain optional requirements for stronger trust.

## 2. Claim a bounded task

Inspect the pinned effective graph revision and latest validated state/checkpoint. Only claim a READY node with all required prerequisites and permissions. Record `claims/<id>.json` with task/run, the four-field actor, acquired time, expiry hint, current status and progress, and the claim's **mode**. In file-only mode it is `advisory`: it is **NOT** an exclusive lock. Do not allow two writers on one run by convention. A stale claim cannot be stolen merely because the timestamp passed; verify takeover using a tested coordinator (not yet present), or have the existing owner explicitly release it. Record claim and release decisions as append-only events; never silently edit history. Never claim a step simply because its definition mentions you as a preferred agent.

## 3. Define QC policy separately from action authority

The effective policy is inherited from protected master to custom template to instance to permitted step overrides; protected parent ceilings and required human gates cannot be weakened by a child. Every step has explicit input/output contract and `quality.gates` references. A workflow can default gates through `policy.default_gates`. Supported gate kinds:

- **deterministic**: verifiable local checks (SHA-256 match, file type/schema, dimensions when a tool exists). Record exactly what tool actually checked; do not mark semantic claims verified by a hash.
- **ai_independent**: a separate agent/instance critiques actual full artifact set under versioned rubric. A role renaming on the *same* agent/platform/instance is not independence.
- **human**: a recorded human quality decision distinct from the producer, with an authenticated host required to **enforce** the role.
- **self_review**: allowed only if the named gate explicitly permits it, generally for low-risk operations; it must never be mislabeled independent.

Each verdict binds the **entire required artifact set**, revisions and exact byte hashes, the graph revision, task attempt, rubric revision, reviewer, date, findings and verdict. Adding a new required image or altering source copy invalidates an old gate's applicability. A partial PASS is not an overall PASS. A waiver may be recorded only for an expressly `waivable: true` nonhuman gate by a separately declared owner, with reason, scope, optional expiry; preserve it as `WAIVED_BY_OWNER` and an `ACCEPTED_WITH_WAIVER` aggregate—not ordinary evidence PASS.

## 4. Fail, correct and resubmit

On `REVISE`, `INSUFFICIENT_EVIDENCE` or other failing verdict, create a persistent `reviews/<id>.json` with actionable findings, then `reviews/remediation-<id>.json` specifying correction work. Append review and remediation events, mark the task `NEEDS_REWORK`, and do **not** release dependent nodes. Unrelated READY sibling branches may progress within any configured single-agent/parallel limit. A new attempt must have its own attempt ID; do not overwrite the old review or evidence. When corrected, submit the **new** complete artifact versions for every currently required gate. Exhausted retry or explicit owner intervention remains BLOCKED/FAILED; no automatic timer in file-only mode.

## 5. Authorize **actions** separately

Policy can allow routine read/research/local drafting/review without repeat human intervention, within its ceiling. Consequential actions—sending a message, live ad activation, spending, production deployment, CRM mutation and conversion-event emission—require a **distinct**, in-scope action grant. Each record includes issuer, task/run, graph revision, specific action class, enumerated resources and exclusions, versioned artifacts where relevant, limits including budget, issued/expiry times and conditions. No wildcard “all” grants, no generic QC PASS as a substitute. A revocation or graph revision makes an old approval unusable for future effects. Keep old approvals and append separate revocation/supersession records. Check authentic owner permissions **again at the actual provider connector/host** before external mutation; a JSON file cannot authorize real external side effects by itself.

## 6. Handoff and resume

Produce a human-readable `handoff.md` and preferably a structured `handoffs/<id>.json`: current pinned graph revision, last verified event sequence, completed/active/eligible/blocked tasks, exact actor claims, review results/pending QC, pending provider readbacks, unfinished correction, current valid scoped approvals, and a proposed **next authorized** action. A fresh agent reads pinned graph, validated event history and provider state before acting. A handoff is a view, not the source of truth when it disagrees with actual events or provider readback.

## 7. Trust / enforcement levels

**FILE-ONLY COOPERATIVE:** one writer, advisory claims, owner/reviewer self-attestations, manual SHA checks if available. An agent should refuse unauthorized work by following this procedure, but other filesystem writers may bypass it.

**OPTIONAL LOCAL CHECKER:** can verify record shape, hashes, gate coverage, date/graph/resource scope, and append state events; it still cannot prove a user identity or stop unrelated host programs. `context_checked` flags in the optional state helper represent **caller-verifiable process checks**, not cryptographic authorizations.

**REAL ENFORCEMENT (NOT BUILT):** authenticated human approvals, isolated reviewer roles, atomic/shared claims, capability-limited provider connectors, signed scope and server readback. These need separate adapters/tests and cannot be inferred from passing local tests.

No installed Python, Git, MCP server, database, scheduler or cloud service is required to read or follow these conventions manually. All normal workflow changes remain under `agent-files/`.
