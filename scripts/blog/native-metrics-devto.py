#!/usr/bin/env python3
"""Read-only collector for platform-native syndication metrics (Layer A).

Dev.to is the one syndication surface with an authenticated API that returns
per-article native numbers: GET /api/articles/me/published (header `api-key`)
carries page_views_count, public_reactions_count and comments_count. This
script reads them and APPENDS one observation per article to a JSONL log.

It never writes to Dev.to, never prints the key, and never turns a failure
into a zero. A missing key, a 401/403 or a network/5xx failure writes ONE
explicit status record (`unavailable` / `auth_failed`) for the run instead of
article rows, so a gap in the log is distinguishable from "nobody read it".

Every other surface is listed in SURFACE_REGISTRY with the reason it has no
collector, and each run appends one status record per such surface. Absence
of data is recorded as absence, never as 0.

Key source, in order: $DEVTO_API_KEY, then the DEVTO_API_KEY line of the
parent blog/.env (the same file post-to-devto.sh and the crosspost sweep
already use). Only that one line is parsed; nothing else is read or exported.

Usage:
  native-metrics-devto.py [--out PATH] [--env-file PATH] [--dry-run]
  native-metrics-devto.py --list-surfaces

Default output: <repo>/.native-metrics.jsonl (gitignored runtime state, beside
.crosspost-queue.json and .blog-syndication-ledger.json).

Proposed schedule (NOT installed): daily 06:15, after the 05:30 crosspost
sweep and before the 06:30 analytics brief:
  15 6 * * * <repo>/scripts/blog/native-metrics-devto.py
Dev.to counts are cumulative lifetime numbers, so consumers derive deltas
between observations; one observation per day is enough. A re-run on a UTC
date that already has a successful Dev.to observation in the log writes
nothing and exits 0 (logged as `skip:` on stderr); --force overrides.

Exit codes: 0 ok, 2 auth_failed, 3 unavailable, 4 usage/output error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / ".native-metrics.jsonl"
DEFAULT_ENV_FILE = REPO.parent / ".env"
API_URL = "https://dev.to/api/articles/me/published"
PER_PAGE = 1000
MAX_PAGES = 20
SOURCE = "devto_api"
USER_AGENT = "startaitools-native-metrics/1 (read-only)"

# Surfaces without a collector, and why. `status` is what each run records.
SURFACE_REGISTRY: dict[str, dict[str, str]] = {
    "devto": {
        "status": "collected",
        "source": SOURCE,
        "note": "Authenticated Forem API: page views, reactions, comments per article.",
    },
    "hashnode": {
        "status": "paid_api",
        "source": "none",
        "note": "Post views need the Hashnode Pro API; not provisioned. Dashboard only.",
    },
    "substack": {
        "status": "unavailable_without_dashboard",
        "source": "none",
        "note": "No public stats API. Public pages show reactions/comments only; "
        "views, opens and subscriber deltas are dashboard-only.",
    },
    "medium": {
        "status": "unavailable_without_dashboard",
        "source": "none",
        "note": "Medium API exposes no stats; views/reads are dashboard-only.",
    },
    "linkedin_company": {
        "status": "unavailable_without_dashboard",
        "source": "none",
        "note": "Page analytics need LinkedIn Marketing API approval; admin dashboard only.",
    },
    "linkedin_personal": {
        "status": "unavailable_without_dashboard",
        "source": "none",
        "note": "No API for member post analytics; in-account only.",
    },
    "x": {
        "status": "unavailable_without_dashboard",
        "source": "none",
        "note": "Post metrics need a paid X API tier (not provisioned); in-account only.",
    },
}

Fetcher = Callable[[str, dict[str, str]], tuple[int, bytes]]


def now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_key(env_file: Path) -> str | None:
    """Return the Dev.to key from env or the single matching .env line."""
    key = os.environ.get("DEVTO_API_KEY", "").strip()
    if key:
        return key
    try:
        lines = env_file.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        line = line.strip()
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if not line.startswith("DEVTO_API_KEY="):
            continue
        value = line.split("=", 1)[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        return value or None
    return None


def http_get(url: str, headers: dict[str, str]) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (fixed https URL)
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""


def status_record(status: str, observed_at: str, **extra: object) -> dict:
    rec: dict[str, object] = {
        "surface": "devto",
        "status": status,
        "observed_at": observed_at,
        "source": SOURCE,
    }
    rec.update(extra)
    return rec


def _count(article: dict, field: str) -> int | None:
    value = article.get(field)
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def article_record(article: dict, observed_at: str) -> dict:
    """One observation. A missing/non-integer metric is null, never 0."""
    return {
        "surface": "devto",
        "status": "ok",
        "article_id": article.get("id"),
        "url": article.get("url"),
        "canonical_url": article.get("canonical_url"),
        "published_at": article.get("published_at"),
        "page_views": _count(article, "page_views_count"),
        "reactions": _count(article, "public_reactions_count"),
        "comments": _count(article, "comments_count"),
        "observed_at": observed_at,
        "source": SOURCE,
    }


def collect_devto(key: str | None, fetch: Fetcher, observed_at: str) -> tuple[list[dict], int]:
    """Return (records, exit_code). Records are either all `ok` rows or one status row."""
    if not key:
        return [status_record("unavailable", observed_at, reason="missing_api_key")], 3
    headers = {"api-key": key, "Accept": "application/json", "User-Agent": USER_AGENT}
    articles: list[dict] = []
    for page in range(1, MAX_PAGES + 1):
        url = f"{API_URL}?per_page={PER_PAGE}&page={page}"
        try:
            code, body = fetch(url, headers)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            reason = f"network_error:{type(exc).__name__}"
            return [status_record("unavailable", observed_at, reason=reason)], 3
        if code in (401, 403):
            return [status_record("auth_failed", observed_at, http_status=code)], 2
        if code != 200:
            return [status_record("unavailable", observed_at, http_status=code)], 3
        try:
            batch = json.loads(body)
        except ValueError:
            return [status_record("unavailable", observed_at, reason="invalid_json")], 3
        if not isinstance(batch, list):
            return [status_record("unavailable", observed_at, reason="unexpected_shape")], 3
        articles.extend(a for a in batch if isinstance(a, dict))
        if len(batch) < PER_PAGE:
            break
    else:
        return [status_record("unavailable", observed_at, reason="page_limit_reached")], 3
    if not articles:
        # An authenticated empty list is a real answer, but say so explicitly.
        return [status_record("ok_empty", observed_at, articles=0)], 0
    return [article_record(a, observed_at) for a in articles], 0


def registry_records(observed_at: str) -> list[dict]:
    return [
        {
            "surface": name,
            "status": meta["status"],
            "note": meta["note"],
            "observed_at": observed_at,
            "source": "registry",
        }
        for name, meta in SURFACE_REGISTRY.items()
        if meta["status"] != "collected"
    ]


def append_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")


SUCCESS_STATUSES = ("ok", "ok_empty")


def already_observed(path: Path, day: str) -> bool:
    """True when the log already holds a successful Dev.to row for this UTC day.

    Failure rows do not count, so a failed day is retried. An unreadable or
    malformed line is ignored rather than trusted.
    """
    if not path.is_file():
        return False
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            if (
                isinstance(rec, dict)
                and rec.get("surface") == "devto"
                and rec.get("status") in SUCCESS_STATUSES
                and str(rec.get("observed_at", ""))[:10] == day
            ):
                return True
    return False


def summarize(records: list[dict]) -> dict:
    rows = [r for r in records if r.get("surface") == "devto" and r.get("status") == "ok"]

    def total(field: str) -> int | None:
        vals = [r[field] for r in rows if r.get(field) is not None]
        return sum(vals) if vals else None

    status = rows[0]["status"] if rows else next(
        (r["status"] for r in records if r.get("surface") == "devto"), "unknown"
    )
    return {
        "devto_status": status,
        "articles": len(rows),
        "page_views_total": total("page_views"),
        "reactions_total": total("reactions"),
        "comments_total": total("comments"),
    }


def main(argv: list[str] | None = None, fetch: Fetcher = http_get) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    ap.add_argument("--dry-run", action="store_true", help="collect and summarize, write nothing")
    ap.add_argument("--list-surfaces", action="store_true")
    ap.add_argument("--force", action="store_true", help="write even if today is already observed")
    args = ap.parse_args(argv)

    if args.list_surfaces:
        print(json.dumps(SURFACE_REGISTRY, indent=2, sort_keys=True))
        return 0

    observed_at = now_iso()
    day = observed_at[:10]
    if not args.dry_run and not args.force:
        try:
            done = already_observed(args.out, day)
        except OSError as exc:
            print(f"error: cannot read {args.out}: {exc}", file=sys.stderr)
            return 4
        if done:
            print(
                f"skip: {args.out} already has a Dev.to observation for {day} (UTC);"
                " --force to add another",
                file=sys.stderr,
            )
            skipped = {"devto_status": "skipped_already_observed", "day": day}
            print(json.dumps(skipped, sort_keys=True))
            return 0
    records, code = collect_devto(read_key(args.env_file), fetch, observed_at)
    records += registry_records(observed_at)
    if not args.dry_run:
        try:
            append_jsonl(args.out, records)
        except OSError as exc:
            print(f"error: cannot append to {args.out}: {exc}", file=sys.stderr)
            return 4
    print(json.dumps(summarize(records), sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
