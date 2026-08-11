#!/usr/bin/env python3
"""
feedback-sweep.py — deterministic retrospective grader for blog-backfill posts.

Walks every classifier record in decisions.jsonl that lacks a corresponding
feedback.jsonl entry. For each:
  1. Reads the post's markdown file.
  2. Applies the strict rubric: line count -> structural tier; title heuristics
     for "named transferable artifact" and "narrative drama" -> apparent tier.
  3. Writes a feedback.jsonl entry with source="structural_auto_confirm".
  4. Stdout reports a digest of mismatches (classifier vs rubric).

This runs from cron weekly. It is deterministic: no LLM, no API calls.
Engagement-driven grading (Umami views, dwell, bounce) is future work — once
this v1 is shown to catch the inflation patterns we see, v2 layers on
engagement signal to flip "borderline" calls.

Exit codes:
  0 — sweep ran, regardless of how many records were added or how many
      mismatches were found. The digest is informational.
  1 — fatal IO error (missing file, write failure).

Output:
  - Appends to <repo>/.claude/skills/blog-backfill/methodology/feedback.jsonl
  - Writes digest to stdout (caller wires this into email/ntfy)
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

# --- Paths ---
# Resolve relative to the script's own location so the sweep works regardless
# of where the skill family lives on disk.
#   script:       <repo>/.claude/skills/blog-backfill/scripts/feedback-sweep.py
#   skill root:   parents[1] -> <repo>/.claude/skills/blog-backfill
#   repo root:    parents[3] -> <repo>
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SCRIPT_DIR.parents[3]
METHODOLOGY = SKILL_ROOT / "methodology"
DECISIONS = METHODOLOGY / "decisions.jsonl"
FEEDBACK = METHODOLOGY / "feedback.jsonl"
POSTS = REPO_ROOT / "content/posts"

# --- Rubric thresholds ---
TIER1_MAX_LINES = 145
TIER2_MAX_LINES = 260
# RETIRED 2026-08-11: the title heuristic (NAMED_ARTIFACT_WORDS / DRAMA_WORDS /
# apparent_tier()). It demoted any structurally-Tier-2 post whose TITLE lacked one
# of 15 literal jargon nouns, and it had no branch that could raise a tier.
#
# Measured over the 206 posts on disk before removal:
#   * only 19 (9%) of titles contained any of the 15 words
#   * 72 of 79 structurally-Tier-2 posts (91%) were demoted by the title alone
#   * 187 of 206 posts were INELIGIBLE for a Tier 2 grade at any length or depth
#
# The house title voice is narrative by design ("The Drills Passed. Reality Did
# Not.", "Empty Is Not Clean"), so the heuristic demoted the STYLE and reported it
# as a depth finding. Because apparent <= struct always, it was also incapable of
# ever reporting "too low", which is why the corpus shows 90 mismatches and 90
# downgrades: a one-directional function can only disagree in one direction. That
# 90-to-0 split was read for months as classifier over-confidence. It was the
# grader.
#
# Grading is now the structural signal alone. Headline Brier over August fell from
# 0.5368 to 0.2643 on removal, with no change to classifier behaviour: the whole
# gap was measurement error. Full detail: methodology/calibration-2026-08-interim-0811.md.


def parse_frontmatter(text: str) -> dict:
    """Extract TOML or YAML front matter as a flat dict."""
    if text.startswith("+++"):
        m = re.search(r"^\+\+\+\n(.*?)\n\+\+\+", text, re.DOTALL | re.MULTILINE)
        delim_pattern = r"^(\w+)\s*=\s*['\"]?([^'\"]+?)['\"]?\s*$"
    elif text.startswith("---"):
        m = re.search(r"^---\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
        delim_pattern = r"^(\w+):\s*['\"]?([^'\"]+?)['\"]?\s*$"
    else:
        return {}
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        kv = re.match(delim_pattern, line)
        if kv:
            fm[kv.group(1)] = kv.group(2)
    return fm


def structural_tier(lines: int) -> int:
    if lines <= TIER1_MAX_LINES:
        return 1
    if lines <= TIER2_MAX_LINES:
        return 2
    return 3


def rubric_tier(struct_tier: int, title: str = "") -> int:
    """The rubric grade for a post. Structural signal only.

    `title` is accepted and ignored, kept so callers and tests that still pass it
    do not break. If a future rubric wants a content signal it must read the BODY
    (where a named artifact actually appears if the post has one), never the title.
    """
    return struct_tier


def load_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def main():
    if not DECISIONS.exists():
        print(f"FATAL: {DECISIONS} not found", file=sys.stderr)
        return 1
    if not POSTS.exists():
        print(f"FATAL: {POSTS} not found", file=sys.stderr)
        return 1

    decisions = load_jsonl(DECISIONS)
    feedback = load_jsonl(FEEDBACK)
    feedback_slugs = {r.get("slug") for r in feedback if r.get("slug")}

    # Classifier records keyed by slug (most recent wins)
    classifiers = {}
    for d in decisions:
        if "tier" not in d or "dimensions" not in d:
            continue
        slug = d.get("slug")
        if slug:
            classifiers[slug] = d

    added = []
    skipped = []
    mismatches = []

    for slug, cls in classifiers.items():
        if slug in feedback_slugs:
            skipped.append(slug)
            continue
        post_path = POSTS / f"{slug}.md"
        if not post_path.exists():
            skipped.append(slug)
            continue
        text = post_path.read_text()
        fm = parse_frontmatter(text)
        title = fm.get("title", slug)
        body = text.split("+++", 2)[-1] if text.startswith("+++") else text.split("---", 2)[-1]
        lines = body.count("\n")

        struct = structural_tier(lines)
        apparent = rubric_tier(struct, title)
        orig = cls.get("tier")
        correct = orig == apparent

        record = {
            "slug": slug,
            "date_assessed": str(date.today()),
            "original_tier": orig,
            "correct_tier": apparent if not correct else None,
            "was_correct": 1 if correct else 0,
            "reasoning": (
                f"Auto-sweep: post is {lines} lines (structural tier {struct}). "
                f"Classifier said tier {orig}. "
                f"Rubric = structural signal only; the title heuristic was retired "
                f"2026-08-11 (it made 187 of 206 posts ineligible for Tier 2 at any "
                f"length and could only ever demote)."
            ),
            "year_from_now_useful": None,
            "engagement_data": None,
            "source": "structural_auto_confirm",
            "metadata": {
                "lines": lines,
                "structural_tier": struct,
                "rubric_tier": apparent,
                "title": title,
            },
        }
        added.append(record)
        if not correct:
            mismatches.append((slug, orig, apparent, lines))

    # Append in one shot
    if added:
        with FEEDBACK.open("a") as f:
            for r in added:
                f.write(json.dumps(r) + "\n")

    # Digest
    print(f"feedback-sweep: scanned {len(classifiers)} classifier records")
    print(f"  added {len(added)} new feedback records")
    print(f"  skipped {len(skipped)} (already had feedback or post missing)")
    print(f"  mismatches: {len(mismatches)} of {len(added)} added")
    if mismatches:
        print("\n  Mismatches (classifier_tier -> rubric_tier):")
        for slug, orig, apparent, lines in mismatches:
            print(f"    {slug[:60]:<60}  T{orig} -> T{apparent}  ({lines} lines)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
