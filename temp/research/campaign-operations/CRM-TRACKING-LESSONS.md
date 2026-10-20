# Prompt 05 CRM, website, consent and conversion dependencies

Source audit R92–R100, R105–R107. Historical record, **not newly tested live systems**.

## Observable journeys

Message ads -> selectable full-text Meta QUESTION with blank RESPONSE -> Facebook Messenger or Instagram Direct -> HighLevel Max offer routing -> real conversation -> optional booking -> actual appointment/qualification. Saved Meta message fields and HighLevel offer knowledge were verifiable. Independent real Messenger/Instagram end-to-end C01 replay was not.

Website -> user consent -> PageView where allowed -> offer path/CTA -> LeadConnector booking -> genuine HighLevel appointment -> server CAPI `Schedule`; proposed qualification -> Good Lead. The Oct 14 audit verified one real server booking event but **probable** browser/server Schedule duplication, not conclusively proven final Meta deduplication. Reported Meta Schedule/Good Lead event counts included test/unknown-sourced data and were **not** numbers of validated customers.

Static source-site QA, consent policy descriptions, uploaded websites, Meta Pixel stats, published HighLevel workflows and actual CRM trigger logic all represent **distinct kinds of evidence**. Fred #129 reported Pixel consent-gated deployment complete; Fred #130 remained open/partial. B9 bot task #147 remained open for safe behavioral replay despite saved config.

## Proposed acceptance matrix for reusable module

- Website Reject All -> no optional browser tracking; consent opt-in -> expected PageView; revoke -> stop optional scripts.
- Chat consent and CTA -> actual working widget; optional offer context passed through must be separately tested rather than assumed from visible page label.
- Booking CTA click is not `Schedule`. Confirmed CRM appointment is Schedule source of truth. Cancelled/test appointments separately flagged.
- Use appointment-specific stable event ID across retry, test browser/server dedup and correct calendar filtering.
- Qualifying a lead requires defined CRM/human criteria. Good Lead chatbot-trigger presence does not establish quality, consent, dedup or Meta match.
- Purchase only after recorded won revenue. Do not send Purchase merely because the customer made an appointment.
- Test FB Messenger and Instagram Direct separately, with four canonical questions and unrelated-offer negative controls, no real customer contact without authorization.
- Explain source attribution gaps for anonymous browser-to-DM/CRM matching; avoid claiming Pixel PageView automatically enables lead-optimized delivery.
- Testing actions must avoid leaking email/phone or webhook tokens into logs, source control or public reports.
- If the actual GHL workflow definition cannot be read due to connector scope, record `UNKNOWN/BLOCKED`, never `PASS`.

## PRD implications

The contract for each tracked milestone needs event name/meaning, actual user action, owner/source of truth, intended receiver, consent rule, trusted identifiers and attribution, dedup key and TTL, source timestamp, retry policy, observed provider response and evidence/review gate. An optional repeating monitoring template can later run read-only diagnostics if a host supplies scheduling; AOS-W itself must not require a daemon.
