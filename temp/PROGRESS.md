# AOS-W Development Progress

Date: 2026-10-20
Phase: **Prompt 12 — agent provenance, quality gates and scoped permissions implemented**
Status: PORTABLE FILE-ONLY PROTOCOL + OPTIONAL LOCAL GOVERNANCE CHECKER. No runtime-independent hard security.

## Completed foundation
Prompts 01–10 research, PRD, portable scaffold and composition; Prompt 11 SHA-256 event journal, attempt/retry/checkpoint and recovery. Prompt 11's staged files were **separately committed to main** before beginning Prompt 12 so no unpublished prerequisite was lost.

## Prompt 12 implementation
- Version 0.4.0 file-first governance protocol, with optional Python local checker in `tools/governance` and CLI.
- Four-field actor identity on task claim/release, run events, QC decisions, approvals/revocations, remediation and handoffs.
- Task claims record owner, task ID, expiry, progress, and explicitly **advisory** mode. Manual release and parallel task ceilings; no hard multi-agent locks.
- Workflow-default and per-step quality gates: deterministic artifact hashes, independent AI reviewer, human-declared review, explicitly allowed self-review. Current attempt, full artifact set and graph revision must match.
- Failed QC records structured corrections, blocks dependent tasks but leaves unrelated siblings eligible, and requires a new reviewed attempt. Explicit waivers are recorded as `WAIVED_BY_OWNER` only on gates that opt in; aggregate marks `ACCEPTED_WITH_WAIVER`.
- Bounded routine autonomy and exact action-level owner-declared grants, with graph/resource/target/amount/expiry checks, revocation and recheck after claiming before start. No wildcard approval, no live provider action.
- Verified record JSON must match SHA-256-chained event ledger; mismatched/tampered approval files denied. Handoff names owners, pending QC, current state and next steps.
- Added additive schemas and two new record schemas (`remediation`, `governance-handoff`) in development and shipped folders; all older optional fields preserved.
- Full manual protocol in `scaffold/aos-w/references/PROVENANCE-QUALITY-PERMISSIONS.md`; no mandatory Python, Git, MCP, database or scheduler.

## Tests executed
- **38 Prompt 12 governance/CLI tests PASS**
- **26 Prompt 11 state/recovery tests PASS**
- **11 Prompt 10 composition tests PASS**
- **75 total PASS**, all on synthetic local files; no internet/external provider tools used.
- Source test report: `temp/tests/PROMPT-12-GOVERNANCE-CONFORMANCE.md`.

## Not built/not claimed
- Hard OS/provider enforcement, cryptographically authenticated human decisions, independent model execution, real simultaneous writer fencing or Git LFS/CAS locks.
- Auto scheduling, server synchronization, authorized Meta/HighLevel/website/social actions, real work launched from test data.
- JSON Schema contents specify record shapes, not runtime authority; self-attested `role=owner` is not proof of user consent. A malicious process could bypass the optional checker.

## Next action
Prompt 13: optional Git synchronization and empirical Git LFS vs atomic Git claims (same-credential races, stale leases, crash, network errors, fencing). Keep no-Git manual path the default. Continue preserving source PRD and runtime `agent-files` boundary.
