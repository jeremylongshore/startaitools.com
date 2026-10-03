"""E01-T02/T03 (startaitools.com#121): the reader brief, the outsider record, Tier 1
consistency, and a disclaimer footer that states only the checks that ran.

Rollout is OBSERVATION MODE first (E01-T05): before AMENDED_CONTRACT_ENFORCE_FROM a gap
is an ADVISORY line, after it the same gap refuses. The switch is keyed on the run's
target date, so these tests move the constant instead of waiting for a calendar day.
"""

import json
import re
import sys
from pathlib import Path

import pytest
from blog_roles import stage_roles
from test_blog_producer_contract import DATE, RUN, contract, produced  # noqa: F401
from test_packet_campaign_tags import PACKET, needs_tools, payload, render

ROOT = Path(__file__).resolve().parents[1]
BASE = {"blog-classifier", "content-marketer", "seo-meta-optimizer"}
CHECKER = "blog-consistency-checker"

COMPLETE_BRIEF = {
    "finding": {
        "sentence": "A monitor that checks reachability cannot tell you the data is fresh.",
        "reader": "An engineer who runs scheduled jobs behind a health check.",
        "problem": "The health check stays green while the job silently stops updating data.",
        "outcome": "Add a freshness probe that fails when the newest record is too old.",
        "source_evidence": ["merged pull request with the probe", "job log of the stale run"],
        "destination": "https://github.com/example/repo",
    },
    "outsider_test": {"verdict": "REVISE", "rounds": 2, "unknown_terms": ["receipt"]},
}

# 2026-10-01 published post, reduced to the sentences that contradict each other.
INCONSISTENT_POST = (
    "+++\ntitle = \"Offline fixture\"\nslug = \"fixture-post\"\ndraft = false\n"
    'date = "2026-09-15"\n+++\n'
    "We built a ten-scenario drill to prove the restore path.\n\n"
    "All six cases passed on the first run.\n\n"
    "Case seven is the one that matters: the restore from a cold host.\n"
)
INCONSISTENT_VERDICT = (
    "Internal count contradiction: the opening promises a ten-scenario drill, the "
    "results report six cases, and the next paragraph discusses case seven. A reader "
    "cannot tell how many scenarios ran.\n"
)


@pytest.fixture
def enforce(monkeypatch):
    """Move the dated switch so the fixture's run date is on/after it."""
    monkeypatch.setattr(sys.modules["blogpipe.brief"], "AMENDED_CONTRACT_ENFORCE_FROM", DATE)


def gate_receipt(post, verdict, agent=CHECKER, note="No contradictions found.\n"):
    receipt = {
        "agent": agent,
        "date": DATE,
        "slug": post.stem,
        "run_id": RUN,
        "post_sha256": contract.digest(post),
        "verdict": verdict,
    }
    return note + json.dumps({"blog_gate_receipt": receipt})


def restage(repo, post, extra=None):
    outputs = dict.fromkeys(BASE, "offline fixture result")
    outputs.update(extra or {})
    stage_roles(repo, date=DATE, run_id=RUN, slug=post.stem, post=post, outputs=outputs)


def rewrite_audit(repo, change):
    """Edit the appended (uncommitted) audit row in place, as the failure tests do."""
    path = repo / contract.DECISIONS
    rows = contract.records(path)
    change(rows[-1]["agent_audit"])
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def pass_consistency(repo, post, sentinel):
    restage(repo, post, {CHECKER: gate_receipt(post, "PASS")})
    value = json.loads(sentinel.read_text())
    value["gates"]["consistency"] = "pass"
    sentinel.write_text(json.dumps(value))


def advisory(stderr):
    lines = [line for line in stderr.splitlines() if "ADVISORY: amended contract" in line]
    assert lines, stderr
    return lines[-1]


# ---- E01-T02: the brief and the outsider record ------------------------------------


def test_observation_mode_reports_every_gap_and_still_passes(produced, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    line = advisory(capsys.readouterr().err)
    assert "observation until " in line
    for gap in ("agent_audit.finding", "agent_audit.outsider_test", CHECKER):
        assert gap in line


MISSING = {
    "finding": lambda a: a.pop("finding"),
    "sentence": lambda a: a["finding"].pop("sentence"),
    "reader": lambda a: a["finding"].update(reader="  "),
    "problem": lambda a: a["finding"].pop("problem"),
    "outcome": lambda a: a["finding"].update(outcome=None),
    "source_evidence": lambda a: a["finding"].update(source_evidence=[]),
    "destination": lambda a: a["finding"].pop("destination"),
    "destination_reason": lambda a: a["finding"].update(destination=None),
    "outsider_test": lambda a: a.pop("outsider_test"),
    "outsider_shape": lambda a: a["outsider_test"].update(verdict="PASS-ish"),
}


def brief_audit(audit, field):
    audit.update(json.loads(json.dumps(COMPLETE_BRIEF)))
    MISSING[field](audit)


@pytest.mark.parametrize("field", sorted(MISSING))
def test_missing_brief_field_is_advisory_before_the_switch(produced, field, capsys):  # noqa: F811
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)
    rewrite_audit(repo, lambda a: brief_audit(a, field))
    contract.validate(repo, DATE, RUN, transcript)
    line = advisory(capsys.readouterr().err)
    assert "missing" in line and field.split("_shape")[0] in line


@pytest.mark.parametrize("field", sorted(MISSING))
def test_missing_brief_field_refuses_after_the_switch(produced, enforce, field):  # noqa: F811
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)
    rewrite_audit(repo, lambda a: brief_audit(a, field))
    with pytest.raises(contract.ContractError, match="amended reader contract incomplete"):
        contract.validate(repo, DATE, RUN, transcript)


