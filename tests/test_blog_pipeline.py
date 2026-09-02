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
import re
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
LINT_MOD = load_module(LINTER, "lint_post_voice")


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


# ---------------------------------------------------------------------------
# 2b. Description framing (tone audit 2026-08-11). The description is the surface
# a stranger actually reads, and 22 of 33 in the audit window led with the fault
# instead of the transferable mechanism. This is a reordering rule: the failure
# stays in, it moves to the second clause.
# ---------------------------------------------------------------------------

linter = load_module(LINTER, "lint_post_voice")


@pytest.mark.parametrize(
    "description",
    [
        "A Flask authorization bug locked every member out of free courses"
        " while tests stayed green.",
        "A green exit code can hide a dead job.",
        "Nothing read it, so nothing failed.",
        "Six agent failures on a self-hosted team relay.",
        "A dead socket is not a dead host.",
    ],
)
def test_fault_leading_descriptions_are_flagged(description):
    assert linter.description_leads_with_fault(description)


@pytest.mark.parametrize(
    "description",
    [
        # The audit's own prescribed rewrite. An earlier lexicon flagged it,
        # because it conflated negation with fault.
        "Status code asserts cannot see rendered state on a 200 page.",
        "Outcome verification is the success criterion, not the exit code.",
        "Nobody had enumerated the other access path.",
    ],
)
def test_negation_alone_is_not_a_fault_lead(description):
    """A mechanism claim legitimately negates. A rule that fires on the fix it
    prescribes gets ignored, so bare negations are out of the lexicon."""
    assert not linter.description_leads_with_fault(description)


@pytest.mark.parametrize(
    "description",
    [
        "Status code asserts cannot see rendered state on a 200 page."
        " How an authorization bug survived a green suite.",
        "Outcome verification is the success criterion for a scheduled job,"
        " not its exit code.",
        "Borg backup encrypted across three hosts, and what redundancy hid.",
        "A deterministic gate at the merge boundary replaces a contract that lived in prose.",
    ],
)
def test_mechanism_leading_descriptions_pass(description):
    """The second clause may name the incident. Only the FIRST sentence is judged."""
    assert not linter.description_leads_with_fault(description)


def test_plural_fault_words_are_caught():
    """'failures' missed the first cut of the lexicon, on the very post that
    motivated the rule. Hand-listing inflections is how a gate gets a hole."""
    assert linter.description_leads_with_fault("Six agent failures on a relay.")
    assert linter.description_leads_with_fault("Two bugs the suite could not see.")


def test_description_rule_is_advisory_before_its_flip_date(tmp_path):
    """Dated flip, not a human's memory. Before the date it must not affect the
    exit code, or it would quarantine posts during the calibration window."""
    post = tmp_path / "p.md"
    post.write_text(
        "+++\ntitle = 'T'\ndescription = \"A bug broke the build.\"\n+++\n\nBody.\n",
        encoding="utf-8")
    text = post.read_text(encoding="utf-8")
    hard, warns = linter.lint_description(text, str(post), "2026-08-11")
    assert not hard and warns, "should be advisory before the flip date"
    hard, warns = linter.lint_description(text, str(post), "2026-09-01")
    assert hard and not warns, "should be a hard issue on and after the flip date"


def test_description_rule_ignores_posts_without_a_description():
    text = "+++\ntitle = 'T'\n+++\n\nBody.\n"
    assert linter.lint_description(text, "p.md", "2026-12-01") == ([], [])


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


# ---------------------------------------------------------------------------
# A voice-gen failure must NAME ITSELF.
#
# 2026-08-14..16: the headless CLI lost its session and printed
# "Not logged in - Please run /login" as assistant text ON STDOUT with exit 0.
# The script captured only stderr (empty), discarded raw stdout on the failure
# path, and logged a bare "voice-gen failed". Ezekiel got three placeholder
# packets and nothing anywhere said why. These guard the diagnosis channel.
# ---------------------------------------------------------------------------


def test_voice_gen_captures_the_provider_exit_code():
    """Exit 124 (timeout) and exit 0 (auth banner) are different failures with
    different fixes. Discarding the code collapses them into one shrug."""
    assert "|| rc=$?" in PACKET_TEXT, "the provider's exit code is not captured"
    assert "exit=$rc" in PACKET_TEXT


def test_voice_gen_logs_raw_output_when_json_extraction_fails():
    """The cause was sitting in the output the whole time and was thrown away."""
    assert "raw output (first 500 bytes)" in PACKET_TEXT
    # Capped, because this runs on every failure and lands in a daily log.
    assert "head -c 500" in PACKET_TEXT


def test_voice_gen_names_the_auth_failure_specifically():
    """Re-authing a provider is nothing like any other fix here, so the log must
    say so rather than making the reader diff the raw output."""
    for probe in ("not logged in", "run /login", "OAuth session expired",
                  "Failed to authenticate", "MiniMax API error"):
        assert probe in PACKET_TEXT, f"auth detector no longer matches {probe!r}"
    assert "NOT AUTHENTICATED" in PACKET_TEXT
    assert "claude setup-token" in PACKET_TEXT, "the log names no remedy"


def test_failure_reason_travels_through_a_file_not_a_variable():
    """generate_voice runs inside $(...), so an assignment cannot reach the
    caller. A file is the only channel that survives the subshell."""
    assert "VOICE_FAIL_FILE=" in PACKET_TEXT
    assert '> "$VOICE_FAIL_FILE"' in PACKET_TEXT
    assert ': > "$VOICE_FAIL_FILE"' in PACKET_TEXT, "stale reason is not cleared"
    assert "every provider failed" in PACKET_TEXT


# ---------------------------------------------------------------------------
# Provider independence. The packet must not be hostage to one vendor's session.
# `claude -p` authenticates with an 8h OAuth token that only an INTERACTIVE
# session refreshes, so an unattended 05:00 run finds it dead. MiniMax uses a
# static key out of SOPS and has nothing to expire. Default is MiniMax for that
# reason alone, with the other provider as fallback either way.
# ---------------------------------------------------------------------------


