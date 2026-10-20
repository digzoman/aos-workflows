# AOS-W Cross-Session Handoff — Prompt 13

Updated: 2026-10-20
Status: AOS-W 0.5.0 optional Git synchronization and provisional Git ref CAS; 90 local tests passed.
Repo: digzoman/aos-workflows public main. Inspect current HEAD and progress before changes.

## Required next reads
1. temp/OPERATING-RULES.md, temp/DESIGN-DECISIONS.md and temp/CONCEPT-NOTES-01B.md
2. temp/WORK-PLAN.md, temp/PROGRESS.md and this handoff
3. scaffold/aos-w/README.md, PROTOCOL.md, VERSION.json and agent-files/config/sync.json
4. scaffold/aos-w/references/GIT-SYNC-AND-COORDINATION.md
5. tools/git/coordination.py, cli.py, README.md, tests/test_git_coordination.py
6. temp/tests/PROMPT-13-GIT-COORDINATION.md, docs/specs/adrs/ADR-014-git-cas-provisional-selection.md
7. docs/specs/schemas/sync-config.schema.json, sync-state.schema.json, plus existing state/governance and test suites.

## Observed guarantees
- Git-free standalone mode unaffected; only agent-files normally writable after install.
- Optional Git mode supports remote readback and non-force agent-files-only commit/push; dirty/diverged or unknown ahead history is blocked rather than overwritten.
- Per-task remote ref CAS had exactly one winner in competing local clones sharing Git username/email. Token/epoch identifies separate logical agents; expiring a lease does not grant automatic takeover.
- Loss of network stops shared claims, verification and mutation; one-writer mirrored mode can keep bounded local work marked sync pending.
- Git LFS prototype is documented but actual binary/server unavailable. Hosted GitHub Git transport cannot resolve from this container. CAS is **provisional preference only**.
- No provider API fences, human identity authentication, cross-file atomic transactions, or live campaign changes.

## Next: Prompt 14
Produce self-contained downloadable package; test install/upgrade preserving user data, optional helpers, complete schemas and cold-start. Test live remote CAS/LFS separately in a suitably connected host before production claims. Keep no-runtime standalone mode and avoid public user data/secrets.
