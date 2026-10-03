#!/usr/bin/env python3
"""Bounded cross-post dispatch; uncertain remote outcomes are never resent."""

from __future__ import annotations

import argparse
import datetime as dt
import math
import os
import resource
import select
import signal
import stat
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlparse

sys.dont_write_bytecode = True  # keep run workspaces free of __pycache__
from blog_publication_state import (  # noqa: E402
    PublicationError,
    atomic_state,
    load_state,
    state_locked,
)


def clock():
    return dt.datetime.now(dt.UTC)


def stamp(value=None):
    return (value or clock()).isoformat().replace("+00:00", "Z")


def duration():
    value = float(os.environ.get("CROSSPOST_PROVIDER_TIMEOUT_SECONDS", "150"))
    if not math.isfinite(value) or not 0 < value <= 600:
        raise PublicationError("provider deadline must be positive and at most 600 seconds")
    return value


def consumer_authority(path):
    """Verify the inherited descriptor is the already-held canonical kernel lease."""
    lock = path.parent / ".blog-crosspost-consumer.lock"
    held = os.fstat(8)
    actual = lock.lstat()
    if not stat.S_ISREG(actual.st_mode) or (held.st_dev, held.st_ino) != (
        actual.st_dev,
        actual.st_ino,
    ):
        raise PublicationError("consumer lease descriptor is not the canonical lock")
    details = Path("/proc/self/fdinfo/8").read_text()
    if not any(
        "FLOCK" in line and "WRITE" in line and f":{held.st_ino} " in line
        for line in details.splitlines()
    ):
        raise PublicationError("consumer lease is not already held")


def due(state):
    for field in ("publish_after", "retry_after"):
        value = state.get(field)
        if value is None:
            continue
        try:
            parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                raise ValueError("missing timezone")
        except (AttributeError, TypeError, ValueError) as exc:
            raise PublicationError("dispatch due clock is invalid") from exc
        if parsed > clock():
            return False
    return True


def recover(path):
    """Only called while holding the consumer lease, so no dispatch remains live."""
    consumer_authority(path)
    with state_locked(path.parent):
        rows = load_state(path)
        changed = False
        for row in rows:
            for platform in ("devto", "hashnode"):
                state = row.get(platform)
                if isinstance(state, dict) and state.get("status") == "dispatching":
                    state.update(
                        status="ambiguous",
                        error="dispatch interrupted; verify remote before retry",
                        finished_at=stamp(),
                    )
                    changed = True
        if changed:
            atomic_state(path, rows)


def begin(path, slug, platform, seconds):
    with state_locked(path.parent):
        rows = load_state(path)
        row = next((row for row in rows if row["slug"] == slug), None)
        if row is None or not isinstance(row.get(platform), dict):
            raise PublicationError("dispatch identity is missing or invalid")
        state = row[platform]
        if state.get("status") != "pending" or not due(state):
            return None
        attempts = state.get("attempts", 0)
        if type(attempts) is not int or attempts < 0:
            raise PublicationError("dispatch attempt count is invalid")
        if attempts >= 5:
            state.update(status="failed", error="safe-rejection retry budget exhausted")
            atomic_state(path, rows)
            return None
        identity = str(uuid.uuid4())
        state.update(
            status="dispatching",
            dispatch_id=identity,
            started_at=stamp(),
            deadline_at=stamp(clock() + dt.timedelta(seconds=seconds + 2)),
        )
        atomic_state(path, rows)
        return identity


