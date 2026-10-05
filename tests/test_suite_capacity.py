"""Capacity guards: the test-suite preflight and the daily producer's admission line.

startaitools-9a8.4.2. On 2026-10-03 concurrent full runs of this suite plus an
unretired run-workspace registry took the dev box to 0 bytes free. These tests
pin the guards that stop either from happening silently again.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest
import suite_capacity as capacity

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts/blog/blog-backfill-daily.sh"


# --- test-suite preflight ----------------------------------------------------


def test_disk_admission_requires_suite_peak_plus_daily_line_on_a_pipeline_host(monkeypatch):
    monkeypatch.delenv(capacity.ENV_SUITE_PEAK, raising=False)
    need = capacity.SUITE_PEAK_MB + capacity.DAILY_ADMISSION_MB
    assert capacity.check_disk(need, pipeline_host=True).ok
    refused = capacity.check_disk(need - 1, pipeline_host=True)
    assert not refused.ok
    assert f"need {need}MiB" in refused.message
    assert "daily blog admission" in refused.message


def test_disk_admission_without_the_pipeline_needs_only_the_suite_peak(monkeypatch):
    monkeypatch.delenv(capacity.ENV_SUITE_PEAK, raising=False)
    assert capacity.check_disk(capacity.SUITE_PEAK_MB, pipeline_host=False).ok
    assert not capacity.check_disk(capacity.SUITE_PEAK_MB - 1, pipeline_host=False).ok


def test_the_incident_reading_is_refused(monkeypatch):
    monkeypatch.delenv(capacity.ENV_SUITE_PEAK, raising=False)
    assert not capacity.check_disk(0, pipeline_host=True).ok
    assert not capacity.check_disk(217, pipeline_host=False).ok


def test_an_override_can_raise_the_suite_reserve_but_never_lower_it(monkeypatch):
    monkeypatch.setenv(capacity.ENV_SUITE_PEAK, "1")
    assert capacity.required_mb(pipeline_host=False) == capacity.SUITE_PEAK_MB
    monkeypatch.setenv(capacity.ENV_SUITE_PEAK, "not-a-number")
    assert capacity.required_mb(pipeline_host=False) == capacity.SUITE_PEAK_MB
    monkeypatch.setenv(capacity.ENV_SUITE_PEAK, str(capacity.SUITE_PEAK_MB * 2))
    assert capacity.required_mb(pipeline_host=False) == capacity.SUITE_PEAK_MB * 2


@pytest.mark.parametrize("value", [None, 0, "0", 1, 2])
def test_bounded_worker_counts_are_admitted(value):
    assert capacity.check_workers(value) is None


@pytest.mark.parametrize("value", [3, 16, "auto", "logical"])
def test_unbounded_worker_counts_are_refused(value):
    message = capacity.check_workers(value)
    assert message is not None and message.startswith("refusing to start")


def test_a_second_holder_of_the_suite_lock_is_refused(tmp_path):
    lock = tmp_path / "suite.lock"
    holder = subprocess.Popen(
        [
            sys.executable,
            "-c",
            textwrap.dedent(
                f"""
                import sys, time
                sys.path.insert(0, {str(Path(__file__).parent)!r})
                import suite_capacity
                fd = suite_capacity.acquire_suite_lock(__import__("pathlib").Path({str(lock)!r}))
                print("held" if fd is not None else "refused", flush=True)
                time.sleep(30)
                """
            ),
        ],
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert holder.stdout.readline().strip() == "held"
        assert capacity.acquire_suite_lock(lock) is None
        assert capacity.holder_of(lock) == str(holder.pid)
    finally:
        holder.kill()
        holder.wait()
    fd = capacity.acquire_suite_lock(lock)  # released with the holder
    assert fd is not None
    os.close(fd)


def test_a_concurrent_pytest_session_refuses_before_running_any_test(tmp_path):
    """End to end: the conftest preflight refuses a second session on the same lock."""
    lock = tmp_path / "suite.lock"
    held = capacity.acquire_suite_lock(lock)
    assert held is not None
    probe = tmp_path / "test_probe.py"
    probe.write_text("def test_never_runs():\n    raise AssertionError('preflight let it run')\n")
    (tmp_path / "pytest.ini").write_text("[pytest]\n")
    env = dict(
        os.environ,
        PYTHONPATH=str(ROOT / "tests"),
        PYTHONDONTWRITEBYTECODE="1",
        **{capacity.ENV_LOCK: str(lock)},
    )
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-p", "conftest",
             "-c", str(tmp_path / "pytest.ini"), str(probe)],
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=tmp_path,
        )
    finally:
        os.close(held)
    output = result.stdout + result.stderr
    assert result.returncode == pytest.ExitCode.USAGE_ERROR, output
    assert "another run of this suite" in output
    assert "preflight let it run" not in output


# --- daily producer admission line ---------------------------------------------


def _disk_check(tmp_path: Path, free_mb: int, **env: str) -> subprocess.CompletedProcess:
    home = tmp_path / "home"
    fake_bin = home / ".local/bin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    fake_df = fake_bin / "df"
    fake_df.write_text(
        "#!/bin/sh\n"
        "echo 'Filesystem 1048576-blocks Used Available Capacity Mounted on'\n"
        f"echo '/dev/fake 400000 1 {free_mb} 1% /'\n"
    )
    fake_df.chmod(0o755)
    run_env = {
        "HOME": str(home),
        "PATH": f"{fake_bin}:/usr/bin:/bin",
        "BLOG_REPO_DIR": str(tmp_path),
        "BLOG_LOG_DIR": str(tmp_path / "logs"),
        **env,
    }
    return subprocess.run(
        ["bash", str(WRAPPER), "--disk-check"],
        env=run_env,
        capture_output=True,
        text=True,
        timeout=60,
    )


@pytest.mark.parametrize(
    ("free_mb", "rc", "state"),
    [
        (217, 1, "BELOW-FLOOR"),  # the 2026-09-04 reading
        (600, 1, "BELOW-FLOOR"),  # admitted by the old 500 MiB line; one run would hit 0
        (4083, 1, "BELOW-FLOOR"),  # one MiB under floor 500 + reserve 3584
        (4084, 0, "warn"),
        (10239, 0, "warn"),
        (10240, 0, "ok"),
    ],
)
def test_daily_admission_is_the_floor_plus_the_measured_run_reserve(tmp_path, free_mb, rc, state):
    result = _disk_check(tmp_path, free_mb)
    assert result.returncode == rc, result.stdout + result.stderr
    assert f"state={state}" in result.stdout
    assert "admission=4084MiB (floor=500MiB + reserve=3584MiB) warn=10240MiB" in result.stdout


def test_the_residual_floor_cannot_be_lowered_by_the_environment(tmp_path):
    result = _disk_check(tmp_path, 4000, BLOG_BACKFILL_DISK_MIN_MB="0")
    assert result.returncode == 1
    assert "floor=500MiB" in result.stdout


def test_the_floor_and_reserve_can_be_raised_by_hand(tmp_path):
    result = _disk_check(
        tmp_path, 8999, BLOG_BACKFILL_DISK_MIN_MB="1000", BLOG_BACKFILL_RUN_RESERVE_MB="8000"
    )
    assert result.returncode == 1
    assert "admission=9000MiB" in result.stdout


def test_the_guard_admits_runs_against_the_admission_line_not_the_floor():
    text = WRAPPER.read_text()
    assert "DISK_MIN_MB=$((DISK_FLOOR_MB + RUN_RESERVE_MB))" in text
    assert 'disk_guard "$BLOG_DIR" "$DISK_MIN_MB" "$LOG" "$DISK_WARN_MB"' in text


def test_pytest_keeps_only_failed_temp_trees_from_the_latest_session():
    import tomllib

    options = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"]["pytest"]["ini_options"]
    assert options["tmp_path_retention_policy"] == "failed"
    assert options["tmp_path_retention_count"] == 1
