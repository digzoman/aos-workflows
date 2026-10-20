# Prompt 17 — multi-process Git collaboration acceptance

This suite is **optional developer testing**, not required by the file-only installed `aos-w/` folder. It uses a real local Git bare remote with three clones and separate Python operating-system processes, a single shared Git login, independent four-field AOS-W agent identities, durable child runs (events, artifacts, checkpoint and handoff), and simulated offline competitor research. It does **not** impersonate or actually connect Claude, Codex, Muse, or another commercial AI harness. The 'independent reviewer' is a **separate deterministic process**, not an independent AI assessment.

Run from the development repository root:

```bash
python -m pip install pyyaml  # test host only
python -m unittest discover -s tests/acceptance -p 'test_git_cross_agent.py' -v
```

Optional **hosted** GitHub CAS and Git LFS probe is `hosted_github_claims.py`, invoked only by GitHub Actions with a scoped short-lived token. It creates unique namespaced claim refs and attempts to delete them after inspection. It never commits advertising data. GitHub access/branch rules and live LFS-lock support are observed separately as PASS, BLOCKED, or REVIEW_REQUIRED—not inferred from the local bare remote.

For production claims, refer to the existing provisional ADR-014 and the new P17 acceptance report. Claim refs cannot fence external APIs or prove a human approval. When remotes are unavailable, coordinated steps remain BLOCKED rather than treating a stale offline claim as ownership.
