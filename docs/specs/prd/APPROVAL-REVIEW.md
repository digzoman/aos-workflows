# Owner review checklist for PRD 1.0-rc1

**Current state: APPROVAL REQUEST NOT YET RESOLVED.** Prompt 07 creates/commits a draft PRD; it never self-approves or builds the engine.

## Executive review points

1. **Portability:** Is the intended product a plain-file, downloadable workflow standard, with optional stricter host integrations and no mandatory Git/runtime?
2. **Installation boundary:** Is only agent-files writable during normal use, including custom template skills, state, reviews, handoffs and Git sync metadata?
3. **V1 scope:** Do research, creative QA and a bounded safe Meta/CRM implementation handoff meet the intended "advertising implementation" objective? Does owner want live test-account integration for V1?
4. **Collaboration:** Is task-exclusive ownership required only when a tested adapter can enforce it, with advisory/manual single-agent mode otherwise?
5. **Lock study:** Confirm both LFS and atomic Git claims must actually be prototyped/tested before the winner is chosen.
6. **Quality/authority:** Confirm configurable autonomous execution with human approval for consequential actions by default, without treating QC as automatic publish permission.
7. **Recurrence and skills:** Confirm default one-off, overrideable scheduled templates with manual ad hoc launch, and step-local bundled/installed/pinned remote skills.
8. **Success criteria:** Confirm all six original V1 demonstrations and additional no-Git/scheduling/skill tests must pass.
9. **Research vs current truth:** The PRD uses historical Ampgent cases as design evidence, not as currently verified Meta/GHL delivery/performance.
10. **Public release:** Confirm sanitization and accept that license choice, live provider scope, and several technical defaults remain unresolved.

## What explicit approval should mean

Approval accepts product scope, architecture principles, constraints and test requirements **as documented**, while allowing Prompt 08 to choose schema syntax and optional adapter engineering details **within** those constraints. It should **not** be interpreted as:
- automatically accepting every proposed ADR without review;
- authorizing live Meta/HighLevel/website changes, spend, outreach or publication;
- asserting that shared locking, timed execution or image QA can be enforced by plain Markdown alone;
- deciding license or unresolved provider/locking capabilities without evidence.

## Suggested review outcomes

**APPROVE PRD**: Accept the product requirements and proceed to Prompt 08 architecture/schemas, with open decisions handled through the recorded escalation gates.

**APPROVE WITH SPECIFIC CHANGES**: List mandatory changes first; revise PRD and record owner confirmation before engine implementation.

**REQUEST REVISIONS**: Hold implementation, record the affected section and preferred outcome.

**REJECT OR DEFER**: Maintain research documents, no implementation work.

## Approval record to fill only after owner action

- Decision: **PENDING**
- Owner message and date: **PENDING**
- PRD version and exact Git commit: **PENDING**
- ADRs accepted/rejected/deferred: **PENDING**
- Authorizations: **none for production/external actions**
- Next permitted step: **owner review; Prompt 08 only after explicit approval**

Use PRD.md §23 for detailed open decisions and DECISION-REGISTER.md to distinguish approved requirements from research recommendations.
