# Scheduled work: nurseisangel-www (R93)

**Nothing is scheduled in this repo** (checked 2026-11-18). GitHub Pages serves `docs/`, which is written only by a reviewed
PR from audience-pages (`publish.py nurseisangel --to …/docs`).

**Waiting on an event:** the gift page (`/gifts/`, ptk-studio#223) is published when the first Nurse Is Angel
product is live (mm1-worker2's sweep check), then its 12 Amazon items are re-checked monthly.

**Runs elsewhere and touches this site:** the funnel beacon's counts (88eggs-worker, `funnel-retention` daily) and
the daily Funnel rows (a hub-wide job in the hub's `mochi-factory/SCHEDULE.md`).
