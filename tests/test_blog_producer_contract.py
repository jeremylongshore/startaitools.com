"""Offline regression replay of Sept15/16 semantic completion failures."""

import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "contract", ROOT / "scripts/blog/blog-producer-contract.py"
)
contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contract)
DATE = "2026-09-15"
RUN = "offline-run-one"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def produced(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.invalid")
    git(repo, "config", "user.name", "Offline fixture")
    meth = repo / Path(contract.DECISIONS).parent
    meth.mkdir(parents=True)
    (meth / "decisions.jsonl").write_text("{}\n")
    (meth / "patterns.jsonl").write_text("")
    engine = meth.parent / "scripts/apply-patterns.py"
    engine.parent.mkdir()
    shutil.copy(ROOT / ".claude/skills/blog-backfill/scripts/apply-patterns.py", engine)
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "fixture baseline")
    posts = repo / "content/posts"
    posts.mkdir(parents=True)
    post = posts / "fixture-post.md"
    post.write_text('+++\ndate = "2026-09-15"\n+++\nAn offline fixture.\n')
    identity = {"date": DATE, "slug": post.stem, "run_id": RUN}
    receipt = subprocess.run(
        ["python3", str(engine), "digest"], capture_output=True, text=True, check=True
    ).stdout.strip()
    classifier = {**identity, "tier": 1, "pattern_engine": {"ran": True, "ruleset_digest": receipt}}
    classifier.update(
        tier_name="Field Note",
        confidence=0.8,
        dimensions={key: 1 for key in ("novelty", "arc", "nar", "tch", "scp", "rpr")},
    )
    audit = {**identity, "audit_addendum": True, "agent_audit": {"writer": "content-marketer"}}
    contract.append_record(repo, DATE, post.stem, RUN, classifier)
    contract.append_record(repo, DATE, post.stem, RUN, audit)
    staging = repo / ".blog-staging"
    staging.mkdir()
    sentinel = staging / f"{DATE}.intent.json"
    sentinel.write_text(
        json.dumps(
            {
                **identity,
                "schema_version": 1,
                "ready": True,
                "tier": 1,
                "post_sha256": contract.digest(post),
                "gates": {"build": "pass", "voice_lint": "pass"},
            }
        )
    )
    transcript = tmp_path / f"{RUN}.jsonl"
    rows = []
    for i, agent in enumerate(["blog-classifier", "content-marketer", "seo-meta-optimizer"]):
        rows.extend(
            [
                {
                    "message": {
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "Agent",
                                "id": str(i),
                                "input": {"subagent_type": agent},
                            }
                        ]
                    }
                },
                {
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": str(i),
                                "content": "offline fixture result",
                            }
                        ]
                    }
                },
            ]
        )
    for row in rows:
        row["sessionId"] = RUN
    transcript.write_text("\n".join(map(json.dumps, rows)))
    return repo, post, sentinel, transcript


@pytest.mark.parametrize(
    "failure",
    [
        "sentinel",
        "audit",
        "missing_slug",
        "pattern",
        "wrong_date",
        "wrong_run",
        "wrong_revision",
        "missing_agent",
        "blocked_gate",
        "historical_edit",
    ],
)
def test_clean_exit_never_overrides_incomplete_contract(produced, failure):
    repo, post, sentinel, transcript = produced
    path = repo / contract.DECISIONS
    rows = contract.records(path)
    if failure == "sentinel":
        sentinel.unlink()
    elif failure == "audit":
        rows.pop()
    elif failure == "missing_slug":
        rows[-1].pop("slug")  # actual Sept16 regression
    elif failure == "pattern":
        rows[-2].pop("pattern_engine")
    elif failure == "wrong_date":
        rows.append({"date": "2026-09-14", "slug": post.stem, "tier": 1})
    elif failure == "wrong_run":
        rows[-1]["run_id"] = "stale-run"
    elif failure == "wrong_revision":
        post.write_text(post.read_text() + "Changed after gates.\n")
    elif failure == "missing_agent":
        transcript.write_text("{}\n")
    elif failure == "blocked_gate":
        value = json.loads(sentinel.read_text())
        value["gates"]["build"] = "blocked"
        sentinel.write_text(json.dumps(value))
    elif failure == "historical_edit":
        rows[0] = {"tampered": True}
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)


def test_valid_run_and_duplicate_delivery(produced):
    repo, post, _, transcript = produced
    path = repo / contract.DECISIONS
    before = path.read_bytes()
    row = contract.records(path)[-1]
    contract.append_record(repo, DATE, post.stem, RUN, row)
    assert path.read_bytes() == before
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    row["agent_audit"] = {"writer": "docs-architect"}
    with pytest.raises(contract.ContractError, match="conflicting"):
        contract.append_record(repo, DATE, post.stem, RUN, row)


def test_wrong_target_append_is_transactionally_refused(produced):
    repo, post, _, _ = produced
    path = repo / contract.DECISIONS
    before = path.read_bytes()
    with pytest.raises(contract.ContractError):
        contract.append_record(
            repo,
            DATE,
            post.stem,
            RUN,
            {"date": "wrong", "slug": post.stem, "run_id": RUN, "tier": 1},
        )
    assert path.read_bytes() == before


