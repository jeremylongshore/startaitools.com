"""Metric dictionary and versioned rollup header (startaitools-9a8.2.3, 9a8.13.3).

Offline. The dictionary must define every reported metric completely, keep the
three headline measures, and keep unknown, unavailable, n/a and zero distinct.
The header must stamp versions, show the baseline-reset note once, and keep
native platform numbers in their own units, never summed with site sessions.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
BLOG = REPO / "scripts" / "blog"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, BLOG / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


md = _load("metric_dictionary", "metric_dictionary.py")
hdr = _load("rollup_report_header", "rollup-report-header.py")


@pytest.fixture()
def data():
    return md.load()


def test_every_metric_defines_the_six_required_parts_and_na_rule(data):
    for mid, metric in data["metrics"].items():
        for field in ("numerator", "denominator", "eligibility", "window", "filter_version",
                      "unit", "n_a"):
            assert str(metric.get(field, "")).strip(), f"{mid}.{field}"


def test_headline_measures_are_the_plan_of_record(data):
    h = data["headline"]
    primary = data["metrics"][h["pilot_primary"]]
    secondary = data["metrics"][h["pilot_secondary"]]
    recovery = data["metrics"][h["recovery"]]
    assert "28 days" in primary["window"] and primary["unit"] == "session"
    assert "search engine" in primary["numerator"]
    assert "outbound_click" in secondary["numerator"]
    assert "per 100" in secondary["unit"]
    assert "not a visit, install" in secondary["never"]
    assert "oldest" in recovery["denominator"]


def test_sessions_are_not_people_and_states_stay_distinct(data):
    assert "NOT a person" in data["units"]["session"]
    states = data["value_states"]
    for state in ("unavailable", "unknown", "n/a"):
        assert "0" in states[state] and "never" in states[state].lower()
    native = data["metrics"]["devto_native_page_views"]
    assert "site sessions" in native["never"]


def test_dictionary_carries_definitions_only_no_measured_values(data):
    text = json.dumps(data)
    # Baseline distributions live in the private store; none of their keys leak here.
    for key in ("share_zero", "\"median\"", "p75", "website_id"):
        assert key not in text


def test_validation_refuses_an_incomplete_metric(data):
    broken = copy.deepcopy(data)
    del broken["metrics"]["weekly_change"]["denominator"]
    with pytest.raises(md.DictionaryError, match="weekly_change.denominator"):
        md.validate(broken)
    broken = copy.deepcopy(data)
    broken["headline"]["pilot_primary"] = "nonexistent"
    with pytest.raises(md.DictionaryError, match="pilot_primary"):
        md.validate(broken)


def test_cli_check_and_stamp(capsys):
    assert md.main(["check"]) == 0
    assert "OK metric dictionary v" in capsys.readouterr().out
    assert md.main(["stamp"]) == 0
    assert "filter 2026-10-03.v2" in capsys.readouterr().out


def _write_native(path: Path, lines: list[dict]) -> Path:
    path.write_text("".join(json.dumps(x) + "\n" for x in lines))
    return path


def _ok(aid, views, at, reactions=1, comments=0):
    return {"surface": "devto", "status": "ok", "article_id": aid, "page_views": views,
            "reactions": reactions, "comments": comments, "observed_at": at,
            "source": "devto_api"}


def test_native_panel_measures_delta_only_across_seven_days(tmp_path):
    log = _write_native(tmp_path / "n.jsonl", [
        _ok(1, 10, "2026-09-27T12:15:00Z"), _ok(2, 5, "2026-09-27T12:15:00Z"),
        _ok(1, 30, "2026-10-04T12:15:00Z"), _ok(2, 6, "2026-10-04T12:15:00Z"),
        _ok(3, 99, "2026-10-04T12:15:00Z"),
        {"surface": "x", "status": "unavailable_without_dashboard", "note": "in-account only",
         "observed_at": "2026-10-04T12:15:00Z", "source": "registry"},
        _ok(1, 500, "2026-10-05T12:15:00Z"),  # on/after the report day: excluded
    ])
    panel = hdr.native_panel(log, date(2026, 10, 5))
    assert panel["status"] == "measured"
    assert panel["page_views"] == 135 and panel["articles"] == 3 and panel["age_days"] == 1
    assert panel["delta"] == {"status": "measured", "since": "2026-09-27T12:15:00Z",
                              "page_views": 21, "articles": 2}
    assert panel["others"][0]["surface"] == "x"


def test_native_panel_gaps_are_named_never_zero(tmp_path):
    missing = hdr.native_panel(tmp_path / "missing.jsonl", date(2026, 10, 5))
    assert missing["status"] == "unavailable"
    log = _write_native(tmp_path / "n.jsonl", [
        _ok(1, None, "2026-10-04T12:15:00Z"),
        {"surface": "devto", "status": "auth_failed", "observed_at": "2026-10-04T13:00:00Z",
         "source": "devto_api"},
    ])
    panel = hdr.native_panel(log, date(2026, 10, 5))
    assert panel["page_views"] is None  # unknown, not 0
    assert panel["delta"]["status"] == "n/a"
    assert panel["newer_failures"][0]["status"] == "auth_failed"
    html = hdr.render_native(panel, date(2026, 10, 5))
    assert "unknown page views" in html and "failed (auth_failed)" in html


def test_header_stamps_versions_flags_unavailable_and_shows_reset_once(tmp_path, data):
    metrics = {
        "timezone": "Etc/GMT+6",
        "automation_rule": {"version": "2026-10-03.v2"},
        "windows": {"week": {"start": "2026-09-28T00:00:00-06:00",
                             "end_exclusive": "2026-10-05T00:00:00-06:00"}},
        "sites": [
            {"domain": "a.example.com", "filtered": {"week": {"visitors": 1},
                                                     "prior_week": {"unavailable": "HTTPError"}}},
            {"domain": "startaitools.com", "filtered": {"week": {}, "prior_week": {}},
             "referrals": {"week": [{"surface": "x", "tagged": "untagged — unmeasurable"}]}},
        ],
    }
    marker = tmp_path / "reset"
    assert hdr.reset_pending(marker, data["version"]) is True
    html = hdr.render(metrics, data, date(2026, 10, 5), {"status": "unavailable",
                                                         "reason": "none"}, True)
    assert f"metric dictionary v{data['version']}" in html
    assert f"v{hdr.REPORT_VERSION}" in html and "traffic filter 2026-10-03.v2" in html
    assert "[2026-09-28, 2026-10-05)" in html
    assert "Filtered tier unavailable for: a.example.com" in html
    assert "untagged (unmeasurable): 1" in html
    assert "Baseline reset" in html and "never summed with site sessions" in html
    assert "Filter mismatch" not in html
    assert hdr.main(["mark-reset", "--reset-marker", str(marker)]) == 0
    assert hdr.reset_pending(marker, data["version"]) is False
    metrics["automation_rule"]["version"] = "2026-09-01.v1"
    again = hdr.render(metrics, data, date(2026, 10, 5), {"status": "unavailable"}, False)
    assert "Baseline reset" not in again and "Filter mismatch" in again


def test_render_cli_writes_header(tmp_path, capsys):
    metrics = tmp_path / "m.json"
    metrics.write_text(json.dumps({"sites": []}))
    out = tmp_path / "h.html"
    rc = hdr.main(["render", "--metrics", str(metrics), "--date", "2026-10-05", "--out", str(out),
                   "--native", str(tmp_path / "absent.jsonl")])
    assert rc == 0
    assert "Report version" in out.read_text()
    assert "native panel unavailable" in capsys.readouterr().out
