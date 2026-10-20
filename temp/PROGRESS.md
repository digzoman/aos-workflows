# AOS-W Progress Snapshot

Date: 2026-10-20
Phase: Prompt 06, research of existing frameworks and architecture alternatives
Status: **Research stage COMPLETED; architecture choices proposed, NOT approved.**
Next: Prompt 07, enhanced PRD and human review/approval.

## Verified prior work

Prompts 01–05 completed and committed as research/design; see earlier `temp/IMPLEMENTATION-HISTORY.md`, evidence indexes and the operation/creative/research candidate template catalogs.

## Prompt 06 completed

- Read current AOS-W rules, design baseline, work plan, prior handoff and open questions and verified starting repo branch SHA.
- Authenticated read-only inspection of `digzoman/a-rep` (public), `digzoman/a-rep-Fred` (private) and `digzoman/a-rep-Max` (private). Traced skills, one-PRIMARY authority, four-field provenance, plan-work/data-ledger, hot/deep context, Fred active scheduler and Max dormant/manual pattern. Verified one actual Fred PLAN/EVENTS example.
- Compared official current LangGraph documentation for nodes/edges, checkpoint/thread state, retries, conditional routing, parallelism, interrupts, idempotency, time travel and subgraphs.
- Reviewed Agent Skills specification and Git official documentation for worktrees, LFS locking and Git ref/push semantics.
- Kept separate text-file graph description and any enforcing runtime; wrote shared-Git claim CAS design as **provisional preference**, with LFS comparison still explicitly required.
- Described standalone local/cloud, Git synced and collaborative modes as orthogonal capabilities, never separate workflow languages.
- Recorded proposed state/event/checkpoint, optional scheduling, just-in-time skill trust, A Rep integration, file-only execution limits and external-action approval boundaries.
- Created source register, architecture alternatives comparison, LangGraph/A Rep/coordination/skills notes, PRD recommendations and eight draft ADRs, all PROPOSED.
- Updated work plan, durable handoff and open questions. Public docs have no private repo raw content or secrets.

## Not done, not claimed

- No workflow implementation, runtime, schema validator, lock, scheduler, MCP server, database or automated host.
- No empirical Git LFS or atomic Git double-claim race test, stale lock recovery or network-outage test. These remain Prompts 13 and 17.
- No claim that plain Markdown/YAML enforces parallelism, exclusive locks, time-triggered wake or external spend boundaries.
- No approval or final selection of ADRs and no unapproved agent/prod account changes.
- No assertion that private Fred's installed host runtime version equals the differing public A Rep documentation versions (CURRENT 1.5.0, SKILL 1.5.1).

## Next action

Run Prompt 07. Read `temp/architecture/SOURCES-06.md`, `ALTERNATIVES-COMPARISON.md`, `PRD-INPUTS-06.md`, all proposed ADRs and the preceding marketing workflow research. Draft enhanced `docs/specs/prd/PRD.md` with explicit evidence/requirement tags and user approval checkpoint. **Stop before coding until owner approves PRD.**
