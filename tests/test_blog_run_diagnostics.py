"""Real local Git/children only: diagnostics must never enlarge publication writes."""

from __future__ import annotations

import json
import os
import shlex
import signal
import subprocess
import sys
import time
import types
from pathlib import Path

import pytest
from test_blog_publication_state import run as run
from test_blog_workspace import DATE, DECISIONS, HELPER, POST, action, command, create, git, produce
from test_blog_workspace import repository as repository

core = types.ModuleType("diagnostic_workspace")
core.__file__ = str(HELPER)
exec(compile(HELPER.read_bytes(), str(HELPER), "exec"), core.__dict__)


def diagnostic_child(run, *, stderr="real diagnostic\n", code=0, label="apply-patterns"):
    child = (
        "import sys;sys.stdout.write('{\"fixture\":true}\\n');"
        f"sys.stderr.write({stderr!r});sys.exit({code})"
    )
    arguments = shlex.join([sys.executable, "-c", child])
    script = (
        'python3 "$BLOG_RUN_WORKSPACE_HELPER" diagnostic '
        '--manifest "$BLOG_RUN_MANIFEST" '
        f'--label {shlex.quote(label)} -- {arguments} '
        f'> ".blog-staging/{DATE}.{run["run_id"]}.classifier.json"'
    )
    return command(sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                   "--", "bash", "-c", script)


def test_actual_registered_stderr_preserves_stdout_and_write_set(repository):
    run = create(repository)
    root = produce(run)
    result = diagnostic_child(run)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(Path(run["manifest"]).read_text())
    directory = Path(manifest["diagnostics_dir"])
    assert directory == Path(run["manifest"]).parent / "diagnostics"
    assert not directory.is_relative_to(root)
    assert (directory / "apply-patterns.stderr").read_text() == "real diagnostic\n"
    receipt = json.loads((directory / "apply-patterns.json").read_text())
    assert receipt["exit_code"] == 0
    assert receipt["state"] == "completed"
    assert receipt["run_id"] == run["run_id"]
    assert receipt["date"] == DATE
    assert receipt["producer_attempt_id"] == manifest["producer_attempt"]["attempt_id"]
    assert (root / f'.blog-staging/{DATE}.{run["run_id"]}.classifier.json').read_text() == (
        '{"fixture":true}\n'
    )
    validated = action(run, "validate")
    assert validated["publish_paths"] == [POST, DECISIONS]
    git(root, "add", "--", *validated["publish_paths"])
    git(root, "commit", "-m", "offline publication fixture")
    assert "diagnostic" not in git(root, "ls-tree", "-r", "--name-only", "HEAD")
    assert manifest["producer_attempt"]["exit_code"] == 0


def test_actual_old_workspace_stderr_stays_forbidden(repository):
    run = create(repository)
    root = produce(run)
    unexpected = root / f'.blog-staging/{DATE}.{run["run_id"]}.apply.stderr'
    unexpected.touch()
    error = action(run, "validate", success=False)
    assert "changes outside run write-set" in error
    assert unexpected.name in error
    assert unexpected.read_bytes() == b""


@pytest.mark.parametrize("code", [1, 23, 143])
def test_nonzero_command_diagnostics_survive_quarantine(repository, code):
    owner, _, _ = repository
    dirty = owner / "layouts/partials/schema.html"
    dirty.write_text("owner edit must remain\n")
    before = git(owner, "status", "--porcelain=v1")
    run = create(repository)
    produce(run)
    result = diagnostic_child(run, code=code)
    assert result.returncode == code
    directory = Path(run["manifest"]).parent / "diagnostics"
    evidence = {p.name: p.read_bytes() for p in directory.iterdir()}
    action(run, "quarantine", "--reason", "offline diagnostic command failed")
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == evidence
    assert git(owner, "status", "--porcelain=v1") == before
    assert dirty.read_text() == "owner edit must remain\n"
    assert Path(run["workspace"]).exists()
    assert json.loads((directory / "apply-patterns.json").read_text())["exit_code"] == code


