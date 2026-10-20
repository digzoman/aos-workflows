# Prompt 05 campaign implementation lifecycle

**O** = observed in R82–R107, **P** = proposed AOS-W contract, *not implemented*.

```text
Approved research + creative + offer -> exact scoped task authority
 -> read Meta account and existing objects
 -> plan desired campaign / ad set / ad tree, budget + targeting
 -> verify website / CRM / tracking / message dependencies
 -> authorize and STAGE PAUSED -> reconcile writes with Meta readback
 -> independently QA assets, placements, native CTA, chat and exclusions
 -> owner approval specifically for activation -> enable approved ads
 -> enable approved adsets -> enable approved parent campaigns
 -> read back configured/effective status and review/serving evidence
 -> read measured insights and CRM milestones -> recommend controlled iteration
```

## Stage-by-stage contracts

1. **Offer identity and authority. O [R83/R86/R101–R103].** Owner approved only exact offer-specific images/copy and a bounded write scope. **P inputs** immutable source repo commit, approved copy/media hashes, stable bucket ID, offer promise/CTA, permission. **P output** authorized desired-state manifest. **Gate** no stale creative or implicit permission to launch.
2. **Account/tool access. O [R82/R83/R88].** Read account status, currency, cap and existing campaigns, working message example, tool abilities before writes. **P output** actual provider snapshot and known access faults. **Gate** stale local state not accepted as provider reality.
3. **Build campaign tree. O [R82/R83/R101].** Earlier shared V3 campaign replaced by dedicated campaign-per-offer design, campaign budgets rather than ad-set budgets, one adset and selected creative variants. **P output** parent/adset/ad specification plus legacy objects and exclusion list. **Gate** total budget exposure and objectives match exact approval.
4. **Geography and audience. O [R84–R85/R70].** National US+Canada excluding Quebec and US territories; provincial funding targeted Ontario. CallRail US-only targeting corrected because offer competed with rather than resold source provider. Oct 14 broad 65+ ages superseded by Oct 15 offer-specific caps, because Meta 65 means an open-ended category. Some Advantage+ semantics were suggestions, not hard controls, requiring standard audiences. Two replacement adsets were archived after accurate transfer and readback. **P output** before/after targeting diff, exact exclusions and mode, unchanged other fields.
5. **Creative media and placements. O [R83/R89/R90/R104].** Read actual attached image hashes, copy, native CTA/destination, portrait/square; Meta rejected a mixed Messenger/IG per-placement rule and approved safe-square fallback. **P output** source hash -> media hash -> creative ID -> ad ID -> intended placements, separate visual preview evidence. **Gate** 1:1 pass is not 9:16 pass.
6. **Messaging/CRM. O [R86/R97–R99/R107].** Full prospect Question, blank Meta Response, offer-specific fingerprint, GHL Max bot knowledge and testing. **P output** message intent/routing and regression matrix plus real channel test. **Gate** saved knowledge != actual DM delivery.
7. **Website/landing and tracking. O [R92–R100/R105–R106].** Max staging and webdev/Firebase deployment separated. Consent-gated Pixel PageView and booked appointment server event were documented; native/browser Schedule may duplicate server CAPI; Good Lead trigger and contact attribution unresolved. **P output** offer page/UTM map, DEV/PROD build QA, privacy consent, event taxonomy and end-to-end tests. **Gate** click != booking, booking != Qualified Lead or Purchase.
8. **Paused staging and independent prelaunch checks. O [R83/R89/R90].** All new objects initially paused, full campaign/adset/ad/creative read-back and selected-media verification. **P gate** record each exact passing field separately, with PENDING preview, chat or tracking gates left visibly open.
9. **Activation authorization. O [R88/R91].** Owner explicitly selected 11 launch campaigns and held five plus legacy ads; later B9 authorized one C01 subtree despite a shared parent. **P output** signed launch authorization, exact IDs, cap/budget/exclusions and last observed baseline. **Gate** no creative QA or staging approval converts to spend authority.
10. **Activation and reconciliation. O [R88/R91].** Historical Oct 15 write order was selected ads then adsets then parent campaigns. Successful writes were followed by account-wide rate limit; later campaign-level readback confirmed active selected vs paused holds but child-level serving remained unverified. B9 later read back its activated C01 subtree; impressions and messaging behavior still pending. **P output** distinct write accepted/configured/effective/review/delivery observations.
11. **Monitoring and changes. O [R88/R100 and project-context conversation].** Users requested CPC/CTR, clicks, messages, errors and estimated CPC where no click exists. **P output** dated provider insights, calculation source, observations vs estimates, qualified CRM evidence, change recommendation and **new permission** before automatic live budget/target edits.

## Key design principles

Default mode can create a file-based *plan and QA package* without Git/Meta/HighLevel tools, but claiming a live change requires a connected authenticated adapter. Approval boundaries must separate research, local files, PAUSED staging, DEV deploy, PROD deploy, activation and budget changes. AOS-W should persist configured vs effective Meta status, not infer state from `P:` names. A successful API write or visible PageView does not prove ad delivery or attributable qualified leads.
