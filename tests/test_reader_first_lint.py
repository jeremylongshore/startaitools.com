"""Reader-first lint: can a stranger follow the post? (glossary, opening, ledes)."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".claude/skills/blog-backfill/scripts/lint-post-voice.py"
SPEC = importlib.util.spec_from_file_location("lint_post_voice_reader", SCRIPT)
lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lint)
ENFORCED, ADVISORY = "2099-01-01", "2000-01-01"
FILLER = " ".join(["word"] * 320)


def post(body, *, title="Monitoring Freshness Separately", description="A check.", tldr="A."):
    return (
        f"+++\ntitle = '{title}'\ndescription = \"{description}\"\ntldr = \"{tldr}\"\n"
        f"date = 2026-09-20T08:00:00-06:00\ndraft = false\n+++\n\n{body}\n"
    )


def findings(text):
    return lint.lint_reader_first(text, "p.md", ENFORCED)[0]


@pytest.mark.parametrize(
    "sentence",
    [
        "The lander (the script that commits and publishes) refused the run.",
        "The lander, the script that commits and publishes, refused the run.",
        "The lander is the script that commits and publishes.",
        "A separate script called the lander refused the run.",
    ],
)
def test_a_term_defined_in_its_first_sentence_passes(sentence):
    assert findings(post(f"A publish step can refuse a run. {sentence}")) == []


def test_a_term_used_before_it_is_defined_is_named_with_a_suggested_gloss():
    (message,) = findings(post("A publish step can refuse a run. The lander refused it."))
    assert "house term 'lander'" in message
    assert "the script that commits and publishes" in message


def test_only_the_first_use_needs_the_definition():
    body = "The lander (the publish script) refused it. Later the lander accepted it."
    assert findings(post(body)) == []


def test_a_definition_that_arrives_after_the_first_use_is_too_late():
    body = "The lander refused it. The lander (the publish script) accepted the next one."
    assert len(findings(post(body))) == 1


def test_ordinary_english_is_not_the_house_sense():
    assert findings(post("It was an epic rewrite of the parser and it shipped.")) == []
    assert findings(post("A receipt email follows every deletion.")) == []
    assert len(findings(post("One epic groups the work; each bead under it ships alone."))) == 2


def test_first_house_use_after_an_ordinary_use_is_still_checked():
    body = "A receipt email follows every deletion. The run then wrote a receipt to disk."
    (message,) = findings(post(body))
    assert "house term 'receipt'" in message


def test_case_sensitive_terms_do_not_fire_on_the_common_word():
    assert findings(post("There was a lot of buzz about the release.")) == []
    assert len(findings(post("The alert reached Buzz within a minute."))) == 1


def test_fenced_code_and_headings_are_not_prose():
    body = "A publish step can refuse a run.\n\n## The lander\n\n```sh\nlander --dry-run\n```\n"
    assert findings(post(body)) == []


@pytest.mark.parametrize(
    "reference,label",
    [("a1b2c3d", "commit hash"), ("#1234", "PR or issue number"), ("064-DR-STND", "doc number")]
    + [("decision-log/043", "decision number"), ("D159", "decision number")],
)
def test_internal_references_are_refused_in_the_opening_and_allowed_later(reference, label):
    (message,) = findings(post(f"The fix landed in {reference} on the first try. {FILLER}"))
    assert label in message and "first 300 words" in message
    assert findings(post(f"{FILLER} The fix landed in {reference}.")) == []


@pytest.mark.parametrize("innocent", ["deadbeef", "1234567", "the #1 cause", "H2O and CO2"])
def test_the_hash_and_number_patterns_do_not_fire_on_ordinary_tokens(innocent):
    assert findings(post(f"We measured {innocent} before anything else.")) == []


@pytest.mark.parametrize(
    "field,value",
    [("title", "The Day's Work on the Parser"), ("description", "Today the parser shipped.")]
    + [("tldr", "On September 20 the parser shipped."), ("body", "The day started with a parser.")],
)
def test_nothing_opens_on_the_day_or_a_date(field, value):
    text = post(value) if field == "body" else post("A parser can stall.", **{field: value})
    (message,) = findings(text)
    assert "opens on the day or a date" in message


def test_the_rule_is_advisory_until_its_date_then_blocks():
    text = post("The lander refused it.")
    hard, warnings = lint.lint_reader_first(text, "p.md", ADVISORY)
    assert hard == [] and len(warnings) == 1
    assert f"advisory until {lint.READER_RULE_ENFORCE_FROM}" in warnings[0]
    hard, warnings = lint.lint_reader_first(text, "p.md", lint.READER_RULE_ENFORCE_FROM)
    assert len(hard) == 1 and warnings == []


def test_a_missing_glossary_disables_the_term_check_loudly_not_silently(monkeypatch, capsys):
    monkeypatch.setattr(lint, "GLOSSARY_PATH", ROOT / "no-such-glossary.json")
    assert findings(post("The lander refused it.")) == []
    assert "first-use definitions are NOT being checked" in capsys.readouterr().err


def test_every_glossary_hint_is_twelve_words_or_fewer_and_no_term_repeats():
    terms = lint._load_glossary()
    assert len(terms) >= 10
    assert [t["term"] for t in terms if len(t["hint"].split()) > 12] == []
    names = [n.lower() for t in terms for n in (t["term"], *t.get("aliases", []))]
    assert len(names) == len(set(names))


def test_only_articles_are_checked_not_scripts_or_docs(tmp_path):
    outside = tmp_path / "notes.md"
    outside.write_text(post("The lander refused it."))
    assert lint.lint_file(outside) == []
