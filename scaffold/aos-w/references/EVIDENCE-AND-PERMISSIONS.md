# Identity, evidence, review, approval and provider truth

## Task provenance

Use four-part identity `[Agent | Platform | Role | Instance]` consistently in significant events, attempts, claims, reviews, handoffs and optional Git commit trailers. This is a **producer label**, not authentication or permission. Two agents using the same GitHub account must still have separate logical identities. Do not invent an agent identifier or a review that did not occur.

## Local completion versus quality acceptance

A task can have a verified output file while its independent review is still pending. A review verdict must state:
- exact artifact IDs, versions/hashes and required complete set;
- rubric and version; reviewer identity distinct from producer if required;
- evidence and whether PASS, REVISE, INSUFFICIENT_EVIDENCE, BLOCKED or authorized WAIVER;
- the gate and graph revision it evaluated.

If a creative adds a new square variant after an old review of portrait only, the earlier review does not certify the full new output set. An invalid square does not erase a valid portrait.

## Authorization is not quality approval

A quality PASS never grants external actions. Separate approval records define an authorized `action` (e.g., `activate_live`, `change_budget`, `send_message`, `deploy_prod`), exact affected object IDs, allowed versions, excluded siblings, budget/time limits, issuer and revocation. A reference to an agent skill, Git write access or a provider token cannot expand scope.

The initial bundled templates permit only benign local research/drafting/review. They do not provide approvals for advertising accounts or CRM changes.

## What was actually verified?

Mark evidence as **LIVE/REAL**, **MOCKED/CONTROLLED**, **MANUAL/COOPERATIVE** or **NOT_RUN** and state any missing tool.

- Local `state.json` is evidence about the workflow, **not** actual Meta campaign status.
- Meta API update response ACCEPTED is not subsequent configured/effective ACTIVE and not proof of ad delivery.
- A saved HighLevel bot instruction is not a successful live IG/Messenger exchange.
- Website source commit is not a confirmed production deployment.
- A PageView/CTA click does not prove a confirmed Schedule booking, Good Lead or Purchase.
- `P:` in an ad name, stale indexes and previous chat summaries are not live provider readback.

For ambiguous side effects, record RECONCILE_REQUIRED and **read** provider state before retrying a write. In file-only standalone without provider tools, stop honestly and ask for authorized verification. This starter does not include provider APIs.
