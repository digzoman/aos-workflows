---
name: evidence-handling
description: Record source observations separately from inference and unverified gaps in a bounded research workflow.
---

# Evidence handling for research-starter

Load this skill **only** at `collect-evidence` (or a step that explicitly references it). It does not provide new permissions or require a script.

1. Record a source name/locator, actual access date and what text or asset was **directly observed**.
2. Separate observed facts from interpretations, plans and recommendations.
3. When a source is inaccessible, label **SOURCE_UNAVAILABLE** or **RETRY_REQUIRED** and preserve what was actually attempted; do not count that as verified empty.
4. If two sources conflict, preserve both, record timestamps and flag which requires verification.
5. Do not reproduce private customer messages, proprietary ad images, API keys or tokens in a public example.
6. End with limitations, next bounded research actions and source references that a different agent can check.

Never silently upgrade confidence, execute tools without authorization, or override a higher-priority owner instruction.
