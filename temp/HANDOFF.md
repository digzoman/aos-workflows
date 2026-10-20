# AOS-W Cross-Session Handoff — Prompt 14

Updated: 2026-10-20
Status: **0.6.0 portable distribution tools committed; 108/108 local conformance tests PASS.** GitHub Actions 39415147383 SUCCESS and v0.6.0-portable-preview ZIP published and verified.
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
- Verified Actions run 39415147383 SUCCESS, artifact ID 12261710573 available, prerelease v0.6.0-portable-preview with SHA256 digest independently matched; permanent release asset link below.
- Does not authenticate human reviews/permissions, enforce provider-side fencing or run unattended work.

## Next prompt 15

Create sanitized actual Ampgent-style workflow master templates, protecting owner boundaries and preserving all file-only operation. Do not touch live advertising/CRM accounts. Use evidence-indexed research templates as basis. Commit outputs and updated progress/handoff.

## Reserved follow-ups

Real hosted GitHub CAS races and Git LFS server lock competition remain Prompt 17 tasks; ZIP installation on varied cloud filesystems still needs broader release test coverage.

## Hosted verified distribution download

- GitHub release: https://github.com/digzoman/aos-workflows/releases/download/v0.6.0-portable-preview/aos-w-portable-0.6.0.zip
- SHA-256: `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`
- Hosted workflow: https://github.com/digzoman/aos-workflows/actions/runs/39415147383 (SUCCESS, 108 tests)
- Release ZIP: 97,648 bytes, 63 manifest entries, 20 schemas, clean agent-files; installed, initialized and upgraded independently after download.
- Failed first run 39414897602 was corrected by mocking absence of Git LFS rather than assuming host environment. No live Git LFS lock server test was performed.
