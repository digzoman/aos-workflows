# ADR-011: Versioned DAG and protected policy inheritance

**Status:** PROPOSED, Prompt 08 technical design; **not owner-accepted**. 2026-10-20. PRD review record remained pending when this document was written.

## Context
Q03/Q11/Q12/Q13 require reusable composed workflows, dynamic children, conditions, QC and configurable autonomy, without changing previously approved completed work.

## Proposed decision
Represent graph as stable-ID nodes with needs, three-valued declarative predicates, optional fan-out and join; pin effective graph snapshot per version. Inheritance merges by stable keys, protected permission ceilings intersect, weakening protected QC requires owner action. Graph revision records a diff and invalidates only downstream-dependent results, preserving old events and accepted unrelated branches.

## Consequences and alternatives
Using arbitrary executable predicates would require unsafe mandatory runtime. Strict keyed merge requires clearer authoring than naive YAML overlay; human-readability and explainable impact win over hidden magic.

## Required validation and reconsideration
Compound workflows, unknown source route, graph revision with price/logo updates, interrupted generator dedupe, independent parallel children and QC gates.