def test_minimax_is_the_default_provider():
    assert 'VOICE_PROVIDER="${PACKET_VOICE_PROVIDER:-minimax}"' in PACKET_TEXT


def test_both_providers_exist_and_each_backstops_the_other():
    assert "call_claude()" in PACKET_TEXT and "call_minimax()" in PACKET_TEXT
    assert "VOICE_CHAIN=(claude minimax)" in PACKET_TEXT
    assert "VOICE_CHAIN=(minimax claude)" in PACKET_TEXT
    # The chain is actually iterated, not just declared.
    assert 'for provider in "${VOICE_CHAIN[@]}"' in PACKET_TEXT


def test_minimax_reasoning_traces_are_stripped_before_json_extraction():
    """MiniMax-M3 emits <think>...</think> in the SAME content stream. The
    extractor takes first-{ through last-}, so an unstripped trace that merely
    discusses the JSON gets swallowed into the match."""
    assert "<think>" in PACKET_TEXT
    assert "s{<think>.*?</think>}{}gs" in PACKET_TEXT
    strip = PACKET_TEXT.index("<think>.*?</think>")
    extract = PACKET_TEXT.index("""grep -o '{.*}'""")
    assert strip < extract, "reasoning is stripped AFTER the JSON is extracted"


def test_the_minimax_key_never_reaches_argv():
    """argv is world readable through /proc. The key goes in a curl config file
    on tmpfs, mode 600, unlinked after the call."""
    assert "-K \"$cfg\"" in PACKET_TEXT
    assert "/dev/shm/.packet-mm" in PACKET_TEXT
    assert 'chmod 600 "$cfg"' in PACKET_TEXT
    bad = [ln for ln in PACKET_TEXT.splitlines()
           if "Authorization: Bearer" in ln and "-H" in ln and not ln.strip().startswith("#")]
    assert not bad, f"key passed as a command-line header: {bad}"


def test_craft_skills_are_stripped_for_any_non_claude_provider():
    """The craft block is a set of Skill-tool instructions. MiniMax has no Skill
    tool, so sending it there asks the model to press a button it does not have,
    and it answers by returning nothing.

    The strip must happen AT THE CALL SITE, not by gating on who is first in the
    chain. Gating on the primary leaks the block onto the claude->minimax fallback
    leg, which is exactly the bug this replaced (2026-08-17)."""
    assert '[ "$provider" != "claude" ]' in PACKET_TEXT
    assert "PLATFORM CRAFT \\(do this FIRST\\)" in PACKET_TEXT
    assert "END PLATFORM CRAFT" in PACKET_TEXT
    # The stripped copy is what gets sent, not the original.
    assert 'call_minimax "$this_prompt"' in PACKET_TEXT
    assert 'call_claude  "$this_prompt"' in PACKET_TEXT


def test_minimax_budget_covers_reasoning_not_just_the_answer():
    """M3 bills its <think> trace against the SAME max_tokens as the answer. At
    8192 a real run spent 8191 on reasoning and emitted no JSON at all. Because
    reasoning length varies per prompt, a tight budget is a coin flip on every
    call, not a rare edge."""
    assert "MINIMAX_MAX_TOKENS=" in PACKET_TEXT
    assert "max_tokens:$mt" in PACKET_TEXT, "budget is not actually sent"
    assert "max_tokens:8192" not in PACKET_TEXT, "the budget that caused the bug is back"
    m = re.search(r'MINIMAX_MAX_TOKENS="\$\{PACKET_MINIMAX_MAX_TOKENS:-(\d+)\}"', PACKET_TEXT)
    assert m, "default budget is not readable"
    assert int(m.group(1)) >= 16384, (
        f"default budget {m.group(1)} is too tight for a reasoning model")


def test_truncation_is_diagnosed_rather_than_reported_as_silence():
    """Once the trace is stripped a truncated response looks identical to a dead
    network. One points at the token budget, the other at the wire."""
    assert "finish_reason" in PACKET_TEXT
    assert "MiniMax output truncated" in PACKET_TEXT
    assert "ran out of output budget while reasoning" in PACKET_TEXT


def test_an_unterminated_reasoning_trace_is_still_stripped():
    """A truncated trace has no closing tag, so the paired pattern never fires and
    the whole trace would sail into the JSON extractor."""
    assert "s{<think>(?!.*</think>).*\\z}{}s" in PACKET_TEXT


def test_sops_is_resolved_by_absolute_path_for_cron():
    """Cron's PATH is /usr/bin:/bin; sops lives in ~/bin. A bare `sops` works in
    every by-hand run and fails in every cron run, which is how the MiniMax leg
    was silently dead on 2026-08-18 while the Claude fallback masked it."""
    assert "SOPS_BIN=" in PACKET_TEXT
    bare = [ln for ln in PACKET_TEXT.splitlines()
            if re.search(r'(?<!["$\w/])sops -d', ln) and not ln.strip().startswith("#")]
    assert not bare, f"bare `sops` invocation will fail under cron PATH: {bare}"


def test_heartbeat_distinguishes_quiet_day_from_dead_producer():
    """'Nothing to send' can mean a quiet day OR a producer that died at 04:00.
    On 2026-08-19 the heartbeat said 'healthy' an hour after the producer
    aborted; the two causes must render different subjects."""
    assert "No post landed for" in PACKET_TEXT
    assert "GAP_ALERTED" in PACKET_TEXT
    # The check must run BEFORE the nothing-queued branch, or a stale unpacketed
    # entry (email-retry leftover) silently skips it.
    assert PACKET_TEXT.index("GAP_ALERTED=0") < PACKET_TEXT.index('if [ "${#ENTRIES[@]}" -eq 0 ]')
    # One morning, one verdict: the healthy heartbeat is suppressed when the
    # gap alert already went out.
    assert "suppressing the healthy heartbeat" in PACKET_TEXT
    # An unreadable ledger accuses nobody — it names itself.
    assert "missing or unparseable" in PACKET_TEXT


