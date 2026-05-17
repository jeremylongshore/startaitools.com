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
  - Appends to /home/jeremy/000-projects/blog/startaitools/.claude/skills/blog-backfill/methodology/feedback.jsonl
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
# Words in a title that justify TCH >= 3 (named transferable artifact)
NAMED_ARTIFACT_WORDS = {
    "pattern", "framework", "methodology", "principle", "guard", "guards",
    "rubric", "playbook", "contract", "cascade", "dual-layer", "three-act",
    "anti-pattern", "playbook", "checklist", "protocol",
}
# Words suggesting genuine narrative drama (Tier 3 NAR floor)
DRAMA_WORDS = {
    "reversal", "surprise", "three-act", "cascade", "discovered", "hidden",
    "broke", "broken", "wrong", "miscalibrat",
}


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


def apparent_tier(struct_tier: int, title: str) -> int:
    """Apply title heuristics on top of structural tier.

    Demotion rules:
      Tier 2 without a named artifact in the title -> Tier 1
      Tier 3 without both named-artifact AND drama markers -> Tier 2
    """
    title_lower = title.lower()
    has_artifact = any(w in title_lower for w in NAMED_ARTIFACT_WORDS)
    has_drama = any(w in title_lower for w in DRAMA_WORDS)

    apparent = struct_tier
    if apparent == 2 and not has_artifact:
        apparent = 1
    if apparent == 3 and not (has_artifact and has_drama):
        apparent = 2
    return apparent


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
        apparent = apparent_tier(struct, title)
        orig = cls.get("tier")
        correct = orig == apparent

        record = {
            "slug": slug,
            "date_assessed": str(date.today()),
            "original_tier": orig,
            "correct_tier": apparent if not correct else None,
            "was_correct": 1 if correct else 0,
            "reasoning": (
                f"Auto-sweep: post is {lines} lines (structural tier {struct}); "
                f"title heuristic -> apparent tier {apparent}. "
                f"Classifier said tier {orig}."
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
