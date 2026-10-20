# ADR-007, AOS-W is a workflow layer, not a second A Rep PRIMARY

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

A Rep uses agent Issues and optional plan-work for open-ended prioritized activity [A01/A08]. Fred has one mutating PRIMARY and advisory Guardian [A04/A10], while Max's repo supports manual sessions [A14].

## Proposed decision

A Rep may link an authorized issue or plan to an AOS-W run. AOS-W controls per-task dependency/QA/recovery within its instance, not the agent's high-level goals, wake cycle, system authority, or source-of-truth business records. Four-field provenance compatible with A Rep, but cannot grant authority.

## Alternatives and tradeoffs

Duplicating plan-work into another authoritative planner creates contradictory statuses. For users without A Rep, AOS-W remains complete enough for a manual agent to execute a bounded workflow.

## Validation and reconsideration

Pilot a linked Fred work Issue without altering PRIMARY runtime and a manually invoked Max run; cold-start recovery and human authorization remain correct.
