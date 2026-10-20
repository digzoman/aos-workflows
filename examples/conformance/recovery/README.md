# Recovery conformance examples (fictional data)

These scenarios are exercised by `tests/test_state.py` under disposable local `agent-files/instances/fixture/runs/run-001/` directories. **No production accounts are accessed.**

| Scenario | Local source of truth | Required next behavior |
| --- | --- | --- |
| Fresh session after valid checkpoint | JSONL events + pinned graph | Rebuild current steps, owners, evidence and next eligible node |
| Torn last JSONL line | Longest valid prefix | BLOCKED until explicit repair, preserve the suspect tail bytes |
| Snapshot says event 9000 but journal ends earlier | Verified event prefix | Save stale snapshot, replay actual events, record recovery |
| Event digest tampered | Digest chain and preserved bytes | Reject as corrupt; operator-authorized tail quarantine only |
| Uncertain provider create/activation | Operation key and external request state | Do not repeat mutation; record readback or remain RECONCILE_REQUIRED |
| Two pending children, one partially created | Child proposal IDs and directories | Report PARTIAL/MISSING, no overwrite or unintended second child |
| Post-event graph revision crash | graph_revised event + immutable g0002 SHA | Repair stale current graph pointer only when bytes match |
| Previously completed output removed | Historical completion event + current file hash | Preserve history; mark present evidence invalid and block dependents |
| Failed review correction | Exact review on artifact revision | New bounded attempt and revised review, not retroactive PASS |
| Schedule or real provider integration absent | File protocol only | Never claim background wake or live mutation |

The files `scaffold/aos-w/references/STATE-AND-RECOVERY.md` and `tools/state/README.md` define manual and optional deterministic procedures. Historical 0.1 pinned practice runs remain unmodified in this version.
