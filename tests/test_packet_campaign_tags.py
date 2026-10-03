"""Every distributed packet link carries campaign tags; every canonical stays clean.

Runs the packet's REAL utm() and build_payload() bodies (sliced out of the script, the
same way test_blog_consumer_source.py does, because sourcing the script runs its main
body) with offline stand-ins for the model, the committed-source resolver and the
mailer, then renders the HTML with the real renderer and parses every href and every
copy box the poster would paste from. Nothing is sent and no real ledger is read.
"""

import json
import os
import shlex
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
PACKET = SCRIPTS / "blog-posting-packet.sh"
RENDERER = SCRIPTS / "blog-packet-html.cjs"
SLUG = "fixture-campaign-post"
CANONICAL = f"https://startaitools.com/posts/{SLUG}/"
TAGS = ("utm_source", "utm_medium", "utm_campaign", "utm_content")

# surface -> (utm_source, utm_medium). This table IS the documented tagging contract.
EXPECTED = {
    "x": ("x", "social"),
    "li_personal": ("linkedin", "social"),
    "li_company": ("linkedin", "social"),
    "x_article": ("x", "syndication"),
    "substack": ("substack", "syndication"),
    "medium": ("medium", "syndication"),
    "buymeacoffee": ("buymeacoffee", "syndication"),
}
BARE_FIELDS = ("substack_canonical", "medium_canonical", "medium_import")

needs_tools = pytest.mark.skipif(
    not (shutil.which("node") and shutil.which("jq")), reason="node and jq are required"
)


def function(name: str) -> str:
    text = PACKET.read_text()
    start = text.index(f"{name}() {{")
    return text[start : text.index("\n}\n", start) + 3]


def build_payload_body() -> str:
    text = PACKET.read_text()
    return text[text.index("build_payload() {") : text.index("\nmark_sent() {")]


def call_utm(*args: str) -> str:
    script = function("utm") + "\nutm " + " ".join(shlex.quote(a) for a in args)
    return subprocess.run(
        ["bash", "-c", script], capture_output=True, text=True, check=True
    ).stdout


