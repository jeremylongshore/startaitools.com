"""Observed numeric substitution must fail before report composition or delivery."""
import copy
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/blog"))
import rollup_narrative as narrative


def metrics():
    raw = {"visitors": 321, "pageviews": 654}
    tier = {"visitors": 123, "pageviews": 345,
            "visitors_raw": 321, "pageviews_raw": 654}
    return {"fixed_cohort": {"name": "fixed cohort", "domains": ["startaitools.com"]},
            "sites": [{"domain": "startaitools.com",
                       "periods": {p: raw.copy() for p in ("week", "prior_week")},
                       "filtered": {p: tier.copy() for p in ("week", "prior_week")},
                       "referrals": {"week": [
                           {"surface": "linkedin", "status": "ok", "tagged": True,
                            "tagged_raw": 0, "tagged_filtered": 0,
                            "any_raw": 0, "any_filtered": 0},
                           {"surface": "medium", "status": "ok", "tagged": False,
                            "tagged_raw": 0, "tagged_filtered": 0,
                            "any_raw": 0, "any_filtered": 0},
                           {"surface": "x", "status": "unavailable"},
                       ]}}]}


def draft():
    item = {"text": "Review the traffic rule before changing the distribution plan.",
            "evidence": ["fixed/week/filtered"]}
    return {"interpretation": [copy.deepcopy(item)], "referrals": [copy.deepcopy(item)],
            "evergreen": {"url": "https://startaitools.com/posts/2026-example/",
                          "angle": "Explain the deployment failure and recovery."},
            "actions": [copy.deepcopy(item), copy.deepcopy(item)]}


def test_evidence_labels_own_population_period_tier_unit_and_value():
    data = draft()
    data["interpretation"][0]["evidence"].append("fixed/week/raw")
    html = narrative.render(data, narrative.catalog(metrics()))
    assert "fixed cohort; week; filtered: 123 sessions; 345 pageviews" in html
    assert "fixed cohort; week; raw: 321 sessions; 654 pageviews" in html
    assert "href=\"https://startaitools.com/posts/2026-example/\"" in html


@pytest.mark.parametrize("text", [
    "Fixed cohort (filtered): 321 visitors and 654 pageviews.",
    "We had three thousand filtered sessions.", "Traffic doubled.",
    "Traffic fell １０％.", "Traffic share is ½.", "<script>alert('bad')</script>",
])
def test_unsupported_numeric_or_html_prose_refuses_the_report(text):
    data = draft()
    data["interpretation"][0]["text"] = text
    with pytest.raises(ValueError):
        narrative.render(data, narrative.catalog(metrics()))


def test_unknown_metric_ref_cannot_be_zero_filled_or_ignored():
    data = draft()
    data["actions"][0]["evidence"] = ["made-up/sessions"]
    with pytest.raises(ValueError, match="unknown metric"):
        narrative.render(data, narrative.catalog(metrics()))


def test_unavailable_untagged_and_measured_zero_remain_distinct():
    data = metrics()
    data["sites"][0]["filtered"]["week"] = {"unavailable": "timeout"}
    refs = narrative.catalog(data)
    assert "unavailable" in refs["fixed/week/filtered"]
    assert "0 filtered sessions; 0 raw sessions" in refs[
        "startaitools.com/week/referral/linkedin/tagged"]
    assert "untagged - unmeasurable" in refs["startaitools.com/week/referral/medium/any"]
    assert "unavailable" in refs["startaitools.com/week/referral/x/any"]


def test_mismatched_populations_refuse_before_narration():
    data = metrics()
    data["sites"][0]["filtered"]["week"]["visitors_raw"] = 333
    with pytest.raises(ValueError, match="populations disagree"):
        narrative.catalog(data)


@pytest.mark.parametrize("url", [
    "javascript:alert(1)", "https://startaitools.com.evil.test/posts/a/",
    "https://startaitools.com@evil.test/posts/a/", "https://startaitools.com/posts/",
    "https://startaitools.com/posts/a/?tracking=123",
])
def test_untrusted_nomination_urls_are_rejected(url):
    data = draft()
    data["evergreen"]["url"] = url
    with pytest.raises(ValueError):
        narrative.render(data, narrative.catalog(metrics()))


def test_missing_cohort_member_is_not_a_smaller_portfolio():
    data = metrics()
    data["fixed_cohort"]["domains"].append("missing.example.com")
    with pytest.raises(ValueError):
        narrative.catalog(data)


def test_empty_cohort_and_invalid_filtered_total_refuse():
    data = metrics()
    data["fixed_cohort"]["domains"] = []
    with pytest.raises(ValueError):
        narrative.catalog(data)
    data = metrics()
    data["sites"][0]["filtered"]["week"]["visitors"] = 9999
    with pytest.raises(ValueError):
        narrative.catalog(data)
