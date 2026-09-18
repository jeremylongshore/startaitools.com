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
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "workspace.lock").open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield stream


@contextlib.contextmanager
def producer_lock(run_dir: Path):
    with (run_dir / "producer.lock").open("a") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise WorkspaceError(
                "producer is still running; workspace cannot be reused or closed"
            ) from exc
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
            run_dir.mkdir(parents=True, exist_ok=False)
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
        return quarantine_owned(manifest_path, load(manifest_path), reason)


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
    with producer_lock(manifest_path.parent) as lock:
        manifest = load(manifest_path)
        if manifest["status"] != "ready" or manifest.get("quality_seal_sha256"):
            raise WorkspaceError("sealed or terminal workspace cannot run a producer")
        if git(root, "rev-parse", "HEAD").decode().strip() != manifest["baseline_sha"]:
            raise WorkspaceError("producer cannot start after Git HEAD changed")
        event(manifest, "producer started; run lock inherited by child")
        environment = {
            **os.environ,
            "BLOG_RUN_MANIFEST": str(manifest_path.absolute()),
            "BLOG_DIR": str(root),
            "BLOG_TARGET_DATE": manifest["date"],
            "BLOG_RUN_ID": manifest["run_id"],
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