def payload(tmp_path: Path, tier: int = 2, disclaimers: dict | None = None) -> dict:
    """The packet payload for one fixture post, built by the script's own code."""
    resolver = tmp_path / "resolver.py"
    resolver.write_text(
        "import sys\n"
        "out = sys.argv[sys.argv.index('--output') + 1]\n"
        "open(out, 'w').write(\"+++\\ntitle = 'Fixture'\\n+++\\n"
        "A recorded observation about a governed partner.\\n\")\n"
    )
    library = tmp_path / "disclaimers.json"
    library.write_text(json.dumps(disclaimers or {"default_footer": "f", "entities": {}}))
    entry = {
        "slug": SLUG,
        "title": "Fixture",
        "canonical_url": CANONICAL,
        "tier": tier,
        "github_links": [],
    }
    prelude = f"""
set -uo pipefail
DRY_RUN=1
BLOG_DIR={shlex.quote(str(tmp_path))}
LOG={shlex.quote(str(tmp_path / "log"))}
VOICE_FAIL_FILE={shlex.quote(str(tmp_path / "voice-fail"))}
CONSUMER_SOURCE_HELPER={shlex.quote(str(resolver))}
DISCLAIMER_LIB={shlex.quote(str(library))}
log() {{ printf '%s\\n' "$*" >&2; }}
post_body() {{ awk 'f{{print}} /^\\+\\+\\+|^---/{{c++}} c==2 && !f {{f=1}}' "$1"; }}
lint_voice_fields() {{ return 0; }}
generate_voice() {{
  printf '%s' '{{"x_post":"x copy","li_personal":"personal","li_company":"house",
    "substack_subtitle":"sub","x_article_title":"T","x_article_subtitle":"S",
    "bmc_note":"note"}}'
}}
{function("utm")}
{function("select_disclaimers")}
{build_payload_body()}
build_payload "$FIXTURE_ENTRY"
"""
    result = subprocess.run(
        ["bash", "-c", prelude],
        env={**os.environ, "FIXTURE_ENTRY": json.dumps(entry)},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def render(data: dict) -> str:
    result = subprocess.run(
        ["node", str(RENDERER), "--fragment"],
        input=json.dumps(data),
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )
    return result.stdout


class Collector(HTMLParser):
    """Decoded hrefs and decoded <pre> text: exactly what a reader clicks or copies."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.boxes, self._in_pre = [], [], False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(v for k, v in attrs if k == "href")
        self._in_pre = tag == "pre" or self._in_pre
        if tag == "pre":
            self.boxes.append("")

    def handle_endtag(self, tag):
        if tag == "pre":
            self._in_pre = False

    def handle_data(self, data):
        if self._in_pre:
            self.boxes[-1] += data


def blog_urls(html: str) -> list[str]:
    collected = Collector()
    collected.feed(html)
    found = [h for h in collected.hrefs if h.startswith("https://startaitools.com/posts/")]
    for box in collected.boxes:
        for token in box.split():
            if token.startswith("https://startaitools.com/posts/"):
                found.append(token)
    return found


def tags(url: str) -> dict:
    query = urlsplit(url).query
    parsed = parse_qs(query, keep_blank_values=True, strict_parsing=bool(query))
    assert all(len(v) == 1 for v in parsed.values()), f"repeated key in {url}"
    return {k: v[0] for k, v in parsed.items()}


@needs_tools
def test_every_surface_link_carries_four_normalized_tags(tmp_path):
    links = payload(tmp_path)["links"]
    for surface, (source, medium) in EXPECTED.items():
        assert tags(links[surface]) == {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": SLUG,
            "utm_content": surface,
        }, surface
        assert links[surface].startswith(CANONICAL + "?")


@needs_tools
def test_platform_canonical_fields_stay_bare(tmp_path):
    data = payload(tmp_path)
    assert data["canonical_url"] == CANONICAL
    for field in BARE_FIELDS:
        assert data["links"][field] == CANONICAL, field


@needs_tools
def test_rendered_packet_tags_every_link_a_reader_can_click_or_copy(tmp_path):
    data = payload(tmp_path)
    html = render(data)
    assert "&amp;amp;" not in html, "double-escaped ampersand in the packet"
    urls = blog_urls(html)
    tagged = [u for u in urls if urlsplit(u).query]
    bare = [u for u in urls if not urlsplit(u).query]
    # Every tagged link decodes to exactly the four tags with normalized values.
    for url in tagged:
        assert "amp;" not in url, f"HTML entity leaked into a link: {url}"
        values = tags(url)
        assert set(values) == set(TAGS), url
        assert values["utm_campaign"] == SLUG
        assert EXPECTED[values["utm_content"]] == (values["utm_source"], values["utm_medium"])
    # All seven tier-2 surfaces reach the poster with their own tagged link.
    assert {tags(u)["utm_content"] for u in tagged} == set(EXPECTED)
    # The only untagged blog links are the canonical itself (callout, canonical boxes,
    # Medium import, "open the live article" steps).
    assert bare and set(bare) == {CANONICAL}


@needs_tools
def test_substack_and_medium_get_a_tagged_body_link_beside_a_bare_canonical(tmp_path):
    html = render(payload(tmp_path))
    substack = html[html.index("<h2>Substack") : html.index("<h2>Medium")]
    medium = html[html.index("<h2>Medium") : html.index("<h2>X (long-form article)")]
    for section, name in ((substack, "substack"), (medium, "medium")):
        urls = blog_urls(section)
        assert CANONICAL in urls, f"{name}: canonical box missing"
        assert any(tags(u).get("utm_content") == name for u in urls if "?" in u), name
    collected = Collector()
    collected.feed(medium)
    assert "https://medium.com/p/import" in collected.hrefs
    assert CANONICAL in collected.hrefs  # the import URL is the bare canonical


@needs_tools
def test_tier_one_tags_its_four_surfaces_and_omits_the_reposts(tmp_path):
    data = payload(tmp_path, tier=1)
    assert set(data["destinations"]) == {"x", "li_personal", "li_company", "buymeacoffee"}
    found = {tags(u)["utm_content"] for u in blog_urls(render(data)) if "?" in u}
    assert found == {"x", "li_personal", "li_company", "buymeacoffee"}


@needs_tools
def test_a_held_packet_is_flagged_and_still_tagged(tmp_path):
    held = {"default_footer": "f", "entities": {"acme": {"match": ["governed partner"],
                                                         "approved": []}}}
    data = payload(tmp_path, disclaimers=held)
    assert data["hold"] is True
    assert tags(data["links"]["x"])["utm_campaign"] == SLUG


def test_utm_strips_escaped_ampersands_and_hostile_values():
    url = call_utm("https://startaitools.com/p/?a=1&amp;b=2", "linked in&amp;", "li_personal",
                   "Some Slug/../<x>", "social")
    assert "amp;" not in url
    assert tags(url) == {
        "a": "1",
        "b": "2",
        "utm_source": "linkedin",
        "utm_medium": "social",
        "utm_campaign": "someslugx",
        "utm_content": "li_personal",
    }


def test_utm_carries_no_personal_data():
    """The tag vocabulary is closed: platform tokens, a medium, a surface, the slug."""
    text = PACKET.read_text()
    body = text[text.index("local link_x link_x_article") : text.index("# GitHub \"Code:\" line.")]
    for line in body.splitlines():
        if "$(utm " in line:
            assert "@" not in line and "EMAIL" not in line and "jeremy" not in line.lower()


@pytest.mark.skipif(not shutil.which("curl"), reason="curl unavailable")
def test_live_tagged_link_survives_the_trailing_slash_redirect():
    """Read-only check against the real site: a 308 to the slash form keeps the query."""
    live = "rehearse-before-production-catches-what-tests-cant"
    query = call_utm(f"https://startaitools.com/posts/{live}", "linkedin", "li_personal", live)
    try:
        result = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-L", "--max-time", "20",
             "-w", "%{http_code} %{num_redirects} %{url_effective}", query],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        pytest.skip("network timeout")
    if result.returncode != 0:
        pytest.skip(f"network unavailable: {result.stderr.strip()[:80]}")
    code, redirects, effective = result.stdout.split(" ", 2)
    assert code == "200", result.stdout
    assert int(redirects) >= 1, "expected the slashless URL to redirect"
    assert urlsplit(effective).path.endswith(f"/{live}/")
    assert tags(effective)["utm_campaign"] == live
    assert tags(effective)["utm_content"] == "li_personal"
