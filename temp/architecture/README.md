# Prompt 06 architectural research

All work here is **research and draft decisions**, not runnable AOS-W code or owner-approved architecture.

Suggested reading:

1. [SOURCES-06.md](SOURCES-06.md), directly inspected A Rep repositories and official LangGraph/Agent Skills/Git documentation.
2. [A-REP-COMPATIBILITY.md](A-REP-COMPATIBILITY.md), Fred/Max and plan/skill/provenance integration.
3. [LANGGRAPH-PATTERN-MAPPING.md](LANGGRAPH-PATTERN-MAPPING.md), graph patterns mapped to declarative files versus actual runtime enforcement.
4. [ENVIRONMENTS-AND-MINIMAL-CORE.md](ENVIRONMENTS-AND-MINIMAL-CORE.md), local/cloud, Git synced, collaborative capability matrix.
5. [COORDINATION-AND-LOCKING.md](COORDINATION-AND-LOCKING.md), LFS, Git claims, worktrees, shared identity and failure/test matrix.
6. [SKILLS-SCHEDULING-AND-SECURITY.md](SKILLS-SCHEDULING-AND-SECURITY.md), skills and optional recurring triggers.
7. [ALTERNATIVES-COMPARISON.md](ALTERNATIVES-COMPARISON.md), decision matrix and smallest recommended file-first model.
8. [PRD-INPUTS-06.md](PRD-INPUTS-06.md), explicit guidance for Prompt 07.
9. [adrs/README.md](adrs/README.md), eight individual PROPOSED Architecture Decision Records.

No lock, Git LFS experiment, CAS claim, task engine, scheduler or skill loader was built in Prompt 06. The user's requirement to **test both Git LFS and atomic Git claims** remains open for Prompts 13 and 17.
