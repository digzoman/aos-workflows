# Prompt 05 primary source index

Research conducted 2026-10-20. These restricted-source pointers refer to authenticated private repositories; no raw internal account IDs, private transcripts, tokens, webhook payloads, customers, or actual performance figures have been copied to this **public** repo. **R** means the original document or issue was directly read; source-recorded actions do not constitute new live provider verification.

Private Max repo aliases:
- V3 = `work/ampgent-adaptive-offer-testing/meta-ad-creatives-v3-five-buckets-2026-09-26/`
- ADS = `work/ampgent-adaptive-offer-testing/`
- B8 = `work/ampgent-adaptive-offer-testing/meta-ad-creative-bakeoff-2026-10-04/chatgpt/run-5-the-doers-way-va/`
- B9 = `work/ampgent-adaptive-offer-testing/meta-ads-buckets-9-10-2026-10-16/bucket-9-paid-marketing/ampgent-9.1-ai-media-buyer/verticals/coaches-consultants/`
- WEB = `work/ampgent-website-redesign-2026-10-08/`

| ID | Original private source | Directly supported process evidence |
|---|---|---|
| R82 | V3/META-STAGING-2026-09-26.md | Early one-campaign V3 paused structure with 20 ads. |
| R83 | V3/META-STAGING-2026-09-28.md | Per-offer paused campaign creation, asset mapping, API timeout causing duplicate objects, later cleanup and copy/messaging corrections. |
| R84 | V3/META-AUDIENCE-TARGETING-2026-10-14.md | First age targeting update, standard versus Advantage+ audiences, in-place edits and two replacement adsets. |
| R85 | V3/META-AUDIENCE-TARGETING-2026-10-15.md | Superseding age caps, 16 adset verification, geographic/hold preservation. |
| R86 | V3/META-MESSAGING-TEMPLATE-RULES.md | Full selectable Meta Question, blank Response, routing fingerprints. |
| R87 | V3/LAUNCH-RANKING-2026-09-28.md | Stable offer identifiers and initial launch ranking. |
| R88 | ADS/meta-launch-2026-10-15.md | Owner activation, child-first updates, rate-limited read-back and later campaign-level confirmation. |
| R89 | B8/meta-ad-manager-qa.md | Square feed fixes, rejected mixed-placement Meta operation and bounded fallback. |
| R90 | B9/META-SETUP-QA-2026-10-18.md | Paused C01 staging and exact creative/message read-back, incomplete placement/chat tests. |
| R91 | B9/meta-ad-manager-qa.md | Later activation of C01 in shared parent, paused siblings, P-prefix/actual status discrepancy. |
| R92 | WEB/PROMPT.md | Offer pages, CTA/UTM plans, consent, DEV/PROD authority boundaries. |
| R93 | WEB/README.md | Site source staged in Max; DEV handoff distinguished from production. |
| R94 | WEB/qa/FULL-SITE-QA.md | Static QA versus pending actual hosted browser QA. |
| R95 | WEB/qa/chat-widget-qa.md | Consent gating for analytics/chat, unverified CRM offer-context transfer. |
| R96 | WEB/handoff/FRED-DEPLOYMENT-HANDOFF.md | Cross-repo deployment, backup, DEV QA and production approval. |
| R97 | B9/GHL-MAX-MESSAGING-BOT-HANDOFF-2026-10-18.md | Additive Max-bot offer knowledge, question/reply and regression tests. |
| R98 | B9/GHL-MAX-MESSAGING-BOT-INDEPENDENT-QA-2026-10-18.md | Saved bot configuration verified, independent real DM behavior untested. |
| R99 | `scratch/max-chatbot-qa/2026-10-10/QA-REPORT.md` | Read-only simulated offer-routing test cases. |
| R100 | `scratch/notes/tracking-verification-report-2026-10-14.md` | Browser Pixel/server CAPI audit, real booking event, probable Schedule double count, Good Lead trigger unknown. |
| R101 | Private `digzoman/a-rep-Fred` issue #96 | Owner revised campaign structure and restricted staging to PAUSED. |
| R102 | Fred issue #108 | Check-before-create Votel staging and correct message fields. |
| R103 | Fred issue #124 | Only one owner-approved AltaHQ image staged, others untouched. |
| R104 | Fred issue #135 | Narrow square-feed repair scope; unrelated ads untouched. |
| R105 | Fred issue #129 and closure comments | Consent-gated Pixel deployment and later source-recorded PageView verification. |
| R106 | Fred issue #130 and comments | Booking/Good Lead CAPI partial state, unavailable workflow definition, dedupe risk; still open at inspection. |
| R107 | Fred issue #147 and comments | Saved B9 chatbot setup but no independently verified FB/IG live replay; still open at inspection. |

The Ampgent project context also contains `B1-7: Ads Management 2 - Ampgent Meta Launch Review`, `Audit Ad Geographies`, B9 offer development, HighLevel connector checks and site-related conversations. Those private full chat transcripts were not all reopened. Earlier reported CPC/CTR snapshots are historical conversation claims, **not live Meta insights independently verified by this Prompt 05 research**.

**Temporal source conflicts:** R84 was superseded by R85; R82 was superseded in campaign architecture by R83/R101; R90 paused B9 staging preceded R91 later activation. R91 noted an actual ACTIVE campaign still named `P:`. Older website DEV-only documents are not proof that later production deployment never happened. Bot configuration PASS does not mean independent end-to-end Messenger/Instagram behavior passed. R100's browser/server Schedule dedup issue is **probable, not definitively proven**.

No live account changes or performance API queries were made.
