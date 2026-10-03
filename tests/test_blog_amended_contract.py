"""E01-T02/T03 (startaitools.com#121): the reader brief, the outsider record, Tier 1
consistency, and a disclaimer footer that states only the checks that ran.

Rollout is OBSERVATION MODE first (E01-T05): before AMENDED_CONTRACT_ENFORCE_FROM a gap
is an ADVISORY line, after it the same gap refuses. The switch is keyed on the run's
target date, so these tests move the constant instead of waiting for a calendar day.
"""

import json
import re
import subprocess
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


@pytest.fixture(autouse=True)
def no_override(monkeypatch):
    """The operator lever must not leak in from the environment running the tests."""
    monkeypatch.delenv("BLOG_BRIEF_ENFORCE_FROM", raising=False)


def brief():
    return sys.modules["blogpipe.brief"]


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


# ---- review fixes: soft pre-switch receipts, the env lever, readiness ---------------


@pytest.mark.parametrize("fault", ["stale-hash", "foreign-run", "no-receipt"])
def test_pre_switch_tier_one_receipt_mismatch_is_advisory_not_a_refusal(
    produced, fault, capsys  # noqa: F811
):
    repo, post, _, transcript = produced
    if fault == "no-receipt":
        output = "Consistency report without a structured receipt."
    else:
        receipt = json.loads(gate_receipt(post, "PASS").split("\n", 1)[1])
        key, value = ("post_sha256", "0" * 64) if fault == "stale-hash" else ("run_id", "x")
        receipt["blog_gate_receipt"][key] = value
        output = json.dumps(receipt)
    restage(repo, post, {CHECKER: output})
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    assert f"{CHECKER} receipt not counted" in advisory(capsys.readouterr().err)
    assert "consistency" not in contract.performed_checks(repo, identity(post), post, 1)


@pytest.mark.parametrize("fault", ["stale-hash", "no-receipt"])
def test_post_switch_tier_one_receipt_mismatch_refuses(produced, enforce, fault):  # noqa: F811
    repo, post, sentinel, transcript = produced
    pass_consistency(repo, post, sentinel)
    rewrite_audit(repo, lambda a: a.update(json.loads(json.dumps(COMPLETE_BRIEF))))
    if fault == "no-receipt":
        output = "Consistency report without a structured receipt."
    else:
        output = gate_receipt(post, "PASS").replace(contract.digest(post), "0" * 64)
    restage(repo, post, {CHECKER: output})
    with pytest.raises(contract.ContractError, match=CHECKER):
        contract.validate(repo, DATE, RUN, transcript)


def test_a_stale_revise_before_the_switch_is_not_counted_but_does_not_refuse(
    produced, capsys  # noqa: F811
):
    """A REVISE bound to EARLIER bytes is a stale receipt; a REVISE on these bytes refuses."""
    repo, post, _, transcript = produced
    stale = gate_receipt(post, "REVISE").replace(contract.digest(post), "0" * 64)
    restage(repo, post, {CHECKER: stale})
    contract.validate(repo, DATE, RUN, transcript)
    assert "receipt not counted" in advisory(capsys.readouterr().err)


def test_the_real_switch_constant_boundary():
    assert brief().AMENDED_CONTRACT_ENFORCE_FROM == "2026-10-14"
    assert brief().enforced("2026-10-13") is False
    assert brief().enforced("2026-10-14") is True


def test_env_lever_moves_or_disables_the_switch(monkeypatch):
    monkeypatch.setenv("BLOG_BRIEF_ENFORCE_FROM", "off")
    assert brief().enforced("2099-01-01") is False
    monkeypatch.setenv("BLOG_BRIEF_ENFORCE_FROM", "2026-10-20")
    assert brief().enforced("2026-10-14") is False
    assert brief().enforced("2026-10-20") is True
    for bad in ("tomorrow", "20261020", "2026-13-01"):
        monkeypatch.setenv("BLOG_BRIEF_ENFORCE_FROM", bad)
        with pytest.raises(contract.ContractError, match="BLOG_BRIEF_ENFORCE_FROM"):
            brief().enforced("2026-10-14")


