# Agent Files, the Writable Workspace

This is the **only normally writable directory within an installed `aos-w/` folder**.

Future installed systems will store project-specific configuration, customized templates, workflow runs, progress, state, checkpoints, evidence, reviews, handoffs, revisions, and history here.

This boundary allows the standardized AOS-W framework to be replaced or updated without silently replacing user data.

Standalone use must not require Git. When Git synchronization is intentionally configured, agents must check current remote state before shared edits and synchronize completed work using the selected coordination policy.

**Current state:** documentation only. No workflow execution conventions have been finalized or implemented yet.
