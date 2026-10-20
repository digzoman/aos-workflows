# Chronological Project History

## 2026-10-20. Prompt 01, initialization

- Confirmed requested repository name `digzoman/aos-workflows` and explicitly public visibility.
- Created GitHub repository and initial documentation.
- Set up tracked `temp/` workspace for plans, requirements, research, open questions, progress, and durable cross-session handoff.
- Defined the portable scaffold path and initially reserved `agent-files` as the only runtime-modifiable subtree.
- No engine, lock, Git synchronization, or operational workflow functionality implemented.
- Next task is research indexing, Prompt 02.

## 2026-10-20. Prompt 01b, requirements amendment

- User added non-repeating versus recurring workflows. Default is one-off; reusable templates can declare an overridable schedule and can still launch ad hoc.
- User added skills stored inside templates and workflow instances and referenced at the relevant step. Skills may also point to installed or repository-hosted skill packages.
- Recorded compatibility with no mandatory scheduler, Git, or agent daemon. Trigger execution infrastructure and detailed schema remain unresolved.
- Updated design baseline, scaffold documentation, work plan, open questions, progress, and handoff.
- No scheduling service, workflow engine, or skill resolver implemented. Next step still Prompt 02.

Future sessions should append substantive events with changed files, test evidence, commit references, and failures. Avoid copying raw private logs.
