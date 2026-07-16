#!/usr/bin/env python3
"""lint-post-voice.py: hard fail on em/en dashes and banned AI-slop phrases.

Gates NEW blog prose only (the daily produce -> land path). Does not rewrite
history: callers pass specific post paths (the post being landed / PR-changed
files). Exit 0 = clean, 1 = violations found, 2 = usage/IO error.

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


def lint_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [f"{path}: IO error: {e}"]
    return lint_text(text, str(path))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Markdown post path(s) to lint (new/changed posts only)",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=50,
        help="Cap printed issues per file (default 50); full count still reported",
    )
    args = parser.parse_args(argv)

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
