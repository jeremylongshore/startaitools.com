#!/usr/bin/env python3
"""Materialize a verified committed post without reading an owner's working files."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from blog_publication_state import (
    PublicationError,
    frontmatter,
    read_quality_seal,
    sha,
    source_reference,
    strict_json,
)

DEFAULT_REMOTE = "https://github.com/jeremylongshore/startaitools.com.git"
MAX_POST_BYTES = 1024 * 1024


class GitSource:
    def __init__(self, repo: Path):
        self.repo = repo
        self.deadline = time.monotonic() + 60

    def run(self, *args: str) -> bytes:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise PublicationError("consumer source Git deadline exceeded")
        result = subprocess.run(
            ["git", "-C", str(self.repo), *args],
            capture_output=True,
            check=False,
            timeout=min(20, remaining),
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode:
            raise PublicationError("consumer source Git verification failed")
        return result.stdout

    def authoritative_head(self, expected: str) -> str:
        actual = self.run("remote", "get-url", "origin").decode().strip()
        if actual != expected or re.match(r"https?://[^/]*@", actual):
            raise PublicationError("consumer source origin is not the approved remote")
        default = self.run("ls-remote", "--symref", "origin", "HEAD").decode()
        if "ref: refs/heads/master\tHEAD" not in default:
            raise PublicationError("consumer source remote default must remain master")
        self.run("fetch", "--no-tags", "origin", "refs/heads/master:refs/remotes/origin/master")
        return self.run("rev-parse", "refs/remotes/origin/master").decode().strip()

    def blob(self, commit: str, path: str) -> bytes:
        if not re.fullmatch(r"[0-9a-f]{40,64}", commit):
            raise PublicationError("consumer source commit is invalid")
        metadata = self.run("ls-tree", commit, "--", path).decode().split()
        if len(metadata) != 4 or metadata[0] not in ("100644", "100755") or metadata[1] != "blob":
            raise PublicationError("consumer source is not a tracked regular post")
        size = int(self.run("cat-file", "-s", f"{commit}:{path}"))
        if not 0 < size <= MAX_POST_BYTES:
            raise PublicationError("consumer source post size is invalid")
        return self.run("show", f"{commit}:{path}")


def safe_proof_path(registry: Path, date: str, run_id: str) -> Path:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        raise PublicationError("consumer source date is invalid")
    dt.date.fromisoformat(date)
    path = registry / "runs" / date / run_id / "manifest.json"
    if path.resolve() != path or not path.is_file():
        raise PublicationError("consumer source retained manifest is missing or symlinked")
    return path


def resolve_source(repo: Path, entry: dict, *, state_dir: Path, expected_remote: str) -> bytes:
    repo = repo.absolute()
    if repo.resolve() != repo or not repo.is_dir():
        raise PublicationError("consumer source repository must be a real directory")
    slug = entry.get("slug")
    if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,199}", slug):
        raise PublicationError("consumer source slug is invalid")
    if entry.get("canonical_url") != f"https://startaitools.com/posts/{slug}/":
        raise PublicationError("consumer source canonical identity mismatch")
    reader = GitSource(repo)
    top = reader.run("rev-parse", "--show-toplevel").decode().strip()
    if Path(top).resolve() != repo:
        raise PublicationError("consumer source repository is not its Git root")
    common = reader.run("rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()
    common = str(Path(common).resolve())
    path = f"content/posts/{slug}.md"
    reference = entry.get("source")
    governed = any(key in entry for key in ("source", "run_id", "post_sha256"))
    if governed:
        run_id = entry.get("run_id")
        if not isinstance(run_id, str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", run_id
        ):
            raise PublicationError("consumer source run identity is invalid")
        registry = state_dir.expanduser().absolute() / sha(common.encode())[:20]
        if registry.resolve() != registry:
            raise PublicationError("consumer source proof registry may not be symlinked")
        # Older sealed queue rows had no date/reference. Only their exact retained
        # run proof can bridge that format; source-only legacy fallback is forbidden.
        dates = (
            [entry["date"]]
            if "date" in entry
            else (
                [reference.get("date")]
                if isinstance(reference, dict)
                else [item.parent.name for item in (registry / "runs").glob(f"*/{run_id}")]
            )
        )
        if len(dates) != 1 or not isinstance(dates[0], str):
            raise PublicationError("consumer source retained run is missing or ambiguous")
        manifest_path = safe_proof_path(registry, dates[0], run_id)
        manifest = strict_json(manifest_path.read_text())
        if (
            manifest.get("source_repo") != str(repo)
            or manifest.get("common_dir") != common
            or manifest.get("remote_url") != expected_remote
            or manifest.get("deploy_branch") != "master"
            or manifest.get("status") != "published"
            or manifest.get("run_id") != run_id
            or manifest.get("date") != dates[0]
        ):
            raise PublicationError("consumer source publication owner or proof identity mismatch")
        seal = read_quality_seal(manifest_path, manifest)
        expected = source_reference(seal, manifest)
        if reference is not None and (
            not isinstance(reference, dict)
            or type(reference.get("schema_version")) is not int
            or reference != expected
        ):
            raise PublicationError("consumer source reference differs from retained quality proof")
        if "source" in entry and not isinstance(reference, dict):
            raise PublicationError("consumer source reference is malformed")
        if (
            seal.get("slug") != slug
            or seal.get("post") != path
            or seal.get("canonical_url") != entry["canonical_url"]
            or entry.get("post_sha256") != expected["sha256"]
            or ("title" in entry and entry["title"] != seal.get("title"))
            or ("tier" in entry and entry["tier"] != seal.get("tier"))
        ):
            raise PublicationError("consumer source row differs from sealed article identity")
        commit = expected["commit"]
    else:
        expected = None
        commit = None
    remote = reader.authoritative_head(expected_remote)
    commit = commit or remote
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40,64}", commit):
        raise PublicationError("consumer source commit is invalid")
    reader.run("merge-base", "--is-ancestor", commit, remote)
    raw = reader.blob(commit, path)
    if expected and sha(raw) != expected["sha256"]:
        raise PublicationError("consumer source blob differs from quality-approved content")
    if expected and sha(reader.blob(remote, path)) != expected["sha256"]:
        raise PublicationError("consumer source published article changed after quality approval")
    fields, body = frontmatter(raw.decode("utf-8"))
    draft = fields.get("draft", False)
    if (
        not body.strip()
        or not isinstance(fields.get("title"), str)
        or not fields["title"].strip()
        or ("slug" in fields and fields["slug"] != slug)
        or not (draft is False or (type(draft) is str and draft.lower() == "false"))
    ):
        raise PublicationError("consumer source article body or front matter is invalid")
    date = str(fields.get("date", ""))[:10]
    dt.date.fromisoformat(date)
    if date != (expected["date"] if expected else entry.get("date", date)):
        raise PublicationError("consumer source article date mismatch")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--state-dir",
        type=Path,
        default=Path(os.environ.get("BLOG_RUN_STATE_DIR", "~/.local/state/blog-run-workspaces")),
    )
    parser.add_argument(
        "--expected-remote", default=os.environ.get("BLOG_EXPECTED_REMOTE", DEFAULT_REMOTE)
    )
    args = parser.parse_args()
    try:
        entry = strict_json(sys.stdin.read(MAX_POST_BYTES + 1))
        raw = resolve_source(
            args.repo, entry, state_dir=args.state_dir, expected_remote=args.expected_remote
        )
        output = args.output.absolute()
        if output.parent.resolve() != output.parent or output.parent.stat().st_mode & 0o077:
            raise PublicationError("consumer source output needs a private real directory")
        fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
        return 0
    except Exception as exc:
        # Git/provider stderr and private corpus are never emitted.
        reason = str(exc) if isinstance(exc, PublicationError) else type(exc).__name__
        print(f"Consumer source verification failed: {reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
