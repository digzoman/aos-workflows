# Git synchronization and task coordination — optional protocol

**Read this only if the workspace explicitly enables Git mode.** A copied `aos-w/` folder used by one agent requires **no Git**. `agent-files/` remains the only normally writable subtree; do not use project framework docs or master templates as task scratch.

## Modes and first steps

Read `agent-files/config/settings.json`, `sync.json` and `sync-state.json` (if present). Record actual persistent filesystem, Git availability, remote URL/config, actor `[Agent | Platform | Role | Instance]`, and current remote reachability. Distinguish:

1. `standalone_single_writer`: one agent; file-only handoffs/checkpoints; sync disabled; no remote claim.
2. `git_mirrored_single_writer`: Git transport, only one active writer; before session and after task/handoff verify remote status; do not silently merge diverged histories.
3. `shared_coordinated`: more than one agent could edit. Require a **verified** remote claim protocol, per task, before writing shared artifacts. A Git checkout, worktree, local `.lock`, LFS owner's account name or local timestamp **does not prove ownership**.

Never infer one mode from an agent's chat context alone; read config and verify host capabilities.

## Task lifecycle with a reachable remote

1. **Session start:** check remote, fetch and compare local/remote branch head. If clean and strictly behind, fast-forward only. If dirty/diverged, stop and report the conflict rather than overwrite it.
2. **Before task:** recompute pinned workflow graph, dependencies, current QC/permissions and provider uncertainty. If shared, acquire remote task claim via explicit expected-value Git-ref compare-and-swap under `refs/heads/aosw-claims/<run>/<task>`. Store actor, token, fence epoch, lease and remote ref SHA in local run claim/handoff; record that Git account identity and actor identity are not interchangeable.
3. **During task:** re-check live remote claim before any significant irreversible/shared action. Local owner files remain advisory; no separate external permission arises from task ownership.
4. **Checkpoint:** append event history, materialize run state/checkpoint, update handoff, then commit only allowed `agent-files/` files with `Agent-Provenance` trailer. Push non-force; verify remote SHA. If rejected, stop, fetch for read-only inspection, and preserve local branch.
5. **Release:** use the exact still-current token and epoch to update the claim ref to released via a new expected-value push. A stale worker cannot release someone else's later epoch.
6. **Cold start after crash:** read pinned run and remote claim ref, note claimant, epoch, lease and source evidence. An expired timestamp is **not** automatic takeover. Request an explicit owner-reviewed reclaim reason, inspect external-effect ambiguity, then require remote CAS to establish a new epoch.

## When Git goes offline

- Standalone: continue normally with local checkpoints.
- Git mirrored single writer: continue **only local bounded drafts** if compatible with task policy; report `sync_pending` and remote check failure in `sync-state.json` and handoff. Never say that a commit was pushed or accepted.
- Shared coordinated: **stop owned task execution, new shared mutations, publishing, provider effects and exclusive claim/release**. Read-only research may continue as explicitly provisional. Local cached claim information does not restore exclusivity.
- After reconnection, fetch and check divergence, the remote claim epoch and provider readback before accepting queued work. Do not automatically reapply unverified writes.

## Identity, authority and privacy

Producer identity is `[Agent | Platform | Role | Instance]`, stored in claim refs and significant Git commit trailers; Git `user.name`, auth login and remote token are separate and cannot authorize a task. QC PASS, workflow approval and live-provider permission remain distinct. Remote CAS is coordination **only**, not a provider-side transaction fence. Avoid secrets/private clients in publicly readable branches or `agent-files/` pushed to public Git. Only nonsecret, approved project files may be mirrored to a public repository.

## Git LFS vs Git ref CAS

Git LFS locks are file-path locks and require Git LFS client/server and an existing lockable file. Verify with live server before using. Git LFS server's ownership model can collapse agents sharing one authentication identity. The optional preferred experiment uses one Git ref per task and `git push --force-with-lease=<ref>:<actual-old-sha>`; a real local bare Git remote demonstrated race rejection. **Hosted GitHub behavior remains unverified** in this development environment, and Git host protection policies may reject special claim branches.

## Fail-safe handoff fields

Include `mode`, `remote_checked_at`, `remote_head`, `sync_status`, logical owner, `claim_ref`, `claim_ref_sha`, `claim_epoch`, `claim_expires_at`, unverified provider effects, pending QC/approval, last locally stored checkpoint, pending push commit(s), and **next safe action**. Prefer structured `agent-files/config/sync-state.json`; never overwrite event history to make sync look successful.

See the optional helper in the development repository's `tools/git/` and the full experiment report in `temp/tests/`. Neither is a required dependency of standalone file-only workflows.
