#!/usr/bin/env python3
"""lint-post-voice.py: hard fail on em/en dashes and banned AI-slop phrases.

Gates NEW blog prose only (the daily produce -> land path). Does not rewrite
history: callers pass specific post paths (the post being landed / PR-changed
files). Exit 0 = clean, 1 = violations found, 2 = usage/IO error.

Two input modes:
  path mode   (default) lint one or more markdown files on disk
  --stdin     lint a single blob of text piped in, labelled by --label

--stdin exists because the ARTICLE was the only linted surface. The social copy
the posting packet generates and mails to Ezekiel went out ungated, so dashes and
slop reached the one surface a reader sees first. blog-posting-packet.sh now pipes
every model-authored copy field through this same linter, which means the article
and the syndication copy are held to one deny-list instead of two drifting ones.

Banned punctuation (hard no, anywhere in the file including title/description):
  U+2014 em dash
  U+2013 en dash
  HTML entities &mdash; &ndash; &#8212; &#8211; &#x2014; &#x2013;

Banned AI-slop phrases: case-insensitive whole-phrase / word-boundary matches.

SINGLE SOURCE OF TRUTH for the phrase list is voice-denylist.json (this dir).
Thread B1 (2026-07-16) extracted the list from here into that JSON so the linter
and the writer instruction docs stop drifting. Edit the JSON, not this file.

Robustness: the dash ban is hardcoded below (the invariant #1 rule) and always
enforces. The phrase list is LOADED from the JSON; if the JSON is missing or
malformed, the linter prints a loud warning and enforces dashes only rather than
crashing (a crash here would quarantine every post via blog-land.sh).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# Unicode dashes
EM = "\u2014"
EN = "\u2013"

HTML_DASH_RE = re.compile(
    r"&(?:mdash|ndash);|&#(?:8212|8211);|&#x(?:2014|2013);",
    re.IGNORECASE,
)

DENYLIST_PATH = Path(__file__).resolve().parent / "voice-denylist.json"


def load_slop_patterns(
    path: Path = DENYLIST_PATH,
) -> list[tuple[str, re.Pattern[str]]]:
    """Load the banned-phrase patterns from voice-denylist.json.

    Returns a list of (label, compiled-regex) tuples. On any failure (missing
    file, bad JSON, bad regex, empty list) prints a loud warning to stderr and
    returns [] so the caller enforces the hardcoded dash ban only. Never raises:
    this runs on the land path where an exception would quarantine every post.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        raw = data["slop_phrases"]
        patterns: list[tuple[str, re.Pattern[str]]] = []
        for entry in raw:
            patterns.append((entry["label"], re.compile(entry["pattern"], re.I)))
        if not patterns:
            raise ValueError("slop_phrases is empty")
        return patterns
    except Exception as e:  # noqa: BLE001 - degrade, never brick the gate
        print(
            f"WARNING: could not load voice deny-list from {path} ({e}); "
            "enforcing the em/en dash ban only. Fix the JSON.",
            file=sys.stderr,
        )
        return []


SLOP_PATTERNS: list[tuple[str, re.Pattern[str]]] = load_slop_patterns()


def _line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_nl = text.rfind("\n", 0, index)
    col = index - last_nl
    return line, col


def _mask_for_slop(text: str) -> str:
    """Blank out fenced code, inline code, and URLs for phrase checks only.

    Replaces matched spans with spaces of equal length so line/col offsets from
    the original text stay valid. Em/en dash scanning still uses raw text.
    """

    def blank(m: re.Match[str]) -> str:
        return " " * len(m.group(0))

    cleaned = re.sub(r"```[\s\S]*?```", blank, text)
    cleaned = re.sub(r"`[^`\n]+`", blank, cleaned)
    cleaned = re.sub(r"https?://[^\s)>\]]+", blank, cleaned)
    return cleaned


# --- runaway-sentence guard (opt-in, syndication copy only) -----------------
#
# This is NOT a "write short" rule, and the distinction is the whole point.
#
# Measured against the persona corpus, sentence length does not separate Jeremy
# from our own AI prose: our posts run a sentence p50 of 11 words and his
# composed writing runs 10. Targeting a short sentence length is therefore
# cargo cult, and an earlier version of the packet wiring did exactly that,
# handing composed LinkedIn copy a median derived from one-line commands.
#
# What IS worth catching is the runaway tail. When the model drifts it does not
# drift to 12-word sentences, it drifts to a median of 35, meaning over half the
# copy is longer than 90% of anything he has written. That is a defect a human
# would catch instantly and no other gate in this pipeline sees.
#
# So the threshold is deliberately permissive and derived, not chosen: it is the
# p90 of his composed-band sentence length, passed in by the caller from
# voice-fingerprint.json. It should almost never fire. When it does, the packet
# regenerates once and then degrades loudly, same as a deny-list hit.
SENTENCE_SPLIT_RE = re.compile(r"[.!?]+\s+|\n+")


