# Portable AOS-W scaffold

The self-contained installable folder is [aos-w/](aos-w/). It now contains operating documentation, 16 draft JSON Schemas, master templates, a bundled skill, user-only writable agent-files config, and an inert practice instance.

**Standalone operation is manual and cooperative.** Download GitHub's whole-repository ZIP, then extract/copy only `scaffold/aos-w/` to a local or persistent cloud folder. After installation no Git, Python, Node, database, MCP or scheduler is required for a capable agent to follow the file protocol.

Only `aos-w/agent-files/` is normally writable. Future framework releases replace protected material while preserving this user-owned subtree. See `aos-w/references/UPGRADE-AND-PORTABILITY.md`.

Optional project maintainer helper: `sh scripts/package-scaffold.sh` from the development repository root creates a ZIP containing only the installable folder if `zip` is installed.

This is an initial scaffold, **not** a fully automated agent workflow engine or tested multi-agent locking system.
