"""CLI 2.1.274 native async launch is not mandatory Agent completion."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "native_async_contract", ROOT / "scripts/blog/blog-producer-contract.py"
)
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)
RUN = "native-async-fixture"


def invocation(call="call-one", agent="blog-classifier", background=None):
    inputs = {"subagent_type": agent}
    if background is not None:
        inputs["run_in_background"] = background
    return [
        {
            "sessionId": RUN,
            "message": {
                "content": [{"type": "tool_use", "name": "Agent", "id": call, "input": inputs}]
            },
        },
        {
            "sessionId": RUN,
            "toolUseResult": {
                "isAsync": True,
                "status": "async_launched",
                "agentId": "agent-" + call,
                "outputFile": "/private/tasks/" + call + ".output",
            },
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": call,
                        "content": "Async agent launched successfully.",
                    }
                ]
            },
        },
    ]


def notification(call="call-one", status="completed", output="genuine fixture output"):
    return {
        "type": "user",
        "sessionId": RUN,
        "origin": {"kind": "task-notification"},
        "promptSource": "sdk",
        "isSidechain": False,
        "message": {
            "role": "user",
            "content": (
                "<task-notification>\n<task-id>agent-" + call + "</task-id>\n"
                "<tool-use-id>" + call + "</tool-use-id>\n"
                "<output-file>/private/tasks/" + call + ".output</output-file>\n"
                "<status>" + status + "</status>\n<summary>Native completion</summary>\n"
                "<result>" + output + "</result>\n<usage>fixture</usage>\n"
                "</task-notification>"
            ),
        },
    }


def check(tmp_path, rows, failures=None):
    transcript = tmp_path / (RUN + ".jsonl")
    transcript.write_text("\n".join(json.dumps(row) for row in rows))
    return contract.completed_agents(transcript, RUN, failures=failures)


@pytest.mark.parametrize("background", [None, False, True])
def test_async_launch_never_counts_as_completion(tmp_path, background):
    assert check(tmp_path, invocation(background=background)) == {}


@pytest.mark.parametrize("background", [None, False, True])
def test_native_bound_completion_returns_actual_output(tmp_path, background):
    assert check(tmp_path, invocation(background=background) + [notification()]) == {
        "blog-classifier": "genuine fixture output"
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("type", "assistant"),
        ("origin", {"kind": "user"}),
        ("promptSource", "cli"),
        ("isSidechain", True),
        ("origin", None),
    ],
)
def test_quoted_or_untrusted_notification_cannot_complete(tmp_path, field, value):
    row = notification()
    row[field] = value
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize(
    "tag,value",
    [
        ("task-id", "another-agent"),
        ("tool-use-id", "another-call"),
        ("output-file", "/foreign/output"),
        ("status", "running"),
    ],
)
def test_notification_identity_and_status_are_bound(tmp_path, tag, value):
    row = notification()
    import re

    row["message"]["content"] = re.sub(
        "<" + tag + ">.*?</" + tag + ">",
        "<" + tag + ">" + value + "</" + tag + ">",
        row["message"]["content"],
    )
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("tag", ["task-id", "tool-use-id", "output-file", "status", "result"])
def test_duplicate_notification_fields_are_not_completion(tmp_path, tag):
    row = notification()
    row["message"]["content"] = row["message"]["content"].replace(
        "<result>", "<" + tag + ">duplicate</" + tag + "><result>", 1
    )
    assert check(tmp_path, invocation() + [row]) == {}


def test_completion_before_launch_is_not_bound(tmp_path):
    assert check(tmp_path, [notification()] + invocation()) == {}


def test_foreign_session_notification_fails_closed(tmp_path):
    row = notification()
    row["sessionId"] = "foreign-session"
    with pytest.raises(contract.ContractError, match="different session"):
        check(tmp_path, invocation() + [row])


def test_later_pending_invocation_invalidates_prior_completion(tmp_path):
    rows = invocation() + [notification()] + invocation("call-two")
    assert check(tmp_path, rows) == {}


@pytest.mark.parametrize("status", ["failed", "cancelled", "killed", "timed_out"])
def test_native_failure_remains_visible(tmp_path, status):
    failures = {}
    assert check(tmp_path, invocation() + [notification(status=status)], failures) == {}
    assert failures == {"blog-classifier": True}


def test_hard_gate_output_is_completion_result_not_launch_text(tmp_path):
    output = json.dumps({"blog_gate_receipt": {"agent": "code-reviewer", "verdict": "BLOCK"}})
    completed = check(tmp_path, invocation(agent="code-reviewer") + [notification(output=output)])
    assert (
        contract.receipt_objects(completed["code-reviewer"])[0]["blog_gate_receipt"]["verdict"]
        == "BLOCK"
    )


def test_background_without_native_binding_cannot_complete(tmp_path):
    rows = invocation(background=True)
    del rows[1]["toolUseResult"]
    assert check(tmp_path, rows) == {}


@pytest.mark.parametrize(
    "invalid",
    [
        {"message": "malformed"},
        {"message": {"content": ["malformed"]}},
        {"message": {"content": [{"type": "tool_use", "name": "Agent", "input": "malformed"}]}},
    ],
)
def test_malformed_native_record_has_precise_contract_failure(tmp_path, invalid):
    invalid["sessionId"] = RUN
    with pytest.raises(contract.ContractError, match="Agent transcript"):
        check(tmp_path, [invalid])


def test_unknown_pending_native_status_is_not_synchronous_success(tmp_path):
    rows = invocation()
    del rows[1]["toolUseResult"]["isAsync"]
    rows[1]["toolUseResult"]["status"] = "running"
    assert check(tmp_path, rows) == {}


@pytest.mark.parametrize("tag", ["task-id", "tool-use-id", "output-file", "status"])
def test_duplicate_notification_fields_after_result_are_not_completion(tmp_path, tag):
    row = notification()
    row["message"]["content"] = row["message"]["content"].replace(
        "</result>", "</result><" + tag + ">duplicate</" + tag + ">", 1
    )
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("native", [None, [], False, "malformed"])
@pytest.mark.parametrize("shape", ["string", "text-blocks"])
def test_launch_ack_missing_native_metadata_is_not_synchronous_completion(tmp_path, native, shape):
    rows = invocation()
    rows[1]["toolUseResult"] = native
    if shape == "text-blocks":
        block = rows[1]["message"]["content"][0]
        block["content"] = [{"type": "text", "text": block["content"]}]
    assert check(tmp_path, rows) == {}


@pytest.mark.parametrize("output", ["", "  \n  "])
def test_empty_native_completion_result_does_not_attest_work(tmp_path, output):
    assert check(tmp_path, invocation() + [notification(output=output)]) == {}


@pytest.mark.parametrize("output", ["", None, False, {}, [], [{"type": "text", "text": None}]])
def test_empty_or_malformed_synchronous_output_does_not_attest_work(tmp_path, output):
    rows = invocation()
    del rows[1]["toolUseResult"]
    rows[1]["message"]["content"][0]["content"] = output
    assert check(tmp_path, rows) == {}


def test_native_tool_failure_status_is_visible_without_completed_notification(tmp_path):
    rows = invocation()
    rows[1]["toolUseResult"].update(isAsync=False, status="failed")
    failures = {}
    assert check(tmp_path, rows, failures) == {}
    assert failures == {"blog-classifier": True}


def test_tool_result_before_dispatch_cannot_complete(tmp_path):
    rows = invocation()
    assert check(tmp_path, [rows[1], rows[0], notification()]) == {}


def test_duplicate_dispatch_identity_is_precise_refusal(tmp_path):
    rows = invocation()
    with pytest.raises(contract.ContractError, match="duplicate Agent tool call"):
        check(tmp_path, rows + [notification(), rows[0]])


@pytest.mark.parametrize("field,value", [("id", None), ("id", ""), ("agent", None), ("agent", "")])
def test_agent_dispatch_requires_unambiguous_native_identity(tmp_path, field, value):
    rows = invocation()
    block = rows[0]["message"]["content"][0]
    if field == "id":
        block["id"] = value
    else:
        block["input"]["subagent_type"] = value
    with pytest.raises(contract.ContractError, match="requires tool call and Agent identity"):
        check(tmp_path, rows)
