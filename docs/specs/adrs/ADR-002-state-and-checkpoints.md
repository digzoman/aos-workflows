# ADR-002, Per-run state and append-oriented audit with versioned checkpoints

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

A Rep plan-work [A08] uses authoritative PLAN plus EVENTS with a derived index; data-ledger [A09] has stable event_id. LangGraph checkpointers [W03/W04] persist thread-scoped state; execution can resume/replay [W05/W06].

## Proposed decision

Store machine-readable current per-run state (JSON), append-oriented versioned events (JSONL), human-readable task/progress/handoff (Markdown), and template graph YAML. Each event references logical identity, timestamp, actor, source revision and affected artifacts/approval. Summaries/indexes are rebuildable. Treat unclear partially completed attempts as reconciliation-needed rather than completed.

## Alternatives and tradeoffs

Snapshot-only loses provenance; raw event-only raises rebuild burden. Append to plain files is not crash-atomic or concurrently safe by default, so enforced writers need host-level transaction/claim adapter. Avoid dual competing authoritative state; define revision/checksum and recovery procedure in Prompt 08.

## Validation and reconsideration

Test interrupted write/partial JSONL line, lost write acknowledgment, stale portfolio rollup, changed artifact hash invalidating old QC, and resumption by different agent. No claim of exactly-once execution.
