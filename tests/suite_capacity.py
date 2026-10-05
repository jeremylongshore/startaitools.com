"""Capacity preflight for this test suite on the shared dev box.

On 2026-10-03 several full runs of this suite ran at once on the dev box while
the run-workspace registry was already ~45 GB, and the root filesystem reached
0 bytes free. One full run is not small: its fixtures build real Hugo/git
fixture repositories and run workspaces, and pytest keeps their temp trees until
the session ends. Measured numbers and their source are in
000-docs/004-OP-RUNB-blog-low-disk-recovery.md, section "Capacity limits".

Three rules, enforced by tests/conftest.py before any test runs:

1. One suite at a time per user. A second concurrent session refuses instead of
   doubling the temp footprint (an exclusive, non-blocking flock).
2. Bounded workers. pytest-xdist may use at most MAX_WORKERS workers; "-n auto"
   refuses, because it scales with CPU count, not with free disk.
3. Disk admission. A session starts only when free space on its temp filesystem
   covers the suite's measured peak plus, on a host that runs the daily blog
   pipeline, the daily producer's own admission line, so a test run can never
   be the reason the 04:00 run refuses.

The functions here are pure (no pytest import) so tests/test_suite_capacity.py
can exercise them directly.
"""

from __future__ import annotations

import fcntl
import os
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

# Measured peak temp usage of one full serial run: 4252 MiB on 2026-10-05, plus ~20%
# growth headroom (see the runbook).
SUITE_PEAK_MB = 5120
# blog-backfill-daily.sh admission line: 500 MiB residual floor + 3584 MiB run reserve.
DAILY_ADMISSION_MB = 4084
MAX_WORKERS = 2
# Present only on a host that runs the daily pipeline (the run-workspace registry).
PIPELINE_HOST_MARKER = Path.home() / ".local/state/blog-run-workspaces"

ENV_SUITE_PEAK = "STARTAITOOLS_TEST_SUITE_PEAK_MB"
ENV_LOCK = "STARTAITOOLS_TEST_LOCK"


@dataclass(frozen=True)
class Admission:
    ok: bool
    free_mb: int
    required_mb: int
    message: str


def _int_env(name: str, default: int) -> int:
    raw = os.environ.get(name, "")
    try:
        value = int(raw)
    except ValueError:
        return default
    # An override may raise the reserve, never lower it below the measured peak.
    return max(value, default)


def required_mb(pipeline_host: bool) -> int:
    peak = _int_env(ENV_SUITE_PEAK, SUITE_PEAK_MB)
    return peak + (DAILY_ADMISSION_MB if pipeline_host else 0)


def check_disk(free_mb: int, pipeline_host: bool) -> Admission:
    need = required_mb(pipeline_host)
    if free_mb >= need:
        return Admission(True, free_mb, need, f"{free_mb}MiB free >= {need}MiB required")
    detail = f"suite peak {need - (DAILY_ADMISSION_MB if pipeline_host else 0)}MiB"
    if pipeline_host:
        detail += f" + daily blog admission {DAILY_ADMISSION_MB}MiB"
    return Admission(
        False,
        free_mb,
        need,
        f"refusing to start: {free_mb}MiB free on the temp filesystem, need {need}MiB "
        f"({detail}). Free space first (runbook 000-docs/004-OP-RUNB-blog-low-disk-"
        "recovery.md); do not lower this number.",
    )


def free_mb_of(path: str | os.PathLike[str]) -> int:
    return shutil.disk_usage(path).free // (1024 * 1024)


def check_workers(numprocesses: object) -> str | None:
    """Return a refusal message, or None when the worker count is bounded."""
    if numprocesses in (None, 0, "0"):
        return None
    try:
        count = int(numprocesses)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return (
            f"refusing to start: -n {numprocesses} scales with CPU count, not free disk; "
            f"use -n {MAX_WORKERS} or fewer"
        )
    if count > MAX_WORKERS:
        return f"refusing to start: -n {count} exceeds the {MAX_WORKERS}-worker limit"
    return None


def lock_path() -> Path:
    override = os.environ.get(ENV_LOCK)
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / f"startaitools-test-suite-{os.getuid()}.lock"


def acquire_suite_lock(path: Path) -> int | None:
    """Take the per-user suite lock without waiting; None when another run holds it."""
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        return None
    os.ftruncate(fd, 0)
    os.write(fd, f"{os.getpid()}\n".encode())
    return fd


def holder_of(path: Path) -> str:
    try:
        return path.read_text().strip() or "unknown"
    except OSError:
        return "unknown"
