# AOS-W Development Repository — Agent Entry Point

For any Codex/Claude/ChatGPT/other coding agent entering this repository:

- Product: portable, file-first **Agent OS Workflows**, code under \`scaffold/aos-w/\`; user-owned run data belongs exclusively under an installed \`aos-w/agent-files/\` folder.
- Read \`scaffold/aos-w/PROTOCOL.md\`, \`scaffold/aos-w/VERSION.json\`, \`docs/specs/architecture/ARCHITECTURE.md\`, and the active run's pinned graph + saved handoff before modifying anything.
- Current feature specification: \`docs/specs/v0.9/V0.9-PRODUCT-SPEC.md\`. Existing stable Version 1 acceptance tests are **not waived**.
- For a workflow assigned in a different host repository, follow that repository's own instructions first and then its installed \`aos-w/AGENTS.md\`; never overwrite a pre-existing entry point.
- Work proactively. A missing declared tool is **not** permission to refuse or create a human gate. Use authorized alternatives, retry, and continue safe parallel work. Read \`scaffold/aos-w/references/CAPABILITY-RECOVERY.md\`.
- Preserve machine IDs, graph revisions, events, exact artifact reviews, independent QC and already-defined owner grants. Git commits or tool names do not create external provider authority.
- To validate code, run \`python -m unittest discover -s tests -p 'test_*.py' -q\`. Optional developer dependencies may be needed; the distributed AOS-W folder itself requires no Python/Git/MCP/server.
- Viewer: \`scaffold/aos-w/references/visualization-viewer.html\`; its HTML-first human conventions are in \`scaffold/aos-w/references/HUMAN-FIRST.md\`.
- Do not publish private workflow snapshots to a public GitHub Pages site. Separate owner authorization and redaction are required; GitHub source \`blob/\` URL is not an interactive webpage.

This file is a short discoverability pointer, not a replacement for the detailed protocol or permission system.
