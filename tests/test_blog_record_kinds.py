"""E07-T02/T03 (startaitools.com#127): record kinds, shipped tier, and the producer schema.

T02. decisions.jsonl recorded only the classifier's tier; the lander's length-gate
downgrades lived in feedback.jsonl. The September 2026 fixture below is a FROZEN COPY of
the real files (every line byte-identical to the committed source, asserted below):
classifier 20/9/1, shipped 23/6/1, 30 decisions including the 09-12 decision that was
recovered from quarantine with `audit_addendum: true`.

T03. The producer contract checks record_type, the flag enum, cadence_type and
rhetorical_structure on the run's own records, in observation mode until
RECORD_SCHEMA_ENFORCE_FROM (the brief.py dated switch, reused), refusal after.
"""

import importlib
import importlib.util
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from test_blog_producer_contract import DATE, RUN, contract, git, produced  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
METH = ROOT / ".claude/skills/blog-backfill/methodology"
FIXTURE = ROOT / "tests/fixtures/calibration-2026-09"
SEPTEMBER = ("2026-09-01", "2026-10-01")
RECOVERED = "sealing-a-168-bead-planning-graph-took-three-reviews-and-a-seven-seat-council"
DOWNGRADED = {
    "2026-09-08": "hardening-a-marketplace-in-one-day",
    "2026-09-12": RECOVERED,
    "2026-09-24": "pin-the-installer-and-add-a-renewer",
}
VALID_CLASSIFIER = {
    "record_type": "classifier",
    "anti_inflation_flags": ["distribution-pressure"],
    "cadence_type": "daily",
    "rhetorical_structure": "thematic-grouping",
}

# The contract shim above put scripts/blog on sys.path and imported the package.
records = importlib.import_module("blogpipe.records")
ledger = importlib.import_module("blogpipe.ledger")
schema = importlib.import_module("blogpipe.schema")


@pytest.fixture(autouse=True)
def no_override(monkeypatch):
    """Neither operator lever may leak in from the environment running the tests."""
    monkeypatch.delenv("BLOG_RECORD_SCHEMA_ENFORCE_FROM", raising=False)
    monkeypatch.delenv("BLOG_BRIEF_ENFORCE_FROM", raising=False)


def fixture_rows(name):
    return contract.records(FIXTURE / name)


# ---- T02: the frozen September fixture ------------------------------------------------


def test_fixture_is_a_byte_identical_subset_of_the_real_append_only_files():
    for name in ("decisions.jsonl", "feedback.jsonl"):
        live = set((METH / name).read_text().splitlines())
        frozen = (FIXTURE / name).read_text().splitlines()
        assert frozen and all(line in live for line in frozen), name


def test_september_reproduces_classifier_20_9_1_and_shipped_23_6_1():
    rows = records.tier_ledger(
        fixture_rows("decisions.jsonl"), fixture_rows("feedback.jsonl"),
        start=SEPTEMBER[0], end=SEPTEMBER[1],
    )
    assert len(rows) == 30
    assert len({row["date"] for row in rows}) == 30  # one decision per day, edges excluded
    assert records.distribution(rows, "classifier_tier") == (20, 9, 1)
    assert records.distribution(rows, "shipped_tier") == (23, 6, 1)
    downgraded = {r["date"]: r["slug"] for r in rows if r["shipped_tier"] != r["classifier_tier"]}
    assert downgraded == DOWNGRADED
    (recovered,) = [row for row in rows if row["recovered"]]
    assert (recovered["date"], recovered["classifier_tier"]) == ("2026-09-12", 2)


def test_the_old_audit_addendum_filter_loses_the_recovered_day():
    """The regression the record kind fixes: 29 decisions, not 30."""
    old = [
        r for r in fixture_rows("decisions.jsonl")
        if "tier" in r and not r.get("audit_addendum") and r["date"].startswith("2026-09")
    ]
    assert len(old) == 29 and RECOVERED not in {r["slug"] for r in old}


def test_record_type_fallback_classifies_every_historical_shape():
    kinds = [records.record_type(r) for r in fixture_rows("decisions.jsonl")]
    assert kinds.count("classifier") == 32 and kinds.count("audit") == 32  # 30 days + 2 edges
    assert records.record_type({"record_type": "agent_audit", "agent_audit": {}}) == "audit"
    assert records.record_type({"event": "agent_audit", "audit_addendum": True}) == "audit"
    assert records.record_type({"publication_status": "not_published"}) == "reconciliation"
    # An audit addendum carrying a tier but no dimensions is still an audit.
    assert records.record_type({"tier": 2, "audit_addendum": True}) == "audit"
    shipped = shipped_for("2026-09-08", DOWNGRADED["2026-09-08"])
    assert records.record_type(shipped) == "shipped_tier" and "tier" not in shipped


