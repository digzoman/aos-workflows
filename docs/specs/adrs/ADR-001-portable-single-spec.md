# ADR-001, One portable file-based workflow specification

**Status:** PROPOSED, research outcome only, **not approved**. Date: 2026-10-20. Prompt 07 PRD review is required before implementation.

## Context and evidence

User requirement: standalone downloaded \`scaffold/aos-w\`, no required Git/runtime/db/MCP/cloud; one spec must support ordered, conditional, child-run and parallel workflows. LangGraph graph API [W01/W02] demonstrates useful graph vocabulary while running a real Python framework.

## Proposed decision

Use one text-based workflow definition and one instance/run vocabulary across all environments. A compatible agent follows a documented manual runbook; optional host adapters can execute identical graph semantics more strictly. Keep installed base read-mostly; only \`agent-files/\` changes in ordinary use.

## Alternatives and tradeoffs

Separate offline and online workflow languages fragment templates; mandatory LangGraph fails zero-install. Bare instructions are advisory and cannot promise hard runtime enforcement. Optional helper scripts may add validation and performance without becoming dependencies.

## Validation and reconsideration

Prompt 16 prove single-agent cold-start resume from a copied folder; Prompt 17 prove same template in Git/shared mode. Label manual versus enforced capabilities accurately.
