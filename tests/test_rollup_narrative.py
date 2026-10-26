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


def site(domain, week, prior):
    raw = {"visitors": 999, "pageviews": 999}
    return {"domain": domain,
            "periods": {"week": raw.copy(), "prior_week": raw.copy()},
            "filtered": {p: {"visitors": v, "pageviews": v, "visitors_raw": 999,
                             "pageviews_raw": 999}
                         for p, v in (("week", week), ("prior_week", prior))},
            "top_pages": [{"x": "/", "y": 9}, {"x": "/posts/a/", "y": 3}],
            "top_referrers": [{"x": "google.com", "y": 4}]}


def cohort_metrics():
    return {"fixed_cohort": {"name": "fixed cohort", "domains": ["big.example", "mid.example"]},
            "sites": [site("big.example", 800, 1000), site("mid.example", 120, 100),
                      site("tiny.example", 9, 3)]}


def test_summary_headline_is_computed_from_filtered_cohort():
    html = narrative.summary(cohort_metrics())
    assert "920 sessions" in html and "down 16.4% from 1,100" in html
    assert "big.example carried 87% of them." in html
    assert "Biggest rise: mid.example, up 20.0% (100 to 120)." in html
    assert "Biggest fall: big.example, down 20.0% (1,000 to 800)." in html
    assert "/posts/a/" in html


def test_tiny_sites_are_never_movers_or_table_rows():
    # tiny.example tripled, but nine sessions is below both floors.
    html = narrative.summary(cohort_metrics())
    assert "tiny.example" not in html


def test_unavailable_cohort_is_not_a_zero_headline():
    data = cohort_metrics()
    data["sites"][0]["filtered"]["week"] = {"unavailable": "timeout"}
    html = narrative.summary(data)
    assert "unavailable this week (not zero)" in html
    assert "sessions across" not in html


def test_story_order_puts_summary_and_asks_before_interpretation():
    data = metrics()
    html = narrative.render(draft(), narrative.catalog(data), data)
    assert (html.index("The week in one look") < html.index("This week's asks")
            < html.index("What it means"))


def with_tripwire(data):
    data["automation_rule"] = {"tripwire": {"max_removed_share": 0.85, "min_sessions": 50,
                                            "max_wow_jump_points": 20}}
    return data


def test_rule_check_site_is_left_out_of_headline_and_movers():
    # 2026-10-26: a one-day bot burst passed the filter and read as +364%.
    data = with_tripwire(cohort_metrics())
    big = data["sites"][0]["filtered"]
    big["week"].update(visitors=4000, visitors_raw=6000)    # 33% removed
    big["prior_week"].update(visitors=900, visitors_raw=3600)  # 75% removed
    mid = data["sites"][1]["filtered"]
    mid["week"].update(visitors_raw=150)
    mid["prior_week"].update(visitors_raw=130)
    html = narrative.summary(data)
    assert "Rule check needed for big.example</b>" in html
    assert "120 sessions</b> across the other site in the fixed cohort" in html
    assert "Biggest rise: big.example" not in html
    assert "(rule check needed)" in html


def test_every_member_flagged_prints_no_total():
    data = with_tripwire(cohort_metrics())
    for row in data["sites"][:2]:
        row["filtered"]["week"].update(visitors=900, visitors_raw=1000)
        row["filtered"]["prior_week"].update(visitors=100, visitors_raw=1000)
    html = narrative.summary(data)
    assert "Rule check needed for big.example, mid.example" in html
    assert "sessions</b> across" not in html


def test_no_tripwire_config_keeps_plain_headline():
    assert "Rule check needed" not in narrative.summary(cohort_metrics())


@pytest.mark.parametrize("status", [404, 410])
def test_nominated_post_that_does_not_exist_refuses(status):
    # 2026-10-12: the rollup nominated a slug that returned 404.
    with pytest.raises(ValueError, match="does not resolve"):
        narrative.render(draft(), narrative.catalog(metrics()), url_status=lambda url: status)


@pytest.mark.parametrize("status", [200, 301, None, 503])
def test_live_or_unreachable_nomination_is_accepted(status):
    html = narrative.render(draft(), narrative.catalog(metrics()), url_status=lambda url: status)
    assert "/posts/2026-example/" in html
