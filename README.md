# nurseisangel-www

**https://nurseisangel.com**: the Nurse Is Angel page (thank-you gifts for nurses; campaign 001 First Cent,
ptk-studio#191). Hosted on **GitHub Pages** like ptk-studio.com and honeystorm.com (Owner, 2026-11-17).

## Update the site
```
python3 publish.py        # runs build.py, writes docs/ (the Pages source: main, /docs)
python3 -m unittest discover -s tests
git add -A && git commit -m "…" && git push
```
Edit the content in `sites/nurseisangel/` (`site.toml` = products and links, `content.md` = text, `img/`).
The generator (`build.py`, `templates/`, `tests/`) is copied from `ptk-studio/audience-pages`, which stays the
template for future audience sites.

## GitHub Pages vs the generator's Cloudflare files
- `/go/<id>` product links: `_redirects` → `docs/go/<id>/index.html` (only ids in `site.toml`; store hosts are
  checked by `build.py`, so there is no open redirect). A "coming" product has no link and no page.
- `_headers` → a CSP and referrer `<meta>` in every page. `X-Content-Type-Options`, `Permissions-Policy` and
  `frame-ancestors` can't be set by a page; add them as a Cloudflare response-header rule if wanted (the DNS is on
  Cloudflare).
- The visit/click counter posts to `https://api.88eggs.com/funnel/v1/nurseisangel` (R53). No IP, cookie or device data.

## Hosting
- GitHub: Settings → Pages → Deploy from a branch → `main` / `/docs`; custom domain `nurseisangel.com` (`docs/CNAME`);
  Enforce HTTPS.
- Cloudflare DNS (nurseisangel.com): apex A 185.199.108.153, .109, .110, .111; `www` CNAME `ptk-studio.github.io`.
