#!/usr/bin/env python3
"""Repair published Dev.to articles that show the producer's JSON-LD block as escaped text.

Reads every article of the authenticated account (GET /api/articles/me/all), finds bodies that
still contain a <script ...>...</script> block, strips it with the same helper the cross-post
scripts now use, and (only with --apply) PUTs the cleaned body back. Nothing else about the
article is touched: title, tags, canonical_url, published state and description are not sent,
so Dev.to keeps them. Dry run by default; prints one line per affected article and a summary.
Receipts never include the API key or article bodies.

  DEVTO_API_KEY=... devto-strip-jsonld-repair.py            # dry run
  DEVTO_API_KEY=... devto-strip-jsonld-repair.py --apply    # rewrite the affected bodies

Exit 0 on success (including "nothing to repair"), 1 on an API failure, 64 without a key.
Bead startaitools-7l2.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
STRIPPER = HERE.parents[1] / ".claude/skills/blog-backfill/scripts/strip-script-blocks.py"
API = "https://dev.to/api"


def load_stripper():
    spec = importlib.util.spec_from_file_location("strip_script_blocks", STRIPPER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_script_blocks


def request(method: str, path: str, key: str, payload: dict | None = None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"{API}{path}", data=data, method=method,
        headers={"api-key": key, "Content-Type": "application/json",
                 "User-Agent": "startaitools-devto-repair/1.0"},
    )
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(5 * attempt)
                continue
            raise


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="PUT the cleaned bodies (default: dry run)")
    ap.add_argument("--per-page", type=int, default=100)
    args = ap.parse_args()
    key = os.environ.get("DEVTO_API_KEY", "")
    if not key:
        print("DEVTO_API_KEY is not set", file=sys.stderr)
        return 64
    strip = load_stripper()
    affected, repaired, page = [], 0, 1
    try:
        while True:
            batch = request("GET", f"/articles/me/all?page={page}&per_page={args.per_page}", key)
            if not batch:
                break
            for article in batch:
                body = article.get("body_markdown") or ""
                cleaned, count = strip(body)
                if count:
                    affected.append((article["id"], article.get("published_at", "")[:10],
                                     article.get("url", ""), count))
                    if args.apply:
                        request("PUT", f"/articles/{article['id']}", key,
                                {"article": {"body_markdown": cleaned}})
                        repaired += 1
                        time.sleep(1.2)   # Dev.to write rate limit
            if len(batch) < args.per_page:
                break
            page += 1
            time.sleep(0.5)
    except urllib.error.HTTPError as exc:
        print(f"Dev.to API HTTP {exc.code} on {exc.url}", file=sys.stderr)
        return 1
    verb = "repaired" if args.apply else "would repair"
    for art_id, date, url, count in affected:
        print(f"{verb} {date} id={art_id} blocks={count} {url}")
    done = repaired if args.apply else len(affected)
    summary = "repaired" if args.apply else "dry run"
    print(f"{summary}: {done} of {len(affected)} affected article(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
