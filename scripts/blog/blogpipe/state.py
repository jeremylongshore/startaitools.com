"""Shared ledger and cross-post queue transactions: one lock, atomic writes, strict rows.

Every script that touches .blog-syndication-ledger.json or .crosspost-queue.json goes
through here, so a crash can never leave a half-written or silently reset state file.
"""

from __future__ import annotations

import contextlib
import fcntl
import json
import os
import tempfile
import time
from pathlib import Path

from .errors import PublicationError

STATE_FILES = {".blog-syndication-ledger.json", ".crosspost-queue.json"}


def no_canary() -> None:
    if os.environ.get("BLOG_CANARY") == "1":
        raise PublicationError("canary cannot seal or mutate publication delivery state")


def state_path(path: Path) -> Path:
    path = Path(path).absolute()
    if path.name not in STATE_FILES or path.is_symlink():
        raise PublicationError("unapproved or symlinked publication state file")
    if path.parent != path.parent.resolve() or not path.parent.is_dir():
        raise PublicationError("publication state root must be an existing real directory")
    return path


@contextlib.contextmanager
def state_locked(root: Path, timeout: float = 30):
    no_canary()
    root = Path(root).absolute()
    if root != root.resolve() or not root.is_dir():
        raise PublicationError("publication state root must be an existing real directory")
    fd = os.open(
        root / ".blog-publication-state.lock",
        os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW,
        0o600,
    )
    with os.fdopen(fd, "a") as stream:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise PublicationError("publication state transaction lock timed out") from None
                time.sleep(min(0.05, max(0, deadline - time.monotonic())))
        yield


def validate_rows(value: object) -> list[dict]:
    if not isinstance(value, list):
        raise PublicationError("publication state must be a JSON array")
    slugs = set()
    for row in value:
        if not isinstance(row, dict) or not isinstance(row.get("slug"), str) or not row["slug"]:
            raise PublicationError("publication state has an invalid row identity")
        if row["slug"] in slugs:
            raise PublicationError("publication state has duplicate row identities")
        slugs.add(row["slug"])
    return value


def load_state(path: Path) -> list[dict]:
    path = state_path(path)
    if not path.exists():
        return []
    return validate_rows(strict_json(path.read_text()))


def strict_json(text: str):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise PublicationError("duplicate key in publication evidence/state")
            result[key] = value
        return result

    def constant(_value):
        raise PublicationError("non-finite value in publication evidence/state")

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def atomic_state(path: Path, value: list[dict]) -> None:
    """Caller holds state_locked across the read, modification and this write."""
    no_canary()
    path = state_path(path)
    validate_rows(value)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        Path(temporary).unlink(missing_ok=True)


def deep_merge(value: dict, patch: dict) -> dict:
    result = dict(value)
    for key, item in patch.items():
        result[key] = (
            deep_merge(result[key], item)
            if isinstance(result.get(key), dict) and isinstance(item, dict)
            else item
        )
    return result


def update_row(path: Path, slug: str, patch: dict) -> None:
    no_canary()
    path = state_path(path)
    if not isinstance(patch, dict):
        raise PublicationError("row patch must be an object")
    with state_locked(path.parent):
        rows = load_state(path)
        matches = [row for row in rows if row["slug"] == slug]
        if len(matches) != 1:
            raise PublicationError("publication row to update is missing")
        row = matches[0]
        for key in ("slug", "date", "canonical_url", "tier", "published_at", "source"):
            if key in patch and patch[key] != row.get(key):
                raise PublicationError("row update cannot change publication identity")
        rows[rows.index(row)] = deep_merge(row, patch)
        atomic_state(path, rows)
