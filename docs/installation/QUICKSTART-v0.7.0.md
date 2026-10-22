# Install and operate AOS-W 0.7.0 portable preview

Current preview as of October 20, 2026. Version 1 stable is NOT approved or published. The portable core is a set of Markdown, YAML and JSON/JSONL files, usable manually by an agent with durable filesystem access. It does not require Python, Git, a database, dedicated MCP server, or scheduler. Those capabilities are optional if installed by a separate host.

## Obtain and check the current release

Official prerelease page.
https://github.com/digzoman/aos-workflows/releases/tag/v0.7.0-portable-preview

Direct current asset.
https://github.com/digzoman/aos-workflows/releases/download/v0.7.0-portable-preview/aos-w-portable-0.7.0.zip

Archive SHA-256, verified in independently executed GitHub CI 39499859355.
0826ddf9807354e80e22b757dd129b86539aae8d6ff3c7799029e5f3719c74f7

Verify the downloaded ZIP's digest using a native OS hash utility. The package's only top-level folder is aos-w. It includes protected specs, schemas, README, templates, skills, reference manuals, manifest and a clean agent-files seed. It excludes developer scripts, tests, temp, .git, active instances and custom user data.

## Manual no-Git installation

1. Extract aos-w-portable-0.7.0.zip into any working directory with durable file storage.
2. Open aos-w/README.md, aos-w/PROTOCOL.md and aos-w/agent-files/README.md.
3. Ask a capable agent to list templates under aos-w/templates and create a new pinned instance under aos-w/agent-files/instances.
4. Follow aos-w/references/START-A-RUN.md to create a unique run and exact pinned graph/template snapshot.
5. For each step, check dependencies, permitted actions, skills, current evidence/reviews and side effect authorization. Record events, output digests, checkpoints and a handoff under the instance.
6. Before a fresh session resumes, read saved handoff and event history, confirm real on-disk inputs and avoid replaying an ambiguous external action.
7. Normal installed use changes only files under aos-w/agent-files. Other files are protected framework content.

No programming runtime is required inside aos-w itself. A capable manually directed agent still needs access to read/write the selected durable files. The archive does not create autonomous processes.

## Optional developer/helper commands

From a checkout of the development repository, Python may optionally be installed to validate the ZIP and safely upgrade.

~~~sh
python scripts/aosw-distribution.py verify dist/aos-w-portable-0.7.0.zip
python scripts/aosw-distribution.py install dist/aos-w-portable-0.7.0.zip /work/project/aos-w
python scripts/aosw-ops.py list /work/project/aos-w
~~~

With optional PyYAML installed, create a clean research instance without executing it.

~~~sh
python scripts/aosw-ops.py init /work/project/aos-w marketing-research-plan research-demo run-001 \
  --actor '{"agent":"Demo","platform":"local","role":"worker","instance":"demo-session"}' \
  --parameters '{"research_question":"Compare three fictional audience niches"}'
python scripts/aosw-ops.py status /work/project/aos-w research-demo run-001
~~~

The initializer only creates a CREATED run and an advisory READY task list. It does NOT complete work, run an agent, authenticate an approval, schedule occurrences or call an external provider.

## Safely upgrade an existing installation

Never blindly unzip a new distribution over an active install. First back up the entire aos-w folder, including private agent-files, somewhere secure. Verify the current and destination schema compatibility and pinned versions.

With the optional maintainer installer, verify the exact ZIP and then execute.

~~~sh
python scripts/aosw-distribution.py verify dist/aos-w-portable-0.7.0.zip
python scripts/aosw-distribution.py upgrade dist/aos-w-portable-0.7.0.zip /work/project/aos-w
~~~

The tested installer verifies allowlisted ZIP names and manifest hashes, refuses user-symlink escapes, stages replacement of framework content, and copies existing agent-files byte-for-byte to the replacement with a rollback sibling backup. An interrupted upgrade may still require operator inspection, and filesystem rename atomicity/durability depends on the host. Never delete the rollback copy before verifying your specific active instances and securing their private data.

For a manual upgrade with no Python, replace only protected framework content from the new archive after a complete backup, keep agent-files unchanged, and review schema compatibility and all pinned instance graph snapshots. A schema-major migration is not automatic.

## Advanced optional features and limitations

Optional developer helpers live under repository tools/state, tools/governance, tools/composition and tools/git. These files are NOT included in the standalone ZIP. Local deterministic helpers have tested single-writer event integrity, retry/QC and graph revision behavior. Git mirroring is optional. Git ref CAS remains an experimental multi-agent coordination approach, not production-certified hosted exclusivity. No external action is fenced automatically by Git.

A template may declare a schedule, but no background scheduler is included. Missing remote skills, no actual durable cloud storage, unverified reviews, mismatched files, unknown provider writes or missing authorization are BLOCKED, never a silent PASS.

## Verified tests, release and historical notes

GitHub Actions release audit 39499859355 verified 126 regressions, 13 practical standalone 0.7.0 acceptance scenarios, manifest/ZIP checks and selected current/historical repository secret patterns. That is NOT full V1 acceptance or a complete privacy certificate.

The older v0.6.0 installation guide is preserved as QUICKSTART-v0.6.0.md for its historical commands and evidence, but this file is the current guide. Read docs/release/V1-RELEASE-APPROVAL-PACKET.md and docs/release/V1-LIMITATIONS-AND-RISKS.md before recommending production use.
