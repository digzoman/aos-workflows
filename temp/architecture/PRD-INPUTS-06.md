# Prompt 06 requirements and design questions for Prompt 07 enhanced PRD

**Priority source** is user-selected `temp/DESIGN-DECISIONS.md`. This file is analyst recommendations only. See [ALTERNATIVES-COMPARISON.md](ALTERNATIVES-COMPARISON.md) and the eight [draft ADRs](adrs/README.md).

## Must retain from user decisions

- Public `digzoman/aos-workflows`, downloadable `scaffold/aos-w/`, all ordinary runtime changes only inside `agent-files/`; Git optional.
- Same reusable YAML/Markdown graph supported local and cloud, single-agent and multi-agent, manual ad hoc or optionally scheduled.
- Reusable child templates, conditional steps, parallel *when supported*, independent QC, dynamic generation and merge.
- Agent-provenance convention, version-bound review and permission, no QC implied external authorization.
- Skills bundled in master/custom templates and individual workflow runs, or pinned reference to installed/repo skills, loaded when needed.
- Prototype and **empirically compare** LFS and Git CAS claims, same credential, crash/lease/network conditions, before selecting.
- Before implementation, review human-approved PRD and test plan.

## Recommended smallest schema design tasks for Prompt 08

1. Manifest version, template version and immutable run revision identity; no hardcoded Git assumption.
2. Task node identity, stable dependency edges, predicate expression with UNKNOWN state, output and quality expectations.
3. Generated child-run proposal/authorization and parent-child merge contract.
4. Per-task lifecycle and separate domain outcome, approval, reviewer and evidence confidence.
5. Canonical state JSON, append-only logical events JSONL, human Markdown handoff, hash/revision, torn-write handling.
6. Optional capability registry for storage durability, actual file atomics, Git mirror, exclusive task lock, host scheduler and external connectors.
7. Lock lease/fencing epoch, owner identity and output revision acceptance, with conservative offline behavior.
8. Scheduled occurrence identity, IANA timezone, DST, missed and overlap policy, deduplication.
9. Skill ref/manifest, trust precedence, pin/hash, offline fallback and script/privilege boundaries.
10. Provider operation idempotency and read-before-retry, actual configured/effective/business outcome differences.
11. Explicit approval scope and preconditions for account writes, live spend and production deployment.
12. Observable verification test contract: declared LIVE / MOCKED / MANUAL / NOT RUN, not unsupported PASS.

## Decisions still open for user acceptance

- Details of YAML expression language and risk of executable arbitrary conditions.
- What exactly is required in the minimum file-only one-agent installer.
- Where exactly within `agent-files/` run/instance/custom template folders live and how versions are upgraded.
- Whether a remote Git CAS claim adapter is the first shared backend after test or whether another mechanism is needed; feasibility in GitHub connectors that do **not** expose an expected-old SHA.
- Whether human-reviewed acceptance of reduced coverage permits proceeding through some QA gates, and default gates for consequential marketing.
- Scheduled recurrence format and overlap/missed/DST policies, with no mandatory always-on host.
- Skill source priority on conflicts and separate authorization for untrusted executable scripts.
- Exact boundary of A Rep issue vs AOS-W graph/plan when both are installed.
- Repository license remains **undecided**; public visibility does not grant an open-source license.
- No additional design change automatically overrides a user-approved baseline; resolve only in Prompt 07 review.

## Acceptance test traceability

The preapproved six V1 demonstrations remain: a real bounded Ampgent workflow; cross-platform resume; exclusive double-claim rejection in tested coordination mode; failed QC blocks then correction passes; mid-run revision preserving completed history; clone/move to new Git repo and resume. Add explicit standalone no Git test and scheduled/manual skill tests from Prompt 01b. Include negative tests for offline shared claims and stale permission.

**Do not present Promise of exactly-once side effects, crash-atomic writes, enforced reviewer independence or automation while host is off** unless actual executor/adapter has been tested to supply it.
