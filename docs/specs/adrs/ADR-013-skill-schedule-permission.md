# ADR-013: On-demand skills, optional recurrence, explicit external authority

**Status:** PROPOSED, Prompt 08 technical design; **not owner-accepted**. 2026-10-20. PRD review record remained pending when this document was written.

## Context
Prompt 01b added master/custom/instance skills and optional scheduling. Historical Ampgent Meta/CRM failures show QC is not publication authority and provider write/readback differ.

## Proposed decision
Default manual trigger, optional recurrence stored as template/instance metadata and each due occurrence uniquely keyed; host performs real wake only when configured. Skill loaded on the relevant task from pinned/trusted local or external ref, with conflict/missing-source failure. No skill or due schedule escalates scope, and external production actions require separate valid approval plus readback.

## Consequences and alternatives
An always-on scheduler or Python skill resolver violates minimum standalone portability. Remote skill fetch has trust/supply-chain risks; schedule syntax/DST defaults remain open and cannot be invented by a reader.

## Required validation and reconsideration
Manual launch from recurring template, duplicate scheduled wake, missing remote skill offline, contradictory skill names, owner-declined activation, verified no-Git path.
