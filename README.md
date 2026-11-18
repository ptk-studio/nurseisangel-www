# nurseisangel-www

The published files for **https://nurseisangel.com** (GitHub Pages: branch `main`, folder `/docs`; DNS on Cloudflare,
not proxied). **Don't edit `docs/` by hand.** It's built from the generator
[`ptk-studio/audience-pages`](https://github.com/ptk-studio/audience-pages) (site `nurseisangel`):

```
cd audience-pages && python3 publish.py nurseisangel --to ../nurseisangel-www/docs
```

then open a PR here with the changed `docs/`. Content, products, privacy text, analytics and hosting settings all live in
`audience-pages/sites/nurseisangel/site.toml` and its templates.

- Counter: `https://api.88eggs.com/funnel/v1/nurseisangel` (no cookies; 365 days).
- Feedback: 88eggs project Web:NurseIsAngel.
- Google Analytics 4: Firebase project `ptk-studio-nurseisangel`, consent mode v2 (analytics denied in the EEA/UK/CH,
  ads always denied), ptk-studio#199.