def test_env_off_keeps_observation_mode_past_the_switch(produced, monkeypatch, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    monkeypatch.setattr(brief(), "AMENDED_CONTRACT_ENFORCE_FROM", DATE)
    monkeypatch.setenv("BLOG_BRIEF_ENFORCE_FROM", "off")
    contract.validate(repo, DATE, RUN, transcript)
    assert "enforcement off via BLOG_BRIEF_ENFORCE_FROM" in advisory(capsys.readouterr().err)


def write_runs(directory, statuses):
    """statuses: {date: True (complete) | False (incomplete) | None (no line)}."""
    for day, status in statuses.items():
        line = {True: "complete", False: "missing agent_audit.finding"}.get(status)
        text = "unrelated log line\n"
        if line is not None:
            text += f"[t] PRODUCER-CONTRACT: ADVISORY: amended contract (observation): {line}\n"
        (directory / f"run-{day}.log").write_text(text)


def days(start, count):
    import datetime as dt

    first = dt.date.fromisoformat(start)
    return [(first + dt.timedelta(days=i)).isoformat() for i in range(count)]


def test_readiness_is_silent_until_three_days_before_the_switch(tmp_path):
    write_runs(tmp_path, dict.fromkeys(days("2026-10-01", 10), True))
    assert brief().readiness(tmp_path, "2026-10-10") == (None, False)
    message, urgent = brief().readiness(tmp_path, "2026-10-11")
    assert message.startswith("brief enforcement in 3 day(s)") and not urgent
    assert "consecutive complete 7/7" in message


def test_readiness_counts_down_with_incomplete_runs(tmp_path):
    statuses = dict.fromkeys(days("2026-10-06", 7), True)
    statuses["2026-10-11"] = False
    statuses["2026-10-12"] = None
    write_runs(tmp_path, statuses)
    message, urgent = brief().readiness(tmp_path, "2026-10-12")
    assert "in 2 day(s)" in message and "consecutive complete 0/7" in message
    assert "5 complete, 2 incomplete" in message and not urgent


def test_readiness_raises_urgent_at_the_switch_without_seven_complete_runs(tmp_path):
    write_runs(tmp_path, {**dict.fromkeys(days("2026-10-08", 7), True), "2026-10-13": False})
    message, urgent = brief().readiness(tmp_path, "2026-10-14")
    assert urgent and message.startswith("URGENT: brief enforcement active since 2026-10-14")
    assert "BLOG_BRIEF_ENFORCE_FROM" in message


def test_readiness_is_quiet_at_the_switch_after_seven_complete_runs(tmp_path):
    write_runs(tmp_path, dict.fromkeys(days("2026-10-08", 7), True))
    message, urgent = brief().readiness(tmp_path, "2026-10-14")
    assert not urgent and message.startswith("brief enforcement active since 2026-10-14")


def test_readiness_cli_exit_codes(tmp_path, monkeypatch):
    write_runs(tmp_path, {"2026-10-14": False})

    def cli(env):
        return subprocess.run(
            [sys.executable, "-B", "-m", "blogpipe", "brief-readiness", "--log-dir",
             str(tmp_path), "--date", "2026-10-14"],
            cwd=ROOT / "scripts/blog", capture_output=True, text=True, env=env,
        )

    import os

    base = {k: v for k, v in os.environ.items() if k != "BLOG_BRIEF_ENFORCE_FROM"}
    urgent = cli(base)
    assert urgent.returncode == 2 and urgent.stdout.startswith("URGENT:")
    off = cli({**base, "BLOG_BRIEF_ENFORCE_FROM": "off"})
    assert off.returncode == 0 and "enforcement off" in off.stdout
    bad = cli({**base, "BLOG_BRIEF_ENFORCE_FROM": "soon"})
    assert bad.returncode == 2 and "readiness check failed" in bad.stdout


@needs_tools
def test_footer_wording_comes_from_the_approved_library_entry(tmp_path):
    library = {"default_footer": "f", "footer_suffix": "Suffix.", "entities": {},
               "checks_footer": {"lead": "Approved lead:", "unrecorded": "Approved none."}}
    recorded = payload(tmp_path, tier=1, disclaimers=library, checks=["hugo"])["footer"]
    assert recorded == "Approved lead: Hugo build. Suffix."
    assert payload(tmp_path, tier=1, disclaimers=library)["footer"] == "Approved none. Suffix."
