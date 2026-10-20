**Latest published preview:** v0.7.0 with the 21-module marketing library. Download https://github.com/digzoman/aos-workflows/releases/download/v0.7.0-portable-preview/aos-w-portable-0.7.0.zip . Verified hosted SHA-256 0826ddf9807354e80e22b757dd129b86539aae8d6ff3c7799029e5f3719c74f7 . Hosted CI 39434478250 and subsequent 39495294210 both succeeded. The 0.6.0-specific commands and original evidence below remain as a historical reference, replace the version and ZIP filename with 0.7.0 for current installs. Do not treat preview as approved V1.

# Install and start AOS-W 0.6.0

AOS-W's **portable core is a set of Markdown, YAML and JSON files**. It does not need Python, Git, Node, MCP, a server or a running daemon. A capable AI agent follows `aos-w/README.md` and `PROTOCOL.md` using persistent file storage. No background execution or distributed-lock guarantee is implied.

## Downloading the standalone archive

The development repository's distribution workflow builds **`aos-w-portable-0.6.0.zip`**, whose only top-level directory is `aos-w/`. It has been published and verified: [download the 0.6.0 standalone preview ZIP](https://github.com/digzoman/aos-workflows/releases/download/v0.6.0-portable-preview/aos-w-portable-0.6.0.zip). The [CI workflow run](https://github.com/digzoman/aos-workflows/actions/runs/39415147383) passed the complete regression suite and install/upgrade tests; the ZIP's SHA-256 is `7d9ce9a3ea72f9546fe9d398647d76867bd1766a42bae717d6912f827734c5e9`. This archive does **not** contain `docs/`, `tools/`, `scripts/`, `tests/`, `temp/`, `.git/`, examples, existing runs, or custom user templates. It includes protected specifications, master templates, bundled skills, documentation, `VERSION.json`, an integrity manifest, and a clean starter `agent-files` layout. The synthetic repo practice run is deliberately *not* included in clean installs.

**No helper required:** Download and extract the ZIP into any durable local/cloud working directory. The extracted folder `aos-w/` is immediately usable. Read `aos-w/README.md`, `aos-w/PROTOCOL.md` and `aos-w/agent-files/README.md`. Ask an AI agent to list templates and create a *new* instance under `agent-files/instances/`, pin the selected source `template.yaml`, and write event/state/handoff records. See `aos-w/references/START-A-RUN.md`.

**Optional checked installation:** From the **development repository** and with Python available (not required after installation):

```sh
python scripts/aosw-distribution.py verify dist/aos-w-portable-0.6.0.zip
python scripts/aosw-distribution.py install dist/aos-w-portable-0.6.0.zip /work/project/aos-w
python scripts/aosw-ops.py list /work/project/aos-w
```

If `PyYAML` is **optionally** installed in this development/host environment:

```sh
python scripts/aosw-ops.py init /work/project/aos-w research-starter research-demo run-001 \
  --actor '{"agent":"researcher","platform":"local","role":"worker","instance":"session-001"}' \
  --parameters '{"question":"Compare three fictional services"}'
python scripts/aosw-ops.py status /work/project/aos-w research-demo run-001
```

The initializer records CREATED and first READY candidates. **It does not run a research task, make provider calls, grant human authority, or schedule anything.** For actual work follow the in-folder manual protocol or use optional state/governance helpers explicitly.

## Upgrades preserving user data

**Never** extract a fresh ZIP blindly over an existing installation. A normal workflow must write only under `agent-files/`. For a manual upgrade, take a complete backup; replace protected `README.md`, `PROTOCOL.md`, `VERSION.json`, `spec/`, `templates/`, and `references/` from the new ZIP, retaining the original `agent-files/` untouched. Check any schema-major compatibility requirements and pinned graph history before resuming.

The optional installer safely stages a replacement and keeps a rollback backup:

```sh
python scripts/aosw-distribution.py upgrade dist/aos-w-portable-0.6.0.zip /work/project/aos-w
```

It checks ZIP entry names and SHA-256 manifest, disallows symlinked user trees, copies the **entire** existing `agent-files/` byte-for-byte, stages a new protected tree, and renames the old installation to a sibling backup. On error it attempts to restore the original. Atomic rename/durability depend on the actual host filesystem. The backup includes private user data; secure it and remove it only after verification. No automated migration of schema-major versions is attempted.

## Optional helper index

| Work | Manual path | Optional deterministic helper |
| --- | --- | --- |
| Find workflows / inspect state | `templates/README.md`, `instances/`, pinned graph + event log | `scripts/aosw-ops.py list/status` |
| Start one-off workflow | `references/START-A-RUN.md`; pin immutable template | `scripts/aosw-ops.py init` (PyYAML optional) |
| Validate graph, parameters and fan-out | `references/COMPOSITION.md` | `tools/composition/cli.py validate/resolve/propose` (PyYAML) |
| Claim and review a task | `references/PROVENANCE-QUALITY-PERMISSIONS.md` | `tools/governance/cli.py claim/review/revoke/...` (PyYAML as needed) |
| Append event/checkpoint/recover | `references/STATE-AND-RECOVERY.md` | `tools/state/cli.py checkpoint/recover/...` (PyYAML) |
| Optional Git sync/CAS | `references/GIT-SYNC-AND-COORDINATION.md` | `tools/git/cli.py` (Git required **only for that mode**) |
| ZIP build/verify/upgrade | Manual folder transfer and protected-file-only upgrade | `scripts/aosw-distribution.py` (stdlib only) |

All helpers are **developer or host opt-ins**, not included in the installed core ZIP. None authenticates a human decision, proves an external service changed, or creates an unattended scheduler. The core is usable offline by an agent capable of reading/writing files.

## Troubleshooting

A missing task source, unknown schema version, invalid ZIP hash, unavailable reviewer or provider readback, or unverified shared task claim is a **BLOCKED** condition. Record it in `handoff.md`. Do not transform uncertainties into PASS or retry unknown external side effects. An upstream template update never modifies an existing pinned run without an authorized revision.
