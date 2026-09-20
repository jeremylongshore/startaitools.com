"""Validate scoped blog production; process exit alone is never completion.

Read-only verification is shared by the producer boundary and lander. Appends use
an exclusive file lock, preserve historical bytes and reject conflicting identities.
"""

from __future__ import annotations

import argparse
import fcntl
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .errors import ContractError, Identity
from .jsonio import digest, parse_json, records
from .roles import (
    contains_code,
    receipt_objects,
    receipt_roles,
    required_agents,
    validate_gate_receipts,
)
from .transcript import transcript_advisory

DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"


TIER_NAMES = {1: "Field Note", 2: "Technical Deep-Dive", 3: "Case Study"}


def target_posts(repo: Path, date: str) -> list[Path]:
    expression = re.compile(r"^date\s*(?:=|:)\s*[\'\"]?" + re.escape(date), re.M)
    return [
        p
        for p in (repo / "content/posts").glob("*.md")
        if expression.search(p.read_text().split("\n+++", 1)[0].split("\n---", 1)[0])
    ]


def final_post(repo: Path, date: str, *, strict: bool = False) -> Path:
    posts = target_posts(repo, date)
    if len(posts) != 1:
        raise ContractError(f"expected exactly one target post; found {len(posts)}")
    (post,) = posts
    spec = importlib.util.spec_from_file_location(
        "producer_publication_fields",
        Path(__file__).resolve().parents[1] / "blog_publication_state.py",
    )
    publication = importlib.util.module_from_spec(spec)
    # Verification is read-only: SourceFileLoader would create __pycache__ in
    # the producer's strict write-set. Compile the shared parser without caches.
    exec(compile(Path(spec.origin).read_bytes(), spec.origin, "exec"), publication.__dict__)
    try:
        fields, _ = publication.frontmatter(post.read_text())
    except ValueError as exc:
        raise ContractError("publishable front matter is invalid") from exc
    draft = fields.get("draft", False)
    if not (draft is False or (type(draft) is str and draft.lower() == "false")):
        raise ContractError("final post remains a draft; producer is not publication-ready")
    if strict:
        raw = post.read_text()
        if post.is_symlink() or post.parent.resolve() != post.parent.absolute():
            raise ContractError("final post may not escape the workspace through a symlink")
        # The fallback YAML reader returns strings for scalar values. Require an
        # unquoted false declaration to retain Boolean-false publication semantics.
        yaml_false = raw.startswith("---\n") and re.search(
            r"^draft:\s*false\s*(?:#.*)?$", raw.split("\n---", 1)[0], re.M
        )
        if not (fields.get("draft") is False or yaml_false):
            raise ContractError("staged final post requires explicit Boolean draft:false")
        if fields.get("slug") != post.stem or str(fields.get("date", ""))[:10] != date:
            raise ContractError("staged final front matter must match exact date/slug")
    return post


