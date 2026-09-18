#!/usr/bin/env python3
"""Own one daily producer's isolated worktree; never clean the owner's checkout.

This tool does not commit, push, rebase, or delete branches. Verified completed
checkouts may retire; immutable proof, manifests, branches and logs are retained.
Use one canonical state directory for cron and manual producers alike.
"""

from __future__ import annotations

import argparse
import contextlib
import contextvars
import datetime as dt
import fcntl
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import types
import uuid
from pathlib import Path

DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"
FEEDBACK = ".claude/skills/blog-backfill/methodology/feedback.jsonl"
ACTIVE = {"creating", "ready", "sealed", "pending_publication"}
PIPELINE_LOCK = Path("/tmp/blog-pipeline.lock")
RUNTIME_PATHS = {
    ".hugo_build.lock",
    ".beads/export-state.json",
    ".claude/skills/blog-backfill/methodology/index.db",
    ".claude/skills/blog-backfill/methodology/index.db.rebuild.lock",
}
# SessionStart/PreCompact `bd prime` creates these already-ignored local runtime
# stores. Tracked Beads records/config and all other paths remain write-set errors.
RUNTIME_PREFIXES = ("public/", "resources/_gen/", ".beads/backup/", ".beads/embeddeddolt/")
RESERVE_BYTES = 500 * 1024 * 1024
ARCHIVE_LIMIT_BYTES = 64 * 1024 * 1024
INVENTORY_LIMIT_BYTES = 16 * 1024 * 1024
INVENTORY_MAX_FILES = 100_000
INVENTORY_MAX_CONTENT = 8 * 1024 * 1024 * 1024
RETIREMENT_IDENTITY = (
    "date", "run_id", "workspace", "branch", "status", "source_repo", "common_dir",
    "remote_url", "baseline_sha", "published_sha", "quality_seal_sha256", "delivery_status",
)
RETIREMENT_LOCK_FDS = contextvars.ContextVar("retirement_lock_fds", default=())
RETIREMENT_GIT_TIMEOUT_SECONDS = 60
RETIREMENT_GIT_KILL_GRACE_SECONDS = 5
RETIREMENT_GIT_CAPTURE_GRACE_SECONDS = 5
DIAGNOSTICS_MAX_LABELS = 16
DIAGNOSTICS_MAX_ATTEMPTS = 8
DIAGNOSTICS_LOG_BYTES = 1024 * 1024
DIAGNOSTICS_RECEIPT_BYTES = 4096
DIAGNOSTICS_TOTAL_BYTES = DIAGNOSTICS_MAX_LABELS * (
    DIAGNOSTICS_LOG_BYTES + DIAGNOSTICS_RECEIPT_BYTES
)
DIAGNOSTIC_COMMAND_SECONDS = 60
DIAGNOSTIC_KILL_GRACE_SECONDS = 5
# GNU timeout exits as soon as its command exits. Keep the monitored process alive
# until adopted Git descendants exit, and after timeout's TERM, so KILL covers
# descendants still holding the same lock descriptions. No PID/group reuse: the
# watchdog remains the process-group leader throughout its termination grace.
RETIREMENT_GIT_KEEPER = """
import ctypes, os, signal, subprocess, sys
if ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
    print("retirement watchdog cannot establish descendant ownership", file=sys.stderr)
    sys.exit(125)
expired = False
def deadline(signum, frame):
    global expired
    expired = True
signal.signal(signal.SIGTERM, deadline)
child = subprocess.Popen(sys.argv[2:], pass_fds=tuple(map(int, sys.argv[1].split(','))))
status = child.wait()
# Adopt and reap Git descendants before exiting, even when Git itself succeeds.
# A hung adopted child keeps the external watchdog and its group alive.
while True:
    try:
        os.waitpid(-1, 0)
    except ChildProcessError:
        break
if expired:
    while True:
        signal.pause()
sys.exit(status if status >= 0 else 128 - status)
"""


class WorkspaceError(Exception):
    """A fail-closed ownership or publication boundary."""


class BoundedArchiveWriter:
    """Count tar headers/padding too; never retain an oversized temporary archive."""

    def __init__(self, stream):
        self.stream = stream

    def tell(self):
        return self.stream.tell()

    def write(self, value):
        if self.tell() + len(value) > ARCHIVE_LIMIT_BYTES:
            raise WorkspaceError("serialized retirement archive exceeds bounded evidence limit")
        return self.stream.write(value)


def git_result(repo: Path, *args: str) -> subprocess.CompletedProcess:
    descriptors = RETIREMENT_LOCK_FDS.get()
    command = ["git", "-C", str(repo), *args]
    capture_deadline = 60
    if descriptors:
        command = [
            "/usr/bin/timeout", "--signal=TERM",
            f"--kill-after={RETIREMENT_GIT_KILL_GRACE_SECONDS}",
            str(RETIREMENT_GIT_TIMEOUT_SECONDS), sys.executable, "-c",
            RETIREMENT_GIT_KEEPER, ",".join(map(str, descriptors)), *command,
        ]
        capture_deadline = (RETIREMENT_GIT_TIMEOUT_SECONDS
                            + RETIREMENT_GIT_KILL_GRACE_SECONDS
                            + RETIREMENT_GIT_CAPTURE_GRACE_SECONDS)
    try:
        result = subprocess.run(command, capture_output=True, check=False,
                                timeout=capture_deadline, pass_fds=descriptors)
    except subprocess.TimeoutExpired as exc:
        raise WorkspaceError("Git operation exceeded the 60-second deadline") from exc
    if descriptors and result.returncode in {124, 137, -9}:
        raise WorkspaceError("retirement Git timed out or was killed under the bounded watchdog")
    return result


def git(repo: Path, *args: str) -> bytes:
    proc = git_result(repo, *args)
    if proc.returncode:
        raise WorkspaceError(proc.stderr.decode(errors="replace").strip())
    return proc.stdout


def stamp() -> str:
    return dt.datetime.now(dt.UTC).isoformat()


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(".tmp")
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def event(manifest: dict, message: str) -> None:
    log_path = Path(manifest["workspace"]).parent / "run.log"
    fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a") as stream:
        stream.write(f"{stamp()} {message}\n")
        stream.flush()
        os.fsync(stream.fileno())


def identity(date: str, run_id: str) -> None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise WorkspaceError("date must be YYYY-MM-DD")
    try:
        dt.date.fromisoformat(date)
    except ValueError as exc:
        raise WorkspaceError("date must be a real calendar date") from exc
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run_id):
        raise WorkspaceError("run-id must be a safe 1-64 character identifier")


