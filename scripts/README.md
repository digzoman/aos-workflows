# Optional AOS-W maintainer and host helpers

**No script, Python runtime or Git is required to operate the portable installed `aos-w/` folder.** A capable agent can use the shipped Markdown/YAML/JSON instructions. The scripts in the *development repository* are optional conveniences and are **not packaged** in the ZIP.

## Distribution and quick local work

```sh
python scripts/aosw-distribution.py build scaffold/aos-w dist/aos-w-portable-0.6.0.zip
python scripts/aosw-distribution.py verify dist/aos-w-portable-0.6.0.zip
python scripts/aosw-distribution.py install dist/aos-w-portable-0.6.0.zip /my/project/aos-w
python scripts/aosw-ops.py list /my/project/aos-w
# PyYAML optional for this helper's init command:
python scripts/aosw-ops.py init /my/project/aos-w research-starter first-research run-001 \
  --actor '{"agent":"researcher","platform":"local","role":"worker","instance":"session-001"}' \
  --parameters '{"question":"Compare hypothetical competitors"}'
python scripts/aosw-ops.py status /my/project/aos-w first-research run-001
python scripts/aosw-distribution.py upgrade dist/aos-w-portable-0.6.0.zip /my/project/aos-w
```

The builder packages an **allowlisted clean distribution**: protected master Markdown/YAML/JSON and declared skills plus nonsecret seed config/readmes only. It excludes *all* existing user-owned run/instance data, custom templates, private config, caches, development tools/scripts/tests, temp research, hidden Git metadata and other repo files. ZIP content is verified by a manifest of SHA256 hashes; unsafe ZIP entries, duplicate/case collisions and symlinks are rejected.

**Install** creates an `aos-w` directory at an arbitrary target with clean config and empty instance/custom subfolders. **Upgrade** checks schema compatibility, copies all existing user-owned agent-files, stages new protected files, and renames the previous installation into a sibling rollback backup. Do not delete that backup before verifying your data. Writes aren't a distributed atomic transaction or proof of durable network filesystem behavior.

## Specialized optional helpers already provided

| Operation | Tool | Runtime dependencies |
| --- | --- | --- |
| Discover, inspect, initialize | `scripts/aosw-ops.py` | Python standard library; PyYAML only for `init` |
| Build, verify, install, upgrade ZIP | `scripts/aosw-distribution.py` | Python standard library |
| Check master composition, parameters, child proposal/creation, joins | `tools/composition/cli.py` | Python + opt-in PyYAML |
| State/status, append history, create checkpoint, pause, resume, recover | `tools/state/cli.py` | Python + opt-in PyYAML for pinned graphs |
| Advisory claim, submit/review, grant/revoke, remediation | `tools/governance/cli.py` | Python + opt-in PyYAML |
| Git mirror, CAS claim, reconcile | `tools/git/cli.py` | Git + optional Python helper; Git only in this mode |
| Read-only scaffold structural check | `scripts/validate-scaffold.mjs` | Optional Node.js |

Run tests: `python -m unittest discover -s tests -p 'test_*.py' -q`. CI builds a tested ZIP in GitHub Actions and uploads it as a downloadable artifact. The artifact is **not** a GitHub Release asset unless separately published and verified.

No optional helper grants live external action authority, guarantees shared task exclusivity, or adds an always-on scheduler. See [full quick-start](../docs/installation/QUICKSTART.md) and installed `aos-w/references/INSTALL.md`.
