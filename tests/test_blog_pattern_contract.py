"""Actual deterministic pattern replay; all native/session/Git artifacts are offline fixtures."""

import json
import shutil
import subprocess

import pytest
from test_blog_publication_state import DATE, RUN, contract
from test_blog_publication_state import run as run
from test_blog_staged_contract import ROOT, SCRIPT, arguments

CAP = {
    "pattern_id": "offline-cap-tier",
    "active": True,
    "rule": {
        "all": [{"feature": "max_all", "op": ">=", "value": 0}],
        "action": {"type": "cap_tier", "tier": 1},
    },
}


@pytest.fixture
def candidate(run, monkeypatch):
    monkeypatch.delenv("BLOG_RUN_MANIFEST", raising=False)
    authority = run["root"] / contract.DECISIONS
    classifier, audit = contract.records(authority)[-2:]
    stage = run["root"] / ".blog-staging"
    run.update(
        authority=authority,
        classifier=classifier,
        audit=audit,
        classifier_file=stage / f"{DATE}.{RUN}.classifier.json",
        audit_file=stage / f"{DATE}.{RUN}.audit.json",
    )
    return run


def write_candidate(candidate, *, appended=True, preflight=False):
    baseline = subprocess.check_output(
        ["git", "-C", str(candidate["root"]), "show", f"HEAD:{contract.DECISIONS}"]
    )
    suffix = "".join(json.dumps(candidate[key]) + "\n" for key in ("classifier", "audit"))
    candidate["authority"].write_bytes(baseline + (suffix.encode() if appended else b""))
    for key in ("classifier", "audit"):
        candidate[f"{key}_file"].write_text(json.dumps(candidate[key]))
    sentinel = candidate["root"] / f".blog-staging/{DATE}.intent.json"
    value = json.loads(sentinel.read_text())
    value.update(tier=candidate["classifier"]["tier"], ready=not preflight)
    sentinel.write_text(json.dumps(value))


def forge(candidate, fault):
    classifier = candidate["classifier"]
    if fault == "marker-only":
        classifier["pattern_engine"] = {
            key: classifier["pattern_engine"][key] for key in ("ran", "ruleset_digest")
        }
    elif fault == "wrong-tier":
        # No rules exist. Claiming a downgrade cannot be a real apply result.
        classifier.update(tier=1, tier_name="Field Note")
        classifier["pattern_engine"]["tier_after"] = 1
    else:
        classifier["applied_patterns"] = ["invented-pattern"]
        classifier["pattern_engine"]["matched"] = ["invented-pattern"]


def verify(candidate, script=SCRIPT, *, preflight=False):
    args = [
        "python3",
        str(script),
        "verify",
        "--repo",
        str(candidate["root"]),
        "--date",
        DATE,
        "--run-id",
        RUN,
        "--transcript",
        str(candidate["transcript"]),
    ]
    return subprocess.run(
        args + (["--preflight"] if preflight else []), capture_output=True, text=True
    )


@pytest.mark.parametrize("fault", ["marker-only", "wrong-tier", "wrong-list"])
@pytest.mark.parametrize("preflight", [False, True])
def test_old_cli_accepts_marker_or_false_machine_result_new_refuses(
    candidate, tmp_path, fault, preflight
):
    forge(candidate, fault)
    write_candidate(candidate, preflight=preflight)
    old = tmp_path / "old-pattern-contract.py"
    old.write_bytes(
        subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "show",
                "d471768c:scripts/blog/blog-producer-contract.py",
            ]
        )
    )
    shutil.copyfile(
        ROOT / "scripts/blog/blog_publication_state.py", old.parent / "blog_publication_state.py"
    )
    old_result = verify(candidate, old, preflight=preflight)
    assert old_result.returncode == 0, old_result.stderr
    before = candidate["authority"].read_bytes()
    repaired = verify(candidate, preflight=preflight)
    assert repaired.returncode == 65
    assert not repaired.stdout
    assert candidate["authority"].read_bytes() == before
    (tmp_path / "old-pattern-marker-receipt.json").write_text(
        json.dumps(
            {
                "fixture_only": True,
                "fault": fault,
                "preflight": preflight,
                "old_source": "d471768c:scripts/blog/blog-producer-contract.py",
                "old_source_sha256": contract.digest(old),
                "old_supported_cli": old_result.args,
                "old_exit_code": old_result.returncode,
                "old_completion": json.loads(old_result.stdout),
                "repaired_exit_code": repaired.returncode,
                "repaired_error": repaired.stderr.strip(),
                "authority_unchanged": candidate["authority"].read_bytes() == before,
                "real_native_artifacts_modified": False,
            },
            indent=2,
        )
        + "\n"
    )