def test_resume_appends_evidence_without_reusing_other_run_namespace(repository):
    run = create(repository)
    produce(run)
    assert diagnostic_child(run, stderr="first\n").returncode == 0
    resumed = create(repository)
    assert resumed["diagnostics_dir"] == run["diagnostics_dir"]
    assert diagnostic_child(resumed, stderr="second\n").returncode == 0
    diagnostic = Path(run["diagnostics_dir"]) / "apply-patterns.stderr"
    assert diagnostic.read_text() == "first\nsecond\n"
    action(run, "quarantine", "--reason", "offline completed investigation")
    other = create(repository, run_id="next-run")
    assert other["diagnostics_dir"] != run["diagnostics_dir"]
    assert diagnostic.read_text() == "first\nsecond\n"


@pytest.mark.parametrize("label", ["../escape", "wrong/name", "", "x" * 65])
def test_unsafe_diagnostic_labels_do_not_launch(repository, label):
    run = create(repository)
    produce(run)
    result = diagnostic_child(run, label=label)
    assert result.returncode != 0
    assert not (Path(run["manifest"]).parent / "escape").exists()
    assert "safe diagnostic label" in Path(run["producer_log"]).read_text()


def test_unleased_diagnostic_command_cannot_create_or_run(repository):
    run = create(repository)
    marker = Path(run["workspace"]) / "foreign-marker"
    result = command(sys.executable, str(HELPER), "diagnostic", "--manifest", run["manifest"],
                     "--label", "unleased", "--", sys.executable, "-c",
                     f"from pathlib import Path;Path({str(marker)!r}).touch()")
    assert result.returncode != 0
    assert not marker.exists()
    assert not (Path(run["diagnostics_dir"]) / "unleased.stderr").exists()


@pytest.mark.parametrize("kind", ["directory", "log", "receipt", "lock", "hardlink"])
def test_linked_diagnostic_paths_never_write_through(repository, kind):
    run = create(repository)
    produce(run)
    directory = Path(run["diagnostics_dir"])
    foreign = repository[0] / "private-owner-note"
    foreign.write_text("owner bytes\n")
    if kind == "directory":
        directory.rmdir()
        directory.symlink_to(repository[0], target_is_directory=True)
    else:
        name = {"log": "apply-patterns.stderr", "receipt": "apply-patterns.json",
                "lock": "diagnostics.lock", "hardlink": "apply-patterns.stderr"}[kind]
        if kind == "hardlink":
            os.link(foreign, directory / name)
        else:
            (directory / name).symlink_to(foreign)
    result = diagnostic_child(run)
    assert result.returncode != 0
    assert foreign.read_text() == "owner bytes\n"
    assert not (repository[0] / "apply-patterns.stderr").exists()


@pytest.mark.parametrize("replacement", ["foreign-path", "other-run", "other-date"])
def test_manifest_diagnostic_binding_rejects_forged_namespace(repository, replacement):
    run = create(repository)
    produce(run)
    path = Path(run["manifest"])
    manifest = json.loads(path.read_text())
    if replacement == "foreign-path":
        manifest["diagnostics_dir"] = str(repository[0] / "foreign-diagnostics")
    elif replacement == "other-run":
        manifest["run_id"] = "other-run"
        manifest["branch"] = f"blog-run/{DATE}/other-run"
    else:
        manifest["date"] = "2026-09-17"
        manifest["branch"] = f"blog-run/2026-09-17/{run['run_id']}"
        manifest["permitted_staging_path"] = ".blog-staging/2026-09-17.intent.json"
    path.write_text(json.dumps(manifest))
    assert diagnostic_child(run).returncode != 0
    assert not (repository[0] / "foreign-diagnostics").exists()


def limited_child(run, *, size=100, code=0):
    # Real leased child, with only fixture-local small storage constants. The
    # actual capture code/real subprocess run unchanged, including durable status.
    child = f"import sys;sys.stderr.write(chr(120)*{size});sys.exit({code})"
    source = (
        "import sys,types;from pathlib import Path;"
        f"p=Path({str(HELPER)!r});m=types.ModuleType('fixture_core');m.__file__=str(p);"
        "exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);"
        "m.DIAGNOSTICS_LOG_BYTES=64;"
        f"sys.exit(m.run_diagnostic(Path({run['manifest']!r}),'bounded',"
        f"[sys.executable,'-c',{child!r}]))"
    )
    return command(sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                   "--", sys.executable, "-c", source)


