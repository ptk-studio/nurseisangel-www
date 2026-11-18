# Health check: nurseisangel

Agents read the checks from **this file** (handbook `project-groups/AGENTS.md` → "Health checks"; types in
`PROJECT-TYPES.md`). Change it by PR.

## Type `web`
- **Repo / deploy:** `ptk-studio/nurseisangel-www`, GitHub Pages from `main:/docs`; a merge to `main` is a production
  deploy. Source: `ptk-studio/audience-pages` (`sites/nurseisangel/`).
- **Check URLs (every manager sweep; each must answer as shown):**
  | URL | Expect |
  |---|---|
  | https://nurseisangel.com/ | 200, `og:image` present, the beacon and the Feedback widget in the page |
  | https://nurseisangel.com/privacy/ | 200 |
  | https://nurseisangel.com/robots.txt | 200, names the sitemap |
  | https://nurseisangel.com/sitemap.xml | 200 |
  | https://nurseisangel.com/img/og.jpg | 200 `image/jpeg` |
  | https://api.88eggs.com/funnel/v1/nurseisangel (POST, the page's beacon) | 204 |
  | https://nurseisangel.com/gifts/ | **404 until #223's go-live** (`publish = false` in `gifts.toml`); 200 after |
  | each live product's `https://nurseisangel.com/go/<id>/` | 200 page that forwards to the store (none yet: all "Coming soon") |
- **Hosts a first visit may reach (R53):** nurseisangel.com, api.88eggs.com, and GA4's www.googletagmanager.com /
  www.google-analytics.com (consent mode v2). Anything else is a fail.
- **Traffic source:** the 88eggs funnel counter (daily CSV in the hub) and GA4 `G-S0S9JV0LHQ`.
- **Smoke test:** `node tools/first-visit.mjs --allow nurseisangel.com,api.88eggs.com,www.googletagmanager.com,www.google-analytics.com,region1.google-analytics.com https://nurseisangel.com/?src=test` (in audience-pages) → PASS.
