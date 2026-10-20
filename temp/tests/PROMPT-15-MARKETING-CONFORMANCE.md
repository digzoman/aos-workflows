# Prompt 15 — marketing template library conformance (2026-10-20)

**Status:** Locally implemented and conformance-tested against reconstructed AOS-W 0.6.0 source plus new 0.7.0 modules. No real ad account, CRM, image generator, customer data, or external provider was accessed. GitHub-hosted workflow and release status require separate post-commit verification.

## Deliverables

- **21 independently usable marketing templates**, each with named parameters, stable node identifiers, explicit artifact input/output contracts, dependency DAG, step QA and bounded local actions. Research planning, keyword discovery, competitor execution, research independent QC, evidence consolidation, opportunity scoring, offer hypothesis, verified deliverability, ad copy, creative brief, image generation, creative QA, brand, Meta preparation, CRM preparation, landing page preparation, tracking verification, integration readiness, human launch permit, monitoring and optimization.
- **1 compound lifecycle**, SHA-256- and version-pinning all 21 components; a reviewed research fan-out proposal and all-accepted evidence join; parallel implementation preparatory branches; explicit final integration join; human launch gate. Parent *defines* composition, not an automatic executor.
- **Three provenance types**: observed competitor offer != proposed seller-offer hypothesis != genuinely verified deliverable human-approved product/service offer. Public data is fictional/sanitized.
- **Human-only default live publication approval** and distinct paused staging/PROD deployment/budget permission classes. All tasks permit only local file actions by default. No launch activation node. No actual Meta provider change executed.
- Bundled task-local evidence-claims SKILL.md, standalone catalog and manual guide. Sanitized source lineage to Prompt 03–05 historical documentation.
- Six genuinely initialized fixture run records in CREATED status with template lock, event, state and handoff; three independent research siblings and CRM/landing independent stubs plus compound parent. Separate `-MOCK.json` data demonstrates fan-out, parallel readiness, failure/blocked gates; no fixture represents actual executed research or quality approval.
- Updated compound-template JSON Schema to support explicit human `gates` with no new required fields; both source and bundled copies must match.

## Local tests actually executed

- **18 new marketing conformance tests PASSED**, including JSON Schema Draft 2020-12 validation of every module with cross-file refs, acyclic graphs, all outputs/gates/input references, stable SHA-256 composition pins, human action restrictions, dynamic research join blocked without real reviews, image capability fail-closed, independent instantiation, mock provenance, source truth boundaries, secret scanning of new fixtures, and clean ZIP packaging with the new bundled marketing catalog.
- **126 total local regression tests PASSED**, including prior 108 tests. Local run via `python -m unittest discover -s tests -p 'test_*.py' -q` completed in approximately 31 seconds.
- Optional initializer instantiated `marketing-offer-strategy` under a temporary arbitrary directory, preserved exact master YAML bytes, initialized CREATED state, no completed tasks; status remained advisory and not authorized to execute.
- Existing safe ZIP packager allowlist expanded **only** to `templates/MARKETING-LIBRARY.md`; this does not include any user-owned `agent-files` content.

## Security and implementation boundaries

Template metadata/README is not authentication, an independent reviewer, true product capability, provider configured state, delivery, nor human spending permission. Parent `composition.children` source placeholders are manual bindings; no automatic child execution or authenticated cross-system integration yet. A `launch-permit` gate requires current authenticated owner authorization at the provider boundary. Without approved versioned offer/campaign/CRM/site/tracking evidence, downstream actions remain blocked.

## Still not proven by these tests

- Actual Meta Ads Library accesses, source ad archival, Meta/GHL/website readback and provider writes; actual image creation/pixel quality inspections.
- Real independent AI or authenticated human review execution; environment-specific hard authority/fencing; Git-hosted CAS/LFS multiagent tests.
- New 0.7.0 GitHub Actions build, public preview release and cross-platform host installation until the hosted run is examined after commit.

Next Prompt 16 should perform real standalone local/cloud interruption/recovery, file-only agent cold starts and broader acceptance tests on **actual authorized** or explicitly simulated environments, without conflating fixtures with live provider actions.
