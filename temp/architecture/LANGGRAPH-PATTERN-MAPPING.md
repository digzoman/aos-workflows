# LangGraph concept mapping without LangGraph runtime

Based on current official LangGraph docs W01–W08 in [SOURCES-06.md](SOURCES-06.md). Each row distinguishes what a portable file can **specify** from what requires an executing host to **enforce**. This is an architectural study, **not an implemented LangGraph integration**.

| LangGraph mechanism | Portable AOS-W equivalent proposal | What needs a host/executor |
| --- | --- | --- |
| StateGraph, nodes, edges | YAML task nodes with stable IDs, declared input/output, fixed dependencies and conditional predicates | Actually select/execute nodes, validate conditions, write verified completion |
| Super-steps/checkpoints and thread_id | Distinct workflow-instance/run identity, durable checkpoints after each committed transition, exact artifact revision | Atomic update or concurrency-safe transaction, reliable crash-resume |
| Checkpointer vs store | Per-run state/event log vs separate cross-run/portfolio knowledge/evidence ledger; indexes rebuildable | Backing persistence guarantees, read/write arbitration and collection indexes |
| Reducers for parallel state | Explicit named merge strategy for branch outputs, no silent last-writer-wins | Correct concurrent merge/conflict detection and validation |
| Conditional edges/Command | Versioned predicates with outcomes PASS/FAIL/UNKNOWN, bounded branch selection | Evaluate using live evidence and ensure an agent follows selected next step |
| Send/dynamic fan-out | Generate child-run proposals from approved portfolio plan with stable IDs, dependency and autonomy policy | Actually create instances, coordinate parallel workers and enforce individual authorization |
| Parallel branches | Independent task claims and branch-local outputs, join after accepted/reviewed versions | Concurrent agents, locks, shared store or remote coordination; scheduling/budgets |
| RetryPolicy and backoff | Per-step retry ceiling, recoverable error taxonomy, next-eligible-after timestamp | Timed retry wake, reliable attempt accounting and source-specific backoff |
| interrupt/human gate | WAIT_HUMAN/WAIT_QC with approval requirement bound to scope/revisions | Truly suspend/resume execution and prevent unauthorized side effects |
| Durable task execution | Append events, snapshot state and record outputs/side effects before marking complete | Exactly what tools were executed, resumable safe side effects, atomic commits |
| Subgraphs | Workflow templates composing reusable child workflow packages | Execution isolation and memory/checkpoint mode |
| Time travel/branching | Revision lineage and checkpoint fork that preserves original run and QA findings | Actual reset/fork/re-execute and source/version isolation |

## Important upstream caveats

- LangGraph docs define checkpoint after a super-step and durable thread-scoped state keyed by `thread_id`, distinct from application-level long-term `store` data [W03/W04]. AOS-W should **not** claim exact same semantics until designed and tested.
- Real graph execution uses code nodes, conditional functions, framework runtime, optional durable checkpointers and actual task dispatch [W01/W02]. Markdown/YAML alone can declare graph edges but cannot execute or enforce them.
- LangGraph interrupts re-enter their node on resume, so side effects before the interrupt may run again [W05]. The functional API likewise warns that started-but-unfinished tasks can rerun; use idempotency keys or check provider state [W06].
- Time travel changes may **fork** from a saved checkpoint rather than silently rewrite old history [W07]. AOS-W should version workflow revision, reviewer-gate evidence and affected dependencies rather than edit past APPROVED state in place.
- LangGraph parallel node execution and RetryPolicy are supplied by the running framework [W02]. AOS-W’s first release can specify independent eligible tasks for manual workers, without claiming automatic parallelism in plain-file mode.
- Per-invocation versus per-thread subgraph persistence applies to LangGraph runtime [W08]; a candidate AOS-W child run should have an independent identity and clear parent/child relation.

## Recovery invariants proposed

1. An attempt that began but lacks durable output confirmation is `UNKNOWN/NEEDS_RECONCILIATION`, not automatically PENDING or FAILED.
2. For every side effect, record operation key, expected provider object, permission, requested mutation, response and verified provider readback separately.
3. For deterministic work, artifact hash and gate version determine which downstream checks must be invalidated.
4. On QC failure, retry the smallest impacted subgraph and keep unaffected sibling branches available.
5. Conditional routing must explicitly represent UNKNOWN and BLOCKED; do not coerce no browser evidence into no ads.
6. Resume from canonical per-task status and last verified checkpoint, not a derived dashboard/index or a previous assistant's unverified completion claim.

These are PRD suggestions, not promises of automatic retries or exactly-once execution.
