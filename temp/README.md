# Tracked Development Workspace

Unlike most throwaway temporary folders, `temp/` is **tracked in Git** so independent agents and fresh sessions can reliably recover design decisions and work status.

Required orientation sequence:
1. `OPERATING-RULES.md`
2. `DESIGN-DECISIONS.md`
3. `WORK-PLAN.md`
4. `PROGRESS.md`
5. `HANDOFF.md`
6. Research notes, unresolved decisions, and implementation history as needed.

This is a **public** repository. Never put personal information, private customer/business data, raw conversations, API keys, tokens, credentials, confidential screenshots, unredacted ads-account exports, or identifying provider objects in this directory. Keep useful sanitized summaries and source pointers instead.

The `temp/` folder contains **development** working material. It is separate from the installed scaffold's `agent-files/` directory, which is the only normally writable runtime workspace.

Migrate durable approved specifications into `docs/` after review. Keep a trace in the change history. Do not delete important work-in-progress records solely because a new session starts.
