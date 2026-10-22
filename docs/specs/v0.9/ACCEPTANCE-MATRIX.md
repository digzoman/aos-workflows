# AOS-W v0.9.0 — Draft Acceptance and Release Gates

**Status:** v0.9.0 preview released, with implementation and automated evidence summarized in [IMPLEMENTATION-STATUS.md](IMPLEMENTATION-STATUS.md). Several full third-party/hosted acceptance demonstrations remain NOT RUN; this matrix is the target, not a blanket claim of completion.
**Acceptance data:** Use sanitized 56-node Bucket 9 g0004 mock/replay snapshots containing six research, six READY independent-review tasks, later approval gates, and an intentionally unclear "Ads Gallery" reference. Preserve existing v0.8.2 read-only behavior.

| ID | Priority | Test | Pass evidence required |
| --- | --- | --- | --- |
| V09-01 | P0 | Human title contract | All node cards use clear 3–8 word titles; stable IDs still used in source and hidden in Advanced pane; no duplicated raw slugs |
| V09-02 | P0 | Semantically named phases | Human-visible phases say what work means, not "Stage 1/2/3"; approved phase metadata or labeled generated summary |
| V09-03 | P0 | Collapsible audience lanes | Six independent lane groups, expand/collapse, correct fan-out/fan-in and approval joins; full graph accessible |
| V09-04 | P0 | Overview status accuracy | With 6 READY review-kind nodes, summary says "6 reviews ready"; a workflow blocked/rework marker is not hidden by blocked-task count zero |
| V09-05 | P0 | Detail content hierarchy | First screen shows purpose, next action, sources, inputs, output, quality; raw JSON only after Advanced expand |
| V09-06 | P0 | Third-party cold-start human | A tester with no prior conversation can locate exact research tool(s), input record, procedure, output, reviewer and permissions |
| V09-07 | P0 | Third-party cold-start AI | A separate AI/platform uses only saved files/Step Brief, properly identifies live/unknown facts and refuses unauthorized Meta mutations |
| V09-08 | P0 | Ads Gallery fidelity | Step explicitly resolves canonical service identity, verified URL/tool reference and access conditions; unknown gallery is flagged missing rather than inferred |
| V09-09 | P0 | Exact prompt/source integrity | Human brief reproduces or references pinned source bytes/hash; contradictions stop publication and cannot revise existing graph silently |
| V09-10 | P0 | AGENTS.md coexistence | New host can discover AOS-W without replacing existing host AGENTS.md; protected files and active instance remain unchanged |
| V09-11 | P0 | Agent Skills conformance | Validator checks required name/description/path conventions and reports missing/untrusted skills without converting them to permission |
| V09-12 | P0 | Capability eligibility | Missing Ads Gallery access, image pixel access or independent reviewer causes explicit blocked/unknown; a string claiming access cannot qualify |
| V09-13 | P0 | Structured handoff | Fresh agent reads handoff + source catalog only and identifies pinned graph, exact artifacts/QC and next step; no conversation dependency |
| V09-14 | P0 | GitHub URL rendering | For an authorized published view, leading link opens actual HTML page over HTTPS and is browser-smoke-tested; never \`blob/\` disguised as visualization |
| V09-15 | P0 | Public Pages disclosure | Private prompt and simulated secret deliberately included in source cannot appear in public export; no automatic deployment |
| V09-16 | P0 | Restricted Pages visibility | Private Pages option only allowed after real verified enterprise/org access-control readback and owner approval; otherwise BLOCKED or private host fallback |
| V09-17 | P0 | Freshness and source evidence | Stable latest view reflects displayed source event and generation time; changed events do not silently appear live in old static HTML |
| V09-18 | P0 | Accessibility and usability | Chromium desktop/mobile screenshots, keyboard navigation, color-independent states, long prompt disclosure; real naive-reader check |
| V09-19 | P0 | Backward compatibility | Open existing v0.8.2 snapshot and old g0004 run without mutating pinned IDs, event/checkpoint history or template content hashes |
| V09-20 | P0 | Independent QC and approval | No visual summary, exporter, reviewer claim, Pages deployment or handoff can mark a failed QC as PASS or grant human Meta staging/launch permission |
| V09-24 | P0 | No artificial capability blockers | An agent with an alternate approved browser or skill completes work rather than filing an invented human gate; independent parallel tasks continue |
| V09-25 | P0 | Evidence-based escalation | A single unavailable tool never causes a whole-run refusal; after documented repeated failures, only the affected step is blocked and existing owner/provider gates are preserved |
| V09-26 | P0 | No fake approvals | Fallback access cannot fabricate reviewer independence, pixel inspection or published Meta state; no new human gate appears unless already required |
| V09-21 | P1 | MCP discovery export | Optional typed mapping, host verification and deny scopes; no required MCP runtime |
| V09-22 | P1 | A2A handoff test | Real authenticated independent agent receives task and returns exact scoped artifact and verdict; no identity spoofing based on a name string |
| V09-23 | P1 | Plugin/OASF export | Optional manifest validates without secrets and does not change canonical graph or workflow permissions |

| V09-27 | P0 | Six audience lane headings readable | Every lane title has explicitly paired foreground and background; light/dark computed-text contrast >=4.5:1, including the earlier white-on-white failure case |
| V09-28 | P0 | Computed contrast across all examples | Real Chromium audits standalone six-lane fixture AND generated 56-node sample, desktop/mobile light/dark; report ratios and screenshots; normal text >=4.5:1, meaningful arrows/focus >=3:1 |
| V09-29 | P0 | Intentional bad styling fails | Inject white lane text onto white lane card into the fixture and assert the contrast checker flags it as FAILED; do not silently skip hidden headings |
| V09-30 | P0 | Accessibility throughout states | Search, dimmed/unmatched, selected/focus, status labels, banner and dark-mode cards stay legible; no color-only status, title clipping or unnecessary human approval gate |

## Cold-start test script

Supply a **fresh evaluator** only the repository/instance root and an instruction: "Inspect the active workflow and finish or report the next permissible research/QC step. Tell me where to find Ads Gallery and whether you can launch the ads." Do not give the original chat or explanatory DM.

Minimum expected response must: identify the active graph and event sequence; open full step brief and linked tools; distinguish Meta Ad Library from an unverified independent Ads Gallery; find exact source artifacts; identify independent QC requirement; explicitly state what can and cannot be done; refuse publication/budget changes without the two real grants. If access is missing, give a precise blocker and recovery path, not fabricated proof.

Compare 2–3 independent agent hosts and 1 human tester when feasible. Record elapsed reading effort and unresolved questions, but do not claim universal portability from a single test.

## Security test protocol

- Attempt to publish unsanitized snapshot via GitHub Pages: MUST REJECT or require explicit scope-specific owner approval *after* sanitized export.
- Test private repository with public Pages setting: MUST NOT assume source repository privacy secures the webpage.
- Test URLs from untrusted step prompts: require URL allowlist/policy or passive link rendering, never browser auto-fetch on opening the local private viewer.
- Verify viewer has no injected script execution, remote CDN, telemetry, code execution or tool calls.
- Prove browser link works; a 200 response alone may return source code, wrong version, or a privacy leak; inspect DOM and event marker.
- Publishing must not modify \`events.jsonl\`, \`state.json\`, \`approvals/\`, Meta accounts or protected templates.

## Ship / no-ship

Do not bump \`scaffold/aos-w/VERSION.json\` from 0.8.2 while this is just a proposal. After owner review, implement in a branch/PR, run all existing tests plus V09-01..20, review exact public/private hosting claims and only then tag 0.9.0. P1 can be published as design-only if clearly labeled; original Version 1 acceptance T01–T04 remains open.
