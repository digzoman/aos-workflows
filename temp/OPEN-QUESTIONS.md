# Open Questions, No Unilateral Resolution

These questions are intentionally deferred until research and PRD review. Record proposals with rationale before marking any decision approved.

1. Which Git shared-claim mechanism wins after **real LFS vs atomic claim** tests, especially when different agents share one GitHub identity?
2. What guarantees must cloud file storage provide for persistence, atomic file updates, and concurrent claims?
3. Which restrictions can the file protocol express, and which require optional tooling or an executor for hard enforcement?
4. How are offline and cloud single-agent workflow instances distinguished from collaborative shared instances in config without overly complex modes?
5. What canonical state/event schemas, validation policy, and recovery model best support YAML, Markdown, JSON, and JSONL?
6. How do future standardized scaffold upgrades preserve `agent-files/` reliably?
7. Which open-source license should govern the public framework? None is selected.
8. How much Meta advertising creation and implementation qualifies as a bounded V1 pilot, without implying permission to publish live ads?
9. What is the specific policy for expiring ownership/leases and reclaiming abandoned tasks when no daemon exists?
10. Which LangGraph patterns should be borrowed conceptually, and which require an actual runtime?

11. What portable schedule notation is simplest, and how are timezone, daylight saving time, schedule changes, and ad hoc overrides represented?
12. What performs triggering in each host environment, if anything, and what happens when no scheduler is available?
13. How are missed schedule occurrences, overlap policy, duplicate triggers, pause/resume, retries, and per-occurrence history handled?
14. What is the precise format and resolution order for skills bundled with a base template, custom template, or workflow instance versus an installed or external repository reference?
15. How are remote skills version-pinned, authenticated safely, validated, trusted, cached, updated, and handled when unavailable or offline?
16. Which skills are instructions only versus executable tools, and how do we guarantee skill discovery never expands execution permissions?

Open questions are not blockers for Prompt 02 research unless explicitly noted.

## Research-phase evidence questions for Prompt 03–05

17. What is the precise authoritative precedence when a ChatGPT message shows a newer research run in progress but the repository run index has not yet been updated?
18. How must a QC approval be bound to an exact artifact revision and required output set so that old or partial passes do not approve new work?
19. How will handoff records reference artifacts across separate private agent repositories without making the portable AOS-W core Git-dependent?
20. What provider read-back and idempotency evidence suffices after an ambiguous external API timeout?
21. How should user-facing status distinguish configured active, effective eligible/delivering, review pending, and measured spend/conversion from merely accepted API writes?

## Prompt 03 research-derived decisions for later design

22. Should the agent offer-family ledger and the vertical seller/market observations use one shared identifier envelope or separate domain tables with cross-links?
23. How should a versioned rubric key distinguish advertisement-persistence score, vertical opportunity score and evidence confidence in a mixed portfolio?
24. What is the precise handoff rule when child run PROGRESS has newer observed state than its aggregate RUN-INDEX or cached rollup?
25. Which evidence-quality failures require blocking QC, and when may a human accept a qualified report despite incomplete coverage?
26. What policy controls auto-start of suggested subverticals versus explicit per-run approval, considering the historical 15-run individually authorized program?

## Creative pipeline requirements to finalize in Prompt 07/08

27. Which artifact types require stable hashes, including source screenshots, copy fields, SVGs, portrait/square rasters and Meta imported media?
28. Which exact variant change invalidates semantic/copy/brand/export/placement/human approval gates, and can automatically preserve unaffected approved sibling variants?
29. How should explicitly owner-approved brand or aspect-ratio exceptions be represented and distinguished from errors or incomplete compliance?
30. Which environment-side tools can deterministically inspect image dimensions/mode/hash versus which are only advisory in the plain-file no-runtime mode?
31. How to enforce reviewer independence and preserve first-pass Fred/Muse outputs when file reads and access policy are not technically enforceable in every host?
32. How should placement-specific approved formats and Story/Reels safe zones be versioned, since 1080×1080 and 1350×1350 squares have different historical usage?
33. How will a step-local optional logo skill resolve a pinned source/version and safe fallback without mandatory Python in AOS-W?
34. How should GitHub asset persistence, Meta creative media mapping, actual placement previews, messaging and eventual publication be separate gate states?
35. What is the scope of authorized automatic repair when it changes a headline, price, funding eligibility statement, official brand asset or owner-selected version?

## Operations research decisions to resolve in PRD and runtime design