def test_complete_brief_passes_after_the_switch(produced, enforce, capsys):  # noqa: F811
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)
    rewrite_audit(repo, lambda a: a.update(json.loads(json.dumps(COMPLETE_BRIEF))))
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    assert advisory(capsys.readouterr().err).endswith("(enforced): complete")


def test_a_null_destination_with_a_reason_is_complete(produced, enforce):  # noqa: F811
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)

    def change(audit):
        audit.update(json.loads(json.dumps(COMPLETE_BRIEF)))
        audit["finding"].update(destination=None, destination_reason="internal tool, no repo")

    rewrite_audit(repo, change)
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"


def test_an_honest_outsider_revise_never_blocks(produced, enforce):  # noqa: F811
    """Presence is required; the verdict is not. COMPLETE_BRIEF records a REVISE."""
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)
    rewrite_audit(repo, lambda a: a.update(json.loads(json.dumps(COMPLETE_BRIEF))))
    contract.validate(repo, DATE, RUN, transcript)


# ---- E01-T03: Tier 1 consistency ---------------------------------------------------


def test_tier_one_requires_the_consistency_checker_after_the_switch(produced, enforce):  # noqa: F811
    repo, post, sentinel, transcript = produced
    rewrite_audit(repo, lambda a: a.update(json.loads(json.dumps(COMPLETE_BRIEF))))
    value = json.loads(sentinel.read_text())
    value["gates"]["consistency"] = "pass"
    sentinel.write_text(json.dumps(value))
    assert CHECKER in contract.required_agents(1, post, {"writer": "content-marketer"}, DATE)
    with pytest.raises(contract.ContractError, match=CHECKER):
        contract.validate(repo, DATE, RUN, transcript)


def test_tier_one_consistency_gate_flag_is_required_after_the_switch(produced, enforce):  # noqa: F811
    repo, post, sentinel, transcript = produced
    restage(repo, post, {CHECKER: gate_receipt(post, "PASS")})
    rewrite_audit(repo, lambda a: a.update(json.loads(json.dumps(COMPLETE_BRIEF))))
    with pytest.raises(contract.ContractError, match="required tier/build/voice/code gate"):
        contract.validate(repo, DATE, RUN, transcript)


@pytest.mark.parametrize("switched", [False, True])
def test_the_2026_10_01_count_contradiction_is_rejected(produced, request, switched):  # noqa: F811
    """Regression: 'ten-scenario' drill, 'six cases' passed, then 'case seven'.

    The checker's verdict is simulated (no model call). A staged REVISE refuses the run
    at Tier 1 both before the switch (it ran, so it must pass) and after it.
    """
    if switched:
        request.getfixturevalue("enforce")
    repo, post, sentinel, transcript = produced
    post.write_text(INCONSISTENT_POST)
    value = json.loads(sentinel.read_text())
    value.update(post_sha256=contract.digest(post))
    value["gates"]["consistency"] = "pass"
    sentinel.write_text(json.dumps(value))
    restage(repo, post, {CHECKER: gate_receipt(post, "REVISE", note=INCONSISTENT_VERDICT)})
    with pytest.raises(contract.ContractError, match=CHECKER):
        contract.validate_gate_receipts(
            contract.receipt_roles(repo, {"date": DATE, "slug": post.stem, "run_id": RUN}, post),
            1,
            post,
            {"date": DATE, "slug": post.stem, "run_id": RUN},
        )
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)


# ---- footer: only the checks that actually ran -------------------------------------


def identity(post):
    return {"date": DATE, "slug": post.stem, "run_id": RUN}


def test_performed_checks_read_the_receipts_not_the_tier(produced):  # noqa: F811
    repo, post, sentinel, _ = produced
    assert contract.performed_checks(repo, identity(post), post, 1) == ["hugo", "voice-lint"]
    pass_consistency(repo, post, sentinel)
    checks = contract.performed_checks(repo, identity(post), post, 1)
    assert checks == ["hugo", "voice-lint", "consistency"]
    assert "fact-check" not in checks


def test_footer_vocabulary_matches_the_packet_renderer():
    text = PACKET.read_text()
    block = text[text.index('{"hugo":"Hugo build"') : text.index("as $label")]
    rendered = dict(re.findall(r'"([a-z-]+)":"([^"]+)"', block))
    assert rendered == contract.CHECK_LABELS


@needs_tools
def test_footer_states_only_recorded_checks(tmp_path):
    footer = payload(tmp_path, tier=1, checks=["hugo", "voice-lint", "consistency"])["footer"]
    expected = "Checks run before publish: Hugo build, voice lint, consistency check."
    assert footer.startswith(expected)
    assert "fact" not in footer.lower()
    html = render(payload(tmp_path, tier=1, checks=["hugo", "voice-lint", "consistency"]))
    assert "fact-checked" not in html


@needs_tools
def test_footer_names_fact_checking_only_when_it_ran(tmp_path):
    checks = ["hugo", "voice-lint", "code-review", "consistency", "fact-check"]
    assert "fact check against sources" in payload(tmp_path, tier=3, checks=checks)["footer"]


@pytest.mark.parametrize("checks", [None, [], ["not-a-check"]])
@needs_tools
def test_footer_for_an_unrecorded_post_is_truthful(tmp_path, checks):
    footer = payload(tmp_path, tier=2, checks=checks)["footer"]
    assert footer.startswith("Pre-publish checks were not recorded for this post.")
    assert "fact" not in footer.lower()


def test_renderer_fallback_never_claims_fact_checking():
    text = (ROOT / "scripts/blog/blog-packet-html.cjs").read_text()
    assert "fact-checked" not in text
