"""Sanitized CLI 2.1.274 mid-turn task-delivery fixtures; never queue acknowledgements."""

import copy
import json
import re

import pytest
import test_blog_producer_contract as producer_fixture
from test_native_async_agent_completion import RUN, check, contract, invocation, notification

DATE = producer_fixture.DATE
CONTRACT_RUN = producer_fixture.RUN
produced = producer_fixture.produced


def attachment(call="call-one", status="completed", output="genuine fixture output"):
    return {
        "type": "attachment",
        "sessionId": RUN,
        "isSidechain": False,
        "attachment": {
            "type": "queued_command",
            "commandMode": "task-notification",
            "prompt": notification(call, status, output)["message"]["content"],
            "source_uuid": "a653ef72-48fc-4a13-931d-e30a2f3351c6",
            "timestamp": "2026-09-18T04:01:02.003Z",
        },
    }


@pytest.mark.parametrize("background", [None, False, True])
def test_valid_typed_delivery_completes_actual_pending_call(tmp_path, background):
    assert check(tmp_path, invocation(background=background) + [attachment()]) == {
        "blog-classifier": "genuine fixture output"
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("type", "file"),
        ("type", "task-status"),
        ("type", None),
        ("commandMode", "prompt"),
        ("commandMode", "task_status"),
        ("commandMode", None),
        ("prompt", []),
        ("source_uuid", None),
        ("source_uuid", False),
        ("source_uuid", "not-a-uuid"),
        ("timestamp", None),
        ("timestamp", "not-a-time"),
        ("timestamp", "2026-09-18T04:01:02"),
    ],
)
def test_wrong_or_missing_native_attachment_metadata_cannot_complete(tmp_path, field, value):
    row = attachment()
    if value is None:
        row["attachment"].pop(field)
    else:
        row["attachment"][field] = value
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("value", [None, [], False, "malformed"])
def test_wrong_attachment_object_shape_is_not_delivery(tmp_path, value):
    row = attachment()
    row["attachment"] = value
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize(
    "field,value",
    [
        ("type", "user"),
        ("type", "queue-operation"),
        ("isSidechain", True),
        ("isSidechain", 0),
        ("isSidechain", None),
    ],
)
def test_non_native_or_sidechain_wrapper_cannot_complete(tmp_path, field, value):
    row = attachment()
    row[field] = value
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("session", [None, "foreign-session", False])
def test_attachment_session_binding_is_mandatory(tmp_path, session):
    row = attachment()
    row["sessionId"] = session
    with pytest.raises(contract.ContractError, match="different session"):
        check(tmp_path, invocation() + [row])


def test_queue_enqueue_and_absorption_without_delivery_are_not_completion(tmp_path):
    payload = attachment()["attachment"]
    rows = invocation() + [
        {
            "type": "queue-operation",
            "operation": "enqueue",
            "sessionId": RUN,
            "timestamp": payload["timestamp"],
            "content": payload["prompt"],
        },
        {
            "type": "queue-operation",
            "operation": "remove",
            "reason": "absorbed_mid_turn",
            "sessionId": RUN,
            "timestamp": payload["timestamp"],
            "content": payload["prompt"],
        },
    ]
    assert check(tmp_path, rows) == {}


@pytest.mark.parametrize("kind", ["quoted-user", "manual-read", "task-status"])
def test_ordinary_prompt_or_manual_output_is_not_native_delivery(tmp_path, kind):
    payload = attachment()["attachment"]["prompt"]
    if kind == "quoted-user":
        row = {"type": "user", "sessionId": RUN, "message": {"role": "user", "content": payload}}
    else:
        row = {
            "sessionId": RUN,
            "message": {
                "content": [{"type": "tool_result", "tool_use_id": kind, "content": payload}]
            },
        }
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize(
    "tag,value",
    [
        ("task-id", "wrong-agent"),
        ("tool-use-id", "wrong-call"),
        ("output-file", "/wrong/output"),
        ("status", "running"),
    ],
)
def test_typed_delivery_keeps_task_call_output_status_binding(tmp_path, tag, value):
    row = attachment()
    row["attachment"]["prompt"] = re.sub(
        "<" + tag + ">.*?</" + tag + ">",
        "<" + tag + ">" + value + "</" + tag + ">",
        row["attachment"]["prompt"],
    )
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("tag", ["task-id", "tool-use-id", "output-file", "status", "result"])
def test_typed_delivery_reuses_strict_single_notification_fields(tmp_path, tag):
    row = attachment()
    row["attachment"]["prompt"] = row["attachment"]["prompt"].replace(
        "</result>", "</result><" + tag + ">duplicate</" + tag + ">", 1
    )
    assert check(tmp_path, invocation() + [row]) == {}


