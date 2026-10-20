# AOS-W Version 1 limitations, risks and mitigations

Review date: 2026-10-20. These are release blockers or intentionally documented limitations, not automatically accepted product compromises.

## Highest-priority known limitations

1. File-only instructions do not execute themselves. A capable running agent must interpret the template and persist the workflow; optional Python/Git helper tooling is outside the minimum downloaded package. No automatically dispatched task engine is included.
2. Persistent cloud filesystem survival across terminated cloud agent sessions is not demonstrated. GitHub Actions runners are ephemeral and should not be represented as persistent cloud storage.
3. Actual ChatGPT, Codex, Claude or Muse cross-provider handoff has not been completed. Separate worker subprocesses and deterministic reviewers are not equivalent to independent models.
4. Git CAS is an experimental, cooperative claim protocol. Hosted GitHub CAS result was REVIEW_REQUIRED; LFS server comparison BLOCKED. Shared Git credentials do not authenticate AOS-W's four-field agent identity. No provider-side fencing.
5. Human authorization, QA reviewer identities and permission files are not authenticated at the provider boundary by the file protocol. A forged local owner claim is not permission for spend, messages, deployment, ad activation or sensitive customer access.
6. Automatic parent and child join enforcement is incomplete. The Prompt 18 runner explicitly checked all three independently reviewed SHA-matched research runs before synthesis. Without equivalent validation, parent graph READY eligibility can be misleading.
7. Recurrence and schedules are declarative only. No live host schedule, occurrence dedup, missed/DST windows or overlap policy are validated.
8. Remote skills and trust are not implemented as a safe authenticated fetch/execute pipeline; bundled step skills and certain offline context checks were tested.
9. Actual external API operation write/reconcile/readback, especially Meta Ads Manager and GHL, is not demonstrated. Current staging is a local implementation plan. Timeout/idempotency tests use controlled cases.
10. Research and image creative acceptance remains incomplete. No verified Meta Ad Library cards, independent AI reviewer or approved brand logo/offer fulfillment evidence; the $47 concept is not a production promise.
11. Graph revision authorization tests use mocked owner permission. Event hash chains detect corruption, not malicious alteration by a privileged writer.
12. Major-version migration and compatibility across genuine different model providers were not demonstrated.
13. Open-source licensing remains undecided. Public GitHub visibility by itself does not license reuse.
14. Privacy/security scan is limited to tracked current files and reachable Git object history with selected high-confidence patterns plus ZIP archive checks. Human review of historical business context, retained images, source rights, additional secrets classes, other branches/remotes and the entire external exposure surface remains necessary. CI found one file containing a non-example email requiring context review, without printing it in logs. Do not assert a universal absence of personal data.
15. Durable documentation had become scattered between temp/ and docs/ and older quick starts described 0.6.0. This audit promotes core historical source records and updates the current guide, while preserving temp and avoiding retrospective redaction.

## Risk handling

- Local standalone deployment. Permit controlled manual, single-writer use with explicit status; preserve agent-files during upgrades; do not claim automated background execution.
- Collaborative shared mode. Default BLOCKED when remote CAS enforcement, current claim epoch and stale-lease recovery cannot be verified.
- External actions. Default to read/research/write_local/review only. Require real authenticated scoped authorization at the provider tool boundary before any external mutation. QA PASS is never launch permission.
- Public repository. Keep historical research sanitized, never commit access credentials, private customer communications or identifiable lead records. Scan historic blobs and artifact ZIP for high confidence secrets on CI; require manual privacy review before stable release.
- Release. Maintain v0.7.0 preview for evaluators, do not publish v1.0.0 final/tag until owner signoff and mandatory acceptance coverage or explicitly approved scope change.

## Quality improvements for the V1.x backlog

P0. Native cross-instance all-reviewed join enforcement, formal PRD/ADR approval, independent cross-platform AI test, persistent cloud filesystem test, hosted CAS/LFS resolution, independent QA test, full real ad evidence and image approval, comprehensive privacy/license review.
P1. Host scheduler/occurrence dedup, authenticated approval adapters, provider stage/readback, skill trust and exact asset inspection, semantic scoring/confidence rubric completeness, major upgrade tests.
P2. Optional dashboards, expanded nonmarketing templates, large-workflow stress tests, operator-friendly audit summary and historical index maintenance.

See docs/release/V1-REQUIREMENTS-MATRIX.md for the requirement-by-requirement classification and docs/release/V1-RELEASE-APPROVAL-PACKET.md for the owner decision.
