#!/usr/bin/env python3
"""Validate scoped blog production; process exit alone is never completion.

Read-only verification is shared by the producer boundary and lander. Appends use
an exclusive file lock, preserve historical bytes and reject conflicting identities.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"


class ContractError(ValueError):
    pass


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError("duplicate JSON object key")
        value[key] = item
    return value


def reject_constant(_value):
    raise ContractError("non-finite JSON value")


def parse_json(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path):
    result = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = parse_json(line)
        except ValueError as exc:
            raise ContractError(f"{path.name}:{number}: invalid JSON") from exc
        if not isinstance(value, dict):
            raise ContractError(f"{path.name}:{number}: expected object")
        result.append(value)
    return result


def contains_code(post):
    body = post.read_text().splitlines()
    return any(
        re.match(r"^\s*(?:`{3,}|~{3,})", line) or re.match(r"^(?: {4}|\t)\S", line) for line in body
    )


def target_posts(repo, date):
    expression = re.compile(r"^date\s*(?:=|:)\s*[\'\"]?" + re.escape(date), re.M)
    return [
        p
        for p in (repo / "content/posts").glob("*.md")
        if expression.search(p.read_text().split("\n+++", 1)[0].split("\n---", 1)[0])
    ]


def receipt_objects(value):
    """Read structured receipts inside genuine tool result text, never prose claims."""
    if isinstance(value, list):
        text = "\n".join(
            block.get("text", "")
            for block in value
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        text = value if isinstance(value, str) else json.dumps(value)
    decoder = json.JSONDecoder(object_pairs_hook=unique_object, parse_constant=reject_constant)
    objects = []
    for match in re.finditer(r"\{", text):
        try:
            item, _ = decoder.raw_decode(text[match.start() :])
        except ValueError:
            continue
        if isinstance(item, dict):
            objects.append(item)
    return objects


def completed_agents(transcript, run_id):
    """Require actual Agent dispatch AND matching last invocation completion."""
    calls, results = {}, {}
    for record in records(transcript):
        if record.get("message") and record.get("sessionId") != run_id:
            raise ContractError("Agent transcript belongs to a different session")
        content = record.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                inputs = block.get("input", {})
                if not inputs.get("run_in_background"):
                    calls[block.get("id")] = inputs.get("subagent_type")
            elif block.get("type") == "tool_result":
                results[block.get("tool_use_id")] = block
    completed = {}
    for call, agent in calls.items():
        block = results.get(call)
        completed.pop(agent, None)  # a failed/incomplete later call invalidates an earlier pass
        if agent and block and not block.get("is_error"):
            completed[agent] = block.get("content", "")
    return completed


def validate_gate_receipts(completed, tier, post, identity):
    gates = set()
    if contains_code(post):
        gates.add("code-reviewer")
    if tier >= 2:
        gates.update({"blog-consistency-checker", "article-consistency-checker"})
    if tier >= 3:
        gates.update({"blog-fact-checker", "fact-checker", "seo-content-auditor"})
    expected = {**identity, "post_sha256": digest(post)}
    for agent in gates:
        receipts = [
            item.get("blog_gate_receipt")
            for item in receipt_objects(completed[agent])
            if isinstance(item.get("blog_gate_receipt"), dict)
        ]
        if len(receipts) != 1:
            raise ContractError(f"{agent}: genuine structured gate receipt required")
        (receipt,) = receipts
        if (
            receipt.get("agent") != agent
            or receipt.get("verdict") != "PASS"
            or any(receipt.get(key) != value for key, value in expected.items())
        ):
            raise ContractError(f"{agent}: gate BLOCK/REVISE or target/revision mismatch")


def required_agents(tier, post, audit):
    agents = {"blog-classifier", "seo-meta-optimizer"}
    writer = audit.get("writer")
    if writer not in ("content-marketer", "docs-architect") or (
        tier >= 3 and writer != "docs-architect"
    ):
        raise ContractError("audit writer must name the actual tier writer")
    agents.add(writer)
    if contains_code(post):
        agents.add("code-reviewer")
    if tier >= 2:
        agents.update(
            {
                "blog-consistency-checker",
                "article-consistency-checker",
                "seo-structure-architect",
                "seo-snippet-hunter",
                "seo-keyword-strategist",
            }
        )
    if tier >= 3:
        agents.update(
            {"blog-fact-checker", "fact-checker", "seo-authority-builder", "seo-content-auditor"}
        )
    return agents


def validate(repo, date, run_id, transcript=None, *, preflight=False):
    posts = target_posts(repo, date)
    if len(posts) != 1:
        raise ContractError(f"expected exactly one target post; found {len(posts)}")
    (post,) = posts
    spec = importlib.util.spec_from_file_location(
        "producer_publication_fields", Path(__file__).with_name("blog_publication_state.py")
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
    tier = classifier.get("tier")
    if (
        type(tier) is not int
        or tier not in (1, 2, 3)
        or type(sentinel.get("tier")) is not int
        or sentinel.get("tier") != tier
    ):
        raise ContractError("classifier/sentinel tier invalid or inconsistent")
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
    gates = sentinel.get("gates", {})
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
    records(repo / ".claude/skills/blog-backfill/methodology/patterns.jsonl")
    engine = repo / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    receipt = subprocess.run(
        [sys.executable, str(engine), "digest"], capture_output=True, text=True, check=True
    ).stdout.strip()
    pattern = classifier.get("pattern_engine", {})
    if not isinstance(pattern, dict):
        raise ContractError("pattern-engine receipt must be a structured object")
    if pattern.get("ran") is not True or pattern.get("ruleset_digest") != receipt:
        raise ContractError("pattern-engine current rules receipt missing or obsolete")
    baseline = subprocess.run(
        ["git", "-C", str(repo), "show", f"HEAD:{DECISIONS}"], capture_output=True, check=True
    ).stdout
    current = (repo / DECISIONS).read_bytes()
    if not current.startswith(baseline):
        raise ContractError("historical decisions changed; append-only contract violated")
    for line in current[len(baseline) :].decode().splitlines():
        if line.strip():
            record = parse_json(line)
            if any(record.get(k) != v for k, v in identity.items()):
                raise ContractError("appended decision escaped exact date/slug/run")
    if transcript is None or not transcript.is_file():
        raise ContractError("trusted producer transcript missing; agent receipts unverifiable")
    if transcript.name != f"{run_id}.jsonl" or transcript.resolve().is_relative_to(repo.resolve()):
        raise ContractError("Agent transcript must be the bound session outside the workspace")
    completed = completed_agents(transcript, run_id)
    missing = required_agents(tier, post, audit) - completed.keys()
    if missing:
        raise ContractError("mandatory Agent completion missing: " + ", ".join(sorted(missing)))
    validate_gate_receipts(completed, tier, post, identity)
    return {
        "outcome": "preflight-complete" if preflight else "complete",
        **identity,
        "tier": tier,
        "post_sha256": digest(post),
    }


def append_record(repo, date, slug, run_id, record):
    if not isinstance(record, dict):
        raise ContractError("append record must be a structured object")
    try:
        encoded = json.dumps(record, sort_keys=True, allow_nan=False) + "\n"
    except (ValueError, TypeError) as exc:
        raise ContractError("append record is not finite JSON") from exc
    identity = {"date": date, "slug": slug, "run_id": run_id}
    binding = os.environ.get("BLOG_RUN_MANIFEST")
    if binding:
        manifest = parse_json(Path(binding).read_text())
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
    if any(record.get(k) != v for k, v in identity.items()):
        raise ContractError("append identity escaped requested target")
    if not record.get("audit_addendum") and type(record.get("tier")) is not int:
        raise ContractError("append requires a classifier or audit addendum")
    if record.get("audit_addendum") and not isinstance(record.get("agent_audit"), dict):
        raise ContractError("audit addendum requires agent_audit")
    path = repo / DECISIONS
    if path.is_symlink() or path.parent.resolve() != path.parent.absolute():
        raise ContractError("append authority path may not escape through a symlink")
    descriptor = os.open(path, os.O_RDWR | os.O_APPEND | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        handle.seek(0)
        existing = handle.read()
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
            if all(previous.get(k) == v for k, v in identity.items()) and bool(
                previous.get("audit_addendum")
            ) == bool(record.get("audit_addendum")):
                if previous == record:
                    return
                raise ContractError("conflicting duplicate record; refusing overwrite")
        if existing and not existing.endswith("\n"):
            raise ContractError("source missing final newline; refusing ambiguous append")
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["verify", "append"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--date", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--record", type=Path)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "append":
            if args.preflight:
                raise ContractError("preflight is read-only verification, never append")
            if not args.slug or not args.record:
                raise ContractError("append requires --slug and --record")
            append_record(
                args.repo, args.date, args.slug, args.run_id, parse_json(args.record.read_text())
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


if __name__ == "__main__":
    sys.exit(main())
