# Formal lifecycle, gates, retries, checkpoints and recovery

**Design proposal** drawing on PRD §§8–11/14 and Prompt 03–05 Ampgent interruptions, LangGraph checkpoint/replay study. Plain-file protocol does not itself create atomic writes.

## State domains

**Task lifecycle enum**, specified for V1:
`PROPOSED`, `WAIT_AUTHORIZATION`, `WAIT_DEPENDENCY`, `READY`, `CLAIMED`, `RUNNING`, `WAIT_EXTERNAL`, `WAIT_REVIEW`, `NEEDS_REWORK`, `BLOCKED`, `RECONCILE_REQUIRED`, `COMPLETE`, `SKIPPED`, `CANCELLED`, `SUPERSEDED`.

**Run lifecycle:** `CREATED`, `ACTIVE`, `WAITING`, `BLOCKED`, `COMPLETED`, `CANCELLED`, `SUPERSEDED`; derived from node statuses and parent scope, with event trail.

**QC verdict:** `PENDING`, `PASS`, `REVISE`, `INSUFFICIENT_EVIDENCE`, `BLOCKED`, `WAIVED_BY_OWNER`. **Approval decision:** `GRANTED`, `DENIED`, `REVOKED`, `EXPIRED`. **Provider operation observation:** `NOT_SUBMITTED`, `REQUEST_ACCEPTED`, `READBACK_CONFIRMED`, `UNKNOWN`, `REJECTED`; effective delivery/business outcome tracked separately. Domain research outcomes (e.g. `EMPTY_VERIFIED` or `LAUNCH_CANDIDATE`) never overwrite lifecycle.

## Transition table

| From | To | Preconditions and event |
| --- | --- | --- |
| PROPOSED | WAIT_AUTHORIZATION or WAIT_DEPENDENCY | child proposal recorded; scoped prior permission absent/present; `task_proposed` |
| WAIT_AUTHORIZATION | WAIT_DEPENDENCY | exact required authorization granted; `authorization_granted` |
| WAIT_DEPENDENCY | READY | eligible dependency/conditional/skill/capability gates pass; `task_ready` |
| READY | CLAIMED | advisory single-writer or backend-verified ownership, claim evidence; `task_claimed` |
| CLAIMED | RUNNING | claim current, correct graph revision, task attempt identified, actor and permissions rechecked; `task_started` |
| RUNNING | WAIT_EXTERNAL | authorized work scheduled or provider result pending; `task_wait_external` |
| RUNNING | WAIT_REVIEW | outputs present/verified and review required; `task_submitted_review` |
| RUNNING | COMPLETE | outputs valid, no remaining required gate; `task_completed` |
| WAIT_REVIEW | COMPLETE | exact artifact set passes review or scope-approved waiver; `review_accepted` and `task_completed` |
| WAIT_REVIEW | NEEDS_REWORK | review fail with identified impacted outputs; `review_revise` |
| NEEDS_REWORK | READY | revised candidate/attempt budget and dependencies valid; `task_requeued` |
| RUNNING/WAIT_EXTERNAL | RECONCILE_REQUIRED | unknown external side effect or ambiguous write; `side_effect_unknown` |
| RECONCILE_REQUIRED | RUNNING/WAIT_REVIEW/COMPLETE | authoritative readback resolves actual effect; `provider_reconciled` |
| Any nonterminal | BLOCKED | missing required capability/source/permission, unsafe claim state or exhausted retry; `task_blocked` |
| BLOCKED | READY | recorded blocker resolved, eligibility recomputed; `task_unblocked` |
| Any nonterminal | CANCELLED | authorized cancellation with impact/compensation; `task_cancelled` |
| COMPLETE/SKIPPED | SUPERSEDED | authorized graph revision changes relevant outputs, preserving previous verified result; `task_superseded` |

A transition not present above is invalid unless a formal recovery event reconstructs it from preserved evidence. Never unilaterally change COMPLETE to READY and discard history.

## Side-effect attempt sub-state