def shipped_for(date, slug):
    return records.shipped_record(
        date=date, slug=slug, run_id=f"run-{date}", source_run=f"run-{date}",
        classifier_tier=2, shipped_tier=1, body_lines=92, tier1_max_lines=145,
        tier2_max_lines=260,
    )


def test_shipped_tier_records_reproduce_shipped_without_the_feedback_fallback(tmp_path):
    path = tmp_path / "decisions.jsonl"
    path.write_bytes((FIXTURE / "decisions.jsonl").read_bytes())
    before = path.read_bytes()
    for date, slug in DOWNGRADED.items():
        assert ledger.append_shipped(path, shipped_for(date, slug)) is True
        assert ledger.append_shipped(path, shipped_for(date, slug)) is False  # idempotent
    assert path.read_bytes().startswith(before)  # append-only: history byte-identical
    rows = records.tier_ledger(contract.records(path), [], start=SEPTEMBER[0], end=SEPTEMBER[1])
    assert len(rows) == 30
    assert records.distribution(rows, "classifier_tier") == (20, 9, 1)
    assert records.distribution(rows, "shipped_tier") == (23, 6, 1)
    assert {r["shipped_source"] for r in rows if r["date"] in DOWNGRADED} == {"shipped_tier"}


def test_a_shipped_tier_record_exists_only_for_a_downgrade():
    for classifier_tier, shipped_tier in ((1, 1), (1, 2), (2, 2), (3, 0)):
        with pytest.raises(ValueError, match="downgrade|integers"):
            records.shipped_record(
                date="2026-10-01", slug="s", run_id="r", source_run="r",
                classifier_tier=classifier_tier, shipped_tier=shipped_tier, body_lines=1,
                tier1_max_lines=145, tier2_max_lines=260,
            )


def run_module(*args):
    return subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", *args],
        cwd=SCRIPTS, capture_output=True, text=True, timeout=60,
    )


def test_tier_ledger_cli_reports_both_distributions():
    result = run_module(
        "tier-ledger", "--month", "2026-09",
        "--decisions", str(FIXTURE / "decisions.jsonl"),
        "--feedback", str(FIXTURE / "feedback.jsonl"),
    )
    assert result.returncode == 0, result.stderr
    assert "30 classifier decisions" in result.stdout
    assert "classifier T1/T2/T3: 20/9/1" in result.stdout
    assert "shipped    T1/T2/T3: 23/6/1" in result.stdout
    assert f"recovered from quarantine 2026-09-12 {RECOVERED}" in result.stdout


