# Candidate Workflow Compositions, Non-Executable Examples

Prompt 03. These are **specification sketches only**, not runnable YAML or implemented schemas.

## A. Broad Meta source-ad research, queue driven

```
Start
  -> Preflight T01
  -> Research plan + queues T02/T03
  -> Advertiser batch workers T04 (next 6, repeat from persisted queue)
  -> Advertiser finalizer T07, with T12 access retries
  -> Keyword batch workers T05 (next 8, repeat from persisted queue)
  -> Normalize T06 and targeted T12 retries
  -> Final coverage gate T07
  -> Ad scoring T08
  -> Independent QC T10
  -> Synthesis T11
  -> Handoff T14
```

Observed inspiration R03–R04/R21–R31. Exact original loop counts are historical configuration. **Proposed:** make batch sizes and search gates parameters. The queue, not chat memory, selects work. Do not mark a source absent when a search page did not render.

## B. Fifteen audience investigations, conditional fan-out

```
Start -> Preflight T01 -> Portfolio planning T02
                              |
                         Generated proposals
                              |
                    Human/batch authorization gate
                        /       |       \
                    T09 run A  T09 run B  T09 run N
                      |          |         |
                      QC T10     QC T10    QC T10
                        \         |        /
                  Complete/qualified reviewed set
                              |
                        Synthesis T11
                              |
                Conditional specialty proposals T13
                              |
                    Approval or deferred queue
```

Observed inspiration R37–R49. The **historical 15 runs were separately authorized**, not auto-executed in parallel. **Proposed:** future AOS-W may support approved parallel branches with isolated files and safe coordination, or preserve an individually authorized mode for sensitive research.

## C. Research correction or source-access fallback

```
Claim query -> live source check
   | normal evidence       -> normalize -> QC -> pass
   | legitimately empty    -> EMPTY_VERIFIED with method
   | blocked/unreliable    -> RETRY_REQUIRED -> T12 bounded retry
   |                                     | retry succeeds -> evidence
   |                                     | exhausted -> BLOCKED + impact
   | weak/incomplete       -> REVISE -> only affected query rerun
```

Observed inspiration R24/R34. **Proposed:** do not incorrectly collapse unavailable/empty/not-relevant into one terminal state.

## D. Research to production separation

```
Reviewed research -> strategic candidate decision
                              |
                   **separate authorization**
                              |
                 Creative work (Prompt 04 study)
                              |
                        creative QC
                              |
                   **separate authorization**
                              |
                 Meta staging (Prompt 05 study)
                              |
                     live read-back
                              |
                   **separate launch approval**
```

The current task **only researches** the upstream stages. Nothing here authorizes campaign creation, spending or actual publication.

## Draft artifact contract, for PRD discussion

A hypothetical vertical child run would have immutable run identifier, template version, approved source/market and research objective, output locations for `PROGRESS.md`, `EVIDENCE-LOG.csv`, `SCORECARD.md`, `RESEARCH-REPORT.md`, source verification metadata, one source-of-truth state file, optional agent handoff, independent review, and links to the parent portfolio. The exact format/path is **undecided**.

The baseline trigger is **ad hoc**. An optional template schedule may suggest recurring research refreshes, but without a host scheduler no automatic wake occurs. Run-scoped skills may point to a locally bundled research playbook or an explicitly pinned external research procedure loaded only at the relevant step. These reflect user requirements added under Prompt 01b, **not historical execution features**.
