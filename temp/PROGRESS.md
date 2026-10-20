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
- `.github/workflows/aosw-portable.yml`: authored hosted test/package workflow, uploading independent `aos-w-portable-0.6.0.zip` Actions artifact and attempting best-effort preview release asset. GitHub Actions run 39415147383 completed SUCCESS; artifact and SHA256-verified prerelease asset were independently downloaded and tested.
- Clean ZIP excludes all dev tools/tests/temp/docs/examples and **all active/user private agent-files** (including public repo synthetic practice sample and custom overlay); installs default config and empty instance/custom folders.

## Locally executed tests

- **18 new local distribution/initialization/upgrade tests PASS** with synthetic scaffold files, manifest integrity, arbitrary extraction, preservation of all user bytes, corrupt/malicious ZIP cases and new instance status.
- **108/108 combined tests PASS** with all 90 existing regression cases in local container.
- Additionally initialized from actual preexisting `research-starter` 0.2 YAML, resumed with existing `RunStore.verified()`, confirmed event digest and first eligible task, with zero executed tasks.
- GitHub Actions run 39415147383 completed SUCCESS: full repository packaged, 108 hosted tests PASSED, installed and upgraded. Preview asset SHA256 matches independently downloaded ZIP.

## Remaining limitations

- No background workflow engine, scheduler, authenticated owner approval or live provider integration.
- Hosted CAS/LFS live coordination still untested; Git default disabled.
- Manual agent-file-only operation remains core. Optional tooling does not provide hard OS permissions on arbitrary host.
- GitHub preview release v0.6.0-portable-preview is published and verified, including 97,648-byte ZIP and matching SHA256; temporary Actions artifact also present.

## Next action

Hosted release verification COMPLETE. Next Prompt 15 sanitized Ampgent templates; broader cloud/filesystem, hosted Git CAS/LFS and cross-platform tests remain future work. Prompt 15 adds sanitized Ampgent templates; Prompt 16–17 will stress portability/cross-platform and hosted coordination tests.

### Confirmed release

[Download AOS-W v0.6.0 standalone ZIP](https://github.com/digzoman/aos-workflows/releases/download/v0.6.0-portable-preview/aos-w-portable-0.6.0.zip), SHA256 `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`, GitHub Actions [successful run](https://github.com/digzoman/aos-workflows/actions/runs/39415147383). Actual ZIP verified and installed/upgraded in local independent retest after hosted workflow passed.
