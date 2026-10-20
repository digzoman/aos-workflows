# Optional persistent state helper — AOS-W 0.3.0

`state.py` is an opt-in local-only implementation of the [portable state protocol](../../scaffold/aos-w/references/STATE-AND-RECOVERY.md). It uses Python's standard library for JSON events, SHA-256, fsync and local snapshot replacement; pinned YAML revisions require **optional PyYAML**. It is **not** part of the minimum downloaded `scaffold/aos-w/` runtime. A capable agent can follow the protocol manually using ordinary files without Python, Git or a service.

## CLI

```sh
# Developer optional environment with PyYAML installed:
python tools/state/cli.py /path/to/aos-w/agent-files/instances/fixture/runs/run-001 inspect
python tools/state/cli.py /path/to/.../runs/run-001 checkpoint --actor '{"agent":"demo","platform":"local","role":"worker","instance":"session-1"}'
python tools/state/cli.py /path/to/.../runs/run-001 recover --actor '{...}'
# Corrupt JSONL recovery only after explicit operator decision:
python tools/state/cli.py /path/to/.../runs/run-001 recover --actor '{...}' --repair-tail
```

Other `cli.py --help` actions include task-start, task-complete with declared SHA-256 output references, task-fail/retry, task-unblock, review-submit/pass/revise, run/task pause/resume/cancel, op-intent/ack/reconcile, and authorized graph-revise. `--actor` and payloads can be JSON literals or local JSON file paths. The optional helper performs **no provider requests**, no Git operations, no scheduled work, and no independent authentication. `op-intent` only saves a record after the caller verifies real authority elsewhere.

## Guarantees and limitations

- Event JSONL is append-oriented with monotonically increasing seq and SHA-256 predecessor digest. Snapshot is a derived cache; events are audit history. A legacy 0.1 or 0.2 event without a digest can be replayed but stays **ADVISORY**.
- A completed output requires the declared file under the run root and matching exact SHA-256. Changed/missing evidence blocks current progress and keeps historical events.
- `checkpoint()` writes a snapshot of a verified event prefix then adds a `checkpoint_created` event; interrupted/orphan files are flagged rather than trusted.
- `recover()` quarantines suspect tails **only when explicitly requested**. Stale state and run revision pointers are backed up, then restored from the validated event/graph source.
- Retry is bounded and requires correction acknowledgement for review/incomplete evidence; fixed/exponential backoff timestamps are checked **on invocation**, not background timers.
- Operation intent must precede `operation_submitted`. Ambiguous result blocks duplicates until a supplied readback reference is recorded; only verified NOT_APPLIED outcomes may be explicitly retried with a new key and prior-operation reference; no API is actually contacted, and provided metadata does not prove external truth.
- Graph revision application creates a new immutable file under the instance, checks a scoped approval record **cooperatively**, appends a new version event and preserves prior history. Cryptographic human identity / real permission enforcement remain future work.
- Fsync/replace improve local robustness only on compatible filesystems. They do not establish an atomic transaction across multiple files or Git replicas. **One writer at a time**; no distributed locks.

## Test scope

Run `python -m unittest discover -s tests -p 'test_state.py' -v` from the development repository root. Tests are synthetic/local-only and require PyYAML; no real business/provider data. See `temp/tests/PROMPT-11-STATE-CONFORMANCE.md` for tested cases and limitations.
