# Portable AOS-W distribution (0.6.0)

The self-contained folder is [aos-w/](aos-w/), and [INSTALL.md](aos-w/references/INSTALL.md) explains the zero-runtime/manual installation path. **Standalone usage does not require Git, Python, Node, an MCP server, a database, or a scheduler.**

The project supplies a separate, clean distribution ZIP `aos-w-portable-0.6.0.zip`, built and tested by [.github/workflows/aosw-portable.yml](../.github/workflows/aosw-portable.yml). When available, download it from the workflow's GitHub Actions Artifacts or the verified versioned preview release. The ZIP has only a single `aos-w/` root and a manifest of SHA-256 file hashes; it excludes repository development tooling and **all existing user-specific content** (the in-repo synthetic practice instance is intentionally not shipped). Its `agent-files/` is an **empty clean starter** except for safe default config and guidance.

Installed protected framework paths are replaceable by a versioned upgrade, but existing `agent-files/` must be preserved in their entirety. Never blindly unzip a new ZIP over an active installation. An optional stdlib distributor and safe upgrade helper live under [scripts/](../scripts/).

The core remains a manually operated agent-and-files framework; no unattended executor, authenticated approvals or production distributed task mutex is included.
