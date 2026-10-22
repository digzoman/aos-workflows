# AOS-W v0.9 — Human-first workflow and transferable step brief

A workflow should make immediate sense to a human or a fresh AI agent with access to the same authorized repository. Each step needs a clear action-oriented \`title\`, one-sentence \`summary\`, meaningful \`phase\`, and optional \`lane\`. Internal identifiers stay unchanged and are shown only under technical details.

An executable step brief answers: **what**, **why**, **where to start**, **what tools/resources**, **what to read**, **what to do**, **what to produce**, **how to check**, **what access is needed**, **what to do on failure**, and **what work comes next**. Precise source artifacts, paths, URLs, scope and versions must be grounded in the pinned graph. An AI may propose helpful contextual public sources, but must label them **suggested, not verified or used**.

For advertising workflows, explicitly name **Meta Ad Library** (\`https://www.facebook.com/ads/library/\`) where relevant as a suggested public research resource. If the user meant a distinct "Ads Gallery", identify the actual URL and required account; do NOT claim it is the same product without verifying. Include country/category/time filters and dated evidence requirements, and do not infer ad spend/results from visible ads.

When a resource/tool isn't immediately accessible, apply [CAPABILITY-RECOVERY.md](CAPABILITY-RECOVERY.md). Resourcefulness, alternate tools, autonomous safe progress and narrow evidence-based blockers are required. Do not invent user gates.

The AOS-W viewer should default to plain-English labels and phase/group overview, accurate counts of **READY independent reviews**, and an understandable next action. The sidebar starts with the step brief, with original exact instructions, JSON policies, stable IDs and provenance in a collapsible Advanced section.

**Delivery:** If an agent can render local HTML, show that view. If a GitHub-hosted browser page is requested, prefer a VERIFIED rendered Pages URL after necessary privacy/visibility and publication authority checks. Never link a GitHub blob page as if it were interactive, or auto-publish sensitive private prompts. A self-contained HTML file via an authorized file host is the fallback. The multi-file AOS-W *installer* remains a ZIP.