def safe_file(root: Path, relative: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise WorkspaceError(f"path escapes workspace: {relative}")
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise WorkspaceError(f"symlink is not a run-owned artifact: {relative}")
    if not current.resolve().is_relative_to(root.resolve()):
        raise WorkspaceError(f"path escapes workspace: {relative}")
    return current


@contextlib.contextmanager
def locked(directory: Path):
    if directory.absolute() != directory.resolve():
        raise WorkspaceError("registry lock directory may not be symlinked")
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    if directory.stat().st_uid != os.getuid():
        raise WorkspaceError("registry lock directory is not owned by current user")
    if directory.stat().st_mode & 0o002:
        raise WorkspaceError("registry lock directory is world-writable")
    descriptor = os.open(directory / "workspace.lock",
                         os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
            raise WorkspaceError("registry lock is not an owned regular file")
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield stream


@contextlib.contextmanager
def producer_lock(run_dir: Path, *, allow_diagnostics: bool = False):
    with (run_dir / "producer.lock").open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise WorkspaceError(
                "producer is still running; workspace cannot be reused or closed"
            ) from exc
        # A killed diagnostic supervisor may have a still-live bounded command.
        # Keep its capture coordination through quarantine/retirement mutations.
        # A new producer releases this probe only after owning the producer lease;
        # unrelated/old ancestors cannot authorize another diagnostic command.
        with contextlib.ExitStack() as cleanup:
            directory = safe_file(run_dir, "diagnostics")
            if directory.exists():
                info = directory.lstat()
                if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
                        or info.st_mode & 0o777 != 0o700):
                    raise WorkspaceError("diagnostic coordination directory is unsafe")
                fd = os.open(directory / "diagnostics.lock",
                             os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
                capture = cleanup.enter_context(os.fdopen(fd, "rb"))
                info = os.fstat(capture.fileno())
                if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                        or info.st_nlink != 1 or info.st_mode & 0o777 != 0o600):
                    raise WorkspaceError("diagnostic coordination lock is unsafe")
                try:
                    fcntl.flock(capture, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as exc:
                    raise WorkspaceError(
                        "diagnostic writer still running; retain run until bounded capture exits"
                    ) from exc
                if allow_diagnostics:
                    capture.close()
            yield stream


@contextlib.contextmanager
def retirement_git_locks(registry_stream, producer_stream):
    """A surviving Git child must retain the same three exclusive lock descriptions."""
    verify_pipeline_lock()
    token = RETIREMENT_LOCK_FDS.set((9, registry_stream.fileno(), producer_stream.fileno()))
    try:
        yield
    finally:
        RETIREMENT_LOCK_FDS.reset(token)


def verify_pipeline_lock() -> None:
    """An env marker is not authority: prove FD9 owns the canonical flock."""
    try:
        descriptor = os.fstat(9)
        canonical = PIPELINE_LOCK.stat()
    except OSError as exc:
        raise WorkspaceError("abandoned recovery requires inherited canonical FD9 lock") from exc
    if (descriptor.st_dev, descriptor.st_ino) != (canonical.st_dev, canonical.st_ino):
        raise WorkspaceError("FD9 is not the canonical pipeline lock inode")
    token = f"{os.major(descriptor.st_dev):02x}:{os.minor(descriptor.st_dev):02x}:"
    token += str(descriptor.st_ino)
    records = Path("/proc/locks").read_text().splitlines()
    if not any("FLOCK" in row and "WRITE" in row and token in row.split() for row in records):
        raise WorkspaceError("canonical FD9 lock was not already held")
    try:
        fcntl.flock(9, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        raise WorkspaceError("FD9 does not own the existing canonical flock") from exc


def optional_blob(repo: Path, sha: str, path: str) -> bytes:
    exists = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{sha}:{path}"],
        capture_output=True,
        check=False,
    )
    return git(repo, "show", f"{sha}:{path}") if exists.returncode == 0 else b""


def remote_master(repo: Path, expected: str) -> str:
    actual = git(repo, "remote", "get-url", "origin").decode().strip()
    if actual != expected:
        raise WorkspaceError("origin does not match the approved remote")
    if re.match(r"https?://[^/]*@", actual):
        raise WorkspaceError("credential-bearing remote URLs are not permitted")
    remote_head = git(repo, "ls-remote", "--symref", "origin", "HEAD").decode()
    if "ref: refs/heads/master\tHEAD" not in remote_head:
        raise WorkspaceError("remote default branch must be master")
    local_head = git_result(repo, "symbolic-ref", "refs/remotes/origin/HEAD")
    if local_head.returncode == 0 and local_head.stdout.strip() != b"refs/remotes/origin/master":
        raise WorkspaceError("configured origin/HEAD is not master")
    git(repo, "fetch", "--no-tags", "origin", "refs/heads/master:refs/remotes/origin/master")
    return git(repo, "rev-parse", "refs/remotes/origin/master").decode().strip()


def registry_for(repo: Path, state_dir: Path) -> Path:
    common = git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()
    state = state_dir.expanduser().absolute()
    if state.resolve() != state:
        raise WorkspaceError("workspace registry may not contain symlinks")
    registry = state / hashlib.sha256(common).hexdigest()[:20]
    if registry.resolve() != registry:
        raise WorkspaceError("workspace registry may not contain symlinks")
    return registry


def secure_owned_registry(registry: Path, common: Path) -> None:
    """Upgrade the old umask-derived registry mode, retaining a resumable audit.

    Caller holds the registry lock. Only its verified directory inode changes;
    owner/state roots and all existing run/quarantine bytes and modes stay intact.
    """
    if (registry.resolve() != registry or registry.name
            != hashlib.sha256(str(common).encode()).hexdigest()[:20]):
        raise WorkspaceError("registry permission upgrade needs exact common-Git identity")
    descriptor = os.open(registry, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(descriptor)
        mode = stat.S_IMODE(info.st_mode)
        if info.st_uid != os.getuid() or mode & 0o777 not in {0o700, 0o750, 0o755, 0o770, 0o775}:
            raise WorkspaceError("registry ownership/mode is unsafe for automatic private upgrade")
        receipt_path = safe_file(registry, "registry-permissions.json")
        receipt = None
        if receipt_path.exists():
            saved = receipt_path.lstat()
            if (not stat.S_ISREG(saved.st_mode) or saved.st_uid != os.getuid()
                    or saved.st_nlink != 1 or saved.st_size > 4096
                    or saved.st_mode & 0o777 != 0o600):
                raise WorkspaceError("registry permission receipt is unsafe")
            receipt = json.loads(receipt_path.read_text())
            if (not isinstance(receipt, dict) or receipt.get("schema_version") != 1
                    or receipt.get("common_dir") != str(common)
                    or receipt.get("registry") != str(registry)
                    or receipt.get("uid") != info.st_uid
                    or receipt.get("device") != info.st_dev or receipt.get("inode") != info.st_ino
                    or receipt.get("state") not in {"prepared", "completed"}):
                raise WorkspaceError("registry permission receipt identity mismatch")
        if mode & 0o777 == 0o700 and (receipt is None or receipt["state"] == "completed"):
            return
        if receipt is None:
            receipt = {"schema_version": 1, "registry": str(registry), "common_dir": str(common),
                       "uid": info.st_uid, "device": info.st_dev, "inode": info.st_ino,
                       "previous_mode": mode, "private_mode": 0o700,
                       "state": "prepared", "prepared_at": stamp()}
            atomic_json(receipt_path, receipt)
        elif mode & 0o777 != 0o700 and mode != receipt.get("previous_mode"):
            raise WorkspaceError("registry mode changed after its prepared permission upgrade")
        current = registry.lstat()
        if (current.st_dev, current.st_ino) != (info.st_dev, info.st_ino):
            raise WorkspaceError("registry inode changed before private permission upgrade")
        os.fchmod(descriptor, 0o700)
        os.fsync(descriptor)
        receipt.update(state="completed", completed_at=stamp())
        atomic_json(receipt_path, receipt)
    finally:
        os.close(descriptor)


def diagnostics_directory(path: Path, manifest: dict, *, register: bool = False) -> Path:
    """Bind diagnostics to this real run, never an environment-selected directory."""
    path = path.absolute()
    directory = path.parent / "diagnostics"
    common_hash = hashlib.sha256(manifest["common_dir"].encode()).hexdigest()[:20]
    if (path.resolve() != path or path.name != "manifest.json"
            or list(path.parent.parts[-4:])
            != [common_hash, "runs", manifest["date"], manifest["run_id"]]
            or path.parent.is_relative_to(Path(manifest["source_repo"]))
            or path.parent.is_relative_to(Path(manifest["common_dir"]))):
        raise WorkspaceError("diagnostics require the exact external run namespace")
    for parent in (path.parent, path.parent.parent, path.parent.parents[1], path.parent.parents[2]):
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
            raise WorkspaceError("diagnostics run directory has unsafe ownership")
    if path.parent.parents[2].stat().st_mode & 0o777 != 0o700:
        raise WorkspaceError("diagnostics require the verified private registry")
    declared = manifest.get("diagnostics_dir")
    if declared is None and register:
        manifest["diagnostics_dir"] = str(directory)
    elif declared != str(directory):
        raise WorkspaceError("diagnostics directory is not registered for this run")
    if register:
        directory.mkdir(mode=0o700, exist_ok=True)
    info = directory.lstat()
    if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
            or stat.S_IMODE(info.st_mode) != 0o700):
        raise WorkspaceError("diagnostics directory must be owned, private and not symlinked")
    return directory


def diagnostic_files(directory: Path) -> dict[str, int]:
    """Bound actual retained bytes, including receipts; never remove prior evidence."""
    files = {}
    for entry in directory.iterdir():
        info = entry.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o600):
            raise WorkspaceError("diagnostics contain a linked, foreign or non-private file")
        if entry.name == "diagnostics.lock":
            limit = 0
        elif re.fullmatch(r"[A-Za-z0-9_-]{1,64}\.(stderr|json|tmp)", entry.name):
            limit = (DIAGNOSTICS_LOG_BYTES if entry.suffix == ".stderr"
                     else DIAGNOSTICS_RECEIPT_BYTES)
        else:
            raise WorkspaceError("diagnostics contain an unregistered filename")
        if info.st_size > limit:
            raise WorkspaceError("diagnostic file exceeds retained byte limit; evidence preserved")
        files[entry.name] = info.st_size
        if (len(files) > DIAGNOSTICS_MAX_LABELS * 2 + 2
                or sum(files.values()) > DIAGNOSTICS_TOTAL_BYTES):
            raise WorkspaceError("diagnostics exceed retained count/byte limit; evidence preserved")
    return files


def verify_diagnostics(manifest: dict) -> None:
    # Historical terminal/sealed manifests stay readable without invented state.
    if "diagnostics_dir" not in manifest:
        return
    path = Path(manifest["workspace"]).parent / "manifest.json"
    directory = diagnostics_directory(path, manifest)
    files = diagnostic_files(directory)
    if any(name.endswith(".tmp") for name in files):
        raise WorkspaceError("interrupted diagnostic receipt retained; replay its diagnostic label")
    labels = {Path(name).stem for name in files if name != "diagnostics.lock"}
    if len(labels) > DIAGNOSTICS_MAX_LABELS:
        raise WorkspaceError("diagnostics exceed registered label count")
    for label in labels:
        receipt_path, output_path = directory / f"{label}.json", directory / f"{label}.stderr"
        if receipt_path.name not in files or output_path.name not in files:
            raise WorkspaceError("diagnostic output has no paired durable receipt")
        receipt = json.loads(receipt_path.read_text())
        if (not isinstance(receipt, dict)
                or type(receipt.get("schema_version")) is not int or receipt["schema_version"] != 1
                or any(receipt.get(key) != manifest[key]
                       for key in ("date", "run_id", "baseline_sha"))
                or receipt.get("label") != label or receipt.get("state") != "completed"
                or type(receipt.get("exit_code")) is not int or receipt["exit_code"] != 0
                or receipt.get("capture_failed") is not False
                or receipt.get("stderr_sha256")
                != hashlib.sha256(output_path.read_bytes()).hexdigest()):
            raise WorkspaceError(
                "diagnostic capture incomplete, failed or changed; evidence preserved"
            )


def prior_diagnostic_receipt(path: Path, manifest: dict, label: str) -> dict:
    receipt = json.loads(path.read_text())
    if (not isinstance(receipt, dict) or type(receipt.get("schema_version")) is not int
            or receipt["schema_version"] != 1 or receipt.get("label") != label
            or any(receipt.get(key) != manifest[key] for key in ("date", "run_id", "baseline_sha"))
            or receipt.get("state") not in {"running", "completed"}
            or not re.fullmatch(r"[0-9a-f]{32}", str(receipt.get("invocation_id", "")))
            or not re.fullmatch(r"[0-9a-f]{32}", str(receipt.get("producer_attempt_id", "")))
            or not isinstance(receipt.get("history", []), list)):
        raise WorkspaceError("prior diagnostic receipt has invalid run identity; evidence retained")
    return receipt


def write_diagnostic_receipt(path: Path, receipt: dict) -> None:
    serialized = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    if len(serialized) > DIAGNOSTICS_RECEIPT_BYTES:
        raise WorkspaceError("diagnostic receipt exceeds metadata bound; evidence retained")
    # Count the temporary replacement alongside the existing receipt and logs,
    # not just the smaller post-rename state.
    if sum(diagnostic_files(path.parent).values()) + len(serialized) > DIAGNOSTICS_TOTAL_BYTES:
        raise WorkspaceError("diagnostic atomic metadata exceeds total capacity; evidence retained")
    atomic_json(path, receipt)


def require_diagnostic_lease(path: Path, manifest: dict) -> None:
    attempt = manifest.get("producer_attempt", {})
    if (manifest["status"] != "ready" or manifest.get("quality_seal_sha256")
            or attempt.get("state") != "running"
            or any(attempt.get(key) != manifest[key]
                   for key in ("date", "run_id", "baseline_sha"))):
        raise WorkspaceError("diagnostic command requires the active owning producer lease")
    lease = safe_file(path.parent, "producer.lock").stat()
    token = f"{os.major(lease.st_dev):02x}:{os.minor(lease.st_dev):02x}:{lease.st_ino}"
    ancestors, process = set(), os.getpid()
    while process > 0 and process not in ancestors:
        ancestors.add(process)
        try:
            process = int(Path(f"/proc/{process}/stat").read_text().rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            break
    # Native Bash tools close non-stdio FDs. The actual runner must still be a
    # live ancestor holding this kernel lease; an unrelated lock holder is not authority.
    for row in Path("/proc/locks").read_text().splitlines():
        fields = row.split()
        if (len(fields) > 5 and "FLOCK" in fields and "WRITE" in fields
                and token in fields and int(fields[4]) in ancestors):
            return
    raise WorkspaceError("diagnostic command requires the held owning producer lease")


def run_diagnostic(path: Path, label: str, argv: list[str]) -> int:
    """Pass stdout through; bound stderr persistence without changing child success."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", label):
        raise WorkspaceError("a safe diagnostic label is required")
    if argv and argv[0] == "--":
        argv = argv[1:]
    if not argv:
        raise WorkspaceError("diagnostic requires a command after --")
    manifest = load(path)
    directory = diagnostics_directory(path, manifest)
    require_diagnostic_lease(path, manifest)
    descriptor = os.open(directory / "diagnostics.lock",
                         os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(descriptor, "rb") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise WorkspaceError("another diagnostic command holds capture lease") from exc
        manifest = load(path)
        diagnostics_directory(path, manifest)
        require_diagnostic_lease(path, manifest)
        files = diagnostic_files(directory)
        labels = {Path(name).stem for name in files if name != "diagnostics.lock"}
        output_path, receipt_path = directory / f"{label}.stderr", directory / f"{label}.json"
        temporary = receipt_path.with_suffix(".tmp")
        if temporary.name in files:
            # An atomic-write crash may leave a complete fsynced receipt before
            # rename. Replay only this validated run/label; never discard unknown
            # or incomplete bytes. Running remains running, not inferred success.
            pending = prior_diagnostic_receipt(temporary, manifest, label)
            if pending["state"] == "completed" and (
                not output_path.is_file() or pending.get("stderr_sha256")
                != hashlib.sha256(output_path.read_bytes()).hexdigest()
            ):
                raise WorkspaceError("interrupted receipt does not match retained stderr")
            temporary.replace(receipt_path)
            descriptor = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            event(manifest, f"diagnostic label={label} recovered interrupted receipt rename")
            files = diagnostic_files(directory)
        if any(name.endswith(".tmp") for name in files):
            raise WorkspaceError("another interrupted diagnostic label requires explicit replay")
        history = []
        if receipt_path.name in files:
            prior = prior_diagnostic_receipt(receipt_path, manifest, label)
            if prior["state"] == "completed" and prior.get("stderr_sha256") != hashlib.sha256(
                output_path.read_bytes()
            ).hexdigest():
                raise WorkspaceError("prior diagnostic stderr changed; evidence retained")
            history = [*prior.get("history", []), {
                key: prior[key] for key in (
                    "invocation_id", "producer_attempt_id", "state", "started_at",
                    "finished_at", "exit_code", "capture_failed", "stderr_offset",
                    "stderr_seen_bytes", "stderr_stored_bytes", "omitted_bytes",
                ) if key in prior
            }]
        if len(history) >= DIAGNOSTICS_MAX_ATTEMPTS:
            raise WorkspaceError("diagnostic attempt capacity exhausted; all evidence retained")
        size = files.get(output_path.name, 0)
        if label not in labels and len(labels) >= DIAGNOSTICS_MAX_LABELS:
            raise WorkspaceError("diagnostic label capacity exhausted; previous evidence retained")
        if size >= DIAGNOSTICS_LOG_BYTES:
            raise WorkspaceError("diagnostic byte capacity exhausted; previous evidence retained")
        receipt = {
            "schema_version": 1, "label": label, "invocation_id": uuid.uuid4().hex,
            **{key: manifest[key] for key in ("date", "run_id", "baseline_sha")},
            "producer_attempt_id": manifest["producer_attempt"]["attempt_id"],
            "state": "running", "started_at": stamp(), "stderr_offset": size,
            "history": history,
        }
        # Reserve metadata space as well as remaining stderr capacity before launch.
        remaining = min(DIAGNOSTICS_LOG_BYTES - size,
                        DIAGNOSTICS_TOTAL_BYTES - sum(files.values())
                        - DIAGNOSTICS_RECEIPT_BYTES)
        if remaining <= 0:
            raise WorkspaceError("diagnostic total capacity exhausted; previous evidence retained")
        output_fd = os.open(output_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW,
                            0o600)
        with os.fdopen(output_fd, "ab", buffering=0) as output:
            # Leave enough reserved metadata for completion before launching.
            completion = {**receipt, "finished_at": stamp(), "exit_code": 255,
                          "stderr_seen_bytes": 10**20, "stderr_stored_bytes": 10**20,
                          "omitted_bytes": 10**20, "capture_failed": True,
                          "stderr_sha256": "0" * 64}
            if len((json.dumps(completion, indent=2, sort_keys=True) + "\n").encode()) > (
                DIAGNOSTICS_RECEIPT_BYTES
            ):
                raise WorkspaceError("diagnostic metadata capacity exhausted; evidence retained")
            write_diagnostic_receipt(receipt_path, receipt)
            event(manifest, f"diagnostic label={label} started "
                  f"invocation={receipt['invocation_id']}")
            seen = stored = 0
            # The controller survives this capture process being killed. The
            # existing subreaper keeps ordinary descendants inside timeout's
            # process group even when their original command exits early.
            command = ["/usr/bin/timeout", "--signal=TERM",
                       f"--kill-after={DIAGNOSTIC_KILL_GRACE_SECONDS}",
                       str(DIAGNOSTIC_COMMAND_SECONDS), sys.executable, "-c",
                       RETIREMENT_GIT_KEEPER.replace("retirement watchdog", "diagnostic watchdog"),
                       str(lock.fileno()), *argv]
            with subprocess.Popen(command, cwd=manifest["workspace"], stderr=subprocess.PIPE,
                                  pass_fds=(lock.fileno(),)) as child:
                # No stderr enters memory without a bound. Overflow is drained
                # under the surviving local-command deadline and explicitly fails.
                while chunk := child.stderr.read1(65536):
                    seen += len(chunk)
                    keep = chunk[:max(0, remaining - stored)]
                    output.write(keep)
                    stored += len(keep)
                    os.fsync(output.fileno())
                code = child.wait()
            code = code if code >= 0 else 128 - code
        receipt.update(state="completed", finished_at=stamp(), exit_code=code,
                       stderr_seen_bytes=seen, stderr_stored_bytes=stored,
                       omitted_bytes=seen - stored, capture_failed=seen != stored,
                       stderr_sha256=hashlib.sha256(output_path.read_bytes()).hexdigest())
        if code in {124, 137}:
            receipt["watchdog_or_signal_failure"] = True
        write_diagnostic_receipt(receipt_path, receipt)
        event(manifest, f"diagnostic label={label} completed exit_code={code} "
              f"stored={stored} omitted={seen - stored} capture_failed={seen != stored}")
        if seen != stored:
            print(f"diagnostic capture exceeded capacity: stored={stored} omitted={seen - stored}; "
                  "bounded evidence retained outside publication checkout", file=sys.stderr)
        return code or (65 if seen != stored else 0)


def allocated_bytes(path: Path) -> int:
    """Count actual allocated bytes without following any link or changing files."""
    if not path.exists() and not path.is_symlink():
        return 0
    total = path.lstat().st_blocks * 512
    if path.is_dir() and not path.is_symlink():
        for parent, directories, files in os.walk(path, followlinks=False):
            for name in directories + files:
                total += (Path(parent) / name).lstat().st_blocks * 512
    return total


def census(repo: Path, state_dir: Path) -> dict:
    registry = registry_for(repo, state_dir)
    runs = []
    for path in sorted(registry.glob("runs/*/*/manifest.json")):
        safe_file(registry, str(path.relative_to(registry)))
        manifest = load(path, require_workspace=False)
        status = manifest["status"]
        candidate = status == "noop" or (
            status == "published" and manifest.get("delivery_status") == "complete"
        )
        workspace_bytes = allocated_bytes(Path(manifest["workspace"]))
        runs.append({
            "date": manifest["date"], "run_id": manifest["run_id"], "status": status,
            "delivery_status": manifest.get("delivery_status"),
            "registry_bytes": allocated_bytes(path.parent), "workspace_bytes": workspace_bytes,
            "quarantine_bytes": allocated_bytes(path.parent / "quarantine"),
            "diagnostics_bytes": allocated_bytes(path.parent / "diagnostics"),
            "retired": manifest.get("checkout_retirement", {}).get("state") == "retired",
            "protected_reason": ("completed-requires-verification" if candidate
                                 else "unfinished-or-quarantined") if workspace_bytes else None,
        })
    return {"registry": str(registry), "registry_bytes": allocated_bytes(registry),
            "workspace_bytes": sum(row["workspace_bytes"] for row in runs),
            "protected_bytes": sum(row["workspace_bytes"] for row in runs
                                   if row["protected_reason"]), "runs": runs}


def admission(repo: Path, state_dir: Path, baseline: str) -> dict:
    report = census(repo, state_dir)
    # Account for tiny files' allocation as well as large media; Hugo copies most
    # content into public/, so reserve a second full checkout plus transaction room.
    tracked = 0
    for row in git(repo, "ls-tree", "-r", "-l", "-z", baseline).split(b"\0"):
        if not row:
            continue
        fields = row.split(b"\t", 1)[0].split()
        if fields[1] == b"blob":
            tracked += ((int(fields[3]) + 4095) // 4096) * 4096
    target = Path(report["registry"])
    while not target.exists():
        target = target.parent
    available = shutil.disk_usage(target).free
    required = tracked * 2 + RESERVE_BYTES
    return {**report, "tracked_allocated_estimate": tracked,
            "required_free_bytes": required, "available_bytes": available,
            "admitted": available >= required}


def retirement_files(root: Path, manifest: dict) -> list[str]:
    if git(root, "diff", "HEAD", "--") or git(root, "diff", "--cached", "--"):
        raise WorkspaceError("retirement protects changed tracked files")
    others = set()
    for flags in (("--exclude-standard",), ("--ignored", "--exclude-standard")):
        others.update(names(root, "ls-files", "--others", "-z", *flags))
    retained = []
    for relative in sorted(others):
        path = safe_file(root, relative)
        if not stat.S_ISREG(path.lstat().st_mode):
            raise WorkspaceError("retirement protects nonregular workspace artifacts")
        if relative.startswith(("public/", "resources/_gen/")) or relative in RUNTIME_PATHS:
            if relative.startswith(".beads/"):
                raise WorkspaceError("retirement protects local Beads state pending review")
            continue
        staged = relative == manifest["permitted_staging_path"] or (
            relative.startswith(f".blog-staging/{manifest['date']}.{manifest['run_id']}.")
            and relative.endswith(".json")
        )
        if relative.startswith(RUNTIME_PREFIXES[2:]):
            raise WorkspaceError("retirement protects local Beads state pending review")
        if not staged:
            raise WorkspaceError("retirement protects unexpected workspace artifacts")
        retained.append(relative)
    return retained


def submodule_evidence(root: Path) -> dict:
    """Retain every byte of clean, run-private initialized submodules and their refs."""
    worktree_gitdir = Path(git(root, "rev-parse", "--absolute-git-dir").decode().strip())
    if (worktree_gitdir / "locked").exists():
        raise WorkspaceError("retirement protects locked worktrees")
    files, gitlinks = {}, {}

    def inventory(directory: Path, prefix: str) -> None:
        if directory.resolve() != directory:
            raise WorkspaceError("submodule evidence path may not contain symlinks")
        for parent, directories, names_ in os.walk(directory, followlinks=False):
            for name in directories + names_:
                path = Path(parent) / name
                mode = path.lstat().st_mode
                if stat.S_ISDIR(mode):
                    continue
                if not stat.S_ISREG(mode) or path.stat().st_uid != os.getuid():
                    raise WorkspaceError("retirement protects foreign submodule evidence")
                if path.name == "alternates" and path.stat().st_size:
                    raise WorkspaceError("retirement protects external submodule object stores")
                files[f"{prefix}/{path.relative_to(directory)}"] = path

    def visit(parent: Path) -> None:
        for record in git(parent, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
            if not record:
                continue
            info, relative = record.split(b"\t", 1)
            mode, _kind, expected = info.split()
            if mode != b"160000":
                continue
            module = safe_file(parent, os.fsdecode(relative))
            entry = {"commit": expected.decode(), "initialized": (module / ".git").exists()}
            gitlinks[str(module.relative_to(root))] = entry
            if not (module / ".git").exists():
                if module.exists() and any(module.iterdir()):
                    raise WorkspaceError("retirement protects uninitialized submodule contents")
                continue
            gitdir = Path(git(module, "rev-parse", "--absolute-git-dir").decode().strip())
            common = Path(git(module, "rev-parse", "--path-format=absolute", "--git-common-dir")
                          .decode().strip())
            module_top = Path(git(module, "rev-parse", "--show-toplevel").decode().strip())
            if (not gitdir.is_relative_to(worktree_gitdir) or gitdir == worktree_gitdir
                    or common != gitdir or gitdir.resolve() != gitdir
                    or module_top != module):
                raise WorkspaceError("retirement protects shared or external submodule Git data")
            entry["gitdir"] = str(gitdir)
            if git(module, "rev-parse", "HEAD").strip() != expected:
                raise WorkspaceError("retirement protects changed submodule HEAD")
            if git(module, "status", "--porcelain", "--untracked-files=all", "--ignored"):
                raise WorkspaceError("retirement protects dirty submodule bytes")
            git(module, "fsck", "--connectivity-only", "--no-dangling")
            inventory(module, f"submodule-workspace/{module.relative_to(root)}")
            inventory(gitdir, f"submodule-git/{gitdir.relative_to(worktree_gitdir)}")
            visit(module)

    visit(root)
    return {"files": files, "gitlinks": gitlinks}


def retirement_proof(path: Path, manifest: dict) -> dict:
    """Verify publication before recording authority to remove only this checkout."""
    root = Path(manifest["workspace"])
    check_workspace(manifest)
    verify_diagnostics(manifest)
    files = retirement_files(root, manifest)
    modules = submodule_evidence(root)
    if manifest["status"] == "published" and manifest.get("delivery_status") == "complete":
        # Loading the verifier must not create __pycache__ inside a run checkout.
        module_path = Path(__file__).with_name("blog_publication_state.py")
        publication = types.ModuleType("retirement_publication")
        publication.__file__ = str(module_path)
        exec(compile(module_path.read_bytes(), str(module_path), "exec"), publication.__dict__)
        seal = publication.read_quality_seal(path, manifest)
        published = manifest["published_sha"]
        remote = remote_master(root, manifest["remote_url"])
        git(root, "merge-base", "--is-ancestor", published, remote)
        for name, expected in seal["artifact_hashes"].items():
            if hashlib.sha256(git(root, "show", f"{published}:{name}")).hexdigest() != expected:
                raise WorkspaceError("published artifacts differ from immutable quality proof")
        public_hash = hashlib.sha256(git(root, "show", f"{remote}:{seal['post']}")).hexdigest()
        if public_hash != seal["receipt"]["post_sha256"]:
            raise WorkspaceError("authoritative post changed after quality approval")
        posts = list(seal["artifact_hashes"])
        proof = ["quality-seal.json", "quality-proof/sentinel.json",
                 f"quality-proof/{manifest['run_id']}.jsonl"]
    elif manifest["status"] == "noop":
        published = manifest["baseline_sha"]
        if git(root, "rev-parse", "HEAD").decode().strip() != published:
            raise WorkspaceError("no-op checkout changed since completion")
        posts = manifest.get("existing_posts", [])
        if not posts or files:
            raise WorkspaceError("no-op retirement requires unchanged source and target archive")
        remote = remote_master(root, manifest["remote_url"])
        for post in posts:
            if (not post.startswith("content/posts/") or not post.endswith(".md")
                    or git(root, "show", f"{published}:{post}")
                    != git(root, "show", f"{remote}:{post}")
                    or post_date(safe_file(root, post).read_text()) != manifest["date"]):
                raise WorkspaceError("no-op target no longer matches authoritative publication")
        proof = []
    else:
        raise WorkspaceError("retirement protects unfinished or quarantined runs")
    return {"published_sha": published, "artifacts": posts, "auxiliary_files": files,
            "submodule_files": {name: str(value) for name, value in modules["files"].items()},
            "gitlinks": modules["gitlinks"],
            "proof_hashes": {
                name: hashlib.sha256(safe_file(path.parent, name).read_bytes()).hexdigest()
                for name in proof}}


def file_identity(path: Path) -> dict:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid():
            raise WorkspaceError("retirement inventory protects foreign or nonregular files")
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
        after = os.fstat(stream.fileno())
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_ino, after.st_size, after.st_mtime_ns
        ):
            raise WorkspaceError("retirement inventory changed during hashing")
    return {"sha256": digest, "mode": stat.S_IMODE(before.st_mode),
            "uid": before.st_uid, "bytes": before.st_size, "dev": before.st_dev}


def directory_identity(path: Path) -> dict:
    value = path.lstat()
    if not stat.S_ISDIR(value.st_mode) or value.st_uid != os.getuid():
        raise WorkspaceError("retirement inventory protects foreign or linked directories")
    return {"mode": stat.S_IMODE(value.st_mode), "uid": value.st_uid,
            "dev": value.st_dev, "inode": value.st_ino}


def tree_inventory(root: Path) -> dict:
    identity_ = directory_identity(root)
    directories, files = {".": identity_}, {}
    size = 0
    for parent, dirs, names_ in os.walk(root, followlinks=False):
        for name in dirs:
            path = Path(parent) / name
            value = directory_identity(path)
            if value["dev"] != identity_["dev"]:
                raise WorkspaceError("retirement inventory cannot cross filesystems")
            directories[str(path.relative_to(root))] = value
            if len(files) + len(directories) > INVENTORY_MAX_FILES:
                raise WorkspaceError("retirement inventory exceeds bounded checkout limit")
        for name in names_:
            path = Path(parent) / name
            if size + path.lstat().st_size > INVENTORY_MAX_CONTENT:
                raise WorkspaceError("retirement inventory exceeds bounded checkout limit")
            value = file_identity(safe_file(root, str(path.relative_to(root))))
            if value["dev"] != identity_["dev"]:
                raise WorkspaceError("retirement inventory cannot cross filesystems")
            files[str(path.relative_to(root))] = value
            size += value["bytes"]
            if len(files) + len(directories) > INVENTORY_MAX_FILES or size > INVENTORY_MAX_CONTENT:
                raise WorkspaceError("retirement inventory exceeds bounded checkout limit")
    return {"path": str(root), "directories": directories, "files": files}


def remaining_inventory(root: Path, expected: dict) -> dict | None:
    if not root.exists() and not root.is_symlink():
        return None
    current = tree_inventory(root)
    for section in ("directories", "files"):
        if any(expected[section].get(name) != value for name, value in current[section].items()):
            raise WorkspaceError("retirement remainder contains new or changed owned bytes")
    return current


def remove_proved_remainder(root: Path, expected: dict) -> None:
    """No recursive delete: remove only exact unchanged entries in prepared inventory."""
    current = remaining_inventory(root, expected)
    if current is None:
        return
    for name, identity_ in current["files"].items():
        path = safe_file(root, name)
        if file_identity(path) != identity_:
            raise WorkspaceError("retirement file changed before unlink")
        path.unlink()
    for name, identity_ in sorted(current["directories"].items(),
                                  key=lambda entry: len(Path(entry[0]).parts), reverse=True):
        path = root if name == "." else safe_file(root, name)
        if directory_identity(path) != identity_:
            raise WorkspaceError("retirement directory changed before removal")
        path.rmdir()  # A newly appearing entry makes this fail rather than deleting it.
    descriptor = os.open(root.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def validate_retirement_git_identity(manifest: dict, receipt: dict) -> None:
    source = Path(manifest["source_repo"])
    common = git(source, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    if common != manifest["common_dir"]:
        raise WorkspaceError("retirement common Git identity changed")
    if git(source, "remote", "get-url", "origin").decode().strip() != manifest["remote_url"]:
        raise WorkspaceError("retirement source remote identity changed")
    admin = Path(receipt["worktree_gitdir"])
    if admin.parent != Path(common) / "worktrees" or admin.resolve() != admin:
        raise WorkspaceError("retirement Git admin escaped its exact private directory")
    if (admin / "locked").exists():
        raise WorkspaceError("retirement protects locked worktrees")
    registered = git(source, "worktree", "list", "--porcelain").decode()
    for block in registered.split("\n\n"):
        if f"worktree {manifest['workspace']}\n" not in block + "\n":
            continue
        for line in block.splitlines():
            if ((admin / "HEAD").exists() and line.startswith("HEAD ")
                    and line != f"HEAD {receipt['head']}"):
                raise WorkspaceError("retirement registered HEAD changed")
            if line.startswith("branch ") and line != f"branch refs/heads/{manifest['branch']}":
                raise WorkspaceError("retirement registered branch changed")
            if line.startswith("locked"):
                raise WorkspaceError("retirement protects locked worktrees")


def retire_checkout(path: Path, manifest: dict) -> None:
    """Prepared archive is durable before Git removes the registered checkout.

    A missing checkout is accepted only after a matching prepared journal. No
    general forced removal, branch deletion, or worktree pruning is permitted.
    Git's clean-submodule guard alone permits one --force with archived module data.
    """
    root = Path(manifest["workspace"])
    if root.is_symlink():
        raise WorkspaceError("retirement checkout may not be symlinked")
    receipt_path = safe_file(path.parent, "checkout-retirement.json")
    archive_path = safe_file(path.parent, "checkout-evidence.tar")
    inventory_path = safe_file(path.parent, "checkout-inventory.json")
    resumed = receipt_path.exists()
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        if (receipt.get("schema_version") != 1
                or receipt.get("state") not in ("prepared", "retired")):
            raise WorkspaceError("unsupported retirement journal")
        for key in RETIREMENT_IDENTITY:
            if receipt[key] != manifest.get(key):
                raise WorkspaceError("retirement journal identity mismatch")
        if receipt["archive_sha256"] != hashlib.sha256(archive_path.read_bytes()).hexdigest():
            raise WorkspaceError("retirement evidence archive changed")
        for name, expected in receipt["proof_hashes"].items():
            if hashlib.sha256(safe_file(path.parent, name).read_bytes()).hexdigest() != expected:
                raise WorkspaceError("retirement immutable proof changed")
        retained_head = git(
            Path(manifest["source_repo"]), "rev-parse", manifest["branch"]
        ).decode().strip()
        if retained_head != receipt["head"]:
            raise WorkspaceError("retirement retained branch changed")
        if inventory_path.stat().st_size > INVENTORY_LIMIT_BYTES:
            raise WorkspaceError("retirement inventory exceeds bounded metadata limit")
        raw_inventory = inventory_path.read_bytes()
        if hashlib.sha256(raw_inventory).hexdigest() != receipt["inventory_sha256"]:
            raise WorkspaceError("retirement inventory changed")
        inventory = json.loads(raw_inventory)
        if (inventory.get("schema_version") != 1
                or inventory["checkout"]["path"] != str(root)
                or inventory["git_admin"]["path"] != receipt["worktree_gitdir"]):
            raise WorkspaceError("retirement inventory identity mismatch")
    else:
        details = retirement_proof(path, manifest)
        head = git(root, "rev-parse", "HEAD").decode().strip()
        admin = Path(git(root, "rev-parse", "--absolute-git-dir").decode().strip())
        if admin.parent != Path(manifest["common_dir"]) / "worktrees":
            raise WorkspaceError("retirement needs an exact run-private Git admin directory")
        admin_inventory = tree_inventory(admin)
        module_paths = set(details["submodule_files"].values())
        details["admin_files"] = {
            f"worktree-git/{name}": str(admin / name)
            for name in admin_inventory["files"] if str(admin / name) not in module_paths
        }
        archive_size = sum(int(git(root, "cat-file", "-s", f"{details['published_sha']}:{name}"))
                           for name in details["artifacts"])
        archive_size += sum(safe_file(root, name).stat().st_size
                            for name in details["auxiliary_files"])
        archive_size += sum(Path(value).stat().st_size
                            for value in details["submodule_files"].values())
        archive_size += sum(Path(value).stat().st_size for value in details["admin_files"].values())
        if archive_size > ARCHIVE_LIMIT_BYTES:
            raise WorkspaceError("retirement archive exceeds bounded evidence limit")
        contents = {f"committed/{name}": git(root, "show", f"{details['published_sha']}:{name}")
                    for name in details["artifacts"]}
        contents.update({f"workspace/{name}": safe_file(root, name).read_bytes()
                         for name in details["auxiliary_files"]})
        contents.update({name: Path(value).read_bytes()
                         for name, value in details["submodule_files"].items()})
        contents.update({name: Path(value).read_bytes()
                         for name, value in details["admin_files"].items()})
        if sum(map(len, contents.values())) > ARCHIVE_LIMIT_BYTES:
            raise WorkspaceError("retirement archive exceeds bounded evidence limit")
        temporary = safe_file(path.parent, "checkout-evidence.tmp")
        # Before the journal exists the original checkout is still authoritative;
        # rewriting our own interrupted temporary archive cannot lose evidence.
        fd = os.open(temporary, os.O_CREAT | os.O_TRUNC | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "wb") as stream:
            with tarfile.open(fileobj=BoundedArchiveWriter(stream), mode="w") as archive:
                for name, content in sorted(contents.items()):
                    member = tarfile.TarInfo(name)
                    member.size, member.mode = len(content), 0o600
                    if name in details["submodule_files"]:
                        member.mode = Path(details["submodule_files"][name]).stat().st_mode & 0o777
                    elif name in details["admin_files"]:
                        member.mode = Path(details["admin_files"][name]).stat().st_mode & 0o777
                    archive.addfile(member, io.BytesIO(content))
            stream.flush()
            os.fsync(stream.fileno())
        if temporary.stat().st_size > ARCHIVE_LIMIT_BYTES:
            raise WorkspaceError("serialized retirement archive exceeds bounded evidence limit")
        temporary.replace(archive_path)
        inventory = {"schema_version": 1, "checkout": tree_inventory(root),
                     "git_admin": tree_inventory(admin)}
        if inventory["git_admin"] != admin_inventory:
            raise WorkspaceError("private Git evidence changed while archiving")
        encoded_inventory = (json.dumps(inventory, indent=2, sort_keys=True) + "\n").encode()
        if len(encoded_inventory) > INVENTORY_LIMIT_BYTES:
            raise WorkspaceError("retirement inventory exceeds bounded metadata limit")
        atomic_json(inventory_path, inventory)
        if inventory_path.stat().st_size > INVENTORY_LIMIT_BYTES:
            raise WorkspaceError("written retirement inventory exceeds bounded metadata limit")
        receipt = {"schema_version": 1, "state": "prepared", "prepared_at": stamp(),
                   **{key: manifest.get(key) for key in RETIREMENT_IDENTITY},
                   **details, "head": head,
                   "worktree_gitdir": str(admin),
                   "inventory_sha256": hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
                   "discarded_derived_categories": ["public/", "resources/_gen/",
                                                    "Hugo lock", "methodology index"],
                   "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
                   "auxiliary_hashes": {
                       name: hashlib.sha256(contents[f"workspace/{name}"]).hexdigest()
                       for name in details["auxiliary_files"]},
                   "submodule_hashes": {name: hashlib.sha256(contents[name]).hexdigest()
                                        for name in details["submodule_files"]}}
        atomic_json(receipt_path, receipt)
    validate_retirement_git_identity(manifest, receipt)
    remaining_root = remaining_inventory(root, inventory["checkout"])
    admin = Path(receipt["worktree_gitdir"])
    remaining_admin = remaining_inventory(admin, inventory["git_admin"])
    partial = (remaining_root != inventory["checkout"]
               or remaining_admin != inventory["git_admin"])
    if partial:
        if not resumed or not receipt.get("removal_started_at"):
            raise WorkspaceError("checkout changed before authorized Git removal started")
        # A killed Git removal leaves an unchanged subset. Validate BOTH trees
        # before unlinking any remainder; all module/admin bytes are archived.
        remove_proved_remainder(root, inventory["checkout"])
    if root.exists():
        current = retirement_proof(path, manifest)
        if (git(root, "rev-parse", "HEAD").decode().strip() != receipt["head"]
                or current["proof_hashes"] != receipt["proof_hashes"]
                or current["auxiliary_files"] != receipt["auxiliary_files"]
                or current["gitlinks"] != receipt["gitlinks"]
                or current["submodule_files"] != receipt["submodule_files"]
                or any(hashlib.sha256(Path(value).read_bytes()).hexdigest()
                       != receipt["submodule_hashes"][name]
                       for name, value in current["submodule_files"].items())
                or any(hashlib.sha256(safe_file(root, name).read_bytes()).hexdigest() != digest
                       for name, digest in receipt["auxiliary_hashes"].items())):
            raise WorkspaceError("retirement candidate changed after evidence was retained")
        receipt["removal_started_at"] = receipt.get("removal_started_at") or stamp()
        atomic_json(receipt_path, receipt)
        try:
            git(Path(manifest["source_repo"]), "worktree", "remove", str(root))
        except WorkspaceError as exc:
            # Git forbids normal removal even after clean submodule deinit. Only
            # this specific guard permits ONE force flag, after retaining all
            # clean private module bytes/refs. Never override dirty/locked errors.
            if ("working trees containing submodules cannot be moved or removed" not in str(exc)
                    or not receipt["gitlinks"]):
                raise
            if (remaining_inventory(root, inventory["checkout"]) != inventory["checkout"]
                    or remaining_inventory(admin, inventory["git_admin"])
                    != inventory["git_admin"]):
                raise WorkspaceError("prepared inventory changed before submodule removal") from exc
            if (retirement_files(root, manifest) != receipt["auxiliary_files"]
                    or git(root, "rev-parse", "HEAD").decode().strip() != receipt["head"]
                    or any(hashlib.sha256(safe_file(root, name).read_bytes()).hexdigest() != digest
                           for name, digest in receipt["auxiliary_hashes"].items())):
                raise WorkspaceError("workspace changed before submodule checkout removal") from exc
            current_modules = submodule_evidence(root)
            if (current_modules["gitlinks"] != receipt["gitlinks"]
                    or set(current_modules["files"]) != set(receipt["submodule_hashes"])
                    or any(hashlib.sha256(value.read_bytes()).hexdigest()
                           != receipt["submodule_hashes"][name]
                           for name, value in current_modules["files"].items())):
                raise WorkspaceError("submodule evidence changed before checkout removal") from exc
            git(Path(manifest["source_repo"]), "worktree", "remove", "--force", str(root))
    # Git may have removed the directory before a crash while keeping its own
    # registration. Removing that one registered missing path is safe and bounded.
    registered = git(Path(manifest["source_repo"]), "worktree", "list", "--porcelain").decode()
    if f"worktree {root}\n" in registered:
        try:
            git(Path(manifest["source_repo"]), "worktree", "remove", str(root))
        except WorkspaceError as exc:
            if (not root.exists() and receipt["gitlinks"]
                    and "working trees containing submodules cannot be moved or removed"
                    in str(exc)):
                if remaining_inventory(root, inventory["checkout"]) is not None:
                    raise WorkspaceError("checkout reappeared before private Git cleanup") from exc
                remaining_inventory(admin, inventory["git_admin"])
                git(Path(manifest["source_repo"]), "worktree", "remove", "--force", str(root))
            else:
                raise
    # Git may have lost its registration midway through deleting private admin
    # files. Its prepared inventory is the only authority for finishing that path.
    if admin.exists():
        if not receipt.get("removal_started_at") or root.exists():
            raise WorkspaceError("private Git admin cleanup was not authorized")
        remove_proved_remainder(admin, inventory["git_admin"])
    receipt.update(state="retired", retired_at=receipt.get("retired_at") or stamp())
    atomic_json(receipt_path, receipt)
    manifest["checkout_retirement"] = {"state": "retired", "at": receipt["retired_at"],
                                      "archive_sha256": receipt["archive_sha256"]}
    atomic_json(path, manifest)
    event(manifest, "completed checkout retired; branch, immutable proof and logs retained")
    if hashlib.sha256(inventory_path.read_bytes()).hexdigest() != receipt["inventory_sha256"]:
        raise WorkspaceError("completed retirement inventory changed before cleanup")
    inventory_path.unlink()
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def retire_registry(repo: Path, state_dir: Path, expected_remote: str, *,
                    keep: int = 2, min_age_hours: float = 24) -> dict:
    if os.environ.get("BLOG_CANARY") == "1":
        raise WorkspaceError("canary cannot retire retained checkouts")
    verify_pipeline_lock()
    if keep < 0 or min_age_hours < 0 or not math.isfinite(min_age_hours):
        raise WorkspaceError("retention count and minimum age must be nonnegative")
    registry = registry_for(repo, state_dir)
    retired, protected = [], []
    with locked(registry) as registry_stream:
        candidates = []
        for path in registry.glob("runs/*/*/manifest.json"):
            safe_file(registry, str(path.relative_to(registry)))
            manifest = load(path, require_workspace=False)
            if (manifest["source_repo"] != str(repo.resolve())
                    or manifest["remote_url"] != expected_remote):
                raise WorkspaceError("retirement registry publication owner mismatch")
            if (manifest.get("checkout_retirement", {}).get("state") == "retired"
                    and not (path.parent / "checkout-inventory.json").exists()):
                continue
            if manifest["status"] == "noop" or (
                manifest["status"] == "published" and manifest.get("delivery_status") == "complete"
            ):
                times = [dt.datetime.fromisoformat(manifest[name])
                         for name in ("created_at", "published_at", "completed_at",
                                      "delivery_completed_at") if manifest.get(name)]
                if any(value.tzinfo is None for value in times):
                    raise WorkspaceError("retention timestamp needs an explicit timezone")
                created = max(times)
                candidates.append((created, path, manifest))
        for index, (created, path, manifest) in enumerate(sorted(candidates, reverse=True)):
            prepared = (path.parent / "checkout-retirement.json").exists()
            age = (dt.datetime.now(dt.UTC) - created).total_seconds() / 3600
            if not prepared and (index < keep or age < min_age_hours):
                protected.append({"run_id": manifest["run_id"], "reason": "retention-window"})
                continue
            try:
                with producer_lock(path.parent) as producer_stream:
                    with retirement_git_locks(registry_stream, producer_stream):
                        retire_checkout(path, manifest)
                retired.append(manifest["run_id"])
            except (WorkspaceError, OSError, ValueError, KeyError) as exc:
                protected.append({"run_id": manifest["run_id"], "reason": str(exc)})
    report = census(repo, state_dir)
    protection = {row["run_id"]: row["reason"] for row in protected}
    for row in report["runs"]:
        row["protected_reason"] = protection.get(row["run_id"], row["protected_reason"])
    report["protected_bytes"] = sum(row["workspace_bytes"] for row in report["runs"]
                                    if row["protected_reason"])
    return {**report, "retired_runs": retired, "protected_runs": protected}


def create(args: argparse.Namespace) -> dict:
    identity(args.date, args.run_id)
    source = Path(args.repo).resolve()
    source = Path(git(source, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    common = Path(
        git(source, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    ).resolve()
    state = Path(args.state_dir).expanduser().absolute()
    if state.resolve() != state:
        raise WorkspaceError("workspace registry may not contain symlinks")
    if state.is_relative_to(source) or state.is_relative_to(common):
        raise WorkspaceError("state directory must be outside the owner checkout and Git directory")
    registry = state / hashlib.sha256(str(common).encode()).hexdigest()[:20]
    run_dir = registry / "runs" / args.date / args.run_id
    workspace = run_dir / "workspace"
    manifest_path = run_dir / "manifest.json"
    branch = f"blog-run/{args.date}/{args.run_id}"
    retention = None
    if args.recover_abandoned:
        verify_pipeline_lock()
        if os.environ.get("BLOG_CANARY") != "1":
            retention = retire_registry(
                source, state, args.expected_remote,
                keep=int(getattr(args, "retain_checkouts",
                                 os.environ.get("BLOG_WORKSPACE_KEEP_CHECKOUTS", 2))),
                min_age_hours=float(getattr(args, "retirement_min_age_hours",
                                            os.environ.get("BLOG_WORKSPACE_MIN_AGE_HOURS", 24))),
            )
    with locked(registry):
        secure_owned_registry(registry, common)
        if manifest_path.exists():
            manifest = load(manifest_path, require_workspace=False)
            if (
                manifest["source_repo"] != str(source)
                or manifest["remote_url"] != args.expected_remote
            ):
                raise WorkspaceError("existing run belongs to another source or remote")
            if manifest["status"] not in ACTIVE:
                raise WorkspaceError("terminal run retained; use a new run-id")
            if manifest.get("quality_seal_sha256"):
                raise WorkspaceError("sealed workspace cannot reopen a producer")
        else:
            for other in registry.glob("runs/*/*/manifest.json"):
                previous = load(other, require_workspace=False)
                if previous["status"] in ACTIVE:
                    if not args.recover_abandoned:
                        raise WorkspaceError(
                            f"unfinished run {previous['date']}/{previous['run_id']}; "
                            "resume or quarantine that manifest first"
                        )
                    recover_abandoned(other, previous)
            baseline = remote_master(source, args.expected_remote)
            capacity = admission(source, state, baseline)
            if not capacity["admitted"]:
                raise WorkspaceError(
                    "workspace admission refused: "
                    f"available_bytes={capacity['available_bytes']} "
                    f"required_free_bytes={capacity['required_free_bytes']} "
                    f"registry_bytes={capacity['registry_bytes']} "
                    f"protected_bytes={capacity['protected_bytes']}"
                )
            for parent in (registry / "runs", registry / "runs" / args.date):
                parent.mkdir(mode=0o700, exist_ok=True)
            run_dir.mkdir(mode=0o700, exist_ok=False)
            decision_bytes = git(source, "show", f"{baseline}:{DECISIONS}")
            manifest = {
                "schema_version": 1,
                "run_id": args.run_id,
                "date": args.date,
                "source_repo": str(source),
                "common_dir": str(common),
                "remote_url": args.expected_remote,
                "deploy_branch": "master",
                "branch": branch,
                "baseline_sha": baseline,
                "workspace": str(workspace),
                "status": "creating",
                "requires_quality_seal": True,
                "created_at": stamp(),
                "owner_status_sha256": hashlib.sha256(
                    git(source, "status", "--porcelain=v1", "-z")
                ).hexdigest(),
                "baseline_decisions_sha256": hashlib.sha256(decision_bytes).hexdigest(),
                "permitted_publish_paths": [
                    "content/posts/<one-new-target-date-slug>.md",
                    DECISIONS,
                    FEEDBACK,
                ],
                "permitted_staging_path": f".blog-staging/{args.date}.intent.json",
                "log_file": str(run_dir / "run.log"),
                "producer_log": str(run_dir / "producer.log"),
            }
            diagnostics_directory(manifest_path, manifest, register=True)
            atomic_json(manifest_path, manifest)
            event(manifest, f"created baseline={baseline} branch={branch}")
        if not workspace.exists():
            exists = subprocess.run(
                ["git", "-C", str(source), "show-ref", "--verify", f"refs/heads/{branch}"],
                capture_output=True,
                check=False,
            )
            if exists.returncode == 0:
                if git(source, "rev-parse", branch).decode().strip() != manifest["baseline_sha"]:
                    raise WorkspaceError(
                        "existing run branch differs from baseline; evidence retained"
                    )
                git(source, "worktree", "add", str(workspace), branch)
            else:
                git(
                    source,
                    "worktree",
                    "add",
                    "-b",
                    branch,
                    str(workspace),
                    manifest["baseline_sha"],
                )
        check_workspace(manifest)
        if "diagnostics_dir" not in manifest:
            # Only active runs may gain new diagnostics metadata. Loading old
            # sealed/terminal records never edits their historical evidence.
            with producer_lock(run_dir):
                diagnostics_directory(manifest_path, manifest, register=True)
        else:
            diagnostic_files(diagnostics_directory(manifest_path, manifest))
        manifest["status"] = "ready"
        atomic_json(manifest_path, manifest)
        event(manifest, "workspace ready/resumed; source checkout not changed")
        return {"manifest": str(manifest_path), **manifest, "retention": retention}


def load(path: Path, *, require_workspace: bool = True) -> dict:
    if path.is_symlink():
        raise WorkspaceError("manifest symlinks are not permitted")
    value = json.loads(path.read_text())
    identity(value["date"], value["run_id"])
    if value["schema_version"] != 1 or value["deploy_branch"] != "master":
        raise WorkspaceError("unsupported workspace manifest")
    if value["branch"] != f"blog-run/{value['date']}/{value['run_id']}":
        raise WorkspaceError("manifest branch does not match its run")
    if value["permitted_staging_path"] != f".blog-staging/{value['date']}.intent.json":
        raise WorkspaceError("manifest staging path does not match its target date")
    if Path(value["workspace"]).absolute() != path.absolute().parent / "workspace":
        raise WorkspaceError("manifest workspace escaped run directory")
    if require_workspace:
        check_workspace(value)
    return value


def check_workspace(manifest: dict) -> None:
    root = Path(manifest["workspace"])
    if root.is_symlink():
        raise WorkspaceError("workspace symlinks are not permitted")
    top = Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    common = Path(
        git(root, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    ).resolve()
    branch = git(root, "symbolic-ref", "--short", "HEAD").decode().strip()
    if (
        top != root.resolve()
        or common != Path(manifest["common_dir"])
        or branch != manifest["branch"]
    ):
        raise WorkspaceError("worktree identity no longer matches manifest")


def names(repo: Path, *args: str) -> set[str]:
    return {x.decode() for x in git(repo, *args).split(b"\0") if x}


def post_date(content: str) -> str:
    lines = content.splitlines()
    if not lines or lines[0] not in {"+++", "---"}:
        raise WorkspaceError("post has no front matter")
    try:
        end = lines.index(lines[0], 1)
    except ValueError as exc:
        raise WorkspaceError("post front matter is incomplete") from exc
    matches = [
        re.match(r"^date\s*(?:=|:)\s*['\"]?(\d{4}-\d{2}-\d{2})(?:T|\s|['\"]|$)", x)
        for x in lines[1:end]
    ]
    dates = [x.group(1) for x in matches if x]
    if len(dates) != 1:
        raise WorkspaceError("post must have exactly one dated front-matter field")
    return dates[0]


def validate(manifest: dict, *, committed: bool = False) -> dict:
    verify_diagnostics(manifest)
    root = Path(manifest["workspace"])
    baseline = manifest["baseline_sha"]
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if not committed and head != baseline:
        raise WorkspaceError("producer changed Git HEAD; refusing to land")
    tracked = names(root, "diff", "--name-only", "-z", baseline, "--")
    untracked = names(root, "ls-files", "--others", "--exclude-standard", "-z")
    ignored = names(root, "ls-files", "--others", "--ignored", "--exclude-standard", "-z")
    runtime = {x for x in ignored if x in RUNTIME_PATHS or x.startswith(RUNTIME_PREFIXES)}
    changed = tracked | untracked | (ignored - runtime)
    stage_prefix = f".blog-staging/{manifest['date']}.{manifest['run_id']}."
    stage_records = {
        x
        for x in changed
        if x.startswith(stage_prefix)
        and re.fullmatch(r"[A-Za-z0-9_-]+\.json", x[len(stage_prefix) :])
    }
    if stage_records & tracked:
        raise WorkspaceError("staging records must remain uncommitted and ignored")
    if stage_records - ignored:
        raise WorkspaceError("staging records must be ignored runtime artifacts")
    posts = sorted(x for x in changed if re.fullmatch(r"content/posts/[a-z0-9][a-z0-9-]*\.md", x))
    if len(posts) != 1:
        raise WorkspaceError("run must own exactly one new flat post")
    post = posts[0]
    previous = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-e", f"{baseline}:{post}"],
        capture_output=True,
        check=False,
    )
    if previous.returncode == 0:
        raise WorkspaceError("existing baseline posts cannot be owned by a daily run")
    if post_date(safe_file(root, post).read_text()) != manifest["date"]:
        raise WorkspaceError("post date differs from run target")
    allowed = {post, DECISIONS, FEEDBACK, manifest["permitted_staging_path"]} | stage_records
    unexpected = sorted(changed - allowed)
    if unexpected:
        raise WorkspaceError(f"changes outside run write-set: {unexpected}")
    for relative in changed | runtime:
        safe_file(root, relative)
    original = git(root, "show", f"{baseline}:{DECISIONS}")
    current = safe_file(root, DECISIONS).read_bytes()
    if not current.startswith(original) or (original and not original.endswith(b"\n")):
        raise WorkspaceError("decisions history was rewritten or lacks an append boundary")
    tail = current[len(original) :]
    if not tail or not tail.endswith(b"\n"):
        raise WorkspaceError("run decisions must be complete appended JSONL records")
    slug = Path(post).stem
    for line in tail.splitlines():
        record = json.loads(line)
        if (
            not isinstance(record, dict)
            or record.get("date") != manifest["date"]
            or record.get("slug") != slug
        ):
            raise WorkspaceError("appended decisions belong to another date or slug")
    sentinel = safe_file(root, manifest["permitted_staging_path"])
    if sentinel.exists():
        value = json.loads(sentinel.read_text())
        if (
            not isinstance(value, dict)
            or value.get("run_id") != manifest["run_id"]
            or value.get("date", value.get("target_date")) != manifest["date"]
        ):
            raise WorkspaceError("staging sentinel belongs to another run or date")
    for relative in stage_records:
        json.loads(safe_file(root, relative).read_text())
    publish_paths = [post, DECISIONS]
    if FEEDBACK in changed:
        baseline_feedback = optional_blob(root, baseline, FEEDBACK)
        current_feedback = safe_file(root, FEEDBACK).read_bytes()
        if not current_feedback.startswith(baseline_feedback) or (
            baseline_feedback and not baseline_feedback.endswith(b"\n")
        ):
            raise WorkspaceError("feedback history was rewritten")
        feedback_tail = current_feedback[len(baseline_feedback) :]
        if not feedback_tail or not feedback_tail.endswith(b"\n"):
            raise WorkspaceError("feedback requires complete appended records")
        for line in feedback_tail.splitlines():
            value = json.loads(line)
            if (
                not isinstance(value, dict)
                or value.get("slug") != slug
                or value.get("run_id") != manifest["run_id"]
            ):
                raise WorkspaceError("feedback append belongs to another slug or run")
            dt.date.fromisoformat(value["date_assessed"])
        publish_paths.append(FEEDBACK)
    if committed:
        ancestor = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", baseline, head],
            capture_output=True,
            check=False,
        )
        if ancestor.returncode:
            raise WorkspaceError("candidate history no longer descends from run baseline")
        if git(root, "status", "--porcelain=v1", "--untracked-files=no").strip():
            raise WorkspaceError("publication candidate has uncommitted tracked changes")
        if post in untracked or DECISIONS not in tracked:
            raise WorkspaceError(
                "publication candidate did not commit its owned post and decisions"
            )
        commits = git(root, "rev-list", "--reverse", f"{baseline}..HEAD").decode().splitlines()
        for commit in commits:
            paths = names(root, "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", commit)
            if paths - set(publish_paths):
                raise WorkspaceError(
                    "candidate history changed paths outside its owned publication"
                )
    result = {
        "run_id": manifest["run_id"],
        "date": manifest["date"],
        "post": post,
        "slug": slug,
        "publish_paths": publish_paths,
        "head": head,
        "staging_path": manifest["permitted_staging_path"],
        "runtime_artifacts": sorted(runtime),
    }
    event(manifest, f"validated committed={committed} post={post} head={head}")
    return result


def quarantine_owned(manifest_path: Path, manifest: dict, reason: str) -> dict:
    """Caller holds registry lock; this function never reads through artifact symlinks."""
    run_dir = manifest_path.parent
    with producer_lock(run_dir):
        if manifest["status"] == "quarantined":
            return manifest
        if manifest["status"] not in ACTIVE:
            raise WorkspaceError("only an unfinished run may be quarantined")
        root = Path(manifest["workspace"])
        snapshot = safe_file(run_dir, "quarantine")
        snapshot.mkdir(exist_ok=True)
        baseline = manifest["baseline_sha"]
        skipped = []
        for post in sorted((root / "content/posts").glob("*.md")):
            relative = post.relative_to(root).as_posix()
            exists = subprocess.run(
                ["git", "-C", str(root), "cat-file", "-e", f"{baseline}:{relative}"],
                capture_output=True,
                check=False,
            )
            if exists.returncode != 0:
                try:
                    safe_file(root, relative)
                except WorkspaceError:
                    skipped.append(relative)
                    continue
                safe_file(snapshot, "posts").mkdir(exist_ok=True)
                shutil.copyfile(post, safe_file(snapshot, f"posts/{post.name}"))
        try:
            staging = safe_file(root, manifest["permitted_staging_path"])
            if staging.is_file():
                shutil.copyfile(staging, snapshot / staging.name)
        except WorkspaceError:
            skipped.append(manifest["permitted_staging_path"])
        (snapshot / "decisions.diff").write_bytes(git(root, "diff", baseline, "--", DECISIONS))
        if optional_blob(root, baseline, FEEDBACK):
            (snapshot / "feedback.diff").write_bytes(git(root, "diff", baseline, "--", FEEDBACK))
        else:
            try:
                feedback = safe_file(root, FEEDBACK)
                if feedback.is_file():
                    shutil.copyfile(feedback, safe_file(snapshot, "feedback.jsonl"))
            except WorkspaceError:
                skipped.append(FEEDBACK)
        stage_prefix = f"{manifest['date']}.{manifest['run_id']}."
        staging_dir = safe_file(root, ".blog-staging")
        if staging_dir.is_dir():
            for staged in staging_dir.glob(f"{stage_prefix}*.json"):
                relative = staged.relative_to(root).as_posix()
                try:
                    safe_file(root, relative)
                    shutil.copyfile(staged, snapshot / staged.name)
                except WorkspaceError:
                    skipped.append(relative)
        manifest.update(
            status="quarantined",
            quarantined_at=stamp(),
            reason=reason,
            quarantine=str(snapshot),
            retained_workspace=str(root),
            skipped_unsafe_artifacts=skipped,
        )
        atomic_json(manifest_path, manifest)
        event(manifest, "quarantined owned artifacts; workspace and logs retained without cleanup")
        return manifest


def quarantine(manifest_path: Path, reason: str) -> dict:
    with locked(manifest_path.parent.parents[2]):
        manifest = load(manifest_path)
        try:
            return quarantine_owned(manifest_path, manifest, reason)
        except WorkspaceError as exc:
            event(manifest, f"quarantine refused; original state/evidence retained: {exc}")
            raise


def recover_abandoned(manifest_path: Path, manifest: dict) -> None:
    """Only create's verified canonical lock holder can reconcile an older run."""
    root = Path(manifest["workspace"])
    if not root.exists():
        manifest.update(
            status="quarantined",
            quarantined_at=stamp(),
            reason="abandoned before worktree creation; manifest and logs retained",
        )
        atomic_json(manifest_path, manifest)
        event(manifest, manifest["reason"])
        return
    check_workspace(manifest)
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if head == manifest["baseline_sha"]:
        quarantine_owned(manifest_path, manifest, "abandoned run recovered under canonical lock")
        return
    with producer_lock(manifest_path.parent):
        try:
            validate(manifest, committed=True)
            check_sealed_revision(manifest, committed=True)
            remote = remote_master(root, manifest["remote_url"])
            check = subprocess.run(
                ["git", "-C", str(root), "merge-base", "--is-ancestor", head, remote],
                capture_output=True,
                check=False,
            )
            if check.returncode:
                raise WorkspaceError("committed run is not on remote master")
        except WorkspaceError as exc:
            manifest.update(status="pending_publication", recovery_error=str(exc))
            atomic_json(manifest_path, manifest)
            event(manifest, "pending publication retained; refusing to discard committed run")
            raise WorkspaceError(
                "previous committed run needs publication reconciliation; "
                f"evidence: {manifest_path}"
            ) from exc
        manifest.update(
            status="published",
            published_at=manifest.get("published_at") or stamp(),
            published_sha=head,
            verified_remote_master=remote,
            recovered_abandoned=True,
        )
        if manifest.get("quality_seal_sha256"):
            manifest.setdefault("delivery_status", "pending")
        atomic_json(manifest_path, manifest)
        event(manifest, "previous publication verified; workspace retained")


def publication_check(manifest: dict) -> dict:
    result = validate(manifest, committed=True)
    check_sealed_revision(manifest, committed=True)
    root = Path(manifest["workspace"])
    remote = remote_master(root, manifest["remote_url"])
    check = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", remote, result["head"]],
        capture_output=True,
        check=False,
    )
    if check.returncode:
        raise WorkspaceError(
            "origin/master moved or diverged; retain run and reconcile through review"
        )
    return {**result, "remote_master": remote, "push_refspec": "HEAD:refs/heads/master"}


def check_sealed_revision(manifest: dict, *, committed: bool) -> None:
    # Older source-only manifests remain inspectable, but never authorize
    # automatic delivery. Every new lander calls seal before entering this path.
    if (not manifest.get("quality_seal_sha256") and not manifest.get("requires_quality_seal")
            and manifest["status"] != "sealed"):
        return
    spec = importlib.util.spec_from_file_location(
        "blog_publication_state", Path(__file__).with_name("blog_publication_state.py")
    )
    publication = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(publication)
    try:
        publication.verify_candidate_seal(manifest, committed=committed)
    except (ValueError, OSError) as exc:
        raise WorkspaceError("candidate differs from its genuine quality seal") from exc


def complete(manifest_path: Path) -> dict:
    manifest = load(manifest_path)
    with locked(manifest_path.parent.parents[2]), producer_lock(manifest_path.parent):
        validate(manifest, committed=True)
        check_sealed_revision(manifest, committed=True)
        root = Path(manifest["workspace"])
        remote = remote_master(root, manifest["remote_url"])
        head = git(root, "rev-parse", "HEAD").decode().strip()
        check = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", head, remote],
            capture_output=True,
            check=False,
        )
        if check.returncode:
            raise WorkspaceError("run commit is not published on origin/master")
        manifest.update(
            status="published",
            published_at=manifest.get("published_at") or stamp(),
            published_sha=head,
            verified_remote_master=remote,
        )
        if manifest.get("quality_seal_sha256"):
            manifest.setdefault("delivery_status", "pending")
        atomic_json(manifest_path, manifest)
        event(manifest, f"publication verified remote_master={remote}; workspace retained")
        return manifest


