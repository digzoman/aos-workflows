# Periodic review declaration (not a running scheduler)

This template demonstrates the *data model* for recurrence:

- `trigger.kind: schedule` and RRULE `FREQ=WEEKLY;BYDAY=MO`
- Timezone `Etc/UTC`
- `enabled: false` in the bundled master example
- `missed_policy: manual_review`, `overlap_policy: block`

No scheduled execution takes place when you copy this folder. A template can always be launched **ad hoc**, recording `trigger_kind: manual` in its run. A real recurring run requires host wake plus authorization, unique occurrence IDs and (if shared) tested deduplication.

Only bounded read/local summary work is described. This does not grant ongoing permission to query private systems or send reports.
