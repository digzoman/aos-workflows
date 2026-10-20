# Coordination adapter notes

A file named CLAIMED or a timestamp/lease in `claims/` is **advisory** under standalone/single-writer use. This directory may store configuration/results from a future tested local atomic-claim or Git-based coordination adapter.

Git worktree lock is not a workflow task lock. Git LFS and Git ref CAS are competing future prototypes; no selected or tested default exists in this 0.1.0 scaffold. Never enable shared exclusive task execution on this documentation alone.