def load_script(name):
    spec = importlib.util.spec_from_file_location(
        name.replace("-", "_"), ROOT / ".claude/skills/blog-backfill/scripts" / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_tier_creep_guard_counts_the_recovered_day_and_never_a_shipped_record(tmp_path):
    path = tmp_path / "decisions.jsonl"
    path.write_bytes((FIXTURE / "decisions.jsonl").read_bytes())
    ledger.append_shipped(path, shipped_for("2026-09-08", DOWNGRADED["2026-09-08"]))
    rows = load_script("tier-creep-guard").load_daily_tiers(str(path))
    assert len(rows) == 32 and ("2026-09-12", 2) in rows


# ---- T02: the lander's length gate appends the shipped tier ---------------------------

LAND = (SCRIPTS / "blog-land.sh").read_text()
GATE = LAND[
    LAND.index("# --- Deterministic tier-and-length gate")
    : LAND.index("# tldr is the LLM-citation surface")
]


def run_gate(tmp_path, *, dry_run=0, body_lines=92, classifier_tier=2):
    blog = tmp_path / "blog"
    meth = blog / ".claude/skills/blog-backfill/methodology"
    if not blog.exists():
        meth.mkdir(parents=True)
        (blog / "scripts").mkdir()
        (blog / "scripts/blog").symlink_to(SCRIPTS)
        (meth / "decisions.jsonl").write_text('{"date": "2026-10-01", "tier": 2}\n')
        (meth / "feedback.jsonl").write_text("")
    post = tmp_path / "post.md"
    post.write_text("+++\ntitle = \"t\"\n+++\n" + "line\n" * body_lines)
    variables = {
        "BLOG_DIR": blog, "DECISIONS": meth / "decisions.jsonl", "POST": post,
        "TARGET_DATE": "2026-10-01", "SLUG": "fixture-post", "BLOG_RUN_ID": "run-a",
        "CLASSIFIER_RUN_ID": "run-a", "CLASSIFIER_TIER": classifier_tier,
        "DRY_RUN": dry_run, "LOG": tmp_path / "land.log", "TITLE": "t",
    }
    assignments = "\n".join(f"{k}={shlex.quote(str(v))}" for k, v in variables.items())
    shell = f"set -uo pipefail\n{assignments}\nlog() {{ printf '%s\\n' \"$*\" >> \"$LOG\"; }}\n"
    result = subprocess.run(
        ["/bin/bash", "-c", shell + GATE], capture_output=True, text=True, timeout=60,
        env={k: v for k, v in os.environ.items() if not k.startswith("BLOG_")},
    )
    assert result.returncode == 0, result.stderr
    return contract.records(meth / "decisions.jsonl"), (tmp_path / "land.log").read_text()


def test_lander_appends_one_shipped_tier_record_when_length_downgrades(tmp_path):
    rows, log = run_gate(tmp_path)
    assert rows[0] == {"date": "2026-10-01", "tier": 2}  # history untouched
    assert rows[1:] == [{
        "record_type": "shipped_tier", "date": "2026-10-01", "slug": "fixture-post",
        "run_id": "run-a", "source_run": "run-a", "classifier_tier": 2, "shipped_tier": 1,
        "downgrade_reason": "length_gate", "body_lines": 92,
        "thresholds": {"tier1_max_lines": 145, "tier2_max_lines": 260},
    }]
    assert "recorded shipped tier 1 beside classifier tier 2" in log
    again, _ = run_gate(tmp_path)
    assert again == rows  # a re-entered lander does not double-count


def test_lander_records_nothing_without_a_downgrade_or_in_a_dry_run(tmp_path):
    rows, _ = run_gate(tmp_path, body_lines=200)
    assert len(rows) == 1
    rows, log = run_gate(tmp_path, dry_run=1)
    assert len(rows) == 1 and "DRY-RUN: would append a shipped_tier record" in log


def test_producer_append_skips_a_lander_shipped_record_with_the_same_identity(produced):  # noqa: F811
    repo, post, _, transcript = produced
    rows = contract.records(repo / contract.DECISIONS)
    classifier, audit = rows[-2], rows[-1]
    shipped = {**shipped_for(DATE, post.stem), "run_id": RUN, "source_run": RUN}
    assert ledger.append_shipped(repo / contract.DECISIONS, shipped)
    contract.append_record(
        repo, DATE, post.stem, RUN, audit,
        classifier_record=classifier, audit_record=audit, transcript=transcript,
    )
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"


# ---- T03: the producer schema ---------------------------------------------------------


def test_the_september_regression_shapes_are_named_by_field():
    rows = {r["date"]: r for r in fixture_rows("decisions.jsonl") if records.is_classifier(r)}
    early, late = rows["2026-09-02"], rows["2026-09-22"]
    gaps = " ".join(schema.classifier_gaps(late))
    assert "classifier.cadence_type (got absent" in gaps
    assert "classifier.rhetorical_structure (got {" in gaps
    assert "classifier.record_type" in gaps
    assert schema.classifier_gaps({**early, "record_type": "classifier"}) == []
    flagged = {**early, **VALID_CLASSIFIER, "anti_inflation_flags": ["none triggered"]}
    assert schema.classifier_gaps(flagged) == [
        "classifier.anti_inflation_flags (off-enum 'none triggered'; allowed: "
        + "|".join(records.ANTI_INFLATION_FLAGS) + ")"
    ]


def test_september_flag_conformance_matches_the_report():
    """Producer switch on 09-15: exact-enum flags fell from most to under half."""
    def exact(start, end):
        flags = [
            flag
            for r in fixture_rows("decisions.jsonl")
            if records.is_classifier(r) and start <= r["date"] < end
            for flag in r.get("anti_inflation_flags") or []
        ]
        return sum(flag in records.ANTI_INFLATION_FLAGS for flag in flags), len(flags)

    first, second = exact("2026-09-01", "2026-09-15"), exact("2026-09-15", "2026-10-01")
    assert first[0] / first[1] > 0.6 and second[0] / second[1] < 0.5


def rewrite_run(repo, classifier_change=None, audit_change=None):
    """Edit the run's appended (uncommitted) pair in place, as the brief tests do."""
    path = repo / contract.DECISIONS
    rows = contract.records(path)
    (classifier_change or (lambda r: None))(rows[-2])
    (audit_change or (lambda r: None))(rows[-1])
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))


def make_valid(repo):
    rewrite_run(repo, lambda r: r.update(VALID_CLASSIFIER), lambda r: r.update(record_type="audit"))


@pytest.fixture
def enforce(monkeypatch):
    monkeypatch.setattr(schema, "RECORD_SCHEMA_ENFORCE_FROM", DATE)


def schema_line(stderr):
    lines = [line for line in stderr.splitlines() if "ADVISORY: record schema" in line]
    assert lines, stderr
    return lines[-1]


