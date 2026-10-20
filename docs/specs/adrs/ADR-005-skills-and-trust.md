# ADR-005, Reusable step-local Agent Skills with explicit trust and version

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

User Prompt 01b requires template and instance skills, installed/local and repository references. Agent Skills spec [W09] defines progressive-disclosure \`SKILL.md\` package; A Rep [A05] separates experimental and human-approved skills.

## Proposed decision

Each step declares required/on-demand skills with explicit resolver paths and optional pinned revision/hash. Official master-template skills stay in read-mostly scaffold; custom/run-specific ones under \`agent-files/\`. External skill source is untrusted until checked; instructions or scripts never expand permission. Missing mandatory skill marks step BLOCKED or uses an approved local fallback.

## Alternatives and tradeoffs

Global automatic imports risk malicious instructions and broken offline runs. Only local skills reduce portability of references. Remote scripts must never execute on reference alone. Exact precedence for conflicting names remains open for PRD approval.

## Validation and reconsideration

Test offline missing skill, hash mismatch, malicious/conflicting remote instruction, custom override, optional logo skill without Python and just-in-time resource loading.
