# AOS-W Portable Folder

**Status: structural placeholder, not implemented.** This folder is the future standalone AOS-W distribution and should not depend on the surrounding development repository to operate.

Planned standardized contents:
- Instructions and specifications describing task selection, operation, quality control, handoffs, and recovery.
- Versioned master workflow templates and optional structured schemas.
- An explicit `agent-files/` workspace.

**Immutable-by-default boundary:** During normal use of an installed copy, agents must only edit files underneath `agent-files/`. They must not alter framework documentation, base templates, or schemas. Changes to standardized materials require an intentional versioned upgrade or maintenance action, not routine workflow execution.

When built, `agent-files/` will include custom templates, current workflow definitions, configured execution modes, runs, evidence, state, review results, and history.

Do not claim execution, locks, permissions, validation, or synchronization work already. All are future features documented in the design records.
