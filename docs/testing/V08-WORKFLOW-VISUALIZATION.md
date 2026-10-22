# AOS-W 0.8 workflow visualization execution and test evidence

Review and feature date: October 22, 2026.
Status: additive v0.8.0 portable preview PUBLISHED, controlled code/CLI acceptance PASS, manual browser visual smoke still pending.
Implementation: docs/specs/visualization/V0.8-SPEC.md.
Portable read-only viewer: scaffold/aos-w/references/visualization-viewer.html.
Portable no-code guide: scaffold/aos-w/references/VISUALIZATION.md.
Portable contract: scaffold/aos-w/spec/schemas/visualization-snapshot.schema.json.
Writable clean seed: scaffold/aos-w/agent-files/visualizations/README.md.
Optional developer converter: scripts/aosw-visualize.py.
Sample data: examples/visualization/bucket9-stage.json.
Tests: tests/test_visualization.py, 19 added standalone checks.

## Actual hosted evidence

GitHub Actions 39741816281 completed SUCCESS:
https://github.com/digzoman/aos-workflows/actions/runs/39741816281

- 145 total unit/conformance tests PASS, including 19 visualization tests.
- Actual dependency-free offline HTML generated from 21-node marketing-lifecycle-compound TEMPLATE, status SOURCE_SNAPSHOT_UNVERIFIED.
- Actual self-contained HTML and snapshot.json generated from sanitized 11-node Bucket 9 RUN example, status SOURCE_SNAPSHOT_UNVERIFIED.
- HTML/JSON files saved strictly in ephemeral runner path ending in aos-w/agent-files/visualizations/<view-id>/, rather than under protected source.
- Sanitized Bucket 9 example HTML/JSON archived in GitHub Actions artifact aos-w-v08-interactive-visualization-demo, ID 12409532047.
- Portable ZIP build/verify/install/upgrade smoke passed. Published preview v0.8.0-portable-preview asset aos-w-portable-0.8.0.zip, SHA-256 0c0bd727d8c29b98662d7ab44e8358a96fbcfab95e4e699a8d8e550080834b80.
- v0.8 specs and current installation docs are in source; v0.7 marketing templates/child module version identifiers are unchanged.

## 19 visualizer-specific automated checks

1. Viewer is local/offline and has SVG arrows, no fetch/CDN.
2. Sanitized 11-node demo passes visualization JSON Schema and retains blocked approval status.
3. Drawer source code includes exact instruction, QA, output and evidence fields.
4. Script-like malicious prompt string is escaped inside embedded application/json script, not executable HTML.
5. Real research-starter YAML converts with 3 declared template-only nodes and NOT_STARTED statuses.
6. Real 21-node compound marketing template includes child generation and joins.
7. Synthetic state overlay preserves recorded status and labels reconciliation as unverified.
8. Missing YAML graph dependency rejects conversion.
9. Cyclic YAML graph rejects conversion.
10. Duplicate YAML node IDs reject conversion.
11. Output outside agent-files/visualizations rejects writes.
12. Symlink output directory rejects writes.
13. Snapshot/HTML files written and preserve synthetic withheld launch gate.
14. ZIP allowlist permits protected HTML guide and clean visualization README, not private view content.
15. No automatic provider publication/GitHub Pages behavior is introduced.
16. Prepared JSON snapshot rejects duplicate node IDs.
17. Prepared JSON snapshot rejects cycles.
18. Overlength exact prompt rejects conversion instead of silently truncating.
19. Prepared JSON snapshot rejects unknown dependency references.

## Remaining UI/verification limits

The hosted test actually generated two self-contained webpages and archived the public sanitized sample, but this job did NOT open a browser for human visual inspection of arrow geometry, keyboard focus, printed layout or mobile viewport. The JS/CSS interface is reviewed structurally, not visually certified. Browser-level smoke and usability refinements should be an 0.8.x follow-on before advertising cross-browser compatibility as proven.

The generator treats run state as SOURCE_SNAPSHOT_UNVERIFIED unless a host separately validates the authoritative journal and reviewer records. Pages is suggested as a separately authorized/public-safe fallback, not automatically deployed or tested. The page does not perform task execution, approvals, coordination, provider API calls or live refresh.

