# Agent Files, the Writable Workspace

This is the **only normally writable directory within an installed `aos-w/` folder**.

Future installed systems will store project-specific configuration, customized templates (including their bundled skills), active workflow instances (including their bundled skills), optional schedule overrides, workflow runs, progress, state, checkpoints, evidence, reviews, handoffs, revisions, and history here.

A step may refer to bundled, previously installed, local, or repository-hosted skills, to be consulted only when that step needs them. A remote skill reference never grants new access or execution permissions.

This boundary allows the standardized AOS-W framework to be replaced or updated without silently replacing user data.

Standalone use must not require Git. When Git synchronization is intentionally configured, agents must check current remote state before shared edits and synchronize completed work using the selected coordination policy.

**Current state:** documentation only. No workflow execution conventions have been finalized or implemented yet.
