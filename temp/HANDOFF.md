# Latest Cross-Session Handoff

Updated: 2026-10-20
Previous completed assignment: Prompt 02, Ampgent history and evidence index.
Result: Sanitized history indexed and work-pattern cases documented in the public repository. Verify current GitHub branch head and read the source index before starting.

## First reads for Prompt 03

1. `temp/OPERATING-RULES.md`
2. `temp/DESIGN-DECISIONS.md`
3. `temp/WORK-PLAN.md`
4. `temp/PROGRESS.md`
5. `temp/research/SOURCE-INDEX.md`
6. `temp/research/WORKFLOW-PATTERNS.md`
7. `temp/research/EVIDENCE-GAPS.md`
8. `temp/OPEN-QUESTIONS.md`
9. `temp/CONCEPT-NOTES-01B.md`, as relevant to recurring workflows and skill references

## Evidence collected

- Private Max repo inspected at `work/ampgent-adaptive-offer-testing/`, including research refresh, meta-ad bakeoff, creative bakeoff, Meta staging/launch, B9 and vertical portfolio directories, plus the separate website-redesign work area.
- Twenty source documents indexed (R01–R20) with exact authorized repo-relative locators and explicit evidence types.
- One B9.1 ChatGPT conversation directly viewed, while many historical titles had only project-context excerpts, not fully retrieved transcripts. Links to private chats were deliberately **not** published.
- Historic cases include batch research and retries, false missing files from cross-repo lookup, independent Fred/Muse evaluation, QA tied to the artifact revision, timeout-related duplicate external objects, launch read-back rate limits, new category definitions, vertical portfolio run status and staged website handoff.

## Next assignment, Prompt 03

Reverse-engineer the existing Meta Ads Library research methodology in depth. Start from R02–R05 and R16–R18 in the source index, then inspect queues, result records, evidence grading, selection/scoring logic and individual research run templates.

Pay particular attention to:
- planned vs authorized vs running vs reviewed vs completed states;
- unreliable Ads Library access and `RETRY_REQUIRED` handling;
- exactly what counts as observed Meta evidence versus inference;
- how new research runs are spawned and tracked;
- QC gates that depend on actual artifact sets and versions;
- consistency between per-run `PROGRESS.md` and portfolio-level status.

Use sanitized process explanations, not internal account IDs or copied source evidence. Report gaps honestly. Commit the detailed analysis and update handoff.

## Guardrails

- No engine implementation and no premature PRD approval.
- No live Meta/GHL/website changes.
- No publishing of private conversation links or unsanitized data.
- Prompt 07 is still the human approval checkpoint for the enhanced PRD.
