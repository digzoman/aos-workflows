# ADR-010: Validated events as audit authority, derived state and anchored checkpoints

**Status:** PROPOSED, Prompt 08 technical design; **not owner-accepted**. 2026-10-20. PRD review record remained pending when this document was written.

## Context
A Rep's PLAN/EVENTS shows durable progress; research portfolio indexes can become stale. LangGraph replay warns interrupted steps and side effects may repeat. PRD D-05 was open.

## Proposed decision
Use ordered event.jsonl log as audit source for a run; state.json materializes current status and checkpoints store immutable event-prefix resume anchors. On mismatched/truncated event or inconsistent snapshot, preserve suspect data, recover last verified prefix and reconcile unknown provider effects before retry.

## Consequences and alternatives
Snapshot-only is easier but cannot prove history. Pure event sourcing may be cumbersome for manual agents; materialized state is the acceptable convenience. Without host atomic file writes, do not claim crash-proof updates; integrity strength must be explicit.

## Required validation and reconsideration
Simulated torn JSONL, stale state, replay by different agent, ambiguous provider write; verify prior accepted reviews remain traceable.