@pytest.mark.parametrize("code,expected", [(0, 65), (7, 7)])
def test_capacity_failure_is_visible_and_retains_bounded_prefix(repository, code, expected):
    run = create(repository)
    produce(run)
    result = limited_child(run, code=code)
    assert result.returncode == expected
    directory = Path(run["diagnostics_dir"])
    assert (directory / "bounded.stderr").read_bytes() == b"x" * 64
    receipt = json.loads((directory / "bounded.json").read_text())
    assert receipt["exit_code"] == code
    assert receipt["omitted_bytes"] == 36
    assert receipt["capture_failed"] is True
    assert "capture exceeded capacity" in Path(run["producer_log"]).read_text()
    assert "diagnostic capture incomplete" in action(run, "validate", success=False)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    repeated = limited_child(run)
    assert repeated.returncode != 0
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


@pytest.mark.parametrize("filename", ["foreign.json", "2026-09-17.other.classifier.json",
                                     f"{DATE}.offline-run.notes.txt"])
def test_unknown_staging_files_remain_rejected_after_valid_capture(repository, filename):
    run = create(repository)
    root = produce(run)
    assert diagnostic_child(run).returncode == 0
    (root / ".blog-staging" / filename).write_text("untrusted scratch\n")
    assert "changes outside run write-set" in action(run, "validate", success=False)


def test_old_active_manifest_registers_only_when_running_and_terminal_stays_immutable(repository):
    run = create(repository)
    produce(run)
    path = Path(run["manifest"])
    manifest = json.loads(path.read_text())
    directory = Path(manifest.pop("diagnostics_dir"))
    directory.rmdir()
    path.write_text(json.dumps(manifest))
    before = path.read_bytes()
    assert "diagnostics_dir" not in core.load(path)
    assert path.read_bytes() == before
    assert not directory.exists()
    assert diagnostic_child(run).returncode == 0
    assert json.loads(path.read_text())["diagnostics_dir"] == str(directory)
    action(run, "quarantine", "--reason", "offline legacy proof")
    terminal = json.loads(path.read_text())
    terminal.pop("diagnostics_dir")
    path.write_text(json.dumps(terminal))
    before = path.read_bytes()
    assert core.load(path)["status"] == "quarantined"
    assert diagnostic_child(run).returncode != 0
    assert path.read_bytes() == before


def test_diagnostics_survive_completed_checkout_retirement(run, tmp_path, monkeypatch):
    # Shared fixture supplies real valid quality proof and local-only publication.
    from test_blog_workspace_retention import completed, retire

    result = diagnostic_child({**run, "manifest": str(run["manifest"]),
                               "run_id": "offline-delivery-run"})
    assert result.returncode == 0, result.stderr
    manifest = completed(run)
    directory = Path(manifest["diagnostics_dir"])
    evidence = {p.name: p.read_bytes() for p in directory.iterdir()}
    retire(run, tmp_path, monkeypatch)
    assert not run["root"].exists()
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == evidence


def test_native_style_closed_fds_still_require_actual_ancestor_producer(repository):
    run = create(repository)
    produce(run)
    args = [sys.executable, str(HELPER), "diagnostic", "--manifest", run["manifest"],
            "--label", "closed-fds", "--", sys.executable, "-c",
            "import sys;sys.stderr.write('native child diagnostic\\n')"]
    source = f"import os;os.closerange(3,1024);os.execv({sys.executable!r},{args!r})"
    result = command(sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                     "--", sys.executable, "-c", source)
    assert result.returncode == 0, result.stderr
    assert (Path(run["diagnostics_dir"]) / "closed-fds.stderr").read_text() == (
        "native child diagnostic\n"
    )
    assert action(run, "validate")["post"] == POST


@pytest.mark.parametrize("value", ["[]", "{bad", '{"schema_version":1}', "null"])
def test_malformed_receipt_is_preserved_and_not_replaced_by_success(repository, value):
    run = create(repository)
    produce(run)
    assert diagnostic_child(run).returncode == 0
    receipt = Path(run["diagnostics_dir"]) / "apply-patterns.json"
    receipt.write_text(value)
    assert diagnostic_child(run).returncode != 0
    assert receipt.read_text() == value


