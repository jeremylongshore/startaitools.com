"""Tests for the startaitools.com site action events (bead bhn.11).

Three layers:
1. Source checks (always run): the templates carry the tracker restriction and
   the static event attributes.
2. Built-HTML checks: parse a real Hugo build and assert the attributes sit on
   the right elements. Uses $SITE_PUBLIC_DIR when set (CI's hugo-build-check
   job passes its build), or builds into a temp dir with SITE_EVENTS_BUILD=1.
3. Classifier checks: execute assets/js/measure.js under node so the outbound
   destination classes are tested as shipped, not re-implemented here.

Run:  pytest tests/test_site_events.py -q
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
MEASURE_JS = REPO / "assets" / "js" / "measure.js"
TRACKER_SRC = "https://analytics.intentsolutions.io/script.js"


class _Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def _elements(path: Path):
    parser = _Collector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.elements


def _with_event(elements, name):
    return [(t, a) for t, a in elements if a.get("data-umami-event") == name]


# ---------------------------------------------------------------- 1. source


def test_tracker_tag_restricts_recording_to_canonical_host():
    header = (REPO / "layouts" / "partials" / "header.html").read_text()
    assert 'data-domains="startaitools.com,www.startaitools.com"' in header


def test_event_attributes_are_in_the_templates():
    sources = {
        "layouts/partials/head.html": 'data-umami-event="work_with_us_click"',
        "layouts/partials/footer.html": 'data-umami-event="subscribe_click"',
        "layouts/partials/contact-cta.html": 'data-umami-event="contact_submit_click"',
        "content/contact.md": 'data-umami-event="contact_submit_click"',
    }
    for rel, needle in sources.items():
        assert needle in (REPO / rel).read_text(), rel


def test_accepted_events_fire_only_on_ok_branches():
    main = (REPO / "assets" / "js" / "main.js").read_text()
    for name in ("subscribe_accepted", "contact_accepted"):
        idx = main.index(f"trackAccepted('{name}'")
        # The nearest preceding branch must be the r.ok one.
        assert main.rfind("if (r.ok) {", 0, idx) > main.rfind("else", 0, idx), name


def test_measure_js_is_bundled_with_main():
    head = (REPO / "layouts" / "partials" / "head.html").read_text()
    assert '(resources.Get "js/measure.js")' in head


def test_netlify_default_host_redirects_to_apex():
    toml = (REPO / "netlify.toml").read_text()
    block = toml[toml.index('from = "https://startaitools.netlify.app/*"') :][:200]
    assert 'to = "https://startaitools.com/:splat"' in block
    assert "status = 301" in block and "force = true" in block


# ---------------------------------------------------------------- 2. built HTML


@pytest.fixture(scope="module")
def public_dir(tmp_path_factory):
    env = os.environ.get("SITE_PUBLIC_DIR")
    if env:
        path = Path(env)
        if not (path / "index.html").is_file():
            pytest.fail(f"SITE_PUBLIC_DIR={env} has no index.html")
        yield path
        return
    # A full build is ~1.4 GB, so building here is opt-in. CI's hugo-build-check
    # job builds once and passes SITE_PUBLIC_DIR.
    hugo = shutil.which("hugo")
    if os.environ.get("SITE_EVENTS_BUILD") != "1" or not hugo:
        pytest.skip("set SITE_PUBLIC_DIR=<built public/> or SITE_EVENTS_BUILD=1 (needs hugo)")
    if not (REPO / "themes" / "archie" / "layouts").is_dir():
        pytest.skip("themes/archie submodule not checked out")
    out = tmp_path_factory.mktemp("site")
    try:
        subprocess.run(
            [hugo, "--buildFuture", "--minify", "--quiet", "-d", str(out)],
            cwd=REPO, check=True, timeout=900,
        )
        yield out
    finally:
        shutil.rmtree(out, ignore_errors=True)


def _a_post(public_dir: Path) -> Path:
    posts = sorted((public_dir / "posts").glob("*/index.html"))
    assert posts, "no built posts"
    return posts[-1]


def test_built_tracker_tag_has_domains(public_dir):
    for page in (public_dir / "index.html", _a_post(public_dir)):
        scripts = [a for t, a in _elements(page) if t == "script" and a.get("src") == TRACKER_SRC]
        assert len(scripts) == 1, page
        assert scripts[0].get("data-domains") == "startaitools.com,www.startaitools.com"
        assert scripts[0].get("data-website-id")


def test_built_header_work_with_us(public_dir):
    els = _with_event(_elements(public_dir / "index.html"), "work_with_us_click")
    assert len(els) == 1
    tag, attrs = els[0]
    assert tag == "a" and attrs["href"].rstrip("/").endswith("/contact")
    assert attrs.get("data-umami-event-location") == "header"


def test_built_subscribe_button(public_dir):
    els = _elements(_a_post(public_dir))
    hits = _with_event(els, "subscribe_click")
    assert len(hits) == 1
    tag, attrs = hits[0]
    assert tag == "button" and attrs.get("type") == "submit"
    assert attrs.get("data-umami-event-form") == "startaitools-footer"
    assert any(t == "form" and a.get("data-signup-form") == "startaitools-footer" for t, a in els)


def test_built_contact_submits(public_dir):
    post_hits = _with_event(_elements(_a_post(public_dir)), "contact_submit_click")
    assert [(t, a.get("type"), a.get("data-umami-event-form")) for t, a in post_hits] == [
        ("button", "submit", "startaitools-post-cta")
    ]
    contact_hits = _with_event(_elements(public_dir / "contact" / "index.html"),
                               "contact_submit_click")
    assert [(t, a.get("data-umami-event-form")) for t, a in contact_hits] == [
        ("button", "startaitools-contact")
    ]


def test_built_bundle_carries_measurement_code(public_dir):
    bundles = list((public_dir / "js").glob("main.bundle.min.*.js"))
    assert len(bundles) == 1
    js = bundles[0].read_text()
    for name in ("outbound_click", "subscribe_accepted", "contact_accepted",
                 "support_widget_click", "email_click"):
        assert name in js, name
    index_scripts = [a.get("src") for t, a in _elements(public_dir / "index.html") if t == "script"]
    assert any(s and s.endswith(bundles[0].name) for s in index_scripts)


# ---------------------------------------------------------------- 3. classifier


@pytest.fixture(scope="module")
def node():
    exe = shutil.which("node")
    if not exe:
        pytest.skip("node not installed")
    return exe


def _js(node, expr: str):
    module = json.dumps(str(MEASURE_JS))
    script = f"const m = require({module}); console.log(JSON.stringify({expr}));"
    out = subprocess.run([node, "-e", script], check=True, capture_output=True, text=True)
    return json.loads(out.stdout)


@pytest.mark.parametrize(
    ("href", "dest"),
    [
        ("https://tonsofskills.com/blog/x/", "tonsofskills"),
        ("https://www.tonsofskills.com/", "tonsofskills"),
        ("https://intentsolutions.io/about/", "intentsolutions"),
        ("https://labs.intentsolutions.io/r/1", "intentsolutions"),
        ("https://demos.intentsolutions.io/", "intentsolutions"),
        ("https://github.com/jeremylongshore/x", "github"),
        ("https://gist.github.com/a/b", "github"),
        ("https://ko-fi.com/jeremylongshore", "support"),
        ("https://buymeacoffee.com/x", "support"),
        ("https://example.org/?q=1", "other"),
        ("https://notintentsolutions.io/", "other"),
    ],
)
def test_outbound_classes(node, href, dest):
    host = href.split("/")[2]
    got = _js(node, f"m.eventForHref({json.dumps(href)}, 'startaitools.com')")
    assert got == {"name": "outbound_click", "data": {"dest": dest, "host": host}}


@pytest.mark.parametrize(
    "href",
    [
        "https://startaitools.com/posts/x/",
        "https://www.startaitools.com/",
        "javascript:void(0)",
        "tel:+15555550100",
        "/relative/path",
    ],
)
def test_internal_and_non_http_links_are_not_tracked(node, href):
    assert _js(node, f"m.eventForHref({json.dumps(href)}, 'startaitools.com')") is None


def test_same_host_preview_link_is_not_outbound(node):
    host = "deploy-preview-9--startaitools.netlify.app"
    assert _js(node, f"m.eventForHref('https://{host}/a/', '{host}')") is None


def test_mailto_is_email_click(node):
    got = _js(node, "m.eventForHref('mailto:jeremy@intentsolutions.io', 'startaitools.com')")
    assert got == {"name": "email_click", "data": {}}
