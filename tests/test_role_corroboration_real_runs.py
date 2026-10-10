"""Regression: the advisory corroboration count on three real nightly runs.

The fixtures are the real producer sessions for 2026-10-03, 2026-10-04 and
2026-10-05, reduced to their Agent dispatch, tool result and task-notification
records, with agent prose and host paths removed. Before this fix the advisory
reported 1/9, 4/4 and 0/9 while the roles receipt said complete every night.

What actually ran (confirmed against each subagent's own CLI sidecar,
subagents/agent-*.meta.json, at investigation time):

* 2026-10-03, Tier 2, nine mandatory roles: five ran under their own agent type.
  The session had not loaded seo-meta-optimizer, seo-snippet-hunter,
  seo-keyword-strategist or code-reviewer ("Agent type ... not found"); the
  producer ran those briefs through the catch-all `claude` type and staged the
  output under the role names, so the receipt claimed nine completed roles.
* 2026-10-04, Tier 1, four mandatory roles: all four ran.
* 2026-10-05, Tier 2, nine mandatory roles: all nine ran.

The count moved because the CLI delivers a background Agent's completion in one
of two shapes: an attachment envelope when absorbed mid-turn, or its own user turn.
CLI 2.1.289 stamps the second with promptSource "system" and
origin {"kind": "task-notification", "producer": "session-task"}; the parser
accepted only promptSource "sdk" and an exact {"kind": ...} origin, so every
completion that started a turn was invisible. 2026-10-04 happened to receive all of
its completions mid-turn.
"""

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from blog_roles import stage_roles
from test_blog_producer_contract import DATE, RUN, contract, produced  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures"
OLD_PARSER = "35984b2c"  # origin/master when the three runs were logged

TIER2 = {
    "blog-classifier",
    "content-marketer",
    "seo-meta-optimizer",
    "seo-structure-architect",
    "seo-snippet-hunter",
    "seo-keyword-strategist",
    "blog-consistency-checker",
    "article-consistency-checker",
    "code-reviewer",
}
TIER1 = {"blog-classifier", "content-marketer", "seo-meta-optimizer", "code-reviewer"}
SUBSTITUTED = {
    "seo-meta-optimizer",
    "seo-snippet-hunter",
    "seo-keyword-strategist",
    "code-reviewer",
}

RUNS = {
    "2026-10-03": ("94c4389b-665c-4be8-864b-a388fa8fd619", TIER2, TIER2 - SUBSTITUTED, 1),
    "2026-10-04": ("80091962-213b-4ca5-acd0-d6232bf58d33", TIER1, TIER1, 4),
    "2026-10-05": ("5d0694b1-d897-4471-9ecf-619fceb67cbb", TIER2, TIER2, 0),
}


def fixture(date):
    run = RUNS[date][0]
    return FIXTURES / f"role-corroboration-{date}-{run[:8]}.transcript.jsonl", run


def advisory(transcript_module, path, run, mandatory, capsys):
    transcript_module.transcript_advisory(path, run, mandatory)
    return capsys.readouterr().err


@pytest.fixture(scope="module")
def old_parser(tmp_path_factory):
    """The advisory module as it was on the night of each run."""
    package = tmp_path_factory.mktemp("old") / "oldpipe"
    shutil.copytree(ROOT / "scripts/blog/blogpipe", package)
    (package / "transcript.py").write_bytes(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{OLD_PARSER}:scripts/blog/blogpipe/transcript.py"]
        )
    )
    sys.path.insert(0, str(package.parent))
    try:
        yield importlib.import_module("oldpipe.transcript")
    finally:
        sys.path.remove(str(package.parent))


@pytest.mark.parametrize("date", sorted(RUNS))
def test_old_parser_reproduces_the_logged_counts(old_parser, date, capsys):
    path, run = fixture(date)
    _, mandatory, _, logged = RUNS[date]
    line = advisory(old_parser, path, run, mandatory, capsys)
    assert f"corroborates {logged}/{len(mandatory)} mandatory roles" in line


