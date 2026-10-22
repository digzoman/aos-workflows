# Writable workflow visualizations

Agents can create read-only HTML workflow diagrams here under agent-files/visualizations/<view-id>/index.html, with a JSON source projection in snapshot.json if available. Only agent-files is writable during normal usage.

Read ../../references/VISUALIZATION.md. Workflow status is a point-in-time snapshot, not actual provider truth. A visualization never changes run data, approves work or executes actions. Open index.html in a local browser, or provide it as a file to the user. Public GitHub Pages deployment requires separate explicit approval and sanitization.

## HTML-first viewing and sharing

Render/open the generated index.html directly in a supported HTML/browser preview, or share a direct individual HTML file link/attachment. A ZIP is the last resort only for platform-forced bundling, multiple assets, or a user request; say how to open index.html after extraction. The separate AOS-W multi-file framework release remains a ZIP. GitHub Pages requires prior owner approval and a distinct sanitized export.
