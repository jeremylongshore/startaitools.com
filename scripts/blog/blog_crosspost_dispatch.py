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

from blog_publication_state import PublicationError, atomic_state, load_state, state_locked


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
    parser.add_argument("action", choices=("recover", "dispatch"))
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--slug")
    parser.add_argument("--platform", choices=("devto", "hashnode"))
    parser.add_argument("--provider")
    parser.add_argument("--source")
    args = parser.parse_args()
    # Retain only the consumer lease among inherited non-standard descriptors.
    maximum = min(resource.getrlimit(resource.RLIMIT_NOFILE)[0], 65536)
    os.closerange(3, 8)
    os.closerange(9, int(maximum))
    if args.action == "recover":
        recover(args.queue)
        return 0
    if not all((args.slug, args.platform, args.provider, args.source)):
        parser.error("dispatch needs slug, platform, provider and source")
    return dispatch(args.queue, args.slug, args.platform, args.provider, args.source)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (PublicationError, ValueError) as exc:
        print(f"Cross-post dispatch held: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
