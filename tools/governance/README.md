# AOS-W 0.4.0 optional governance adapter

**Capabilities:** four-part agent identity (`[Agent | Platform | Role | Instance]`), append-audited advisory task claims, claimant-aware task starting, configurable inherited per-workflow and per-step quality gates, deterministic artifact digest verification, declared independent AI and human reviews, permitted self-review, explicit (distinct) human waiver, remediation and retry, scoped owner-declared action authorization with expiry/revocation and graph-version binding, and durable handoffs.

**Limitations:** No user authentication, signature validation, OS sandbox, hard role isolation or distributed lock is provided. A file containing `role: owner`, a GitHub identity, a passing AI review, or approval JSON **is not proof** of the owner's identity or consent. The local helper enforces checks only for operations routed through it; another process with filesystem access could bypass it. A real external action MUST be authorized again at its tool/provider boundary by an authenticated host. No Meta, HighLevel, website, messaging, CAPI, background scheduler, or other provider call is implemented here.

The core downloaded `scaffold/aos-w/` remains **purely file-and-agent-operable**, without mandatory Python, Git, cloud storage, database or MCP. The optional implementation uses Python stdlib plus PyYAML when reading the current pinned YAML definition (already optional for the Prompt 11 helper). It only writes inside `agent-files/instances/<id>/runs/<id>/`.

## Manual and optional workflows

A manual agent reads `scaffold/aos-w/references/PROVENANCE-QUALITY-PERMISSIONS.md` and the pinned instance graph. To use the optional helper:

```sh
python tools/governance/cli.py /path/to/aos-w/agent-files/instances/example/runs/run-001 inspect
python tools/governance/cli.py /path/to/.../runs/run-001 grant --actor path/to/owner-actor.json --payload path/to/approval-request.json
python tools/governance/cli.py /path/to/.../runs/run-001 claim --actor path/to/worker.json --payload path/to/claim-request.json
python tools/governance/cli.py /path/to/.../runs/run-001 begin --actor path/to/worker.json --payload '{"task_id":"draft"}'
python tools/governance/cli.py /path/to/.../runs/run-001 submit-review --actor path/to/worker.json --payload '{"task_id":"draft"}'
python tools/governance/cli.py /path/to/.../runs/run-001 review --actor path/to/reviewer.json --payload path/to/review-request.json
```

The helper supports `release`, `revoke`, `authorize`, `resubmit`, `finalize`, `handoff` and **intent-only** `op-intent`. No CLI operation actually contacts providers. `grant` checks an owner *declaration*, not an external identity provider.

## File contracts

`claims/<claim-id>.json`: owner four-field identity, acquired/expiry times, current progress, advisory mode and release record. Stale lease never automatically transfers ownership; Git/CAS enforcement is Prompt 13.

`approvals/<approval-id>.json`: issuer, scope, actions, resource identities/exclusions, task and graph revision, optional artifact hashes, limits, issued/expiry dates. Revocation creates a **new** record with `supersedes_id`, preserving prior approval history.

`reviews/<review-id>.json`: producer and reviewer identities, gate type/rubric, exact artifact IDs/hash/revisions, actual attempt and graph revision, PASS/REVISE/INSUFFICIENT/BLOCKED or distinct `WAIVED_BY_OWNER`. A failed review creates `reviews/remediation-<review-id>.json` and sends task to `NEEDS_REWORK`; resubmission must describe correction and start a new attempt. An owner waiver is permitted only when the gate expressly specifies `waivable: true`; the aggregate reports `ACCEPTED_WITH_WAIVER`, never evidence PASS.

`handoffs/governance-handoff-*.json`: typed owner, current graph and journal prefix, completed/active/ready work, claims, pending gates and provider uncertainty, and explicit next action. Generated `handoff.md` remains a convenience view; events and current provider state are separate authorities.

All material changes are appended as SHA-256-chained event types `claim_recorded`, `claim_released`, `permission_granted`, `permission_revoked`, `quality_recorded`, `remediation_requested` and `governance_handoff`. Snapshot `state.json` includes `governance` projections rebuilt from events. Files are written before event append, so an interrupted write can leave an **orphan** JSON record; this should be reconciled, not silently interpreted as consent. Event-chain integrity is not a signature/authentication mechanism.

## Conformance

```sh
python -m unittest discover -s tests -p 'test_governance*.py' -q
python -m unittest discover -s tests -p 'test_*.py' -q
```

Synthetic tests cover unauthorized transitions and permissions, identity, reviewer independence, exact artifact binding, gate scope, remediation, expiry/revocation, owner waivers, claimant ownership, parallel limits and old Prompt 10–11 regression behavior. See `temp/tests/PROMPT-12-GOVERNANCE-CONFORMANCE.md` for test results and known limitations.
