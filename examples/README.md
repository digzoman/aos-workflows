# Sanitized examples and fixtures

The downloaded [AOS-W scaffold](../scaffold/aos-w/) contains its own immediately inspectable starter examples:

- [research-starter master template](../scaffold/aos-w/templates/research-starter/template.yaml) with [step-local evidence-handling skill](../scaffold/aos-w/templates/research-starter/skills/evidence-handling/SKILL.md).
- [periodic-review-example template](../scaffold/aos-w/templates/periodic-review-example/template.yaml), a **disabled** weekly schedule declaration that can be manually invoked without a scheduler.
- [demo-local-research](../scaffold/aos-w/agent-files/instances/demo-local-research/README.md), a pre-seeded **CREATED, not executed** practice instance with pinned template, run/events/state/checkpoint, task/claim/review/approval directories and handoff. Its source data is synthetic; no actions were actually executed.

This project will later add sanitized Ampgent research, creative production and advertising implementation templates. The original private advertising sources and live provider records are **not** public fixtures.

No example grants Meta, CRM, messaging or production deployment access.

- [Prompt 10 composition fixtures](conformance/README.md), a sanitized 3-investigation portfolio and deliberately simulated approvals, with real **local-file-only** conformance tests. These are not completed real competitor investigations.

- [Prompt 11 recovery scenarios](conformance/recovery/README.md) describe interrupted, inconsistent and incomplete local runs with no real provider actions. The executable `tests/test_state.py` builds these disposable fixtures and checks their safe outcomes.