def test_two_consecutive_representative_dates(produced):
    repo, post, sentinel, transcript = produced
    assert contract.validate(repo, DATE, RUN, transcript)["outcome"] == "complete"
    git(repo, "add", "content/posts", contract.DECISIONS)
    git(repo, "commit", "-qm", "offline first landing fixture")
    next_date, next_run = "2026-09-16", "offline-run-two"
    second = post.with_name("second-post.md")
    second.write_text(post.read_text().replace(DATE, next_date))
    for row in contract.records(repo / contract.DECISIONS)[-2:]:
        row.update(date=next_date, run_id=next_run, slug=second.stem)
        contract.append_record(repo, next_date, second.stem, next_run, row)
    value = json.loads(sentinel.read_text())
    value.update(
        date=next_date, run_id=next_run, slug=second.stem, post_sha256=contract.digest(second)
    )
    sentinel.with_name(f"{next_date}.intent.json").write_text(json.dumps(value))
    next_transcript = transcript.with_name(f"{next_run}.jsonl")
    transcript_rows = contract.records(transcript)
    for row in transcript_rows:
        row["sessionId"] = next_run
    next_transcript.write_text("\n".join(map(json.dumps, transcript_rows)))
    assert contract.validate(repo, next_date, next_run, next_transcript)["outcome"] == "complete"


@pytest.mark.parametrize("verdict", ["BLOCK", "REVISE", "missing", "old-revision"])
def test_actual_gate_block_cannot_be_overridden_by_ready_self_attestation(produced, verdict):
    repo, post, sentinel, transcript = produced
    post.write_text(post.read_text() + "\n```python\nprint(1)\n```\n")
    value = json.loads(sentinel.read_text())
    value["post_sha256"] = contract.digest(post)
    value["gates"]["code_review"] = "pass"
    sentinel.write_text(json.dumps(value))
    receipt = {
        "blog_gate_receipt": {
            "agent": "code-reviewer",
            "run_id": RUN,
            "date": DATE,
            "slug": post.stem,
            "post_sha256": contract.digest(post),
            "verdict": verdict,
        }
    }
    if verdict == "missing":
        receipt = {"prose": "Looks great. PASS."}
    elif verdict == "old-revision":
        receipt["blog_gate_receipt"].update(verdict="PASS", post_sha256="old-draft")
    rows = [
        {
            "sessionId": RUN,
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "name": "Agent",
                        "id": "code",
                        "input": {"subagent_type": "code-reviewer"},
                    }
                ]
            },
        },
        {
            "sessionId": RUN,
            "message": {
                "content": [
                    {"type": "tool_result", "tool_use_id": "code", "content": json.dumps(receipt)}
                ]
            },
        },
    ]
    with transcript.open("a") as output:
        output.write("\n" + "\n".join(map(json.dumps, rows)))
    with pytest.raises(contract.ContractError, match="gate|receipt"):
        contract.validate(repo, DATE, RUN, transcript)


@pytest.mark.parametrize("shape", ["string", "real-claude-text-blocks"])
def test_real_gate_pass_receipt_shape_and_binding(produced, shape):
    _, post, _, _ = produced
    identity = {"date": DATE, "slug": post.stem, "run_id": RUN}
    receipt = json.dumps(
        {
            "blog_gate_receipt": {
                **identity,
                "agent": "code-reviewer",
                "post_sha256": contract.digest(post),
                "verdict": "PASS",
            }
        }
    )
    post.write_text(post.read_text() + "\n~~~python\nprint(1)\n~~~\n")
    receipt = receipt.replace(
        json.loads(receipt)["blog_gate_receipt"]["post_sha256"], contract.digest(post)
    )
    result = receipt if shape == "string" else [{"type": "text", "text": receipt}]
    contract.validate_gate_receipts({"code-reviewer": result}, 1, post, identity)
    assert contract.contains_code(post)


@pytest.mark.parametrize("body", ["~~~python\nprint(1)\n~~~", "    print(1)", "\tprint(1)"])
def test_markdown_code_forms_require_code_review(produced, body):
    _, post, _, _ = produced
    post.write_text(post.read_text() + "\n" + body + "\n")
    assert "code-reviewer" in contract.required_agents(1, post, {"writer": "content-marketer"})


@pytest.mark.parametrize("field,value", [("schema_version", True), ("tier", True), ("gates", [])])
def test_readiness_schema_rejects_ambiguous_scalar_or_container_types(produced, field, value):
    repo, _, sentinel, transcript = produced
    obj = json.loads(sentinel.read_text())
    obj[field] = value
    sentinel.write_text(json.dumps(obj))
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)


@pytest.mark.parametrize("target", ["sentinel", "decision"])
def test_duplicate_json_keys_fail_before_publication(produced, target):
    repo, _, sentinel, transcript = produced
    if target == "sentinel":
        sentinel.write_text(
            sentinel.read_text().replace('"ready": true', '"ready": false,"ready": true')
        )
    else:
        path = repo / contract.DECISIONS
        path.write_text(path.read_text().replace('"tier": 1', '"tier": 2,"tier": 1'))
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)


def test_nonfinite_unscoped_metadata_is_refused_transactionally(produced):
    repo, post, _, _ = produced
    path = repo / contract.DECISIONS
    before = path.read_bytes()
    row = contract.records(path)[-1]
    row["run_id"] = RUN + "-nonfinite"
    row["metadata"] = {"bad": float("nan")}
    with pytest.raises(contract.ContractError):
        contract.append_record(repo, DATE, post.stem, row["run_id"], row)
    assert path.read_bytes() == before
