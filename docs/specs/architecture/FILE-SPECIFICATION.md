# Directory, file, protection and compatibility specification

**Design proposal 0.1.** Files in this map are **future installation targets**, not claims that the directories have already been built in `scaffold/aos-w/`. PRD §§6/8/11/13 define immutable/writable split.

```text
digzoman/aos-workflows/                  PUBLIC DEVELOPMENT REPOSITORY
  README.md
  docs/
    specs/
      prd/                               approved-requirement source (PRD currently draft)
      architecture/                      Prompt 08 design docs
      schemas/                           JSON Schema designs
      adrs/                              technical proposals
  examples/                              sanitized, distributable reference projects
  scripts/                               optional executables, never mandatory
  tools/                                 optional integrations and helper apps
  temp/                                  tracked RESEARCH/decisions/planning, not user run scratch
  scaffold/
    aos-w/                                DIRECTLY DOWNLOADABLE INSTALLABLE ROOT
      README.md                           [F] Quick start, constraints, how to recover
      PROTOCOL.md                         [F] Human/agent execution & safety procedure
      VERSION.json                        [F] Installed framework/protocol compatibility
      spec/                               [F] Copied or self-contained schema/contract reference
      references/                         [F] Reusable guidance and QA conventions
      templates/
        <template-id>/
          template.yaml                   [F] Master workflow graph & contract
          README.md                       [F] Purpose/usage/owner review
          skills/<skill-id>/SKILL.md      [F] Bundled approved read-only skill
          assets/                         [F] Nonconfidential template fixtures
      agent-files/                        THE ONLY NORMAL WRITABLE SUBTREE
        README.md                         [A] Usage and safe migration notes
        config/
          settings.json                   [A] Default project limits and identity
          capabilities.json               [A] Last observed host capabilities (optional)
          sync.json                       [A] Optional Git remote/sync, NO SECRETS
        custom-templates/
          <template-id>/
            template.yaml                 [A] Custom overlay or complete template
            README.md
            skills/<skill-id>/SKILL.md
        instances/
          <instance-id>/
            instance.json                 [A] Identity, inputs, scope, current graph revision
            template-lock.json            [A] Parent refs + exact pinned snapshot digests
            graph-revisions/
              <revision-id>.yaml          [A] Immutable fully resolved graph snapshot
            template-snapshots/
              <content-id>/template.yaml  [A] Local fully resolved upstream snapshot
            skills/                       [A] Instance-specific skill packages
            runs/
              <run-id>/
                run.json                   [A] Trigger/occurrence identity and context
                state.json                 [A] Derived current state and event anchor
                events.jsonl               [A] Validated append-ordered domain events
                checkpoints/
                  <checkpoint-id>.json    [A] Validated resume anchors
                tasks/
                  <task-id>/
                    attempts/
                      <attempt-id>.json   [A] Attempt/outcome and operation evidence
                claims/
                  <task-id>.json          [A] Logical claim, advisory or host-verified
                reviews/
                  <review-id>.json        [A] Version-specific independent QC
                approvals/
                  <approval-id>.json      [A] Human/delegated permissions or waivers
                artifacts/                [A] Work outputs & evidence owned by this run
                skills/                   [A] Run-specific skill snapshots/instructions
                handoff.json              [A] Optional structured handoff companion
                handoff.md                [A] Durable human-readable resume report
        indexes/                          [A] DERIVED: portfolio summary only
        cache/                            [A] Rebuildable, no credentials
        coordination/                     [A] Optional adapter hints, NOT mutex without CAS
```

**[F] Protected framework:** no normal edits by task execution. Changed only by explicit, versioned upgrade with backup/compatibility test. **[A] agent-files:** ordinary writes, subject to user filesystem/privacy policy. `VERSION.json` describes framework, but per-instance `template-lock.json` preserves older template dependencies.

## File responsibilities and authority

