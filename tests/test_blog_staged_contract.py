"""Pre-append native coverage regressions; every provider/session is an offline fixture."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from blog_roles import historical_publication, restage_roles
from test_blog_publication_state import DATE, POST, RUN, SLUG, contract, git, workspace
from test_blog_publication_state import run as run

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/blog/blog-producer-contract.py"
SEO = {
    "seo-meta-optimizer",
    "seo-structure-architect",
    "seo-snippet-hunter",
    "seo-keyword-strategist",
}


@pytest.fixture
def staged(run, monkeypatch):
    monkeypatch.delenv("BLOG_RUN_MANIFEST", raising=False)
    authority = run["root"] / contract.DECISIONS
    classifier, audit = contract.records(authority)[-2:]
    authority.write_bytes(
        subprocess.check_output(
            ["git", "-C", str(run["root"]), "show", f"HEAD:{contract.DECISIONS}"]
        )
    )
    staging = run["root"] / ".blog-staging"
    classifier_file = staging / f"{DATE}.{RUN}.classifier.json"
    audit_file = staging / f"{DATE}.{RUN}.audit.json"
    classifier_file.write_text(json.dumps(classifier))
    audit_file.write_text(json.dumps(audit))
    (staging / f"{DATE}.intent.json").unlink()
    run.update(
        classifier=classifier,
        audit=audit,
        classifier_file=classifier_file,
        audit_file=audit_file,
        authority=authority,
    )
    return run


def restage(run):
    """Play the producer: stage role outputs for the fixture's current rows."""
    restage_roles(run["root"], run["transcript"], date=DATE, run_id=RUN, post=run["root"] / POST)


def remove_agents(run, names):
    rows = contract.records(run["transcript"])
    calls = {
        block["id"]
        for row in rows
        for block in row["message"]["content"]
        if block.get("type") == "tool_use" and block["input"]["subagent_type"] in names
    }
    rows = [
        row
        for row in rows
        if all(
            block.get("id", block.get("tool_use_id")) not in calls
            for block in row["message"]["content"]
        )
    ]
    run["transcript"].write_text("\n".join(map(json.dumps, rows)))
    restage(run)


def arguments(run, action, selected=None, script=SCRIPT):
    args = [
        sys.executable,
        str(script),
        action,
        "--repo",
        str(run["root"]),
        "--date",
        DATE,
        "--slug",
        SLUG,
        "--run-id",
        RUN,
        "--classifier-record",
        str(run["classifier_file"]),
        "--audit-record",
        str(run["audit_file"]),
        "--transcript",
        str(run["transcript"]),
    ]
    if selected:
        args += ["--record", str(run[f"{selected}_file"])]
    return args


def append(run, selected):
    return contract.append_record(
        run["root"],
        DATE,
        SLUG,
        RUN,
        run[selected],
        classifier_record=run["classifier"],
        audit_record=run["audit"],
        transcript=run["transcript"],
    )


