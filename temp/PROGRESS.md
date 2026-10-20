# AOS-W Development Progress

Date: 2026-10-20
Phase: **Prompt 14 portable distribution and optional helpers — IMPLEMENTED / local tests PASS**
Framework: **0.6.0** portable Markdown/YAML/JSON manual core; optional host tools separate.
Next: Prompt 15, sanitized Ampgent marketing workflow modules, pending distribution-hosted verification details.

## Prior foundation

- Prompts 01–08: decisions, research, enhanced PRD and technical file/state/QC/Git architecture.
- Prompt 09: protected downloadable scaffold, writable agent-files.
- Prompt 10: reusable templates/compound graph rules, optional composition helper; 11 tests.
- Prompt 11: append-oriented event ledger, recovery/checkpoints/retries; 26 tests.
- Prompt 12: identity, advisory claims, reviews, permissions and remediation; 38 tests.
- Prompt 13: optional Git sync and local bare-ref CAS experiments; 15 tests, production claim backend still provisional.

## Prompt 14 deliverables

- `scripts/aosw-distribution.py`: Python **stdlib-only, optional maintainer** ZIP builder/manifest verifier/clean installer/safe upgrade. Whitelists protected readmes/templates/reference/schema files and **only** nonsecret config/readme seeds from agent-files. Rejects ZIP traversal, case collisions, symlinks, mismatched hashes, size excess and unintended source paths. SHA256 file manifest; deterministic archive bytes.
- Upgrade stages protected files, copies the **entire existing agent-files subtree byte-for-byte**, uses same-parent filesystem renames with rollback recovery on supported hosts and retains previous installation as sibling backup; unknown schema major blocked. Not a distributed transaction and not guaranteed crash atomic on cloud/NFS.
- `scripts/aosw-ops.py`: optional list/status (status explicitly advisory, not permission), new one-off workflow init from pinned master YAML (PyYAML only for init) using four-field actor, immutable template snapshot/graph, CREATED run, SHA256 genesis event, state and handoff. No task/provider executions.
- `scripts/package-scaffold.sh` now delegates to safe builder instead of recursively zipping possibly private agent-files data. `scripts/validate-scaffold.mjs` updated to 0.6.0 and handles clean ZIP without the repository's synthetic demo.
- `scaffold/aos-w/references/INSTALL.md` and `docs/installation/QUICKSTART.md` provide manually executable, **no Python/Git required** directions.
- `.github/workflows/aosw-portable.yml`: authored hosted test/package workflow, uploading independent `aos-w-portable-0.6.0.zip` Actions artifact and attempting best-effort preview release asset. Actual run/asset status must be verified separately before promising link.
- Clean ZIP excludes all dev tools/tests/temp/docs/examples and **all active/user private agent-files** (including public repo synthetic practice sample and custom overlay); installs default config and empty instance/custom folders.

## Locally executed tests

- **18 new local distribution/initialization/upgrade tests PASS** with synthetic scaffold files, manifest integrity, arbitrary extraction, preservation of all user bytes, corrupt/malicious ZIP cases and new instance status.
- **108/108 combined tests PASS** with all 90 existing regression cases in local container.
- Additionally initialized from actual preexisting `research-starter` 0.2 YAML, resumed with existing `RunStore.verified()`, confirmed event digest and first eligible task, with zero executed tasks.
- Real GitHub Actions run to package complete repository is distinct from local tests and needs independent readback after commit; no run result claimed yet.

## Remaining limitations

- No background workflow engine, scheduler, authenticated owner approval or live provider integration.
- Hosted CAS/LFS live coordination still untested; Git default disabled.
- Manual agent-file-only operation remains core. Optional tooling does not provide hard OS permissions on arbitrary host.
- Action artifact may expire; publication of persistent prerelease needs actual GitHub permission/verification.

## Next action

Verify published commit, Actions workflow run/artifact and any prerelease asset. If hosted job fails, record blocker/fix separately without claiming a release. Prompt 15 adds sanitized Ampgent templates; Prompt 16–17 will stress portability/cross-platform and hosted coordination tests.