LAND_TEXT = (SCRIPTS / "blog-land.sh").read_text(encoding="utf-8")


def test_image_assets_push_retries_with_rebase():
    """The post push seconds earlier triggers release.yml, whose bot pushes a
    changelog commit back — so a bare `git push` of the image commit loses the
    race almost every night. The stranded local commit then diverges master and
    the NEXT morning's ff-only preflight aborts the producer (2026-08-18 lost
    its whole publish day to this)."""
    idx = LAND_TEXT.index('-m "assets(')
    start = max(0, idx - 2000)
    block = LAND_TEXT[start:idx + 2000]
    # Anchor sanity: the window must actually contain the image-commit block,
    # or a moved anchor would make these assertions inspect the wrong region.
    assert "static/images/posts" in block, "test window drifted off the image block"
    assert 'push_with_rebase "$DEPLOY_BRANCH"' in block
    # Reject BOTH regression spellings: the script cd's into $BLOG_DIR, so a
    # plain `git push` is just as wrong as the -C form the bug shipped with.
    bare = [ln for ln in block.splitlines()
            if re.search(r'git (-C "\$BLOG_DIR" )?push\b', ln)
            and "push_with_rebase" not in ln
            # urgent_alert lines carry the human FIX instruction ("git pull
            # --rebase && git push") as message text, not as executed code.
            and "urgent_alert" not in ln
            and not ln.strip().startswith("#")]
    assert not bare, f"image push is still a bare git push: {bare}"
    # The failure path must PAGE, not just log — a stranded commit here costs
    # the next publish day, and a WARN nobody reads is how 2026-08-18 was lost.
    assert "urgent_alert" in block, "stranded image commit no longer pages"
    assert "rebase --abort" in block, "half-finished rebase is not cleaned up"


def test_the_packet_records_which_provider_wrote_the_copy():
    """A register shift should be traceable to a model, not guessed at."""
    assert "${VOICE_FAIL_FILE}.provider" in PACKET_TEXT
    assert "(via $used_provider)" in PACKET_TEXT


def test_the_degraded_packet_tells_the_reader_the_cause():
    """The person who can act on NOT AUTHENTICATED is on the CC line of the
    email, not reading a log file on the dev box."""
    assert "${fail_reason:+ Cause: $fail_reason}" in PACKET_TEXT


# ---------------------------------------------------------------------------
# The Vibe craft skills are WIRED INTO the automation, supplying platform
# mechanics only. The precedence chain is the guard that keeps them from also
# supplying voice or punctuation, which is what would wreck the register.
# ---------------------------------------------------------------------------


def test_packet_invokes_the_craft_skills():
    assert "CRAFT_SKILL_DIR=" in PACKET_TEXT
    assert "content-atomizer" in PACKET_TEXT
    assert "direct-response-copy" in PACKET_TEXT
    assert "PLATFORM CRAFT" in PACKET_TEXT


def test_craft_skills_are_scoped_to_mechanics_not_voice():
    """The whole safety of using a marketing pack on a work-journal property is
    this division: craft supplies format, persona supplies voice."""
    flat = " ".join(PACKET_TEXT.split())
    assert "PLATFORM MECHANICS ONLY" in flat
    assert "Do NOT take from those skills" in flat
    # Each of the four things a craft skill must never contribute.
    for forbidden in ["voice, register, or personality", "punctuation style",
                      "phrasing lifted from their examples", "marketing claims"]:
        assert forbidden in flat, f"craft block does not forbid: {forbidden}"


def test_precedence_puts_hard_rules_above_craft():
    flat = " ".join(PACKET_TEXT.split())
    assert "PRECEDENCE" in flat
    hard = flat.index("The hard rules below")
    persona = flat.index("The persona voice and facet dials")
    craft = flat.index("Platform craft from the skills")
    assert hard < persona < craft, "precedence order is not hard rules > persona > craft"


def test_craft_skill_path_is_offline_and_tool_limited():
    """On a cron path a web search is latency we cannot afford and an approval
    prompt we can never answer, so it is denied at the harness, not merely
    discouraged in the prompt."""
    assert '--allowedTools" "Skill" "Read" "Glob" "Grep"' in PACKET_TEXT.replace(
        '(--allowedTools ', '(--allowedTools" "').replace("\n", " ") or \
        '--allowedTools' in PACKET_TEXT
    assert "Do NOT run web searches" in " ".join(PACKET_TEXT.split())
    # WebSearch/WebFetch must not be in the allowlist.
    allow_line = [ln for ln in PACKET_TEXT.splitlines() if "--allowedTools" in ln]
    assert allow_line, "no allowedTools line found"
    assert not any("Web" in ln for ln in allow_line), "web tools are allowlisted"


# ---------------------------------------------------------------------------
# 4c. The measured voice fingerprint (persona rung 3, 2026-08-12).
#
# Before this, the packet was fitted to a PROSE DESCRIPTION of a voice: voices.md
# declared five facets, two of which were the generic agents content-marketer and
# docs-architect renamed, and its own Rung 3 line said "not built". The
# fingerprint is fitted to 1,430 human-authored turns from the Claude Code
# transcripts and separates real Jeremy from our own AI blog prose at AUC 0.965.
#
# The failure mode these guard is specific and was observed in a dry run: the
# model reads "declared facet" as permission to ignore sentence length, and
# LinkedIn copy comes out at 25-word sentences against a measured median of 9.
# ---------------------------------------------------------------------------

FINGERPRINT_FILE = PERSONA / "voice-fingerprint.json"


