"""Tests for the 2026-08-09 blog-pipeline upgrade.

Scope: the packet defect fixes, the persona wiring, the image path, and the
guards that keep third-party marketing text out of this repo. The bash-native
half of the suite (UTM distinctness, disclaimer fail-closed, empty-field
degradation, the media block) lives in scripts/blog/test-pipeline-invariants.sh
because those exercise shell functions and a node renderer directly.

Everything here runs OFFLINE and spends nothing. The one test that makes a real
API call is gated behind BLOG_IMAGE_LIVE_SMOKE=1 and skips by default, so CI
never reaches a vendor and never bills.

Run:  pytest tests/test_blog_pipeline.py -q
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts" / "blog"
SKILL_SCRIPTS = REPO / ".claude" / "skills" / "blog-backfill" / "scripts"
SKILL_REFS = REPO / ".claude" / "skills" / "blog-backfill" / "references"
GLOBAL_SKILL = Path.home() / ".claude" / "skills" / "blog-backfill"
PERSONA = Path.home() / "000-projects" / "intent-os" / "persona"
LINTER = SKILL_SCRIPTS / "lint-post-voice.py"
PACKET = SCRIPTS / "blog-posting-packet.sh"


def load_module(path: Path, name: str):
    """Import a hyphenated script as a module (they are not importable by name)."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


img = load_module(SCRIPTS / "make-post-image.py", "make_post_image")
card = load_module(SCRIPTS / "make-social-card.py", "make_social_card")


# ---------------------------------------------------------------------------
# 2. Social-copy lint: known-bad copy through the new --stdin mode must FAIL.
#
# Before this, the article could not ship with an em dash but the LinkedIn post
# quoting it could, and did. The packet was the one unlinted surface.
# ---------------------------------------------------------------------------


def lint_stdin(text: str, label: str = "test") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(LINTER), "--stdin", "--label", label],
        input=text, capture_output=True, text=True, check=False,
    )


@pytest.mark.parametrize(
    ("copy", "why"),
    [
        ("We shipped the gate — it caught the bug.", "em dash"),
        ("Runtime dropped 40s – 6s on the runner.", "en dash"),
        ("We shipped the gate &mdash; it caught the bug.", "html em dash entity"),
        ("Excited to share what we built this week.", "slop opener"),
        ("Let's dive into how the gate works.", "slop phrase"),
        ("This is a comprehensive look at the pipeline.", "slop phrase"),
        ("A game-changer for how we ship.", "slop phrase"),
    ],
)
def test_bad_social_copy_fails_the_lint(copy, why):
    result = lint_stdin(copy, "li_company")
    assert result.returncode == 1, f"{why!r} was not caught: {copy!r}"
    assert "li_company" in result.stderr


@pytest.mark.parametrize(
    "copy",
    [
        "We shipped the gate. It caught the bug on the first run.",
        "The email said OK. Nothing went out. That took a morning to prove.",
        "Intent Solutions built the check that catches it, and stated what it costs.",
    ],
)
def test_good_social_copy_passes_the_lint(copy):
    result = lint_stdin(copy, "x_post")
    assert result.returncode == 0, result.stderr


def test_stdin_mode_rejects_stray_path_arguments():
    result = subprocess.run(
        [sys.executable, str(LINTER), "--stdin", "somefile.md"],
        input="clean text", capture_output=True, text=True, check=False,
    )
    assert result.returncode == 2