No stable Version 1 declaration. T01 actual end-to-end Ampgent acceptance, T02 cross-platform AI handoff, T03 hosted CAS locking and T04 independent AI QA remain open from Prompt 19. Visualization is an additive 0.8 preview capability and did not modify those criteria.

## Extended executable implementation and browser test

After the original preview, extra tests were added for the real persisted Bucket 9 parent run stored in docs/testing/evidence/p18-grounded-39498378421. The visualization CLI now verifies its actual event ledger/checkpoint status, exact graph revision, rejected invalid event history and preserves UNVERIFIED labels for optional advisory mode. The viewer includes a short metadata-only activity history, human approval policy and child template reference on step drilldown.

A separate dedicated GitHub Actions workflow .github/workflows/aosw-v08-browser.yml generates actual HTML and drives headless Chromium to check SVG dependency edges, click and keyboard drilldown, desktop/mobile layout, search behavior, false publication status and lack of network requests. It archives screenshots and test results. The browser result should be checked by its actual CI conclusion before representing this as verified.


## Final v0.8.1 code and browser acceptance evidence, October 22, 2026

The original 0.8.0 was the first visualization preview. The code has since been materially extended and shipped as a new immutable **0.8.1 patch preview** rather than silently replacing the same GitHub release ZIP.

Changes implemented in main:
- From any active AOS-W run, use `python scripts/aosw-visualize.py --run-dir <path-to-run>` to auto-discover the pinned graph and saved state, verify journal event chain and checkpoint anchors where available, and create the page under the installation's own `agent-files/visualizations/`.
- Read-only selected step now shows a bounded journal activity history, the precise current event sequence, policy/approval requirements, artifacts, review metadata and all original prompt text.
- For a published compound marketing template, the generator resolves sibling child module templates only after verifying exact SHA-256 pinned content and version. Nested expandable child steps show their actual prompts, inputs, expected outputs, QA gates and done_when. Mismatched/missing pins refuse child expansion.
- Corrupt/tampered journal, wrong graph digest, mismatched state, duplicate/cyclic graph IDs, unsafe output path or out-of-policy prompt all block validated rendering rather than produce misleading progress.
- Public GitHub Pages is NOT enabled; no web server, provider writes, tracking, remote scripts or live automatic refresh.

Verifications:
- Hosted CI release audit 39747746118 SUCCESS, 152 conformance/unit tests including 26 visualization tests, and 13/13 practical standalone 0.8.1 cases PASS.
- Hosted CI build 39747745980 SUCCESS and published 0.8.1 preview ZIP at https://github.com/digzoman/aos-workflows/releases/tag/v0.8.1-portable-preview.
- Independent desktop/mobile headless Chromium run 39747505741 SUCCESS, 9 browser checks including all arrows, accessible click/keyboard selection, search, full selected prompts/QC, mobile layout, nested verified child module expansion and zero outgoing network requests/JS errors.
- Browser screenshots/evidence: https://github.com/digzoman/aos-workflows/actions/runs/39747505741/artifacts/12411797423
- Published archive SHA-256: 3357d523e576180b65036c80e149517f658a6920b228d03db28d15826894a91b.
- GitHub release uploader changed to never overwrite an existing published tag asset. New release content requires a version increment.

Outstanding outside v0.8.1 scope: live state auto-refresh without a verified agent watcher, real GitHub Pages deployment (intentionally unapproved), a native cross-agent collaborative viewer, and original stable V1 acceptance T01–T04. No owner authorization to publish Meta, change spend, create Pages or share private customer/workflow data.


## v0.8.2 HTML-first visualization presentation

The agent-facing display rule now prefers an actual HTML/browser preview and direct single index.html file link/attachment over zipped visualization artifacts. ZIP remains allowed when forced by the platform, explicitly requested or needed for a multi-file evidence bundle, with clear file-opening instructions. The versioned AOS-W multi-file framework package still uses ZIP. GitHub Pages remains optional, sanitized and approval-gated.
