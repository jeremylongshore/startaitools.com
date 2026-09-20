"""ADVISORY ONLY: parse the Claude CLI session JSONL for corroboration logging.

The format is private to the CLI and broke this pipeline twice (2.1.274 attachment
envelope, 2.1.27x promptSource). Nothing in here may grant or refuse completion.
The whole module is scheduled for deletion after seven unattended green nights
(first: 2026-09-19); keep it free of anything another module needs.
"""

from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path
from typing import Any

from .errors import ContractError
from .jsonio import records


def native_task_notification(record: dict[str, Any]) -> dict[str, str] | None:
    """Read CLI-origin completion, never a quoted message or a launch receipt."""
    if record.get("isSidechain") is not False:
        return None
    if record.get("type") == "attachment":
        # CLI 2.1.274 delivers callbacks absorbed during a turn through this
        # typed envelope. Queue enqueue/remove events alone are not delivery.
        attachment = record.get("attachment")
        if (
            not isinstance(attachment, dict)
            or attachment.get("type") != "queued_command"
            or attachment.get("commandMode") != "task-notification"
            or not isinstance(attachment.get("source_uuid"), str)
            or not re.fullmatch(
                r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}",
                attachment["source_uuid"],
            )
            or not isinstance(attachment.get("timestamp"), str)
        ):
            return None
        try:
            timestamp = datetime.datetime.fromisoformat(attachment["timestamp"])
        except ValueError:
            return None
        if timestamp.tzinfo is None:
            return None
        text = attachment.get("prompt")
    else:
        message = record.get("message", {})
        if (
            not isinstance(message, dict)
            or record.get("type") != "user"
            or message.get("role") != "user"
            or record.get("origin") != {"kind": "task-notification"}
            or record.get("promptSource") != "sdk"
        ):
            return None
        text = message.get("content")
    if (
        not isinstance(text, str)
        or not text.strip().startswith("<task-notification>")
        or not text.strip().endswith("</task-notification>")
        or text.count("<task-notification>") != 1
        or text.count("</task-notification>") != 1
        or text.count("<result>") != 1
        or text.count("</result>") != 1
    ):
        return None
    prefix, remainder = text.split("<result>", 1)
    result, _ = remainder.split("</result>", 1)
    if not result.strip():
        return None
    fields = {}
    for name in ("task-id", "tool-use-id", "status", "output-file"):
        if text.count("<" + name + ">") != 1 or text.count("</" + name + ">") != 1:
            return None
        values = re.findall(r"<" + name + r">([^<>]+)</" + name + r">", prefix)
        if len(values) != 1 or not values[0].strip():
            return None
        fields[name] = values[0].strip()
    return {**fields, "result": result}


def agent_result_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            item["text"]
            for item in value
            if isinstance(item, dict)
            and item.get("type") == "text"
            and isinstance(item.get("text"), str)
        )
    return ""


def completed_agents(
    transcript: Path, run_id: str, *, failures: dict[str, bool] | None = None
) -> dict[str, Any]:
    """Require actual Agent dispatch AND matching last invocation completion."""
    calls, results, notifications = {}, {}, {}
    for position, record in enumerate(records(transcript)):
        message = record.get("message", {})
        if not isinstance(message, dict):
            raise ContractError("Agent transcript message must be an object")
        if record.get("message") and record.get("sessionId") != run_id:
            raise ContractError("Agent transcript belongs to a different session")
        notification = native_task_notification(record)
        if notification:
            if record.get("sessionId") != run_id:
                raise ContractError("Agent transcript belongs to a different session")
            notifications[notification["tool-use-id"]] = (position, notification)
        content = message.get("content", [])
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                raise ContractError("Agent transcript content block must be an object")
            if block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task"):
                inputs = block.get("input", {})
                if not isinstance(inputs, dict):
                    raise ContractError("Agent transcript input must be an object")
                call, agent = block.get("id"), inputs.get("subagent_type")
                if not isinstance(call, str) or not call or not isinstance(agent, str) or not agent:
                    raise ContractError("Agent transcript requires tool call and Agent identity")
                if call in calls:
                    raise ContractError("duplicate Agent tool call identity")
                calls[call] = (
                    agent,
                    bool(inputs.get("run_in_background")),
                    position,
                )
            elif block.get("type") == "tool_result":
                results[block.get("tool_use_id")] = (position, block, record.get("toolUseResult"))
    completed = {}
    for call, (agent, background, dispatch_position) in calls.items():
        result = results.get(call)
        block = result[1] if result and result[0] > dispatch_position else None
        completed.pop(agent, None)  # a failed/incomplete later call invalidates an earlier pass
        if failures is not None:
            failures.pop(agent, None)
            if agent and block and block.get("is_error"):
                failures[agent] = True
        if agent and block and not block.get("is_error"):
            native = result[2]
            if isinstance(native, dict) and native.get("status") in (
                "failed",
                "cancelled",
                "killed",
                "timed_out",
            ):
                if failures is not None:
                    failures[agent] = True
                continue
            if isinstance(native, dict) and (
                native.get("isAsync") is True
                or ("status" in native and native["status"] != "completed")
            ):
                pending = notifications.get(call)
                if (
                    not pending
                    or pending[0] <= result[0]
                    or not isinstance(native.get("agentId"), str)
                    or not native["agentId"]
                    or not isinstance(native.get("outputFile"), str)
                    or not native["outputFile"]
                    or pending[1]["task-id"] != native["agentId"]
                    or pending[1]["output-file"] != native["outputFile"]
                ):
                    continue
                notification = pending[1]
                if notification["status"] != "completed":
                    if failures is not None and notification["status"] in (
                        "failed",
                        "cancelled",
                        "killed",
                        "timed_out",
                    ):
                        failures[agent] = True
                    continue
                completed[agent] = notification["result"]
            elif not background:
                text = agent_result_text(block.get("content", ""))
                if text.strip() and not text.lstrip().startswith(
                    "Async agent launched successfully"
                ):
                    completed[agent] = block["content"]
    return completed


def transcript_advisory(transcript: Path | None, run_id: str, mandatory: set[str]) -> None:
    """Log what the CLI transcript shows. Advisory only: its format is private
    to the CLI and changed under us in 2.1.27x, rejecting four finished posts."""
    if transcript is None or not transcript.is_file():
        print("PRODUCER-CONTRACT: ADVISORY: no session transcript supplied", file=sys.stderr)
        return
    try:
        seen = completed_agents(transcript, run_id)
    except (ContractError, OSError, ValueError) as exc:
        print(f"PRODUCER-CONTRACT: ADVISORY: transcript unreadable: {exc}", file=sys.stderr)
        return
    unseen = sorted(mandatory - seen.keys())
    print(
        "PRODUCER-CONTRACT: ADVISORY: transcript corroborates "
        f"{len(mandatory) - len(unseen)}/{len(mandatory)} mandatory roles"
        + (f"; not visible in transcript: {', '.join(unseen)}" if unseen else ""),
        file=sys.stderr,
    )
