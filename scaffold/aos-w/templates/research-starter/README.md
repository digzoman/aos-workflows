# Research starter template

**Template ID:** `research-starter`; `version: 0.1.0`. Standalone manual, non-repeating, local-file-only by default.

1. Supply a bounded `question` and optional `scope`.
2. Pin `template.yaml` to your new instance under `agent-files/` before starting.
3. `define-scope` creates `artifacts/scope.md`.
4. `collect-evidence` uses only the [bundled evidence-handling skill](skills/evidence-handling/SKILL.md) at that step, preserving source dates/limitations in `artifacts/evidence.md`.
5. `review-evidence` performs a permitted self-review on the exact artifact set, documents the verdict and produces `artifacts/summary.md`.

The review is **not independently reviewed**; the configured gate is `self_review` because this is a low-risk local starter. More consequential workflows can require `ai_independent` or human gates. This template never authorizes live provider writes, messages, deployment or ad spend.

Outputs are **run-root-relative** paths, e.g. `agent-files/instances/<instance-id>/runs/<run-id>/artifacts/scope.md`, not paths inside this protected template directory.

If source material is inaccessible, use retry/blocked notes instead of declaring it absent. No scheduled execution or automatic runtime is included.
