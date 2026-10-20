# Workflow instances and active runs

**This directory includes one clearly labeled synthetic practice instance, `demo-local-research`, which has been created but has not executed any research tasks.** Create a new instance directory `<instance-id>/` when a user starts a workflow. Empty nested directories are not preserved by Git, so create them on demand.

Every new instance owns:

```text
<instance-id>/
  instance.json
  template-lock.json
  template-snapshots/<content-id>/template.yaml
  graph-revisions/g0001.yaml
  skills/                       # optional instance-local skills
  runs/<run-id>/
    run.json
    state.json
    events.jsonl
    checkpoints/
    tasks/<task-id>/attempts/
    claims/
    reviews/
    approvals/
    artifacts/
    skills/
    handoff.md
    handoff.json                 # optional structured companion
```

Only the immutable/pinned snapshot under the instance defines an **active** run, not the current `../../templates/` content.

The saved `events.jsonl` is the historical audit; `state.json` is the derived current view. A handoff is a readable guide, **not** the provider's or run event trail's substitute for truth.

Start/resume instructions: `../../references/START-A-RUN.md` and `../../PROTOCOL.md`.
