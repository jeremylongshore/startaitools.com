#!/usr/bin/env python3
"""Deterministically reconcile published posts with catalog claims and audit state."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DECISIONS = ROOT / ".claude/skills/blog-backfill/methodology/decisions.jsonl"
DATE_RE = re.compile(r"^date\s*[=:]\s*['\"]?(\d{4}-\d{2}-\d{2})")
TITLE_RE = re.compile(r"^title\s*[=:]\s*['\"](.*?)['\"]\s*$")
SLUG_RE = re.compile(r"^slug\s*[=:]\s*['\"](.*?)['\"]\s*$")
ROW_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\s{2,}(.+?)\s*$")


def tracked_posts() -> list[dict[str, str]]:
    output = subprocess.check_output(
        ["git", "ls-files", "-z", "content/posts/*.md"], cwd=ROOT
    )
    records: list[dict[str, str]] = []
    for raw in output.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode()
        text = (ROOT / rel).read_text(encoding="utf-8")
        record = {"path": rel, "slug": Path(rel).stem}
        for line in text.splitlines()[:30]:
            if match := DATE_RE.match(line):
                record["date"] = match.group(1)
            elif match := TITLE_RE.match(line):
                record["title"] = match.group(1)
            elif match := SLUG_RE.match(line):
                record["slug"] = match.group(1)
        if "date" not in record or "title" not in record:
            raise ValueError(f"missing date/title front matter: {rel}")
        records.append(record)
    return records


def article_rows(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- catalog-inventory:start -->(.*?)<!-- catalog-inventory:end -->",
        text,
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"catalog inventory markers missing: {path}")
    rows = []
    for line in match.group(1).splitlines():
        if row := ROW_RE.match(line):
            rows.append((row.group(1), row.group(2)))
    return rows


def decisions() -> list[dict[str, object]]:
    records = []
    for number, line in enumerate(DECISIONS.read_text(encoding="utf-8").splitlines(), 1):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid decisions JSON at line {number}: {error}") from error
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--end", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--article", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.end < args.start:
        raise ValueError("--end must not precede --start")
    posts = [
        post
        for post in tracked_posts()
        if args.start <= dt.date.fromisoformat(post["date"]) <= args.end
    ]
    posts.sort(key=lambda post: (post["date"], post["title"], post["slug"]))
    failures: list[str] = []

    if args.article:
        expected = [(post["date"], post["title"]) for post in posts]
        claimed = article_rows(args.article)
        if claimed != expected:
            failures.append(
                "article inventory differs from Git-tracked catalog\n"
                f"  expected={expected!r}\n  claimed={claimed!r}"
            )

    records = decisions()
    classifiers = {
        str(record["slug"])
        for record in records
        if record.get("slug") and record.get("tier") is not None
    }
    audits = {
        str(record["slug"])
        for record in records
        if record.get("slug") and record.get("audit_addendum") is True
    }
    unpublished = {
        str(record["slug"])
        for record in records
        if record.get("slug") and record.get("publication_status") == "not_published"
    }
    published_slugs = {post["slug"] for post in posts}

    for post in posts:
        if post["slug"] not in classifiers:
            failures.append(f"published post lacks classifier record: {post['slug']}")
        if post["slug"] not in audits:
            failures.append(f"published post lacks audit addendum: {post['slug']}")

    for record in records:
        slug = str(record.get("slug", ""))
        date = str(record.get("date", ""))
        if (
            slug
            and args.start.isoformat() <= date <= args.end.isoformat()
            and (record.get("tier") is not None or record.get("audit_addendum") is True)
            and slug not in published_slugs
            and slug not in unpublished
        ):
            failures.append(f"decision record points to no tracked publication: {slug}")

    if failures:
        print("CATALOG AUDIT FAILED", file=sys.stderr)
        for failure in dict.fromkeys(failures):
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        f"CATALOG AUDIT OK: {len(posts)} tracked posts from {args.start} through {args.end}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
