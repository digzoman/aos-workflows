# Prompt 01b. Recurring Workflows and Just-in-Time Skills

Added 2026-10-20. **Design-only concepts. No engine, scheduler, schema, skills loader or runtime code exists yet.**

## 1. User-confirmed requirements

### Repeating versus non-repeating workflows

- Normal workflows are non-repeating by default and are started as needed.
- A default or customized template may contain an optional schedule that can be changed.
- A scheduled-capable template can also be instantiated manually on an ad hoc basis.
- This is a useful building block for recurring tasks, independent of whether one or several agents operate the workflow.

### Skills contained in or referenced by workflow packages

- Templates and actual workflow instances must be able to **contain** their own skills or skill information, instead of only relying on a global skill collection.
- Individual workflow steps refer to the relevant skill(s) and their location.
- Locations can be inside the template, inside that workflow instance, already installed locally, or in a repository.
- Agents should receive or retrieve the relevant skill information at the point in the workflow where it is needed.

## 2. Proposed design interpretation, subject to PRD/architecture approval

### Execution triggers versus workflow runs

One-off and recurring are **trigger policies**, distinct from the DAG steps inside a single execution. A single template could be used for either a scheduled occurrence or an ad hoc launch. Consider giving each recurring occurrence its own run ID, history, state, approval and checkpoint records so retries and duplicate triggers do not silently duplicate external actions.

No AOS-W background process is mandatory. When no host scheduler is configured, declarative schedules can be stored and recognized as due when an agent next checks; they do **not** autonomously start anything. A host app or optional integration may provide real timed launch, subject to authority rules.

Future scheduling spec needs timezone, daylight-saving changes, recurrence expression, start/end bounds, missed-event handling, overlap restrictions, deduplication keys, changes to active schedules, and separate policies for runs and retries.

### Skills packaged within templates and instances

Illustrative *layout only*, not a finalized or implemented schema:

```text
scaffold/aos-w/
  templates/
    competitor-research/
      workflow.yaml
      skills/
        ad-library-method/
          SKILL.md
  agent-files/
    custom-templates/
      dental-research/
        workflow.yaml
        skills/
          dental-ad-rules/
            SKILL.md
    workflows/
      example-workflow/
        workflow.yaml
        skills/
          custom-evaluator/
            SKILL.md
    runs/
      example-run/
        state.json
        skills/
          run-specific-guidance/
            SKILL.md
```

A step would name its required skills and a resolvable source locator; the agent consults the content **just in time** before taking that step. Support references to installed skills, local relative paths, and Git repository URLs/refs if supported by its environment. Prefer an explicit pinned version/revision for externally referenced skills to preserve reproducibility.

Unresolved: exact folder vocabulary (`workflows/` vs `runs/`), skill manifest schema, local or remote priority, how to pin or snapshot a skill into an active run, offline availability and fallback, and safe skill source verification. Skills are **capabilities and instructions, not permissions**; no external skill may automatically expand agent or project authority.

## 3. Required upcoming research and acceptance coverage

- Prompt 06 must examine recurring workflow scheduling, trigger adapters without mandatory daemons, and existing skill conventions including Agent Skills and A Rep.
- Prompt 07 PRD must define expected behavior and unresolved execution guarantees.
- Prompt 08 technical spec must formalize the trigger policy and skill locator/bundle contracts.
- Prompts 09–15 should implement the selected contracts only after approval.
- Prompt 16 tests should exercise ad hoc launches from a recurring-capable template, non-repeating default behavior, bundled skills and missing external skills.
- Prompt 17 tests should cover distinct schedule occurrence identity and safe shared coordination where capabilities exist.

No live scheduling task or automated job has been created in Prompt 01b.
