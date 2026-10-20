# Optional Git coordination conformance fixture

`tests/test_git_coordination.py` creates an isolated **real bare Git server repository on local disk**, then clones it twice under the **same Git user name and email** while assigning different logical agent identities:

- `Max | ChatGPT | worker | process-a`
- `Fred | Codex | worker | process-b`

The suite exercises simultaneous new-claim pushes, ref-level CAS winner, stale worker token after release/reclaim, crash/expired claim needing recorded reassignment, unavailable remote, clean fast-forward, dirty tree rejection, divergent branches, path-safe staging and Git-provenance commit. No fixture contains credentials or real user content. The local bare repo is deleted after each test.

The `LFSLockPrototype` adapter has an unavailable-client test and a mocked JSON parsing test. **There are no actual Git LFS server lock/unlock tests** and no hosted GitHub push race results. See `temp/tests/PROMPT-13-GIT-COORDINATION.md`.
