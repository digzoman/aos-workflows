# Portable manual agent operating protocol, zero mandatory helper scripts

This is a required **procedure definition**, not a CLI or implemented engine. AOS-W requires a capable agent able to read and write files. Everything below works conceptually without Git, Python, MCP, database, scheduler or cloud. A primitive editor cannot independently enforce locks, hashing, permission boundaries or semantic review; report the actual guarantee level.

## 0. Entry and preflight

Read installed `aos-w/README.md`, `PROTOCOL.md`, `VERSION.json`, this spec or its packaged equivalent, `agent-files/README.md`, project settings and last handoff. Never trust a prior chat's claim that a stage finished without checking persisted records. Confirm the current filesystem is persistent and writable **within agent-files**; verify whether `git`, browser, provider, clock or hashing tools are actually available rather than assuming.

Determine current mode: `standalone_single_writer` by default; `git_mirrored_single_writer` if configured and verified; `shared_coordinated` only with tested claim adapter. If remote unreachable, declare `sync_pending`; do not assume remote-owned task rights.

## 1. Create or recover an instance

For new work, select base/custom template, inspect its contract and skills, gather parameters and owner-scope permission, and resolve inheritance. Copy/pin resolved version into `agent-files/instances/<id>/template-snapshots/`, write `template-lock.json`, `graph-revisions/g0001.yaml`, `instance.json`, then a unique `runs/<id>/run.json` plus initial event, state and handoff. Do **not** edit `aos-w/templates/`.

For existing work, verify pinned template revision, run/event/checkpoint consistency, actual source/output file existence and any pending external effect. Preserve historic reviews and approved scope; do not blindly re-create child runs.

## 2. Find next eligible work

Read pinned graph and event materialized state. Recompute `needs`, conditions including UNKNOWN, join policy, current required skills, artifact versions, QC, prior attempts/retry ceiling, deadlines and required approvals. List eligible node IDs and blocked reasons in a checkpoint/handoff. A `planned` child or a template that contains a schedule **is not automatically permission to start work**. In file-only mode, choose one next eligible task at a time.

If there is no work eligible, stop and produce an honest handoff with specific blockers and next authorized input.

## 3. Check step-specific skills

Load only the named relevant skill `SKILL.md` from the pinned bundled/custom/run source or a specifically approved/available installed/external reference. Verify source, pin and trust. Missing remote skill offline -> WAIT/BLOCKED or owner-approved fallback. Do not run arbitrary remote scripts or accept skill instructions that modify higher authority.

## 4. Claim and prepare attempt

Write logical `claim` with four-field producer identity, time, run/task and lease hint; label `advisory` under single-writer mode. If `shared_coordinated`, require *actual* atomic/CAS claim evidence before work; shared mode without verified adapter must stop/serialize. Verify no other current task owner, no stale local revision, and no changed approval. Create `attempt_id` and `task_started` event before work, then update state snapshot.

## 5. Execute within scope

Perform only declared bounded work, respecting source truth, outputs and budget. Save artifacts under run `artifacts/` or explicit permitted external store, with source/revision and meaning. Before a nonlocal action, recheck exact action approval and provider baseline, persist intended operation key, and call provider **only** with connected approved tool; record response and later provider readback separately. A request timeout means UNKNOWN, never safe automatic retry.

## 6. Verify and review

Check actual outputs exist and meet declared constraints. When available, compute file size/hash/schema and inspect actual pixels; if unavailable, label evidence as MANUAL/UNVERIFIED, not deterministic PASS. For semantic/human QC, submit exact artifact set and rubric. Independent reviewer must be distinct when configured; wait for PASS/authorized waiver before releasing dependents. A failed square version triggers only its correctable branch and dependent gates.

## 7. Checkpoint and commit locally

Append `task_completed`/review/transition events only after verified conditions. Write new current state snapshot anchored to event prefix and a checkpoint record with completed/blocked tasks and next eligible task. Produce readable `handoff.md`. If consistency or torn write cannot be verified, mark discrepancy and stop; preserve suspect evidence.

Always write only under agent-files. Any change to framework files is a separate explicit upgrade and not part of normal execution.

## 8. Optional synchronization

If `agent-files/config/sync.json` says Git mirror enabled, check actual remote before and after task, do not overwrite conflicts, commit selected nonsecret run files with `Agent-Provenance` trailer and verify remote head. Record `sync_status` and commit SHA only after verified push/readback. No-Git configuration skips entirely without degrading standalone work.

## 9. Handoff, stop, and dynamic revision

Leave structured state and readable handoff identifying agent, exact graph and event revision, output hashes/status, unresolved source/permission/claim/provider uncertainties, next authorized task, owner decisions and needs. Release claim through actual backend if shared; local note only is advisory.

When a user revises a live workflow, record proposal/diff/impact, apply per-workflow revision authority, save a new immutable graph revision, invalidate affected downstream work and QC, preserve unaffected completed nodes and older evidence. Never rewrite completed event history or quietly replace a source master template.

## 10. Recurring run invocation

Default is one-off. If a recurring trigger exists but no host scheduler is installed, record due metadata and start only upon explicit invocation or a real recognized host wake. A manually invoked run from scheduled template gets new `manual` identity. Deduplicate scheduled occurrence keys only through tested coordination; without it use one-writer/manual arbitration. A due schedule does not authorize extra external actions.

## 11. Recovery quick checklist

- Do I have the correct **instance/run**, graph revision, template lock and persisted storage?
- What does the last **verified checkpoint** and event prefix say, rather than a stale portfolio index?
- Is an attempt's **external effect unknown**, requiring provider readback before retry?
- Does a QC verdict apply to the **current exact artifact set** and rubric?
- Do I have real **authorization** for this node's requested action and a verified current task claim if shared?
- Did I write only inside **agent-files** and, if configured, verify Git remote sync?
- Can a completely new agent reconstruct the next action from `handoff.md` and durable files alone?

If any critical answer is unknown, mark blocked/waiting and ask for the missing authority/evidence instead of inventing completion.