@pytest.mark.parametrize("output", ["", " \n "])
def test_typed_delivery_requires_nonempty_completed_output(tmp_path, output):
    assert check(tmp_path, invocation() + [attachment(output=output)]) == {}


def test_delivery_before_actual_launch_stays_pending(tmp_path):
    assert check(tmp_path, [attachment()] + invocation()) == {}


@pytest.mark.parametrize("status", ["failed", "cancelled", "killed", "timed_out"])
def test_last_typed_failure_invalidates_prior_sdk_completion(tmp_path, status):
    failures = {}
    assert (
        check(tmp_path, invocation() + [notification(), attachment(status=status)], failures) == {}
    )
    assert failures == {"blog-classifier": True}


def test_later_pending_invocation_invalidates_typed_completion(tmp_path):
    assert check(tmp_path, invocation() + [attachment()] + invocation("call-two")) == {}


@pytest.mark.parametrize(
    "invalid", [None, "BLOCK", "REVISE", "stale-hash", "wrong-run", "missing-receipt"]
)
def test_hard_gate_still_validates_actual_typed_completed_output(tmp_path, invalid):
    post = tmp_path / "fixture.md"
    post.write_text("```python\nprint('fixture')\n```\n")
    identity = {"run_id": RUN, "date": "2026-09-15", "slug": "fixture"}
    receipt = {
        "blog_gate_receipt": {
            **identity,
            "agent": "code-reviewer",
            "verdict": "PASS",
            "post_sha256": contract.digest(post),
        }
    }
    if invalid in ("BLOCK", "REVISE"):
        receipt["blog_gate_receipt"]["verdict"] = invalid
    elif invalid == "stale-hash":
        receipt["blog_gate_receipt"]["post_sha256"] = "0" * 64
    elif invalid == "wrong-run":
        receipt["blog_gate_receipt"]["run_id"] = "another-run"
    elif invalid == "missing-receipt":
        receipt = {"prose": "all gates passed"}
    completed = check(
        tmp_path, invocation(agent="code-reviewer") + [attachment(output=json.dumps(receipt))]
    )
    assert "code-reviewer" in completed
    if invalid:
        with pytest.raises(contract.ContractError, match="receipt|BLOCK/REVISE"):
            contract.validate_gate_receipts(completed, 1, post, identity)
    else:
        contract.validate_gate_receipts(completed, 1, post, identity)


@pytest.mark.parametrize("completion", ["completed", "failed", "absent"])
def test_transcript_delivery_shape_is_advisory_and_never_decides_the_contract(produced, completion):
    repo, post, _, transcript = produced
    decisions = repo / contract.DECISIONS
    before = decisions.read_bytes()
    classifier, audit = contract.records(decisions)[1:]
    rows = []
    for i, agent in enumerate(["blog-classifier", "content-marketer", "seo-meta-optimizer"]):
        call = "fixture-call-" + str(i)
        rows.extend(invocation(call, agent))
        if completion != "absent":
            rows.append(attachment(call, status=completion))
    for row in rows:
        row["sessionId"] = CONTRACT_RUN
    transcript.write_text("\n".join(map(json.dumps, rows)))
    # The CLI's private delivery envelope no longer decides publication: the staged
    # roles receipt does. Whatever this transcript shows, the verdict is the same.
    seen = contract.completed_agents(transcript, CONTRACT_RUN)
    assert bool(seen) is (completion == "completed")
    assert contract.validate(repo, DATE, CONTRACT_RUN, transcript)["outcome"] == "complete"
    contract.append_record(
        repo,
        DATE,
        post.stem,
        CONTRACT_RUN,
        copy.deepcopy(classifier),
        classifier_record=classifier,
        audit_record=audit,
        transcript=transcript,
    )
    assert decisions.read_bytes() == before
