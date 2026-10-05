#!/usr/bin/env python3
"""next-topics.py: deterministic manager for the analytics-driven topic queue.

Thread D Phase 1 (2026-07-16), the front-of-funnel performance loop:
  Umami content-performance  ->  content-seo agent (LLM)  ->  THIS queue  ->  writers

The LLM half only PRODUCES candidate objects into a staging file. This script is
the deterministic half: it validates, assigns ids, dedups, ranks by score, and
appends to the real queue, so a bad model run can never corrupt it (same
produce/land split the blog pipeline uses everywhere else).

Queue file: .next-topics.jsonl at the repo root (gitignored, transient). Each
line is one candidate:
  {
    "id": "nt-YYYYMMDD-NNN",        # assigned on ingest
    "generated_at": "ISO8601",       # assigned on ingest
    "topic": "short human title",    # required
    "slug_hint": "kebab-slug",       # required, the dedup key
    "angle": "the specific thesis / angle",
    "rationale": "why now, grounded in real traffic numbers",
    "source_signals": { ... },       # top performers / gap / cluster that drove it
    "score": 0.0-1.0,                # required, ranking priority
    "target_tier": 1-4,              # suggested tier (4 => blog-research-article)
    "status": "open",                # open | consumed | merged
    "consumed_by": null,             # post slug, once written
    "consumed_at": null
  }

Clusters (2026-10-05). Repeated near-duplicate rows on one problem are merged into
ONE cluster row by `cluster --spec`. The cluster row carries:
    "kind": "cluster",
    "merged_from": [ids],            # every row folded in, kept in the file
    "children": [ {"key", "question", "source_ids", "partial_source_ids",
                   "status", "consumed_by", "consumed_at", "url"} ]
Each merged row keeps all its fields and gets "status": "merged" and
"merged_into": <cluster id>, so its source evidence is never lost. A child is
consumed one at a time, only with the published URL (`consume <cluster> --child K
--by SLUG --url URL`); the cluster itself turns consumed when every child is.

Subcommands:
  ingest [--staging PATH]   validate staged candidates, dedup vs open items, append
  top [--tier N] [--json]   print the single highest-score OPEN candidate
  list [--all]              list open (or all) candidates, ranked
  consume <id|slug> --by S  mark an item consumed by post slug S
          [--child K --url U]   for a cluster: consume one child, URL required
  cluster --spec PATH       merge rows into one cluster row (see Clusters)
  validate                  validate the whole queue, non-zero exit on any bad line

Never corrupts the queue: ingest writes atomically (temp + replace). Read paths
never raise on a missing queue (they treat it as empty).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent  # scripts/blog/ -> repo root
QUEUE = REPO / ".next-topics.jsonl"
STAGING = REPO / ".next-topics.staging.jsonl"

REQUIRED = ("topic", "slug_hint", "score")
STATUSES = ("open", "consumed", "merged")
CHILD_STATUSES = ("open", "consumed")


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise ValueError(f"{path.name}:{i}: invalid JSON ({e})") from e
    return out


def _write_atomic(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def _valid_candidate(c: dict) -> str | None:
    for k in REQUIRED:
        if k not in c or c[k] in (None, ""):
            return f"missing required field '{k}'"
    try:
        s = float(c["score"])
    except (TypeError, ValueError):
        return "score is not a number"
    if not 0.0 <= s <= 1.0:
        return "score out of range 0.0-1.0"
    return None


def cmd_ingest(args) -> int:
    staging = Path(args.staging) if args.staging else STAGING
    try:
        staged = _read(staging)
    except ValueError as e:
        print(f"ingest: {e}", file=sys.stderr)
        return 1
    if not staged:
        print("ingest: no staged candidates (nothing to do)")
        return 0

    existing = _read(QUEUE)
    # Merged rows still block re-ingest of the exact same slug: the cluster owns it.
    open_slugs = {_slug(r.get("slug_hint", "")) for r in existing
                  if r.get("status") in ("open", "merged")}

    today = datetime.now(UTC).strftime("%Y%m%d")
    seq = 1 + sum(1 for r in existing if r.get("id", "").startswith(f"nt-{today}-"))

    added, skipped = [], []
    for c in staged:
        err = _valid_candidate(c)
        if err:
            skipped.append((c.get("topic", "?"), err))
            continue
        sl = _slug(c["slug_hint"])
        if sl in open_slugs:
            skipped.append((c.get("topic", "?"), "duplicate of an open item"))
            continue
        rec = {
            "id": f"nt-{today}-{seq:03d}",
            "generated_at": _now(),
            "topic": c["topic"],
            "slug_hint": sl,
            "angle": c.get("angle", ""),
            "rationale": c.get("rationale", ""),
            "source_signals": c.get("source_signals", {}),
            "score": round(float(c["score"]), 3),
            "target_tier": int(c.get("target_tier", 2)),
            "status": "open",
            "consumed_by": None,
            "consumed_at": None,
        }
        existing.append(rec)
        open_slugs.add(sl)
        added.append(rec)
        seq += 1

    if added:
        _write_atomic(QUEUE, existing)
    if not args.keep_staging:
        staging.unlink(missing_ok=True)

    print(f"ingest: added {len(added)}, skipped {len(skipped)}")
    for topic, why in skipped:
        print(f"  skipped: {topic!r} ({why})")
    return 0


def _open_ranked(rows: list[dict], tier: int | None = None) -> list[dict]:
    items = [r for r in rows if r.get("status") == "open"]
    if tier is not None:
        items = [r for r in items if int(r.get("target_tier", 2)) == tier]
    return sorted(items, key=lambda r: float(r.get("score", 0)), reverse=True)


def cmd_top(args) -> int:
    ranked = _open_ranked(_read(QUEUE), args.tier)
    if not ranked:
        print("", end="") if args.json else print("(no open topics in the queue)")
        return 0 if not args.json else 3
    top = ranked[0]
    if args.json:
        json.dump(top, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(f"{top['id']}  [score {top['score']}  tier {top['target_tier']}]  {top['topic']}")
        print(f"  slug: {top['slug_hint']}")
        print(f"  angle: {top.get('angle','')}")
        print(f"  why: {top.get('rationale','')}")
    return 0


def cmd_list(args) -> int:
    rows = _read(QUEUE)
    items = rows if args.all else [r for r in rows if r.get("status") == "open"]
    items = sorted(items, key=lambda r: float(r.get("score", 0)), reverse=True)
    if not items:
        print("(queue empty)")
        return 0
    for r in items:
        mark = r.get("status", "open")
        if r.get("kind") == "cluster":
            kids = r.get("children", [])
            done = sum(1 for k in kids if k.get("status") == "consumed")
            mark += f" cluster {done}/{len(kids)}"
        if mark == "merged":
            mark += f" -> {r.get('merged_into')}"
        print(f"{r.get('id','?')}  [{r.get('score','?')} "
              f"t{r.get('target_tier','?')} {mark}]  {r.get('topic','?')}")
    return 0


def cmd_consume(args) -> int:
    rows = _read(QUEUE)
    key = args.item
    keyslug = _slug(key)
    hit = None
    for r in rows:
        if r.get("id") == key or _slug(r.get("slug_hint", "")) == keyslug:
            hit = r
            break
    if not hit:
        print(f"consume: no queue item matching {key!r}", file=sys.stderr)
        return 1
    if hit.get("status") == "merged":
        print(f"consume: {hit['id']} was merged into {hit.get('merged_into')}; "
              f"consume a child of that cluster instead", file=sys.stderr)
        return 1
    if hit.get("kind") == "cluster":
        return _consume_child(rows, hit, args)
    if args.child:
        print(f"consume: {hit['id']} is not a cluster; --child does not apply", file=sys.stderr)
        return 1
    if hit.get("status") == "consumed":
        print(f"consume: {hit['id']} already consumed by {hit.get('consumed_by')}")
        return 0
    hit["status"] = "consumed"
    hit["consumed_by"] = args.by
    hit["consumed_at"] = _now()
    _write_atomic(QUEUE, rows)
    print(f"consume: {hit['id']} -> consumed by {args.by}")
    return 0


def _consume_child(rows: list[dict], cluster: dict, args) -> int:
    """Consume ONE child question of a cluster, only with its published URL."""
    if not args.child or not args.url:
        print(f"consume: {cluster['id']} is a cluster; pass --child KEY and --url "
              f"<published URL> (consume only after verified publication)", file=sys.stderr)
        return 1
    if not re.match(r"^https://", args.url):
        print("consume: --url must be the published https:// URL", file=sys.stderr)
        return 1
    kid = next((k for k in cluster.get("children", []) if k.get("key") == args.child), None)
    if kid is None:
        keys = [k.get("key") for k in cluster.get("children", [])]
        print(f"consume: {cluster['id']} has no child {args.child!r} (children: {keys})",
              file=sys.stderr)
        return 1
    if kid.get("status") == "consumed":
        print(f"consume: {cluster['id']}/{args.child} already consumed by {kid.get('consumed_by')}")
        return 0
    kid.update(status="consumed", consumed_by=args.by, consumed_at=_now(), url=args.url)
    if all(k.get("status") == "consumed" for k in cluster.get("children", [])):
        cluster.update(status="consumed", consumed_by=args.by, consumed_at=_now())
    _write_atomic(QUEUE, rows)
    print(f"consume: {cluster['id']}/{args.child} -> consumed by {args.by} ({args.url})")
    return 0


def _valid_cluster_spec(spec: dict, by_id: dict) -> str | None:
    err = _valid_candidate(spec)
    if err:
        return err
    kids = spec.get("children")
    if not isinstance(kids, list) or not kids:
        return "children must be a non-empty list"
    keys = [k.get("key") for k in kids]
    if any(not k for k in keys) or len(set(keys)) != len(keys):
        return "every child needs a unique non-empty key"
    for k in kids:
        if not k.get("question"):
            return f"child {k.get('key')!r} has no question"
    merged = spec.get("merged_from") or []
    if not merged:
        return "merged_from must list the rows being merged"
    if len(set(merged)) != len(merged):
        return "merged_from has duplicate ids"
    referenced = set(merged)
    for k in kids:
        referenced |= set(k.get("source_ids", [])) | set(k.get("partial_source_ids", []))
    missing = sorted(i for i in referenced if i not in by_id)
    if missing:
        return f"unknown queue ids: {missing}"
    for i in merged:
        if by_id[i].get("status") != "open":
            return f"{i} is {by_id[i].get('status')}, only open rows can be merged"
    for k in kids:
        overlap = set(k.get("partial_source_ids", [])) & set(merged)
        if overlap:
            return (f"child {k['key']!r}: partial sources must stay open, "
                    f"not be merged: {sorted(overlap)}")
    return None


def cmd_cluster(args) -> int:
    """Merge near-duplicate open rows into one cluster row, atomically."""
    try:
        rows = _read(QUEUE)
        spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    except (ValueError, OSError) as e:
        print(f"cluster: {e}", file=sys.stderr)
        return 1
    by_id = {r.get("id"): r for r in rows}
    err = _valid_cluster_spec(spec, by_id)
    if err:
        print(f"cluster: refused: {err}", file=sys.stderr)
        return 1
    today = datetime.now(UTC).strftime("%Y%m%d")
    seq = 1 + sum(1 for r in rows if r.get("id", "").startswith(f"nt-{today}-"))
    cid = f"nt-{today}-{seq:03d}"
    rec = {
        "id": cid,
        "generated_at": _now(),
        "kind": "cluster",
        "topic": spec["topic"],
        "slug_hint": _slug(spec["slug_hint"]),
        "angle": spec.get("angle", ""),
        "rationale": spec.get("rationale", ""),
        "source_signals": spec.get("source_signals", {}),
        "score": round(float(spec["score"]), 3),
        "target_tier": int(spec.get("target_tier", 2)),
        "status": "open",
        "consumed_by": None,
        "consumed_at": None,
        "merged_from": list(spec["merged_from"]),
        "children": [
            {
                "key": k["key"],
                "question": k["question"],
                "source_ids": list(k.get("source_ids", [])),
                "partial_source_ids": list(k.get("partial_source_ids", [])),
                "status": "open",
                "consumed_by": None,
                "consumed_at": None,
                "url": None,
            }
            for k in spec["children"]
        ],
    }
    for i in spec["merged_from"]:
        by_id[i]["status"] = "merged"
        by_id[i]["merged_into"] = cid
    rows.append(rec)
    if args.dry_run:
        json.dump(rec, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        print(f"cluster: dry run, would merge {len(spec['merged_from'])} rows into {cid}")
        return 0
    _write_atomic(QUEUE, rows)
    print(f"cluster: {cid} created with {len(rec['children'])} children; "
          f"merged {len(spec['merged_from'])} rows")
    return 0


def _structural_errors(rows: list[dict]) -> list[str]:
    errs = []
    by_id = {r.get("id"): r for r in rows}
    for r in rows:
        rid = r.get("id", "?")
        st = r.get("status", "open")
        if st not in STATUSES:
            errs.append(f"{rid}: unknown status {st!r}")
        if st == "merged":
            target = by_id.get(r.get("merged_into"))
            if not target or target.get("kind") != "cluster":
                errs.append(f"{rid}: merged_into {r.get('merged_into')!r} is not a cluster row")
            elif rid not in target.get("merged_from", []):
                errs.append(f"{rid}: not listed in {target['id']} merged_from")
        if r.get("kind") == "cluster":
            for i in r.get("merged_from", []):
                if by_id.get(i, {}).get("merged_into") != rid:
                    errs.append(f"{rid}: merged_from {i} does not point back")
            for k in r.get("children", []):
                if k.get("status") not in CHILD_STATUSES:
                    errs.append(f"{rid}/{k.get('key')}: bad child status {k.get('status')!r}")
                if k.get("status") == "consumed" and not k.get("url"):
                    errs.append(f"{rid}/{k.get('key')}: consumed without a published url")
                for i in k.get("source_ids", []) + k.get("partial_source_ids", []):
                    if i not in by_id:
                        errs.append(f"{rid}/{k.get('key')}: unknown source id {i}")
    return errs


def cmd_validate(args) -> int:
    try:
        rows = _read(QUEUE)
    except ValueError as e:
        print(f"validate: {e}", file=sys.stderr)
        return 1
    bad = 0
    for r in rows:
        err = _valid_candidate(r)
        if err:
            print(f"validate: {r.get('id','?')}: {err}", file=sys.stderr)
            bad += 1
    for err in _structural_errors(rows):
        print(f"validate: {err}", file=sys.stderr)
        bad += 1
    n_open = sum(1 for r in rows if r.get("status") == "open")
    print(f"validate: {len(rows)} items ({n_open} open), {bad} invalid")
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("ingest", help="validate + dedup + append staged candidates")
    i.add_argument("--staging", help="staging JSONL path (default .next-topics.staging.jsonl)")
    i.add_argument("--keep-staging", action="store_true", help="do not delete staging after ingest")
    i.set_defaults(func=cmd_ingest)

    t = sub.add_parser("top", help="print the highest-score open candidate")
    t.add_argument("--tier", type=int, help="restrict to a target_tier")
    t.add_argument("--json", action="store_true", help="emit the full JSON object")
    t.set_defaults(func=cmd_top)

    ls = sub.add_parser("list", help="list ranked candidates")
    ls.add_argument("--all", action="store_true", help="include consumed items")
    ls.set_defaults(func=cmd_list)

    c = sub.add_parser("consume", help="mark an item consumed")
    c.add_argument("item", help="queue id or slug_hint")
    c.add_argument("--by", required=True, help="the post slug that consumed it")
    c.add_argument("--child", help="cluster child key to consume")
    c.add_argument("--url", help="published URL (required for a cluster child)")
    c.set_defaults(func=cmd_consume)

    cl = sub.add_parser("cluster", help="merge duplicate rows into one cluster row")
    cl.add_argument("--spec", required=True, help="JSON cluster spec path")
    cl.add_argument("--dry-run", action="store_true", help="print the cluster row, write nothing")
    cl.set_defaults(func=cmd_cluster)

    v = sub.add_parser("validate", help="validate the whole queue")
    v.set_defaults(func=cmd_validate)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
