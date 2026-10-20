# AOS-W Cross-Session Handoff — Prompt 12

Updated: 2026-10-20
Status: Prompt 12 governance implementation complete, 75 synthetic/local tests passed. Next: Prompt 13 optional Git synchronization and real claim experiments.
Repo: `digzoman/aos-workflows`, main — verify HEAD and readback before edits.

## Required next reads
1. `temp/OPERATING-RULES.md`, `temp/DESIGN-DECISIONS.md`, `temp/CONCEPT-NOTES-01B.md`
2. `temp/WORK-PLAN.md`, `temp/PROGRESS.md`, `temp/IMPLEMENTATION-HISTORY.md`
3. `scaffold/aos-w/README.md`, `PROTOCOL.md`, `VERSION.json`
4. `scaffold/aos-w/references/PROVENANCE-QUALITY-PERMISSIONS.md` and `STATE-AND-RECOVERY.md`
5. `tools/governance/governance.py`, `cli.py`, `README.md`
6. `tools/state/state.py` plus `tools/composition/`
7. `temp/tests/PROMPT-12-GOVERNANCE-CONFORMANCE.md`, `tests/test_governance.py`, `tests/test_governance_cli.py`
8. `docs/specs/prd/PRD.md`, `docs/specs/architecture/COORDINATION-AND-LOCKING.md` if available, and `temp/architecture/COORDINATION-AND-LOCKING.md`

## Actual current behavior
- The installed scaffold remains file-based and operable by agents without programming runtime. Optional local checker supports actor provenance `[Agent | Platform | Role | Instance]`, advisory task ownership and release, append-only governance history, exact artifact-set independent/human/self/deterministic QC, structured remediation and version-bound waiver, scope-limited action approvals and revocation/expiry/amount controls, and detailed handoffs.
- `RunStore` Prompt 11 reducer now handles governance events and optional `context_checked` for authorized local adapter paths, with existing tests unchanged. This flag and user roles are NOT authenticated credentials.
- A grant valid at claim time is rechecked at task begin. Sender/publisher side effects are never performed; `operation_intent` records only intent after cooperative approval check.
- New record JSON is cross-checked against verified SHA-256 event content before reuse; file tampering fails closed, but filesystem access remains ultimately untrusted.
- Reviewer PASS on a changed artifact or old attempt/graph cannot unlock new work. Independent siblings may progress when a failed gate blocks dependents.
- More restrictive host permissions and real identity verification are not implemented.

## Test scope
- 38 new governance/CLI tests, 26 Prompt 11, and 11 Prompt 10: **75/75 pass** on isolated local files.
- No two-host collision, signed grant, true owner verification, provider request, image interpretation, or live business integration tested.

## Prompt 13 deliverables needed
Test both Git LFS file locks and genuinely conditional atomic Git task claims with real simultaneous workers, including shared GitHub identity, stale leases, crashes and loss of network; evaluate fencing. Add optional Git sync with check-before/write-after/verified-readback, conflict reporting, handoff and no hidden provider authority. Do not automatically select an untested winner. The base manual/no-Git folder must continue to work.

## Hard boundaries
All ordinary writes confined to `agent-files/`. Public repo contains no private contacts, credentials or raw Ampgent account details. `role=owner` and a QC PASS are not permission to send, spend or publish without actual host authentication; the test fixtures use declared simulated actors only.