def validate_evidence(
    repo: Path,
    post: Path,
    identity: Identity,
    classifier: dict[str, Any],
    addendum: dict[str, Any],
    gates: dict[str, Any],
    transcript: Path | None,
) -> int:
    for record in (classifier, addendum):
        if not isinstance(record, dict) or any(record.get(k) != v for k, v in identity.items()):
            raise ContractError("staged classifier/audit identity must match exact date/slug/run")
        try:
            json.dumps(record, allow_nan=False)
        except (ValueError, TypeError) as exc:
            raise ContractError("staged classifier/audit must be finite JSON") from exc
    if classifier.get("audit_addendum") or addendum.get("audit_addendum") is not True:
        raise ContractError("staged pair requires classifier and separate audit addendum")
    run_id = identity["run_id"]
    tier = classifier.get("tier")
    if type(tier) is not int or tier not in (1, 2, 3):
        raise ContractError("classifier tier invalid or inconsistent")
    if not isinstance(classifier.get("tier_name"), str) or not classifier["tier_name"]:
        raise ContractError("classifier tier_name missing")
    confidence = classifier.get("confidence")
    if (
        type(confidence) not in (int, float)
        or not math.isfinite(confidence)
        or not 0 <= confidence <= 1
    ):
        raise ContractError("classifier confidence invalid")
    dimensions = classifier.get("dimensions")
    if not isinstance(dimensions, dict) or any(
        type(dimensions.get(key)) not in (int, float) or not 0 <= dimensions[key] <= 5
        for key in ("novelty", "arc", "nar", "tch", "scp", "rpr")
    ):
        raise ContractError("classifier dimensions missing or invalid")
    audit = addendum.get("agent_audit")
    if not isinstance(audit, dict):
        raise ContractError("agent_audit must be a structured object")
    if not isinstance(gates, dict):
        raise ContractError("readiness gates must be a structured object")
    required = {"build", "voice_lint"}
    if tier >= 2:
        required.add("consistency")
    if tier >= 3:
        required.add("fact_check")
    if contains_code(post):
        required.add("code_review")
    if any(gates.get(gate) != "pass" for gate in required):
        raise ContractError("required tier/build/voice/code gate did not PASS")
    validate_pattern_result(repo, classifier)
    failures: dict[str, bool] = {}
    completed = receipt_roles(repo, identity, post, failures=failures)
    mandatory = required_agents(tier, post, audit)
    transcript_advisory(transcript, run_id, mandatory)
    failed = mandatory & failures.keys()
    if failed:
        raise ContractError("mandatory Agent tool failed/unavailable: " + ", ".join(sorted(failed)))
    missing = mandatory - completed.keys()
    if missing:
        raise ContractError(
            "PENDING WORK: mandatory Agent completion missing: " + ", ".join(sorted(missing))
        )
    for agent in mandatory:
        if any(
            item.get("blog_gate_receipt", {}).get("verdict") in ("BLOCK", "REVISE")
            for item in receipt_objects(completed[agent])
            if isinstance(item.get("blog_gate_receipt"), dict)
        ):
            raise ContractError(f"{agent}: actual gate BLOCK/REVISE")
    validate_gate_receipts(completed, tier, post, identity)
    return tier


