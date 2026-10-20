# Prompt 16: practical standalone acceptance (not just static code inspection)

This optional local harness runs a **real extracted AOS-W ZIP** against local filesystem workflows. It uses a small fictional, offline research source fixture to avoid relying on third-party services or making unverifiable advertiser claims.

## Reproduce

From the development repository root, on a host with Python 3 and the optional PyYAML package:

```sh
python tests/acceptance/run_standalone_acceptance.py \
  --zip /path/to/aos-w-portable-0.6.0.zip \
  --evidence /tmp/aosw-p16-acceptance
```

The test deliberately leaves the extracted work directory and all per-run files in the chosen evidence folder. **Use a fresh/empty evidence folder** for every new run. The installed `aos-w/` contains no `.git` and no dependency scripts. The test harness imports optional developer helpers from `tools/state/` and `scripts/aosw-ops.py` located *outside* the installation. It does not run a server, scheduler, browser, or provider integration.

`resume_agent.py` runs in a **separate OS process** with only installed folder, run/instance IDs and persisted evidence. It reads the pinned graph, handoff, skill and current event chain, recognizes an interrupted running task, saves correction/restart events, performs actual offline evidence collection and QC, and completes the workflow. It has no access to previous conversation text or the calling Python process's variables. This is **not** a real second vendor AI harness (that is Prompt 17).

The suite covers 13 passing local cases and one explicitly **NOT_RUN** case for a separate persistent cloud filesystem. The cloud test must be performed on a genuinely separate persisted cloud volume, not merely another directory on the local CI runner.

## Evidence and reproducibility

- `../../docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md` — detailed expected vs actual, evidence mapping, known limits.
- `evidence/acceptance-results.json` — machine-readable real execution outcomes.
- `evidence/offline-research/` — sanitized event chain, final state, scope, fictional source inputs, evidence log and reviewed summary.
- `evidence/custom-instance/` — append-only retry/revision history and both immutable graph versions.
- `evidence/recovery/` and `evidence/cancellation/` — corruption recovery and cancellation event trails.
- `evidence/protected-baseline.json` — SHA-256 protected file integrity before/after normal execution.

**No live Meta/CRM/website actions were performed.** The owner approval used for graph revision is deliberately mocked; it is not authenticated. File-based AOS-W remains manual and cooperative without hard OS security or production distributed claims.

## Initial test correction

The first draft of this test incorrectly expected skill-dependent `collect-evidence` to appear on the *unconditionally READY* list. The implementation correctly required a separate skill/context check. The test was fixed and all 13 local cases re-executed successfully; no framework defect was found in that specific check.
