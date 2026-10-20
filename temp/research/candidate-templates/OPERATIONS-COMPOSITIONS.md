# Prompt 05 composition sketches, non-executable

These are **design proposals only**, intended to feed Prompt 07 PRD and Prompt 08 schema.

## A. Safe new offer staging

```text
Research QC + Creative final asset selection
       -> M01 provider preflight
       -> M02 campaign/adset/ad plan + M03 target review
       -> [M04 creative bind, M05 message fields,
           M06 CRM, M07 website, M08 tracking]
       -> M09 PAUSED stage (authorized)
       -> provider readback -> M10 independent launch QA
       -> report gaps and request owner launch permit M11
```

One branch may be done while another is pending; passing exact media and text cannot silently waive CRM/routing or placement issues.

## B. Controlled, owner-approved launch

```text
M10 latest QA + M11 exact owner permit
   -> fresh campaign tree and holds
   -> activate only selected ads
   -> activate selected adsets
   -> activate selected parent campaigns
   -> M12 provider read-back per object level
   -> review/serving/first insights observation
   -> M13 read-only monitoring
```

The exact historical Oct 15 sequence is observed in R88. Do not call a write accepted "delivering"; if account readback is rate-limited, record pending verification and do not issue duplicate activation changes.

## C. Geographical correction without destructive replay

```text
Current targeting readback + owner-specific correction
  -> M03 explicit diff and implications
  -> approve scope and age/Advantage+ constraints
  -> update only affected adset or safely replace if required
  -> provider readback, preserve paused/live parent state
  -> selectively refresh audience QA + launch readback
```

B5 geographic correction and Oct 14/15 age revisions demonstrate why an old targeting research conclusion must not be assumed permanently correct.

## D. Failed click-to-message/CRM or tracking check

```text
Meta creative and message fields PASS
       |
HighLevel end-to-end behavior UNKNOWN -> M06 safe regression and channel test
       |
Booking Schedule dedup UNKNOWN -> M08 event identity and consent audit
       |
Only the failing integration QA is retested
       |
M10 records independently verified status per gate
```

Do not reissue ads, rewrite copy or mutate GHL automation because a read-only access surface failed.

## E. Optional recurring performance review

Template includes an **optional declared schedule**; default manual invocation remains possible. A connected host may initiate a read-only M13 instance with its own date window and result files. The scaffold itself has no always-running scheduler. Proposed optimization M14 needs separate workflow-specific permissions before applying any live change.
