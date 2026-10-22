# AOS-W preview release change notes

## v0.8.1 portable preview, October 22, 2026

Final implementation polish for v0.8 workflow visualization, including one-command rendering of real saved runs with verified event-ledger checks, immutable pinned-graph matching, bounded per-step journal activity, exact effective approval policy, SHA-256 pinned nested child-module prompt/QA drilldowns, cycle/hash/path fail-closed checks, and confirmed real Chromium desktop/mobile/keyboard/arrow browser smoke. 152 CI conformance tests and all 13 standalone acceptance cases passed, plus 9 browser checks. This patch is a new versioned preview, not a stable Version 1 release. Existing marketing template 0.7 pins remain unchanged. Publishing tooling now preserves existing versioned release assets rather than overwriting them.


## v0.8.0 portable preview, October 22, 2026

Introduced a **read-only interactive workflow visualization** capability. Agents can construct a local single-file HTML/SVG diagram for any template, pinned instance or workflow run, show dependency arrows, statuses, parallel branches/joins and click-to-inspect exact prompts, inputs, outputs and quality/approval contracts. Installed reference viewer and JSON Schema do not require Git, Python, CDN or a web server; visualizations are generated only inside agent-files/visualizations. An optional developer Python/YAML converter and a sanitized 11-step Bucket 9 example are included in the development repository. Publishing via GitHub Pages remains opt-in and requires explicit sanitized owner-approved export, never automatic. The existing 21 marketing modules retain their pinned 0.7.0 template versions.

New executable conformance checks cover source graph conversion, schema, offline viewer, security escaping, cycle/dependency rejection, user directory protection and safe packaging. This remains a preview and does not satisfy the four outstanding stable V1 acceptance tests T01–T04.


## v0.7.0 portable preview, October 20, 2026

This is a PREVIEW release, not stable Version 1.

Added 21 independent sanitized marketing workflow templates plus one compound research-to-staged-campaign lifecycle. Added a source-claim skill, distinct observed-competitor versus offer-hypothesis versus owner-verified deliverability classes, safe mock marketing fixtures and 18 additional conformance tests.

The 0.7.0 source schema initially rejected compound quality gates in hosted validation. Commit a7b7e8ac corrected the source and bundled schema. GitHub Actions run 39434478250 then passed 126 conformance/regression tests, built a SHA-256 manifested portable archive, and verified its installation smoke test. Published preview ZIP SHA-256: 0826ddf9807354e80e22b757dd129b86539aae8d6ff3c7799029e5f3719c74f7.

New synthetic Prompt 18 hosted test at run 39495294275 passed with 77 actual local AOS-W file/event transitions. It does not qualify as a real marketing production pilot or prove external integrations.

Existing limitations: no mandatory runtime and no automatic scheduler, no authenticated owner approval, no host-enforced external operation authority, Git coordination still experimental, external skill fetching not proven, genuine multi-provider AI handoff not demonstrated. Do not self-publish.

Download: https://github.com/digzoman/aos-workflows/releases/tag/v0.7.0-portable-preview

## v0.6.0 portable preview

First independently packaged clean ZIP including optional deterministic build/install/upgrade tooling, safe preservation of user agent-files, hosted 108 regression tests and an actual local standalone offline acceptance workflow with 13/13 cases passed. See docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md.

The changelog records preview development evidence. Release approval remains HOLD in docs/release/V1-READINESS-2026-10-20.md.