| File | Source of truth for | Change policy |
| --- | --- | --- |
| `templates/*/template.yaml` | published master graph, defaults, skills and contracts | Only signed/reviewed framework update |
| `custom-templates/*/template.yaml` | user custom definition | May change; active run uses pinned copy, not live ref |
| `instance.json` | instance ID, approved context/current graph pointer | Scoped revision event and review |
| `template-lock.json` | exact template source+version, resolved digest, origin | Immutable once instance started; updated only via explicit revision with history |
| `graph-revisions/*.yaml` | exact effective graph version at transition time | Append-only new files; old versions preserved |
| `run.json` | one manual/scheduled occurrence identity/policy snapshot | Immutable trigger identity; status in events |
| `events.jsonl` | chronological verified run audit | Append-only meaning; repair through explicit correction event, never silent rewrite |
| `state.json` | current **derived** task/gate status for fast resume | Rebuild from valid events; not external provider reality |
| `checkpoints/*.json` | validated restart boundary and event prefix | Immutable anchor, never label durable unless stored/verified |
| `attempts/*.json` | task attempt inputs, side-effect intent+ACK+verification | Written/updated with corresponding events; outcome UNKNOWN until reconciled |
| `claims/*.json` | claimed logical owner and lease/fence observation | Advisory unless verified backend CAS |
| `reviews/*.json` | exact artifact/rubric/version evaluation | Immutable verdict, revised artifact needs new review |
| `approvals/*.json` | specific authorized action, object set, budget and expiry | Append supersession/revocation; QC never substitutes |
| `handoff.md` | human-friendly last verified status and next eligible work | Rewritten at checkpoint, derived from run record |
| `indexes/` | quick portfolio listing | Rebuildable, never outranks per-run state |
| `sync.json` | whether/how to inspect/push remote | Only in agent-files; credentials as provider references, never secrets |

## Path and identity rules

- IDs are lowercase ASCII slugs or UUID-compatible safe tokens; reject `..`, traversal, path separators inside IDs, reserved shell characters and case-colliding identities. Paths use relative POSIX-style strings under this install, no silently resolved `../` escapes or symlink/hardlink escapes. External references are explicitly typed `external_uri` with scope.
- Run artifacts may reference outside storage, but normal local *writes* go only under agent-files. Optional external provider tools are separate permission-checked operations, not loopholes.
- Fixed framework files are never used as scratch during a run. To modify an approved base template, create a custom template under agent-files and pin a new instance/revision.
- A synced Git repo uses Git as optional transport; no rule assumes `.git/` exists or is writable. The sync adapter may have its own Git metadata outside the installed framework but cannot alter protected framework content except through an approved upgrade.
- `temp/` in project repo is **development history**, not an installed run's temp directory.
- User-specific data belongs outside the public framework repo unless sanitized and expressly approved for publication.

## Version pinning and upgrade contract

Instance creation resolves template inheritance and copies the effective template into `template-snapshots/<content-id>`, preserves origin reference/version/digest in `template-lock.json`, and writes `graph-revisions/g0001.yaml`. No live edge to master-template HEAD determines an active run's semantics. A *later* base-template edit does not alter existing runs.

A requested upgrade generates a *candidate* new graph revision and impact report with changed/removed nodes, protected gate changes, skill-source changes, permission diff and affected artifact hashes. Only after configured approval does it append a revision event and update instance's current graph pointer. Archived snapshots and old reviews remain addressable.

`schema_version` MAJOR mismatch blocks execution pending explicit migration; MINOR additions permitted under documented safe defaults. Readers cannot discard unknown access-control fields. JSON serialization UTF-8, LF newlines and UTC ISO8601 timestamps are recommended. File encoding and hash algorithm are pinned per record; hash verification may be unavailable in manual-only hosts, which must report UNVERIFIED instead of PASS.

## Installation compatibility probes

1. Copy only `scaffold/aos-w/` to an unrelated working directory; read README and built-in template.
2. Create a new instance+run under agent-files and zero files changed outside it.
3. Restart as fresh agent and resolve exact pinned graph.
4. Modify master template upstream; old run remains pinned.
5. Demonstrate custom template and instance skill inside agent-files.
6. No Git, Python, hosted database or MCP required for manual single-writer flow.

These are future tests, not tests executed in Prompt 08.
