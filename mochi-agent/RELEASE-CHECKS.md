# Release checks: nurseisangel

After every publish (a merged `publish.py` PR here):
1. The Pages run for the merge commit is **success**.
2. Every URL in `HEALTH-CHECK.md` answers as listed (cache-busted).
3. The first-visit smoke test passes (hosts as listed; widget.js 200; the beacon 204).
4. What the PR changed is read back live (e.g. a product's card and its `/go/<id>/` → 302 to the store; the head tags).
5. **No /gifts/** unless the PR is #223's go-live (`publish = true`), and then its 12 picks re-checked on amazon.com.
6. A product that goes live: one `?src=test` click seen end to end (page → `/go/` → store; the counter's `go`).
Results on the PR's Task issue.
