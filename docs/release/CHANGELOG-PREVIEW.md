# AOS-W preview release change notes

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
