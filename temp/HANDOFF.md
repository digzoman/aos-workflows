# AOS-W Cross-Session Handoff — Prompt 14

Updated: 2026-10-20
Status: **0.6.0 portable distribution tools committed; 108/108 local conformance tests PASS.** Hosted artifact status requires post-commit verification.
Repository: public digzoman/aos-workflows, main. Check exact HEAD and recent Actions run before changes.

## Mandatory opening reads

1. `temp/OPERATING-RULES.md`, `temp/DESIGN-DECISIONS.md`, `temp/CONCEPT-NOTES-01B.md`
2. `temp/WORK-PLAN.md`, `temp/PROGRESS.md`, this handoff
3. `scaffold/aos-w/README.md`, `PROTOCOL.md`, `VERSION.json`
4. `scaffold/aos-w/references/INSTALL.md`, `UPGRADE-AND-PORTABILITY.md`
5. `docs/installation/QUICKSTART.md`
6. `scripts/aosw-distribution.py`, `scripts/aosw-ops.py`, `scripts/package-scaffold.sh`
7. `tests/test_distribution.py`, `temp/tests/PROMPT-14-DISTRIBUTION.md`
8. `.github/workflows/aosw-portable.yml`
9. Prior Prompt 10–13 helper/tests/manual references, particularly governance and current publisher/source permissions.

## What is actually implemented

- Portable standalone `scaffold/aos-w/` manual core requiring no Git, Python, Node, MCP or database.
- Optional clean ZIP builder/verify/install/upgrade: format `aos-w-standalone-zip-v1`, a self-contained ZIP rooted at `aos-w/`, SHA256 integrity manifest, only standardized protected framework and nonsecret starter agent-files config. **No generated user work** included.
- Fresh installs create an empty user-workspace instances area. Existing installs upgraded with `agent-files/` kept unchanged, rollback backup retained; no automatic major-schema migration.
- Optional developer Python quickstarter lists templates/instances, creates a pinned/manual CREATED run and emits initial event/handoff; status is advisory and never grants permission.
- Optional GitHub Actions workflow builds full repo versioned ZIP, runs complete regressions and install/init/upgrade smoke, uploads Actions artifact and tries a separately observable prerelease asset.
- Old repo's synthetic demonstration remains present in **development** agent-files but is intentionally excluded from standalone clean release.

## Validation evidence and limits

- 18 new + 90 old = **108 local tests passed**, including ZIP privacy/safety, upgrade preservation and task initialization. Tested on synthetic local ZIP; the full public repository artifact is tested in hosted workflow, not presumed from code alone.
- The quickstarter was separately tested with real prior research-starter YAML and Prompt 11 RunStore verifying event prefix.
- No shell script is mandatory for *using* the ZIP. Builder itself requires optional Python, only in development host.
- Need to verify Actions run, artifact ID and prerelease before giving users an actual asset link. Actions may be unavailable, and artifact retention limited.
- Does not authenticate human reviews/permissions, enforce provider-side fencing or run unattended work.

## Next prompt 15

Create sanitized actual Ampgent-style workflow master templates, protecting owner boundaries and preserving all file-only operation. Do not touch live advertising/CRM accounts. Use evidence-indexed research templates as basis. Commit outputs and updated progress/handoff.

## Reserved follow-ups

Real hosted GitHub CAS races and Git LFS server lock competition remain Prompt 17 tasks; ZIP installation on varied cloud filesystems still needs broader release test coverage.
