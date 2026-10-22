# Workflow visualization example

This **sanitized fictional Bucket 9** snapshot exercises parallel coach/agency research, an all-reviewed join, offer/copy/creative and parallel CRM/landing branches, a prelaunch check and a withheld human launch gate. It is not current Ampgent provider state.

The schema is in ../../scaffold/aos-w/spec/schemas/visualization-snapshot.schema.json. The reference generator can render this JSON without PyYAML:

~~~sh
python scripts/aosw-visualize.py --snapshot examples/visualization/bucket9-stage.json --out /path/to/aos-w/agent-files/visualizations/bucket9-example/index.html
~~~

Open the resulting self-contained index.html in a browser and click any step. No external script or network required. Before publishing any real project snapshot to GitHub Pages, obtain explicit authorization and sanitize separately.


**How an agent should present a visualization:** prefer directly rendered HTML or a direct index.html file link. The GitHub Actions artifact may be ZIP-wrapped by GitHub; that is a secondary fallback and not the recommended user-facing interface. If only ZIP is possible, instruct the user to extract and open index.html. Hosting a sanitized public GitHub Pages site is optional, subject to explicit approval.


## v0.9 human-first illustration

A separate fictional 56-node sample is provided at synthetic-six-audience.json. The optional scripts/aosw-visualize.py generator turns it into human-readable HTML with six ready independent reviews, semantic workstream labels and source guidance. No private Ampgent research, brand assets or live campaigns are included. GitHub Actions can generate this page; a public browser URL requires an intentionally manual, approved Pages deployment (see docs/installation/V09-PAGES.md), not simply linking to a GitHub source file.


## v0.9 accessibility six-lane example

**[Six parallel audience lanes — accessible standalone HTML](six-lane-accessible.html)** is a fictional UI fixture for the exact reported **nearly-white-on-white audience heading** defect. The six headings have explicit contrasting color/background pairs and do not inherit host text colors. Desktop/mobile and light/dark browser screenshots plus computed contrast ratios are checked in CI.

The [synthetic 56-step sample](synthetic-six-audience.json) exercises the *actual viewer*, complete with six parallel audiences, 6 READY review steps, and readable stage labels. It remains test data, not a real Bucket 9 work report.

Optional standalone audit after generating a page: \`python scripts/aosw-contrast-audit.py --html /path/to/index.html --out /path/to/screenshots --six-lanes\` (use \`--six-lanes\` for the six-heading standalone fixture, not the generic DAG columns). If a heading becomes white-on-white, the audit must fail. Code files on GitHub are not executed HTML pages; download/open the individual HTML file or use an explicitly approved rendered host.
