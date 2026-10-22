# AOS-W 0.9.2 Implementation and Remaining Acceptance

Date: October 22, 2026.
Status: SHIPPED PREVIEW, not stable Version 1 approval. Current portable version 0.9.2. See V0.9-PRODUCT-SPEC.md and ACCEPTANCE-MATRIX.md for the target specification.

## v0.9.2 accessibility verification

- Readable six-lane headings use paired foreground and background colors in light, dark and forced-colors themes. Explicit focus states and legible workflow arrows are required.
- A Chromium audit exercises the six-lane fixture and generated workflow in desktop and mobile light/dark modes. The audit enforces at least 4.5:1 text contrast and 3:1 meaningful non-text contrast, and deliberately rejects a white-on-white lane-title mutation.
- Verification on commit `8a04c57d92203a1f20324b5f32fff8d5b781bf34`: [browser accessibility acceptance passed](https://github.com/digzoman/aos-workflows/actions/runs/39864824024), [Version 1 readiness audit passed](https://github.com/digzoman/aos-workflows/actions/runs/39864816925), and [portable preview built and published](https://github.com/digzoman/aos-workflows/releases/tag/v0.9.2-portable-preview). The complete unit suite ran 162 tests successfully.
- This demonstrates the checked accessibility scenarios, not complete WCAG certification, external human usability acceptance, private Pages authorization, or stable Version 1 acceptance.

## Implemented and tested
- Human-first offline HTML workflow viewer: readable generated labels, semantic phase names, overview-first navigation for larger workflows, workstream/status filters, quality review READY counters, task detail drawer with actionable next step and source references, original instructions and machine JSON accessible under Advanced.
- Portable human step brief projection derived from saved instructions and existing graph state; includes named tools, source references, access guidance, task inputs/outputs, current status, scope and explicit source provenance. All generated titles are marked GENERATED_FROM_ID until an actual approved author title exists. Exact source prompt preserved, never silently rewritten.
- AOS-W root and installed AGENTS.md entry point. Existing host AGENTS.md files are not overwritten by the normal installer.
- Advisory, non-gating Agent Skills checker and proactive capability recovery policy. Agents are directed to try available tools, switch to authorized alternatives and continue unrelated work; no capability flag adds a human approval checkpoint.
- New synthetic 56-node, six-audience workflow, portable schema support and browser acceptance checks, with real read-only approval boundaries and no provider execution.
- GitHub Pages workflow and privacy preflight coded for a deliberately fictional, public-safe sample, manual/opt-in only; publication settings and actual rendered site URL remain to be verified by a responsible repository administrator.

## Not proven or intentionally not implemented
- A complete independent human and external AI cold-start exercise using the new Step Brief has not been demonstrated yet; this remains important acceptance work.
- Automated refresh of a live private GitHub Pages deployment, independent agent capability dispatch with verified connectors, and secure private Pages access are not available as general portable features.
- A2A, MCP runtime, agent plugins, OASF mapping and OpenTelemetry exports remain optional planned adapters. No server/plugin/cloud runtime is required for standalone.
- No GitHub Pages site has been deployed by this task. The manual fictional example can be deployed after its hosting environment is authorized and configured. A private source repo alone is NOT evidence of private website visibility.
- Stable Version 1 T01 real full marketing E2E, T02 real cross-platform AI handoff, T03 hosted exclusive CAS coordination and T04 independent AI QC original acceptance remain open.

## Owner clarification enforced

**Tool/capability checks should make capable agents more effective, not become excuses to stop.** Before escalating, discover working tools, use existing connected services, try safe alternatives, continue safe parallel work, and report a specific reproducible blocker only when mandatory evidence or authority is genuinely impossible. Do not introduce new human gates for ordinary tool limitations. Preserve only the already approved human requirements for consequential provider, spending and launch actions.

## Public/private guidance

For an actual private workflow, prefer authenticated HTML preview. For explicitly approved public-safe demos, a working rendered Pages URL is preferable to a GitHub blob link. A standalone HTML file (not ZIP) is the fallback. The framework installer remains ZIP.
