# AOS-W v0.9 — Visualization, Human Language and Third-Party Handoff

**Status:** DRAFT SPEC, not shipped. Companion to [V0.9-PRODUCT-SPEC.md](V0.9-PRODUCT-SPEC.md).
**User report:** screenshot "Bucket 9 · Six-Audience Wave 1 · saved event 89", showing \`hvac-installation-owners--qc-research\` as both card title and ID; "Stage 1 / 2 / 3"; 56 cards in a flat graph; a right pane starting with huge machine JSON policy; top counters "Steps 56 / Complete 16 / Review 0 / Blocked 0" even though 6 review-kind nodes were READY; and a github.com/blob link that displayed HTML text.

## Desired first impression

"Within five seconds, a manager can see what the team is doing, what was finished, what needs checking, what is blocking launch and what they should do next." No prior AOS-W vocabulary should be necessary.

### Example human-first Buckets 9 phase overview

\`\`\`text
RESEARCH ADVERTISERS ─→ INDEPENDENT REVIEW ─→ AD CREATIVE & COPY
         6 audiences          6 reviews ready          Not started
                                     │                        ↓
                              Waiting for reviewer     OWNER APPROVAL
                                     │                        ↓
                              When passed → next     PAUSED META SETUP
                                                              ↓
                                                       APPROVED LAUNCH
\`\`\`

Only show "6 reviews ready" if exactly six review-kind tasks have \`READY\`. Do not imply they passed independent review. Show run-level status separately, for example "**Research corrected; awaiting independent approval**" when grounded. Human title and phase must be editorially sourced or clearly marked as generated summary and reviewed. Do not invent expected output or actual ads created.

### Suggested v0.9 step card

\`\`\`text
┌──────────────────────────────────┐
│ Review HVAC competitor research  │
│ HVAC businesses                  │
│ READY FOR REVIEW                 │
│ Waiting for independent reviewer │
└──────────────────────────────────┘
\`\`\`

The machine ID \`hvac-installation-owners--qc-research\` appears only after selecting *Technical details*. No duplicate slug. Node kind is a small badge rather than the entire heading. A card with a long source title should wrap gracefully rather than overflow.

### Selected-step information hierarchy

1. **What is this?** "An independent reviewer checks the HVAC competitor research for reliable sources, relevant audience and accurate product claims."
2. **What happens next?** Concrete next action for the current status, including who needs to act and why this work is held.
3. **Where to look / what tools?** Named resources in plain English; clickable authorized URLs or repo paths, and "Access required", "Not verified" or "Unavailable" annotations.
4. **What information do I need?** Each input's purpose, exact path and revision.
5. **How do I complete it?** Plain-language procedure, expected output, checkpoint path.
6. **How will it be accepted?** Quality gates, distinct independent reviewer criteria, exact-revision evidence, human approval boundaries.
7. **What if I can't proceed?** Block reason, missing capability, retry limit, safe fallback, handoff.
8. **Advanced**: full exact source \`instructions\` prompt, raw ID, JSON contract, event log, policy, hashes, origin revisions.

The page should provide a "View original instructions" disclosure so operators and agents can inspect the exact saved prompt without imposing JSON on every manager. Any summary must be a faithful, attributable derivative, not a replacement for source.

### Search, filtering, zoom, grouping

- Default "overview" uses 5–8 semantic phases, each with completion/readiness counts. Expand a phase for six independent audience lanes, or switch to "All steps" full graph. Show merges/joins with arrows; no false independent edges.
- Provide a lane selector ("All", "HVAC", "General trades", "Meta marketers", "Agencies", "Life insurance", "Small businesses"), phase filter and status filter, including **Review ready** and **Needs rework**.
- Active blocker ribbon: plain text explanation and link to exact tasks/reviews. An absent \`BLOCKED\` task status must not hide an active run-level blocker.
- Include keyboard operation, adequate contrast, responsive panel and outline; use no external fonts/scripts/telemetry for local private mode.
- Accessibility: ensure links are actual, keyboard focus visible, all status differences described in text and screen reader descriptions include plain titles not raw IDs.

## A fully transferable example: research competitor ads

This is a SPECIMEN Step Brief, not a claim that the existing Bucket 9 source contains every reference below.

**Task:** Research HVAC companies' Facebook and Instagram advertising
**Purpose:** Find dated competitor ad examples relevant to owners of HVAC installation businesses to inform a proposed ad angle. Do not infer advertising performance from mere presence of an ad.
**Audience/market:** HVAC installation and replacement business owners, United States and Canada as applicable; separate country evidence.
**Start here:** pin exact AOS-W run and graph from \`aos-w/agent-files/instances/<instance-id>/\`; read saved input reports and last checkpoint before research.
**Source:** Meta Ad Library, https://www.facebook.com/ads/library/ . Sometimes described colloquially as "Ads Gallery." If the workflow instead means another distinct proprietary **Ads Gallery**, author MUST provide its real canonical URL, account access, search procedure and source record; do not assume it is identical to Meta Ad Library.
**Other required materials:** exact historic research report, evidence log and scorecard, all from pinned versioned paths in the active run or linked source portfolio. No unspecified "previous research" references.
**Required access:** browser-readable public ad library; specific country/category filters (record selected values), source reading permission, workspace write access restricted to task artifacts. If the ad gallery is unavailable, record UNVERIFIED/UNAVAILABLE and preserve the gap; do not invent ad IDs.
**How:** (1) load source reports, (2) identify advertiser names and keywords, (3) select country and ad category in library, (4) capture ads with advertiser/page, displayed ad ID or stable URL where available, text/creative summary and observed timestamp, (5) cross-check and mark any inaccessible examples, (6) distinguish verified observations from hypotheses, (7) write result to declared artifact path, (8) request the exact independent reviewer gate. Capture authorization and no-scraping restrictions.
**Outputs:** \`research-six-verticals.md\` (dated source observations, confidence, limitations); \`evidence-log.csv\` or existing approved equivalent; exact hash/version references; next review task pointer.
**Acceptance:** dated traceable source entries, correct audience definition, no invented live/ad performance claims, QA review by distinct verified independent agent or explicit BLOCKED/REVIEW_REQUIRED.
**Forbidden:** publish ads, alter budgets, claim campaign results or independently approve your own submission.

If the needed input filename, source URL or tool identity is absent, the step brief must say **"Missing required reference — cannot reproduce independently"**, not imply readiness. A cold-start operator follows only this brief and linked saved materials.

## Minimum typed Step Brief v0.9 proposal

Use a separate validated optional \`human_step_brief\` object or adjacent file, not raw unvalidated inline HTML:

\`\`\`yaml
id: hvac-installation-owners--qc-research  # stable identity
title: Review HVAC competitor research     # human
summary: Independently verify sources, audience and claims before preparing ads.
phase: {id: independent-review, title: Check the research}
lane: {id: hvac-installation-owners, title: HVAC businesses}
status_summary: Waiting for independent review
purpose: Confirm that the dated research supports proposed ad claims.
context:
  project: Bucket 9, six-audience Wave 1
  workspace_root: <exact authorized repo/workspace path>
  pinned_graph: g0004
  run_id: run-001
  source_ref: <hash/path of saved step and reviewer source>
resources:
  - name: Meta Ad Library
    aliases: [Ads Gallery, Facebook Ads Library]  # only if these refer to same verified service
    url: https://www.facebook.com/ads/library/
    use: Check actual advertiser ad cards and dated source examples.
    access: Browser access required; exact country/filter to be recorded.
    verification: NOT_YET_RECHECKED
inputs: [{label: HVAC research record, path: <real versioned path>}]
procedure:
  - Read exact saved research and evidence.
  - Check source citations and distinct claims.
  - Save a reviewer verdict with evidence.
outputs: [{label: Research QC verdict, path: <exact review path>}]
done_when: Current exact research artifact gets an independent PASS.
quality: {kind: independent-ai, requires_distinct_actor: true}
permissions: {allowed: [read, review], forbidden: [stage_paused, activate_live, change_budget]}
blockers: [No independently verified PASS yet.]
resume: Read the current handoff and last event before claiming the task.
\`\`\`

Replace all angle-bracket placeholders with real values before declaring any brief runnable; the examples are intentionally incomplete. Source/role identity must be verified on the host, not by a user-authored YAML claim.

## GitHub Pages presentation contract

**The problem:** \`https://github.com/<owner>/<repo>/blob/main/.../index.html\` is a code browsing page; it does not execute the embedded SVG/JS diagram as the user's interactive web page.

**Preferred solution when using GitHub and hosting is approved:** link to the **actual deployed Pages site**, verified by visiting that URL and checking title, embedded revision/event and expected node count.

Decision:
- If data are confidential and verified **private Pages** access control exists: ask for explicit publication approval for this private access-controlled destination, deploy only under protected role and verify restricted access.
- If the preview is sanitized and owner explicitly accepts public distribution: export the minimal public-safe snapshot to a dedicated Pages source, deploy, and confirm it is accessible.
- If a private repo lacks a verified private Pages capability: **do not deploy raw private run HTML to public Pages**. Instead render in an authenticated workspace browser/preview or provide a directly accessible single HTML file via a suitable authorized private host. Explain why GitHub raw/source view is not an interactive page.
- If neither render nor host is supported, give an HTML attachment, never a ZIP as default. If user specifically insists on a public site, request scope-specific permission and sanitized content review.

Avoid links formed by guessing \`<owner>.github.io/<repo>\`. Use the actual returned published URL and confirm readback. Pages is a static site and not an always-on watcher. Proposed private rollout requires a verified hosting account and access model; a private GitHub repository alone does not guarantee private website visibility.

## Acceptance examples linked to source screenshot

- Main header shows \`Bucket 9 · Six-audience rollout\`, with "56 steps" in a secondary caption, no exposed machine slugs by default.
- Instead of "STAGE 1", use "Research advertisers"; instead of "STAGE 2", use "Check research"; avoid semantically false grouping based solely on dependency depth.
- Cards display "Research HVAC companies" and "Review HVAC research", not \`hvac-installation-owners--qc-research\` twice.
- Count six READY review nodes as "6 reviews ready" and zero finished reviews separately; do not show "Review 0" as the only QC summary.
- Opening an ad-research step reveals clickable "Meta Ad Library" and the workflow's actual "Ads Gallery" tool mapping if relevant, not merely an unexplained URL or absent dependency.
- A previously uninvolved human/AI given only the saved repo and Step Brief can locate the right inputs, source service, exact procedure, output and QC gate without asking "what ad gallery?" or "what did you mean previously?"
- If the only available URL is a GitHub blob, label it "Source file (not rendered)" and do not present it as an "Open interactive webpage" action.
- Published private data must have actual tested private-site access control or else the deployment is blocked. Public output must have separate sanitized approval and no private source file copied to the Pages root.
