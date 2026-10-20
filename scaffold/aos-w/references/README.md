# Reference guides

Start with `../README.md` and `../PROTOCOL.md`, then use these references **just when relevant**:

- [START-A-RUN.md](START-A-RUN.md), exact manual folder and record creation, safe task selection and resume.
- [INSTANCE-LAYOUT.md](INSTANCE-LAYOUT.md), protected base definitions versus user-generated instance/run trees.
- [UPGRADE-AND-PORTABILITY.md](UPGRADE-AND-PORTABILITY.md), copy/unzip to local/cloud and upgrade without overwriting agent-files.
- [EVIDENCE-AND-PERMISSIONS.md](EVIDENCE-AND-PERMISSIONS.md), review, identity, approval and source-of-truth distinctions.
- [SCHEDULES-AND-SKILLS.md](SCHEDULES-AND-SKILLS.md), manual defaults, optional host wake and task-specific trusted skills.

These documents are part of the **protected** scaffold. Put project-specific variants into `agent-files/`.

- [COMPOSITION.md](COMPOSITION.md), new 0.2.0 file-native template overlays, dependency/readiness contracts, dynamic child approval and reviewed merging.

- [STATE-AND-RECOVERY.md](STATE-AND-RECOVERY.md), 0.3.0 event history, checkpoint, bounded retry, external-operation reconciliation and cold-start handoff protocol.

- [PROVENANCE-QUALITY-PERMISSIONS.md](PROVENANCE-QUALITY-PERMISSIONS.md), v0.4.0 identity, advisory claims, version-bound reviews, remediation, scoped approvals and handoffs.

- [GIT-SYNC-AND-COORDINATION.md](GIT-SYNC-AND-COORDINATION.md), v0.5.0 optional local/Git/multiagent modes, remote refresh, explicit Git ref CAS, LFS limitations, offline recovery and safe handoffs.

- [INSTALL.md](INSTALL.md), clean standalone ZIP installation, no-script quick start and upgrades preserving agent-files.
