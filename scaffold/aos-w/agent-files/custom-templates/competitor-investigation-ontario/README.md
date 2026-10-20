# Example custom overlay, user-owned

This example stays under **agent-files**, not in protected master templates. It changes the competitor investigation search instruction for Ontario while preserving the exact approved parent template version and a SHA-256 source pin.

To use it, resolve it against `templates/competitor-investigation/template.yaml` whose SHA-256 must match `base.content_digest`. Do not silently rebase when the publisher changes the master; create a new explicit custom revision after review. The overlay narrows or preserves permissions and cannot remove mandatory human approval or independent evidence gates.

This is a sanitized example, not a completed live competitor investigation or permission to access accounts.
