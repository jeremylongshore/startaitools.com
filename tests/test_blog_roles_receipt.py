"""Regression: rejected run 2026-09-17/679b62a4 and the receipt that replaces its gate.

The fixture transcript is the real session, reduced to its Agent records. All six
Agent invocations in it COMPLETED, yet the gate at 624f80fd counted none because
CLI 2.1.27x labels task notifications promptSource "system", never "sdk". Four
finished posts (09-15..09-18) were rejected on that alone while every content gate
passed. Completion is now read from what each role produced, staged and hash-bound.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from blog_roles import stage_roles
from test_blog_producer_contract import DATE, RUN, contract, produced  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/blog/blog-producer-contract.py"
REJECTED = ROOT / "tests/fixtures/rejected-run-2026-09-17-679b62a4.transcript.jsonl"
REJECTED_RUN = "679b62a4-af0b-4ec0-a1c7-d66a419ede89"
OLD_GATE = "624f80fd"  # origin/master when the run was rejected
MANDATORY = {"blog-classifier", "content-marketer", "seo-meta-optimizer"}


def verify(script, repo, transcript):
    return subprocess.run(
        [sys.executable, str(script), "verify", "--repo", str(repo), "--date", DATE]
        + ["--run-id", RUN, "--transcript", str(transcript)],
        capture_output=True,
        text=True,
    )


@pytest.fixture
def rejected(produced, tmp_path):  # noqa: F811
    """The real session's records, rebound to the offline workspace's run."""
    repo, post, sentinel, _ = produced
    transcript = tmp_path / "real" / f"{RUN}.jsonl"
    transcript.parent.mkdir()
    transcript.write_text(REJECTED.read_text().replace(REJECTED_RUN, RUN))
    return repo, post, sentinel, transcript


def test_real_session_completed_every_agent_but_the_transcript_gate_saw_none():
    rows = [json.loads(line) for line in REJECTED.read_text().splitlines()]
    notified = [r for r in rows if r.get("origin") == {"kind": "task-notification"}]
    assert len(notified) == 6
    assert all("<status>completed</status>" in r["message"]["content"] for r in notified)
    assert {r["promptSource"] for r in notified} == {"system"}
    assert contract.completed_agents(REJECTED, REJECTED_RUN) == {}


def test_old_gate_rejects_the_real_run_and_the_receipt_accepts_it(rejected, tmp_path):
    repo, _, _, transcript = rejected
    old = tmp_path / "old-gate.py"
    old.write_bytes(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{OLD_GATE}:scripts/blog/blog-producer-contract.py"]
        )
    )
    (tmp_path / "blog_publication_state.py").write_bytes(
        (ROOT / "scripts/blog/blog_publication_state.py").read_bytes()
    )
    before = verify(old, repo, transcript)
    assert before.returncode == 65
    assert "PENDING WORK: mandatory Agent completion missing" in before.stderr
    after = verify(SCRIPT, repo, transcript)
    assert after.returncode == 0, after.stderr
    assert json.loads(after.stdout)["outcome"] == "complete"
    assert "ADVISORY: transcript corroborates 0/3 mandatory roles" in after.stderr


@pytest.mark.parametrize(
    "fault",
    ["absent", "edited-output", "empty-output", "stale-post", "foreign-run", "role-missing"]
    + ["role-failed", "foreign-agent", "symlink"],
)
def test_receipt_cannot_vouch_for_output_that_is_not_there(produced, tmp_path, fault):  # noqa: F811
    repo, post, _, transcript = produced
    staging = repo / ".blog-staging"
    receipt = staging / f"{DATE}.{RUN}.roles.json"
    role = staging / f"{DATE}.{RUN}.role-seo-meta-optimizer.json"
    outputs = dict.fromkeys(MANDATORY, "offline fixture result")
    arguments = dict(date=DATE, run_id=RUN, slug=post.stem, post=post)
    if fault == "absent":
        receipt.unlink()
    elif fault == "edited-output":
        role.write_text(role.read_text().replace("offline", "rewritten after the receipt"))
    elif fault == "empty-output":
        stage_roles(repo, outputs={**outputs, "seo-meta-optimizer": "   "}, **arguments)
    elif fault == "stale-post":
        value = json.loads(receipt.read_text())
        value["post_sha256"] = "0" * 64
        receipt.write_text(json.dumps(value))
    elif fault == "foreign-run":
        value = json.loads(receipt.read_text())
        value["run_id"] = "another-run"
        receipt.write_text(json.dumps(value))
    elif fault == "role-missing":
        outputs.pop("seo-meta-optimizer")
        stage_roles(repo, outputs=outputs, **arguments)
    elif fault == "role-failed":
        outputs.pop("seo-meta-optimizer")
        stage_roles(repo, outputs=outputs, statuses={"seo-meta-optimizer": "failed"}, **arguments)
    elif fault == "foreign-agent":
        value = json.loads(role.read_text())
        value["agent"] = "content-marketer"
        role.write_text(json.dumps(value))
        stored = json.loads(receipt.read_text())
        stored["roles"]["seo-meta-optimizer"]["output_sha256"] = contract.digest(role)
        receipt.write_text(json.dumps(stored))
    elif fault == "symlink":
        outside = tmp_path / "outside-roles.json"
        outside.write_bytes(receipt.read_bytes())
        receipt.unlink()
        receipt.symlink_to(outside)
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)


def test_transcript_is_optional_corroboration(produced):  # noqa: F811
    repo, _, _, transcript = produced
    transcript.unlink()
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    assert contract.validate(repo, DATE, RUN, None)["outcome"] == "complete"


@pytest.mark.parametrize("field", ["date", "run_id"])
def test_staging_identity_cannot_carry_path_syntax(produced, field):  # noqa: F811
    repo, _, _, _ = produced
    identity = {"date": DATE, "run_id": RUN, "slug": "fixture-post", field: "../../elsewhere"}
    with pytest.raises(contract.ContractError, match="path syntax"):
        contract.staged_file(repo, identity, "roles")
