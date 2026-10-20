# Open Questions, No Unilateral Resolution

These questions are intentionally deferred until research and PRD review. Record proposals with rationale before marking any decision approved.

1. Which Git shared-claim mechanism wins after **real LFS vs atomic claim** tests, especially when different agents share one GitHub identity?
2. What guarantees must cloud file storage provide for persistence, atomic file updates, and concurrent claims?
3. Which restrictions can the file protocol express, and which require optional tooling or an executor for hard enforcement?
4. How are offline and cloud single-agent workflow instances distinguished from collaborative shared instances in config without overly complex modes?
5. What canonical state/event schemas, validation policy, and recovery model best support YAML, Markdown, JSON, and JSONL?
6. How do future standardized scaffold upgrades preserve `agent-files/` reliably?
7. Which open-source license should govern the public framework? None is selected.
8. How much Meta advertising creation and implementation qualifies as a bounded V1 pilot, without implying permission to publish live ads?
9. What is the specific policy for expiring ownership/leases and reclaiming abandoned tasks when no daemon exists?
10. Which LangGraph patterns should be borrowed conceptually, and which require an actual runtime?

Open questions are not blockers for Prompt 02 research unless explicitly noted.
