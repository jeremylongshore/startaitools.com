"""Output-based completion: what each mandatory Agent PRODUCED, staged and hash-bound.

This is completion authority (startaitools.com#86). Nothing here reads how the CLI
logged a session; it re-hashes staged bytes and reads gate verdicts from them.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .errors import ContractError, Identity
from .jsonio import digest, parse_json, reject_constant, unique_object

ROLE_STATUSES_FAILED = ("failed", "cancelled", "killed", "timed_out", "unavailable")


def contains_code(post: Path) -> bool:
    body = post.read_text().splitlines()
    return any(
        re.match(r"^\s*(?:`{3,}|~{3,})", line) or re.match(r"^(?: {4}|\t)\S", line) for line in body
    )


def receipt_objects(value: Any) -> list[dict[str, Any]]:
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


def staged_file(repo: Path, identity: Identity, suffix: str) -> Path:
    """Resolve one run-scoped staging record without following links out."""
    for key in ("date", "run_id"):
        if not re.fullmatch(r"[0-9A-Za-z][0-9A-Za-z_-]*", str(identity[key])):
            raise ContractError(f"{key}: staging identity may not contain path syntax")
    path = repo / ".blog-staging" / f"{identity['date']}.{identity['run_id']}.{suffix}.json"
    if path.is_symlink() or path.parent.resolve() != path.parent.absolute():
        raise ContractError(f"{suffix}: staging record may not escape through a symlink")
    if not path.is_file():
        raise ContractError(f"{suffix}: staging record missing")
    return path


def receipt_roles(
    repo: Path, identity: Identity, post: Path, *, failures: dict[str, bool] | None = None
) -> dict[str, str]:
    """Read completion from what each role PRODUCED, never from how the CLI logged it.

    The producer stages one `role-AGENT.json` per mandatory Agent holding that
    Agent's actual returned output, plus a `roles.json` receipt binding every
    output SHA256 to the exact date/slug/run and final post revision. Verification
    re-hashes the staged bytes, so a receipt cannot vouch for output that is absent,
    empty, edited after the fact, or reviewed against different post bytes.
    """
    try:
        receipt = parse_json(staged_file(repo, identity, "roles").read_text())
    except ValueError as exc:
        raise ContractError("roles receipt is not valid JSON") from exc
    if not isinstance(receipt, dict) or any(receipt.get(k) != v for k, v in identity.items()):
        raise ContractError("roles receipt identity must match exact date/slug/run")
    if type(receipt.get("schema_version")) is not int or receipt["schema_version"] != 1:
        raise ContractError("roles receipt must be schema_version 1")
    if receipt.get("post_sha256") != digest(post):
        raise ContractError("roles receipt post revision does not match final post bytes")
    roles = receipt.get("roles")
    if not isinstance(roles, dict) or not roles:
        raise ContractError("roles receipt must list each mandatory role")
    completed = {}
    for agent, entry in roles.items():
        if not isinstance(agent, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", agent):
            raise ContractError("roles receipt role name invalid")
        if not isinstance(entry, dict):
            raise ContractError(f"{agent}: roles receipt entry must be an object")
        status = entry.get("status")
        if status in ROLE_STATUSES_FAILED:
            if failures is not None:
                failures[agent] = True
            continue
        if status != "completed":
            continue
        claimed = entry.get("output_sha256")
        if not isinstance(claimed, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed):
            raise ContractError(f"{agent}: roles receipt output_sha256 invalid")
        path = staged_file(repo, identity, f"role-{agent}")
        if digest(path) != claimed:
            raise ContractError(f"{agent}: staged role output differs from receipt hash")
        try:
            output = parse_json(path.read_text())
        except ValueError as exc:
            raise ContractError(f"{agent}: staged role output is not valid JSON") from exc
        if (
            not isinstance(output, dict)
            or output.get("agent") != agent
            or any(output.get(k) != v for k, v in identity.items() if k != "slug")
            or not isinstance(output.get("output"), str)
            or not output["output"].strip()
        ):
            raise ContractError(f"{agent}: staged role output missing identity or content")
        completed[agent] = output["output"]
    return completed


def validate_gate_receipts(
    completed: dict[str, Any], tier: int, post: Path, identity: Identity
) -> None:
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


def required_agents(tier: int, post: Path, audit: dict[str, Any]) -> set[str]:
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
