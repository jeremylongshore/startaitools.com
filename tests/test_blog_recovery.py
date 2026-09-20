"""Failure router: one failed producer attempt becomes exactly one action."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts/blog"))
from blogpipe import recovery  # noqa: E402

# Verbatim from the 2026-09-15..18 incident logs.
REAL_429 = (
    '[claude-code:unrecognized_model] {"model":"MiniMax-M3","query_source":"sdk"}\n'
    "API Error: Request rejected (429) · Token Plan usage limit reached: Upgrade your "
    "Token Plan or purchase Credits for more usage. (2056)"
)
REAL_PENDING = (
    "PRODUCER-CONTRACT: FAILED: PENDING WORK: mandatory Agent completion missing: "
    "blog-classifier, content-marketer, seo-meta-optimizer"
)
REAL_NO_RECEIPT = "PRODUCER-CONTRACT: FAILED: roles: staging record missing"
REAL_WRITE_SET = '{"ok": false, "error": "run decisions must be complete appended JSONL records"}'
REAL_GROK_402 = "grok: HTTP 402 Payment Required"


@pytest.mark.parametrize("evidence", [REAL_PENDING, REAL_NO_RECEIPT, REAL_WRITE_SET])
def test_a_finished_run_the_contract_refused_is_repaired_with_its_own_message(evidence):
    decision = recovery.classify(0, evidence)
    assert (decision.action, decision.source) == ("repair", "deterministic")


def test_the_repair_reason_is_the_contracts_last_line_not_an_earlier_one():
    log = f"{REAL_PENDING}\nretrying\n{REAL_NO_RECEIPT}\n"
    assert recovery.classify(0, log).detail == REAL_NO_RECEIPT


@pytest.mark.parametrize("evidence", [REAL_429, REAL_GROK_402, "529 Overloaded", "invalid api key"])
def test_a_dead_provider_fails_over_instead_of_repairing(evidence):
    decision = recovery.classify(1, evidence)
    assert (decision.action, decision.source) == ("failover", "deterministic")


def test_a_recovered_429_in_the_log_does_not_override_the_contracts_complaint():
    """Exit 0 means the producer reached the contract; stray provider noise is history."""
    decision = recovery.classify(0, f"{REAL_429}\n...recovered...\n{REAL_NO_RECEIPT}")
    assert decision.action == "repair" and decision.detail == REAL_NO_RECEIPT


def test_a_timeout_gets_one_more_go_at_the_same_work():
    assert recovery.classify(124, "still writing").action == "repair"


@pytest.mark.parametrize(
    "evidence",
    [
        "FATAL: producer changed Git HEAD; producer/lander boundary was violated.",
        "PRODUCER-CONTRACT: FAILED: historical decisions changed; append-only contract violated",
        "decisions history was rewritten or lacks an append boundary",
        "blogpipe resolved from /x, not beside /y: mixed checkouts",
    ],
)
def test_integrity_damage_stops_even_when_it_looks_like_a_contract_message(evidence):
    for exit_code in (0, 1):
        assert recovery.classify(exit_code, evidence).action == "stop"


def test_an_unrecognised_failure_defaults_to_the_other_provider_without_a_model():
    decision = recovery.classify(1, "Segmentation fault (core dumped)")
    assert (decision.action, decision.source) == ("failover", "default")


def test_a_model_is_asked_only_for_unrecognised_failures(monkeypatch):
    asked = []
    monkeypatch.setattr(recovery, "ask_cheap_model", lambda text: asked.append(text) or "repair")
    assert recovery.classify(1, REAL_429, ask_model=True).source == "deterministic"
    assert asked == []
    decision = recovery.classify(1, "Segmentation fault", ask_model=True)
    assert (decision.action, decision.source) == ("repair", "model") and len(asked) == 1


@pytest.mark.parametrize(
    "reply,expected",
    [("repair", "repair"), ("Failover.", "failover"), ("  STOP\n", "stop")]
    + [("I think repair, or maybe failover", None), ("restart the server", None), ("", None)],
)
def test_a_model_answer_counts_only_if_it_names_exactly_one_fixed_action(reply, expected):
    assert recovery._one_word(reply) == expected


def test_a_model_that_errors_or_waffles_changes_nothing(monkeypatch):
    def broken(*_args, **_kwargs):
        raise OSError("no such binary")

    monkeypatch.setattr(recovery.subprocess, "run", broken)
    assert recovery.ask_cheap_model("anything") is None
    assert recovery.classify(1, "Segmentation fault", ask_model=True).source == "default"


def test_the_repair_prompt_names_the_gap_and_restates_every_hard_limit():
    text = recovery.repair_prompt("2026-09-17", REAL_NO_RECEIPT, 1, 2)
    assert text.startswith("/blog-backfill 2026-09-17 2026-09-17")
    assert REAL_NO_RECEIPT in text and "REPAIR ROUND 1 of 2" in text
    for limit in (
        "may NOT edit anything under scripts/",
        "may not touch\ngit",
        "never write a role",
    ):
        assert limit.replace("\n", " ") in text.replace("\n", " ")
    assert "may not mark a failing verdict as passing" in text.replace("\n", " ")


def test_an_empty_reason_still_tells_the_producer_how_to_find_it():
    assert recovery.NO_MESSAGE in recovery.repair_prompt("2026-09-17", "", 2, 2)


def test_the_command_line_is_what_the_bash_wrapper_calls(tmp_path):
    evidence = tmp_path / "tail.txt"
    evidence.write_text(REAL_429)
    script = ROOT / "scripts/blog/blog-recovery.py"
    done = subprocess.run(
        [sys.executable, str(script), "classify", "--exit-code", "1"]
        + ["--evidence-file", str(evidence)],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(done.stdout)["action"] == "failover"
    missing = subprocess.run(
        [sys.executable, str(script), "classify", "--exit-code", "1"]
        + ["--evidence-file", str(tmp_path / "absent.txt")],
        capture_output=True,
        text=True,
    )
    assert json.loads(missing.stdout)["action"] == "failover", "unreadable evidence must not crash"
