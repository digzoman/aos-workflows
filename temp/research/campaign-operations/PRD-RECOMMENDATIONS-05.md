# Prompt 05 prioritized recommendations for the enhanced PRD

All items are **proposals** based on historical cases R82–R107, not user-approved implementation or code.

**P0. Explicit external-operation contracts.** Treat operations as read/plan, stage paused, activate, spend/budget change, production deploy, GHL bot edit and CAPI send, each with separate scoped authorization. Include positive allowlist and negative exclusion list.

**P0. Provider-truth reconciliation.** Every external mutation saves prior observed state, expected new state, operation signature, provider write acknowledgement, actual follow-up field readback, and unknown/pending outcomes. File names and local docs are not authoritative current Meta states.

**P0. Prevent duplicate/irreversible actions.** For create operations, lookup current objects and reconcile timeout before retry. For CAPI, stable business milestone/dedup ID and consent prior to transmit. Compensation is a new authorized operation, not an assumed rollback of an atomic transaction.

**P0. Typed approval + QA matrix.** Asset source, semantic/visual approval, Meta creative field QA, audience/geo, messaging, real chatbot routing, consent/site, Pixel/CAPI, launch permission, effective delivery and commercial outcomes require independent evidence and distinct states. Quality pass never creates permission to spend.

**P0. Historical status conflicts.** Preserve superseded target settings, early paused staging, active newer state and changed campaign architectures. A stale P prefix or old `META-STAGING` record must not override a fresh provider readback.

**P1. Audience semantic validation.** Hard-vs-suggested target restrictions, age 65+ distinction, jurisdiction exclusions, restricted local/regional marketing and campaign budget placement should be encoded into provider-specific validation skills.

**P1. Separation of current config and business results.** ACTIVE doesn't prove delivering, delivery isn't attributed booking, Meta event total isn't deduped appointments, and GHL chatbot config isn't actual channel response.

**P1. Cross-repo deployment and skills.** Templates can reference exact Git sources/local bundles but never require Git for offline use. DEV/PROD require separate approval with backup and hosted browser verification. Connector-provided functions and installed skill files are loaded just in time by stage, not as global authority.

**P1. Narrow remediation and continuous read-only reviews.** A targeting mistake reopens targeting/affected launch QA, not research/image generation. Recurring monitoring may be scheduled via optional host without required daemon; corrective action remains separately authorized.

## V1 acceptance experiments to specify

1. PAUSED staging attempt interrupted after provider creates adset; resume and reconcile without duplicate.
2. Wrong geographic exclusion or 65+ hard/suggestion setting causes targeting QA failure and surgical correction.
3. One placement-rule rejected; alternate approved square mapping passes, creative source and copy unchanged.
4. Simulate accepted activation writes but readback rate limit; outcome remains VERIFY_PENDING until readback.
5. Shared campaign parent activates while four sibling adsets remain PAUSED, proven by provider state.
6. CRM knowledge saved but live messaging unavailable; integration status remains BEHAVIOR_UNVERIFIED.
7. Real booking + browser/server event replay yields exactly one deduped business conversion or a candid unresolved flag.
8. Website source committed but DEV not deployed; cannot claim live. PROD deploy demands separate permission and backup.
9. Measured CPC/CTR distinguished from clearly labeled modeled/no-click CPC estimate, with provider date window.
10. No live provider connections in file-only mode; test can record requested actions, never claim actual Meta change.

All demonstrations can use controlled mocks initially; live-provider integration acceptance must be independently described as live or not executed.
