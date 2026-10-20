# Optional Git synchronization and claim prototypes (AOS-W 0.5.0)

**Requires Git only when this optional mode is selected.** The standalone `scaffold/aos-w/` folder remains agent-readable and writable under `agent-files/` without Git, Python, remote, scheduler or coordinator. This helper adds **no provider authorization**, multi-file atomic transactions or automatic agent execution.

## Supported modes

| Mode | Git required? | Ownership | Behavior during disconnection |
| --- | --- | --- | --- |
| `standalone_single_writer` | No | One cooperating agent, advisory claims | Normal local work continues, no remote promises |
| `git_mirrored_single_writer` | Yes | Still one writer, remote sync verified | Local drafts/checkpoints may proceed, mark `sync_pending`; no claim of push success |
| `shared_coordinated` | Yes, verified reachable remote | Per-task explicit ref-CAS claim | **Stop shared mutations/claims/provider effects**; read-only analysis may continue with stale-data warning |

## Claim CAS operations (developer/host-optional)

`coordination.py` stores one claim per **dedicated remote Git branch ref**:

`refs/heads/aosw-claims/<run-id>/<task-id>`.

Each ref tip points to an immutable Git commit containing `claim.json`, including **[Agent | Platform | Role | Instance]**, logical owner, unique token, monotonic fence epoch, claim status, UTC timestamps, lease and prior ref. Claim updates use:

`git push --force-with-lease=refs/heads/aosw-claims/<run>/<task>:<explicit-old-sha> origin <new-commit>:refs/heads/aosw-claims/<run>/<task>`

On initial creation `<explicit-old-sha>` is empty, requiring **ref absence**. A stale or competing old SHA fails; the loser must refresh and stop, never force-update. Git commits are created without switching the user's current branch and are not ordinary AOS-W workflow files. Every push is read back by `ls-remote`. No remote connectivity means claim verification is **unavailable**.

Caveats: Git branch protections, hosting policies, remote branch creation quotas, stale clock, active owner crash, and different Git host compatibility must be tested **on the real chosen host**. CAS protects the **single Git claim ref**, not arbitrary files or external systems. Provider side effects still need explicit authority, idempotency, reconciliation and ideally provider-enforced fencing. **Do not treat a lease expiry as automatic right to take over.** Reclaim requires explicit reviewed rationale, remote availability and a successful new CAS epoch. The worker that lost the claim must stop on re-verification.

## Local sync protocol

Before session/start/resume: read `agent-files/config/sync.json`, verify Git checkout, actual remote `ls-remote`, then `git fetch`. If behind and clean, a fast-forward refresh is allowed; if divergent or dirty, preserve edits and stop—**never reset --hard, auto-merge, or force-push**. Check remote before shared claims and before any owned mutation. After a completed task, checkpoint/handoff first, then commit **only explicitly selected paths under `scaffold/aos-w/agent-files/`** and push normally. Verify the remote branch SHA. Include `Agent-Provenance: [Agent | Platform | Role | Instance]` trailer; Git account identity is a separate authentication notion.

When online in shared mode: acquire CAS claim, check returned ref token/epoch, verify again immediately before consequential changes, commit/push appropriately, then release by a new CAS update. Re-read remote on any ambiguous push ACK. CAS claim does not bypass QC, host authorization or P11 provider-operation idempotency.

When offline: stand-alone is unaffected; mirrored single writer may checkpoint locally but reports `sync_pending`; **shared mode is fail-closed** for task ownership, shared writes and external effects. Do not use a cached ref or a local `.lock` file as proof of current exclusive ownership.

## CLI (developer tool, Python standard library and Git)

```sh
python tools/git/cli.py --repo /path/to/repo sync-status
python tools/git/cli.py --repo /path/to/repo sync-refresh
python tools/git/cli.py --repo /path/to/repo claim-status --run run-001 --task research-a
python tools/git/cli.py --repo /path/to/repo claim --run run-001 --task research-a --actor /private/actor.json
python tools/git/cli.py --repo /path/to/repo claim-verify --run run-001 --task research-a --token <returned-token> --epoch 1
python tools/git/cli.py --repo /path/to/repo claim-release --run run-001 --task research-a --actor /private/actor.json --token <returned-token> --epoch 1
python tools/git/cli.py --repo /path/to/repo lfs-probe
```

**Do not include access tokens/passwords** in any command, example record, claim ref, handoff or Git commit. Let credential helpers supply access to the underlying Git remote. Optional `--sync-state /repo/scaffold/aos-w/agent-files/config/sync-state.json` records verified status without credentials.

## Alternative: LFS file-locking candidate

`LFSLockPrototype` wraps actual documented `git lfs lock --json <existing-file>`, `git lfs locks --verify --json`, `git lfs unlock --json --id=...`. It **requires** Git LFS client, configured lockable file, a supporting server, and dependable lock verification on pushes. The local test environment has **no git-lfs executable**; live LFS lock acquisition and remote-server collision results are **NOT TESTED**. One mocked parser test confirms returned owner is a Git account, not the logical AOS-W agent. Shared GitHub authentication cannot by itself distinguish Max and Fred, so LFS cannot be used as the primary same-account task-owner authority without another verified mechanism.

## Tests and evidence

`python -m unittest discover -s tests -p 'test_git_coordination.py' -q`: 15 PASS (Git 2.47.3, real **local bare remote**; LFS unavailable and mock clearly labeled). `python -m unittest discover -s tests -p 'test_*.py' -q`: 90 PASS including previous 75. See `temp/tests/PROMPT-13-GIT-COORDINATION.md` and `docs/specs/adrs/ADR-014-git-cas-provisional-selection.md`.

**Preferred optional coordinated transport: explicit Git ref CAS, provisionally**. Do not assert hosted GitHub CAS tests or a secure global task lock until real remote experiments pass. Default portable mode remains standalone single writer.
