# AOS-W Development Operating Rules

Status: adopted development conventions for project creation and subsequent implementation sessions, 2026-10-20.

## Before doing work

1. Read `temp/DESIGN-DECISIONS.md`, `temp/WORK-PLAN.md`, `temp/PROGRESS.md`, and `temp/HANDOFF.md`, plus the relevant durable specification in `docs/`.
2. Check the current repository branch, recent Git commits, and any open relevant changes to avoid duplicating, overwriting, or falsely assuming work is finished.
3. Identify current task scope, its acceptance criteria, dependencies, and any approvals required.
4. Inspect real artifacts and evidence. Never claim tests, publishing, synchronization, or agent handoffs have happened unless verified.
5. Keep original user decisions distinct from architectural recommendations, inferred requirements, and experiments.

## While working

- Use the smallest justified changes and preserve previous decisions with rationale.
- Record new substantive design decisions, their source, and open alternatives in `DESIGN-DECISIONS.md`; register unresolved items in `OPEN-QUESTIONS.md`.
- Sanitize **before committing** anything to this public repository. Do not include customer data, credentials, unreleased internal documentation, proprietary raw transcripts, or private repository artifacts. Prefer summaries and pointers.
- Treat Git as optional for AOS-W end users, but mandatory for this **development repository** and these cross-session commits.
- Installed `scaffold/aos-w/` runs may edit only `agent-files/` by default. Framework upgrades are explicit exceptions.
- Maintain A Rep compatibility, including producer provenance `[Agent | Platform | Role | Instance]`; identity does not grant authority.
- Never confuse research, a plan, or a quality pass with authorization to make external changes or spend money.
- Do not implement the workflow engine before the enhanced PRD is reviewed and approved.

## At the end of every implementation or research session

1. Check work against task acceptance criteria.
2. Update `temp/PROGRESS.md` and `temp/HANDOFF.md` with completed work, verification, blockers, and the **next exact step**.
3. Record significant decisions and chronological events in `DESIGN-DECISIONS.md` and `IMPLEMENTATION-HISTORY.md`.
4. Commit changed files, with a meaningful message. Where practical include an `Agent-Provenance: [Agent | Platform | Role | Instance]` commit trailer. If the identity or instance is unknown, do not invent it.
5. Read back GitHub's latest commit or changed files and report the actual commit SHA.
6. If a tool is unavailable, preserve an honest blocked status and a reproducible handoff. Do not claim success.

## Scope and evidence boundaries

Planning and scaffold placeholders are not a runtime.
Prompt 01 establishes the repository and records only. Historical workflow research starts with Prompt 02. Enhanced PRD in Prompt 07 is a deliberate human approval checkpoint.