@pytest.mark.parametrize("date", sorted(RUNS))
def test_corrected_count_is_what_ran_under_its_own_agent_type(date, capsys):
    path, run = fixture(date)
    _, mandatory, ran, _ = RUNS[date]
    assert mandatory & contract.completed_agents(path, run).keys() == ran
    line = advisory(contract, path, run, mandatory, capsys)
    assert f"corroborates {len(ran)}/{len(mandatory)} mandatory roles" in line
    if ran != mandatory:
        assert "not visible in transcript: " + ", ".join(sorted(mandatory - ran)) in line


def test_both_delivery_shapes_occur_in_the_real_runs():
    """The count depended on which shape each completion took, not on what ran."""
    for date in RUNS:
        path, _ = fixture(date)
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        turns = [r for r in rows if r.get("origin", {}).get("kind") == "task-notification"]
        assert {r["promptSource"] for r in turns} <= {"system"}
        assert all(
            r["origin"] == {"kind": "task-notification", "producer": "session-task"} for r in turns
        )
    shapes = {}
    for date in RUNS:
        rows = [json.loads(line) for line in fixture(date)[0].read_text().splitlines()]
        shapes[date] = (
            sum(r.get("type") == "attachment" for r in rows),
            sum("origin" in r for r in rows),
        )
    assert shapes["2026-10-04"][1] == 0  # every completion absorbed mid-turn: 4/4
    assert shapes["2026-10-05"][1] > 0 and shapes["2026-10-03"][1] > 0


def test_substituted_roles_were_refused_by_the_cli_then_run_as_claude():
    path, run = fixture("2026-10-03")
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    calls = {
        block["id"]: block["input"]["subagent_type"]
        for row in rows
        for block in row.get("message", {}).get("content", [])
        if isinstance(block, dict) and block.get("type") == "tool_use"
    }
    refused = {
        calls[block["tool_use_id"]]
        for row in rows
        for block in row.get("message", {}).get("content", [])
        if isinstance(block, dict) and block.get("type") == "tool_result" and block.get("is_error")
    }
    assert refused == SUBSTITUTED
    assert "claude" in contract.completed_agents(path, run)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("promptSource", "cli"),
        ("promptSource", None),
        ("origin", {"kind": "task-notification", "producer": 7}),
        ("origin", {"kind": "task-notification", "quoted": "yes"}),
        ("origin", {"kind": "user", "producer": "session-task"}),
    ],
)
def test_widened_shape_still_refuses_untrusted_notifications(field, value):
    path, run = fixture("2026-10-05")
    record = next(
        json.loads(line) for line in path.read_text().splitlines() if "origin" in json.loads(line)
    )
    assert contract.native_task_notification(record) is not None
    record[field] = value
    assert contract.native_task_notification(record) is None


def test_role_output_from_another_agent_type_is_refused(produced):  # noqa: F811
    """2026-10-03 staged catch-all output under role names; a receipt cannot say complete."""
    repo, post, _, transcript = produced
    staging = repo / ".blog-staging"
    role = staging / f"{DATE}.{RUN}.role-seo-meta-optimizer.json"
    receipt = staging / f"{DATE}.{RUN}.roles.json"
    value = json.loads(role.read_text())
    value["subagent_type"] = "claude"
    role.write_text(json.dumps(value))
    stored = json.loads(receipt.read_text())
    stored["roles"]["seo-meta-optimizer"]["output_sha256"] = contract.digest(role)
    receipt.write_text(json.dumps(stored))
    with pytest.raises(contract.ContractError, match="produced by agent type 'claude'"):
        contract.validate(repo, DATE, RUN, transcript)


def test_role_output_naming_its_own_agent_type_is_accepted(produced):  # noqa: F811
    repo, post, _, transcript = produced
    staging = repo / ".blog-staging"
    role = staging / f"{DATE}.{RUN}.role-seo-meta-optimizer.json"
    receipt = staging / f"{DATE}.{RUN}.roles.json"
    value = json.loads(role.read_text())
    value["subagent_type"] = "seo-meta-optimizer"
    role.write_text(json.dumps(value))
    stored = json.loads(receipt.read_text())
    stored["roles"]["seo-meta-optimizer"]["output_sha256"] = contract.digest(role)
    receipt.write_text(json.dumps(stored))
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"