def complete_noop(manifest_path: Path) -> dict:
    manifest = load(manifest_path)
    root = Path(manifest["workspace"])
    with locked(manifest_path.parent.parents[2]), producer_lock(manifest_path.parent):
        if git(root, "rev-parse", "HEAD").decode().strip() != manifest["baseline_sha"]:
            raise WorkspaceError("no-op requires unchanged baseline HEAD")
        if git(root, "status", "--porcelain=v1", "--untracked-files=all").strip():
            raise WorkspaceError("no-op cannot close a workspace with producer changes")
        targets = []
        for relative in names(
            root,
            "ls-tree",
            "--name-only",
            "-r",
            "-z",
            manifest["baseline_sha"],
            "--",
            "content/posts",
        ):
            if relative.endswith(".md"):
                try:
                    if post_date(safe_file(root, relative).read_text()) == manifest["date"]:
                        targets.append(relative)
                except WorkspaceError:
                    continue
        if not targets:
            raise WorkspaceError("no-op requires an existing target-date baseline post")
        remote = remote_master(root, manifest["remote_url"])
        for target in targets:
            if git(root, "show", f"{remote}:{target}") != safe_file(root, target).read_bytes():
                raise WorkspaceError("existing target post differs from remote publication")
        manifest.update(
            status="noop",
            completed_at=stamp(),
            existing_posts=sorted(targets),
            verified_remote_master=remote,
        )
        atomic_json(manifest_path, manifest)
        event(manifest, "existing target publication verified; no-op workspace retained")
        return manifest


