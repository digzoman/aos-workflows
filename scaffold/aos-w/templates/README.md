# Built-in templates (read-only)

These are discoverable **master definitions**, not active runs. Never write results into this directory; to customize one copy it to `../agent-files/custom-templates/` or create a new pinned instance in `../agent-files/instances/`.

| Template | Trigger | Required tools | What it demonstrates |
|---|---|---|---|
| [research-starter](research-starter/README.md) | Manual, non-repeating | Files and capable agent | 3-step dependent research, bounded retry, step-local skill, manual evidence review |
| [periodic-review-example](periodic-review-example/README.md) | Optional disabled weekly schedule (manual launch always possible) | Files and capable agent | Stored recurrence **does not** wake any process, ad hoc invocation |

Find a `template.yaml`, read its `parameters`, `policy`, `skills`, `graph.nodes` and any `gates`. Verify the schema and avoid unapproved external effects. See `../references/START-A-RUN.md` to instantiate under agent-files.

The full Ampgent research-to-creative-to-Meta reusable template catalog is a **later milestone**, not bundled as a functioning suite yet.