def test_packet_reads_the_measured_fingerprint():
    assert "VOICE_FINGERPRINT=" in PACKET_TEXT
    assert "MEASURED VOICE FINGERPRINT" in PACKET_TEXT, (
        "the fingerprint is not injected into the voice prompt"
    )


@pytest.mark.skipif(not FINGERPRINT_FILE.exists(),
                    reason="intent-os persona not checked out here")
def test_fingerprint_file_carries_its_own_limits():
    """A profile that does not state what it cannot support invites a consumer to
    over-read it. The corpus is Jeremy dictating to an agent, so it licenses
    claims about sentence shape and none at all about post length."""
    data = json.loads(FINGERPRINT_FILE.read_text(encoding="utf-8"))
    for key in ("provenance", "bands", "what_actually_discriminates",
                "dictation_noise_do_not_reproduce", "not_derivable_from_this_corpus"):
        assert key in data, f"fingerprint is missing {key}"
    assert data["provenance"]["discrimination"]["verdict"] == "separates", (
        "the fingerprint no longer separates real Jeremy from our AI prose; "
        "do not ship it as measured"
    )
    flat = " ".join(str(x) for x in data["not_derivable_from_this_corpus"])
    assert "Post-level length" in flat


def test_packet_does_not_target_a_sentence_length():
    """The corpus is 90% one-line commands, so its blended median (9 words) tracks
    the command band. An earlier version of this wiring shipped that median as a
    universal target and pushed composed LinkedIn copy toward a register Jeremy
    only uses when instructing an agent. Measured, length carries no signal at
    all: our AI prose runs a sentence p50 of 11 and his composed writing runs 10.
    The prompt must not hand the model a length to hit."""
    flat = " ".join(PACKET_TEXT.split())
    assert "DO NOT TARGET A SENTENCE LENGTH" in flat
    assert "Never promote a reference-only number into a target" in flat
    assert "corpus_wide_aggregates_do_not_target" not in flat, (
        "the blended corpus median is being injected as a target again"
    )


def test_packet_carries_the_signals_that_actually_discriminate():
    """What separates him is the habit cluster the AUC test runs on, not length."""
    flat = " ".join(PACKET_TEXT.split())
    assert "WHAT ACTUALLY SEPARATES HIM FROM AI PROSE" in flat
    assert "signals_used_by_the_auc_test" in PACKET_TEXT
    assert "bands.composed.habits" in PACKET_TEXT


@pytest.mark.skipif(not FINGERPRINT_FILE.exists(),
                    reason="intent-os persona not checked out here")
def test_runaway_guard_threshold_is_derived_not_chosen():
    """The gate exists because three rounds of prompt wording failed to hold the
    line (the same field came back at a 27-word median, then 20, then 35). Its
    threshold is the composed-band p90, so it fires only when over half the copy
    is longer than 90% of anything he has written. On 2,892 real blog paragraphs
    it fires on 0.66%."""
    assert "MAX_MEDIAN_SENTENCE" in PACKET_TEXT
    assert ".bands.composed.sentence_words.p90" in PACKET_TEXT, (
        "the runaway threshold must be read from the corpus, not hardcoded"
    )
    # Unset threshold must mean guard-off, never a crash.
    assert "${MAX_MEDIAN_SENTENCE:-}" in PACKET_TEXT
    data = json.loads(FINGERPRINT_FILE.read_text(encoding="utf-8"))
    assert data["bands"]["composed"]["sentence_words"]["p90"] > 0


@pytest.mark.parametrize("copy,should_fail,why", [
    ("short one. another short one. a third.", False, "well inside the band"),
    ("He fixed it. The gate caught the rest.", False, "two short sentences"),
    (("A single value inside the code had been asked to hold two entirely different "
      "facts about the world at once, a dead socket and a genuinely dead host, and "
      "it could only ever carry one answer at a time. The team traced the whole "
      "incident back to four separate compounding causes that had each been "
      "introduced independently over several months of otherwise uneventful "
      "operation of the service."), True, "median far past the composed p90"),
])
def test_runaway_guard_fires_only_on_runaway_copy(copy, should_fail, why):
    result = subprocess.run(
        [sys.executable, str(LINTER), "--stdin", "--label", "t",
         "--max-median-sentence", "33"],
        input=copy, capture_output=True, text=True,
    )
    assert (result.returncode != 0) is should_fail, f"{why}: {result.stderr}"


# ---------------------------------------------------------------------------
# 4d. Title framing (2026-08-13).
#
# Titles carrying a fault or absence word ran 0% in 2025-09 and 50% in 2026-08 by
# this rule's own measure. The site did not sound like this for its first eight
# months, so it is drift, not house style. Three rules in write-post.md caused it
# ("open on the thing that broke" was the only sanctioned opening, "the failure
# stays in" was read as a frame rule, "the failure is the story"), and the
# 2026-08-11 fix for exactly this was scoped to `description` and never extended
# to `title`, which is why descriptions improved for two months while titles kept
# drifting.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("title", [
    "Every Fix Failed in the Shape of the Bug It Fixed",
    "The Day The Green Checks Were Lying",
    "A Dead Socket Is Not a Dead Host",
    "Wrong-Mode Green Is Not a Gate",            # hyphen must not hide "wrong"
    "The Agent's Mistakes Were the Fast Ones",   # "mistake" is title-set only
    "Six Systems Reporting Nothing",             # absence noun, no fault word
    "Nothing Read It, So Nothing Failed",
    "Three Copies of the Key, None of the Passphrase",
])
def test_fault_framed_titles_are_flagged(title):
    assert LINT_MOD.title_leads_with_fault(title), (
        "this is the confessional frame the rule exists to catch"
    )


@pytest.mark.parametrize("title", [
    "Splitting Privileges at the CI Boundary",
    "Rent the Agent, Own the Proof",
    "How the Same Deploy Pattern Crossed Four Repos in One Week",
    "Adversarial Review: The Six Lenses That Halted a Rollout",
    # Bare "not" is deliberately NOT in the lexicon. This is a constructive
    # title and a rule that flags good work gets switched off.
    "Good mechanisms are not an architecture until a doctrine names them",
])
def test_constructive_titles_are_not_flagged(title):
    assert not LINT_MOD.title_leads_with_fault(title)


