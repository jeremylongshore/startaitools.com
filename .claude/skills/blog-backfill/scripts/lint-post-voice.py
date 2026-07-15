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
Keep this list in sync with references/write-post.md (Absolutely forbidden).
"""
from __future__ import annotations

import argparse
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

# Phrase patterns — word boundaries where applicable. Keep aligned with
# write-post.md / writer-briefing-template.md / social-bundle.md.
SLOP_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("in this blog post", re.compile(r"\bin this blog post\b", re.I)),
    ("let's dive in", re.compile(r"\blet'?s dive in\b", re.I)),
    ("dive into", re.compile(r"\bdive into\b", re.I)),
    ("diving deep", re.compile(r"\bdiving deep\b", re.I)),
    ("it's worth noting", re.compile(r"\bit'?s worth noting\b", re.I)),
    ("worth noting that", re.compile(r"\bworth noting that\b", re.I)),
    ("delve", re.compile(r"\bdelve[sd]?\b", re.I)),
    ("delving", re.compile(r"\bdelving\b", re.I)),
    ("in today's fast-paced", re.compile(r"\bin today'?s fast[- ]paced\b", re.I)),
    ("game-changer", re.compile(r"\bgame[- ]changers?\b", re.I)),
    ("revolutionize", re.compile(r"\brevolutioniz(?:e|es|ed|ing)\b", re.I)),
    ("seamless", re.compile(r"\bseamless(?:ly)?\b", re.I)),
    ("supercharge", re.compile(r"\bsupercharg(?:e|es|ed|ing)\b", re.I)),
    ("excited to share", re.compile(r"\bexcited to share\b", re.I)),
    ("thrilled to", re.compile(r"\bthrilled to\b", re.I)),
    ("unlock", re.compile(r"\bunlock(?:s|ed|ing)? the\b", re.I)),
    ("leverage (verb hype)", re.compile(r"\bleverag(?:e|es|ed|ing)\b", re.I)),
    ("at its core", re.compile(r"\bat its core\b", re.I)),
    ("in conclusion", re.compile(r"\bin conclusion\b", re.I)),
    ("the landscape of", re.compile(r"\bthe landscape of\b", re.I)),
    ("navigate the", re.compile(r"\bnavigate the\b", re.I)),
    ("comprehensive", re.compile(r"\bcomprehensive\b", re.I)),
    ("in this article", re.compile(r"\bin this article\b", re.I)),
    ("in this post", re.compile(r"\bin this post\b", re.I)),
    ("without further ado", re.compile(r"\bwithout further ado\b", re.I)),
    ("it goes without saying", re.compile(r"\bit goes without saying\b", re.I)),
]


def _line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_nl = text.rfind("\n", 0, index)
    col = index - last_nl
    return line, col


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
    for label, pat in SLOP_PATTERNS:
        for m in pat.finditer(text):
            line, col = _line_col(text, m.start())
            issues.append(f"{path}:{line}:{col}: AI-slop phrase ({label}): {m.group()!r}")

    return issues


def lint_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
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
        if issues and issues[0].endswith("IO error:"):
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
