# Creative workflow compositions, non-executable drafts

Prompt 04. These are proposed DAG examples, not YAML code or working execution definitions.

## Composition A, single source into approved Meta assets

```text
Research-selected source
 -> C01 verify -> C02 product truth -> C03 semantic gate
 -> C04 exact copy lock -> C05 art direction
 -> C06 generate hero / supporting imagery
 -> C07 brand/layout composite
 -> [no-imagery, imagery] variant branches
 -> C08 portrait/square per variant -> C09 export/integrity
 -> C10 semantic+visual+brand QC
 -> C13 owner variant selection
 -> C14 saved artifact read-back and separately authorized handoff
```

A failed format gate routes only to C08/C09 and affected QC. A semantic error routes upstream C03/C04 and only then dependent imagery/overlay parts. The owner may approve one variant and reject another, without discarding the approved sibling.

## Composition B, independent Fred/Muse bakeoff

```text
Shared source and truth/semantic specification
       /                                \
 Agent Fred independent pack      Agent Muse independent pack
       |                                |
 Own copy/images/QC files          Own copy/images/QC files
       |                                |
 Commit + submission freeze         Commit + submission freeze
       \                                /
      Independence gate (both submitted)
                    |
     Reciprocal separate peer critiques
                    |
  Comparison + human selection + revision request
                    |
    Only selected, rejected or revised branches
                    |
           Final asset approval
```

Historical R56/R61–R62 mandate that peer agents must not inspect new rival work before both first-pass sets are committed, and must preserve original submissions during critiques. AOS-W should capture that rule via configured dependencies, read restrictions where enforceable, and provenance rather than assuming instructions provide technical access control.

## Composition C, one brand/compliance fix without redoing research

```text
Approved source -> copy -> image candidate -> QC
                                   |
                        WRONG LOGO / WRONG SIZE
                                   |
                C12 selects narrow remediation
                                   |
                C07 official logo / C08 format
                                   |
                C09 export -> C10 affected visual QC
                                   |
                 Original research and copy PASS
                                   |
                 C13 owner confirms new exact hash
```

If changed embedded copy or funding number instead, route to C02/C04 and invalidate relevant downstream imagery/provider approvals. Preserve archived prior version.

## Composition D, research to staging separation

```text
Competitor research QC -> creative assignment
        -> creative branches and owner selection
        -> approved asset manifest
                  |
      **separate staging authorization**
                  |
      Meta fields+images uploaded PAUSED
                  |
       Provider read-back and previews
                  |
      **separate launch authorization**
```

Source evidence and local image QA never by themselves authorize live marketing changes. Each actual external action needs a host/connector and read-back.