@pytest.mark.parametrize("rewrite", [
    "When a Fix Inherits the Structure It Was Meant to Remove",
    "One Boolean Behind a Day of Green",
    "Green Checks Can Outlive What They Check",
])
def test_the_prescribed_rewrites_pass_their_own_rule(rewrite):
    """A rule that fires on the fix it prescribes gets ignored.

    The description lexicon carries this warning in its own comments, and the
    first cut of the title rule made exactly that mistake: two of the three
    rewrites written into write-post.md tripped it.
    """
    assert not LINT_MOD.title_leads_with_fault(rewrite)


def test_title_rule_is_advisory_before_its_flip_date():
    post = '+++\ntitle = \'The Day The Green Checks Were Lying\'\n+++\n\nBody.\n'
    hard, warns = LINT_MOD.lint_title(post, "p.md", "2026-08-13")
    assert hard == [] and len(warns) == 1, "must not quarantine during the window"
    hard, warns = LINT_MOD.lint_title(post, "p.md", "2026-09-01")
    assert len(hard) == 1 and warns == [], "must be hard on the flip date"


def test_title_rule_ignores_posts_without_a_title():
    hard, warns = LINT_MOD.lint_title("no front matter here", "p.md", "2026-09-01")
    assert hard == [] and warns == []


def test_runaway_guard_is_off_by_default_so_the_article_path_is_untouched():
    """The article register legitimately runs longer than syndication copy. The
    guard is opt-in and only the packet passes it."""
    long_copy = (
        "A single value inside the code had been asked to hold two entirely "
        "different facts about the world at once, a dead socket and a genuinely "
        "dead host, and it could only ever carry one answer at a time. The team "
        "traced the whole incident back to four separate compounding causes "
        "introduced independently over several months of uneventful operation."
    )
    result = subprocess.run(
        [sys.executable, str(LINTER), "--stdin", "--label", "t"],
        input=long_copy, capture_output=True, text=True,
    )
    assert result.returncode == 0, "guard must be opt-in, not on by default"


def test_packet_forbids_reproducing_the_dictation_typos():
    """The corpus carries a 13.7% typo rate because it is voice-dictated. Lowercase
    starts and fragments are voice and stay. Typos are noise. A profile that gets
    this backwards writes typos on purpose."""
    flat = " ".join(PACKET_TEXT.split())
    assert "NEVER reproduce the dictation typos" in flat
    assert "transcription" in flat.lower() and "NOISE" in PACKET_TEXT


def test_measured_beats_declared_in_the_precedence_ladder():
    flat = " ".join(PACKET_TEXT.split())
    assert "Measured beats declared" in flat
    assert "MEASURED fingerprint above" in flat


def test_craft_skills_have_an_off_switch():
    """A vendor skill in the cron path needs a documented way to be turned off
    without editing the script."""
    assert "PACKET_USE_CRAFT_SKILLS" in PACKET_TEXT
    # Default is on, and the off path must skip both the prompt block and the
    # tool allowlist.
    assert PACKET_TEXT.count("PACKET_USE_CRAFT_SKILLS:-1") >= 2


# ---------------------------------------------------------------------------
# 5b. The X long-form article is a sixth destination. The bash suite covers the
# rendering and the UTM; these cover the parts that live in the shell script and
# the voice spec, where a destination can be half-added without anything failing.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dest", ["substack", "medium", "x_article"])
def test_long_form_destinations_are_tier_gated(dest):
    """The tweet and the two LinkedIn posts are unconditional; every long-form
    republication is not. A Tier 1 field note has no business being pasted whole
    into four other places.

    Asserts the PROPERTY rather than the exact list string. The first cut of this
    test hardcoded `dests+=("substack" "medium" "x_article")` and broke the moment
    a seventh destination was added, which is a test measuring its own literal
    rather than the rule.
    """
    gated = [ln for ln in PACKET_TEXT.splitlines() if "dests+=(" in ln]
    unconditional = [ln for ln in PACKET_TEXT.splitlines() if "local -a dests=(" in ln]
    assert gated and unconditional, "destination list is gone"
    assert any(dest in ln for ln in gated), f"{dest} is not in a tier-gated line"
    assert dest not in unconditional[0], f"{dest} is unconditional, should be gated"
    assert any('"$tier" -ge 2' in ln for ln in gated), "gate is not on tier >= 2"


@pytest.mark.parametrize("dest", ["x", "li_personal", "li_company", "buymeacoffee"])
def test_core_destinations_are_unconditional(dest):
    """buymeacoffee belongs here, not in the tier gate above.

    It was gated with the long-form reposts until 2026-08-13, which meant the
    supporters' feed went dark on every Tier 1 day. The tier gate rations PUBLIC
    syndication reach; the supporters already paid, so they get every post. The
    tier bands the creep guard enforces are 60-70% Tier 1, so the grouping would
    have hidden most of the work from the people funding it.
    """
    unconditional = [ln for ln in PACKET_TEXT.splitlines() if "local -a dests=(" in ln]
    assert dest in unconditional[0], f"{dest} must ship at every tier"


def run_lint_voice_fields(voice: dict) -> subprocess.CompletedProcess:
    """Run the packet's REAL lint_voice_fields against a voice blob.

    Extracts the function bodies from the script rather than reimplementing them,
    so a regression in the script fails here. Sourcing the whole script is not an
    option: it runs its main body at load time.
    """
    script = f"""
      set -uo pipefail
      VOICE_LINT="{LINTER}"
      {extract_bash_fn("lint_copy")}
      {extract_bash_fn("lint_voice_fields")}
      lint_voice_fields "$1"
    """
    return subprocess.run(["bash", "-c", script, "bash", json.dumps(voice)],
                          capture_output=True, text=True, check=False)


