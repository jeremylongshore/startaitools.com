#!/usr/bin/env python3
"""Restore ledger and API queue entries for posts landed outside blog-land."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / ".blog-syndication-ledger.json"
QUEUE = ROOT / ".crosspost-queue.json"
DECISIONS = ROOT / ".claude/skills/blog-backfill/methodology/decisions.jsonl"


def scalar(text: str, name: str) -> str:
    match = re.search(rf"^{name}\s*=\s*['\"](.*?)['\"]\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"missing {name} in front matter")
    return match.group(1)


def date_value(text: str) -> str:
    match = re.search(r"^date\s*=\s*([^\s]+)", text, re.MULTILINE)
    if not match:
        raise ValueError("missing date in front matter")
    return match.group(1).strip("'\"")


def load(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"expected JSON array: {path}")
    return value


def atomic_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def tier_for(slug: str) -> int:
    matches = []
    for line in DECISIONS.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("slug") == slug and record.get("tier") is not None:
            matches.append(int(record["tier"]))
    if not matches:
        raise ValueError(f"no classifier tier for {slug}")
    return matches[-1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", action="append", required=True)
    parser.add_argument("--apply", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ledger = load(LEDGER)
    queue = load(QUEUE)
    changed_ledger = 0
    changed_queue = 0

    for slug in args.slug:
        post = ROOT / "content" / "posts" / f"{slug}.md"
        if not post.exists():
            raise ValueError(f"tracked post not found: {post}")
        text = post.read_text(encoding="utf-8")
        title = scalar(text, "title")
        published = date_value(text)
        moment = dt.datetime.fromisoformat(published)
        tier = tier_for(slug)
        canonical = f"https://startaitools.com/posts/{slug}/"

        if not any(entry.get("slug") == slug for entry in ledger):
            manual_status = "pending" if tier >= 2 else "n/a"
            ledger.append(
                {
                    "date": moment.date().isoformat(),
                    "slug": slug,
                    "title": title,
                    "canonical_url": canonical,
                    "tier": tier,
                    "published_at": moment.isoformat(),
                    "github_links": [],
                    "packet_sent": False,
                    "syndication": {
                        "x": {"status": "pending", "posted_at": None, "url": None, "by": None},
                        "li_personal": {
                            "status": "pending",
                            "posted_at": None,
                            "url": None,
                            "by": None,
                        },
                        "li_company": {
                            "status": "pending",
                            "posted_at": None,
                            "url": None,
                            "by": None,
                        },
                        "substack": {
                            "status": manual_status,
                            "posted_at": None,
                            "url": None,
                            "by": None,
                        },
                        "medium": {
                            "status": manual_status,
                            "posted_at": None,
                            "url": None,
                            "by": None,
                        },
                    },
                }
            )
            changed_ledger += 1

        if tier >= 2 and not any(entry.get("slug") == slug for entry in queue):
            publish_after = moment + dt.timedelta(hours=24)
            queue.append(
                {
                    "slug": slug,
                    "title": title,
                    "canonical_url": canonical,
                    "published_at": moment.isoformat(),
                    "tier": tier,
                    "devto": {"status": "pending", "publish_after": publish_after.isoformat()},
                    "hashnode": {"status": "pending", "publish_after": publish_after.isoformat()},
                    "medium": {
                        "status": "skipped",
                        "error": "No MEDIUM_INTEGRATION_TOKEN; Medium API cross-posting retired.",
                    },
                }
            )
            changed_queue += 1

    print(f"ledger additions: {changed_ledger}; queue additions: {changed_queue}")
    if args.apply:
        atomic_write(LEDGER, ledger)
        atomic_write(QUEUE, queue)
    else:
        print("dry run; pass --apply to write runtime state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