def successful_producer_attempt(manifest: dict) -> dict:
    """A completed process is necessary but never substitutes for quality checks."""
    attempt = manifest.get("producer_attempt")
    if (
        not isinstance(attempt, dict)
        or type(attempt.get("schema_version")) is not int
        or attempt["schema_version"] != 1
        or attempt.get("state") != "completed"
        or type(attempt.get("exit_code")) is not int
        or attempt["exit_code"] != 0
        or any(attempt.get(key) != manifest[key] for key in ("run_id", "date", "baseline_sha"))
        or not isinstance(attempt.get("attempt_id"), str)
        or not re.fullmatch(r"[0-9a-f]{32}", attempt["attempt_id"])
    ):
        raise WorkspaceError("producer has no bound completed exit0 attempt")
    try:
        started = dt.datetime.fromisoformat(attempt["started_at"])
        finished = dt.datetime.fromisoformat(attempt["finished_at"])
        if started.tzinfo is None or finished.tzinfo is None or finished < started:
            raise ValueError("invalid completion time")
    except (KeyError, TypeError, ValueError) as exc:
        raise WorkspaceError("producer completion timestamps are invalid") from exc
    return attempt


def run_producer(manifest_path: Path, argv: list[str]) -> dict:
    """Hold the run lock in child too: termination cannot leave an unguarded writer."""
    if argv and argv[0] == "--":
        argv = argv[1:]
    if not argv:
        raise WorkspaceError("run requires an actual producer command after --")
    manifest = load(manifest_path)
    if manifest["status"] != "ready" or manifest.get("quality_seal_sha256"):
        raise WorkspaceError("sealed or terminal workspace cannot run a producer")
    root = Path(manifest["workspace"])
    if git(root, "rev-parse", "HEAD").decode().strip() != manifest["baseline_sha"]:
        raise WorkspaceError("producer cannot start after Git HEAD changed")
    with producer_lock(manifest_path.parent, allow_diagnostics=True) as lock:
        manifest = load(manifest_path)
        if manifest["status"] != "ready" or manifest.get("quality_seal_sha256"):
            raise WorkspaceError("sealed or terminal workspace cannot run a producer")
        if git(root, "rev-parse", "HEAD").decode().strip() != manifest["baseline_sha"]:
            raise WorkspaceError("producer cannot start after Git HEAD changed")
        diagnostic_files(diagnostics_directory(manifest_path, manifest, register=True))
        attempt = {
            "schema_version": 1,
            **{key: manifest[key] for key in ("run_id", "date", "baseline_sha")},
            "attempt_id": uuid.uuid4().hex,
            "state": "running",
            "started_at": stamp(),
        }
        # Persist before launch: a killed supervisor leaves an unfinished attempt,
        # never an earlier process success that can authorize a new seal.
        manifest["producer_attempt"] = attempt
        atomic_json(manifest_path, manifest)
        event(manifest, "producer started; run lock inherited by child")
        environment = {
            **os.environ,
            "BLOG_RUN_MANIFEST": str(manifest_path.absolute()),
            "BLOG_DIR": str(root),
            "BLOG_TARGET_DATE": manifest["date"],
            "BLOG_RUN_ID": manifest["run_id"],
            "BLOG_RUN_DIAGNOSTICS_DIR": manifest["diagnostics_dir"],
            "BLOG_RUN_WORKSPACE_HELPER": str(Path(__file__).resolve()),
        }
        inherited = (lock.fileno(),)
        try:
            verify_pipeline_lock()
        except WorkspaceError as exc:
            event(manifest, f"manual producer holds per-run lock only: {exc}")
        else:
            inherited += (9,)
        output_path = safe_file(manifest_path.parent, "producer.log")
        with output_path.open("ab") as output:
            proc = subprocess.run(
                argv,
                cwd=root,
                env=environment,
                stdout=output,
                stderr=output,
                pass_fds=inherited,
                check=False,
            )
        exit_code = proc.returncode if proc.returncode >= 0 else 128 - proc.returncode
        manifest = load(manifest_path)
        if manifest.get("producer_attempt") != attempt:
            raise WorkspaceError("producer attempt identity changed while child ran")
        manifest["producer_attempt"] = {
            **attempt, "state": "completed", "finished_at": stamp(), "exit_code": exit_code,
        }
        atomic_json(manifest_path, manifest)
        event(manifest, f"producer exited rc={exit_code}; output retained in producer.log")
        return {"exit_code": exit_code, "producer_log": manifest["producer_log"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    make = subs.add_parser("create")
    for flag in ("repo", "date", "run-id", "expected-remote"):
        make.add_argument(f"--{flag}", required=True)
    make.add_argument("--state-dir", default="~/.local/state/blog-run-workspaces")
    make.add_argument("--recover-abandoned", action="store_true")
    for command in ("census", "admission", "retire"):
        sub = subs.add_parser(command)
        sub.add_argument("--repo", type=Path, required=True)
        sub.add_argument("--state-dir", type=Path, default="~/.local/state/blog-run-workspaces")
        if command != "census":
            sub.add_argument("--expected-remote", required=True)
        if command == "retire":
            sub.add_argument("--retain-checkouts", type=int,
                             default=os.environ.get("BLOG_WORKSPACE_KEEP_CHECKOUTS", 2))
            sub.add_argument("--retirement-min-age-hours", type=float,
                             default=os.environ.get("BLOG_WORKSPACE_MIN_AGE_HOURS", 24))
    for command in ("validate", "quarantine", "publication-check", "complete", "complete-noop"):
        sub = subs.add_parser(command)
        sub.add_argument("--manifest", type=Path, required=True)
        if command == "quarantine":
            sub.add_argument("--reason", required=True)
    run = subs.add_parser("run")
    run.add_argument("--manifest", type=Path, required=True)
    run.add_argument("argv", nargs=argparse.REMAINDER)
    diagnostic = subs.add_parser("diagnostic")
    diagnostic.add_argument("--manifest", type=Path, required=True)
    diagnostic.add_argument("--label", required=True)
    diagnostic.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.command == "create":
            result = create(args)
        elif args.command == "census":
            result = census(args.repo, args.state_dir)
        elif args.command == "admission":
            result = admission(args.repo, args.state_dir,
                               remote_master(args.repo, args.expected_remote))
        elif args.command == "retire":
            result = retire_registry(args.repo, args.state_dir, args.expected_remote,
                                     keep=args.retain_checkouts,
                                     min_age_hours=args.retirement_min_age_hours)
        elif args.command == "quarantine":
            result = quarantine(args.manifest, args.reason)
        elif args.command == "complete":
            result = complete(args.manifest)
        elif args.command == "complete-noop":
            result = complete_noop(args.manifest)
        elif args.command == "run":
            result = run_producer(args.manifest, args.argv)
        elif args.command == "diagnostic":
            return run_diagnostic(args.manifest, args.label, args.argv)
        else:
            manifest = load(args.manifest)
            if manifest["status"] not in ACTIVE:
                raise WorkspaceError("terminal workspace cannot be landed")
            result = (
                validate(manifest) if args.command == "validate" else publication_check(manifest)
            )
        print(json.dumps(result, sort_keys=True))
        if args.command == "admission":
            return 0 if result["admitted"] else 1
        return result["exit_code"] if args.command == "run" else 0
    except (WorkspaceError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
