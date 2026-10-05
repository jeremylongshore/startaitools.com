#!/usr/bin/env python3
"""Count estate activity for one time window with one documented method (E06-T01).

The monthly retrospective used to count commits on each checkout's local HEAD across the
top-level project directories. That lens undercounts checkouts nobody pulled, double-counts
two clones of the same repository, and missed the nested canonical blog checkout. This script
replaces it with one repeatable method:

1. Discover git checkouts under --root to --max-depth. A directory whose ``.git`` is a FILE is
   a linked worktree of another checkout and is excluded (its commits are the main checkout's).
2. Resolve each checkout's ``origin`` remote to an identity ``owner/repo`` (lowercase).
   No origin: excluded. Owner outside --owner (default: the two estate owners): excluded as
   third-party; contributions upstream are a known gap, not counted here.
3. Deduplicate by identity. The canonical checkout is the one whose counting ref carries the
   newest commit; ties go to the shorter path. The others are listed as duplicates.
4. Count on the remote default branch (``origin/HEAD``, else ``origin/main``/``origin/master``),
   never on local HEAD. --fetch refreshes it first; without --fetch the age of the last fetch is
   reported and a checkout older than 24 h is flagged ``stale-fetch``. A checkout with no remote
   default ref falls back to local HEAD and is flagged ``local-head``.
5. The window is half-open [since, until) in the --tz offset and filters on COMMITTER date
   (when the commit landed on the branch). Counts: all, merges, non-merge, and non-merge
   commits whose author name or email matches --author (bots and upstream authors excluded).
6. --github adds merged PRs (by mergedAt) and published non-draft releases (by publishedAt) per
   identity, and lists owned repositories pushed in the window that have NO local checkout,
   which is the coverage gap a local-only count can never see.

Output is JSON (sorted, stable) to stdout or --json; --markdown writes a short summary.
Read-only: the only write to any checkout is ``git fetch`` when --fetch is given.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

METHOD_VERSION = "estate-activity/1"
DEFAULT_OWNERS = ("jeremylongshore", "intent-solutions-io")
DEFAULT_AUTHORS = ("jeremylongshore", "Jeremy Longshore", "intentsolutions.io")
SKIP_DIRS = {"node_modules", ".worktrees", ".venv", "venv", "__pycache__", ".cache"}
STALE_FETCH_HOURS = 24


def git(repo: Path, *args: str, check: bool = True) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=False
    )
    if check and out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {repo}: {out.stderr.strip()}")
    return out.stdout.strip() if out.returncode == 0 else ""


def identity_from_url(url: str) -> str | None:
    """Normalize a git remote URL to ``owner/repo`` (lowercase), or None if unparseable."""
    url = url.strip()
    m = re.search(r"[:/]([^/:]+)/([^/]+?)(?:\.git)?/?$", url)
    if not m:
        return None
    return f"{m.group(1)}/{m.group(2)}".lower()


def discover(root: Path, max_depth: int) -> tuple[list[Path], list[dict]]:
    """Return (checkouts with a .git directory, excluded linked worktrees)."""
    checkouts: list[Path] = []
    worktrees: list[dict] = []
    root = root.resolve()

    def walk(d: Path, depth: int) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(d.iterdir())
        except OSError:
            return
        dotgit = d / ".git"
        if d != root and dotgit.is_dir():
            checkouts.append(d)
        elif d != root and dotgit.is_file():
            worktrees.append({"path": str(d), "reason": "linked-worktree"})
        for e in entries:
            if e.is_dir() and not e.is_symlink() and e.name not in SKIP_DIRS and e.name != ".git":
                walk(e, depth + 1)

    walk(root, 0)
    return checkouts, worktrees


def counting_ref(repo: Path) -> tuple[str, bool]:
    """Return (ref, is_local_head_fallback)."""
    head = git(repo, "symbolic-ref", "-q", "refs/remotes/origin/HEAD", check=False)
    if head:
        return head, False
    for cand in ("refs/remotes/origin/main", "refs/remotes/origin/master"):
        if git(repo, "rev-parse", "-q", "--verify", cand, check=False):
            return cand, False
    return "HEAD", True


def fetch_age_hours(repo: Path, now: float) -> float | None:
    gd = git(repo, "rev-parse", "--absolute-git-dir", check=False)
    if not gd:
        return None
    fh = Path(gd) / "FETCH_HEAD"
    if not fh.exists():
        return None
    return round((now - fh.stat().st_mtime) / 3600, 1)


def count_commits(repo: Path, ref: str, since: str, until: str, authors: tuple[str, ...]) -> dict:
    fmt = "%H%x09%P%x09%an%x09%ae%x09%cI"
    out = git(repo, "log", ref, f"--since={since}", f"--until={until}", f"--format={fmt}",
              check=False)
    since_dt, until_dt = datetime.fromisoformat(since), datetime.fromisoformat(until)
    total = merges = nonmerge = authored = 0
    lowered = {a.lower() for a in authors}
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 5:
            continue
        _sha, parents, name, email, cdate = parts
        # git's --until is inclusive; enforce the half-open window exactly.
        when = datetime.fromisoformat(cdate)
        if not (since_dt <= when < until_dt):
            continue
        total += 1
        if len(parents.split()) > 1:
            merges += 1
            continue
        nonmerge += 1
        if name.lower() in lowered or email.lower() in lowered or any(
            a in email.lower() for a in lowered if "." in a
        ):
            authored += 1
    return {"commits": total, "merges": merges, "non_merge": nonmerge,
            "authored_non_merge": authored}


def head_date(repo: Path, ref: str) -> str:
    return git(repo, "log", "-1", "--format=%cI", ref, check=False)


def gh_json(args: list[str]) -> object | None:
    out = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if out.returncode != 0:
        return None
    try:
        return json.loads(out.stdout or "null")
    except json.JSONDecodeError:
        return None


def in_window(ts: str | None, lo: datetime, hi: datetime) -> bool:
    if not ts:
        return False
    when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return lo <= when < hi


def github_counts(ident: str, lo: datetime, hi: datetime) -> dict:
    day_lo = (lo - timedelta(days=1)).date().isoformat()
    day_hi = (hi + timedelta(days=1)).date().isoformat()
    prs = gh_json(["pr", "list", "-R", ident, "--state", "merged", "--limit", "2000",
                   "--search", f"merged:{day_lo}..{day_hi}",
                   "--json", "number,mergedAt,author"])
    rels = gh_json(["release", "list", "-R", ident, "--limit", "1000",
                    "--json", "tagName,publishedAt,isDraft"])
    if prs is None and rels is None:
        return {"github": "unresolved"}
    merged = [p for p in (prs or []) if in_window(p.get("mergedAt"), lo, hi)]
    bots = [p for p in merged if "dependabot" in ((p.get("author") or {}).get("login") or "")]
    published = [r for r in (rels or []) if not r.get("isDraft")
                 and in_window(r.get("publishedAt"), lo, hi)]
    return {"github": "ok", "prs_merged": len(merged), "prs_merged_excl_dependabot":
            len(merged) - len(bots), "releases": len(published)}


def uncloned_active(owners: tuple[str, ...], have: set[str], lo: datetime) -> list[dict]:
    rows = []
    for owner in owners:
        repos = gh_json(["repo", "list", owner, "--limit", "2000",
                         "--json", "nameWithOwner,pushedAt,isFork,isArchived"]) or []
        for r in repos:
            ident = r["nameWithOwner"].lower()
            if ident in have or not r.get("pushedAt"):
                continue
            if datetime.fromisoformat(r["pushedAt"].replace("Z", "+00:00")) >= lo:
                rows.append({"identity": ident, "pushed_at": r["pushedAt"],
                             "fork": r.get("isFork", False)})
    return sorted(rows, key=lambda r: r["identity"])


def run(args: argparse.Namespace) -> dict:
    tz = timezone(timedelta(hours=args.tz_hours))
    lo = datetime.fromisoformat(args.since).replace(tzinfo=tz)
    hi = datetime.fromisoformat(args.until).replace(tzinfo=tz)
    since, until = lo.isoformat(), hi.isoformat()
    now = time.time()
    root = Path(os.path.expanduser(args.root))
    checkouts, worktrees = discover(root, args.max_depth)
    for extra in args.extra or []:
        e = Path(os.path.expanduser(extra)).resolve()
        if (e / ".git").is_dir() and e not in checkouts:
            checkouts.append(e)
    owners = tuple(o.lower() for o in args.owner)

    excluded: list[dict] = list(worktrees)
    candidates: dict[str, list[dict]] = {}
    for co in checkouts:
        url = git(co, "remote", "get-url", "origin", check=False)
        ident = identity_from_url(url) if url else None
        if not ident:
            excluded.append({"path": str(co), "reason": "no-origin-remote"})
            continue
        if ident.split("/")[0] not in owners:
            excluded.append({"path": str(co), "identity": ident, "reason": "third-party"})
            continue
        if args.fetch:
            git(co, "fetch", "--quiet", "origin", check=False)
        ref, local = counting_ref(co)
        candidates.setdefault(ident, []).append(
            {"path": str(co), "ref": ref, "local_head": local, "tip": head_date(co, ref)})

    rows = []
    for ident in sorted(candidates):
        group = sorted(candidates[ident], key=lambda c: (c["tip"] or "", -len(c["path"])),
                       reverse=True)
        canon = group[0]
        for dup in group[1:]:
            excluded.append({"path": dup["path"], "identity": ident, "reason": "duplicate",
                             "duplicate_of": canon["path"], "tip": dup["tip"]})
        repo = Path(canon["path"])
        flags = []
        age = fetch_age_hours(repo, now)
        if canon["local_head"]:
            flags.append("local-head")
        elif not args.fetch and (age is None or age > STALE_FETCH_HOURS):
            flags.append("stale-fetch")
        row = {"identity": ident, "path": canon["path"], "ref": canon["ref"],
               "tip": canon["tip"], "fetch_age_hours": age, "flags": flags,
               **count_commits(repo, canon["ref"], since, until, tuple(args.author))}
        if args.github:
            row.update(github_counts(ident, lo.astimezone(UTC), hi.astimezone(UTC)))
        rows.append(row)

    keys = ("commits", "merges", "non_merge", "authored_non_merge", "prs_merged",
            "prs_merged_excl_dependabot", "releases")
    totals = {k: sum(r.get(k, 0) for r in rows) for k in keys if any(k in r for r in rows)}
    totals["repos_counted"] = len(rows)
    totals["repos_active"] = sum(1 for r in rows if r["commits"] > 0)
    result = {
        "method": METHOD_VERSION,
        "window": {"since": since, "until": until, "half_open": True, "date_field": "committer"},
        "root": str(root), "extra": list(args.extra or []), "max_depth": args.max_depth,
        "owners": list(owners),
        "authors": list(args.author), "fetched": bool(args.fetch),
        "totals": totals, "repos": rows,
        "excluded": sorted(excluded, key=lambda e: (e["reason"], e["path"])),
        "coverage_gaps": [
            "commits on branches never merged to the default branch are not counted",
            "contributions to third-party repositories are not counted (see excluded)",
            "a checkout counted without --fetch can trail its remote (see stale-fetch flags)",
            "owned repositories with no local checkout are listed only with --github",
        ],
    }
    if args.github:
        result["uncloned_active"] = uncloned_active(owners, set(candidates), lo.astimezone(UTC))
    return result


def markdown(res: dict) -> str:
    t = res["totals"]
    w = res["window"]
    lines = [f"# Estate activity ({res['method']})", "",
             f"Window [{w['since']}, {w['until']}) on {w['date_field']} date; "
             f"fetched first: {res['fetched']}.", "",
             "| Measure | Value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in t.items()]
    reasons: dict[str, int] = {}
    for e in res["excluded"]:
        reasons[e["reason"]] = reasons.get(e["reason"], 0) + 1
    lines += ["", "Excluded: " + ", ".join(f"{k} {v}" for k, v in sorted(reasons.items())), ""]
    flagged = [r for r in res["repos"] if r["flags"]]
    lines.append(f"Flagged checkouts: {len(flagged)} "
                 f"({', '.join(sorted({f for r in flagged for f in r['flags']})) or 'none'}).")
    if "uncloned_active" in res:
        lines.append(f"Owned repositories pushed in window with no local checkout: "
                     f"{len(res['uncloned_active'])}.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--since", required=True, help="window start, YYYY-MM-DD[THH:MM] local")
    p.add_argument("--until", required=True, help="window end (exclusive), same format")
    p.add_argument("--tz-hours", type=int, default=-6, help="UTC offset of the window (default -6)")
    p.add_argument("--root", default="~/000-projects")
    p.add_argument("--max-depth", type=int, default=3)
    p.add_argument("--owner", action="append", default=None)
    p.add_argument("--author", action="append", default=None)
    p.add_argument("--extra", action="append", default=None,
                   help="an additional checkout outside --root (repeatable)")
    p.add_argument("--fetch", action="store_true", help="git fetch origin in each checkout first")
    p.add_argument("--github", action="store_true", help="add PR, release and uncloned counts")
    p.add_argument("--json", help="write JSON here instead of stdout")
    p.add_argument("--markdown", help="also write a short Markdown summary here")
    args = p.parse_args(argv)
    args.owner = args.owner or list(DEFAULT_OWNERS)
    args.author = args.author or list(DEFAULT_AUTHORS)
    res = run(args)
    text = json.dumps(res, indent=2, sort_keys=True) + "\n"
    if args.json:
        Path(args.json).write_text(text)
    else:
        sys.stdout.write(text)
    if args.markdown:
        Path(args.markdown).write_text(markdown(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
