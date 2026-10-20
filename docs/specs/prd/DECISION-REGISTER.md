# PRD decision register

Date 2026-10-20. **Status: DRAFT FOR OWNER REVIEW**. This file prevents previously agreed constraints, proposed engineering choices and test-dependent decisions from being conflated.

## A. Agreed/user-selected product constraints

A-01 Public digzoman/aos-workflows with a directly downloadable scaffold/aos-w and repo-root documentation, optional helpers/scripts.  
A-02 Installed scaffold's only normally writable area is agent-files; custom templates, skills, runs and config there.  
A-03 No mandatory Git, Python or other coding runtime, database, MCP server, cloud provider, dashboard or scheduler.  
A-04 Support standalone local/cloud and optional shared collaboration/sync through the **same** file protocol.  
A-05 Reusable template composition, sequential/parallel, dynamic child runs, conditional routing, result merging.  
A-06 Markdown/YAML/JSON/JSONL, A Rep four-field producer identity and step-level ownership/claims.  
A-07 Automated, AI-independent, self-review and human QC/approval gates configurable per workflow/step.  
A-08 Bounded default autonomy, configurable delegated authority and dynamic revision policies; QC is not publish permission.  
A-09 Six V1 success tests mandatory including actual two-agent collision prevention in the capable shared mode.  
A-10 Compare Git LFS and atomic Git claim designs in real tests, **not** preselect a winner.  
A-11 Default one-off workflow invocation, optional recurrence and ad hoc manual starts from recurring templates.  
A-12 Skills within master/custom/instance packages, plus local and remote references; just-in-time loading and no permission escalation.  
A-13 No engine implementation before explicit PRD owner approval.

These are summarized in temp/DESIGN-DECISIONS.md and the [survey audit](SURVEY-TRACEABILITY.md).

## B. Draft architecture decisions for owner review

All eight remain **PROPOSED** in temp/architecture/adrs/ and must not be marked ACCEPTED merely by committing this PRD.

| ADR | Proposed direction | Core concern / approval point |
| --- | --- | --- |
| ADR-001 | Portable single file-based graph specification plus optional host adapters | What counts as a usable minimal standalone execution |
| ADR-002 | Per-run JSON snapshot, append-style JSONL events, Markdown handoff; derived indexes | Torn-write and authoritative replay semantics |
| ADR-003 | Independent storage/sync/coordination/execution capability flags | Fail-closed shared-mode limitations |
| ADR-004 | Research preference for task-ref CAS with LFS as required empirical alternative | Test actual conditional ref semantics first; no lock winner |
| ADR-005 | Agent Skills-style packaged/lazy/pinned skill refs with trust | Precedence, remote code trust, offline fallback |
| ADR-006 | Declarative schedule plus optional host wake, unique occurrence | Missed events, overlap, DST, default policy |
| ADR-007 | AOS-W task graph not a competing A Rep PRIMARY/long-term issue plan | Single source of authority per layer |
| ADR-008 | Exact-version QC, separate permission, provider readback and controlled compensation | Default human gates, external action boundaries |

## C. Decisions that can be deferred to technical design after PRD approval

D-01 file names within agent-files; D-03 declarative predicate grammar; D-04 task/gate enums; D-05 torn-write/snapshot-event consistency; D-11 cloud storage durability probes; D-15 artifact hash and migration mechanics; D-17 domain ledger identities and rubric metadata; D-19 measured operating bounds.

Deferral means **the requirements and acceptance invariants remain fixed**, not that the engineer may quietly grant additional external authority or introduce mandatory dependencies. Material scope/policy changes return to owner review.

## D. Decisions needing owner input or empirical tests

- **D-02:** exact override precedence, rules for owner-protected policy and conflicting config.
- **D-06/D-12:** Git LFS versus atomic ref claim winner, stale lease reclamation and output fencing. Empirical evidence required Prompts 13 and 17.
- **D-07:** recurrence notation, missed/overlap/DST defaults and optional host wake semantics.
- **D-08:** skill collision/precedence and remote script execution permissions.
- **D-09:** whether any live Meta/GHL **test account** integration is expected for V1 rather than mocked PAUSED workflow.
- **D-10:** public release license.
- **D-13/D-14:** scope of autonomous corrections, QA waivers, generated-child auto-start and consequential marketing permissions.
- **D-16:** installed Fred A Rep host version unverified; current docs differ.
- **D-18:** enforced vs cooperative independent reviewer isolation.
- **D-20:** data-usage rights and sensitive private-run sync/storage policy.

## E. Non-negotiable review statements

1. This document is a **requirements and proposed architecture** record, not approval to implement.
2. Passing a QC gate is not permission to send messages, deploy production, activate campaigns or spend.
3. Text files cannot guarantee hard locks/timers exactly once without tested host-side enforcement.
4. A Git repo mirror is not the current source of truth for Meta/HighLevel/website production facts.
5. The owner must explicitly respond with PRD approval after review; otherwise Prompt 08 stays blocked.