36. Which provider-specific source-of-truth reads and external action adapters will be optional V1 capabilities, and what is the standalone file-only fallback?
37. How to bind scoped launch authorization to exact child IDs, media/target revisions, permitted budget and excluded sibling campaigns without requiring Git?
38. How to model write acceptance, provider configured/effective status, Meta review eligibility and actual insights as separate evidence dimensions?
39. Which operations are idempotent by stable key versus need read-before-retry plus compensating work? What explicit emergency pause authority should exist?
40. How should critical but incomplete CRM end-to-end messaging/tracking gates influence a conversations-optimized campaign launch, including documented human exception?
41. How should channel attribution, booking Schedule browser/server dedup, Good Lead qualification and consent be represented without leaking sensitive customer data?
42. How are provider API rate limits, unknown GHL definition scopes and ephemeral Meta preview URLs handled in durable checkpoints?
43. Which measured/estimated reporting metrics, freshness windows and uncertainty flags belong in reusable recurring monitoring templates?
44. When a parent campaign has held sibling adsets, what preflight prevents activating unapproved children?
45. How should deployment authority distinguish a Max source build, Firebase DEV preview and subsequent production with explicit backup/rollback?

## Prompt 06 architecture decisions explicitly awaiting PRD review

46. Which proposed ADRs 001–008 may be ACCEPTED in whole or with modifications, given zero-runtime manual guarantees?
47. Are task graph predicates restricted to declarative operators (to be evaluated manually where no validator exists), and which UNKNOWN outcome is blocking?
48. How can snapshot JSON and append-style JSONL be kept coherent after torn writes in a plain-files-only environment without claiming host atomics?
49. Does AOS-W need adapter capability levels (advisory, verified local exclusive, verified remote exclusive), and how should a user switch safely?
50. If an arbitrary GitHub API client exposes only REST PATCH ref without expected-SHA semantics, what tested atomic create/renew/reclaim mechanism will work?
51. Which stale-lease fencing and output acceptance checks must be mandatory in shared mode, and who authorizes reclaim after crashes?
52. What is the minimum cloud persistent-filesystem durability proof, especially where agent containers may be ephemeral?
53. How should skills in AOS-W and existing A Rep procedures coexist without ambiguous shadowing/override?
54. Should workflow-instance checkpoints be snapshots + events with both authoritative roles or should one dominate reconstruction under conflict?
55. Which exact manual/offline guarantees can reasonably be asserted in V1 and which require a verified runtime?
56. How should AOS-W integrate with an existing A Rep plan-work without creating a second competing business-work plan?
57. Need to reconcile public A Rep doc version mismatch CURRENT 1.5.0 versus main SKILL 1.5.1 when selecting an integration baseline. Installed Fred host remains unverified.

## Prompt 08 final technical-design review gates

58. PRD formal approval record remains pending though user requested Prompt 08. How should owner record explicit decision and selected ADR statuses before Prompt 09?
59. Finalize proposed schema and file layout within agent-files after trial cold-start with independent agent; record any user-requested deviations, do not silently alter protocol.
60. Verify JSON Schema with actual Draft 2020-12 validator and YAML-to-JSON parser, beyond document parsing/reference checks.
61. Choose tested Git LFS vs Git CAS coordination adapter only after same-credential two-worker races, crash, lease, reclaim, fencing and offline network tests.
62. Approve exact recurrence syntax, DST/missed/overlap default policies, and host trigger abilities.
63. Review trust precedence and installed/remote skill collision handling, optional scripts and external privilege policy.
64. Test events-as-audit/state-as-derived reconstruction on interrupted/torn writes with no mandatory Python, and articulate manual integrity limitations.
65. Define production provider adapter permission scope, actual provider readback and CAPI idempotency only after separate owner authorization.

## Prompt 09 follow-up work

66. The scaffold ships two YAML templates and 16 copied structural schemas; run an actual YAML-to-JSON JSON-Schema library validation and test cases in Prompt 10 or 14. The staged graph shape/static JSON checks are not full schema execution.
67. Optionally automate safe upgrades and scaffold-only ZIP releases. The current manual upgrade guide and packaging script are documented; no automated release/upgrade or ZIP artifact generated in this turn.
68. Test the pre-seeded created practice run with a fresh AI agent and verify real task transitions/checkpoint write/recovery, including one actual file-only without Git environment.
69. Decide whether future releases should include the inert practice instance in agent-files or move it to a protected reference-only fixture. Keep user-owned data safe during upgrades.
70. Confirm exact interpretation of owner Prompt 09 "using the approved PRD" within the formal PRD signoff register before accepting all proposed ADRs. Only scoped scaffold authorization was recorded.
