"""Persona is not evidence: enforced on the article AND the channel-copy path.

Editorial rule (blog-backfill write-post.md / social-bundle.md): persona and voice
guidance are not evidence that the author experienced an event. Hypothetical examples
must be identifiable as hypothetical; factual first-person anecdotes require source
support. One linter enforces it on both surfaces:

* article: blog-land.sh runs `lint-post-voice.py <post>` (path mode, content/ posts);
* channel copy: blog-posting-packet.sh pipes every model-authored field through
  `lint-post-voice.py --stdin --source-post <article>` via lint_copy/lint_voice_fields.

Every negative fixture below is run through the REAL entry point of each path, so
removing the rule (or the packet's --source-post wiring) fails these tests.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LINTER = ROOT / ".claude/skills/blog-backfill/scripts/lint-post-voice.py"
LANDER = ROOT / "scripts/blog/blog-land.sh"
PACKET = ROOT / "scripts/blog/blog-posting-packet.sh"
PACKET_TEXT = PACKET.read_text(encoding="utf-8")

# Each negative fixture is one defect class the rule exists to stop.
FABRICATED_ANECDOTES = [
    # The defect the 2026-10-02 rewrite trial produced, verbatim in shape.
    "Same thing I learned running restaurants. The best closer covers a dozen gaps.",
    "Back when I was driving trucks, a missed log meant a fine at the scale.",
    "The Marines taught me to check the gear before anything moves.",
    "My old GM said the dinner rush exposes every weak station.",
]
BYLINE_CLAIMS = [
    "As an Anthropic partner, we see this pattern every week.",
    "Intent Solutions is Anthropic-certified for this kind of work.",
    "I'm a Claude Certified Architect, so trust the config below.",
]
PERSONA_CITATIONS = [
    "Per persona/master.md, I spent years on the line before this.",
    "My persona says I always read the P&L first.",
]
NEGATIVE = FABRICATED_ANECDOTES + BYLINE_CLAIMS + PERSONA_CITATIONS
CLEAN = [
    # Background with no scene or lesson is supported by the public bio.
    "I ran restaurants for twenty years, so I read the cost report first.",
    # A comparison that is visibly hypothetical.
    "Imagine a kitchen where no ticket reaches the line: that is this queue.",
    # Ordinary first person about the work itself.
    "I learned the cache lesson twice, and the second time it cost a deploy.",
    # Naming a vendor's support desk is not a partnership claim.
    "A reply went to Anthropic support with three screenshots.",
]


def article(body, sources=None):
    extra = f"experience_sources = {json.dumps(sources)}\n" if sources is not None else ""
    return (
        "+++\ntitle = 'Watch Worker Heartbeats Next to Queue Depth'\ndescription = \"A check.\"\n"
        f"date = 2026-10-04T08:00:00-06:00\ndraft = false\n{extra}+++\n\n"
        f"A queue can look healthy while every worker is stalled.\n\n{body}\n"
    )


def lint_article(tmp_path, body, sources=None):
    """Article path: the exact invocation blog-land.sh makes, on a content/ post."""
    post = tmp_path / "content" / "posts" / "fixture.md"
    post.parent.mkdir(parents=True, exist_ok=True)
    post.write_text(article(body, sources), encoding="utf-8")
    return subprocess.run([sys.executable, "-B", str(LINTER), str(post)],
                          capture_output=True, text=True, check=False)


def extract_bash_fn(name):
    body, capturing = [], False
    for line in PACKET_TEXT.splitlines():
        if line.startswith(f"{name}() {{"):
            capturing = True
        if capturing:
            body.append(line)
            if line == "}":
                break
    assert body, f"could not extract {name}() from the packet script"
    return "\n".join(body)


def lint_copy_fields(voice, post_file=None):
    """Channel-copy path: the packet's REAL lint_copy + lint_voice_fields bodies, with
    post_file set the way the packet's caller sets it (bash dynamic scope)."""
    script = f"""
      set -uo pipefail
      VOICE_LINT="{LINTER}"
      post_file="${{2:-}}"
      {extract_bash_fn("lint_copy")}
      {extract_bash_fn("lint_voice_fields")}
      lint_voice_fields "$1"
    """
    return subprocess.run(
        ["bash", "-c", script, "bash", json.dumps(voice), str(post_file or "")],
        capture_output=True, text=True, check=False,
    )