def test_path_mode_still_works():
    """The stdin mode must not have broken the original file-path gate, which is
    what blog-land.sh calls to decide whether to publish or quarantine."""
    result = subprocess.run(
        [sys.executable, str(LINTER), str(SKILL_REFS / "seo-grounding.md")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


# ---------------------------------------------------------------------------
# 5. Facet selection: the syndication surfaces carry their marketing facets, and
# the article carries the work-journal register instead. Register drift (a
# marketing tone leaking into the work journal) is the biggest risk in this
# change, so it gets an explicit guard.
# ---------------------------------------------------------------------------

PACKET_TEXT = PACKET.read_text(encoding="utf-8")


def test_packet_maps_each_surface_to_its_named_facet():
    for surface, facet in [("x_post", "Raw"), ("li_personal", "Personal"),
                           ("li_company", "House")]:
        assert f"{surface}" in PACKET_TEXT
        assert f"the {facet} facet" in PACKET_TEXT, (
            f"{surface} is not mapped to the {facet} facet in the voice prompt")


def test_packet_inlines_the_persona_authority_rather_than_naming_it():
    """voice-system-prompt.md and voices.md were cited as paths and never read.
    Reading them is the whole point of the wiring."""
    assert "VOICE_MASTER=" in PACKET_TEXT and "VOICE_FACETS=" in PACKET_TEXT
    assert 'master=$(cat "$VOICE_MASTER")' in PACKET_TEXT
    assert 'facets=$(cat "$VOICE_FACETS")' in PACKET_TEXT
    assert "CANONICAL MASTER VOICE" in PACKET_TEXT


def test_packet_declares_the_syndication_register_and_disclaims_the_article():
    flat = " ".join(PACKET_TEXT.split())
    assert "SYNDICATION copy" in flat
    assert "NOT the register the article itself is written in" in flat
    assert "The article is a work journal" in flat


def test_packet_injects_the_denylist_instead_of_restating_a_subset():
    """The prompt used to restate a hand-picked 7-item list that had drifted from
    the 26-entry deny-list the linter enforces: told one rule, graded on another."""
    assert "VOICE_DENYLIST" in PACKET_TEXT
    assert ".slop_phrases[].label" in PACKET_TEXT
    assert '"in today\'s fast-paced"' not in PACKET_TEXT, "inline subset is back"


def test_packet_pins_a_model_and_drops_the_permission_bypass():
    assert "VOICE_MODEL=" in PACKET_TEXT
    assert '--model "$VOICE_MODEL"' in PACKET_TEXT
    # The flag may still be NAMED in a comment explaining why it was removed.
    # What must not exist is a line that actually passes it.
    live = [ln for ln in PACKET_TEXT.splitlines()
            if "--dangerously-skip-permissions" in ln and not ln.strip().startswith("#")]
    assert not live, f"permission bypass is still live on: {live}"


@pytest.mark.skipif(not (GLOBAL_SKILL / "references" / "write-post.md").exists(),
                    reason="global blog-backfill skill not provisioned on this box")
def test_article_brief_is_work_journal_not_a_marketing_facet():
    text = (GLOBAL_SKILL / "references" / "write-post.md").read_text(encoding="utf-8")
    assert "work journal" in text.lower()
    assert "NO call to action" in text or "No calls to action" in text
    # The article uses the two work-journal facets and must disclaim the rest.
    assert "Field" in text and "Architect" in text
    assert "syndication facets and must not be used for article prose" in text.lower()


@pytest.mark.skipif(not (GLOBAL_SKILL / "references" / "writer-briefing-template.md").exists(),
                    reason="global blog-backfill skill not provisioned on this box")
def test_writer_brief_states_bands_and_forbidden_deliverables():
    text = (GLOBAL_SKILL / "references" / "writer-briefing-template.md").read_text(
        encoding="utf-8")
    for band in ["80 to 140 lines", "150 to 250 lines", "300 to 500 lines"]:
        assert band in text, f"missing tier band: {band}"
    for banned in ["Email subject lines", "Social media promotion posts",
                   "content distribution plan", "call to action"]:
        assert banned.lower() in text.lower(), f"brief does not forbid: {banned}"
    assert "10-100+ pages" in text, "brief does not counter the docs-architect page target"


@pytest.mark.skipif(not PERSONA.exists(), reason="intent-os persona not on this box")
def test_persona_authority_still_defines_the_facets_the_packet_selects():
    """The packet selects facets by name. If intent-os renames one, the packet is
    quietly asking for a voice that no longer exists."""
    facets = (PERSONA / "voices.md").read_text(encoding="utf-8")
    for facet in ["Raw", "Personal", "House", "Field", "Architect"]:
        assert f"### {facet}" in facets, f"facet {facet} is gone from voices.md"


# ---------------------------------------------------------------------------
# 6. Seeded model pick: stable per slug, spread across the catalogue, and an
# unknown provider is rejected rather than silently defaulted.
# ---------------------------------------------------------------------------


def test_model_pick_is_stable_for_a_given_slug():
    models = img.MiniMaxProvider.models
    for slug in ["the-day-the-green-checks-were-lying", "a", "z" * 80]:
        picks = {img.pick_model(slug, models) for _ in range(20)}
        assert len(picks) == 1, f"{slug} picked more than one model: {picks}"


def test_model_pick_is_distributed_across_a_corpus():
    """A seeded pick that clumps on one model is not variation, it is a constant
    with extra steps. Checked against a synthetic multi-model catalogue so the
    property is verified even while the real vetted catalogue holds one model."""
    models = ["m-a", "m-b", "m-c"]
    slugs = [p.stem for p in (REPO / "content" / "posts").glob("*.md")]
    assert len(slugs) > 50, "corpus too small to judge distribution"
    counts = {m: 0 for m in models}
    for slug in slugs:
        counts[img.pick_model(slug, models)] += 1
    for model, n in counts.items():
        assert n > len(slugs) * 0.20, f"{model} got only {n}/{len(slugs)} of the corpus"


def test_vetted_catalogue_excludes_the_off_brand_model():
    """image-01-live authenticates and generates, but it renders stylized game
    and anime art and ignores the charcoal-and-ember photographic frame. Seeding
    across it is a coin flip on whether a post gets an off-brand image, so it is
    reachable only through an explicit --model override."""
    provider = img.MiniMaxProvider
    assert "image-01" in provider.models
    assert "image-01-live" not in provider.models
    assert "image-01-live" in provider.all_models
    assert set(provider.models) <= set(provider.all_models)


def test_seeded_pick_never_reaches_an_unvetted_model():
    provider = img.MiniMaxProvider
    unvetted = set(provider.all_models) - set(provider.models)
    picks = {img.pick_model(f"slug-{i}", provider.models) for i in range(300)}
    assert not (picks & unvetted), f"seeded pick reached unvetted models: {picks & unvetted}"


def test_model_pick_only_returns_models_the_provider_exposes():
    models = img.MiniMaxProvider.models
    slugs = [f"slug-{i}" for i in range(200)]
    assert {img.pick_model(s, models) for s in slugs} <= set(models)


def test_model_pick_rejects_an_empty_catalogue():
    with pytest.raises(ValueError):
        img.pick_model("any-slug", [])


def test_unknown_provider_is_rejected():
    with pytest.raises(ValueError, match="unknown image provider"):
        img.resolve_provider("replicate")
    with pytest.raises(ValueError, match="unknown image provider"):
        img.resolve_provider("")


def test_minimax_is_the_only_wired_provider():
    """The registry is a seam for later, not a set of live vendors. If a second
    provider appears here it was wired without a decision."""
    assert set(img.PROVIDERS) == {"minimax"}


# ---------------------------------------------------------------------------
# 7. Image-prompt guard: no lettering request, no banned visual cliches.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scene",
    [
        "A control panel with the word STOP painted across it",
        "A workshop sign that reads out of service",
        "A machine with a label on its housing",
        "A gauge face showing numerals in the red band",
        "A banner reading closed hangs over the line",
        "A steel plate with an inscription stamped into it",
        "A crate marked with a logo in the corner",
    ],
)
def test_prompt_guard_rejects_lettering_requests(scene):
    assert img.scene_violations(scene), f"lettering slipped through: {scene!r}"
    with pytest.raises(ValueError, match="unsafe scene clause"):
        img.build_prompt(scene)


@pytest.mark.parametrize(
    "scene",
    [
        "A glowing brain floating above a server rack",
        "A circuit board lit from beneath",
        "A robot hand reaching for a lever",
        "A neon grid stretching to the horizon",
        "Binary code streaming down a dark wall",
        "A hologram of a turbine spinning slowly",
        "A network of glowing nodes over a factory floor",
    ],
)
def test_prompt_guard_rejects_ai_slop_visuals(scene):
    assert img.scene_violations(scene), f"cliche slipped through: {scene!r}"
    with pytest.raises(ValueError, match="unsafe scene clause"):
        img.build_prompt(scene)


def test_clean_scene_passes_and_produces_a_constrained_prompt():
    scene = ("A bank of analogue pressure gauges on a scuffed enamel housing, one "
             "needle pinned hard over into the ember-marked band")
    assert img.scene_violations(scene) == []
    prompt = img.build_prompt(scene)
    assert scene.rstrip(".") in prompt
    # Every prompt carries the fixed constraints, whatever the scene was.
    assert "No text, lettering" in prompt
    assert "Avoid AI-stock cliches" in prompt
    assert "Charcoal and ember palette" in prompt


def test_every_deterministic_scene_is_safe_by_construction():
    """The deterministic metaphors are the fallback when the scene step fails or
    is rejected. If one of them trips the guard there is no floor left."""
    for slug in ["a", "b", "some-post-slug", "z" * 40] + [f"s{i}" for i in range(40)]:
        scene = img.deterministic_scene({"slug": slug})
        assert img.scene_violations(scene) == [], f"unsafe fallback scene: {scene!r}"
        img.build_prompt(scene)


def test_deterministic_scene_is_stable_per_slug():
    post = {"slug": "the-day-the-green-checks-were-lying"}
    assert len({img.deterministic_scene(post) for _ in range(10)}) == 1


def test_assembled_prompt_stays_under_the_vendor_ceiling():
    """MiniMax hard-rejects over 1500 characters with error 2013. A long scene
    gets trimmed; it must never produce a prompt the vendor refuses."""
    long_scene = ("A vast machine hall filled with identical stopped conveyors "
                  "and cold indicator lamps, " * 40)
    prompt = img.build_prompt(long_scene)
    assert len(prompt) <= img.MAX_PROMPT
    assert len(prompt) < 1500


def test_scene_cleaner_strips_model_preamble():
    """The scene step leaks task narration despite being told not to, and every
    leaked character comes out of the scene's budget."""
    leaked = ("Reading through the drift-watch failure to ground the scene in the "
              "actual mechanism. A wide inspection gantry rolls past a line of "
              "stamped parts, its approval lamp lit and steady.")
    cleaned = img.clean_scene(leaked)
    assert "Reading through" not in cleaned
    assert "inspection gantry" in cleaned


def test_scene_cleaner_returns_empty_for_an_all_meta_reply():
    """An entirely meta reply must fall back to the deterministic scene rather
    than being sent to the image model as if it were a picture."""
    assert img.clean_scene("Here is the scene you asked for based on the post.") == ""


# ---------------------------------------------------------------------------
# 8. Card renderer: golden sizes, and a long title still fits.
# ---------------------------------------------------------------------------


def test_card_renders_the_two_golden_sizes(tmp_path):
    out = subprocess.run(
        [sys.executable, str(SCRIPTS / "make-social-card.py"),
         "--title", "The Day the Green Checks Were Lying",
         "--quote", "The email said OK. Nothing went out.",
         "--slug", "golden", "--outdir", str(tmp_path), "--json"],
        capture_output=True, text=True, check=False,
    )
    assert out.returncode == 0, out.stderr
    written = json.loads(out.stdout.strip().splitlines()[-1])

    pil = pytest.importorskip("PIL.Image")
    assert pil.open(written["og"]).size == (1200, 630)
    assert pil.open(written["square"]).size == (1080, 1080)


def test_long_title_shrinks_rather_than_overflowing():
    """A fixed point size runs a long title off the canvas, and a card that clips
    its own title is worse than no card."""
    pil = pytest.importorskip("PIL.Image")
    short = "Short One"
    long_title = ("The Day the Green Checks Were Lying and Every Downstream "
                  "Consumer Believed Them for Eleven Straight Days")

    from PIL import ImageDraw
    probe = ImageDraw.Draw(pil.new("RGB", (1200, 630)))
    content_w = 1200 - 2 * 70

    short_font, short_lines = card.fit_title(
        probe, short, content_w, 3, start=62, floor=30)
    long_font, long_lines = card.fit_title(
        probe, long_title, content_w, 3, start=62, floor=30)

    assert long_font.size <= short_font.size, "long title did not shrink"
    assert len(long_lines) <= 3, "long title exceeded its band"
    for line in long_lines:
        assert probe.textlength(line, font=long_font) <= content_w, (
            f"line overflows the canvas: {line!r}")


def test_card_renders_without_a_pull_quote():
    pil = pytest.importorskip("PIL.Image")
    assert card.render(1200, 630, "No Quote Here", "").size == (1200, 630)
    assert isinstance(card.render(1080, 1080, "Square", ""), pil.Image)


def test_card_reads_title_and_quote_from_a_real_post():
    posts = sorted((REPO / "content" / "posts").glob("*.md"))
    assert posts, "no posts to read"
    title, _quote = card.read_post(str(posts[0]))
    assert title and title != posts[0].stem.replace("-", " ")


# ---------------------------------------------------------------------------
# 9. Every file this change authored passes the voice lint.
#
# Writing the dash ban into a doc that contains an em dash is the kind of thing
# that survives review and then gets quoted back as an example.
# ---------------------------------------------------------------------------

# Files this change authored outright. Deliberately NOT listed:
#   lint-post-voice.py  - the enforcement mechanism itself, whose docstring must
#                         spell out the HTML dash entities in order to ban them
#   this test file      - carries known-bad copy as fixtures on purpose
# Both would fail their own gate for the same reason a spell-checker's word list
# fails a spell-check.
AUTHORED_FILES = [
    SKILL_REFS / "seo-grounding.md",
    SCRIPTS / "make-post-image.py",
    SCRIPTS / "make-social-card.py",
    SCRIPTS / "test-pipeline-invariants.sh",
]


@pytest.mark.parametrize("path", AUTHORED_FILES, ids=lambda p: p.name)
def test_authored_files_pass_the_voice_lint(path):
    result = subprocess.run(
        [sys.executable, str(LINTER), str(path)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr


def test_the_grounding_doc_actually_grounds_the_generic_agents():
    """A grounding file that does not name the specific wrong advice is decoration."""
    text = (SKILL_REFS / "seo-grounding.md").read_text(encoding="utf-8")
    for correction in ["WordPress", "special characters for visibility",
                       "2023 to 2025", "Hugo"]:
        assert correction in text, f"grounding does not address: {correction}"
    assert "E-E-A-T" in text
    # The Trust dimension is the one an SEO pass will optimize away.
    assert "never remove a caveat" in text.lower()


# ---------------------------------------------------------------------------
# 10. No-vendoring guard. The Vibe pack is installed and used; its TEXT never
# enters this repo. Its reference files carry 378 em dashes against a hardcoded
# ban, so vendoring them would import the exact thing the linter exists to stop.
# ---------------------------------------------------------------------------

VENDOR_MARKERS = [
    "vibemarketing.dev",
    "Vibe Marketing Skills",
    "TVM_INSTALL_HOME",
    "skills-v2",
]


def test_no_vibe_derived_text_in_the_repo():
    tracked = subprocess.run(
        ["git", "-C", str(REPO), "ls-files"],
        capture_output=True, text=True, check=True).stdout.split()
    hits = []
    for marker in VENDOR_MARKERS:
        found = subprocess.run(
            ["git", "-C", str(REPO), "grep", "-l", "-F", "--", marker],
            capture_output=True, text=True, check=False)
        for path in found.stdout.split():
            # This test file names the markers in order to forbid them.
            if path == os.path.relpath(__file__, REPO):
                continue
            hits.append(f"{marker} -> {path}")
    assert not hits, "Vibe-derived text found in tracked files:\n" + "\n".join(hits)
    assert tracked, "git ls-files returned nothing; the guard would pass vacuously"


def test_the_vibe_pack_is_installed_globally_not_vendored():
    """Install and use: yes. Vendor and imitate: no. If the pack is not installed
    the skills are unavailable; if it IS in the repo the guard above should have
    already failed."""
    installed = Path.home() / ".claude" / "skills"
    if not (installed / "brand-voice").exists():
        pytest.skip("Vibe pack not installed on this box")
    assert not (REPO / "skills-v2").exists()
    assert not (REPO / ".claude" / "skills" / "brand-voice").exists()


# ---------------------------------------------------------------------------
# 11. Live image smoke. One real MiniMax call, asserting a decodable image.
# SKIPPED BY DEFAULT so CI stays offline and spends nothing.
#
# Run deliberately:  BLOG_IMAGE_LIVE_SMOKE=1 pytest tests/test_blog_pipeline.py -k live
# ---------------------------------------------------------------------------


@pytest.mark.skipif(os.environ.get("BLOG_IMAGE_LIVE_SMOKE") != "1",
                    reason="live vendor call; set BLOG_IMAGE_LIVE_SMOKE=1 to run")
def test_live_minimax_call_returns_a_decodable_image(tmp_path):
    pil = pytest.importorskip("PIL.Image")
    provider = img.resolve_provider("minimax")
    prompt = img.build_prompt(img.deterministic_scene({"slug": "live-smoke"}))
    model = img.pick_model("live-smoke", provider.models)

    data = provider.generate(prompt, model)
    assert data, "provider returned no bytes"

    out = tmp_path / "live.png"
    out.write_bytes(data)
    image = pil.open(out)
    image.verify()
    assert min(pil.open(out).size) >= 512, "image is implausibly small"