def finish(path, slug, platform, identity, code, output, error):
    with state_locked(path.parent):
        rows = load_state(path)
        row = next((row for row in rows if row["slug"] == slug), None)
        if row is None or not isinstance(row.get(platform), dict):
            raise PublicationError("dispatch result identity is missing or invalid")
        state = row[platform]
        if state.get("status") != "dispatching" or state.get("dispatch_id") != identity:
            return state.get("status", "unknown")
        attempts = state.get("attempts", 0)
        if type(attempts) is not int or attempts < 0:
            raise PublicationError("dispatch result attempt count is invalid")
        state.update(attempts=attempts + 1, finished_at=stamp())
        url = output.strip().splitlines()[-1] if output.strip() else ""
        parsed = urlparse(url)
        if code == 0 and parsed.scheme == "https" and parsed.netloc and not parsed.username:
            state.update(status="published", url=url, published_at=stamp())
            state.pop("error", None)
            state.pop("retry_after", None)
        elif code == 75 and error.strip().splitlines()[-1:] == ["CROSSPOST_SAFE_REJECTION"]:
            # Only a definitive rejected create uses this explicit provider contract.
            state.update(
                status="pending" if attempts < 4 else "failed",
                error="provider explicitly rejected create",
                retry_after=stamp(clock() + dt.timedelta(minutes=15 * 2 ** min(attempts, 4))),
            )
            state["publish_after"] = state["retry_after"]
        else:
            state.update(
                status="ambiguous", error="remote acceptance unverified; reconcile before retry"
            )
        atomic_state(path, rows)
        return state["status"]


RESOLVABLE = ("ambiguous", "failed", "pending")


def resolve(path, slug, platform, reason, allowed=("ambiguous",)):
    """Owner-decided terminal outcome for a row that must never be retried.

    Only held (ambiguous/failed) or not-yet-sent (pending) rows qualify; a
    published or in-flight row is refused. The row becomes ``skipped`` (terminal
    for the sweep) and the prior state is kept in an append-only ``resolutions``
    list, so the history of what was attempted is preserved.
    """
    if not reason or not reason.strip():
        raise PublicationError("resolution needs an explicit reason")
    if any(value not in RESOLVABLE for value in allowed):
        raise PublicationError("only ambiguous, failed or pending rows can be resolved")
    with state_locked(path.parent):
        rows = load_state(path)
        row = next((row for row in rows if row["slug"] == slug), None)
        if row is None or not isinstance(row.get(platform), dict):
            raise PublicationError("resolution identity is missing or invalid")
        state = row[platform]
        current = state.get("status")
        if current not in allowed:
            raise PublicationError(f"{platform} status {current!r} is not resolvable here")
        history = state.get("resolutions", [])
        if not isinstance(history, list):
            raise PublicationError("existing resolution history is invalid")
        entry = {"from": current, "reason": reason.strip(), "at": stamp()}
        if "error" in state:
            entry["prior_error"] = state["error"]
        state.update(status="skipped", error=reason.strip(), resolutions=[*history, entry])
        state.pop("retry_after", None)
        atomic_state(path, rows)
    print(f"{platform}: skipped (from {current})", flush=True)
    return 0


HELD = ("ambiguous", "failed", "dispatching")
PAUSE_PREFIX = "paused:"


def held(path):
    """Read-only list of held rows with the exact recovery command for each.

    A held row from an earlier post keeps every later run DEGRADED, so the alert
    must say which row it is (date, slug, platform, state), not just "today".
    """
    tool = Path(__file__).resolve()
    lines = []
    for row in load_state(path):
        for platform in ("devto", "hashnode"):
            state = row.get(platform)
            if not isinstance(state, dict) or state.get("status") not in HELD:
                continue
            status = state["status"]
            day = str(row.get("published_at") or row.get("date") or "unknown-date")[:10]
            lines.append(f"HELD {day} {row.get('slug')} {platform} {status}")
            if status == "dispatching":
                lines.append(
                    "  recover: the next queue run marks an interrupted dispatch ambiguous;"
                    " verify on the provider, then resolve it"
                )
                continue
            source = "" if status == "ambiguous" else f" --from {status}"
            lines.append(
                f"  recover (after checking {platform} for the post): python3 {tool} resolve"
                f" --queue {path} --slug {row.get('slug')} --platform {platform}{source}"
                " --reason '<published at URL | abandoned: why>'"
            )
    for line in lines:
        print(line)
    return 0


