# Practice handoff: demo-local-research / run-001

**State:** CREATED. A **synthetic sample instance was initialized only**. No workflow task has run, no source evidence was collected, no review passed and no remote action occurred.

**Pinned template:** `research-starter` 0.1.0 in `graph-revisions/g0001.yaml`, snapshot in `template-snapshots/master-v0-1-0/`. The source Git blob digest is recorded in `template-lock.json`; manual agents should label their own hash verification appropriately.

**Events:** `events.jsonl` seq 1–2, initial checkpoint `checkpoint-0001`. Snapshot `state.json` seq 2, integrity advisory. Neither event claims completion.

**Ready next:** `define-scope` only. Review `run.json`, owner scope, actual storage persistence and source files before writing `artifacts/scope.md`. The remaining nodes wait for dependencies; `collect-evidence` then uses the bundled evidence-handling skill just in time. 

**Approval:** local sample read/write only. No Meta, CRM, Git sync, messaging, scheduling or publishing authority.

**Safe resume:** use actual current actor `[Agent | Platform | Role | Instance]`, append new events with seq >=3 after work, refresh state/checkpoint and handoff; never imply an existing sample event is the current agent's action.
