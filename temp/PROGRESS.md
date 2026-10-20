# AOS-W Development Progress

Date: 2026-10-20
Phase: **Prompt 13 local Git coordination prototype complete; AOS-W 0.5.0**
Status: Portable no-Git baseline preserved; optional Git sync and Git ref CAS tested on local bare remote. Hosted GitHub and live LFS server untested.

## Implemented
- Prompts 01–12 remain committed and covered by 75 local tests.
- New optional tools/git coordination and CLI check remote heads, fast-forward only where clean, preserve dirty/diverged histories, verify ordinary Git push and commit only selected agent-files paths, with four-field Git commit provenance.
- Shared task refs use explicit Git force-with-lease old SHA CAS, logical actors separated from shared Git login, UUID token, lease/epoch and explicit reviewed stale reclaim. Shared mode fails closed without remote.
- Three modes: standalone_single_writer (default, Git-free), git_mirrored_single_writer, shared_coordinated. Config vs actual sync-state separated in agent-files. New sync config/state schemas bring draft total to 20.
- Built Git LFS client wrapper but no git-lfs binary or actual lock server available; preferred mechanism is Git ref CAS **provisionally**, not a production-ready distributed mutex.
- Added manual no-script protocol, ADR-014, sanitized conformance explanation, tests and evidence.

## Actual tests
- **15 new local Git tests PASS** using two clones of real bare Git remote with same Git user identity and distinct agent instances. Six competing claim races each admitted one winner; tests include expired/stale leases, remote outage, fast-forward, divergence, dirty tree and unaudited ahead commit blocking.
- **90/90 total local tests PASS**: 15 new Git, 38 governance, 26 state/recovery, 11 composition.
- Two new JSON Schema Draft 2020-12 documents validated with installed jsonschema; sample sync-state valid.
- GitHub Git transport DNS failed in this container; no hosted concurrent push test. Git LFS actual lock tests NOT RUN. No provider effects attempted.

## Next
Prompt 14 optional helper packaging, installed folder upgrade-preservation, schema checks, release ZIP and portable cold-start. Before production claim guarantees: hosted CAS races and actual LFS lock server tests, plus provider-side action fencing/idempotency, remain explicit gaps.
Source: temp/tests/PROMPT-13-GIT-COORDINATION.md.