def test_actual_old_append_admits_missing_tier2_seo_but_new_refuses(staged, tmp_path):
    remove_agents(staged, SEO)
    path = tmp_path / "old-contract.py"
    path.write_bytes(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "show", "90d1548:scripts/blog/blog-producer-contract.py"]
        )
    )
    before = staged["authority"].read_bytes()
    result = subprocess.run(
        [
            sys.executable,
            str(path),
            "append",
            "--repo",
            str(staged["root"]),
            "--date",
            DATE,
            "--slug",
            SLUG,
            "--run-id",
            RUN,
            "--record",
            str(staged["classifier_file"]),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    incorrectly_appended = staged["authority"].read_bytes()
    assert incorrectly_appended != before
    staged["authority"].write_bytes(before)  # disposable fixture only
    with pytest.raises(contract.ContractError, match="PENDING WORK") as error:
        append(staged, "classifier")
    assert all(name in str(error.value) for name in SEO)
    assert staged["authority"].read_bytes() == before
    (tmp_path / "old90-supported-cli-receipt.json").write_text(
        json.dumps(
            {
                "fixture_only": True,
                "old_source": "90d1548:scripts/blog/blog-producer-contract.py",
                "old_source_sha256": contract.digest(path),
                "old_supported_cli": result.args,
                "old_exit_code": result.returncode,
                "missing_agents": sorted(SEO),
                "baseline_authority_sha256": contract.hashlib.sha256(before).hexdigest(),
                "old_mutated_authority_sha256": contract.hashlib.sha256(
                    incorrectly_appended
                ).hexdigest(),
                "new_error": str(error.value),
                "new_authority_unchanged": staged["authority"].read_bytes() == before,
                "real_producer_artifacts_mutated": False,
            },
            indent=2,
        )
        + "\n"
    )


@pytest.mark.parametrize("selected", ["classifier", "audit"])
def test_neither_first_append_can_admit_incomplete_native_coverage(staged, selected):
    remove_agents(staged, SEO)
    before = staged["authority"].read_bytes()
    result = subprocess.run(arguments(staged, "append", selected), capture_output=True, text=True)
    assert result.returncode == 65
    assert "PENDING WORK" in result.stderr
    assert staged["authority"].read_bytes() == before


def test_second_append_and_duplicate_recheck_native_coverage(staged):
    append(staged, "classifier")
    before = staged["authority"].read_bytes()
    remove_agents(staged, {"seo-snippet-hunter"})
    for selected in ("audit", "classifier"):
        with pytest.raises(contract.ContractError, match="seo-snippet-hunter"):
            append(staged, selected)
        assert staged["authority"].read_bytes() == before


def test_check_staged_cli_is_readonly_and_actual_pair_appends_idempotently(staged, tmp_path):
    helpers = tmp_path / "readonly-helpers"
    helpers.mkdir()
    for name in ("blog-producer-contract.py", "blog_publication_state.py"):
        shutil.copyfile(ROOT / "scripts/blog" / name, helpers / name)
    # The shim imports this package from inside the run workspace, where a written
    # __pycache__ is a change outside the write-set. Copy it WITHOUT bytecode so the
    # before/after listing below proves the import itself writes none.
    shutil.copytree(
        ROOT / "scripts/blog/blogpipe",
        helpers / "blogpipe",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    script = helpers / "blog-producer-contract.py"
    before = staged["authority"].read_bytes()
    baseline_count = len(contract.records(staged["authority"]))
    owner_head = git(staged["owner"], "rev-parse", "HEAD")
    owner_file = staged["owner"] / "untracked-owner-note"
    owner_file.write_text("Pre-existing owner fixture; preserve.\n")
    owner_tracked = staged["owner"] / ".gitignore"
    owner_tracked.write_text(owner_tracked.read_text() + "preexisting-owner-only/\n")
    owner_tracked_bytes = owner_tracked.read_bytes()
    owner_status = git(staged["owner"], "status", "--porcelain")
    env = dict(os.environ)
    env.pop("PYTHONDONTWRITEBYTECODE", None)
    result = subprocess.run(
        arguments(staged, "check-staged", script=script), env=env, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["outcome"] == "staged-complete"
    assert staged["authority"].read_bytes() == before
    assert not (helpers / "__pycache__").exists()
    assert not (staged["root"] / f".blog-staging/{DATE}.intent.json").exists()
    for selected in ("classifier", "audit", "classifier", "audit"):
        result = subprocess.run(
            arguments(staged, "append", selected, script), env=env, capture_output=True, text=True
        )
        assert result.returncode == 0, result.stderr
    assert len(contract.records(staged["authority"])) == baseline_count + 2
    assert staged["authority"].read_bytes().startswith(before)
    assert contract.records(staged["authority"])[-2:] == [staged["classifier"], staged["audit"]]
    assert not (helpers / "__pycache__").exists()
    assert git(staged["owner"], "rev-parse", "HEAD") == owner_head
    assert git(staged["owner"], "status", "--porcelain") == owner_status
    assert owner_file.read_text() == "Pre-existing owner fixture; preserve.\n"
    assert owner_tracked.read_bytes() == owner_tracked_bytes


@pytest.mark.parametrize(
    "fault",
    [
        "identity",
        "hash",
        "pattern",
        "gates",
        "audit",
        "post",
        "draft",
        "missing-draft",
        "string-false",
    ],
)
def test_staged_invalid_pair_never_mutates_authority(staged, fault):
    if fault == "identity":
        staged["audit"]["slug"] = "foreign"
    elif fault == "hash":
        staged["audit"]["post_sha256"] = "0" * 64
    elif fault == "pattern":
        staged["classifier"]["pattern_engine"]["ruleset_digest"] = "obsolete"
    elif fault == "gates":
        staged["audit"]["gates"]["voice_lint"] = "blocked"
    elif fault == "audit":
        staged["audit"]["audit_addendum"] = False
    else:
        post = staged["root"] / POST
        replacement = {
            "post": post.read_text() + "Changed after actual fixture reviews.\n",
            "draft": post.read_text().replace("draft = false", "draft = true"),
            "missing-draft": post.read_text().replace("draft = false\n", ""),
            "string-false": post.read_text().replace("draft = false", 'draft = "false"'),
        }
        post.write_text(replacement[fault])
    before = staged["authority"].read_bytes()
    with pytest.raises(contract.ContractError):
        append(staged, "classifier")
    assert staged["authority"].read_bytes() == before


@pytest.mark.parametrize("verdict", ["BLOCK", "REVISE", "tool-error", "unfinished"])
def test_actual_gate_failure_or_unfinished_invocation_blocks_append(staged, verdict):
    rows = contract.records(staged["transcript"])
    call = next(
        block["id"]
        for row in rows
        for block in row["message"]["content"]
        if block.get("type") == "tool_use"
        and block["input"]["subagent_type"] == "blog-consistency-checker"
    )
    for row in rows:
        for block in row["message"]["content"]:
            if block.get("tool_use_id") == call:
                if verdict == "tool-error":
                    block["is_error"] = True
                elif verdict == "unfinished":
                    row["message"]["content"] = []
                else:
                    receipt = json.loads(block["content"][0]["text"])
                    receipt["blog_gate_receipt"]["verdict"] = verdict
                    block["content"][0]["text"] = json.dumps(receipt)
    staged["transcript"].write_text("\n".join(map(json.dumps, rows)))
    restage(staged)
    before = staged["authority"].read_bytes()
    with pytest.raises(contract.ContractError):
        append(staged, "classifier")
    assert staged["authority"].read_bytes() == before


def test_manifest_env_absence_cannot_bypass_staged_requirement(staged):
    before = staged["authority"].read_bytes()
    with pytest.raises(contract.ContractError, match="required before append"):
        contract.append_record(staged["root"], DATE, SLUG, RUN, staged["classifier"])
    result = subprocess.run(
        arguments(staged, "append", "classifier")[:-6], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert staged["authority"].read_bytes() == before


def test_bound_append_requires_inherited_held_run_lock(staged, monkeypatch):
    monkeypatch.setenv("BLOG_RUN_MANIFEST", str(staged["manifest"]))
    before = staged["authority"].read_bytes()
    with pytest.raises(contract.ContractError, match="producer lock"):
        append(staged, "classifier")
    with workspace.producer_lock(staged["manifest"].parent) as lock:
        result = subprocess.run(
            arguments(staged, "append", "classifier"),
            pass_fds=(lock.fileno(),),
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
    assert staged["authority"].read_bytes().startswith(before)


def test_changed_staged_counterpart_cannot_follow_first_append(staged):
    append(staged, "classifier")
    staged["classifier"]["reasoning"] = "Different classification authority after first append"
    before = staged["authority"].read_bytes()
    with pytest.raises(contract.ContractError, match="existing authority"):
        append(staged, "audit")
    assert staged["authority"].read_bytes() == before


def test_concurrent_pair_and_duplicate_deliveries_preserve_two_records(staged):
    before = staged["authority"].read_bytes()
    children = [
        subprocess.Popen(
            arguments(staged, "append", selected),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for selected in ("classifier", "audit", "classifier", "audit")
    ]
    for child in children:
        _, error = child.communicate(timeout=15)
        assert child.returncode == 0, error
    appended = staged["authority"].read_bytes()[len(before) :].decode().splitlines()
    assert len(appended) == 2
    assert {bool(json.loads(line).get("audit_addendum")) for line in appended} == {False, True}


def test_native_tool_child_with_closed_fds_requires_actual_ancestor_run_lease(staged, monkeypatch):
    monkeypatch.setenv("BLOG_RUN_MANIFEST", str(staged["manifest"]))
    with workspace.producer_lock(staged["manifest"].parent):
        result = subprocess.run(
            arguments(staged, "append", "classifier"),
            close_fds=True,
            capture_output=True,
            text=True,
        )
    assert result.returncode == 0, result.stderr


def test_unrelated_lease_owner_cannot_authorize_bound_append(staged, monkeypatch):
    monkeypatch.setenv("BLOG_RUN_MANIFEST", str(staged["manifest"]))
    lock = staged["manifest"].parent / "producer.lock"
    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import fcntl,sys; f=open(sys.argv[1],'a'); "
            "fcntl.flock(f,fcntl.LOCK_EX); print('fixture-held',flush=True); sys.stdin.read()",
            str(lock),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert child.stdout.readline().strip() == "fixture-held"
        before = staged["authority"].read_bytes()
        result = subprocess.run(
            arguments(staged, "append", "classifier"),
            close_fds=True,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 65
        assert "producer lock" in result.stderr
        assert staged["authority"].read_bytes() == before
    finally:
        child.communicate(timeout=5)


def bind_final_fixture_revision(run, *, preflight=False):
    """Rebind explicitly artificial fixture receipts; never used on real sessions."""
    post_hash = contract.digest(run["root"] / POST)
    sentinel_path = run["root"] / f".blog-staging/{DATE}.intent.json"
    sentinel = json.loads(sentinel_path.read_text())
    sentinel.update(post_sha256=post_hash, ready=not preflight)
    sentinel_path.write_text(json.dumps(sentinel))
    transcript = contract.records(run["transcript"])
    for row in transcript:
        for block in row["message"]["content"]:
            if block.get("type") == "tool_result":
                for text in block["content"]:
                    receipt = json.loads(text["text"])
                    receipt["blog_gate_receipt"]["post_sha256"] = post_hash
                    text["text"] = json.dumps(receipt)
    run["transcript"].write_text("\n".join(map(json.dumps, transcript)))
    restage(run)
    authority = run["root"] / contract.DECISIONS
    rows = contract.records(authority)
    for row in rows:
        if row.get("audit_addendum"):
            row["post_sha256"] = post_hash
    # Deliberate direct JSONL write models append bypass, only in this fixture.
    authority.write_text("".join(json.dumps(row) + "\n" for row in rows))


def verify_arguments(run, script=SCRIPT, *, preflight=False):
    args = [
        sys.executable,
        str(script),
        "verify",
        "--repo",
        str(run["root"]),
        "--date",
        DATE,
        "--run-id",
        RUN,
        "--transcript",
        str(run["transcript"]),
    ]
    return args + (["--preflight"] if preflight else [])


@pytest.mark.parametrize("preflight", [False, True])
@pytest.mark.parametrize("fault", ["string-false", "missing-draft", "wrong-slug"])
def test_normal_cli_requires_same_strict_publication_fields_as_staged(
    run, tmp_path, fault, preflight
):
    post = run["root"] / POST
    if fault == "string-false":
        post.write_text(post.read_text().replace("draft = false", 'draft = "false"'))
    elif fault == "missing-draft":
        post.write_text(post.read_text().replace("draft = false\n", ""))
    else:
        post.write_text(post.read_text().replace(f"slug = '{SLUG}'", "slug = 'foreign-slug'"))
    bind_final_fixture_revision(run, preflight=preflight)
    old = tmp_path / "old-951-contract.py"
    old.write_bytes(
        subprocess.check_output(
            ["git", "-C", str(ROOT), "show", "951f5911:scripts/blog/blog-producer-contract.py"]
        )
    )
    historical_publication(ROOT, "951f5911", old.parent / "blog_publication_state.py")
    old_result = subprocess.run(
        verify_arguments(run, old, preflight=preflight), capture_output=True, text=True
    )
    assert old_result.returncode == 0, old_result.stderr
    assert json.loads(old_result.stdout)["outcome"] == (
        "preflight-complete" if preflight else "complete"
    )
    authority = run["root"] / contract.DECISIONS
    before = authority.read_bytes()
    repaired = subprocess.run(
        verify_arguments(run, preflight=preflight), capture_output=True, text=True
    )
    assert repaired.returncode == 65
    assert not repaired.stdout
    assert authority.read_bytes() == before
    (tmp_path / "old951-normal-verify-receipt.json").write_text(
        json.dumps(
            {
                "fixture_only": True,
                "fault": fault,
                "preflight": preflight,
                "old_source": "951f5911:scripts/blog/blog-producer-contract.py",
                "old_source_sha256": contract.digest(old),
                "old_supported_cli": old_result.args,
                "old_exit_code": old_result.returncode,
                "old_completion": json.loads(old_result.stdout),
                "repaired_exit_code": repaired.returncode,
                "repaired_error": repaired.stderr.strip(),
                "authority_unchanged": authority.read_bytes() == before,
                "real_producer_artifacts_mutated": False,
            },
            indent=2,
        )
        + "\n"
    )


@pytest.mark.parametrize("preflight", [False, True])
def test_normal_cli_preserves_valid_plain_yaml_false(run, preflight):
    post = run["root"] / POST
    body = post.read_text().split("\n+++\n", 1)[1]
    post.write_text(
        f"---\ntitle: Offline fixture\nslug: {SLUG}\ndate: {DATE}T08:00:00-06:00\n"
        f"draft: false\n---\n{body}"
    )
    bind_final_fixture_revision(run, preflight=preflight)
    result = subprocess.run(
        verify_arguments(run, preflight=preflight), capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["outcome"] == (
        "preflight-complete" if preflight else "complete"
    )
