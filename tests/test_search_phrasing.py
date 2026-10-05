"""E03 search phrasing: the staged output and its consumer (startaitools.com#123).

The research step is optional and never gates. These tests pin the consumer:
evidence keeps its source URL and uncertainty, the subject cannot change, and a
timeout, a missing field, no usable result or no file at all each become a
recorded skip while the CLI exits 0 so the writer proceeds. Offline.

Run:  pytest tests/test_search_phrasing.py -q
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts" / "blog"))

from blogpipe import phrasing  # noqa: E402

FIX = REPO / "tests" / "fixtures" / "search_phrasing"
FINDING = json.loads((FIX / "finding.json").read_text(encoding="utf-8"))


def _doc(name: str) -> dict:
    return json.loads((FIX / f"{name}.json").read_text(encoding="utf-8"))


def test_valid_output_keeps_only_sourced_on_topic_candidates():
    rec = phrasing.consume(FIX / "valid.json", FINDING, None)
    assert rec["ran"] is True
    assert rec["skipped_reason"] is None
    # 5 staged: one names no finding term, one has a year, one has no URL.
    assert (rec["candidates"], rec["dropped"]) == (2, 3)
    assert rec["evidence_urls"] == [
        "https://code.claude.com/docs/en/hooks",
        "https://github.com/anthropics/claude-code/issues",
    ]
    assert "inferred from what ranks" in rec["uncertainty"]
    assert rec["recommended_title_form"].startswith("Making a Claude Code SessionEnd Hook")
    assert rec["web_calls"] == 4
    assert rec["used"] is False


def test_used_is_true_only_when_the_shipped_title_is_the_recommendation():
    title = _doc("valid")["recommended_title_form"]
    assert phrasing.consume(FIX / "valid.json", FINDING, title.upper())["used"] is True
    assert phrasing.consume(FIX / "valid.json", FINDING, "Something else")["used"] is False


def test_timeout_fixture_is_a_recorded_skip():
    rec = phrasing.consume(FIX / "timeout.json", FINDING)
    assert (rec["ran"], rec["skipped_reason"]) == (False, "timeout")
    assert rec["candidates"] == 0 and rec["recommended_title_form"] is None


def test_missing_field_fixture_is_refused_as_invalid_output():
    rec = phrasing.consume(FIX / "missing-field.json", FINDING)
    assert (rec["ran"], rec["skipped_reason"]) == (False, "invalid_output")
    assert "uncertainty" in rec["detail"]


def test_no_result_fixture_is_a_recorded_skip():
    rec = phrasing.consume(FIX / "no-result.json", FINDING)
    assert (rec["ran"], rec["skipped_reason"]) == (False, "no_result")
    assert rec["detail"] == "0 of 2 candidates survived validation"


def test_absent_file_reports_missing_when_on_and_disabled_when_off(tmp_path):
    absent = tmp_path / "2026-07-12.r1.search-phrasing.json"
    assert phrasing.consume(absent, FINDING, on=True)["skipped_reason"] == "missing_output"
    assert phrasing.consume(absent, FINDING, on=False)["skipped_reason"] == "disabled"


def test_unparseable_file_is_invalid_output(tmp_path):
    bad = tmp_path / "x.json"
    bad.write_text("{not json", encoding="utf-8")
    assert phrasing.consume(bad, FINDING)["skipped_reason"] == "invalid_output"


# --- topic immutability -------------------------------------------------------


def test_extra_topic_keys_are_topic_drift():
    rec = phrasing.consume(FIX / "topic-drift.json", FINDING)
    assert (rec["ran"], rec["skipped_reason"]) == (False, "topic_drift")
    assert "slug" in rec["detail"] and "topic" in rec["detail"]


def test_a_different_finding_sentence_is_topic_drift():
    doc = _doc("valid")
    doc["finding_sentence"] = "Ten hook frameworks compared."
    assert phrasing.evaluate(doc, FINDING)["skipped_reason"] == "topic_drift"


def test_a_named_term_absent_from_the_finding_is_topic_drift():
    doc = _doc("valid")
    doc["named_terms"] = ["SessionEnd hook", "LangChain callbacks"]
    rec = phrasing.evaluate(doc, FINDING)
    assert rec["skipped_reason"] == "topic_drift"
    assert "LangChain callbacks" in rec["detail"]


def test_the_consumer_never_mutates_the_staged_document_or_finding():
    doc, finding = _doc("valid"), json.loads(json.dumps(FINDING))
    before = (json.dumps(doc, sort_keys=True), json.dumps(finding, sort_keys=True))
    phrasing.evaluate(doc, finding, "x")
    assert (json.dumps(doc, sort_keys=True), json.dumps(finding, sort_keys=True)) == before


def test_off_topic_recommendation_is_dropped_but_evidence_kept():
    doc = _doc("valid")
    doc["recommended_title_form"] = "Ten Ways to Ship Faster"
    rec = phrasing.evaluate(doc, FINDING)
    assert rec["ran"] is True and rec["recommended_title_form"] is None
    assert rec["candidates"] == 2


@pytest.mark.parametrize(
    "mutate, reason",
    [
        (lambda d: d.update(web_calls=7), "invalid_output"),
        (lambda d: d.update(schema="v0"), "invalid_output"),
        (lambda d: d.update(named_terms=[]), "no_named_term"),
        (lambda d: d.update(skipped_reason="because"), "invalid_output"),
        (lambda d: d.update(skipped_reason="no_web"), "no_web"),
    ],
)
def test_contract_violations_become_named_skips(mutate, reason):
    doc = _doc("valid")
    mutate(doc)
    assert phrasing.evaluate(doc, FINDING)["skipped_reason"] == reason


def test_no_recorded_finding_means_no_phrasing():
    assert phrasing.evaluate(_doc("valid"), None)["skipped_reason"] == "no_finding"
    assert phrasing.evaluate(_doc("valid"), {"sentence": " "})["skipped_reason"] == "no_finding"


# --- the CLI the writer calls: every content outcome exits 0 -----------------


@pytest.mark.parametrize(
    "fixture, ran",
    [("valid", True), ("timeout", False), ("missing-field", False), ("no-result", False),
     ("does-not-exist", False)],
)
def test_cli_exits_zero_and_prints_the_record(fixture, ran):
    env = {**os.environ, "BLOG_SEARCH_PHRASING": "1"}
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "search-phrasing",
         "--staging", str(FIX / f"{fixture}.json"), "--finding", str(FIX / "finding.json")],
        cwd=REPO / "scripts" / "blog", env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, proc.stderr
    rec = json.loads(proc.stdout)
    assert rec["ran"] is ran
    assert ("SEARCH-PHRASING: SKIP:" in proc.stderr) is (not ran)


def test_cli_without_the_flag_and_without_a_file_records_disabled(tmp_path):
    env = {k: v for k, v in os.environ.items() if k != "BLOG_SEARCH_PHRASING"}
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "search-phrasing",
         "--staging", str(tmp_path / "none.json"), "--finding", str(FIX / "finding.json")],
        cwd=REPO / "scripts" / "blog", env=env, capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0
    assert json.loads(proc.stdout)["skipped_reason"] == "disabled"
