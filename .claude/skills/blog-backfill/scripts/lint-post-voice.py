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
    hard, warns = lint_description(text, str(path), date.today().isoformat())
    for w in warns:
        print(f"WARN: {w}", file=sys.stderr)
    return issues + hard


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
