# Compound marketing lifecycle — 0.7.0

**Definition only.** Each stage pins an independently executable module by version and SHA-256. Any stage may be started as a standalone workflow; no parent has blanket authority to instantiate children, write to ad accounts, or treat a completed plan as an accepted run.

The parent `research-fanout` node is a child proposal generator and should use an approved buyer portfolio to create stable IDs; generated competitor observations are independently reviewed before evidence consolidation. The planner and reviewer versions are recorded separately. The parent `evidence` node is an ALL ACCEPTED join.

After owner-verified deliverable offer (distinct from competitor research and the proposed hypothesis), copy and visual work branches, while CRM and landing-page preparations can run independently. Tracking depends on the CRM/site definitions. Final integration joins all required producer outputs and exact artifact quality gates.

`launch-approval` requires exact HUMAN approval for live activation, without executing it. The parent deliberately contains **no automatically executable live-publish node**. `monitor` requires actual later provider evidence; the grant itself does not mean ads are running. `optimize` requires separate authorization for any proposed live changes.

The `composition.children` list is an auditable source of digest-pinned subworkflow references; `${artifact...}` strings are **manual binding placeholders** and are not evaluated as code. Resolve them against actual current artifact IDs before child instantiation, or mark child WAITING. The parent is not an automatic dispatcher.

See `examples/conformance/marketing/` in the development repository for mock planning, parallel readiness, review failure and instantiated, never-executed samples.
