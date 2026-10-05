#!/usr/bin/env python3
"""Deterministic version, coverage and native-platform header for the weekly rollup.

blog-team-rollup.sh prepends this block to the numeric dashboard, so every
rollup states which definitions produced its numbers:

  * report version + metric dictionary version (and sha) + filter rule version
  * coverage: which sites/fields are unavailable this week, and what Umami
    never observes
  * a one-time baseline-reset note, shown until a sent rollup has carried it
    for the current dictionary version (mark-reset records that)
  * native platform panels (Dev.to) in their own platform units, with the age of
    the observation. They are never added to, or divided by, site sessions.

No network, no LLM. A missing or failed input renders as "unavailable", never 0.

Usage:
  rollup-report-header.py render --metrics M.json --date YYYY-MM-DD --out H.html
      [--native .native-metrics.jsonl] [--reset-marker PATH] [--dictionary PATH]
  rollup-report-header.py mark-reset --reset-marker PATH [--dictionary PATH]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from datetime import date, datetime
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT_NAME = "weekly growth rollup"
REPORT_VERSION = "2.0.0"  # 2.0.0: first version stamped against metric dictionary 1.x
NATIVE_DELTA_DAYS = 7

_spec = importlib.util.spec_from_file_location("metric_dictionary", HERE / "metric_dictionary.py")
md = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(md)

CELL = "padding:6px 8px;border-bottom:1px solid #e2e8f0;text-align:left"


def _fmt(value: object) -> str:
    if value is None:
        return "unknown"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def coverage(metrics: dict) -> dict:
    sites = metrics.get("sites") or []
    filtered_missing = sorted(
        s.get("domain", "?")
        for s in sites
        for period in ("week", "prior_week")
        if not isinstance((s.get("filtered") or {}).get(period), dict)
        or "unavailable" in (s.get("filtered") or {}).get(period, {})
    )
    referral_unavailable = 0
    referral_untagged = 0
    for s in sites:
        for row in (s.get("referrals") or {}).get("week") or []:
            text = json.dumps(row)
            if "unavailable" in text:
                referral_unavailable += 1
            if "untagged" in text:
                referral_untagged += 1
    return {
        "sites": len(sites),
        "filtered_unavailable": sorted(set(filtered_missing)),
        "referral_unavailable": referral_unavailable,
        "referral_untagged": referral_untagged,
    }


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def native_panel(path: Path | None, report_day: date) -> dict:
    """Summarize the native-metrics log. Every gap is a named state, never 0."""
    if path is None or not path.is_file():
        return {"status": "unavailable", "reason": "native metrics log not found"}
    runs: dict[str, list[dict]] = defaultdict(list)
    failures: list[dict] = []
    others: dict[str, dict] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return {"status": "unavailable", "reason": f"log unreadable ({type(exc).__name__})"}
    for line in lines:
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if not isinstance(rec, dict):
            continue
        observed = rec.get("observed_at")
        if not observed or (_parse_ts(observed) or datetime.max).date() >= report_day:
            continue  # only observations before the report date's 00:00 boundary
        if rec.get("surface") == "devto":
            if rec.get("status") == "ok":
                runs[observed].append(rec)
            elif rec.get("status") == "ok_empty":
                runs.setdefault(observed, [])
            else:
                failures.append(rec)
        elif rec.get("source") == "registry":
            others[rec.get("surface", "?")] = rec
    result: dict = {"others": [others[k] for k in sorted(others)]}
    if not runs:
        result.update(status="unavailable", reason="no successful Dev.to observation")
        return result
    latest_at = max(runs)
    latest = runs[latest_at]
    latest_day = _parse_ts(latest_at).date()
    newer_failures = [f for f in failures if f.get("observed_at", "") > latest_at]

    def total(rows: list[dict], field: str) -> int | None:
        values = [r.get(field) for r in rows]
        if any(not isinstance(v, int) for v in values):
            return None  # a null field is unknown; a partial sum would understate
        return sum(values)

    earlier = [
        k for k in runs if (latest_day - _parse_ts(k).date()).days >= NATIVE_DELTA_DAYS
    ]
    delta: dict = {"status": "n/a", "reason": f"no observation {NATIVE_DELTA_DAYS}+ days older"}
    if earlier:
        base_at = max(earlier)
        base = {r.get("article_id"): r for r in runs[base_at]}
        paired = [
            (r, base[r.get("article_id")]) for r in latest if r.get("article_id") in base
        ]
        diffs = [
            a.get("page_views") - b.get("page_views")
            for a, b in paired
            if isinstance(a.get("page_views"), int) and isinstance(b.get("page_views"), int)
        ]
        if paired and len(diffs) == len(paired):
            delta = {
                "status": "measured",
                "since": base_at,
                "page_views": sum(diffs),
                "articles": len(paired),
            }
        else:
            delta = {"status": "unknown", "reason": "page views missing for a paired article"}
    result.update(
        status="measured",
        observed_at=latest_at,
        age_days=(report_day - latest_day).days,
        articles=len(latest),
        page_views=total(latest, "page_views"),
        reactions=total(latest, "reactions"),
        comments=total(latest, "comments"),
        delta=delta,
        newer_failures=[
            {"observed_at": f.get("observed_at"), "status": f.get("status")} for f in newer_failures
        ],
    )
    return result


def reset_pending(marker: Path | None, version: str) -> bool:
    if marker is None:
        return True
    try:
        return marker.read_text(encoding="utf-8").strip() != version
    except OSError:
        return True


def render(metrics: dict, data: dict, report_day: date, native: dict, show_reset: bool) -> str:
    rule = (metrics.get("automation_rule") or {}).get("version") or "unavailable"
    dict_rule = data["filter"]["rule_version"]
    week = (metrics.get("windows") or {}).get("week") or {}
    window = (
        f"[{escape(week.get('start', '?')[:10])}, {escape(week.get('end_exclusive', '?')[:10])})"
        if week
        else "unavailable"
    )
    h = ['<div style="font-family:Arial,sans-serif;color:#17253b;border:1px solid #cbd5e1;'
         'padding:10px 14px;margin-bottom:14px">']
    h.append(
        f"<p style=\"margin:0 0 6px\"><b>Report version:</b> {REPORT_NAME} v{REPORT_VERSION} · "
        f"metric dictionary v{escape(data['version'])} (sha256 {escape(data['_sha256'][:12])}) · "
        f"traffic filter {escape(rule)} · week {window} "
        f"{escape(str(metrics.get('timezone') or ''))}</p>"
    )
    if rule != dict_rule:
        h.append(
            f"<p style=\"margin:0 0 6px\"><b>Filter mismatch:</b> this report used filter "
            f"{escape(rule)}, the dictionary defines {escape(dict_rule)}. Treat every comparison "
            "with an earlier report or baseline as n/a.</p>"
        )
    cov = coverage(metrics)
    missing = ", ".join(cov["filtered_unavailable"]) or "none"
    h.append(
        "<p style=\"margin:0 0 6px\"><b>Coverage:</b> "
        f"{cov['sites']} sites reported. Filtered tier unavailable for: {escape(missing)}. "
        f"Referral rows unavailable: {cov['referral_unavailable']}; untagged (unmeasurable): "
        f"{cov['referral_untagged']}. Not observed by Umami at all: native readers who never "
        "click through, readers whose blockers drop the tracker, identity across months. "
        "Units: sessions are not people; clicks are attempts, not outcomes; unavailable, "
        "unknown, n/a and 0 are different values.</p>"
    )
    if show_reset:
        h.append(
            "<p style=\"margin:0 0 6px;background:#fff7e6;padding:6px\"><b>Baseline reset "
            f"(shown once):</b> from this report the numbers follow metric dictionary "
            f"v{escape(data['version'])} and filter {escape(dict_rule)}. Rollups sent before this "
            "one used earlier filter versions and unpaired comparisons, so their figures are not "
            "comparable with these. A comparison whose prior window predates verified collection, "
            "or whose site set or cohort changed, now reads n/a instead of a percentage. Dev.to "
            "numbers are reported in their own panel and units below and are never summed with "
            "site sessions.</p>"
        )
    h.append(render_native(native, report_day))
    h.append("</div>")
    return "".join(h)


def render_native(native: dict, report_day: date) -> str:
    h = ["<h3 style=\"margin:8px 0 4px\">Native platform panel (own units; never added to "
         "site sessions)</h3>"]
    rows = []
    if native.get("status") != "measured":
        rows.append(("Dev.to", "unavailable", escape(native.get("reason", "unavailable"))))
    else:
        d = native["delta"]
        if d["status"] == "measured":
            delta = (f"+{d['page_views']:,} Dev.to page views since {escape(d['since'][:10])} "
                     f"({d['articles']} articles in both observations)")
        else:
            delta = f"{d['status']}: {escape(d.get('reason', ''))}"
        stale = ""
        if native.get("newer_failures"):
            last = native["newer_failures"][-1]
            stale = (f" Latest collection attempt {escape(str(last['observed_at']))} failed "
                     f"({escape(str(last['status']))}); figures are from the last success.")
        rows.append((
            "Dev.to",
            f"{_fmt(native['page_views'])} page views · {_fmt(native['reactions'])} reactions · "
            f"{_fmt(native['comments'])} comments across {native['articles']} articles "
            "(lifetime, platform-reported)",
            f"Observed {escape(native['observed_at'])} (age {native['age_days']} days). "
            f"7-day change: {delta}.{stale}",
        ))
    for other in native.get("others", []):
        rows.append((
            escape(str(other.get("surface", "?"))),
            f"unknown ({escape(str(other.get('status', '')))})",
            escape(str(other.get("note", ""))) + " Not 0 readers: nothing records them.",
        ))
    h.append('<table style="border-collapse:collapse;width:100%"><tr>'
             f'<th style="{CELL}">Surface</th><th style="{CELL}">Value (platform unit)</th>'
             f'<th style="{CELL}">Age and notes</th></tr>')
    for surface, value, note in rows:
        h.append(f'<tr><td style="{CELL}">{surface}</td><td style="{CELL}">{value}</td>'
                 f'<td style="{CELL}">{note}</td></tr>')
    h.append("</table>")
    return "".join(h)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("render")
    r.add_argument("--metrics", type=Path, required=True)
    r.add_argument("--date", required=True)
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--native", type=Path, default=None)
    r.add_argument("--reset-marker", type=Path, default=None)
    r.add_argument("--dictionary", type=Path, default=None)
    m = sub.add_parser("mark-reset")
    m.add_argument("--reset-marker", type=Path, required=True)
    m.add_argument("--dictionary", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        data = md.load(args.dictionary)
    except md.DictionaryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.command == "mark-reset":
        args.reset_marker.write_text(data["version"] + "\n", encoding="utf-8")
        print(f"baseline reset recorded as communicated for dictionary v{data['version']}")
        return 0
    try:
        report_day = date.fromisoformat(args.date)
        metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    native = native_panel(args.native, report_day)
    show = reset_pending(args.reset_marker, data["version"])
    args.out.write_text(render(metrics, data, report_day, native, show), encoding="utf-8")
    print(f"report header: {REPORT_NAME} v{REPORT_VERSION}; {md.stamp(data)}; "
          f"baseline reset note {'shown' if show else 'already communicated'}; "
          f"native panel {native.get('status')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
