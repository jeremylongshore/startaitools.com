#!/usr/bin/env python3
"""Durable publication handoff and shared ledger/queue transactions.

Only a quality-sealed run whose exact commit reached the configured remote can
create delivery rows. Existing delivery records are never reset during recovery.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import functools
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

STATE_FILES = {".blog-syndication-ledger.json", ".crosspost-queue.json"}


class PublicationError(ValueError):
    """An unverifiable handoff or failed delivery transaction remains pending."""


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


@functools.lru_cache
def module(name: str):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), Path(__file__).with_name(f"{name}.py")
    )
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def no_canary() -> None:
    if os.environ.get("BLOG_CANARY") == "1":
        raise PublicationError("canary cannot seal or mutate publication delivery state")


def frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0] not in ("+++", "---") or lines[0] not in lines[1:]:
        raise PublicationError("sealed post needs complete front matter")
    end = lines.index(lines[0], 1)
    if lines[0] == "+++":
        fields = tomllib.loads("\n".join(lines[1:end]))
    else:
        fields = {}
        for line in lines[1:end]:
            match = re.fullmatch(r"(title|slug|draft|date):\s*(.*)", line)
            if match:
                fields[match[1]] = match[2].strip().strip("\"'")
    return fields, "\n".join(lines[end + 1 :])


def save_bytes(path: Path, value: bytes) -> None:
    if path.is_symlink():
        raise PublicationError("quality proof may not be a symlink")
    fd, temporary = tempfile.mkstemp(prefix=".proof-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(value)
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


def seal_quality(manifest_path: Path, transcript: Path | None, hugo: str = "hugo") -> dict:
    """Run real quality gates before commit; retain their exact inputs privately."""
    no_canary()
    workspace = module("blog-run-workspace")
    contract = module("blog-producer-contract")
    manifest = workspace.load(manifest_path)
    root = Path(manifest["workspace"])
    with (
        workspace.locked(manifest_path.parent.parents[2]),
        workspace.producer_lock(manifest_path.parent),
    ):
        manifest = workspace.load(manifest_path)
        if manifest.get("quality_seal_sha256"):
            if manifest["status"] not in {"sealed", "published", "pending_publication"}:
                raise PublicationError("terminal workspace cannot acquire a quality seal")
            # Existing genuine seals predate process receipts. Verify those exact
            # bytes idempotently; never infer or rewrite their producer history.
            head = workspace.git(root, "rev-parse", "HEAD").decode().strip()
            verify_candidate_seal(manifest, committed=head != manifest["baseline_sha"])
            retained = read_quality_seal(manifest_path, manifest)
            return {"outcome": "sealed", "run_id": manifest["run_id"], "slug": retained["slug"]}
        if manifest["status"] != "ready":
            raise PublicationError("only a ready accepted producer can acquire a quality seal")
        try:
            attempt = workspace.successful_producer_attempt(manifest)
        except workspace.WorkspaceError as exc:
            raise PublicationError(str(exc)) from exc
        ownership = workspace.validate(manifest)
        receipt = contract.validate(root, manifest["date"], manifest["run_id"], transcript)
        hashes = {name: sha((root / name).read_bytes()) for name in ownership["publish_paths"]}
        # Corroboration only: the staged roles receipt is completion authority, so an
        # absent transcript seals with empty retained proof instead of failing a good post.
        present = transcript is not None and transcript.is_file()
        session = transcript.read_bytes() if present else b""
        commands = [
            [hugo, "--buildFuture", "--gc", "--minify", "--cleanDestinationDir", "--quiet"],
            [
                sys.executable,
                str(root / ".claude/skills/blog-backfill/scripts/lint-post-voice.py"),
                str(root / ownership["post"]),
            ],
        ]
        for name, argv in zip(("build", "voice"), commands, strict=True):
            log = manifest_path.parent / f"quality-{name}.log"
            fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
            with os.fdopen(fd, "w") as stream:
                result = subprocess.run(
                    argv,
                    cwd=root,
                    stdout=stream,
                    stderr=stream,
                    timeout=300 if name == "build" else 60,
                    check=False,
                )
                stream.flush()
                os.fsync(stream.fileno())
            if result.returncode:
                raise PublicationError(f"independent {name} gate failed; no quality seal")
        version = subprocess.run(
            [hugo, "version"], capture_output=True, text=True, timeout=15, check=True
        ).stdout.strip()
        workspace.validate(manifest)
        if contract.validate(root, manifest["date"], manifest["run_id"], transcript) != receipt:
            raise PublicationError("quality receipt changed while sealing")
        if any(sha((root / name).read_bytes()) != value for name, value in hashes.items()):
            raise PublicationError("publication artifacts changed while gates ran")
        if present and transcript.read_bytes() != session:
            raise PublicationError("agent transcript changed while sealing")
        post = root / ownership["post"]
        fields, body = frontmatter(post.read_text())
        if (
            fields.get("slug") != receipt["slug"]
            or not isinstance(fields.get("title"), str)
            or not fields["title"].strip()
            or str(fields.get("draft", False)).lower() == "true"
        ):
            raise PublicationError("post front matter does not identify the publishable article")
        structural_tier = (
            1 if len(body.splitlines()) <= 145 else (2 if len(body.splitlines()) <= 260 else 3)
        )
        proof_dir = manifest_path.parent / "quality-proof"
        proof_dir.mkdir(mode=0o700, exist_ok=True)
        if proof_dir.is_symlink():
            raise PublicationError("quality proof directory may not be a symlink")
        proof_session = proof_dir / f"{manifest['run_id']}.jsonl"
        save_bytes(proof_session, session)
        sentinel = (root / manifest["permitted_staging_path"]).read_bytes()
        save_bytes(proof_dir / "sentinel.json", sentinel)
        value = {
            "schema_version": 1,
            "run_id": manifest["run_id"],
            "date": manifest["date"],
            "slug": receipt["slug"],
            "post": ownership["post"],
            "receipt": receipt,
            "baseline_sha": manifest["baseline_sha"],
            "producer_attempt": attempt,
            "sealed_at": workspace.stamp(),
            "artifact_hashes": hashes,
            "session_sha256": sha(session),
            "sentinel_sha256": sha(sentinel),
            "hugo_version": version,
            "verifier_sha256": sha(Path(contract.__file__).read_bytes()),
            "publication_helper_sha256": sha(Path(__file__).read_bytes()),
            "checks": {"contract": "pass", "build": "pass", "voice": "pass"},
            "title": fields["title"],
            "tier": min(receipt["tier"], structural_tier),
            "canonical_url": f"https://startaitools.com/posts/{receipt['slug']}/",
            "github_links": sorted(
                set(
                    re.findall(
                        r"https://github\.com/(?:jeremylongshore|intent-solutions-io)/"
                        r"[A-Za-z0-9_-][A-Za-z0-9_.-]*",
                        post.read_text(),
                    )
                )
            ),
        }
        workspace.atomic_json(manifest_path.parent / "quality-seal.json", value)
        manifest.update(
            quality_seal_sha256=sha((manifest_path.parent / "quality-seal.json").read_bytes()),
            status="sealed",
            delivery_status="pending",
        )
        workspace.atomic_json(manifest_path, manifest)
        workspace.event(manifest, "quality sealed; delivery pending source/public verification")
        return {"outcome": "sealed", "run_id": manifest["run_id"], "slug": receipt["slug"]}


def read_quality_seal(manifest_path: Path, manifest: dict) -> dict:
    path = manifest_path.parent / "quality-seal.json"
    if path.is_symlink() or not path.is_file():
        raise PublicationError(
            "genuine precommit quality seal missing; source alone is insufficient"
        )
    raw = path.read_bytes()
    if sha(raw) != manifest.get("quality_seal_sha256"):
        raise PublicationError("quality seal hash does not match retained manifest")
    seal = strict_json(raw.decode())
    if (
        seal.get("schema_version") != 1
        or any(seal.get(key) != manifest.get(key) for key in ("date", "run_id", "baseline_sha"))
        or seal.get("checks") != {"contract": "pass", "build": "pass", "voice": "pass"}
    ):
        raise PublicationError("quality seal identity or mandatory checks mismatch")
    proof = manifest_path.parent / "quality-proof"
    for name, expected in (
        (f"{manifest['run_id']}.jsonl", seal["session_sha256"]),
        ("sentinel.json", seal["sentinel_sha256"]),
    ):
        path = proof / name
        if proof.is_symlink() or path.is_symlink() or sha(path.read_bytes()) != expected:
            raise PublicationError("retained genuine quality proof changed")
    return seal


def verify_candidate_seal(manifest: dict, *, committed: bool) -> None:
    """Reject a changed candidate before its commit can be pushed."""
    root = Path(manifest["workspace"])
    seal = read_quality_seal(root.parent / "manifest.json", manifest)
    workspace = module("blog-run-workspace")
    for name, expected in seal["artifact_hashes"].items():
        current = (
            workspace.git(root, "show", f"HEAD:{name}")
            if committed
            else (workspace.safe_file(root, name).read_bytes())
        )
        if sha(current) != expected:
            raise PublicationError("candidate artifact differs from sealed quality revision")
    sentinel = workspace.safe_file(root, manifest["permitted_staging_path"])
    # A successful land consumes its sentinel after delivery. The immutable
    # retained proof still binds a repeated completion to the original review.
    consumed = (
        manifest.get("status") == "published"
        and manifest.get("delivery_status") == "complete"
        and not sentinel.exists()
    )
    if not consumed and sha(sentinel.read_bytes()) != seal["sentinel_sha256"]:
        raise PublicationError("candidate sentinel differs from sealed quality proof")


def verified_seal(manifest_path: Path, manifest: dict) -> dict:
    seal = read_quality_seal(manifest_path, manifest)
    workspace = module("blog-run-workspace")
    root = Path(manifest["workspace"])
    published = manifest.get("published_sha")
    if not published or manifest.get("status") != "published":
        raise PublicationError("source publication has not been verified")
    remote = workspace.remote_master(root, manifest["remote_url"])
    result = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", published, remote],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise PublicationError("sealed source commit is not on the configured remote")
    for name, expected in seal["artifact_hashes"].items():
        if sha(workspace.git(root, "show", f"{published}:{name}")) != expected:
            raise PublicationError("published artifacts differ from the quality-sealed revision")
    if (
        sha(workspace.git(root, "show", f"{remote}:{seal['post']}"))
        != seal["receipt"]["post_sha256"]
    ):
        raise PublicationError("remote article changed since this quality seal")
    return seal


def verify_public(url: str) -> None:
    result = subprocess.run(
        [
            "curl",
            "-sfL",
            "--max-time",
            "20",
            "-o",
            "/dev/null",
            "--write-out",
            "%{http_code}\n%{url_effective}",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=22,
        check=False,
    )
    if result.returncode or result.stdout != f"200\n{url}":
        raise PublicationError("sealed public article unavailable; delivery remains pending")


def source_reference(seal: dict, manifest: dict) -> dict:
    """Called only after retained quality proof and publication are verified."""
    return {
        "schema_version": 1,
        "provenance": "quality-sealed-git",
        "commit": manifest["published_sha"],
        "path": seal["post"],
        "sha256": seal["receipt"]["post_sha256"],
        "date": seal["date"],
        "run_id": seal["run_id"],
        "quality_seal_sha256": manifest["quality_seal_sha256"],
    }


def delivery_rows(seal: dict, manifest: dict) -> tuple[dict, dict | None]:
    published_at = manifest["published_at"]
    moment = dt.datetime.fromisoformat(published_at)
    if moment.tzinfo is None:
        raise PublicationError("source publication observation must include UTC offset")
    common = {key: seal[key] for key in ("slug", "title", "canonical_url", "tier")}
    common.update(
        published_at=published_at,
        publication_timestamp_source="source-observed",
        run_id=seal["run_id"],
        post_sha256=seal["receipt"]["post_sha256"],
        source=source_reference(seal, manifest),
    )

    def status(value):
        return {"status": value, "posted_at": None, "url": None, "by": None}

    ledger = {
        **common,
        "date": seal["date"],
        "github_links": seal["github_links"],
        "packet_sent": False,
        "syndication": {
            name: status(
                "pending" if seal["tier"] >= 2 or name.startswith("li_") or name == "x" else "n/a"
            )
            for name in ("x", "li_personal", "li_company", "substack", "medium")
        },
    }
    queue = None
    if seal["tier"] >= 2:
        due = (moment + dt.timedelta(hours=24)).isoformat()
        queue = {
            **common,
            "devto": {"status": "pending", "publish_after": due},
            "hashnode": {"status": "pending", "publish_after": due},
            "medium": {"status": "skipped", "error": "Medium API cross-posting retired."},
        }
    return ledger, queue


def insert_missing(path: Path, entry: dict) -> bool:
    rows = load_state(path)
    existing = next((row for row in rows if row["slug"] == entry["slug"]), None)
    if existing is not None:
        validate_delivery_row(path.name, existing)
        for key in ("date", "canonical_url", "tier", "run_id", "post_sha256", "source"):
            if (
                key in entry
                and (key in existing or key in ("date", "canonical_url", "tier"))
                and existing.get(key) != entry[key]
            ):
                raise PublicationError(
                    "existing delivery identity conflicts with sealed publication"
                )
        # Upgrade an interrupted older sealed handoff without resetting receipts.
        if "source" not in existing and "source" in entry:
            existing["source"] = entry["source"]
            atomic_state(path, rows)
        return False
    atomic_state(path, [*rows, entry])
    return True


def validate_delivery_row(filename: str, row: dict) -> None:
    for key in ("slug", "title", "canonical_url", "published_at"):
        if not isinstance(row.get(key), str) or not row[key]:
            raise PublicationError("existing delivery row is incomplete")
    if type(row.get("tier")) is not int or row["tier"] not in (1, 2, 3):
        raise PublicationError("existing delivery tier is invalid")
    if dt.datetime.fromisoformat(row["published_at"]).tzinfo is None:
        raise PublicationError("existing publication timestamp lacks timezone")
    if filename == ".blog-syndication-ledger.json":
        dt.date.fromisoformat(row.get("date", ""))
        if type(row.get("packet_sent")) is not bool or not isinstance(row.get("syndication"), dict):
            raise PublicationError("existing packet/syndication state is incomplete")
        destinations = [
            row["syndication"].get(name)
            for name in ("x", "li_personal", "li_company", "substack", "medium")
        ]
    else:
        destinations = [row.get(name) for name in ("devto", "hashnode")]
    for destination in destinations:
        if (
            not isinstance(destination, dict)
            or not isinstance(destination.get("status"), str)
            or not destination["status"]
        ):
            raise PublicationError("existing delivery destination state is incomplete")
        allowed = (
            {"pending", "posted", "assumed_posted", "not_posted", "n/a"}
            if (filename == ".blog-syndication-ledger.json")
            else {"pending", "dispatching", "published", "ambiguous", "failed", "skipped", "n/a"}
        )
        if destination["status"] not in allowed:
            raise PublicationError("existing delivery destination state is unsupported")
        if filename == ".crosspost-queue.json" and destination["status"] == "pending":
            if dt.datetime.fromisoformat(destination.get("publish_after", "")).tzinfo is None:
                raise PublicationError("existing API due time lacks timezone")


def failure_detail(exc: Exception) -> str:
    """Persist actionable known reasons without exposing arbitrary exception data."""
    known = {
        "genuine precommit quality seal missing; source alone is insufficient",
        "quality seal hash does not match retained manifest",
        "quality seal identity or mandatory checks mismatch",
        "retained genuine quality proof changed",
        "source publication has not been verified",
        "sealed source commit is not on the configured remote",
        "published artifacts differ from the quality-sealed revision",
        "remote article changed since this quality seal",
        "sealed public article unavailable; delivery remains pending",
        "existing delivery identity conflicts with sealed publication",
        "existing delivery row is incomplete",
        "existing delivery destination state is unsupported",
        "existing delivery destination state is incomplete",
        "publication state transaction lock timed out",
    }
    if isinstance(exc, PublicationError) and str(exc) in known:
        return str(exc)
    if isinstance(exc, OSError):
        return "publication proof or state filesystem operation failed"
    return "publication proof, public response or delivery state validation failed"


def reconcile_delivery(
    manifest_path: Path, *, public_check=verify_public, after_ledger=None
) -> dict:
    no_canary()
    workspace = module("blog-run-workspace")
    manifest = workspace.load(manifest_path)
    with (
        workspace.locked(manifest_path.parent.parents[2]),
        workspace.producer_lock(manifest_path.parent),
    ):
        try:
            seal = verified_seal(manifest_path, manifest)
            public_check(seal["canonical_url"])
            ledger, queue = delivery_rows(seal, manifest)
            root = Path(manifest["source_repo"])
            with state_locked(root):
                added_ledger = insert_missing(root / ".blog-syndication-ledger.json", ledger)
                if after_ledger:
                    after_ledger()
                added_queue = (
                    insert_missing(root / ".crosspost-queue.json", queue) if queue else False
                )
            manifest.update(delivery_status="complete", delivery_completed_at=workspace.stamp())
            manifest.pop("delivery_error", None)
            manifest.pop("delivery_error_detail", None)
            workspace.atomic_json(manifest_path, manifest)
            workspace.event(manifest, "delivery rows verified; existing statuses preserved")
            return {
                "outcome": "delivery-complete",
                "ledger_inserted": added_ledger,
                "queue_inserted": added_queue,
                "run_id": manifest["run_id"],
            }
        except Exception as exc:
            manifest.update(
                delivery_status="pending",
                delivery_error=type(exc).__name__,
                delivery_error_detail=failure_detail(exc),
            )
            workspace.atomic_json(manifest_path, manifest)
            workspace.event(manifest, "delivery remains pending; proof/public/state check failed")
            raise


def recover_deliveries(current_manifest: Path) -> dict:
    no_canary()
    workspace = module("blog-run-workspace")
    workspace.verify_pipeline_lock()
    current = workspace.load(current_manifest)
    registry = current_manifest.parent.parents[2]
    count, failures = 0, []
    for path in sorted(registry.glob("runs/*/*/manifest.json")):
        previous = workspace.load(path, require_workspace=False)
        if (
            previous["source_repo"] != current["source_repo"]
            or previous["remote_url"] != current["remote_url"]
        ):
            raise PublicationError("recovery registry contains a different publication owner")
        if previous.get("status") == "published" and previous.get("delivery_status") == "pending":
            try:
                reconcile_delivery(path)
                count += 1
            except Exception as exc:
                failures.append(
                    {
                        "run_id": previous["run_id"],
                        "date": previous["date"],
                        "category": type(exc).__name__,
                        "detail": failure_detail(exc),
                    }
                )
    return {
        "outcome": "degraded" if failures else "reconciled",
        "runs": count,
        "failures": failures,
    }


def check_existing(manifest_path: Path, slug: str) -> dict:
    """Legacy rows may be retained, but source alone cannot invent delivery work."""
    no_canary()
    workspace = module("blog-run-workspace")
    manifest = workspace.load(manifest_path)
    root = Path(manifest["source_repo"])
    with state_locked(root):
        ledger = next(
            (
                row
                for row in load_state(root / ".blog-syndication-ledger.json")
                if row["slug"] == slug
            ),
            None,
        )
        if (
            ledger is None
            or ledger.get("date") != manifest["date"]
            or ledger.get("canonical_url") != f"https://startaitools.com/posts/{slug}/"
            or type(ledger.get("tier")) is not int
            or ledger["tier"] not in (1, 2, 3)
        ):
            raise PublicationError("existing public post has no verified delivery identity")
        validate_delivery_row(".blog-syndication-ledger.json", ledger)
        if ledger["tier"] >= 2:
            queue = next(
                (row for row in load_state(root / ".crosspost-queue.json") if row["slug"] == slug),
                None,
            )
            if (
                queue is None
                or queue.get("canonical_url") != ledger["canonical_url"]
                or queue.get("tier") != ledger["tier"]
            ):
                raise PublicationError("existing public post is missing required API queue state")
            validate_delivery_row(".crosspost-queue.json", queue)
    return {"outcome": "existing-delivery-present"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="action", required=True)
    update = subs.add_parser("update")
    update.add_argument("--file", type=Path, required=True)
    update.add_argument("--slug", required=True)
    update.add_argument("--patch-json", required=True)
    seal = subs.add_parser("seal")
    seal.add_argument("--manifest", type=Path, required=True)
    seal.add_argument("--transcript", type=Path, help="advisory corroboration only")
    seal.add_argument("--hugo", default="hugo")
    for action in ("reconcile", "recover"):
        command = subs.add_parser(action)
        command.add_argument("--manifest", type=Path, required=True)
    existing = subs.add_parser("check-existing")
    existing.add_argument("--manifest", type=Path, required=True)
    existing.add_argument("--slug", required=True)
    args = parser.parse_args()
    try:
        no_canary()
        if args.action == "update":
            update_row(args.file, args.slug, strict_json(args.patch_json))
            result = {"outcome": "updated"}
        elif args.action == "seal":
            result = seal_quality(args.manifest, args.transcript, args.hugo)
        elif args.action == "reconcile":
            result = reconcile_delivery(args.manifest)
        elif args.action == "check-existing":
            result = check_existing(args.manifest, args.slug)
        else:
            result = recover_deliveries(args.manifest)
        print(json.dumps(result))
        return 2 if result.get("outcome") == "degraded" else 0
    except Exception as exc:
        print(
            json.dumps(
                {"outcome": "failed", "category": type(exc).__name__, "detail": failure_detail(exc)}
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
