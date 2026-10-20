# Latest AOS-W Cross-Session Handoff

Updated: 2026-10-20
Completed assignment: Prompt 06, architectural research and proposed decision records.
Current repo: `digzoman/aos-workflows`, public `main`. Verify live HEAD before work.

## Mandatory first reads for Prompt 07

1. `temp/OPERATING-RULES.md`
2. `temp/DESIGN-DECISIONS.md`
3. `temp/WORK-PLAN.md`
4. `temp/PROGRESS.md`
5. `temp/OPEN-QUESTIONS.md`
6. `temp/architecture/SOURCES-06.md`
7. `temp/architecture/ALTERNATIVES-COMPARISON.md`
8. `temp/architecture/PRD-INPUTS-06.md`
9. `temp/architecture/ENVIRONMENTS-AND-MINIMAL-CORE.md`
10. `temp/architecture/COORDINATION-AND-LOCKING.md`
11. `temp/architecture/SKILLS-SCHEDULING-AND-SECURITY.md`
12. `temp/architecture/adrs/README.md` and ADR-001 through ADR-008
13. Previous marketing source indexes and candidate template catalogs under `temp/research/`

## Core findings requiring PRD treatment

- **A Rep is not AOS-W**. One nondeterministic PRIMARY, optional plans and events, provenance header, approved vs scratch skills, optional Guardian. Fred is active with host wake; Max remains deliberate manual/dormant. Support both without requiring A Rep.
- **Core must remain standalone**. Downloaded `scaffold/aos-w/` uses immutable standardized files and normally writable `agent-files/`. Git, Python, database, cloud/MCP, dedicated daemon or scheduler never mandatory. Same graph spec regardless of host.
- **Portable text declares, host enforces**. Graph, QC, authorizations, retries, schedules and leases can be described in Markdown/YAML/JSON. Actual atomic locks, concurrency, timers, external action readback and hard permission restrictions depend on appropriate optional host mechanisms.
- **LangGraph inspires** checkpoint/run identity, conditional edges, parallel fan-out, retry isolation, interrupt/human gates, versioned replan and recovery. Runtime is not copied/deployed.
- **Git claim mechanism undecided**. Provisional CAS-backed task refs preferred over LFS for logical tasks/shared credential, but official generic REST PATCH lacks explicit expected_sha; tests must verify available CAS primitive. LFS same-account behavior, crashes/expiry/network and stale fencing remain untested. Worktrees are isolation, not task locks.
- **Skills** follow progressive disclosure and may be bundled with master/custom/workflow packages or pinned externally; scripts/skills do not confer permissions. Remote skill trust, priority and offline fallback need approved resolution.
- **Recurring** is optional scheduling metadata with manual ad hoc always possible. Host wake required for unattended execution. Separate occurrence IDs and overlap/missed/DST decisions required.
- **A Rep public documentation discrepancy**. `CURRENT.md` says V1.5.0, `a-rep/SKILL.md` says V1.5.1; do not silently choose or assume live Fred host version.

## Next assignment, Prompt 07

Synthesize user-approved baseline, Prompt 01b schedule/skills, researched B1–B9 example workflows and this architecture evaluation into a detailed enhanced PRD at `docs/specs/prd/PRD.md`. Link spec requirements to research evidence, state definitions, testable acceptance and explicit risks. Include a decision register separating **approved requirements** from **proposed ADRs** and unresolved choices. Ask for explicit owner review and approval of PRD before building the workflow engine.

## Guardrails

- Do not implement code/engine, claims, Git locking, scheduling or external provider actions yet.
- Do not publish private A Rep repo content or tokens, only sanitized descriptions and restricted-path pointers.
- Do not claim a test passed based on a concept or official documentation alone.
- After research/spec session, update progress, handoff and Git commit; verify actual HEAD and file contents.
