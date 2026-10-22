# AOS-W v0.8 workflow visualization

The visualization is a read-only interactive HTML page showing any template or pinned run with dependency arrows, status labels and a drill-down panel for exact step instructions, requirements, QC and evidence. It does not execute or approve work.

## Default output: directly viewable HTML, not a ZIP

When presenting a completed visualization to a user, **render the standalone index.html webpage in the host's supported HTML/browser preview** whenever possible. Otherwise give an ordinary **link or attachment to the individual index.html file** as the primary deliverable. Never make the user download and unzip an archive simply to inspect one workflow diagram if the host supports HTML.

Only use a ZIP for a requested archive, genuine supporting multi-file bundle, or when the platform (such as GitHub Actions artifacts) forces compressed downloads. If unavoidable, tell the user to extract it and open index.html. Do not describe a ZIP artifact as a working webpage link.

If the environment cannot render or share standalone HTML, a **sanitized GitHub Pages webpage** can be suggested only with explicit owner publishing approval. No automatic Pages deployment, private customer content sharing, or exposure of internal workflows is authorized.

The downloaded AOS-W **framework installer** is deliberately a multi-file ZIP and is NOT covered by the visualization HTML-first preference.

## Output and operation

Save under aos-w/agent-files/visualizations/<safe-id>/index.html, with optional snapshot.json. Only agent-files is normally writable. The protected page skeleton is aos-w/references/visualization-viewer.html, with a single token __AOSW_SNAPSHOT_JSON__ for a serialized visualization JSON object.

For a TEMPLATE read template.yaml. For an INSTANCE use the pinned graph-revisions/gXXXX.yaml. For a RUN use the pinned graph with selected run state.json and reconciled events/checkpoints/reviews if possible. The page must label an unverified state as SOURCE_SNAPSHOT_UNVERIFIED rather than pretend to report live status.

The complete schema is spec/schemas/visualization-snapshot.schema.json. Build node IDs from graph.nodes, arrows from needs, and the selected step prompt from instructions. Include inputs, outputs, contract, quality gates, retry, review and evidence when saved. Serialize the JSON escaping angle brackets, ampersand and Unicode line separators before embedding in the HTML script of type application/json. The viewer renders user text as textContent, never as active HTML.

A capable AI agent may directly copy/modify the bundled viewer's placeholder and create a file without Python. There are no remote libraries, server or build steps in the installed core.

## Optional developer converter

Python and PyYAML for YAML input are optional tools only in the development repository:

~~~sh
python scripts/aosw-visualize.py \
  --template scaffold/aos-w/templates/research-starter/template.yaml \
  --out /path/to/aos-w/agent-files/visualizations/research-preview/index.html

python scripts/aosw-visualize.py \
  --graph /path/to/aos-w/agent-files/instances/my-case/graph-revisions/g0001.yaml \
  --state /path/to/aos-w/agent-files/instances/my-case/runs/run-001/state.json \
  --out /path/to/aos-w/agent-files/visualizations/my-case-run-001/index.html

python scripts/aosw-visualize.py \
  --snapshot /path/to/snapshot.json \
  --out /path/to/aos-w/agent-files/visualizations/my-prepared-view/index.html
~~~

The converter writes index.html and snapshot.json. It never modifies the source template/run or writes to an external provider.

## Updating and publishing

Regenerate on user request, approved state transition or checkpoint. The HTML is a frozen snapshot and does not poll the file system or browser for new events. Opening a card only displays its saved details. Browsers with local file access can open index.html directly. If a cloud agent cannot render local HTML, share the file rather than pretending it is hosted.

If the user requests hosting and local preview is impossible, suggest GitHub Pages as a separate opt-in action. Treat Pages as PUBLIC unless verified private access control exists. Export a separately reviewed sanitized copy; never push private agent-files/visualizations or publish prompts, customer data, secrets or unapproved offer details without authorization.

The specification and acceptance checklist are in docs/specs/visualization/V0.8-SPEC.md in the development repository. Previous stable V1 acceptance blockers remain unaffected.

## One-command rendering of an existing persisted workflow

An optional development helper can now find the **pinned graph and run state directly from the existing run directory**, rather than requiring an agent to supply --graph, --state and --out separately.

~~~sh
python scripts/aosw-visualize.py \
  --run-dir /work/project/aos-w/agent-files/instances/my-case/runs/run-001
~~~

The helper checks run.json, pinned graph revision and a read-only replay of events.jsonl using the optional AOS-W state helper. If the saved snapshot does not match the event-verified sequence/digest or if the journal has a corrupt tail, rendering is blocked instead of displaying false progress. It writes an automatically named view under the same installation's agent-files/visualizations folder. It includes event sequence, current step statuses and up to eight **metadata-only** activity records per task, without copying the event payload or provider credentials. Step panels now display the template policy, child template reference and last saved journal activity.

For a legacy/advisory run that cannot be event-verified, specify --unverified. This renders a visibly SOURCE_SNAPSHOT_UNVERIFIED page and does NOT assert a valid event chain. Never use --unverified to imply real provider truth, review approval or independent verification.

For long source prompts above the schema-supported maximum, conversion fails explicitly rather than shortening the execution instructions and losing a safety gate. No live filesystem watcher or background refresh is included.


## v0.9 human-first viewer

The default diagram now favors readable titles, named phases, workstream labels, a status-aware overview and independent reviews ready for pickup. The step drawer leads with purpose, next action, dated sources, input/output and QC. Source prompts and JSON are preserved in Advanced. Synthetic demo: examples/visualization/synthetic-six-audience.json. Agents must recover available tools rather than inventing user gates. A GitHub blob is source, not a rendered page; see docs/installation/V09-PAGES.md for the manual approved demo deployment path.


## Accessibility checks for generated HTML (v0.9)

A manager must be able to read every audience lane title, including **"Six parallel audience lanes"** examples. Match foreground and background colors explicitly; do not inherit light-on-light or dark-on-dark colors from host themes. Normal labels must contrast >=4.5:1; meaningful arrows/focus >=3:1. Test both browser light and dark schemes, desktop/mobile, focus and dimmed/selected states. The protected viewer supplies \`--aw-lane-fg\`/\`--aw-lane-bg\` and a forced-colors fallback.

Use the optional developer command: \`python scripts/aosw-contrast-audit.py --html /path/to/index.html --out /path/to/audit-evidence\`. Review the generated \`contrast-report.json\` and screenshots; CI must reject noncompliant examples. For an agent with no Chromium available, investigate authorized alternatives and repair clearly deficient CSS without asking for a new human approval. This check does not replace general accessibility testing.