def lint_sentence_runaway(text: str, path: str, max_median: int) -> list[str]:
    lengths = [
        len(s.split())
        for s in SENTENCE_SPLIT_RE.split(text)
        if s.strip()
    ]
    if len(lengths) < 2:
        return []
    lengths.sort()
    mid = len(lengths) // 2
    median = (
        lengths[mid]
        if len(lengths) % 2
        else (lengths[mid - 1] + lengths[mid]) / 2
    )
    if median <= max_median:
        return []
    return [
        f"{path}:1:1: runaway sentences (median {median:g} words > {max_median}, "
        f"the p90 of his composed writing). Over half this copy is longer than "
        f"90% of anything he has written. Break the thought up; do NOT just "
        f"chop it into short sentences."
    ]


def lint_text(text: str, path: str) -> list[str]:
    issues: list[str] = []

    for i, ch in enumerate(text):
        if ch == EM:
            line, col = _line_col(text, i)
            issues.append(
                f"{path}:{line}:{col}: em dash (U+2014) hard ban; use period/comma/colon/parens"
            )
        elif ch == EN:
            line, col = _line_col(text, i)
            issues.append(
                f"{path}:{line}:{col}: en dash (U+2013) hard ban; use hyphen or rephrase"
            )

    for m in HTML_DASH_RE.finditer(text):
        line, col = _line_col(text, m.start())
        issues.append(
            f"{path}:{line}:{col}: HTML dash entity {m.group()!r} hard ban"
        )

    slop_text = _mask_for_slop(text)
    for label, pat in SLOP_PATTERNS:
        for m in pat.finditer(slop_text):
            line, col = _line_col(text, m.start())
            # Report the original surface text (same offsets as slop_text).
            surface = text[m.start() : m.end()]
            issues.append(f"{path}:{line}:{col}: AI-slop phrase ({label}): {surface!r}")

    return issues


# --- Description framing (tone audit 2026-08-11) -----------------------------
#
# The `description` field is the highest-traffic surface this property owns. It
# renders in RSS, in search results, and on every social card, so for most people
# it IS the post. The 2026-08-11 tone audit measured roughly 69% of descriptions
# leading with the fault rather than with the transferable mechanism.
#
# This is not a request to hide the failure. Both halves are already being
# written; they are ordered wrong. Same facts, same failure, nothing removed:
#
#   before: "A Flask authorization bug locked every member out of free courses
#            while tests stayed green. Status code asserts cannot see rendered
#            state on a 200 page."
#   after:  "Status code asserts cannot see rendered state on a 200 page. How an
#            authorization bug survived a green suite."
#
# The scan impression flips from "their product broke" to "they know something
# you do not", and the second one is true.
#
# WARNING-ONLY until DESCRIPTION_RULE_ENFORCE_FROM, then it joins the hard
# issues. Same dated-flip pattern as blog-land.sh's pattern gate: the flip is a
# date, not a human's memory. Warnings never affect the exit code, so nothing
# quarantines during the window.
DESCRIPTION_RULE_ENFORCE_FROM = "2026-09-01"
# Concrete fault and incident words ONLY. Bare negations (not, no, cannot, never,
# nothing, none) are deliberately absent: they mark negation, not fault, and a
# mechanism claim legitimately negates. "Status code asserts cannot see rendered
# state on a 200 page" is the audit's own prescribed REWRITE, and an earlier cut of
# this lexicon flagged it. A rule that fires on the fix it prescribes gets ignored,
# so this errs toward under-flagging.
_FAULT_TOKENS = {
    "broke", "broken", "break", "breaks", "failed", "failure", "fails",
    "lied", "lying", "lies", "wrong", "silently", "silent", "locked",
    "drift", "drifted", "stale", "fabricated", "missed", "missing",
    "defect", "bug", "bugs", "empty", "inert", "hollow", "crash", "crashed",
    "outage", "stalled", "dead", "lost", "corrupted", "wedged", "hung",
}
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


