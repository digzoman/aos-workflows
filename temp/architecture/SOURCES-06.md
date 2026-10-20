# Prompt 06 architecture source register

Prepared 2026-10-20. This public record contains **sanitized summaries and document locators**. Directly accessed A Rep documents are identified A01–A15. Public official documentation accessed independently is W01–W12. Treat repository descriptions as evidence of documented design, **not validation of what is presently running on a host**.

## Inspected repositories

- **A01** `digzoman/a-rep/README.md`, public. Describes A Rep nondeterministic FIRST PRIMARY loop, optional V1.5 plan-work/data-ledger, event/heartbeat wake, scoped skills, provenance and cold-start recovery. [source](https://github.com/digzoman/a-rep/blob/main/README.md)
- **A02** `digzoman/a-rep/CURRENT.md`, public. Describes current **V1.5.0** snapshot, plan status recovery, source authority, and non-authoritative generated indexes. [source](https://github.com/digzoman/a-rep/blob/main/CURRENT.md)
- **A03** `digzoman/a-rep/a-rep/SKILL.md`, public. Main skill's visible heading states **V1.5.1** and the metadata version likewise says 1.5.1; this differs from A02's V1.5.0. Do not silently reconcile this version mismatch. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/SKILL.md)
- **A04** `digzoman/a-rep/a-rep/references/PROTOCOL.md`. Cold-start recovery, authority, one PRIMARY mutator, Guardian advisory role, provenance, event/heartbeat recovery. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/references/PROTOCOL.md)
- **A05** `digzoman/a-rep/a-rep/references/SKILLS.md`. Reusable skill packages, experimental `scratch/skills/` vs human-approved `procedures/skills/`, skill/authority separation. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/references/SKILLS.md)
- **A06** `digzoman/a-rep/a-rep/references/PROVENANCE.md`. Exact producer header `[Agent | Platform | Role | Instance]`, agent run correlation, shared GitHub identity limitation, no permission from provenance. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/references/PROVENANCE.md)
- **A07** `digzoman/a-rep/a-rep/references/ISSUES.md`. Work Issues versus system authority and persistent agent radar. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/references/ISSUES.md)
- **A08** `digzoman/a-rep/a-rep/scaffold/agent-repo/procedures/skills/plan-work/SKILL.md`. Human-readable PLAN/EVENTS, recovery states, current-authoritative PLAN, index derived, helper optional. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/scaffold/agent-repo/procedures/skills/plan-work/SKILL.md)
- **A09** `digzoman/a-rep/a-rep/scaffold/agent-repo/procedures/skills/data-ledger/SKILL.md`. Provider/business/working audit truths, snapshot CSV and stable event_id de-duplication, helper optional. [source](https://github.com/digzoman/a-rep/blob/main/a-rep/scaffold/agent-repo/procedures/skills/data-ledger/SKILL.md)
- **A10** `digzoman/a-rep-Fred/README.md`, **private**. Active agent repo, approved skills, GitHub issue radar, PRIMARY runtime with 30-minute backup heartbeat and event watcher, bounded Guardian. This repo's README says V1.4.1 policy target while public A Rep has changed since; live host version must be independently checked. Restricted source pointer `digzoman/a-rep-Fred/README.md`.
- **A11** `digzoman/a-rep-Fred/work/plans/issue-90-meta-blind-ranking-2026-09-25/PLAN.md` and `EVENTS.md`, **private**. Actual bounded Ampgent multi-chunk plan with source verification, independent scoring, human authority, completion event, and later source re-check that preserved old ranking. Restricted pointer.
- **A12** `digzoman/a-rep-Fred/procedures/graphs/README.md` and `digzoman/a-rep-Max/procedures/graphs/README.md`, **private**. Both permit reviewed graph descriptions using LangGraph terminology **without** requiring LangGraph runtime.
- **A13** `digzoman/a-rep-Fred/scratch/skills/scheduled-wake/SKILL.md`, **private**. Experimental, local delayed wake with explicit issue scope, no added authority, not promoted to canonical scheduler.
- **A14** `digzoman/a-rep-Max/README.md`, **private**. Max **MANUAL AND DORMANT** by design, no cron, heartbeat, VM PRIMARY, watcher or persistent runtime; manually invoked agents share repo state. Reviewed versus scratch skills; no automatic runtime assumed.
- **A15** Fred and Max repository directory listings, **private**. Confirm both have `procedures/skills/plan-work`, `data-ledger`, `scratch/skills` and empty/descriptive `procedures/graphs`. Fred has live `work/plans` examples; Max `work/plans` was not found, which does **not** mean A Rep capabilities are absent.

## Public primary reference documentation reviewed

- **W01** LangGraph Graph API, state/nodes/edges, supersteps: https://docs.langchain.com/oss/python/langgraph/graph-api
- **W02** LangGraph Graph API usage, parallel execution, conditional transitions, retry policy and max concurrency: https://docs.langchain.com/oss/python/langgraph/use-graph-api
- **W03** LangGraph persistence/checkpoint/store distinction: https://docs.langchain.com/oss/python/langgraph/persistence
- **W04** LangGraph checkpoints, thread_id and super-step boundaries: https://docs.langchain.com/oss/python/langgraph/checkpointers
- **W05** LangGraph interrupts and idempotency before interrupted node replay: https://docs.langchain.com/oss/python/langgraph/interrupts
- **W06** LangGraph functional API resume and safe idempotent side-effect tasks: https://docs.langchain.com/oss/python/langgraph/functional-api
- **W07** LangGraph checkpoint forks/time travel do not erase original history: https://docs.langchain.com/oss/python/langgraph/use-time-travel
- **W08** LangGraph subgraphs and checkpointer inheritance: https://docs.langchain.com/oss/python/langgraph/use-subgraphs
- **W09** Agent Skills format (primary spec and vendor-neutral documentation): https://agentskills.io/specification and https://github.com/agentskills/agentskills
- **W10** Git worktrees, `worktree lock` prevents administrative pruning, **not** task-file editing collisions: https://git-scm.com/docs/git-worktree
- **W11** Git LFS lock, locks and GitHub LFS installation requirements: https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-lock.adoc , https://github.com/git-lfs/git-lfs/blob/main/docs/man/git-lfs-locks.adoc , https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
- **W12** Git reference update API, fast-forward default and explicit expected-SHA lease via Git push: https://docs.github.com/en/rest/git/refs , https://git-scm.com/docs/git-push

## Evidence caveats and pending empirical validation

- Official docs document behavior of **their runtime and version**, not automatic behavior of portable AOS-W markdown files.
- Public A Rep `CURRENT.md` / `a-rep/SKILL.md` have different minor versions at retrieval. Do not assume Fred VM installation matches either.
- Git LFS and atomic Git coordination were **researched, not exercised** against two simultaneous real agents in this task. Selecting a final shared-lock implementation requires Prompt 17 empirical tests.
- This project intentionally has no framework runtime, scheduler, or lock implementation at Prompt 06.
