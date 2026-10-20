# AOS-W original 16-question survey traceability

**Status:** Review artifact for the draft PRD (2026-10-20). This document preserves the survey decisions and distinguishes the additional Prompt 01b refinements and later architecture research. It is **not a substitute for the user's approval of PRD.md**.

| Survey question | User decision | PRD location | Verification |
| --- | --- | --- | --- |
| **Q01. V1 objective** | All three objectives equally important: realistic Ampgent example, portable reusable standard, reliable cross-agent collaboration | §§1.1, 1.3, 3.1, 20 | T01, T02 and portable installer T07 |
| **Q02. Included workflow modules** | All five: planning/keyword research; repeatable research runs; independent QC/corrections; synthesis/scoring; ad creative and marketing implementation | §§3.1, 9.3, 18 A–D | T01, T04, T13, T15 |
| **Q03. Composition** | All five: template composition; parallel work; plan-derived dynamic instances; merging; conditional execution | §§7.1–7.3, 16 | T01, T04, T05, parallel/child cases |
| **Q04. Repository visibility** | Entirely public, including nonconfidential examples | §§1, 3.1, 6, 15 | NFR-09, public audit |
| **Q05. Portable install structure** | One self-contained aos-w folder; **agent-files is the only normally writable directory**, even for custom templates; include explanatory Markdown | §§1.4, 6.1–6.4, FR-003 | T07, write-boundary check |
| **Q06. Source formats** | Markdown instructions; YAML workflow definitions; JSON/JSONL execution state/history | §§1.4, 6.2, 8.2, 16.1 | T07, state/event round-trip |
| **Q07. Git task locking** | Prototype and compare **Git LFS locks** and **atomic Git task claims**, including crashes/shared agent identity | §§10, 11, 19–20, 23 D-06 | T03, Prompt 13/17 race suite |
| **Q08. A Rep relationship** | Independent framework that integrates with Fred, Max, A Rep, but does not depend on or replace A Rep | §§1.1, 4, 10, 22.2 | T02, integration/no-A-Rep check |
| **Q09. Identity/provenance** | Record checkout owner/times, commit trailers where Git used, handoffs and QC/approvals; no mandatory audit of every file read | §§5, 8.2, 9, 10, FR-401 | T02/T03, provenance audit |
| **Q10. Ownership** | Step/task-level exclusive ownership with timestamp, expiry, handoff/progress; concurrency when safely coordinated | §§10, 11, 19 | T03 and stale takeover tests |
| **Q11. Quality gates** | Automated/objective checks, independent AI review, human approval, self-review for low-risk work; configurable workflow defaults; future authorized AI publishing possible after gates | §§9.1–9.3, 14, 18 | T04/T13, independent approval and separate publish permission |
| **Q12. Autonomy** | Workflow-specific autonomy with controlled/bounded defaults | §§9.2, FR-306, 14.1, 23 D-13 | Scoped permission/negative side-effect tests |
| **Q13. Dynamic revisions** | Configurable per workflow; preserve history and completed work; reevaluate affected dependent gates | §§7.2, 8.3, 9.2, 20 | T05, targeted rework |
| **Q14. Success criteria** | **All six:** real Ampgent execution, cross-platform handoff, collision prevention, QC block/correct, dynamic revision, Git portability | §§1.3, 20 T01–T06 | All six mandatory |
| **Q15. Exclusions** | Avoid mandatory Python/runtime, dedicated MCP server, database, dashboard and scheduler; allow optional helpers | §§1.4, 3.2, 4, 22 | T07, standalone no-runtime |
| **Q16. Repo name/distribution** | **digzoman/aos-workflows** public repo containing downloadable **scaffold/aos-w/**, with docs/scripts/tools at repository root as needed; **Git is optional**, not assumed local/cloud | §§1, 4, 6, 11 | T06, T07, folder download |

## Later approved user refinements (Prompt 01b), not part of original 16

**Recurrence:** non-repeating by default; master/custom templates may declare overridable recurrence; ad hoc invocation from a recurring template must work; no required daemon. See PRD §12 and tests T08–T09.

**Skills:** bundle per master template, custom template and workflow instance; refer to installed/local/repo skills; load just in time; skill reference is not authorization. See PRD §13 and T10.

**Operating modes:** Git not mandatory and cloud-stored work can be single-agent; Git mirroring needs update/checkpoint behavior; optional multi-agent coordination requires separate capability. See §§4, 11.

**LangGraph inspiration:** checkpoints, interrupts, retries, branches and recovery; not mandatory LangGraph runtime. See §22.2.

## Assessment

**Coverage assessment:** 16/16 survey choices explicitly represented in the draft PRD, plus the Prompt 01b refinements. This is a **document audit**, not evidence that functionality or tests exist.

**No inferred choice to fill gaps:** schema field names, shared locking winner, lease/fencing policy, schedule syntax, skill precedence, storage durability guarantees, live marketing pilot depth, and license remain OPEN in PRD §23.

**Original source provenance:** user-selected answers were consolidated into repository temp/DESIGN-DECISIONS.md by the earlier survey phase; this trace maps that durable baseline. It does not claim the original interactive survey form itself is present in the repo.
