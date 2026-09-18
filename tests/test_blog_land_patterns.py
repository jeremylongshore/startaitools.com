"""Execute actual lander gates with disposable Git and explicit offline Hugo fixtures."""

import json
import os
import shlex
import subprocess
from pathlib import Path

import pytest
from test_blog_publication_state import DATE, POST, RUN, SLUG, contract, git
from test_blog_publication_state import run as run

ROOT = Path(__file__).resolve().parents[1]
LAND = ROOT / "scripts/blog/blog-land.sh"


@pytest.fixture
def candidate(run):
    path = run["root"] / contract.DECISIONS
    rows = contract.records(path)
    rows[-1]["tier"] = rows[-2]["tier"]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    run.update(authority=path, rows=rows)
    return run


def write_rows(candidate):
    candidate["authority"].write_text("".join(json.dumps(row) + "\n" for row in candidate["rows"]))


def land_gates(candidate, tmp_path, *, source=None, bound=True):
    """Execute the actual precondition/classifier/pattern/tier and dry-run exit.

    Earlier manifest/producer checks and the later publication lane are outside
    this focused replay. No pipeline lock, real provider, mail or live URL is used.
    """
    source = LAND.read_text() if source is None else source
    block = source.split("# (2) Classifier record", 1)[1]
    block = "# (2) Classifier record" + block.split("# ---- Land: commit", 1)[0]
    log = tmp_path / "land-gates.log"
    variables = {
        "BLOG_DIR": candidate["root"],
        "DECISIONS": candidate["authority"],
        "BLOG_RUN_MANIFEST": candidate["manifest"] if bound else "",
        "BLOG_RUN_ID": RUN if bound else "",
        "CLASSIFIER_RUN_ID": RUN if bound else "",
        "SKILL_SCRIPTS": candidate["root"] / ".claude/skills/blog-backfill/scripts",
        "TARGET_DATE": DATE,
        "SLUG": SLUG,
        "POST": candidate["root"] / POST,
        "POST_REL": POST,
        "LOG": log,
        "CANONICAL": "https://fixture.example.invalid/no-provider-call/",
        "DEPLOY_BRANCH": "master",
    }
    assignments = "\n".join(f"{key}={shlex.quote(str(value))}" for key, value in variables.items())
    shell = f"""
set -uo pipefail
{assignments}
cd "$BLOG_DIR"
DRY_RUN=1
REASONS=()
log() {{ printf '%s\\n' "$*" | tee -a "$LOG"; }}
hugo() {{ printf 'OFFLINE_HUGO_FIXTURE: build intentionally mocked\\n'; return 0; }}
date() {{ printf '2026-09-18\\n'; }}
{block}
"""
    return subprocess.run(
        ["/bin/bash", "-c", shell],
        cwd=candidate["root"],
        env={**os.environ, "BLOG_CANARY": "1"},
        capture_output=True,
        text=True,
        timeout=20,
    ), log


def test_old_lander_mutates_tiered_audit_new_preserves_valid_classifier(candidate, tmp_path):
    old_source = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", "951f5911:scripts/blog/blog-land.sh"]
    ).decode()
    before = candidate["authority"].read_bytes()
    owner_head = git(candidate["owner"], "rev-parse", "HEAD")
    owner_tracked = candidate["owner"] / ".gitignore"
    owner_tracked.write_text(owner_tracked.read_text() + "owner-preexisting/\n")
    owner_note = candidate["owner"] / "owner-untracked-note"
    owner_note.write_text("Preserve unrelated owner fixture.\n")
    owner_status = git(candidate["owner"], "status", "--porcelain")
    owner_bytes = owner_tracked.read_bytes()
    old, old_log = land_gates(candidate, tmp_path, source=old_source)
    assert old.returncode == 0, old.stderr
    assert "PATTERN-HEAL: producer skipped step 2b" in old_log.read_text()
    old_rows = contract.records(candidate["authority"])
    assert old_rows[-2] == candidate["rows"][-2]
    assert old_rows[-1] != candidate["rows"][-1]
    assert {"pattern_engine", "applied_patterns"} <= old_rows[-1].keys()
    candidate["authority"].write_bytes(before)  # disposable fixture only
    old_log.rename(tmp_path / "old-land-gates.log")
    repaired, repaired_log = land_gates(candidate, tmp_path)
    assert repaired.returncode == 0, repaired.stderr
    assert "PATTERN-HEAL" not in repaired_log.read_text()
    assert "Pattern engine receipt OK" in repaired_log.read_text()
    assert candidate["authority"].read_bytes() == before
    assert git(candidate["owner"], "rev-parse", "HEAD") == owner_head
    assert git(candidate["owner"], "status", "--porcelain") == owner_status
    assert owner_tracked.read_bytes() == owner_bytes
    assert owner_note.read_text() == "Preserve unrelated owner fixture.\n"
    (tmp_path / "old951-land-pattern-receipt.json").write_text(
        json.dumps(
            {
                "fixture_only": True,
                "old_source": "951f5911:scripts/blog/blog-land.sh",
                "old_source_sha256": contract.hashlib.sha256(old_source.encode()).hexdigest(),
                "old_exit_code": old.returncode,
                "old_classifier_unchanged": old_rows[-2] == candidate["rows"][-2],
                "old_audit_mutated": old_rows[-1] != candidate["rows"][-1],
                "old_false_skipped_step_warning": True,
                "repaired_exit_code": repaired.returncode,
                "repaired_authority_unchanged": candidate["authority"].read_bytes() == before,
                "repaired_false_warning_absent": "PATTERN-HEAL" not in repaired_log.read_text(),
                "hugo_is_explicit_offline_fixture": True,
                "full_publication_lane_exercised": False,
                "real_native_artifacts_modified": False,
            },
            indent=2,
        )
        + "\n"
    )