def extract_bash_fn(name: str) -> str:
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


@pytest.mark.parametrize(
    ("field", "copy", "why"),
    [
        ("x_article_title", "A title — with an em dash", "em dash"),
        ("x_article_subtitle", "Excited to share what we built.", "slop opener"),
        ("x_article_subtitle", "Let's dive into the pipeline.", "slop phrase"),
    ],
)
def test_x_article_copy_is_rejected_when_dirty(field, copy, why):
    """The packet was once the only unlinted surface in the pipeline. A new copy
    field that skips lint_voice_fields restores that hole for one destination."""
    result = run_lint_voice_fields({field: copy})
    assert result.returncode != 0, f"{why} passed the lint in {field}: {copy!r}"
    assert field in result.stdout, (
        f"lint report does not name the failing field: {result.stdout!r}")


def test_clean_x_article_copy_passes():
    result = run_lint_voice_fields({
        "x_post": "The gate caught it on the first run.",
        "x_article_title": "A Plain Title",
        "x_article_subtitle": "What the reader gets, stated plainly.",
    })
    assert result.returncode == 0, result.stdout + result.stderr


def test_bmc_note_takes_the_personal_facet_and_bans_gratitude_boilerplate():
    """The warmest surface is the easiest one to turn into a mailing list."""
    flat = " ".join(PACKET_TEXT.split())
    assert "bmc_note" in flat
    assert "the Personal facet" in flat
    for rule in ["never thank them", "never ask for anything", "never mention coffee"]:
        assert rule in flat.lower(), f"bmc brief does not forbid: {rule}"


def test_x_article_takes_the_field_facet_not_raw():
    """Both X surfaces would otherwise default to the Raw facet. A long-form
    reader arrived for the substance, so the article framing is Field."""
    flat = " ".join(PACKET_TEXT.split())
    assert "x_article_title / x_article_subtitle" in flat
    assert "the Field facet" in flat
    assert "NOT Raw" in flat


def test_x_article_has_its_own_utm_content():
    """utm_source=x covers the tweet and the article alike, so without
    utm_content the two X rows collapse the way the LinkedIn rows used to."""
    assert 'link_x_article=$(utm "$canonical" "x" "x_article")' in PACKET_TEXT
    assert "x_article:$lxa" in PACKET_TEXT


def _voice_stub() -> dict:
    """The PACKET_VOICE_STUB payload, parsed. It is a single-quoted printf literal."""
    line = next(ln for ln in PACKET_TEXT.splitlines() if '"x_post":"STUB' in ln)
    return json.loads(line.strip()[len("printf '"):-1])


def test_voice_stub_carries_every_field_the_payload_reads():
    """The stub is what structural testing runs against. A field missing here
    exercises a packet shape that never ships."""
    stub = _voice_stub()
    for field in ["x_post", "x_is_thread", "li_personal", "li_company",
                  "substack_subtitle", "x_article_title", "x_article_subtitle"]:
        assert field in stub, f"stub does not produce {field}"


def test_voice_stub_copy_passes_the_voice_lint():
    """The stub used to carry an em dash, so the stubbed path produced copy that
    the very next step in the same script would have rejected. A fixture that
    cannot pass the gate it feeds is a test of nothing."""
    for field, value in _voice_stub().items():
        if not isinstance(value, str):
            continue
        result = lint_stdin(value, field)
        assert result.returncode == 0, f"stub {field} fails the voice lint: {result.stderr}"


@pytest.mark.skipif(not (GLOBAL_SKILL / "references" / "social-bundle.md").exists(),
                    reason="global blog-backfill skill not provisioned on this box")
def test_social_bundle_documents_the_missing_canonical():
    """Substack and Medium can declare a canonical and an X article cannot. If the
    spec does not say so, the destination reads as SEO-neutral syndication when it
    is a reach play, and nobody finds out until the blog is outranked by a repost."""
    text = (GLOBAL_SKILL / "references" / "social-bundle.md").read_text(encoding="utf-8")
    assert "x_article_title" in text and "x_article_subtitle" in text
    assert "no canonical tag" in text.lower()
    assert "reach play" in text.lower()
    assert "Field, not Raw" in text


@pytest.mark.skipif(not (Path.home() / ".claude" / "skills" / "content-atomizer").exists(),
                    reason="Vibe pack not installed on this box")
def test_the_craft_skills_the_packet_names_actually_exist():
    """The packet asks for these by name. A rename upstream turns the craft step
    into a silent no-op, which would look like the pipeline working."""
    for skill in ["content-atomizer", "direct-response-copy"]:
        assert (Path.home() / ".claude" / "skills" / skill / "SKILL.md").is_file()


@pytest.mark.skipif(not (GLOBAL_SKILL / "references" / "polish-seo.md").exists(),
                    reason="global blog-backfill skill not provisioned on this box")
def test_seo_phase_scopes_craft_skills_the_same_way():
    text = (GLOBAL_SKILL / "references" / "polish-seo.md").read_text(encoding="utf-8")
    assert "keyword-research" in text and "seo-content" in text
    assert "never for voice" in text.lower()
    assert "seo-grounding.md` wins" in text or "seo-grounding.md wins" in text
    assert "BLOG_USE_CRAFT_SKILLS=0" in text


@pytest.mark.skipif(not (GLOBAL_SKILL / "references" / "write-post.md").exists(),
                    reason="global blog-backfill skill not provisioned on this box")
