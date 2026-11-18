"""Tests for build.py (ptk-studio#191). Run: python3 -m unittest discover -s tests"""
import copy, re, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build  # noqa: E402

BASE = {"slug": "t", "domain": "t.example", "title": "T", "audience": "a", "market": "D", "accent": "#123456",
        "content_md": "# Hi", "products": []}


def site(*products):
    s = copy.deepcopy(BASE)
    s["products"] = list(products)
    return s


def prod(pid="tee-a", link="https://www.amazon.com/dp/B000", status="live"):
    return {"id": pid, "name": "A", "type": "T-shirt", "price": "$1", "store": "Amazon", "link": link, "status": status}


class NoOpenRedirect(unittest.TestCase):
    def test_only_listed_live_ids_redirect(self):
        s = site(prod("tee-a"), prod("poster-b", "https://shop.88eggs.com/p/1"), prod("tee-c", status="coming"))
        lines = [l for l in build.redirects(s, preview=False).splitlines() if not l.startswith("#")]
        self.assertEqual(lines, ["/go/tee-a https://www.amazon.com/dp/B000?src=t 302",
                                 "/go/poster-b https://shop.88eggs.com/p/1?src=t 302"])
        for l in lines:  # no wildcard or splat rule that could forward an arbitrary target
            self.assertNotIn("*", l)
            self.assertNotIn(":splat", l)

    def test_links_must_be_https_on_allowed_hosts(self):
        for bad in ["http://www.amazon.com/dp/1", "https://amazon.com.evil.example/x", "https://evil.example/",
                    "javascript:alert(1)", "//evil.example", "https://www.amazon.com@evil.example/"]:
            with self.assertRaises(build.SiteError, msg=bad):
                build.validate(site(prod(link=bad)), preview=False)

    def test_bad_or_duplicate_ids_refused(self):
        with self.assertRaises(build.SiteError):
            build.validate(site(prod("../x")), preview=False)
        with self.assertRaises(build.SiteError):
            build.validate(site(prod("Tee A")), preview=False)
        with self.assertRaises(build.SiteError):
            build.validate(site(prod("a"), prod("a")), preview=False)

    def test_coming_products_build_in_production_without_a_link(self):
        coming = {"id": "tee-x", "name": "X", "type": "T-shirt", "price": "$1", "store": "Amazon", "status": "coming"}
        build.validate(site(coming), preview=False)
        self.assertEqual(build.redirects(site(coming), preview=False).count("/go/"), 0)
        with self.assertRaises(build.SiteError):
            build.validate(site({**coming, "status": "live"}), preview=False)  # live needs a link
        with self.assertRaises(build.SiteError):
            build.validate(site({**coming, "status": "soon"}), preview=False)

    def test_link_check_is_a_full_match(self):
        for bad in ["https://www.amazon.com/dp/1 https://evil.example", "https://www.amazon.com/dp/1\n/go/x https://evil"]:
            with self.assertRaises(build.SiteError, msg=bad):
                build.validate(site(prod(link=bad)), preview=False)

    def test_placeholders_only_in_preview(self):
        with self.assertRaises(build.SiteError):
            build.validate(site(prod(link="#")), preview=False)
        build.validate(site(prod(link="#")), preview=True)
        self.assertEqual(build.redirects(site(prod(link="#")), preview=True).count("/go/"), 0)


class BuiltSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = build.build("nurseisangel", preview=False)  # the real production build

    def read(self, name):
        return (self.out / name).read_text(encoding="utf-8")

    def test_every_template_filled(self):
        for f in ["index.html", "privacy/index.html", "404.html"]:
            self.assertIsNone(re.search(r"\{\{\w+\}\}", self.read(f)), f)

    def test_privacy_page_states_what_is_kept(self):
        p = self.read("privacy/index.html")
        for phrase in ["It doesn't store your IP address, a cookie, your browser or device details",
                       "a keyed hash that changes every day) for 10 minutes", "365 days",
                       "test visits we make ourselves are marked", "doesn't set cookies or use browser storage",
                       "is run by PTK Studio", "hello@ptk-studio.com",
                       "GitHub processes your IP address to deliver the pages",
                       "run behind Cloudflare, which processes your IP address",
                       "The link may carry a tag naming this site",
                       "sends you straight on to the store",
                       # the Owner-approved Feedback paragraph, word for word (incl. the IP sentence)
                       "We also store the IP address your feedback was sent from, to prevent abuse; it is deleted "
                       "with your feedback after one year.",
                       "If you send us feedback in Nurse Is Angel (through the feedback button, form or app screen)"]:
            self.assertIn(phrase, p)

    def test_beacon_sends_only_view_and_click_fields(self):
        i = self.read("index.html")
        self.assertIn("https://api.88eggs.com/funnel/v1/nurseisangel", i)
        self.assertNotIn("document.cookie", i)
        self.assertNotIn("localStorage", i)
        self.assertNotIn("referrer", i)

    def test_beacon_on_every_page_with_a_known_page_path(self):
        for f, page in [("index.html", "/"), ("privacy/index.html", "/privacy/"), ("404.html", "/404")]:
            t = self.read(f)
            self.assertIn(f'data-page="{page}"', t, f)
            self.assertIn("/funnel/v1/nurseisangel", t, f)

    def test_product_images_are_built_copies(self):
        self.assertTrue((self.out / "img" / "planner-2027-nurse-shift.jpg").is_file())
        self.assertIn('src="/img/tee-twelve-hours-of-heart.jpg"', self.read("index.html"))
        self.assertNotIn("X-Amz-Signature", self.read("index.html"))  # no signed asset URLs

    def test_coming_products_have_no_buy_link(self):
        self.assertNotIn('href="/go/', self.read("index.html"))
        self.assertIn("Coming soon", self.read("index.html"))


if __name__ == "__main__":
    unittest.main()
