"""Stage the producer's roles receipt for offline fixtures.

Completion authority is what each mandatory Agent PRODUCED, staged under
`.blog-staging/DATE.RUN.role-AGENT.json` and bound by `DATE.RUN.roles.json`.
These helpers play the producer's part. `restage_roles` derives the staged
outputs from a synthetic fixture transcript by reading its plain rows directly
(never through the contract's own parser) so scenario tests can keep expressing
"this agent never returned" or "this reviewer said BLOCK" as fixture edits.
"""

import hashlib
import json
from pathlib import Path


def _text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict))
    return ""


def stage_roles(repo, *, date, run_id, slug, post, outputs, statuses=None):
    staging = Path(repo) / ".blog-staging"
    staging.mkdir(exist_ok=True)
    prefix = f"{date}.{run_id}"
    for stale in staging.glob(f"{prefix}.role-*.json"):
        stale.unlink()
    roles = {}
    for agent, text in outputs.items():
        body = json.dumps({"agent": agent, "date": date, "run_id": run_id, "output": text})
        (staging / f"{prefix}.role-{agent}.json").write_text(body)
        roles[agent] = {
            "status": (statuses or {}).get(agent, "completed"),
            "output_sha256": hashlib.sha256(body.encode()).hexdigest(),
        }
    for agent, status in (statuses or {}).items():
        roles.setdefault(agent, {"status": status})
    receipt = {
        "schema_version": 1,
        "date": date,
        "slug": slug,
        "run_id": run_id,
        "post_sha256": hashlib.sha256(Path(post).read_bytes()).hexdigest(),
        "roles": roles,
    }
    path = staging / f"{prefix}.roles.json"
    path.write_text(json.dumps(receipt))
    return path


def restage_roles(repo, transcript, *, date, run_id, post, slug=None):
    """Re-derive the staged receipt from a synthetic transcript's plain rows."""
    calls, results = {}, {}
    for line in Path(transcript).read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        message = row.get("message") if isinstance(row, dict) else None
        content = message.get("content") if isinstance(message, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                calls[block["id"]] = block.get("input", {}).get("subagent_type")
            elif block.get("type") == "tool_result":
                results[block.get("tool_use_id")] = block
    outputs, statuses = {}, {}
    for call, agent in calls.items():  # a later invocation replaces an earlier one
        outputs.pop(agent, None)
        statuses.pop(agent, None)
        block = results.get(call)
        if block is None:
            statuses[agent] = "pending"
        elif block.get("is_error"):
            statuses[agent] = "failed"
        else:
            outputs[agent] = _text(block.get("content")) or "offline fixture result"
    return stage_roles(
        repo,
        date=date,
        run_id=run_id,
        slug=slug or Path(post).stem,
        post=post,
        outputs=outputs,
        statuses=statuses,
    )