def test_unavailable_role_refuses(produced):  # noqa: F811
    """The honest record for a role whose agent type was not loaded."""
    repo, post, _, transcript = produced
    outputs = dict.fromkeys(("blog-classifier", "content-marketer"), "offline fixture result")
    stage_roles(
        repo,
        date=DATE,
        run_id=RUN,
        slug=post.stem,
        post=post,
        outputs=outputs,
        statuses={"seo-meta-optimizer": "unavailable"},
    )
    with pytest.raises(contract.ContractError, match="failed/unavailable: seo-meta-optimizer"):
        contract.validate(repo, DATE, RUN, transcript)


# --- 2026-10-07: a third origin shape (CLI 2.1.294 adds origin.runId) -----------------
#
# The run for 2026-10-07 (executed 2026-10-08, CLI 2.1.294) logged 3/9 while its roles
# receipt said complete. Fixture: that session reduced the same way as above. All nine
# Tier 2 roles were dispatched under their own agent type, launched async, and each got
# a "completed" task-notification. The three seen arrived as attachment envelopes; the
# six missed arrived as their own turn with origin
# {"kind": "task-notification", "producer": "session-task", "runId": "..."}, and the
# parser from #153 rejected the unknown "runId" key.

RUN_1007 = "2847cb13-2ec1-491d-85bb-2e067c6ce3b4"
FIXTURE_1007 = FIXTURES / f"role-corroboration-2026-10-07-{RUN_1007[:8]}.transcript.jsonl"
PARSER_1007 = "43609125"  # transcript.py as deployed on the night of the run
SEEN_1007 = {"blog-classifier", "article-consistency-checker", "code-reviewer"}


@pytest.fixture(scope="module")
def parser_1007(tmp_path_factory):
    package = tmp_path_factory.mktemp("p1007") / "pipe1007"
    shutil.copytree(ROOT / "scripts/blog/blogpipe", package)
    (package / "transcript.py").write_bytes(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{PARSER_1007}:scripts/blog/blogpipe/transcript.py"]
        )
    )
    sys.path.insert(0, str(package.parent))
    try:
        yield importlib.import_module("pipe1007.transcript")
    finally:
        sys.path.remove(str(package.parent))


def rows_1007():
    return [json.loads(line) for line in FIXTURE_1007.read_text().splitlines()]


def test_1007_every_role_ran_under_its_own_agent_type_and_completed():
    rows = rows_1007()
    dispatched = [
        block["input"]["subagent_type"]
        for row in rows
        for block in row.get("message", {}).get("content", [])
        if isinstance(block, dict) and block.get("type") == "tool_use"
    ]
    assert sorted(dispatched) == sorted(TIER2)
    statuses = [
        (row.get("attachment") or {}).get("prompt") or row["message"]["content"]
        for row in rows
        if "origin" in row or row.get("type") == "attachment"
    ]
    assert len(statuses) == 9 and all("<status>completed</status>" in s for s in statuses)


def test_1007_parser_of_the_night_reproduces_the_logged_count(parser_1007, capsys):
    line = advisory(parser_1007, FIXTURE_1007, RUN_1007, TIER2, capsys)
    assert "corroborates 3/9 mandatory roles" in line
    assert parser_1007.completed_agents(FIXTURE_1007, RUN_1007).keys() == SEEN_1007


def test_1007_missed_completions_are_exactly_the_runid_turns():
    turns = [row for row in rows_1007() if "origin" in row]
    assert len(turns) == 6
    assert all(set(row["origin"]) == {"kind", "producer", "runId"} for row in turns)


def test_1007_corrected_parser_sees_all_nine(capsys):
    assert contract.completed_agents(FIXTURE_1007, RUN_1007).keys() == TIER2
    line = advisory(contract, FIXTURE_1007, RUN_1007, TIER2, capsys)
    assert "corroborates 9/9 mandatory roles" in line


@pytest.mark.parametrize(
    "origin",
    [
        {"kind": "task-notification", "producer": "session-task", "runId": 7},
        {"kind": "task-notification", "producer": "session-task", "runId": None},
        {"kind": "task-notification", "producer": "session-task", "runId": "r", "quoted": "x"},
    ],
)
def test_runid_widening_still_refuses_untrusted_origins(origin):
    record = next(row for row in rows_1007() if "origin" in row)
    assert contract.native_task_notification(record) is not None
    record["origin"] = origin
    assert contract.native_task_notification(record) is None
