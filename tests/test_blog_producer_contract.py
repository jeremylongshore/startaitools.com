"""Offline regression replay of Sept15/16 semantic completion failures."""

import importlib.util
import json
import os
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


@pytest.mark.parametrize("draft", ["true", '"true"', "1"])
@pytest.mark.parametrize("preflight", [False, True])
def test_final_draft_refused_before_readiness_or_gate_receipts(produced, draft, preflight):
    repo, post, _, transcript = produced
    post.write_text(post.read_text().replace("+++\n", f"+++\ndraft = {draft}\n", 1))
    with pytest.raises(contract.ContractError, match="remains a draft"):
        contract.validate(repo, DATE, RUN, transcript, preflight=preflight)


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


@pytest.mark.parametrize('changed', ['date', 'slug'])
def test_committed_run_identity_cannot_change(produced, changed):
    repo, post, _, _ = produced
    path = repo / contract.DECISIONS
    before = path.read_bytes()
    row = dict(contract.records(path)[-2])
    row[changed] = '2026-09-16' if changed == 'date' else 'renamed-after-append'
    with pytest.raises(contract.ContractError, match='identity already committed'):
        contract.append_record(repo, row['date'], row['slug'], RUN, row)
    assert path.read_bytes() == before


@pytest.mark.parametrize('failure', ['date', 'run_id', 'workspace', 'sealed', 'post_slug'])
def test_append_respects_real_run_binding(produced, tmp_path, monkeypatch, failure):
    repo, post, _, _ = produced
    path = repo / contract.DECISIONS
    before = path.read_bytes()
    row = dict(contract.records(path)[-1])
    manifest = {'workspace': str(repo), 'date': DATE, 'run_id': RUN, 'status': 'ready'}
    if failure == 'sealed':
        manifest['status'] = 'sealed'
    elif failure == 'post_slug':
        row['slug'] = 'wrong-final-post'
    else:
        manifest[failure] = str(tmp_path) if failure == 'workspace' else 'foreign'
    binding = tmp_path / 'manifest.json'
    binding.write_text(json.dumps(manifest))
    monkeypatch.setenv('BLOG_RUN_MANIFEST', str(binding))
    with pytest.raises(contract.ContractError):
        contract.append_record(repo, DATE, row['slug'], RUN, row)
    assert path.read_bytes() == before


def test_staged_slug_revision_is_committed_only_after_final_identity(produced):
    repo, post, sentinel, transcript = produced
    path = repo / contract.DECISIONS
    rows = contract.records(path)[-2:]
    baseline = git(repo, 'show', f'HEAD:{contract.DECISIONS}').stdout
    path.write_bytes(baseline)
    staging = repo / '.blog-staging' / f'{DATE}.{RUN}.classifier.json'
    staging.write_text(json.dumps(rows[0]))
    final = post.with_name('final-voice-approved-slug.md')
    post.rename(final)
    for row in rows:
        row['slug'] = final.stem
        contract.append_record(repo, DATE, final.stem, RUN, row)
    value = json.loads(sentinel.read_text())
    value.update(slug=final.stem, post_sha256=contract.digest(final), ready=False)
    sentinel.write_text(json.dumps(value))
    receipt = contract.validate(repo, DATE, RUN, transcript, preflight=True)
    assert receipt['outcome'] == 'preflight-complete'
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript)
    value['ready'] = True
    sentinel.write_text(json.dumps(value))
    assert contract.validate(repo, DATE, RUN, transcript)['outcome'] == 'complete'
    assert path.read_bytes().startswith(baseline)
    assert all(row['slug'] == final.stem for row in contract.records(path)[-2:])


@pytest.mark.parametrize('missing', ['audit', 'pattern', 'gate', 'transcript', 'revision'])
def test_preflight_preserves_every_other_completion_gate(produced, missing):
    repo, post, sentinel, transcript = produced
    value = json.loads(sentinel.read_text())
    value['ready'] = False
    if missing == 'gate':
        value['gates']['build'] = 'blocked'
    elif missing == 'revision':
        value['post_sha256'] = '0' * 64
    sentinel.write_text(json.dumps(value))
    if missing in ('audit', 'pattern'):
        path = repo / contract.DECISIONS
        rows = contract.records(path)
        if missing == 'audit':
            rows = rows[:-1]
        else:
            rows[-2]['pattern_engine']['ran'] = False
        path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    if missing == 'transcript':
        transcript.unlink()
    with pytest.raises(contract.ContractError):
        contract.validate(repo, DATE, RUN, transcript, preflight=True)


def test_preflight_cli_is_read_only_and_never_final_readiness(produced):
    repo, _, sentinel, transcript = produced
    value = json.loads(sentinel.read_text())
    value['ready'] = False
    sentinel.write_text(json.dumps(value))
    before = sentinel.read_bytes()
    command = ['python3', str(ROOT / 'scripts/blog/blog-producer-contract.py'), 'verify',
               '--repo', str(repo), '--date', DATE, '--run-id', RUN,
               '--transcript', str(transcript)]
    assert subprocess.run(command, capture_output=True).returncode == 65
    result = subprocess.run([*command, '--preflight'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['outcome'] == 'preflight-complete'
    assert sentinel.read_bytes() == before


@pytest.mark.parametrize('escape', ['file', 'directory'])
def test_append_cannot_mutate_symlinked_authority(produced, tmp_path, escape):
    repo, post, _, _ = produced
    path = repo / contract.DECISIONS
    outside = tmp_path / 'unrelated-authority'
    if escape == 'file':
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
        protected = outside
    else:
        shutil.move(str(path.parent), outside)
        path.parent.symlink_to(outside, target_is_directory=True)
        protected = outside / 'decisions.jsonl'
    before = protected.read_bytes()
    row = {'date': DATE, 'slug': post.stem, 'run_id': 'fresh-fixture-run', 'tier': 1}
    with pytest.raises(contract.ContractError, match='symlink'):
        contract.append_record(repo, DATE, post.stem, row['run_id'], row)
    assert protected.read_bytes() == before


def test_cli_frontmatter_verification_does_not_write_helper_bytecode(produced, tmp_path):
    repo, _, _, transcript = produced
    helpers = tmp_path / "readonly-helpers"
    helpers.mkdir()
    for name in ("blog-producer-contract.py", "blog_publication_state.py"):
        shutil.copyfile(ROOT / "scripts/blog" / name, helpers / name)
    before = sorted(p.relative_to(helpers) for p in helpers.rglob("*"))
    result = subprocess.run(
        [
            "python3",
            str(helpers / "blog-producer-contract.py"),
            "verify",
            "--repo",
            str(repo),
            "--date",
            DATE,
            "--run-id",
            RUN,
            "--transcript",
            str(transcript),
        ],
        capture_output=True,
        text=True,
        env={k: v for k, v in os.environ.items() if k != "PYTHONDONTWRITEBYTECODE"},
    )
    assert result.returncode == 0, result.stderr
    assert sorted(p.relative_to(helpers) for p in helpers.rglob("*")) == before

