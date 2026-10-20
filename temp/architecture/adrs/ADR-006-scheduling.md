# ADR-006, Declarative optional recurrence; no mandatory scheduler

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

Prompt 01b user decision: one-off default; templates may contain overridable schedules and always allow ad hoc starts. A Rep Fred offers runtime wake [A01/A13], Max has none [A14].

## Proposed decision

Treat schedule as trigger metadata independent of task DAG. Each actual occurrence gets distinct run ID, event trail and approval scope. Manual agent may check if due on invocation; a configured host trigger may schedule, but AOS-W itself never claims to execute while off.

## Alternatives and tradeoffs

Mandatory cron/daemon conflicts with zero-install. Treating due time as automatic start without a host is false. Duplicate host triggers require shared idempotency key and optional claim coordination. Exact RRULE/cron choice, timezone/DST/missed/overlap policy await PRD.

## Validation and reconsideration

Prompt 16 ad hoc launch from recurring template and no autonomous wake offline. Prompt 17 deduplicate overlapping occurrences in shared host, test DST/missed events.
