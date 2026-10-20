# Prompt 05 provider authority and recovery cases

Source references R82–R107 in [SOURCE-INDEX-05.md](SOURCE-INDEX-05.md). Observed failure -> proposed AOS-W response, not implemented behavior.

## Which system is authoritative?

- **Owner intent and approved asset** -> explicit owner approval plus exact canonical copy/media revision in source repo.
- **Meta object status and ad accounts** -> fresh Meta Graph/Ads Manager configured/effective state, not local Git files, API-request acknowledgment or a name prefix.
- **Actual spend/delivery/clicks** -> Meta insights with attribution window/metric type/time range. A configured ACTIVE ad is not necessarily serving.
- **CRM conversation/offer routing** -> actual HighLevel agent/conversation and real channel test, not just saved instruction or sandbox reply.
- **Bookings and qualified leads** -> actual CRM appointment/stage and human or authenticated qualification criteria, not browser clicks or a chat keyword alone.
- **Browser/server event processing** -> Meta Events Manager diagnostics with event IDs plus worker/GHL sent-event evidence, not just list of published workflows.
- **Website build** -> actual Firebase DEV or PROD hosted app and release metadata, not staged HTML.
- **AOS-W state** -> coordinates agents and stores audit of observations, but must reconcile to each external provider when online.

## Errors, reconciliation, compensation

1. **Ambiguous Meta timeout and duplicates [R83].** A failed create left duplicate adset/ad plus unused creative; cleaned after later discovery. **Propose:** stable operation key, lookup existing objects before retry, attach/reconcile orphan and require explicit scope for deletion.
2. **Rejected placement rules [R89/R104].** Meta would not accept one per-placement creative rule for mixed messaging destinations. **Propose:** record permanent validation failure, use owner-approved fallback format and verify readback, do not retry same invalid payload.
3. **Ages and targeting controls [R84–R85].** `age_max=65` meant 65+, and Advantage+ age limits not equivalent to hard age controls. **Propose:** preserve prior full targeting spec, change only approved fields, verify actual hard/suggested control and every exclusion, revert precisely if needed.
4. **Geographic misunderstanding [R70].** Source competitor's service territory was incorrectly used to constrain Ampgent's competitive offer. **Propose:** target user-approved offer geography and eligible buyer, not provider resemblance.
5. **Rate limit after activation [R88].** Forty-two scoped write calls succeeded but the full readback was rejected; later campaign status verified, per-ad delivery still unknown. **Propose:** `WRITE_ACCEPTED/VERIFY_PENDING` and safe read-only backoff/reconciliation. No extra activation retry solely because GET failed.
6. **Stale status label [R91].** Existing campaign name still began P while Meta reported ACTIVE. **Propose:** labels never determine permission or actual status.
7. **Parent blast radius [R91].** Activated C01 in a shared campaign required verifying unrelated sibling adsets stayed paused. **Propose:** enumerate affected tree and preserve holds.
8. **Creative uploaded versus actual placement safe [R89/R90].** Provider hashes and preview URLs existed while crop/Stories/Reels visual acceptance was pending. **Propose:** placement-specific visual gate beyond metadata.
9. **GHL configuration versus behavior [R98/R107].** Saved knowledge was confirmed, but independent authenticated reply replay/direct DM absent. **Propose:** separate `CONFIG_VERIFIED`, `BOT_REPLAY_VERIFIED`, `LIVE_CHANNEL_VERIFIED`.
10. **Pixel/CAPI double counting [R100/R106].** One server booking verified while browser Schedule probably duplicated; dedup not established. **Propose:** stable appointment event ID, consent, source and dedup proof, do not count test events/duplicates as customers.
11. **Cross-repo website release [R92–R96].** Source in Max; actual website deployment lives elsewhere. **Propose:** exact source and deploy commit, DEV/PROD approval, backups, real hosted QA and explicit rollback authority.
12. **Performance estimate [project context only].** CPC for no-click ads was requested as an estimate. **Propose:** measured/estimated fields and explicit inference formula/window; do not invent clicks or performance.

## External side-effect safety matrix, proposed

- **Create** Meta ad/campaign/adset: lookup/reconcile ambiguous failure first; never blindly duplicate.
- **Update** targeting/budget: before snapshot, scope diff, after readback, emergency pause or restore with configured authority. No assumed transactional rollback.
- **Media attach:** verify repo blob -> provider image hash -> ad creative; orphan cleanup separately authorized.
- **Activate:** approval for exact parent/child set, verify siblings paused and budget unchanged; pause accidentally activated objects promptly if authorized and disclose possible spend.
- **GHL edits:** snapshot current knowledge/workflow, additive scoped change and negative control regression; test actual inbound channels when permitted.
- **Site deploy:** DEV-only first, owner PROD approval, protected backup, smoke test and rollback.
- **CAPI send:** stable milestone/idempotency key and verified consent first, because transmitted events cannot reliably be undone.

AOS-W generic state should track intent, permission, request outcome, configured provider state, effective state, delivery result and business outcome as **separate dimensions**, with exact source/version/time and uncertainty. A retry must not reapply irreversible external effects without reconciliation.
