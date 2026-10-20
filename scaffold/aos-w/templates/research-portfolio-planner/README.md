# Research portfolio planner (0.2.0)

A portable, **manual** four-stage parent graph:

```
define-verticals → approve-plan → propose-investigations → synthesize
```

Approved plan items can generate uniquely identified independent `competitor-investigation` child run **proposals** using `plan_id`, stable `slug` and `revision`. A proposal is not a started run. Creating children requires a separate exact-scoped owner authorization and keeps every child’s own pinned template, state/event history and review outputs.

The final synthesis is **blocked until all required child investigations have COMPLETE status and current evidence-qc PASS**, and a separate synthesis authorization. Parallel branches may be scheduled by different hosts only where actual shared coordination is verified. Otherwise a single manual agent can work child-by-child.

No automated Meta browsing, remote tools, publishing, or background scheduling is included.
