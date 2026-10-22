# Install and visualize AOS-W v0.8.0 portable preview

Current preview, October 22, 2026. This is an additive minor update to v0.7.0, NOT a stable V1 release. Existing marketing templates and their pinned template/child digests are unchanged.

Download https://github.com/digzoman/aos-workflows/releases/tag/v0.8.0-portable-preview
Asset aos-w-portable-0.8.0.zip
For the current exact digest, use the release asset's SHA-256 digest on GitHub and verify it locally before installing. The CI workflow independently builds/verifies the ZIP and preserves existing agent-files.

## File-only installation

1. Download/extract the verified ZIP. It creates one aos-w/ folder containing protected instructions, schemas, base templates, references and a clean user-owned agent-files area.
2. Read aos-w/README.md, aos-w/PROTOCOL.md and aos-w/agent-files/README.md. A capable agent with actual persistent file access can operate manually, with no mandatory Python, Git, local server, daemon or MCP.
3. Choose a master workflow under aos-w/templates or a custom template under aos-w/agent-files/custom-templates. Pin its exact current template revision and create a run under agent-files/instances.
4. Use the normal event/checkpoint/handoff state protocol. No visualization may grant authorization, complete tasks, send messages or change provider state.

## New in v0.8, interactive visualization

Read aos-w/references/VISUALIZATION.md. The framework now includes aos-w/references/visualization-viewer.html and spec/schemas/visualization-snapshot.schema.json.

Ask your agent to create a read-only diagram for a selected template or run, using source graph.nodes and graph.nodes[].needs, with saved instructions, inputs, outputs, QA and exact recorded status. Save the self-contained HTML and optional snapshot JSON under:

~~~text
aos-w/agent-files/visualizations/<view-id>/index.html
aos-w/agent-files/visualizations/<view-id>/snapshot.json
~~~

Open index.html in a browser, click any node for prompts/details and follow arrows to see dependencies, parallel branches, approvals and current blockers. This page is a point-in-time report, NOT a workflow engine or live provider dashboard.

If your agent cannot render local HTML, it can deliver the generated file via its workspace/file tools. GitHub Pages is a separate optional publishing method requiring your **explicit approval and sanitized export**, especially for sensitive internal business workflow prompts. No Pages deployment is automatic.

## Optional developer CLI

Within the development repo, with Python and optional PyYAML for YAML input:

~~~sh
python scripts/aosw-visualize.py \
  --template scaffold/aos-w/templates/research-starter/template.yaml \
  --out /path/to/aos-w/agent-files/visualizations/research-demo/index.html

python scripts/aosw-visualize.py \
  --snapshot examples/visualization/bucket9-stage.json \
  --out /path/to/aos-w/agent-files/visualizations/bucket9-demo/index.html
~~~

The optional generator never mutates the source run. It labels state overlays as SOURCE_SNAPSHOT_UNVERIFIED unless external reconciliation has been explicitly performed. Prepared JSON input mode requires no PyYAML.

## Safe upgrade from v0.7

Back up the ENTIRE installed aos-w directory. Check pinned graph and schema compatibility. Only replace framework-controlled files; preserve the existing agent-files subtree byte-for-byte. Then create any new visualizations directory if missing.

Optional maintainer commands in the development repo:

~~~sh
python scripts/aosw-distribution.py verify dist/aos-w-portable-0.8.0.zip
python scripts/aosw-distribution.py upgrade dist/aos-w-portable-0.8.0.zip /work/project/aos-w
~~~

The distribution upgrader performs content validation, backup and clean user subtree preservation, but a complete real multi-host/cloud migration guarantee remains unproven. Validate your own data after upgrade and do not discard rollback copies prematurely.

The previous [v0.7 installation instructions](QUICKSTART-v0.7.0.md) and [v0.6 guide](QUICKSTART-v0.6.0.md) remain available. Original V1 owner approval and four priority acceptance tests T01–T04 remain pending.

## One-command rendering of an existing persisted workflow

An optional development helper can now find the **pinned graph and run state directly from the existing run directory**, rather than requiring an agent to supply --graph, --state and --out separately.

~~~sh
python scripts/aosw-visualize.py \
  --run-dir /work/project/aos-w/agent-files/instances/my-case/runs/run-001
~~~

The helper checks run.json, pinned graph revision and a read-only replay of events.jsonl using the optional AOS-W state helper. If the saved snapshot does not match the event-verified sequence/digest or if the journal has a corrupt tail, rendering is blocked instead of displaying false progress. It writes an automatically named view under the same installation's agent-files/visualizations folder. It includes event sequence, current step statuses and up to eight **metadata-only** activity records per task, without copying the event payload or provider credentials. Step panels now display the template policy, child template reference and last saved journal activity.

For a legacy/advisory run that cannot be event-verified, specify --unverified. This renders a visibly SOURCE_SNAPSHOT_UNVERIFIED page and does NOT assert a valid event chain. Never use --unverified to imply real provider truth, review approval or independent verification.

For long source prompts above the schema-supported maximum, conversion fails explicitly rather than shortening the execution instructions and losing a safety gate. No live filesystem watcher or background refresh is included.
