"""Session preflight: one bounded suite at a time, and only with measured disk headroom.

See tests/suite_capacity.py for the rules and the runbook for the measurements.
"""

from __future__ import annotations

import os
import tempfile

import pytest
import suite_capacity as capacity


def pytest_configure(config: pytest.Config) -> None:
    if hasattr(config, "workerinput"):
        return  # an xdist worker: the controller already passed the preflight
    refusal = capacity.check_workers(getattr(config.option, "numprocesses", None))
    if refusal:
        pytest.exit(refusal, returncode=pytest.ExitCode.USAGE_ERROR)

    path = capacity.lock_path()
    fd = capacity.acquire_suite_lock(path)
    if fd is None:
        pytest.exit(
            f"refusing to start: another run of this suite (pid {capacity.holder_of(path)}) "
            f"holds {path}. Concurrent full runs filled the dev box disk on 2026-10-03; "
            "wait for it to finish.",
            returncode=pytest.ExitCode.USAGE_ERROR,
        )
    config._startaitools_suite_lock = fd  # released in pytest_unconfigure

    temp_root = config.option.basetemp or tempfile.gettempdir()
    probe = temp_root if os.path.isdir(temp_root) else os.path.dirname(os.path.abspath(temp_root))
    admission = capacity.check_disk(
        capacity.free_mb_of(probe), capacity.PIPELINE_HOST_MARKER.is_dir()
    )
    if not admission.ok:
        pytest.exit(admission.message, returncode=pytest.ExitCode.USAGE_ERROR)


def pytest_unconfigure(config: pytest.Config) -> None:
    fd = getattr(config, "_startaitools_suite_lock", None)
    if fd is not None:
        os.close(fd)
