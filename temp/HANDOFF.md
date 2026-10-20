# Latest Cross-Session Handoff

Updated: 2026-10-20
Previous assignments: Prompt 01 repository initialization, then Prompt 01b requirements amendment for recurring triggers and bundled/referenced skills.
Result: Initial GitHub repository and documentation-only scaffold committed. Prompt 01b design decisions added without implementing any workflow or scheduling runtime. Verify the current branch head before work.

## First reads

1. `temp/OPERATING-RULES.md`
2. `temp/DESIGN-DECISIONS.md`
3. `temp/WORK-PLAN.md`
4. `temp/PROGRESS.md`
5. `temp/OPEN-QUESTIONS.md`
6. `temp/CONCEPT-NOTES-01B.md`

## Next assignment, Prompt 02

Research the actual Ampgent project conversations from recent weeks and relevant `digzoman/a-rep-Max` artifacts, focusing on the multistep Meta Ads Library research process and transition through ad creatives, campaign setup, launch, and performance monitoring.

Create a source index in `temp/research/` with conversation title, date or approximate period, workflow stage, accessible source pointer, evidence strength, and any access limitations.

Capture how tasks were planned, divided into prompt-specific runs, completed, quality checked, revised, and handed off.

Only commit **sanitized summaries and source pointers**, not raw private conversations or personal/client information.

If project conversations are not accessible to the current agent, report which sources can/cannot be reached and record a reproducible blocker. Avoid inventing absent details.

## Important added requirements for later PRD

- Workflows are non-repeating by default. Master/custom templates may provide overridable recurring schedules, and ad hoc launch must always remain an option.
- Recording a schedule does not mean it runs autonomously. No required scheduler, daemon, or background engine.
- Templates and workflow instances may contain their own skill packages; steps may also refer to installed/local/repository skills, loaded only when relevant. A skill does not grant authority.
- See `temp/CONCEPT-NOTES-01B.md` for explicit distinction between confirmed requirements and proposed design examples.

## Scope restrictions

Do not create executable engine code or treat this scaffold as operational. Keep true user choices separate from proposed designs. The next human approval gate is Prompt 07 PRD review.