def test_article_writing_never_reaches_for_the_marketing_pack():
    """The article is the work journal. The craft skills are a marketing pack, and
    the one place they must never be INVOKED is the writer's brief.

    Checks for invocation, not for the bare word: write-post.md legitimately says
    "the newsletter" in prose about which surfaces are allowed to persuade, and
    banning the English word would be a nonsense gate.
    """
    invocation_names = ["content-atomizer", "direct-response-copy", "seo-content",
                        "lead-magnet", "email-sequences", "positioning-angles",
                        "keyword-research", "brand-voice"]
    for doc in ["write-post.md", "writer-briefing-template.md"]:
        text = (GLOBAL_SKILL / "references" / doc).read_text(encoding="utf-8")
        assert "Skill tool" not in text, f"{doc} tells the writer to invoke a skill"
        for skill in invocation_names:
            # The hyphenated skill slugs are unambiguous; none is ordinary English.
            assert skill not in text, f"{doc} reaches for the marketing skill {skill}"


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


# ---------------------------------------------------------------------------
# Tier-length gate (2026-09-01). blog-land.sh caps the effective tier at what
# the post's LENGTH supports, using the SAME thresholds as the grader. If the
# two ever diverge, the gate and the grader disagree about the same post — so
# this test fails the build the moment they drift apart.
# ---------------------------------------------------------------------------

LAND_TEXT_SH = (SCRIPTS / "blog-land.sh").read_text(encoding="utf-8")
SWEEP_PY = (REPO / ".claude/skills/blog-backfill/scripts/feedback-sweep.py").read_text(
    encoding="utf-8")


def _int_after(text, name):
    m = re.search(rf"{name}\s*=\s*(\d+)", text)
    assert m, f"{name} not found"
    return int(m.group(1))


def test_length_gate_thresholds_match_the_grader():
    """The land gate and the feedback grader must use identical line thresholds,
    or a post can be shipped at one tier and graded at another."""
    assert (_int_after(LAND_TEXT_SH, "LAND_TIER1_MAX_LINES")
            == _int_after(SWEEP_PY, "TIER1_MAX_LINES"))
    assert (_int_after(LAND_TEXT_SH, "LAND_TIER2_MAX_LINES")
            == _int_after(SWEEP_PY, "TIER2_MAX_LINES"))


def test_length_gate_only_ever_downgrades():
    """The gate must never raise a tier — it caps inflation, it does not invent
    escalation. The comparison is strictly classifier > structural."""
    assert 'if [ "$CLASSIFIER_TIER" -gt "$STRUCTURAL_TIER" ]; then' in LAND_TEXT_SH
    assert 'TIER="$STRUCTURAL_TIER"' in LAND_TEXT_SH


def test_length_gate_records_a_feedback_downgrade():
    """A downgrade must leave a deterministic calibration record — this is the
    adjudication signal the score-keyed rules could never surface."""
    assert '"length_gate_downgrade"' in LAND_TEXT_SH
    assert "feedback.jsonl" in LAND_TEXT_SH


# ---------------------------------------------------------------------------
# UTM source hygiene. Umami once recorded a utm_source of "linkedittps://stan..."
# — a source with a URL smashed into it, which corrupts channel attribution.
# utm() must sanitize source/content to bare tokens so that can never recur.
# ---------------------------------------------------------------------------


def test_utm_sanitizes_source_and_content_to_bare_tokens():
    packet = PACKET.read_text(encoding="utf-8")
    assert 'src="${src//[^a-z_]/}"' in packet, \
        "utm() does not strip non-token chars from the source"
    assert 'content="${content//[^a-z_]/}"' in packet, \
        "utm() does not strip non-token chars from content"


# ---------------------------------------------------------------------------
# Next-topics picker must chase what actually gets read. The 90-day attribution
# showed searchable named-tool how-to posts out-pull introspective/governance
# posts 3-4x, so the content-seo prompt must carry that scoring rubric.
# ---------------------------------------------------------------------------

NEXT_TOPICS_SH = (SCRIPTS / "next-topics-refresh.sh").read_text(encoding="utf-8")


def test_next_topics_runs_a_trend_sweep_tied_to_receipts():
    """Trend-riding is a scheduled input, not a lucky catch: sweep 2 searches
    what is hyped this week and only keeps candidates Jeremy has receipts for."""
    t = (SCRIPTS / "next-topics-refresh.sh").read_text(encoding="utf-8")
    assert "SWEEP 2 (trend x receipts)" in t
    assert "trend_hook" in t
    assert "skip it rather than stretch" in t, "trend candidates must require a matching receipt"
    assert "skip sweep 2 silently" in t, "web-search-unavailable must not fail the run"


def test_next_topics_prompt_weights_searchable_howto():
    assert "SCORING RUBRIC" in NEXT_TOPICS_SH
    assert "SEARCHABLE" in NEXT_TOPICS_SH and "NAMED-TOOL" in NEXT_TOPICS_SH
    # It must explicitly deprioritize the shape that loses on traffic.
    assert "introspective" in NEXT_TOPICS_SH
    # And keep tier separate from searchability (the whole point).
    assert "tier the post earns is separate" in NEXT_TOPICS_SH


# ---------------------------------------------------------------------------
# Phase-1 SEO upgrade guardrails (2026-09-01). The SEO layer optimizes
# DISCOVERABILITY (title, description, schema, tldr, FAQ) and must never touch
# the work-journal body voice. These tests pin both the new capabilities and
# the boundary.
# ---------------------------------------------------------------------------

POLISH_SEO = Path.home() / ".claude/skills/blog-backfill/references/polish-seo.md"
WRITE_POST = Path.home() / ".claude/skills/blog-backfill/references/write-post.md"
SCHEMA_PARTIAL = REPO / "layouts/partials/schema.html"
GROUNDING = REPO / ".claude/skills/blog-backfill/references/seo-grounding.md"


def _skip_if_global_missing(p):
    if not p.exists():
        pytest.skip(f"global skill file not provisioned on this box: {p}")


