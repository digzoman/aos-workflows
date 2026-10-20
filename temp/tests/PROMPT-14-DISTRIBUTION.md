# Prompt 14 — optional distribution, installation and upgrade conformance

**Date:** October 20, 2026. **Scope:** optional maintainer Python stdlib distribution/quickstart tools, local file fixtures and existing local Git-only earlier tests. This is *not* verification of hosted cloud storage atomicity, GitHub release publishing, live Meta/GHL action permission or a live scheduler.

## Actual local tests performed

- **18/18** new distribution/quickstart tests passed using a temporary synthetic scaffold, including ZIP build/manifest verification, deterministic ZIP content, no private customer or custom/user config leakage, arbitrary-directory extraction, clean install, byte-for-byte `agent-files/` upgrade preservation, symlink/zip-slip/duplicate/unauthorized-path rejection, major schema mismatch block, an initialized local run with pinned graph, and recovery/status disagreement detection.
- **108/108** local combined tests passed (18 new + 90 existing: 15 Git, 38 governance, 26 state/recovery, 11 composition). No external providers contacted.
- Created an instance using the real prior `research-starter` YAML and reopened it with the existing Prompt 11 `RunStore.verified()` SHA256 event validator. Run stayed **CREATED**, first task eligible and no task executed, no provider calls.
- In upgrade fixture test, all user-owned filenames, SHA256 hashes and bytes—including a saved run event log, custom template and user sync settings—remained unchanged after protected files were updated. A rollback backup folder was retained.
- Tests included rejecting an archive altered without manifest update and rejecting intentional private files in user data, malicious `../` entry, duplicate case-insensitive path, schema-major drift and symlinked user data.

## Distribution contents and confidentiality

Builder includes the **protected** README/PROTOCOL/VERSION, spec/schema documents, reference guides, master YAML templates, bundled Agent Skills and **clean** `agent-files` seed config/readmes/empty directories. A SHA256 JSON manifest lists all installed files. It explicitly excludes development-only `docs`, `examples`, `tools`, `scripts`, `tests`, `temp`, `.git`, the public repo's simulated practice instance and any custom user-created data. The ZIP contains no executable runtime tool and does not require Git/Python.

## Hosted workflow / release artifact

A GitHub Actions conformance+package workflow is provided under `.github/workflows/aosw-portable.yml`. It runs the full local suite, builds `dist/aos-w-portable-0.6.0.zip` from the **actual complete repository tree**, verifies the manifest, installs into an arbitrary directory, creates a new run using optional PyYAML and demonstrates upgrade preserving its artifact. Then it uploads the ZIP as an Actions artifact. Its actual hosted job result and artifact availability must be checked **after commit**. An authored workflow is not proof it ran; do not claim a release ZIP exists on GitHub unless that job succeeds and the artifact is confirmed.

## Known limits

- The test packager itself requires optional Python; the downloaded AOS-W folder does not.
- The `aosw-ops.py status` helper is intentionally **advisory** (checks event sequence, not full journal SHA, permissions or provider truth); use optional state `RunStore.verified()` for hash verification.
- Existing manual installation/upgrade instructions are necessary if no helper is available. Manual operations do not provide OS-enforced write protection.
- Upgrades stage a directory and use local rename, not crash-atomic transaction across arbitrary remote/cloud storage.
- Action artifact retention is limited and GitHub Release asset publication requires a separate verified release process.
- End-to-end real cross-platform handoff, hosted shared CAS collision and live Git LFS server tests still pending Prompts 16–17.

## Verified GitHub-hosted distribution — 2026-10-20

- Initial run 39414897602 failed in a legacy environment-dependent Git LFS test: it assumed git-lfs was not installed. GitHub Actions runner **does** have git-lfs; the optional test was corrected to use a simulated unavailable client and committed separately (no server lock claims).
- Successful rerun: [Actions run 39415147383](https://github.com/digzoman/aos-workflows/actions/runs/39415147383), head `558bcc7433188fe8fec830bd26c3c86a28103da2`, **completed SUCCESS**.
- Hosted suite **108 tests PASS**; full-repository independent ZIP build and manifest verification PASSED; install in arbitrary folder, new `research-starter` instance and upgrade preserving `agent-files` artifact PASSED.
- Actions artifact ID **12261710573** (archive containing the standalone ZIP), nonexpired at verification; permanent preview release **v0.6.0-portable-preview** published with `aos-w-portable-0.6.0.zip`.
- [Download release asset](https://github.com/digzoman/aos-workflows/releases/download/v0.6.0-portable-preview/aos-w-portable-0.6.0.zip) — 97,648 bytes. GitHub release API reports SHA-256 **`7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`**.
- Downloaded actual Actions artifact to a separate local container, extracted its inner ZIP, and verified: matching GitHub release digest; v0.6.0; **63 manifest file entries**, 20 draft schemas, bundled install guide, and clean user directory without any instance/custom data except directory READMEs.
- Independently ran the **actual hosted ZIP** through the optional verifier, installed it into an arbitrary nested folder, initialized a real pinned one-off sample, checked next task `define-scope` and zero completed actions, upgraded that installation, and confirmed an added user artifact was **preserved byte-for-byte**, with a rollback backup folder present.
- This proves this ZIP builds, extracts, initializes and upgrades on the tested hosts. It **does not** prove crash atomicity on arbitrary cloud filesystems, authentication of action approvals, unattended workflow execution or production shared coordination.
