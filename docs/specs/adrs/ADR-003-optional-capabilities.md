# ADR-003, Orthogonal execution and storage capabilities

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

Fred active runtime versus Max deliberately dormant [A10/A14] show agent wake and durable storage are different concerns. User requires local standalone, cloud standalone, optional Git mirror and multi-agent.

## Proposed decision

Record capabilities independently: persistent storage location, optional Git remote/mirror, concurrency coordination mechanism, host executor, schedule trigger, provider access, review and rendering tools. The same template is usable in each. A missing hard mutex means collaborative write mode is disabled or human-serialized, not assumed safe.

## Alternatives and tradeoffs

Single \`offline/online\` switch is simpler superficially but conflates cloud storage with multi-agent and remote network access. Always-on service or database imposes a dependency. Some guarantees are impossible when a plain agent manually edits files.

## Validation and reconsideration

Prompt 16 local/cloud persistent no-Git tests; Prompt 17 two-agent and Git sync tests; host capability truth table in PRD.
