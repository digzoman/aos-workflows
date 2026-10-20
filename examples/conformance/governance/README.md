# Governance fixture scenarios (synthetic only)

The companion tests `tests/test_governance.py` and `test_governance_cli.py` create fresh disposable file trees and exercise five example tasks: `draft` with deterministic and independent AI gates, `dependent` waiting for an accepted draft, `parallel` independent of that draft, `human-review` requiring a declared owner-level reviewer, and `send` demanding explicit scoped `send_message` authority. No real messages are sent.

The tests deliberately record both a rejected draft and corrected resubmission. The `parallel` task remains eligible during its sibling's `NEEDS_REWORK` state. A passing QC verdict for `draft` does not grant permission to send a message. The simulated owner can grant a bounded resource-specific authorization, then revoke or expire it. Two agents with the same agent/platform/instance but different role strings are **not** considered independent.

Tests also illustrate advisory claim conflicts, serialized task capacity, complete artifact version/hash matching, explicit `WAIVED_BY_OWNER` on a gate configured as waivable, and append-only reviewer/handoff provenance. No external identity is authenticated or real provider operation executed.

Run from the development repository: `python -m unittest discover -s tests -p 'test_governance*.py' -q` (optional Python+PyYAML) or follow [manual file protocol](../../../scaffold/aos-w/references/PROVENANCE-QUALITY-PERMISSIONS.md) with a capable agent.