# The title gets the same rule as the description, and it matters more: the title
# is the only thing most people ever read, and it is what the archive looks like
# read in bulk.
#
# Measured across all 338 posts on 2026-08-13, titles carrying a fault or negation
# word ran 0% in 2025-09, 3% in 2025-12, 22% in 2026-05, 44% in 2026-06, 51% in
# 2026-07 and 83% in 2026-08. The site did not sound like this for its first eight
# months, so this is drift, not house style.
#
# The 2026-08-11 tone audit fixed exactly this for `description` and stopped
# there, which is why the title kept drifting for another two months while the
# description improved. Same lexicon, same dated flip, same reordering intent:
# lead with the finding, name the wreckage second.
TITLE_RULE_ENFORCE_FROM = "2026-09-01"

# The title lexicon is the description lexicon plus three absence nouns.
#
# The description rule deliberately excludes bare negations, because a mechanism
# claim legitimately negates ("cannot see rendered state on a 200 page"). That
# reasoning holds for a sentence and breaks for a title, where "Nothing", "None"
# and "Never" as the SUBJECT are the confessional tic itself: "Six Systems
# Reporting Nothing", "Nothing Read It, So Nothing Failed", "Three Copies of the
# Key, None of the Passphrase". None of those contains a fault word, and all
# three read as a report of our own incompetence.
#
# Bare "not" stays out on purpose. It fires on "Good mechanisms are not an
# architecture until a doctrine names them", which is a constructive title, and a
# rule that flags good work gets switched off.
# "mistake" is absent from the shared lexicon and belongs here: "The Agent's
# Mistakes Were the Fast Ones" is the frame this rule exists to catch. It is added
# to the title set rather than to _FAULT_TOKENS so the description rule, which was
# tuned separately and is already close to its enforcement date, does not move.
_TITLE_FAULT_TOKENS = _FAULT_TOKENS | {
    "nothing", "none", "never", "mistake", "mistakes",
}


def _front_matter_title(text: str) -> str | None:
    m = re.match(r"^(\+\+\+|---)\n(.*?)\n\1", text, re.DOTALL)
    if not m:
        return None
    t = re.search(r"^title\s*[=:]\s*['\"](.+?)['\"]\s*$", m.group(2), re.M)
    return t.group(1) if t else None


def title_leads_with_fault(title: str) -> bool:
    """True when the fault is the subject of the title.

    Unlike the description rule this scans the WHOLE title, not the first clause.
    A title is six or eight words long, so a fault word anywhere in it is the
    subject of the title, not a detail inside it. Checking only the first clause
    passed "The Day The Green Checks Were Lying", where the whole point of the
    title is the last word.
    """
    words = set()
    # Split hyphens too. "Wrong-Mode Green Is Not a Gate" is a fault title and
    # tokenising on whitespace alone hides "wrong" inside "wrong-mode".
    for w in re.split(r"[\s\-‐‑]+", title.strip()):
        w = w.strip(".,:;!?()[]'\"").lower()
        if not w:
            continue
        words.add(w)
        if w.endswith("s") and len(w) > 3:
            words.add(w[:-1])
    return bool(words & _TITLE_FAULT_TOKENS)


def lint_title(text: str, path: str, today: str) -> tuple[list[str], list[str]]:
    """Return (hard_issues, warnings) for the title field."""
    title = _front_matter_title(text)
    if not title or not title_leads_with_fault(title):
        return [], []
    msg = (
        f"{path}: title leads with the fault, not the finding: {title!r}. "
        f"Lead with what a reader takes away, then name the incident. The failure "
        f"stays in the post; it does not have to be the headline."
    )
    if today >= TITLE_RULE_ENFORCE_FROM:
        return [msg], []
    return [], [f"{msg} (advisory until {TITLE_RULE_ENFORCE_FROM})"]


def _front_matter_description(text: str) -> str | None:
    """Pull `description` out of TOML or YAML front matter. None if absent."""
    m = re.match(r"^(\+\+\+|---)\n(.*?)\n\1", text, re.DOTALL)
    if not m:
        return None
    d = re.search(r"^description\s*[=:]\s*['\"](.+?)['\"]\s*$", m.group(2), re.M)
    return d.group(1) if d else None