@pytest.mark.parametrize("fault", ["marker-only", "wrong-tier", "wrong-list"])
@pytest.mark.parametrize("selected", ["classifier", "audit"])
def test_both_appends_refuse_false_machine_result_before_authority(candidate, fault, selected):
    forge(candidate, fault)
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    result = subprocess.run(
        arguments(candidate, "append", selected), capture_output=True, text=True
    )
    assert result.returncode == 65
    assert "pattern-engine" in result.stderr
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize(
    "field", ["ran", "ruleset_digest", "rules_evaluated", "tier_before", "tier_after", "matched"]
)
def test_every_actual_receipt_field_is_required_before_staged_check(candidate, field):
    del candidate["classifier"]["pattern_engine"][field]
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    result = subprocess.run(arguments(candidate, "check-staged"), capture_output=True, text=True)
    assert result.returncode == 65
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize(
    "fault",
    [
        "boolean-count",
        "boolean-before",
        "boolean-after",
        "wrong-count",
        "wrong-name",
        "extra-receipt-field",
        "non-string-match",
    ],
)
def test_full_receipt_types_and_exact_deterministic_fields_are_checked(candidate, fault):
    classifier = candidate["classifier"]
    receipt = classifier["pattern_engine"]
    if fault.startswith("boolean-"):
        receipt[
            {
                "boolean-count": "rules_evaluated",
                "boolean-before": "tier_before",
                "boolean-after": "tier_after",
            }[fault]
        ] = True
    elif fault == "wrong-count":
        receipt["rules_evaluated"] = 1
    elif fault == "wrong-name":
        classifier["tier_name"] = "Fabricated Field Note label"
    elif fault == "extra-receipt-field":
        receipt["invented-engine-field"] = "not actual engine output"
    else:
        receipt["matched"] = [None]
        classifier["applied_patterns"] = [None]
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    result = subprocess.run(arguments(candidate, "check-staged"), capture_output=True, text=True)
    assert result.returncode == 65
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize("failure", ["nonzero", "malformed", "unchanged-echo"])
def test_actual_engine_failure_cannot_be_attested_away(candidate, failure):
    engine = candidate["root"] / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    scripts = {
        "nonzero": "import sys; sys.exit(42)\n",
        "malformed": "print('not JSON')\n",
        "unchanged-echo": "import sys; print(sys.stdin.read())\n",
    }
    engine.write_text(scripts[failure])
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    result = subprocess.run(
        arguments(candidate, "append", "classifier"), capture_output=True, text=True
    )
    assert result.returncode == 65
    assert "pattern-engine" in result.stderr
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize(
    "malformed",
    [
        "boolean-count",
        "float-count",
        "float-tier",
        "float-after",
        "receipt-list",
        "nested-matched",
        "applied-object",
    ],
)
def test_malformed_actual_engine_output_types_never_complete_staged(candidate, malformed):
    output = json.loads(json.dumps(candidate["classifier"]))
    if malformed == "boolean-count":
        output["pattern_engine"]["rules_evaluated"] = False
    elif malformed == "float-count":
        output["pattern_engine"]["rules_evaluated"] = 0.0
    elif malformed == "float-tier":
        output["tier"] = 2.0
    elif malformed == "float-after":
        output["pattern_engine"]["tier_after"] = 2.0
    elif malformed == "receipt-list":
        output["pattern_engine"] = [output["pattern_engine"]]
    elif malformed == "nested-matched":
        output["pattern_engine"]["matched"] = [[]]
    else:
        output["applied_patterns"] = {"matched": []}
    engine = candidate["root"] / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    # Explicit invalid fixture engine output, never a real producer artifact.
    engine.write_text("import json\nprint(json.dumps(" + repr(output) + "))\n")
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    result = subprocess.run(arguments(candidate, "check-staged"), capture_output=True, text=True)
    assert result.returncode == 65
    assert not result.stdout
    assert "deterministic result differs" in result.stderr
    assert candidate["authority"].read_bytes() == before


@pytest.mark.parametrize("run", [{"patterns": json.dumps(CAP) + "\n"}], indirect=True)
def test_real_cap_result_replays_readonly_and_appends_pair_once(candidate):
    classifier = candidate["classifier"]
    assert classifier["tier"] == 1
    assert classifier["tier_name"] == "Field Note"
    assert classifier["applied_patterns"] == [CAP["pattern_id"]]
    assert classifier["pattern_engine"] == {
        "ran": True,
        "ruleset_digest": classifier["pattern_engine"]["ruleset_digest"],
        "rules_evaluated": 1,
        "tier_before": 2,
        "tier_after": 1,
        "matched": [CAP["pattern_id"]],
    }
    write_candidate(candidate, appended=False)
    before = candidate["authority"].read_bytes()
    checked = subprocess.run(arguments(candidate, "check-staged"), capture_output=True, text=True)
    assert checked.returncode == 0, checked.stderr
    assert candidate["authority"].read_bytes() == before
    for selected in ("classifier", "audit", "classifier", "audit"):
        result = subprocess.run(
            arguments(candidate, "append", selected), capture_output=True, text=True
        )
        assert result.returncode == 0, result.stderr
    assert len(contract.records(candidate["authority"])) == 3
    assert verify(candidate).returncode == 0
