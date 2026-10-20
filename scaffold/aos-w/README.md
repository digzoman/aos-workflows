# AOS-W Portable Folder

**Status: structural placeholder, not implemented.** This folder is the future standalone AOS-W distribution and should not depend on the surrounding development repository to operate.

Planned standardized contents:
- Instructions and specifications describing task selection, operation, quality control, handoffs, and recovery.
- Versioned master workflow templates and optional structured schemas. Templates may bundle skills alongside their definitions and declare an optional overridable schedule; default is one-off execution.
- Step-level references to just-in-time skills, whether template-bundled, instance-bundled, previously installed, local, or external.
- An explicit `agent-files/` workspace.

**Immutable-by-default boundary:** During normal use of an installed copy, agents must only edit files underneath `agent-files/`. They must not alter framework documentation, base templates, or schemas. Changes to standardized materials require an intentional versioned upgrade or maintenance action, not routine workflow execution.

When built, `agent-files/` will include custom templates and any skills bundled within them, workflow-instance skill bundles, current workflow definitions, optional schedule overrides, configured execution modes, runs, evidence, state, review results, and history.

Recording an optional schedule will not by itself launch a workflow. Host-specific triggering, if available, will be optional and separately authorized. A recurring-capable template must also support an ad hoc one-off launch.

Do not claim execution, locks, permissions, validation, or synchronization work already. All are future features documented in the design records.
