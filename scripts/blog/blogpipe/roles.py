"""Output-based completion: what each mandatory Agent PRODUCED, staged and hash-bound.

This is completion authority (startaitools.com#86). Nothing here reads how the CLI
logged a session; it re-hashes staged bytes and reads gate verdicts from them.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .brief import T1_CONSISTENCY_AGENT, enforced
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
    # Resolve OUTSIDE the try: ContractError is a ValueError, so a MISSING receipt used to
    # be reported as "not valid JSON". That message is now the repair instruction the
    # producer receives, so it has to name the real gap.
    receipt_path = staged_file(repo, identity, "roles")
    try:
        receipt = parse_json(receipt_path.read_text())
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
        carrier = output.get("subagent_type", agent)
        if carrier != agent:
            # 2026-10-03: four roles whose agent types were not loaded in the session
            # were run through a catch-all type and staged under the role's name, so
            # the receipt said complete for reviewers that never ran. A role is done
            # only when its own agent type produced the output; anything else is
            # `unavailable`, which refuses above.
            raise ContractError(
                f"{agent}: role output was produced by agent type {carrier!r}, not {agent!r}"
            )
        completed[agent] = output["output"]
    return completed


CONSISTENCY_AGENTS = ("blog-consistency-checker", "article-consistency-checker")
FACT_AGENTS = ("blog-fact-checker", "fact-checker")


def gate_agents(
    tier: int, post: Path, identity: Identity, completed: dict[str, Any] | None = None
) -> set[str]:
    """Every revision-bound reviewer whose PASS receipt this run must carry.

    Tier 1 joins the consistency gate (E01-T03): required from the amended-contract
    date, and before it, a checker that WAS staged must still PASS. A reviewer that
    ran and said REVISE is never quietly dropped because its tier did not need it.
    """
    gates = set()
    if contains_code(post):
        gates.add("code-reviewer")
    if tier >= 2:
        gates.update(CONSISTENCY_AGENTS)
    elif enforced(str(identity["date"])) or T1_CONSISTENCY_AGENT in (completed or {}):
        gates.add(T1_CONSISTENCY_AGENT)
    if tier >= 3:
        gates.update({*FACT_AGENTS, "seo-content-auditor"})
    return gates


def receipt_problem(agent: str, output: Any, expected: dict[str, Any]) -> str | None:
    """None when `output` carries exactly one PASS receipt for these exact bytes."""
    receipts = [
        item.get("blog_gate_receipt")
        for item in receipt_objects(output)
        if isinstance(item.get("blog_gate_receipt"), dict)
    ]
    if len(receipts) != 1:
        return "genuine structured gate receipt required"
    (receipt,) = receipts
    if receipt.get("agent") != agent or any(
        receipt.get(key) != value for key, value in expected.items()
    ):
        return "receipt target/revision mismatch (agent, date, slug, run or post_sha256)"
    if receipt.get("verdict") != "PASS":
        return f"gate verdict {receipt.get('verdict')!r} on the final bytes"
    return None


def soft_t1_consistency(tier: int, identity: Identity) -> bool:
    """Before the switch, the Tier 1 checker's receipt is observed, not enforced."""
    return tier == 1 and not enforced(str(identity["date"]))


def validate_gate_receipts(
    completed: dict[str, Any], tier: int, post: Path, identity: Identity
) -> set[str]:
    """Refuse unless every revision-bound gate PASSED these bytes; return the verified set.

    Pre-switch Tier 1 consistency (E01-T03 observation mode) is the one soft case:
    a staged checker whose receipt is missing, malformed or bound to other bytes or
    another run is NOT counted (it never reaches the footer) and is reported by
    `t1_consistency_gap` as an advisory instead of refusing. A matching REVISE or
    BLOCK verdict on these exact final bytes still refuses NOW, before the switch:
    the reviewer found a defect in what would publish, and that blocks at every tier.
    After the switch the checker is enforced exactly like every other gate.
    """
    gates = gate_agents(tier, post, identity, completed)
    expected = {**identity, "post_sha256": digest(post)}
    verified = set()
    for agent in sorted(gates):
        soft = agent == T1_CONSISTENCY_AGENT and soft_t1_consistency(tier, identity)
        if agent not in completed:
            if soft:
                continue
            raise ContractError(f"PENDING WORK: mandatory gate receipt missing: {agent}")
        problem = receipt_problem(agent, completed[agent], expected)
        if problem is None:
            verified.add(agent)
        elif not soft or problem.startswith("gate verdict"):
            raise ContractError(f"{agent}: gate BLOCK/REVISE or target/revision mismatch")
    return verified


def t1_consistency_gap(
    completed: dict[str, Any], tier: int, post: Path, identity: Identity
) -> str | None:
    """The amended-contract summary entry for the Tier 1 checker, if any."""
    if tier != 1:
        return None
    if T1_CONSISTENCY_AGENT not in completed:
        return f"{T1_CONSISTENCY_AGENT} (Tier 1 consistency gate)"
    expected = {**identity, "post_sha256": digest(post)}
    problem = receipt_problem(T1_CONSISTENCY_AGENT, completed[T1_CONSISTENCY_AGENT], expected)
    if problem is None or problem.startswith("gate verdict"):
        return None  # a PASS, or a REVISE/BLOCK that validate_gate_receipts refuses
    return f"{T1_CONSISTENCY_AGENT} receipt not counted: {problem}"


# Footer vocabulary (E01-T03): the posting packet renders ONLY these, from the seal.
CHECK_LABELS = {
    "hugo": "Hugo build",
    "voice-lint": "voice lint",
    "code-review": "code review",
    "consistency": "consistency check",
    "fact-check": "fact check against sources",
}


def performed_checks(repo: Path, identity: Identity, post: Path, tier: int) -> list[str]:
    """The checks that actually PASSED on these final bytes, for the disclaimer footer.

    Called by the quality seal after the contract and its own Hugo + voice-lint runs
    passed. Reviewer checks are read back from the staged receipts, never inferred
    from the tier, so a footer can never claim a check the run did not perform.
    """
    completed = receipt_roles(repo, identity, post)
    passed = validate_gate_receipts(completed, tier, post, identity)
    checks = ["hugo", "voice-lint"]
    if "code-reviewer" in passed:
        checks.append("code-review")
    if passed & set(CONSISTENCY_AGENTS):
        checks.append("consistency")
    if passed >= set(FACT_AGENTS):
        checks.append("fact-check")
    return checks


def required_agents(
    tier: int, post: Path, audit: dict[str, Any], date: str | None = None
) -> set[str]:
    agents = {"blog-classifier", "seo-meta-optimizer"}
    writer = audit.get("writer")
    if writer not in ("content-marketer", "docs-architect") or (
        tier >= 3 and writer != "docs-architect"
    ):
        raise ContractError("audit writer must name the actual tier writer")
    agents.add(writer)
    if contains_code(post):
        agents.add("code-reviewer")
    if tier == 1 and date is not None and enforced(date):
        agents.add(T1_CONSISTENCY_AGENT)
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
