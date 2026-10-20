# AOS-W Version 1 release readiness review

Review date: 2026-10-20. Status: HOLD, not approved for a Version 1 stable release.
Repository: https://github.com/digzoman/aos-workflows
Current reviewed main HEAD: a7b7e8ac379cef2536d3c7830e2de5b638bf994f
Published preview: v0.7.0-portable-preview

## Executive decision

Version 0.7.0 is a functional, downloadable, file-based preview with a marketing template library. It is not a demonstrated complete V1 product under the six original success criteria. Do not label the repository V1 complete, certify production locking, or authorize live advertising activity.

The repository is ahead of its temp/PROGRESS.md and temp/HANDOFF.md. Prompt 15 was committed at 3512cb7 and its schema repaired at a7b7e8a. The later hosted distribution workflow 39434478250 passed 126 regression/conformance tests and built and published a 0.7.0 preview package. Prompts 18 and 19 have no completed pilot or audit records on main at this review start.

## Reviewed, directly supported progress

1. Prompts 01 through 06, research and history indexing: committed, with noted source-evidence limitations.
2. Prompt 07, enhanced PRD: written and committed. Its distinct formal owner approval record remains PENDING, although the owner explicitly directed subsequent bounded implementation work.
3. Prompts 08 through 14, technical specifications, portable scaffold, composition, state, governance, optional Git coordination and packaging: committed and tested within documented limits.
4. Prompt 15, sanitized Ampgent-inspired marketing library: NOW COMMITTED as 21 independently usable modules and one compound lifecycle, with 18 new marketing conformance tests. An initially failed hosted schema validation was repaired. The final hosted 0.7.0 distribution run passed 126 tests.
5. Prompt 16, standalone execution: 13/13 local real-file acceptance scenarios passed on 0.6.0. A separate truly persistent cloud filesystem was NOT RUN, and the 0.7.0 marketing distribution has not been rerun through the full real-workflow acceptance suite.
6. Prompt 17, collaboration: 11/11 recorded local Git collaboration acceptance cases passed (plus one later LFS parser regression). The hosted GitHub Actions collaboration workflow 39428039269 concluded SUCCESS but its own evidence step says hosted CAS REVIEW_REQUIRED and live LFS BLOCKED. Workflow success is NOT an acceptance PASS. Cross-provider AI handoff was NOT RUN.
7. Prompt 18, staged end-to-end marketing pilot: NOT RUN. Existing marketing example instances are explicitly CREATED-only or MOCK fixtures. See docs/testing/PROMPT-18-PILOT-PLAN.md.
8. Prompt 19, this evidence review and release preparation: partial documentation and gap assessment, NOT a security attestation or owner-approved final release.

## Original six V1 success criteria

- T01 real-world Ampgent workflow end to end: NOT DEMONSTRATED. Fictional standalone and marketing conformance tests are useful lower-tier evidence; full independent research, creative, QC and campaign handoff pilot remains to run.
- T02 real cross-platform ChatGPT/Codex/Claude/Muse handoff: NOT DEMONSTRATED. Separate subprocesses and clones passed, but are not independent model platforms.
- T03 exclusive multi-agent claims: PARTIAL. Actual local bare Git CAS races and stale-token protections passed. Hosted GitHub probe reported REVIEW_REQUIRED, Git LFS server probe BLOCKED, and identity authentication/provider-side fencing are absent.
- T04 failed independent QA with correction and unrelated branches proceeding: PARTIAL. Local synthetic/deterministic quality gates and remediation passed; a distinct independent AI review of an end-to-end marketing artifact has not been demonstrated.
- T05 revise live workflow preserving prior completed work: PARTIAL PASS under isolated local tests using mock approval. No independent agent platform or real owner authorization for revised live runs was evidenced.
- T06 move active run to another Git repository and resume: PASS in real local Git bare remote test with reconfigured claims. Different hosted providers and external cross-platform behavior not tested.

## Required ancillary proof still absent

Persistent cloud filesystem resume after a terminated session. Recurrence and schedule-triggered occurrence deduplication, timezone and missed-trigger policy. Trusted external skill resolution. Real image quality checks against generated assets. Authenticated human approvals. Any host-enforced provider permission or exactly-once external writes. Production integration and readback. Full V1 requirements compliance. Independent post-upgrade 0.7.0 practical acceptance.

## Release and installable ZIP

Verified published preview: https://github.com/digzoman/aos-workflows/releases/tag/v0.7.0-portable-preview
Asset: aos-w-portable-0.7.0.zip
Hosted build SHA-256 in successful run 39434478250: 0826ddf9807354e80e22b757dd129b86539aae8d6ff3c7799029e5f3719c74f7

The published release and CI verify packaging and installation/upgrade smoke tests, not full V1 acceptance. Both README.md and docs/installation/QUICKSTART.md had 0.6.0-focused messaging at review time. Documentation for 0.7.0 and change notes still require a durable coherent update; keep the validated 0.6.0 historical guide rather than discarding it.

## Security and public hygiene scope

Repo visibility is PUBLIC. The HEAD file-tree listing contains no filenames ending in .env, .pem, .key, .p12, .pfx, .sqlite or .db, and no obvious credential-named files. This is only a filename inspection, NOT a content or history secret scan. Do not claim that no secrets or customer data were exposed without scanning current text, binary artifacts, historical commits, release bundles and external copies. In particular, public research and marketing examples require human privacy review and source-rights assessment. No credential values should appear in the audit evidence. The 0.7.0 package builder has a tested clean allowlist, but release contents still need a final independent security review.

## Tracked temp directory review

The temp/ material contains useful original research, survey history, decision reasoning, evolving candidate templates, test reports and handoffs. Do NOT delete it blindly. Migrate approved durable requirements to docs/specs, verified acceptance data to docs/testing, versioned release information to docs/release, and operational startup rules into the portable references. Preserve historical documents for audit and add an archival index. Distinguish proposed ADRs from accepted ADRs. Only suggest deletions after an owner-reviewed inventory.

## Release gate

Stable V1 is BLOCKED until core T01 to T06 acceptance evidence is complete or the owner explicitly changes scope in an updated approved PRD, an independently reviewed security scan passes, the license and outstanding ADR policy decisions are addressed, and the owner gives explicit release approval. Earlier scoped implementation requests do not constitute final V1 sign-off.

Next work: execute Prompt 18 in a controlled, sanitized environment, complete honest independent AI and hosted coordination tests where accessible, update installation docs and release notes, and return a fresh audit for owner decision. No live Meta, GHL, website, spend or publishing operations are authorized by this review.


## Subsequent execution addendum, same-day continuation

After the original main review, commit 0863e3f added an executable Prompt 18 synthetic marketing pilot and GitHub Actions run 39495294275 completed SUCCESS. This generated 77 real AOS-W file/state events including a failed and then corrected mock research review, a failed and corrected SVG creative fixture review, a three-branch join, parallel CRM and landing planning, a cold state reopen, and a launch gate left NOT_GRANTED. Full details in docs/testing/PROMPT-18-SYNTHETIC-PILOT-REPORT.md. This raises Prompt 18 from NOT RUN to PARTIAL, CONTROLLED SYNTHETIC ONLY, while T01 real marketing evidence, independent AI assessment and production-style creative proof remain incomplete. V1 release decision remains HOLD. Later CI run 39495294210 also passed portable distribution tests.