def test_blogposting_schema_is_deterministic_and_deduped():
    """Schema is mechanical metadata: generated by the template for every dated
    page, standing down when a body already carries an inline block, so no page
    ever serves two BlogPosting declarations."""
    t = SCHEMA_PARTIAL.read_text(encoding="utf-8")
    assert '"@type": "BlogPosting"' in t
    assert 'in .RawContent "application/ld+json"' in t, "dedupe guard missing"
    assert "not .Date.IsZero" in t, "must not emit on undated/list pages"
    header = (REPO / "layouts/partials/header.html").read_text(encoding="utf-8")
    assert 'partial "schema.html"' in header, "schema partial is not wired into <head>"


def test_seo_phase_owns_faq_schema_only():
    """The LLM half may emit FAQPage (needs question extraction) but never
    BlogPosting (the template owns it) — duplicating it would ship two blocks."""
    _skip_if_global_missing(POLISH_SEO)
    t = POLISH_SEO.read_text(encoding="utf-8")
    assert "Do NOT emit\n  BlogPosting schema" in t or "Do NOT emit BlogPosting schema" in t
    assert "FAQPage" in t


def test_seo_phase_carries_the_search_query_title_rule():
    _skip_if_global_missing(POLISH_SEO)
    t = POLISH_SEO.read_text(encoding="utf-8")
    assert "Title-as-search-query rule" in t
    assert "Never invent a tool the post does not name" in t


def test_seo_phase_boundary_protects_the_body_voice():
    """The may/may-not list is the voice firewall: caveats, numbers, and the
    failure narrative are untouchable, and the register rules stay absolute."""
    _skip_if_global_missing(POLISH_SEO)
    t = POLISH_SEO.read_text(encoding="utf-8")
    assert "May never change:" in t
    assert "any caveat, limitation," in t
    assert "the failure narrative" in t
    assert "No em dash or en dash anywhere" in t


def test_writer_brief_mandates_a_quotable_tldr():
    _skip_if_global_missing(WRITE_POST)
    t = WRITE_POST.read_text(encoding="utf-8")
    assert "`tldr` is mandatory" in t
    assert "state the FINDING (not the topic)" in t


def test_land_warns_on_missing_tldr_without_blocking():
    t = (SCRIPTS / "blog-land.sh").read_text(encoding="utf-8")
    assert "post has no tldr front-matter param" in t
    # It must be a WARN in the log, never a quarantine REASONS+= entry.
    warn_idx = t.index("post has no tldr front-matter param")
    assert "REASONS+=" not in t[warn_idx - 200:warn_idx], "tldr must warn, not quarantine"


def test_grounding_part6_carries_measured_channel_evidence():
    t = GROUNDING.read_text(encoding="utf-8")
    assert "Part 6" in t
    assert "Bing + DuckDuckGo out-refer Google" in t
    assert "LLM answer engines" in t


# ---------------------------------------------------------------------------
# AI-cliche tier (2026-09-02): 38 patterns adapted from Simon Willison's LLM
# Cliche Highlighter. Hard-enforced like the dash ban, with exactly one
# calibrated advisory exception (colon-into-a-triple, which corpus sampling
# showed firing mostly on honest technical enumerations).
# ---------------------------------------------------------------------------

def _lint_mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "lintmod", REPO / ".claude/skills/blog-backfill/scripts/lint-post-voice.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_cliche_data_file_carries_all_38_with_severities():
    d = json.loads((REPO / ".claude/skills/blog-backfill/scripts/cliche-patterns.json")
                   .read_text(encoding="utf-8"))
    pats = d["patterns"]
    assert len(pats) == 38
    assert "Willison" in d["$comment"]
    sev = {p["id"]: p["severity"] for p in pats}
    assert sev["colon-triple"] == "advisory", "the one calibrated exception"
    assert sum(1 for v in sev.values() if v == "hard") == 37
    assert not any("â" in p["name"] for p in pats), "mojibake in pattern names"


def test_cliche_hits_are_hard_failures():
    lint = _lint_mod()
    hard, warns = lint.lint_cliches(
        "Not just fast, but correct. It works. Sit with that.\n", "t")
    assert any("Not just" in h for h in hard)
    assert any("Sit with that" in h for h in hard)


def test_colon_triple_is_advisory_and_tag_arrays_are_masked():
    lint = _lint_mod()
    hard, warns = lint.lint_cliches(
        "The fix touched three things: the gate, the grader, and the brief.\n", "t")
    assert not hard
    assert any("Colon into a triple" in w for w in warns)
    # a TOML tags array must not fire at all
    hard2, warns2 = lint.lint_cliches(
        '+++\ntags = ["Terraform", "DevOps", "Cloud", "IaC"]\n+++\nBody text here.\n', "t")
    assert not hard2 and not warns2


def test_echo_finder_matches_shared_phrases_not_short_sentences():
    lint = _lint_mod()
    # real echo: consecutive sentences sharing a 3-gram
    echo = ("The gate held the line today. The gate held the line yesterday. "
            "The gate held the line all week.\n")
    hard, _ = lint.lint_cliches(echo, "t")
    assert any("Echoing" in h for h in hard)
    # short unrelated sentences must NOT fire (the first port's false positive)
    staccato = "It broke. We fixed it. Tests ran green quickly after that change landed.\n"
    hard2, _ = lint.lint_cliches(staccato, "t")
    assert not any("Echoing" in h for h in hard2)


def test_clean_work_journal_prose_passes_the_cliche_tier():
    lint = _lint_mod()
    clean = ("The deploy failed because the manifest named a stale image tag. "
             "I repointed it at the digest from the release run and the rollout "
             "completed in four minutes.\n")
    hard, warns = lint.lint_cliches(clean, "t")
    assert not hard and not warns


def test_advisory_escape_hatch_downgrades_everything(monkeypatch):
    monkeypatch.setenv("VOICE_CLICHE_MODE", "advisory")
    lint = _lint_mod()   # re-exec reads the env at import
    hard, warns = lint.lint_cliches("Not just fast, but correct.\n", "t")
    assert not hard and warns