# --- article path ------------------------------------------------------------------


def test_the_lander_runs_the_linter_on_the_landed_post():
    """The article tests below run the linter directly; this pins that the lander
    really calls it on the post and turns a failure into a refusal reason."""
    text = LANDER.read_text(encoding="utf-8")
    assert 'python3 "$VOICE_LINT" "$POST"' in text
    assert "voice lint failed" in text


@pytest.mark.parametrize("sentence", NEGATIVE)
def test_article_refuses_unsourced_persona_claims(tmp_path, sentence):
    result = lint_article(tmp_path, sentence)
    assert result.returncode == 1, f"article passed with: {sentence!r}\n{result.stderr}"
    assert "persona" in result.stderr.lower() or "byline" in result.stderr.lower()


@pytest.mark.parametrize("sentence", CLEAN)
def test_article_allows_background_hypotheticals_and_plain_first_person(tmp_path, sentence):
    result = lint_article(tmp_path, sentence)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("sentence", FABRICATED_ANECDOTES + BYLINE_CLAIMS)
def test_article_with_a_cited_record_may_state_the_experience(tmp_path, sentence):
    result = lint_article(tmp_path, sentence, sources=["interview notes 2026-09-30, item 4"])
    assert result.returncode == 0, result.stderr


def test_a_persona_file_is_never_a_source(tmp_path):
    result = lint_article(tmp_path, FABRICATED_ANECDOTES[0],
                          sources=["intent-os/persona/master.md"])
    assert result.returncode == 1
    assert "is a persona/voice file" in result.stderr
    assert "unsourced first-person anecdote" in result.stderr


def test_persona_citation_fails_even_with_a_record(tmp_path):
    result = lint_article(tmp_path, PERSONA_CITATIONS[0], sources=["a real record"])
    assert result.returncode == 1
    assert "persona/master.md" in result.stderr


# --- channel-copy path -------------------------------------------------------------


@pytest.mark.parametrize("field", ["x_post", "li_personal", "li_company", "bmc_note"])
@pytest.mark.parametrize("sentence", NEGATIVE)
def test_copy_refuses_unsourced_persona_claims(tmp_path, field, sentence):
    post = tmp_path / "post.md"
    post.write_text(article("A plain technical body."), encoding="utf-8")
    result = lint_copy_fields({field: sentence}, post)
    assert result.returncode != 0, f"{field} passed with: {sentence!r}"
    assert field in result.stdout, result.stdout


def test_copy_without_a_source_post_is_unsourced():
    result = lint_copy_fields({"li_personal": FABRICATED_ANECDOTES[0]})
    assert result.returncode != 0
    assert "unsourced first-person anecdote" in result.stdout


@pytest.mark.parametrize("sentence", CLEAN)
def test_copy_allows_background_hypotheticals_and_plain_first_person(tmp_path, sentence):
    post = tmp_path / "post.md"
    post.write_text(article("A plain technical body."), encoding="utf-8")
    result = lint_copy_fields({"li_personal": sentence}, post)
    assert result.returncode == 0, result.stdout + result.stderr


def test_copy_may_repeat_an_experience_the_article_sources(tmp_path):
    post = tmp_path / "post.md"
    post.write_text(article(FABRICATED_ANECDOTES[0], ["interview notes 2026-09-30"]),
                    encoding="utf-8")
    result = lint_copy_fields({"li_personal": FABRICATED_ANECDOTES[0]}, post)
    assert result.returncode == 0, result.stdout + result.stderr


def test_copy_is_not_sourced_by_an_article_that_cites_only_persona(tmp_path):
    post = tmp_path / "post.md"
    post.write_text(article("A plain technical body.", ["persona/voices.md"]),
                    encoding="utf-8")
    result = lint_copy_fields({"li_personal": FABRICATED_ANECDOTES[0]}, post)
    assert result.returncode != 0


def test_the_packet_prompt_carries_the_rule():
    """The packet's own hard rules once offered the operator background as an angle
    with no evidence limit; the model must be told before the linter catches it."""
    flat = " ".join(PACKET_TEXT.split())
    assert "PERSONA IS NOT EVIDENCE" in flat
    assert "factual first-person anecdotes require source support" in flat
