"""Which recent dates still have no post, and may another attempt be spent on them?

Repair and failover save a night when one provider or one attempt fails. They cannot save
a night when everything is down. Catch-up does: every run, after its own date, looks back a
few days, finds dates with no post on the deploy branch, and tries them again, quietly.

This module only PLANS and RECORDS. It never produces, never touches the working tree and
reads git through one `git grep` against a ref. Attempts per date are capped so a date that
cannot be written (no activity, a poisoned input) stops costing tokens; when the cap is
reached the date is reported ONCE as given up, which is the only moment a human is needed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

POSTS = "content/posts"


DRAFT = r"^draft\s*[=:]\s*[\"']?true"


def _grep(repo: Path, ref: str, pattern: str, *flags: str) -> str:
    done = subprocess.run(
        ["git", "-C", str(repo), "grep", *flags, "-E", "-e", pattern, ref, "--", POSTS],
        capture_output=True,
        text=True,
        check=False,
    )
    if done.returncode not in (0, 1):  # 1 = no match, which is a real answer
        raise RuntimeError(f"git grep failed at {ref}: {done.stderr.strip()[:200]}")
    return done.stdout


def published_dates(repo: Path, ref: str, dates: list[str]) -> set[str]:
    """Dates (YYYY-MM-DD) that have at least one NON-DRAFT post at `ref`. Two git calls.

    A draft never goes live, so a date whose only post is a draft is still missing; counting
    it as published would block catch-up for that date forever, with no signal.
    """
    if not dates:
        return set()
    pattern = r"^date\s*[=:]\s*[\"']?(" + "|".join(map(re.escape, dates)) + ")"
    prefix = ref + ":"
    drafts = {
        line[len(prefix) :] if line.startswith(prefix) else line
        for line in _grep(repo, ref, DRAFT, "-l", "-i").splitlines()
    }
    found = set()
    for line in _grep(repo, ref, pattern).splitlines():
        body = line[len(prefix) :] if line.startswith(prefix) else line
        path, _, text = body.partition(":")
        match = re.match(pattern, text)
        if match and path not in drafts:
            found.add(match.group(1))
    return found


def load_state(path: Path) -> dict[str, dict]:
    try:
        value = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def save_state(path: Path, state: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(dir=path.parent, prefix=".catchup-")
    with os.fdopen(handle, "w") as stream:
        json.dump(state, stream, indent=1, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(name, path)


def plan(
    repo: Path, ref: str, target: str, days: int, max_attempts: int, state: dict[str, dict]
) -> dict[str, list[str]]:
    """Newest first: the freshest missing day is worth the most and is tried first."""
    end = dt.date.fromisoformat(target)
    window = [(end - dt.timedelta(days=n)).isoformat() for n in range(1, days + 1)]
    have = published_dates(repo, ref, window)
    attempt, gave_up, newly_gave_up = [], [], []
    for date in window:
        if date in have:
            continue
        entry = state.get(date, {})
        if int(entry.get("attempts", 0)) >= max_attempts:
            gave_up.append(date)
            if not entry.get("gave_up_reported"):
                newly_gave_up.append(date)
        else:
            attempt.append(date)
    return {
        "attempt": attempt,
        "gave_up": gave_up,
        "newly_gave_up": newly_gave_up,
        "published": sorted(have),
    }


def record(state: dict[str, dict], date: str, outcome: str, now: str) -> dict[str, dict]:
    entry = dict(state.get(date, {}))
    if outcome == "attempt":
        entry["attempts"] = int(entry.get("attempts", 0)) + 1
        entry["last_attempt"] = now
        entry.setdefault("first_missed", now)
    elif outcome == "published":
        entry["published"] = now
    elif outcome == "gave-up-reported":
        entry["gave_up_reported"] = now
    else:
        raise ValueError(f"unknown outcome {outcome!r}")
    return {**state, date: entry}


def prune(state: dict[str, dict], target: str, keep_days: int = 30) -> dict[str, dict]:
    floor = (dt.date.fromisoformat(target) - dt.timedelta(days=keep_days)).isoformat()
    return {date: entry for date, entry in state.items() if date >= floor}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    subs = parser.add_subparsers(dest="command", required=True)
    planner = subs.add_parser("plan")
    planner.add_argument("--repo", type=Path, required=True)
    planner.add_argument("--ref", default="origin/master")
    planner.add_argument("--target", required=True, help="the date tonight's run covers")
    planner.add_argument("--days", type=int, default=3)
    planner.add_argument("--max-attempts", type=int, default=3)
    marker = subs.add_parser("record")
    marker.add_argument("--date", required=True)
    marker.add_argument("--outcome", required=True)
    args = parser.parse_args()
    state = load_state(args.state)
    now = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")
    if args.command == "plan":
        try:
            result = plan(args.repo, args.ref, args.target, args.days, args.max_attempts, state)
        except (RuntimeError, ValueError) as exc:
            print(
                json.dumps({"attempt": [], "gave_up": [], "newly_gave_up": [], "error": str(exc)})
            )
            return 0  # planning trouble must never fail the night's own run
        save_state(args.state, prune(state, args.target))
        print(json.dumps(result))
        return 0
    dt.date.fromisoformat(args.date)
    save_state(args.state, record(state, args.date, args.outcome, now))
    return 0


if __name__ == "__main__":
    sys.exit(main())
