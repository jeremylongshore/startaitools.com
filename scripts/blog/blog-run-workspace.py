#!/usr/bin/env python3
"""Own one daily producer's isolated worktree; never clean the owner's checkout.

This tool does not commit, push, rebase, remove worktrees, or delete branches.
Manifest + run.log live outside the source tree, and terminal runs are retained.
Use one canonical state directory for cron and manual producers alike.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"
FEEDBACK = ".claude/skills/blog-backfill/methodology/feedback.jsonl"
ACTIVE = {"creating", "ready", "pending_publication"}
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


class WorkspaceError(Exception):
    """A fail-closed ownership or publication boundary."""


def git(repo: Path, *args: str) -> bytes:
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)
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
        yield


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
    local_head = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "refs/remotes/origin/HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if local_head.returncode == 0 and local_head.stdout.strip() != "refs/remotes/origin/master":
        raise WorkspaceError("configured origin/HEAD is not master")
    git(repo, "fetch", "--no-tags", "origin", "refs/heads/master:refs/remotes/origin/master")
    return git(repo, "rev-parse", "refs/remotes/origin/master").decode().strip()


def create(args: argparse.Namespace) -> dict:
    identity(args.date, args.run_id)
    source = Path(args.repo).resolve()
    source = Path(git(source, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    common = Path(
        git(source, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    ).resolve()
    state = Path(args.state_dir).expanduser().resolve()
    if state.is_relative_to(source) or state.is_relative_to(common):
        raise WorkspaceError("state directory must be outside the owner checkout and Git directory")
    registry = state / hashlib.sha256(str(common).encode()).hexdigest()[:20]
    run_dir = registry / "runs" / args.date / args.run_id
    workspace = run_dir / "workspace"
    manifest_path = run_dir / "manifest.json"
    branch = f"blog-run/{args.date}/{args.run_id}"
    if args.recover_abandoned:
        verify_pipeline_lock()
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
        return {"manifest": str(manifest_path), **manifest}


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
            published_at=stamp(),
            published_sha=head,
            verified_remote_master=remote,
            recovered_abandoned=True,
        )
        atomic_json(manifest_path, manifest)
        event(manifest, "previous publication verified; workspace retained")


def publication_check(manifest: dict) -> dict:
    result = validate(manifest, committed=True)
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


def complete(manifest_path: Path) -> dict:
    manifest = load(manifest_path)
    with locked(manifest_path.parent.parents[2]), producer_lock(manifest_path.parent):
        validate(manifest, committed=True)
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
            published_at=stamp(),
            published_sha=head,
            verified_remote_master=remote,
        )
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
    if manifest["status"] not in ACTIVE:
        raise WorkspaceError("terminal workspace cannot run a producer")
    root = Path(manifest["workspace"])
    if git(root, "rev-parse", "HEAD").decode().strip() != manifest["baseline_sha"]:
        raise WorkspaceError("producer cannot start after Git HEAD changed")
    with producer_lock(manifest_path.parent) as lock:
        manifest = load(manifest_path)
        if manifest["status"] not in ACTIVE:
            raise WorkspaceError("terminal workspace cannot run a producer")
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
        return result["exit_code"] if args.command == "run" else 0
    except (WorkspaceError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
