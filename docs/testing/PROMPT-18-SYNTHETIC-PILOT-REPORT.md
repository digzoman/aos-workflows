# Prompt 18 executable staged marketing pilot, partial acceptance

Date: 2026-10-20
Status: CONTROLLED SYNTHETIC PILOT PASSED, ORIGINAL T01 STILL NOT DEMONSTRATED.
Commit: 0863e3f01807ff99cb7821d47aef69358618de81
CI: https://github.com/digzoman/aos-workflows/actions/runs/39495294275

## Actual execution

GitHub Actions ran tests/acceptance/run_marketing_pilot.py against AOS-W's actual tools/state/RunStore. The job completed SUCCESS. Job log explicitly reports 77 persisted workflow events and launch NOT_GRANTED. An Actions evidence artifact named aos-w-p18-synthetic-pilot (ID 12297606907, retention 90 days) contains the working instance, event journal, state, checkpoints, handoff, artifacts and structured p18-results.json.

The test used the committed v0.7.0 marketing library as a prerequisite, then ran a bounded custom acceptance graph. Three fictional audience research branches were initialized. One research quality review intentionally rejected incomplete output, then accepted a corrected new-hash artifact. A deterministic reviewer also rejected a minimal SVG fixture, then accepted a revised SVG fixture. Both versions and event transitions were persisted.

The test exercised parallel CRM and landing-planning branches, a three-branch reviewed synthesis join, a deliberate interruption, a fresh RunStore reopen from saved files, checkpoint and handoff records, and separate prelaunch and launch permission states. The final launch permit was never granted. No campaign, Meta, GHL, web page or tracking provider was changed.

## Evidence classification

REAL: durable file writes through AOS-W RunStore, event chain, checkpoints, conditional task progress, task retries/review event transitions, parallel branch eligibility, cold object reinitialization from file records and blocked launch completion.

MOCKED: fictional industry/competitor observations and offers, deterministic reviewer personas within one Python process, a simple text SVG as creative proof-of-format, and proposed CRM/landing/tracking specifications.

NOT RUN: genuine Meta Ads Library evidence retrieval, independent AI agent/model review, real image generation or independent visual inspection, authenticated owner launch approval, actual live or staged Meta integration, real CRM/landing deployment, external provider read-back and measurement of time saved relative to previous manual sessions.

## Acceptance implications

- T01 real Ampgent end-to-end: NOT DEMONSTRATED. A synthetic marketing lifecycle runs through the file protocol, but it is not real competitor research and lacks actual creative generation/QA and external handoff evidence.
- T04 failed review and targeted repair: PARTIAL with deterministically controlled test reviewer and exact-hash revisions. Independent AI evidence still missing.
- File state, resume and merge: supported in this bounded host test, but cloud persistence and another AI-platform transfer are not established.

This test supplements and does not supersede Prompt 16 (13 local standalone cases), Prompt 17 (local Git tests) or their distinct evidence limitations. It does not authorize publishing or spending.

## Remaining Prompt 18 work

Execute a real bounded public-source research portfolio, record actual URLs and dated ad observations, require truly independent AI review of source evidence and a generated creative image, archive the actual inspected asset, and compare audited execution to the historical manual process. Record an explicit, still-blocked human launch permit. Repeat against the exact published clean 0.7.0 release if the installation baseline matters. Add a durable post-execution evidence summary to the repository rather than relying only on a 90-day Actions artifact.
