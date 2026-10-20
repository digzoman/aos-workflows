# Optional development helpers

**No helper is required to use the downloaded `scaffold/aos-w/`.** The standalone user follows `scaffold/aos-w/PROTOCOL.md` with an AI agent and persistent files.

- `node scripts/validate-scaffold.mjs` — optional Node.js (no additional packages) read-only structural checks for the scaffold, its 16 copied draft schemas, pinned practice instance, event sequence, directory layout and inert defaults. You can pass a copied folder path. **Does not validate YAML semantics or implement a workflow engine.**
- `sh scripts/package-scaffold.sh` — optional release-packaging helper, requiring `zip`. Should produce an `aos-w-portable.zip` with only `aos-w/`, no Git required inside archive. If your host lacks `zip`, download GitHub's full repository ZIP and copy the subfolder.

All scripts are **developer conveniences** and are never mandatory dependencies of the scaffold. They do not authorize Git/Meta/GHL writes, scheduled execution or agent coordination.