def validate_pattern_result(repo: Path, classifier: dict[str, Any]) -> None:
    """Replay the actual deterministic machine step without repairing authority."""
    records(repo / ".claude/skills/blog-backfill/methodology/patterns.jsonl")
    pattern = classifier.get("pattern_engine")
    required = {"ran", "ruleset_digest", "rules_evaluated", "tier_before", "tier_after", "matched"}
    if not isinstance(pattern, dict) or not required <= pattern.keys():
        raise ContractError("complete real pattern-engine receipt required")
    if (
        pattern["ran"] is not True
        or not isinstance(pattern["ruleset_digest"], str)
        or not re.fullmatch(r"[0-9a-f]{16}", pattern["ruleset_digest"])
        or type(pattern["rules_evaluated"]) is not int
        or pattern["rules_evaluated"] < 0
        or type(pattern["tier_before"]) is not int
        or pattern["tier_before"] not in TIER_NAMES
        or type(pattern["tier_after"]) is not int
        or pattern["tier_after"] not in TIER_NAMES
        or pattern["tier_after"] > pattern["tier_before"]
        or not isinstance(pattern["matched"], list)
        or any(not isinstance(item, str) or not item for item in pattern["matched"])
        or not isinstance(classifier.get("applied_patterns"), list)
        or classifier["applied_patterns"] != pattern["matched"]
        or pattern["tier_after"] != classifier["tier"]
    ):
        raise ContractError("pattern-engine receipt schema/tier/applied patterns inconsistent")
    provisional = {
        key: value
        for key, value in classifier.items()
        if key not in ("pattern_engine", "applied_patterns")
    }
    provisional.update(tier=pattern["tier_before"], tier_name=TIER_NAMES[pattern["tier_before"]])
    engine = repo / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    result = subprocess.run(
        [sys.executable, str(engine), "apply"],
        input=json.dumps(provisional, allow_nan=False),
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        raise ContractError(f"pattern-engine apply failed (exit {result.returncode})")
    try:
        replayed = parse_json(result.stdout)
    except ValueError as exc:
        raise ContractError("pattern-engine apply returned invalid JSON") from exc
    if not isinstance(replayed, dict) or any(
        json.dumps(replayed.get(key), sort_keys=True, allow_nan=False)
        != json.dumps(classifier.get(key), sort_keys=True, allow_nan=False)
        for key in ("tier", "tier_name", "applied_patterns", "pattern_engine")
    ):
        raise ContractError("pattern-engine deterministic result differs from classifier/receipt")


def validate_history(repo: Path, identity: Identity, current: bytes | None = None) -> None:
    baseline = subprocess.run(
        ["git", "-C", str(repo), "show", f"HEAD:{DECISIONS}"], capture_output=True, check=True
    ).stdout
    current = (repo / DECISIONS).read_bytes() if current is None else current
    if not current.startswith(baseline):
        raise ContractError("historical decisions changed; append-only contract violated")
    for line in current[len(baseline) :].decode().splitlines():
        if line.strip():
            record = parse_json(line)
            if any(record.get(k) != v for k, v in identity.items()):
                raise ContractError("appended decision escaped exact date/slug/run")


def validate(
    repo: Path,
    date: str,
    run_id: str,
    transcript: Path | None = None,
    *,
    preflight: bool = False,
) -> dict[str, Any]:
    post = final_post(repo, date, strict=True)
    slug = post.stem
    sentinel_path = repo / ".blog-staging" / f"{date}.intent.json"
    try:
        sentinel = parse_json(sentinel_path.read_text())
    except (OSError, ValueError) as exc:
        raise ContractError("missing or invalid readiness sentinel") from exc
    identity = {"date": date, "slug": slug, "run_id": run_id}
    if not isinstance(sentinel, dict) or any(sentinel.get(k) != v for k, v in identity.items()):
        raise ContractError("sentinel identity must match exact date/slug/run")
    if (
        type(sentinel.get("schema_version")) is not int
        or sentinel.get("schema_version") != 1
        or sentinel.get("ready") is not (not preflight)
    ):
        raise ContractError("sentinel must attest versioned ready completion")
    if sentinel.get("post_sha256") != digest(post):
        raise ContractError("sentinel post revision does not match current draft")
    all_records = records(repo / DECISIONS)
    scoped = [r for r in all_records if all(r.get(k) == v for k, v in identity.items())]
    classifiers = [r for r in scoped if "tier" in r and not r.get("audit_addendum")]
    audits = [r for r in scoped if r.get("audit_addendum") is True]
    if len(classifiers) != 1 or len(audits) != 1:
        raise ContractError("exactly one scoped classifier and agent_audit addendum required")
    (classifier,) = classifiers
    (addendum,) = audits
    tier = validate_evidence(
        repo, post, identity, classifier, addendum, sentinel.get("gates", {}), transcript
    )
    if type(sentinel.get("tier")) is not int or sentinel.get("tier") != tier:
        raise ContractError("classifier/sentinel tier invalid or inconsistent")
    validate_history(repo, identity)
    return {
        "outcome": "preflight-complete" if preflight else "complete",
        **identity,
        "tier": tier,
        "post_sha256": digest(post),
    }


def validate_staged(
    repo: Path,
    date: str,
    slug: str,
    run_id: str,
    classifier_record: dict[str, Any] | None,
    audit_record: dict[str, Any] | None,
    transcript: Path | None,
    *,
    current: bytes | None = None,
) -> dict[str, Any]:
    """Read actual staged/native evidence before making either authority append."""
    if classifier_record is None or audit_record is None:
        raise ContractError("staged classifier and audit are required before append")
    validate_manifest_binding(repo, date, slug, run_id)
    post = final_post(repo, date, strict=True)
    identity = {"date": date, "slug": slug, "run_id": run_id}
    if post.stem != slug:
        raise ContractError("staged final post must match requested slug")
    if not isinstance(audit_record, dict) or audit_record.get("post_sha256") != digest(post):
        raise ContractError("staged audit final post revision does not match current bytes")
    tier = validate_evidence(
        repo,
        post,
        identity,
        classifier_record,
        audit_record,
        audit_record.get("gates", {}),
        transcript,
    )
    validate_history(repo, identity, current)
    if digest(post) != audit_record["post_sha256"]:
        raise ContractError("staged final post changed during evidence validation")
    return {"outcome": "staged-complete", **identity, "tier": tier, "post_sha256": digest(post)}


def validate_manifest_binding(repo: Path, date: str, slug: str, run_id: str) -> None:
    binding = os.environ.get("BLOG_RUN_MANIFEST")
    if not binding:
        return
    path = Path(binding).absolute()
    if path.resolve() != path or not path.is_file():
        raise ContractError("append run manifest may not be missing or symlinked")
    manifest = parse_json(path.read_text())
    if (
        not isinstance(manifest, dict)
        or not isinstance(manifest.get("workspace"), str)
        or Path(manifest.get("workspace", "")).resolve() != repo.resolve()
        or manifest.get("date") != date
        or manifest.get("run_id") != run_id
        or manifest.get("status") != "ready"
        or manifest.get("quality_seal_sha256")
    ):
        raise ContractError("append escaped active manifest-bound workspace/date/run")
    posts = target_posts(repo, date)
    if len(posts) != 1 or posts[0].stem != slug:
        raise ContractError("append must identify the one final target post")
    lock = path.parent / "producer.lock"
    if not lock.is_file() or lock.is_symlink():
        raise ContractError("append requires inherited per-run producer lock")
    owned = lock.stat()
    for descriptor in Path("/proc/self/fd").iterdir():
        try:
            number = int(descriptor.name)
            candidate = os.fstat(number)
            info = Path(f"/proc/self/fdinfo/{number}").read_text()
        except (OSError, ValueError):
            continue
        if (
            (candidate.st_dev, candidate.st_ino) == (owned.st_dev, owned.st_ino)
            and "FLOCK" in info
            and "WRITE" in info
        ):
            return
    # Native Agent/Bash runtimes may close non-stdio descriptors in tool children.
    # The actual workspace.run parent must still own this exact kernel lease and
    # be a live ancestor; an unrelated process holding the inode is insufficient.
    ancestors = set()
    process = os.getpid()
    while process > 0 and process not in ancestors:
        ancestors.add(process)
        try:
            status = Path(f"/proc/{process}/stat").read_text().rsplit(")", 1)[1].split()
            process = int(status[1])
        except (OSError, ValueError, IndexError):
            break
    token = f"{os.major(owned.st_dev):02x}:{os.minor(owned.st_dev):02x}:{owned.st_ino}"
    for record in Path("/proc/locks").read_text().splitlines():
        fields = record.split()
        if len(fields) > 5 and "FLOCK" in fields and "WRITE" in fields and token in fields:
            try:
                if int(fields[4]) in ancestors:
                    return
            except ValueError:
                continue
    raise ContractError("append requires held owning per-run producer lock")


def append_record(
    repo: Path,
    date: str,
    slug: str,
    run_id: str,
    record: dict[str, Any],
    *,
    classifier_record: dict[str, Any] | None = None,
    audit_record: dict[str, Any] | None = None,
    transcript: Path | None = None,
) -> None:
    if not isinstance(record, dict):
        raise ContractError("append record must be a structured object")
    try:
        encoded = json.dumps(record, sort_keys=True, allow_nan=False) + "\n"
    except (ValueError, TypeError) as exc:
        raise ContractError("append record is not finite JSON") from exc
    identity = {"date": date, "slug": slug, "run_id": run_id}
    validate_manifest_binding(repo, date, slug, run_id)
    if any(record.get(k) != v for k, v in identity.items()):
        raise ContractError("append identity escaped requested target")
    if not record.get("audit_addendum") and type(record.get("tier")) is not int:
        raise ContractError("append requires a classifier or audit addendum")
    if record.get("audit_addendum") and not isinstance(record.get("agent_audit"), dict):
        raise ContractError("audit addendum requires agent_audit")
    path = repo / DECISIONS
    if path.is_symlink() or path.parent.resolve() != path.parent.absolute():
        raise ContractError("append authority path may not escape through a symlink")
    if classifier_record is None or audit_record is None:
        raise ContractError("staged classifier and audit are required before append")
    descriptor = os.open(path, os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        existing = handle.read()
        duplicate = False
        for line in existing.splitlines():
            if not line.strip():
                continue
            previous = parse_json(line)
            if not isinstance(previous, dict):
                raise ContractError("append source contains a non-object record")
            if previous.get("run_id") == run_id and any(
                previous.get(key) != identity[key] for key in ("date", "slug")
            ):
                raise ContractError("run identity already committed; refusing date/slug change")
            if all(previous.get(k) == v for k, v in identity.items()):
                staged = audit_record if previous.get("audit_addendum") else classifier_record
                if previous != staged:
                    raise ContractError("conflicting existing authority differs from staged pair")
            if all(previous.get(k) == v for k, v in identity.items()) and bool(
                previous.get("audit_addendum")
            ) == bool(record.get("audit_addendum")):
                if previous == record:
                    duplicate = True
                    continue
                raise ContractError("conflicting duplicate record; refusing overwrite")
        validate_manifest_binding(repo, date, slug, run_id)
        if record != classifier_record and record != audit_record:
            raise ContractError("conflicting append record differs from validated staged pair")
        validate_staged(
            repo,
            date,
            slug,
            run_id,
            classifier_record,
            audit_record,
            transcript,
            current=existing.encode(),
        )
        if duplicate:
            return
        if existing and not existing.endswith("\n"):
            raise ContractError("source missing final newline; refusing ambiguous append")
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["verify", "check-staged", "append"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--date", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--record", type=Path)
    parser.add_argument("--classifier-record", type=Path)
    parser.add_argument("--audit-record", type=Path)
    parser.add_argument("--transcript", type=Path, help="advisory corroboration only")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    try:
        if args.action in ("append", "check-staged"):
            if not args.slug or not args.classifier_record or not args.audit_record:
                raise ContractError(
                    "staged checks require --slug, --classifier-record and --audit-record"
                )
            classifier = parse_json(args.classifier_record.read_text())
            audit = parse_json(args.audit_record.read_text())
        if args.action == "check-staged":
            if args.preflight:
                raise ContractError("check-staged does not use a readiness sentinel or --preflight")
            print(
                json.dumps(
                    validate_staged(
                        args.repo,
                        args.date,
                        args.slug,
                        args.run_id,
                        classifier,
                        audit,
                        args.transcript,
                    )
                )
            )
        elif args.action == "append":
            if args.preflight:
                raise ContractError("preflight is read-only verification, never append")
            if not args.slug or not args.record:
                raise ContractError("append requires --slug and --record")
            append_record(
                args.repo,
                args.date,
                args.slug,
                args.run_id,
                parse_json(args.record.read_text()),
                classifier_record=classifier,
                audit_record=audit,
                transcript=args.transcript,
            )
        else:
            print(
                json.dumps(
                    validate(
                        args.repo, args.date, args.run_id, args.transcript, preflight=args.preflight
                    )
                )
            )
    except (ContractError, OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"PRODUCER-CONTRACT: FAILED: {exc}", file=sys.stderr)
        return 65
    return 0
