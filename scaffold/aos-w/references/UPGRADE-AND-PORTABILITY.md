# Installation, standalone transfer, and safe upgrades

## Install to a local or cloud workspace

The GitHub development repository holds the self-contained folder `scaffold/aos-w/`. If you use GitHub's whole-repository ZIP, extract it and copy **only** `scaffold/aos-w/` to your desired work folder. You do not need a Git checkout after copying. A release ZIP may be supplied separately; **do not assume GitHub's folder view itself is a one-click subfolder ZIP**.

A persistent cloud filesystem or mounted volume works the same way as local standalone. Verify that its data actually survives agent session termination; a temporary browser/cloud VM is not automatically persistent.

## Upgrade safely

**Never delete the installed aos-w folder and blindly reinstall**, because that could erase `agent-files/`.

1. Back up the **entire** installed `aos-w/` (including `agent-files/`) to a private safe location appropriate to data sensitivity.
2. Inspect the new distribution `VERSION.json` and its `spec/` compatibility notes.
3. Keep the old `agent-files/` unchanged. Replace only these standardized paths from the new release: `README.md`, `PROTOCOL.md`, `VERSION.json`, `templates/`, `spec/`, and `references/`.
4. Read any declared major schema migration notes before resuming. Do not change a run's pinned template or graph version merely because the master changed.
5. Verify existing run `events.jsonl`, `state.json`, `template-lock.json`, old pinned graph snapshots and artifact references; if incompatible, pause the run and record a migration proposal.
6. For Git-mirrored work, ensure user-private data is not accidentally copied/pushed into a public repository; remote sync remains optional.
7. Only after checking backups and sample cold-start recovery should the agent resume existing runs.

An automated updater is **not implemented** in scaffold 0.1.0. This procedure is an explicit human/agent-managed file replacement.

## Move active workflows

Copy the complete `agent-files/instances/<instance-id>/` tree, plus required `agent-files/config/` metadata (without secrets), to the target persistent `aos-w` installation. Confirm compatible framework/schema version. Validate template snapshots and artifact locators. Optional Git sync must be reconfigured and reconciled with the **new** remote, never assumed to be identical. AOS-W itself does not upload or transfer files automatically.

## Safety and data ownership

The public repository has sanitized examples. User data in local `agent-files/` may contain sensitive material and must not be pushed to public Git. All backups are the user's responsibility, and a Git commit/release is never evidence that a provider-side action completed.

## 0.6.0 release ZIP (clean starter)

AOS-W now includes an optional **allowlisted** distribution builder and a dedicated, clean standalone ZIP. Its `agent-files/` contains only nonsecret default configuration and directory READMEs/empty directories. The public development repository's synthetic `demo-local-research` instance and example user overlay are **intentionally excluded** from releases; a new installation starts without any claimed work. For real user upgrades, **do not extract directly over an existing folder**—retain all existing `agent-files/` bytes, check schema major compatibility and keep a rollback backup. The optional maintainer `scripts/aosw-distribution.py install|upgrade` performs a staged local replacement; ordinary file-only agents follow the manual procedure here and in `INSTALL.md`.