def test_interrupted_receipt_rename_replays_label_without_erasing_evidence(repository):
    run = create(repository)
    produce(run)
    assert diagnostic_child(run, stderr="first\n").returncode == 0
    directory = Path(run["diagnostics_dir"])
    pending = directory / "apply-patterns.tmp"
    pending.write_bytes((directory / "apply-patterns.json").read_bytes())
    pending.chmod(0o600)
    assert "interrupted diagnostic receipt" in action(run, "validate", success=False)
    assert diagnostic_child(run, stderr="second\n").returncode == 0
    assert not pending.exists()
    receipt = json.loads((directory / "apply-patterns.json").read_text())
    assert len(receipt["history"]) == 1
    assert receipt["history"][0]["state"] == "completed"
    assert (directory / "apply-patterns.stderr").read_text() == "first\nsecond\n"
    assert "recovered interrupted receipt rename" in (
        Path(run["manifest"]).parent / "run.log"
    ).read_text()


def test_partial_temporary_receipt_is_not_discarded_or_misreported_as_success(repository):
    run = create(repository)
    produce(run)
    assert diagnostic_child(run).returncode == 0
    directory = Path(run["diagnostics_dir"])
    pending = directory / "apply-patterns.tmp"
    pending.write_bytes(b'{"schema_version":')
    pending.chmod(0o600)
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    assert diagnostic_child(run).returncode != 0
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


