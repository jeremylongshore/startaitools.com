#!/usr/bin/env python3
"""Publish the canonical derived index from a committed authoritative snapshot.

The owner's checkout and failed producer drafts are never methodology inputs.
A private temporary Git view reads the original object store through alternates,
without copying media, registering worktrees or changing the owner's HEAD. Only
this helper's generated snapshot is removed; producer evidence remains intact.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
METHODOLOGY = ".claude/skills/blog-backfill/methodology"
FILES = (
    "decisions.jsonl",
    "feedback.jsonl",
    "patterns.jsonl",
    "legacy-index-migration-v2.json",
    "rebuild-index.sql",
)
REMOTE = "https://github.com/jeremylongshore/startaitools.com.git"
MAX_SOURCE_BYTES = 16 * 1024 * 1024


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, timeout=60, check=False
    )
    if result.returncode:
        raise ValueError(f"published methodology Git operation failed: {args[0]}")
    return result.stdout


def authoritative_commit(repo: Path, expected_remote: str) -> str:
    actual = git(repo, "remote", "get-url", "origin").decode().strip()
    if actual != expected_remote or re.match(r"https?://[^/]*@", actual):
        raise ValueError("published methodology origin does not match approved remote")
    head = git(repo, "ls-remote", "--symref", "origin", "HEAD").decode()
    if "ref: refs/heads/master\tHEAD" not in head:
        raise ValueError("published methodology remote default must be master")
    git(repo, "fetch", "--no-tags", "origin", "refs/heads/master:refs/remotes/origin/master")
    commit = git(repo, "rev-parse", "refs/remotes/origin/master").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("invalid authoritative methodology commit")
    return commit


def blob(repo: Path, commit: str, relative: str) -> bytes:
    tree = git(repo, "ls-tree", commit, "--", relative).decode().strip()
    if not re.fullmatch(r"100(?:644|755) blob [0-9a-f]{40}\t" + re.escape(relative), tree):
        raise ValueError("published methodology source must be a regular committed blob")
    size = int(git(repo, "cat-file", "-s", f"{commit}:{relative}"))
    if size > MAX_SOURCE_BYTES:
        raise ValueError("published methodology source exceeds the documented 16MiB bound")
    return git(repo, "show", f"{commit}:{relative}")


def rebuild(repo: Path, output: Path, expected_remote: str = REMOTE) -> dict:
    repo, output = repo.resolve(), output.absolute()
    if output != repo / METHODOLOGY / "index.db":
        raise ValueError("destination must be this repository's canonical methodology index")
    current = repo
    for part in Path(METHODOLOGY, "index.db").parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("canonical methodology destination must not be symlinked")
    commit = authoritative_commit(repo, expected_remote)
    spec = importlib.util.spec_from_file_location(
        "published_methodology_index",
        ROOT / METHODOLOGY / "../scripts/rebuild-methodology-index.py",
    )
    index = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(index)
    committed = {name: blob(repo, commit, f"{METHODOLOGY}/{name}") for name in FILES}
    common = Path(
        git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    )
    objects = str(common / "objects")
    if "\n" in objects or "\r" in objects:
        raise ValueError("invalid Git object-store path")
    with tempfile.TemporaryDirectory(prefix="blog-methodology-committed-") as temporary:
        snapshot = Path(temporary) / "snapshot"
        snapshot.mkdir(mode=0o700)
        git(snapshot, "init", "-b", "snapshot")
        alternates = snapshot / ".git/objects/info/alternates"
        alternates.write_text(objects + "\n")
        alternates.chmod(0o600)
        git(snapshot, "update-ref", "refs/heads/snapshot", commit)
        sources = snapshot / METHODOLOGY
        sources.mkdir(parents=True, mode=0o700)
        for name, expected in committed.items():
            target = sources / name
            target.write_bytes(expected)
            target.chmod(0o600)
        summary = index.build(sources, snapshot, output)
    result = {"event": "canonical_methodology_snapshot_published", "source_commit": commit}
    result.update(summary)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--expected-remote", default=REMOTE)
    args = parser.parse_args()
    try:
        # Production callers must inherit the already-held canonical lease.
        spec = importlib.util.spec_from_file_location(
            "workspace", ROOT / "scripts/blog/blog-run-workspace.py"
        )
        workspace = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(workspace)
        workspace.verify_pipeline_lock()
        result = rebuild(args.repo, args.output, args.expected_remote)
    except Exception as exc:
        # Emit failure rather than turning absent output into a successful run.
        print(f"CANONICAL-METHODOLOGY: FAILED: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