For external mutation: `INTENT_RECORDED -> REQUEST_SUBMITTED -> [ACKNOWLEDGED | REJECTED | AMBIGUOUS] -> [VERIFIED | RECONCILE_REQUIRED]`. The intent includes operation key, approval ID, provider identity/object, pre-state version, desired diff and limits. Log intent **before** calling provider; log ACK only upon observed response; attach live readback before declaring provider-state VERIFIED. A write ACK without GET does not imply effective status or delivery.

Idempotency is operation-specific. An unknown Meta create requires provider lookup using stable signature before retry; a CAPI conversion may be irreversible and uses stable milestone/event identity with consent. A compensated action is a new separately authorized event, not removal of history.

## Checkpoint and event semantics

An event is one newline-delimited UTF-8 JSON object with monotonically increasing `seq`, unique `event_id`, run/task/attempt refs, action actor and event payload. Include `prev_digest`/current `digest` when hashing capability is verified. Snapshot `state.json` includes `last_event_seq`, `last_event_digest`, `state_revision` and materialized task map. Checkpoint includes the same event prefix and canonical graph revision plus verified artifact refs and known blockers. A checkpoint is marked durable only after its file is persisted and, where required, remote sync is independently verified.

**Minimal manual host** may be unable to compute SHA-256 or perform atomic write. It must record `integrity_level: advisory` and cannot claim cryptographically verified events or hard concurrency; nonetheless serializes logically consistent events and state within single-writer constraints.

**Optional enforced host** SHOULD append+fsync or temp-file-write+rename and use digest validation. Multi-agent append needs a single serializing event writer or CAS/versioned merge, not independent concurrent append without arbitration.

## Crash and torn-write recovery

1. Open `run.json`, pinned graph/lock, `state.json`, latest checkpoint and event file. Verify schema compatibility and actor authority.
2. Inspect event lines in order. An invalid/truncated last line is **suspect tail**, not accepted history; copy to run-local quarantine/evidence file, do not erase it.
3. Find longest confirmed event prefix and matching checkpoint. If state snapshot is ahead/behind or digest differs, mark reconciliation required and rebuild snapshot from confirmed events, keeping old file.
4. Recover task statuses and outstanding attempt/claim. If an external call may have run but no readback exists, remain RECONCILE_REQUIRED and perform *read* before any retry.
5. Check current claim validity and fencing token if shared mode. Expired timestamp alone is not permission to steal remote claim.
6. Re-evaluate graph dependencies, skill availability, permissions and stale QC. Resume only the eligible task; write `recovery_checked` event and handoff.
7. Record uncertainty explicitly. A human may accept a limited research report, but may not convert unknown provider action into false verified success.

In manual single-agent mode, partial writes may be unavoidable; cold-start protocol emphasizes preserving safe evidence and stopping. AOS-W does **not** claim exactly-once operations or crash-atomic storage without host support.

## Quality and approval semantics

Review binds reviewer identity, rubric version, *entire required artifact set* (IDs+revision/digests), source evidence, verdict, required fixes and exact gate. Independent reviewer cannot be producer when the policy requires independence. New artifact version invalidates affected prior review use; old review stays historical.

Authorization binds issuer/authority, action scope, exact resources/versions, limits/exclusions, optional expiry and conditions. Revocation prevents future side effects, not cancellation of already executed external changes. Approval record must never be inferred from a positive QA verdict. Escalation/default: `write_local` allowed within bounded scope; `activate_live`, `change_budget`, `send_message`, `deploy_prod`, `emit_conversion` require separately approved power.

## Retries and monitoring

Retry policy has `max_attempts`, `on` error types, `backoff` (`manual`, `none`, or host-applied fixed/exponential), `next_eligible_at` and `on_exhausted`. Missing host timer records WAIT, not unattended execution. `UNKNOWN` side effect never automatically retried. Independent branches may proceed if they don't depend on the blocked node and share no mutable artifact/claim conflict.

Documented scenario requirements include stale research index, inaccessible Meta source, only one incorrect square creative, provider rate limit after activation, CRM configuration without channel test, and unknown browser/server Schedule dedup.