def reopen(path, slug, platform, reason):
    """Undo a pause-time skip after the destination is re-enabled (history kept).

    Only a row whose current skip came from the pause switch (``paused:`` reason,
    resolved from ``pending``) can be reopened; owner-abandoned held rows cannot.
    """
    if not reason or not reason.strip():
        raise PublicationError("reopen needs an explicit reason")
    with state_locked(path.parent):
        rows = load_state(path)
        row = next((row for row in rows if row["slug"] == slug), None)
        if row is None or not isinstance(row.get(platform), dict):
            raise PublicationError("reopen identity is missing or invalid")
        state = row[platform]
        history = state.get("resolutions")
        last = history[-1] if isinstance(history, list) and history else {}
        if (
            state.get("status") != "skipped"
            or last.get("from") != "pending"
            or not str(last.get("reason", "")).startswith(PAUSE_PREFIX)
            or state.get("error") != last.get("reason")
        ):
            raise PublicationError(f"{platform} row was not skipped by the pause switch")
        entry = {"from": "skipped", "to": "pending", "reason": reason.strip(), "at": stamp()}
        state.update(status="pending", resolutions=[*history, entry])
        state.pop("error", None)
        atomic_state(path, rows)
    print(f"{platform}: pending (reopened from pause skip)", flush=True)
    return 0


def kill_group(process, sig):
    try:
        os.killpg(process.pid, sig)
    except ProcessLookupError:
        pass


def dispatch(path, slug, platform, provider, source):
    seconds = duration()
    # The watchdog keeps the consumer lease after a shell-wrapper crash. Only
    # FD8 is passed to the provider; unrelated owner/workspace leases are not.
    consumer_authority(path)
    identity = begin(path, slug, platform, seconds)
    if identity is None:
        return 0
    code = 1
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        process = None
        try:
            process = subprocess.Popen(
                [provider, source], stdout=out, stderr=err, start_new_session=True, pass_fds=(8,)
            )
            # pidfd readiness observes exit without reaping. Keeping the child
            # unreaped reserves its PID/group identity until final group cleanup.
            handle = os.pidfd_open(process.pid)
            try:
                timed_out = not select.select([handle], [], [], seconds)[0]
                if timed_out:
                    kill_group(process, signal.SIGTERM)
                    select.select([handle], [], [], 2)
                kill_group(process, signal.SIGKILL)
                code = process.wait(timeout=2)
                if timed_out:
                    code = 124
            finally:
                os.close(handle)
        except (OSError, subprocess.TimeoutExpired):
            if process is not None and process.returncode is None:
                kill_group(process, signal.SIGKILL)
                process.wait(timeout=2)
            code = 124
        out.seek(0)
        err.seek(0)
        output = out.read(1_000_000).decode(errors="replace")
        error = err.read(1_000_000).decode(errors="replace")
    status = finish(path, slug, platform, identity, code, output, error)
    # The receipt is persisted before writing into a possibly dead parent's pipe.
    print(f"{platform}: {status}", flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("recover", "dispatch", "resolve", "reopen", "held"))
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--slug")
    parser.add_argument("--platform", choices=("devto", "hashnode"))
    parser.add_argument("--provider")
    parser.add_argument("--source")
    parser.add_argument("--reason")
    parser.add_argument(
        "--from",
        dest="allowed",
        action="append",
        choices=RESOLVABLE,
        help="status the row must currently have (repeatable; default ambiguous)",
    )
    args = parser.parse_args()
    # Retain only the consumer lease among inherited non-standard descriptors.
    maximum = min(resource.getrlimit(resource.RLIMIT_NOFILE)[0], 65536)
    os.closerange(3, 8)
    os.closerange(9, int(maximum))
    if args.action == "recover":
        recover(args.queue)
        return 0
    if args.action == "held":
        return held(args.queue)
    if args.action == "reopen":
        if not all((args.slug, args.platform, args.reason)):
            parser.error("reopen needs slug, platform and reason")
        return reopen(args.queue, args.slug, args.platform, args.reason)
    if args.action == "resolve":
        if not all((args.slug, args.platform, args.reason)):
            parser.error("resolve needs slug, platform and reason")
        return resolve(
            args.queue, args.slug, args.platform, args.reason, tuple(args.allowed or ("ambiguous",))
        )
    if not all((args.slug, args.platform, args.provider, args.source)):
        parser.error("dispatch needs slug, platform, provider and source")
    return dispatch(args.queue, args.slug, args.platform, args.provider, args.source)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PublicationError, ValueError) as exc:
        print(f"Cross-post dispatch held: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
