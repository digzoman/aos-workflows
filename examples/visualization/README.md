# Workflow visualization example

This **sanitized fictional Bucket 9** snapshot exercises parallel coach/agency research, an all-reviewed join, offer/copy/creative and parallel CRM/landing branches, a prelaunch check and a withheld human launch gate. It is not current Ampgent provider state.

The schema is in ../../scaffold/aos-w/spec/schemas/visualization-snapshot.schema.json. The reference generator can render this JSON without PyYAML:

~~~sh
python scripts/aosw-visualize.py --snapshot examples/visualization/bucket9-stage.json --out /path/to/aos-w/agent-files/visualizations/bucket9-example/index.html
~~~

Open the resulting self-contained index.html in a browser and click any step. No external script or network required. Before publishing any real project snapshot to GitHub Pages, obtain explicit authorization and sanitize separately.


**How an agent should present a visualization:** prefer directly rendered HTML or a direct index.html file link. The GitHub Actions artifact may be ZIP-wrapped by GitHub; that is a secondary fallback and not the recommended user-facing interface. If only ZIP is possible, instruct the user to extract and open index.html. Hosting a sanitized public GitHub Pages site is optional, subject to explicit approval.
