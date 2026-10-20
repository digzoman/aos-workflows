# Selected synthetic acceptance evidence (Prompt 16)

These files come from an actual local execution of the verified AOS-W v0.6.0 standalone ZIP. Fictional offline products and mock approvals are **not** real providers, customers, ad campaigns or permissions.

The evidence under `offline-research/`, `custom-instance/`, `recovery/` and `cancellation/` is **sample output of the acceptance run**, not a user installation or a template. It is intended to demonstrate real event history, evidence hashes, review decisions, retry attempts, graph revision, safe cancellation, and explicit corrupt-tail recovery. It does not establish external truth or hard multi-agent protection.

The complete, independent local installation under the sandbox test working directory is not committed (to prevent copying user-owned runtime folders into the public development repository). The reproducer creates that tree afresh. The corresponding SHA-256 protected manifest is included so future testers can compare release framework files.

See [the detailed report](../../../docs/testing/PROMPT-16-STANDALONE-ACCEPTANCE.md) and [the repeatable runner](../run_standalone_acceptance.py).
