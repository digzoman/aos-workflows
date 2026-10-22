# AOS-W v0.9 — Human-first workflow and transferable step brief

A workflow should make immediate sense to a human or a fresh AI agent with access to the same authorized repository. Each step needs a clear action-oriented \`title\`, one-sentence \`summary\`, meaningful \`phase\`, and optional \`lane\`. Internal identifiers stay unchanged and are shown only under technical details.

An executable step brief answers: **what**, **why**, **where to start**, **what tools/resources**, **what to read**, **what to do**, **what to produce**, **how to check**, **what access is needed**, **what to do on failure**, and **what work comes next**. Precise source artifacts, paths, URLs, scope and versions must be grounded in the pinned graph. An AI may propose helpful contextual public sources, but must label them **suggested, not verified or used**.

For advertising workflows, explicitly name **Meta Ad Library** (\`https://www.facebook.com/ads/library/\`) where relevant as a suggested public research resource. If the user meant a distinct "Ads Gallery", identify the actual URL and required account; do NOT claim it is the same product without verifying. Include country/category/time filters and dated evidence requirements, and do not infer ad spend/results from visible ads.

When a resource/tool isn't immediately accessible, apply [CAPABILITY-RECOVERY.md](CAPABILITY-RECOVERY.md). Resourcefulness, alternate tools, autonomous safe progress and narrow evidence-based blockers are required. Do not invent user gates.

The AOS-W viewer should default to plain-English labels and phase/group overview, accurate counts of **READY independent reviews**, and an understandable next action. The sidebar starts with the step brief, with original exact instructions, JSON policies, stable IDs and provenance in a collapsible Advanced section.

**Delivery:** If an agent can render local HTML, show that view. If a GitHub-hosted browser page is requested, prefer a VERIFIED rendered Pages URL after necessary privacy/visibility and publication authority checks. Never link a GitHub blob page as if it were interactive, or auto-publish sensitive private prompts. A self-contained HTML file via an authorized file host is the fallback. The multi-file AOS-W *installer* remains a ZIP.


## Required color/contrast safeguards for agent-generated workflow HTML

Avoid a repeat of the chat-generated **"Six parallel audience lanes"** headings that were nearly white on white. **Never assume the ChatGPT host, code highlighter, GitHub Pages theme or browser will supply a suitable heading color.** Pair the actual CSS text and background colors on audience headings and all semantic workflow labels. Use at least WCAG 2.2 AA **4.5:1 for standard text**, **3:1 for meaningful non-text edges/controls**, and make statuses readable in words without depending only on color. In the canonical AOS-W viewer use \`--aw-lane-fg\` and \`--aw-lane-bg\`, not inherited heading styles.

Verify desktop/mobile and light/dark using \`scripts/aosw-contrast-audit.py\` where available; it creates four screenshots and a JSON report. If that tool isn't available in an agent-only portable install, use authorized browser inspection, other available capabilities and a programmatic color calculation rather than deferring work. No extra human gate is introduced. Regenerate/repair failing HTML autonomously before claiming it is ready to view. See \`docs/specs/v0.9/V0.9-PRODUCT-SPEC.md\`.
