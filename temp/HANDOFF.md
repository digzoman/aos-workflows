# Latest cross-session handoff

Date: 2026-10-20
Completed: Prompt 05 campaign configuration, launch and monitoring reverse engineering.
Repository: digzoman/aos-workflows, public main. Check current branch HEAD before editing.

## Required next-session reading

1. temp/OPERATING-RULES.md
2. temp/DESIGN-DECISIONS.md
3. temp/WORK-PLAN.md
4. temp/PROGRESS.md
5. temp/research/SOURCE-INDEX.md
6. temp/research/campaign-operations/SOURCE-INDEX-05.md
7. temp/research/campaign-operations/WORKFLOW-MODEL.md
8. temp/research/campaign-operations/FAILURES-AND-AUTHORITY.md
9. temp/research/campaign-operations/CRM-TRACKING-LESSONS.md
10. temp/research/campaign-operations/PRD-RECOMMENDATIONS-05.md
11. temp/research/candidate-templates/OPERATIONS-CATALOG.md

## Completed research and relevant facts

- Private Max records show evolution of campaign architecture from a single paused V3 program to dedicated per-offer campaigns. Actual source/creative/copy IDs should be checked before any Meta mutation.
- Geo and age targeting required owner corrections; Oct 15 caps supersede Oct 14; actual hard versus suggested age constraints need Meta provider readback.
- Oct 15 owner approved eleven campaign trees while holding five and legacy objects. Updates to ads, then adsets, then parents were accepted, but API rate limit prevented full immediate per-ad verification. Later campaign-only readback confirmed expected active/paused at that level.
- Oct 18 B9 C01 was activated in a shared parent, with unrelated adsets read back paused; old P-prefix name did not imply PAUSED. No verified delivery implied.
- Meta messaging Question contains full prospect text and Response is empty; Max bot knowledge/config can be read back, but independent FB/IG click-to-DM behavior remains a distinct unresolved check.
- A real server booking Schedule path and Pixel PageView were documented in Oct 14 audit. Browser/server Schedule duplication is probable, not conclusively proven; Good Lead trigger logic and CAPI dedup/consent still needed verification.
- Website source and DEV/PROD release authority were separated between Max and webdev; static/DEV QA not proof of PROD.
- 15 candidate operations templates and five composition sketches were added **only as specifications**.

## Next assignment, Prompt 06

Investigate actual existing A Rep/Fred/Max scope, plan-work/data-ledger/skills conventions; compare LangGraph checkpoint/interrupt/retry and dynamic graph concepts; agent skill bundling/versioning and remote trust; Git LFS vs atomic branch claims, optional synchronization and cloud local storage; recurring schedule metadata versus an optional host trigger. Capture architectural tradeoffs/ADRs, explicit hard-vs-soft enforcement, no mandatory Git/runtime/server/scheduler.

Do not implement engine before Prompt 07 PRD approval. No live production account activity. Commit sanitized research and update progress/handoff again.