def test_killed_capture_keeps_running_receipt_and_child_lock_until_safe_retry(repository):
    run = create(repository)
    produce(run)
    directory = Path(run["diagnostics_dir"])
    marker = Path(run["manifest"]).parent / "fixture-capture-pid"
    capture_pid = Path(run["manifest"]).parent / "fixture-supervisor-pid"
    child = (
        "import os,sys,time;from pathlib import Path;"
        f"p=Path({str(marker)!r});"
        "sys.stderr.write('before capture crash\\n');sys.stderr.flush();"
        "p.with_suffix('.tmp').write_text(str(os.getppid()));"
        "p.with_suffix('.tmp').replace(p);time.sleep(1.2)"
    )
    capture_args = [sys.executable, str(HELPER), "diagnostic", "--manifest", run["manifest"],
                    "--label", "apply-patterns", "--", sys.executable, "-c", child]
    capture = (
        "import os;from pathlib import Path;"
        f"Path({str(capture_pid)!r}).write_text(str(os.getpid()));"
        f"os.execv({sys.executable!r},{capture_args!r})"
    )
    process = subprocess.Popen(
        [sys.executable, str(HELPER), "run", "--manifest", run["manifest"], "--",
         sys.executable, "-c", capture],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    log = directory / "apply-patterns.stderr"
    deadline = time.monotonic() + 5
    while (not marker.exists() or not log.exists() or not log.stat().st_size):
        assert process.poll() is None
        assert time.monotonic() < deadline
        time.sleep(0.01)
    os.kill(int(capture_pid.read_text()), signal.SIGKILL)
    process.communicate(timeout=5)
    assert process.returncode == 137
    receipt = json.loads((directory / "apply-patterns.json").read_text())
    assert receipt["state"] == "running"
    # The real surviving child inherited capture ownership; no parent-only lock.
    assert diagnostic_child(run).returncode != 0
    assert log.read_text() == "before capture crash\n"
    import fcntl

    with (directory / "diagnostics.lock").open("rb") as stream:
        deadline = time.monotonic() + 5
        while True:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                assert time.monotonic() < deadline
                time.sleep(0.01)
    assert diagnostic_child(run, stderr="after safe retry\n").returncode == 0
    receipt = json.loads((directory / "apply-patterns.json").read_text())
    assert receipt["history"][0]["state"] == "running"
    assert log.read_text() == "before capture crash\nafter safe retry\n"


def test_retry_capacity_stops_without_erasing_prior_history(repository):
    run = create(repository)
    produce(run)
    directory = Path(run["diagnostics_dir"])
    for _ in range(core.DIAGNOSTICS_MAX_ATTEMPTS):
        assert diagnostic_child(run, stderr="a\n").returncode == 0
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    assert diagnostic_child(run, stderr="must not run\n").returncode != 0
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before
    receipt = json.loads((directory / "apply-patterns.json").read_text())
    assert len(receipt["history"]) == core.DIAGNOSTICS_MAX_ATTEMPTS - 1


def legacy_registry(repository):
    run = create(repository)
    produce(run)
    action(run, "quarantine", "--reason", "retained historical fixture")
    path = Path(run["manifest"])
    registry = path.parents[3]
    for directory in (repository[2], registry, registry / "runs", path.parent.parent, path.parent):
        directory.chmod(0o775)
    files = {str(p): p.read_bytes() for p in path.parent.rglob("*") if p.is_file()}
    modes = {str(p): p.stat().st_mode for p in path.parent.rglob("*")}
    modes[str(path.parent)] = path.parent.stat().st_mode
    return run, registry, files, modes


def test_actual_legacy_775_registry_upgrades_only_owned_registry_on_next_create(repository):
    _, registry, files, modes = legacy_registry(repository)
    before = registry.stat()
    following = create(repository, run_id="next-registered-run")
    assert registry.stat().st_mode & 0o777 == 0o700
    assert repository[2].stat().st_mode & 0o777 == 0o775
    receipt = json.loads((registry / "registry-permissions.json").read_text())
    assert receipt["previous_mode"] & 0o777 == 0o775
    assert receipt["state"] == "completed"
    assert receipt["inode"] == before.st_ino
    assert receipt["uid"] == before.st_uid
    assert (registry / "registry-permissions.json").stat().st_mode & 0o777 == 0o600
    for name, original in files.items():
        assert Path(name).read_bytes() == original
    for name, original in modes.items():
        assert Path(name).stat().st_mode == original
    produce(following)
    assert diagnostic_child(following).returncode == 0
    assert action(following, "validate")["post"] == POST


def test_existing_active_775_registry_resume_registers_private_diagnostics(repository):
    run = create(repository)
    root = produce(run)
    path = Path(run["manifest"])
    manifest = json.loads(path.read_text())
    Path(manifest.pop("diagnostics_dir")).rmdir()
    path.write_text(json.dumps(manifest))
    for directory in (path.parents[3], path.parents[2], path.parents[1], path.parent):
        directory.chmod(0o775)
    before = (root / POST).read_bytes()
    resumed = create(repository)
    assert resumed["workspace"] == run["workspace"]
    assert (root / POST).read_bytes() == before
    assert path.parent.stat().st_mode & 0o777 == 0o775
    assert diagnostic_child(resumed).returncode == 0


def test_prepared_registry_upgrade_finishes_after_permission_change_crash(repository, monkeypatch):
    _, registry, files, modes = legacy_registry(repository)
    common = Path(git(repository[0], "rev-parse", "--path-format=absolute", "--git-common-dir"))
    original = core.atomic_json

    def crash(path, value):
        if path.name == "registry-permissions.json" and value["state"] == "completed":
            raise OSError("offline injected crash before completion receipt")
        return original(path, value)

    monkeypatch.setattr(core, "atomic_json", crash)
    with core.locked(registry), pytest.raises(OSError, match="injected crash"):
        core.secure_owned_registry(registry, common)
    assert registry.stat().st_mode & 0o777 == 0o700
    prepared = json.loads((registry / "registry-permissions.json").read_text())
    assert prepared["state"] == "prepared"
    create(repository, run_id="after-crash")
    complete = json.loads((registry / "registry-permissions.json").read_text())
    assert complete["state"] == "completed"
    assert complete["prepared_at"] == prepared["prepared_at"]
    assert complete["previous_mode"] == prepared["previous_mode"]
    for name, original in files.items():
        assert Path(name).read_bytes() == original
    for name, original in modes.items():
        assert Path(name).stat().st_mode == original


def test_readonly_census_and_old_terminal_load_do_not_upgrade_modes(repository):
    run, registry, files, modes = legacy_registry(repository)
    path = Path(run["manifest"])
    manifest = json.loads(path.read_text())
    manifest.pop("diagnostics_dir")
    path.write_text(json.dumps(manifest))
    files[str(path)] = path.read_bytes()
    assert core.load(path)["status"] == "quarantined"
    assert core.census(repository[0], repository[2])["runs"][0]["status"] == "quarantined"
    assert registry.stat().st_mode & 0o777 == 0o775
    assert not (registry / "registry-permissions.json").exists()
    for name, original in files.items():
        assert Path(name).read_bytes() == original
    for name, original in modes.items():
        assert Path(name).stat().st_mode == original


def test_world_writable_registry_refuses_without_permission_or_evidence_change(repository):
    _, registry, files, modes = legacy_registry(repository)
    registry.chmod(0o777)
    (registry / "workspace.lock").unlink()
    assert "world-writable" in create(
        repository, run_id="unsafe", success=False
    )
    assert not (registry / "workspace.lock").exists()
    assert registry.stat().st_mode & 0o777 == 0o777
    assert not (registry / "registry-permissions.json").exists()
    for name, original in files.items():
        assert Path(name).read_bytes() == original
    for name, original in modes.items():
        assert Path(name).stat().st_mode == original


def test_foreign_owner_registry_refuses_permission_upgrade(repository, monkeypatch):
    _, registry, files, _ = legacy_registry(repository)
    common = Path(git(repository[0], "rev-parse", "--path-format=absolute", "--git-common-dir"))
    actual_uid = os.getuid()
    (registry / "workspace.lock").unlink()
    monkeypatch.setattr(core.os, "getuid", lambda: actual_uid + 1)
    with pytest.raises(core.WorkspaceError, match="not owned"), core.locked(registry):
        core.secure_owned_registry(registry, common)
    assert not (registry / "workspace.lock").exists()
    assert registry.stat().st_mode & 0o777 == 0o775
    assert not (registry / "registry-permissions.json").exists()
    for name, original in files.items():
        assert Path(name).read_bytes() == original


def test_atomic_receipt_overhead_counts_toward_actual_total_budget(repository, monkeypatch):
    run = create(repository)
    produce(run)
    assert diagnostic_child(run).returncode == 0
    directory = Path(run["diagnostics_dir"])
    receipt_path = directory / "apply-patterns.json"
    receipt = json.loads(receipt_path.read_text())
    before = {p.name: p.read_bytes() for p in directory.iterdir()}
    monkeypatch.setattr(core, "DIAGNOSTICS_TOTAL_BYTES", sum(map(len, before.values())) + 1)
    with pytest.raises(core.WorkspaceError, match="atomic metadata exceeds total capacity"):
        core.write_diagnostic_receipt(receipt_path, receipt)
    assert {p.name: p.read_bytes() for p in directory.iterdir()} == before


@pytest.mark.parametrize("early_parent_exit", [False, True])
def test_surviving_watchdog_bounds_orphans_and_defers_quarantine(repository, early_parent_exit):
    import fcntl

    run = create(repository)
    root = produce(run)
    directory = Path(run["diagnostics_dir"])
    capture_pid = Path(run["manifest"]).parent / "owned-capture.pid"
    marker = Path(run["manifest"]).parent / "owned-child.pid"
    before = (root / POST).read_bytes()
    child = (
        "import os,sys,time;from pathlib import Path;"
        + ("pid=os.fork();\nif pid: sys.exit(0)\n" if early_parent_exit else "")
        + f"p=Path({str(marker)!r});p.with_suffix('.tmp').write_text(str(os.getpid()));"
        "p.with_suffix('.tmp').replace(p);sys.stderr.write('owned alive\\n');"
        "sys.stderr.flush();time.sleep(120)"
    )
    # Same production capture/keeper; only its bound is shortened in this owned
    # fixture process. Source app and provider deadlines are never changed.
    capture = (
        "import os,sys,types;from pathlib import Path;"
        f"p=Path({str(capture_pid)!r});p.write_text(str(os.getpid()));"
        f"h=Path({str(HELPER)!r});m=types.ModuleType('fixture');m.__file__=str(h);"
        "exec(compile(h.read_bytes(),str(h),'exec'),m.__dict__);"
        "m.DIAGNOSTIC_COMMAND_SECONDS=3;m.DIAGNOSTIC_KILL_GRACE_SECONDS=0.2;"
        f"sys.exit(m.run_diagnostic(Path({run['manifest']!r}),'orphan',"
        f"[sys.executable,'-c',{child!r}]))"
    )
    process = subprocess.Popen(
        ["/usr/bin/timeout", "--kill-after=0.2", "1", sys.executable, str(HELPER), "run",
         "--manifest", run["manifest"], "--", sys.executable, "-c", capture],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    owned = None
    try:
        deadline = time.monotonic() + 4
        while not marker.exists():
            assert process.poll() is None
            assert time.monotonic() < deadline
            time.sleep(0.01)
        owned = int(marker.read_text())
        os.kill(int(capture_pid.read_text()), signal.SIGKILL)
        process.communicate(timeout=4)
        assert process.returncode == 137
        receipt = json.loads((directory / "orphan.json").read_text())
        assert receipt["state"] == "running"
        assert json.loads(Path(run["manifest"]).read_text())["producer_attempt"]["exit_code"] == 137
        assert "diagnostic writer still running" in action(
            run, "quarantine", "--reason", "actual supervisor137", success=False
        )
        assert "quarantine refused" in Path(run["log_file"]).read_text()
        wrapper = HELPER.with_name("blog-backfill-daily.sh").read_text()
        start = wrapper.index('if [ "$LAND_RC" -eq 20 ] || [ "$PRODUCER_ACCEPTED"')
        end = wrapper.index('log "Overall STATUS: $STATUS"', start)
        body = (
            'log() { printf "%s\\n" "$*" >> "$LOG"; }; '
            'STATUS="FAILED (actual supervisor137; land not invoked)"; '
            'LAND_RC=22; PRODUCER_ACCEPTED=0; BLOG_CANARY=1;\n'
            + wrapper[start:end] + '\nprintf "%s\\n" "$STATUS"\n'
        )
        finalized = subprocess.run(
            ["bash", "-c", body], check=False, capture_output=True, text=True,
            env={**os.environ, "WORKSPACE_HELPER": str(HELPER),
                 "BLOG_RUN_MANIFEST": run["manifest"],
                 "LOG": str(Path(run["manifest"]).parent / "wrapper-fixture.log")},
        )
        assert finalized.returncode == 0
        assert "FAILED (quarantine pending" in finalized.stdout
        assert "actual supervisor137; land not invoked" in finalized.stdout
        assert not (Path(run["manifest"]).parent / "quarantine").exists()
        assert (root / POST).read_bytes() == before
        assert diagnostic_child(run).returncode != 0
        with (directory / "diagnostics.lock").open("rb") as lease:
            with pytest.raises(BlockingIOError):
                fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            deadline = time.monotonic() + 6
            while True:
                try:
                    fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    assert time.monotonic() < deadline, "orphan must expire without manual release"
                    time.sleep(0.01)
        # Old unbounded helper fails above. New keeper's ordinary descendants
        # are gone/zombies, no longer writers. No test signal creates success.
        status = Path(f"/proc/{owned}/stat")
        assert not status.exists() or status.read_text().rsplit(")", 1)[1].split()[0] == "Z"
        assert (root / POST).read_bytes() == before
        action(run, "quarantine", "--reason", "bounded capture expired; actual supervisor137")
        assert json.loads(Path(run["manifest"]).read_text())["status"] == "quarantined"
        assert json.loads((directory / "orphan.json").read_text())["state"] == "running"
    finally:
        # Only failed-fixture cleanup may signal its own recorded PID; it never
        # makes an assertion pass or acts on production/native processes.
        if owned is not None:
            try:
                os.kill(owned, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=4)


def test_live_capture_watchdog_expiry_records_nonzero_outcome(repository):
    run = create(repository)
    produce(run)
    capture = (
        "import sys,types;from pathlib import Path;"
        f"h=Path({str(HELPER)!r});m=types.ModuleType('fixture');m.__file__=str(h);"
        "exec(compile(h.read_bytes(),str(h),'exec'),m.__dict__);"
        "m.DIAGNOSTIC_COMMAND_SECONDS=0.2;m.DIAGNOSTIC_KILL_GRACE_SECONDS=0.1;"
        f"sys.exit(m.run_diagnostic(Path({run['manifest']!r}),'expired',"
        "[sys.executable,'-c','import time;time.sleep(120)']))"
    )
    result = command(sys.executable, str(HELPER), "run", "--manifest", run["manifest"],
                     "--", sys.executable, "-c", capture)
    assert result.returncode in {124, 137}
    receipt = json.loads((Path(run["diagnostics_dir"]) / "expired.json").read_text())
    assert receipt["state"] == "completed"
    assert receipt["exit_code"] == result.returncode
    assert receipt["watchdog_or_signal_failure"] is True
    assert "diagnostic label=expired completed" in Path(run["log_file"]).read_text()
    assert "diagnostic capture incomplete" in action(run, "validate", success=False)
