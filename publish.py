#!/usr/bin/env python3
"""Build nurseisangel.com for GitHub Pages: python3 publish.py

Runs build.py (the audience-pages generator), then turns its Cloudflare-only files into
things GitHub Pages can serve, in docs/ (Pages source: main, /docs):
- _redirects (/go/<id> -> store link, ONLY ids in site.toml) -> docs/go/<id>/index.html
- _headers -> a CSP and referrer <meta> in every page (frame-ancestors can't be set in a
  <meta>; add it as a Cloudflare response-header rule if needed)
Standard library only.
"""
import html, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLUG, DOMAIN = "nurseisangel", "nurseisangel.com"
CSP = ("default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; "
       "script-src 'self' 'unsafe-inline' https://api.88eggs.com; connect-src https://api.88eggs.com; "
       "base-uri 'self'; form-action 'self'")
META = (f'<meta http-equiv="Content-Security-Policy" content="{CSP}">\n'
        '<meta name="referrer" content="strict-origin-when-cross-origin">\n')
GO = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
{meta}<meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={url}">
<title>Opening the store…</title></head>
<body><p>Opening the store… <a href="{url}" rel="nofollow">continue</a></p>
<script>location.replace({js});</script></body></html>
"""

def main() -> None:
    subprocess.run([sys.executable, "-I", str(ROOT / "build.py"), SLUG], check=True, cwd=ROOT)
    dist, docs = ROOT / "dist" / SLUG, ROOT / "docs"
    shutil.rmtree(docs, ignore_errors=True)
    shutil.copytree(dist, docs, ignore=shutil.ignore_patterns("_redirects", "_headers"))
    for page in docs.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        if "Content-Security-Policy" not in text:
            text = text.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + META, 1)
        page.write_text(text, encoding="utf-8")
    count = 0
    for line in (dist / "_redirects").read_text(encoding="utf-8").splitlines():
        m = re.fullmatch(r"/go/([a-z0-9-]+) (https://\S+) 302", line.strip())
        if not m:
            continue
        pid, url = m.groups()
        out = docs / "go" / pid / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        js = '"' + url.replace("\\", "\\\\").replace('"', '\\"').replace("<", "\\u003c") + '"'
        out.write_text(GO.format(meta=META, url=html.escape(url, quote=True), js=js), encoding="utf-8")
        count += 1
    (docs / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    print(f"docs/ ready for {DOMAIN}: {sum(1 for _ in docs.rglob('*.html'))} pages, {count} /go links")

if __name__ == "__main__":
    main()