def test_previous_heal_warning_is_not_relogged_for_a_valid_new_run(candidate, tmp_path):
    previous = "PATTERN-HEAL: preserved historical failure evidence\n"
    log = tmp_path / "land-gates.log"
    log.write_text(previous)
    before = candidate["authority"].read_bytes()
    result, _ = land_gates(candidate, tmp_path)
    assert result.returncode == 0, result.stderr
    assert log.read_text().count(previous) == 1
    assert previous.strip() not in result.stdout
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize("receipt", ["missing", "stale"])
def test_bound_classifier_missing_or_stale_receipt_fails_without_heal(candidate, tmp_path, receipt):
    classifier, audit = candidate["rows"][-2:]
    # A tiered audit carrying a valid digest must never stand in for classifier proof.
    audit["pattern_engine"] = classifier["pattern_engine"].copy()
    if receipt == "missing":
        del classifier["pattern_engine"]
    else:
        classifier["pattern_engine"]["ruleset_digest"] = "obsolete-rules"
    write_rows(candidate)
    before = candidate["authority"].read_bytes()
    result, log = land_gates(candidate, tmp_path)
    assert result.returncode == 10
    assert "PATTERN-GATE: bound classifier" in log.read_text()
    assert "PATTERN-HEAL" not in log.read_text()
    assert "PRECONDITIONS FAILED" in result.stdout
    assert candidate["authority"].read_bytes() == before


def test_classifier_and_audit_presence_are_exact_run_scoped(candidate, tmp_path):
    candidate["rows"][-2]["run_id"] = "different-fixture-run"
    write_rows(candidate)
    before = candidate["authority"].read_bytes()
    result, _ = land_gates(candidate, tmp_path)
    assert result.returncode == 10
    assert "no classifier record" in result.stdout
    assert candidate["authority"].read_bytes() == before


def test_audit_presence_cannot_borrow_another_run(candidate, tmp_path):
    candidate["rows"][-1]["run_id"] = "different-fixture-run"
    write_rows(candidate)
    before = candidate["authority"].read_bytes()
    result, _ = land_gates(candidate, tmp_path)
    assert result.returncode == 10
    assert "no agent_audit addendum" in result.stdout
    assert candidate["authority"].read_bytes() == before


def test_tier_comes_from_classifier_even_if_audit_has_a_different_tier(candidate, tmp_path):
    candidate["rows"][-1]["tier"] = 3
    write_rows(candidate)
    before = candidate["authority"].read_bytes()
    result, log = land_gates(candidate, tmp_path)
    assert result.returncode == 0, result.stderr
    assert "Tier: 2 (classifier 2," in log.read_text()
    assert "TIER-LENGTH GATE" not in log.read_text()
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize("failure", ["nonzero", "empty"])
def test_pattern_engine_failure_is_visible_and_cannot_modify_authority(
    candidate, tmp_path, failure
):
    engine = candidate["root"] / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    engine.write_text(
        "import sys\nprint('FIXTURE_PATTERN_ENGINE_FAILURE', file=sys.stderr)\n"
        + ("sys.exit(42)\n" if failure == "nonzero" else "sys.exit(0)\n")
    )
    before = candidate["authority"].read_bytes()
    result, log = land_gates(candidate, tmp_path)
    assert result.returncode == 10
    assert "pattern preparation/validation failed" in result.stdout
    assert "FIXTURE_PATTERN_ENGINE_FAILURE" in log.read_text()
    assert "RuntimeError: pattern engine digest failed or empty" in log.read_text()
    assert "PATTERN-HEAL" not in log.read_text()
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize("committed", [False, True])
def test_explicit_legacy_unbound_heal_only_changes_uncommitted_classifier(
    candidate, tmp_path, committed
):
    del candidate["rows"][-2]["pattern_engine"]
    write_rows(candidate)
    if committed:
        git(candidate["root"], "add", contract.DECISIONS)
        git(
            candidate["root"],
            "-c",
            "user.name=Offline",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "explicit offline committed legacy fixture",
        )
    before = candidate["authority"].read_bytes()
    result, log = land_gates(candidate, tmp_path, bound=False)
    if committed:
        assert result.returncode == 10
        assert "already committed" in log.read_text()
        assert candidate["authority"].read_bytes() == before
    else:
        assert result.returncode == 0, result.stderr
        assert "PATTERN-HEAL" in log.read_text()
        rows = contract.records(candidate["authority"])
        assert rows[-2]["pattern_engine"]["ran"] is True
        assert rows[-1] == candidate["rows"][-1]