def description_leads_with_fault(description: str) -> bool:
    """True when the FIRST sentence of the description leads on the fault.

    Deliberately checks only the first sentence. A description that states the
    mechanism and then names the incident is exactly what we want, and it will
    contain fault words in its second half.
    """
    first = _SENTENCE_SPLIT.split(description.strip(), 1)[0]
    words = set()
    for w in first.split():
        w = w.strip(".,:;!?()[]'\"").lower()
        if not w:
            continue
        words.add(w)
        # Crude depluralisation so the lexicon does not have to carry both forms.
        # "failures" missed the first cut of this list, on the very post that
        # motivated the rule, which is a good argument against hand-listing every
        # inflection.
        if w.endswith("s") and len(w) > 3:
            words.add(w[:-1])
    return bool(words & _FAULT_TOKENS)


def lint_description(text: str, path: str, today: str) -> tuple[list[str], list[str]]:
    """Return (hard_issues, warnings) for the description field."""
    desc = _front_matter_description(text)
    if not desc or not description_leads_with_fault(desc):
        return [], []
    first = _SENTENCE_SPLIT.split(desc.strip(), 1)[0]
    msg = (
        f"{path}: description leads with the fault, not the mechanism: {first!r}. "
        f"Lead with the transferable finding, then name the incident. The failure "
        f"stays in; it moves to the second clause."
    )
    if today >= DESCRIPTION_RULE_ENFORCE_FROM:
        return [msg], []
    return [], [f"{msg} (advisory until {DESCRIPTION_RULE_ENFORCE_FROM})"]


def lint_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"{path}: IO error: {e}"]
    issues = lint_text(text, str(path))
    today = date.today().isoformat()
    hard, warns = lint_description(text, str(path), today)
    t_hard, t_warns = lint_title(text, str(path), today)
    for w in warns + t_warns:
        print(f"WARN: {w}", file=sys.stderr)
    return issues + hard + t_hard


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Markdown post path(s) to lint (new/changed posts only)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Lint a single blob of text read from stdin instead of file paths",
    )
    parser.add_argument(
        "--label",
        default="<stdin>",
        help="Name to report issues against in --stdin mode (e.g. li_company)",
    )
    parser.add_argument(
        "--max-median-sentence",
        type=int,
        default=0,
        help=(
            "--stdin only. Flag copy whose MEDIAN sentence exceeds N words. "
            "Opt-in runaway guard for syndication copy; 0 (default) disables it. "
            "Pass the composed-band p90 from persona/voice-fingerprint.json. This "
            "is not a write-short rule: sentence length does not distinguish his "
            "prose from AI prose, so it only catches the runaway tail."
        ),
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=50,
        help="Cap printed issues per file (default 50); full count still reported",
    )
    args = parser.parse_args(argv)

    if args.stdin:
        if args.paths:
            print("--stdin takes no path arguments", file=sys.stderr)
            return 2
        try:
            text = sys.stdin.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"{args.label}: IO error: {e}", file=sys.stderr)
            return 2
        issues = lint_text(text, args.label)
        if args.max_median_sentence > 0:
            issues += lint_sentence_runaway(
                text, args.label, args.max_median_sentence
            )
        if not issues:
            print(f"OK: {args.label}")
            return 0
        print(f"FAIL: {args.label} ({len(issues)} issue(s))", file=sys.stderr)
        for msg in issues[: args.max_issues]:
            print(f"  {msg}", file=sys.stderr)
        if len(issues) > args.max_issues:
            print(f"  … +{len(issues) - args.max_issues} more", file=sys.stderr)
        return 1

    if not args.paths:
        print("no paths given (and --stdin not set)", file=sys.stderr)
        return 2

    any_fail = False
    io_fail = False
    for path in args.paths:
        if not path.is_file():
            print(f"{path}: not a file", file=sys.stderr)
            io_fail = True
            continue
        issues = lint_file(path)
        if issues and ": IO error:" in issues[0]:
            print(issues[0], file=sys.stderr)
            io_fail = True
            continue
        if not issues:
            print(f"OK: {path}")
            continue
        any_fail = True
        print(f"FAIL: {path} ({len(issues)} issue(s))", file=sys.stderr)
        for msg in issues[: args.max_issues]:
            print(f"  {msg}", file=sys.stderr)
        if len(issues) > args.max_issues:
            print(f"  … +{len(issues) - args.max_issues} more", file=sys.stderr)

    if io_fail:
        return 2
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