def test_observation_mode_reports_the_gaps_and_still_passes(produced, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    line = schema_line(capsys.readouterr().err)
    assert "(observation until 2026-10-17): missing classifier.record_type" in line
    assert "classifier.cadence_type" in line and "audit.record_type" in line


def test_a_valid_pair_reports_complete_and_passes_when_enforced(produced, enforce, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    make_valid(repo)
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    assert schema_line(capsys.readouterr().err).endswith("(enforced): complete")


BREAK = {
    "classifier.record_type": lambda c, a: c.pop("record_type"),
    "classifier.anti_inflation_flags": lambda c, a: c.update(
        anti_inflation_flags=["volume-not-quality: 12 commits but all routine"]
    ),
    "classifier.cadence_type": lambda c, a: c.update(cadence_type=None),
    "classifier.rhetorical_structure": lambda c, a: c.update(rhetorical_structure={"x": 1}),
    "audit.record_type": lambda c, a: a.update(record_type="classifier"),
}


@pytest.mark.parametrize("field", sorted(BREAK))
def test_a_malformed_new_record_refuses_naming_the_field(produced, enforce, field):  # noqa: F811
    repo, _, _, transcript = produced
    make_valid(repo)
    rows = contract.records(repo / contract.DECISIONS)
    BREAK[field](rows[-2], rows[-1])
    (repo / contract.DECISIONS).write_text("".join(json.dumps(r) + "\n" for r in rows))
    with pytest.raises(contract.ContractError, match=rf"record schema invalid: {field} \("):
        contract.validate(repo, DATE, RUN, transcript)


def test_historical_records_are_never_revalidated(produced, enforce):  # noqa: F811
    """A malformed committed record from before the switch cannot fail today's run."""
    repo, _, _, transcript = produced
    make_valid(repo)
    path = repo / contract.DECISIONS
    baseline = git(repo, "show", f"HEAD:{contract.DECISIONS}").stdout.decode()
    tail = path.read_text()[len(baseline):]
    legacy = {
        "date": "2026-09-22", "slug": "old-post", "tier": 1, "dimensions": {},
        "rhetorical_structure": {"closing": "dict"}, "anti_inflation_flags": ["none triggered"],
    }
    path.write_text(baseline + json.dumps(legacy) + "\n")
    git(repo, "add", contract.DECISIONS)
    git(repo, "commit", "-qm", "historical malformed record")
    path.write_text(path.read_text() + tail)
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"


def test_env_lever_disables_or_moves_the_switch(produced, enforce, monkeypatch, capsys):  # noqa: F811
    repo, _, _, transcript = produced
    monkeypatch.setenv("BLOG_RECORD_SCHEMA_ENFORCE_FROM", "off")
    contract.validate(repo, DATE, RUN, transcript)
    assert "enforcement off via BLOG_RECORD_SCHEMA_ENFORCE_FROM" in schema_line(
        capsys.readouterr().err
    )
    monkeypatch.setenv("BLOG_RECORD_SCHEMA_ENFORCE_FROM", "2099-01-01")
    contract.validate(repo, DATE, RUN, transcript)
    monkeypatch.setenv("BLOG_RECORD_SCHEMA_ENFORCE_FROM", "soon")
    with pytest.raises(contract.ContractError, match="BLOG_RECORD_SCHEMA_ENFORCE_FROM"):
        contract.validate(repo, DATE, RUN, transcript)


def test_the_proposed_switch_date_and_shared_mechanism():
    brief = importlib.import_module("blogpipe.brief")
    assert schema.RECORD_SCHEMA_ENFORCE_FROM == "2026-10-17"
    assert schema.enforced("2026-10-16") is False and schema.enforced("2026-10-17") is True
    assert type(schema.SWITCH) is type(brief.SWITCH)  # one mechanism, two switches


def test_contract_readiness_covers_both_switches(tmp_path):
    for day in ("2026-10-12", "2026-10-13"):
        (tmp_path / f"run-{day}.log").write_text(
            "PRODUCER-CONTRACT: ADVISORY: amended contract (observation): complete\n"
            "PRODUCER-CONTRACT: ADVISORY: record schema (observation): missing x\n"
        )
    env = {k: v for k, v in os.environ.items() if not k.startswith("BLOG_")}
    result = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "contract-readiness", "--log-dir",
         str(tmp_path), "--date", "2026-10-14"],
        cwd=SCRIPTS, capture_output=True, text=True, env=env, timeout=60,
    )
    assert result.returncode == 2, result.stderr
    (line,) = result.stdout.splitlines()
    brief_part, schema_part = line.split(" | ")
    assert brief_part.startswith("URGENT: brief enforcement active since 2026-10-14")
    assert schema_part.startswith("record schema enforcement in 3 day(s) (run date 2026-10-17)")
    assert "consecutive complete 0/7" in schema_part
