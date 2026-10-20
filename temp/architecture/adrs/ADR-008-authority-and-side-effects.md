# ADR-008, Permission and external provider truth precede side effects

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

Prompt 03–05 evidence shows QC on wrong artifact versions, duplicate Meta objects after ambiguous API timeout, staged vs launched state, and uncertain CRM CAPI dedup. LangGraph warns interrupted tasks may rerun [W05/W06]. A Rep distinguishes plan, skill, Guardian and external authority [A02/A04/A09].

## Proposed decision

Require approval by exact scope and versions for consequential actions. Keep QC gate and permission gate separate. Before external create/update, inspect provider, record operation key and precondition; after write, read back actual provider state. On timeout, reconcile before retry. Preserve immutable attempts; compensation/rollback is a new authorized operation, not guaranteed transaction.

## Alternatives and tradeoffs

Pure files cannot force every agent to honor approval or network idempotency. Avoid exactly-once marketing claims absent provider guarantees. Manual mode must stop and request approval rather than auto-transmitting anything.

## Validation and reconsideration

Mock ambiguous timeout + retry, stale QC after copy change, human approval missing, approved paused stage vs unauthorized launch, rate-limited GET, and provider-borne duplicate conversion event.
