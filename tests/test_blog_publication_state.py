"""Real Git/filesystem crash replay with offline Agent, Hugo and HTTP fixtures."""

from __future__ import annotations

import importlib.util
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "publication", ROOT / "scripts/blog/blog_publication_state.py"
)
publication = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publication)
workspace = publication.module("blog-run-workspace")
contract = publication.module("blog-producer-contract")
DATE, RUN, SLUG = "2026-09-16", "offline-delivery-run", "delivery-fixture"
POST = f"content/posts/{SLUG}.md"


def git(repo, *args):
    env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True, env=env
    ).stdout.strip()


@pytest.fixture
def run(tmp_path):
    remote, owner = tmp_path / "remote.git", tmp_path / "owner"
    git(tmp_path, "init", "--bare", "--initial-branch=master", str(remote))
    git(tmp_path, "clone", str(remote), str(owner))
    git(owner, "config", "user.name", "Offline fixture")
    git(owner, "config", "user.email", "fixture@example.invalid")
    (owner / "content/posts").mkdir(parents=True)
    (owner / ".gitignore").write_text(
        ".blog-staging/\npublic/\n.hugo_build.lock\n.blog-publication-state.lock\n"
        ".blog-syndication-ledger.json\n.crosspost-queue.json\n"
    )
    method = owner / Path(contract.DECISIONS).parent
    method.mkdir(parents=True)
    (method / "decisions.jsonl").write_text("{}\n")
    (method / "patterns.jsonl").write_text("")
    scripts = method.parent / "scripts"
    scripts.mkdir()
    for name in ("apply-patterns.py", "lint-post-voice.py", "voice-denylist.json"):
        shutil.copy(ROOT / ".claude/skills/blog-backfill/scripts" / name, scripts / name)
    git(owner, "add", ".")
    git(owner, "commit", "-m", "offline baseline")
    git(owner, "push", "origin", "master")
    git(owner, "remote", "set-head", "origin", "master")
    args = type(
        "Args",
        (),
        {
            "repo": owner,
            "expected_remote": str(remote),
            "date": DATE,
            "run_id": RUN,
            "state_dir": tmp_path / "state",
            "recover_abandoned": False,
        },
    )()
    created = workspace.create(args)
    manifest_path, root = Path(created["manifest"]), Path(created["workspace"])
    (root / "content/posts").mkdir(parents=True, exist_ok=True)
    post = root / POST
    post.write_text(
        f"+++\ntitle = 'Offline delivery fixture'\nslug = '{SLUG}'\n"
        f"date = {DATE}T08:00:00-06:00\ndraft = false\n+++\n" + "A recorded observation.\n" * 150
    )
    identity = {"date": DATE, "run_id": RUN, "slug": SLUG}
    rules = subprocess.run(
        [
            sys.executable,
            str(root / ".claude/skills/blog-backfill/scripts/apply-patterns.py"),
            "digest",
        ],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    classifier = {
        **identity,
        "tier": 2,
        "tier_name": "Technical Deep-Dive",
        "confidence": 0.8,
        "dimensions": dict.fromkeys(("novelty", "arc", "nar", "tch", "scp", "rpr"), 2),
        "pattern_engine": {"ran": True, "ruleset_digest": rules},
    }
    audit = {**identity, "audit_addendum": True, "agent_audit": {"writer": "content-marketer"}}
    (root / ".blog-staging").mkdir()
    sentinel = {
        **identity,
        "tier": 2,
        "schema_version": 1,
        "ready": True,
        "post_sha256": publication.sha(post.read_bytes()),
        "gates": dict.fromkeys(("build", "voice_lint", "consistency"), "pass"),
    }
    (root / f".blog-staging/{DATE}.intent.json").write_text(json.dumps(sentinel))
    transcript = tmp_path / f"{RUN}.jsonl"
    rows = []
    for i, agent in enumerate(sorted(contract.required_agents(2, post, audit["agent_audit"]))):
        receipt = {
            "blog_gate_receipt": {
                **identity,
                "agent": agent,
                "verdict": "PASS",
                "post_sha256": sentinel["post_sha256"],
            }
        }
        rows += [
            {
                "sessionId": RUN,
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Agent",
                            "id": str(i),
                            "input": {"subagent_type": agent},
                        }
                    ]
                },
            },
            {
                "sessionId": RUN,
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": str(i),
                            "content": [{"type": "text", "text": json.dumps(receipt)}],
                        }
                    ]
                },
            },
        ]
    transcript.write_text("\n".join(map(json.dumps, rows)))
    audit.update(post_sha256=sentinel["post_sha256"], gates=sentinel["gates"])
    for row in (classifier, audit):
        contract.append_record(
            root,
            DATE,
            SLUG,
            RUN,
            row,
            classifier_record=classifier,
            audit_record=audit,
            transcript=transcript,
        )
    hugo = tmp_path / "hugo-offline-fixture"
    hugo.write_text('#!/bin/sh\nprintf "hugo v0.150.0 offline fixture\\n"\n')
    hugo.chmod(0o755)
    return {
        "manifest": manifest_path,
        "root": root,
        "owner": owner,
        "transcript": transcript,
        "hugo": str(hugo),
    }


def seal(run):
    return publication.seal_quality(run["manifest"], run["transcript"], run["hugo"])


def publish(run, *, complete=True):
    git(run["root"], "add", POST, contract.DECISIONS)
    git(run["root"], "commit", "-m", "post: genuine offline quality fixture")
    git(run["root"], "push", "origin", "HEAD:refs/heads/master")
    if complete:
        workspace.complete(run["manifest"])


def reconcile(run, **kwargs):
    return publication.reconcile_delivery(run["manifest"], public_check=lambda _url: None, **kwargs)


def test_exact_quality_seal_survives_commit_and_restores_both_rows(run):
    assert seal(run)["outcome"] == "sealed"
    saved = json.loads(run["manifest"].read_text())
    assert saved["delivery_status"] == "pending"
    assert saved["status"] == "sealed"
    publish(run)
    original_time = json.loads(run["manifest"].read_text())["published_at"]
    # Original session and sentinel need not remain available after successful sealing.
    run["transcript"].unlink()
    (run["root"] / f".blog-staging/{DATE}.intent.json").unlink()
    assert reconcile(run)["ledger_inserted"] is True
    ledger = publication.load_state(run["owner"] / ".blog-syndication-ledger.json")
    queue = publication.load_state(run["owner"] / ".crosspost-queue.json")
    assert len(ledger) == len(queue) == 1
    assert ledger[0]["published_at"] == queue[0]["published_at"] == original_time
    assert ledger[0]["publication_timestamp_source"] == "source-observed"
    assert ledger[0]["date"] == DATE
    assert ledger[0]["tier"] == 2
    assert json.loads(run["manifest"].read_text())["delivery_status"] == "complete"


def test_crash_after_remote_push_is_recovered_with_original_quality_seal(run):
    seal(run)
    publish(run, complete=False)
    workspace.recover_abandoned(run["manifest"], workspace.load(run["manifest"]))
    assert reconcile(run)["queue_inserted"] is True
    assert json.loads(run["manifest"].read_text())["recovered_abandoned"] is True


def test_actual_process_kill_between_ledger_and_queue_is_idempotently_recovered(run):
    seal(run)
    publish(run)

    def child():
        reconcile(run, after_ledger=lambda: os._exit(73))

    process = multiprocessing.get_context("fork").Process(target=child)
    process.start()
    process.join(timeout=10)
    assert process.exitcode == 73
    ledger_path = run["owner"] / ".blog-syndication-ledger.json"
    queue_path = run["owner"] / ".crosspost-queue.json"
    assert len(publication.load_state(ledger_path)) == 1
    assert not queue_path.exists()
    assert json.loads(run["manifest"].read_text())["delivery_status"] == "pending"
    assert reconcile(run) == {
        "outcome": "delivery-complete",
        "ledger_inserted": False,
        "queue_inserted": True,
        "run_id": RUN,
    }
    assert len(publication.load_state(ledger_path)) == len(publication.load_state(queue_path)) == 1


def test_repeated_delivery_preserves_packet_and_platform_status(run):
    seal(run)
    publish(run)
    reconcile(run)
    ledger = run["owner"] / ".blog-syndication-ledger.json"
    queue = run["owner"] / ".crosspost-queue.json"
    publication.update_row(
        ledger,
        SLUG,
        {
            "packet_sent": True,
            "image": {"provider": "fixture"},
            "syndication": {"x": {"status": "posted"}},
        },
    )
    publication.update_row(
        queue, SLUG, {"devto": {"status": "published", "url": "https://example.invalid/p"}}
    )
    before = ledger.read_bytes(), queue.read_bytes()
    assert reconcile(run)["ledger_inserted"] is False
    assert (ledger.read_bytes(), queue.read_bytes()) == before
    observed_at = json.loads(run["manifest"].read_text())["published_at"]
    (run["root"] / f".blog-staging/{DATE}.intent.json").unlink()
    workspace.complete(run["manifest"])
    assert json.loads(run["manifest"].read_text())["published_at"] == observed_at


@pytest.mark.parametrize("failure", ["build", "voice", "agent", "sentinel", "changed-post"])
def test_no_quality_seal_without_independent_gates(run, failure):
    if failure == "build":
        Path(run["hugo"]).write_text("#!/bin/sh\nexit 1\n")
    elif failure == "voice":
        post = run["root"] / POST
        previous = publication.sha(post.read_bytes())
        post.write_text(post.read_text() + "An em—dash fails the actual independent voice lint.\n")
        current = publication.sha(post.read_bytes())
        sentinel = run["root"] / f".blog-staging/{DATE}.intent.json"
        sentinel.write_text(sentinel.read_text().replace(previous, current))
        run["transcript"].write_text(run["transcript"].read_text().replace(previous, current))
    elif failure == "agent":
        run["transcript"].write_text("{}\n")
    elif failure == "sentinel":
        (run["root"] / f".blog-staging/{DATE}.intent.json").unlink()
    else:
        post = run["root"] / POST
        post.write_text(post.read_text() + "Changed without review.\n")
    with pytest.raises((ValueError, workspace.WorkspaceError)):
        seal(run)
    assert not (run["manifest"].parent / "quality-seal.json").exists()
    assert not (run["owner"] / ".blog-syndication-ledger.json").exists()


@pytest.mark.parametrize("failure", ["seal", "proof", "remote", "public", "ledger", "queue"])
def test_recovery_failure_remains_pending_without_replacing_good_state(run, failure):
    seal(run)
    publish(run)
    ledger = run["owner"] / ".blog-syndication-ledger.json"
    queue = run["owner"] / ".crosspost-queue.json"
    ledger.write_text('[{"slug":"unrelated","packet_sent":true}]\n')
    before = ledger.read_bytes()
    if failure == "seal":
        (run["manifest"].parent / "quality-seal.json").unlink()
    elif failure == "proof":
        (run["manifest"].parent / "quality-proof/sentinel.json").write_text("{}")
    elif failure == "remote":
        post = run["root"] / POST
        post.write_text(post.read_text() + "Unreviewed remote correction.\n")
        git(run["root"], "add", POST)
        git(run["root"], "commit", "-m", "unreviewed correction")
        git(run["root"], "push", "origin", "HEAD:refs/heads/master")
    elif failure == "ledger":
        ledger.write_text("broken-state")
        before = ledger.read_bytes()
    elif failure == "queue":
        queue.write_text("broken-state")

    def unavailable(_url):
        raise publication.PublicationError("offline public outage fixture")

    with pytest.raises(ValueError):
        publication.reconcile_delivery(
            run["manifest"],
            public_check=(unavailable if failure == "public" else lambda _url: None),
        )
    failed = json.loads(run["manifest"].read_text())
    assert failed["delivery_status"] == "pending"
    assert failed["delivery_error_detail"]
    if failure == "remote":
        assert failed["delivery_error_detail"] == "remote article changed since this quality seal"
    if failure != "queue":
        assert ledger.read_bytes() == before
    else:
        assert queue.read_text() == "broken-state"
        assert publication.load_state(ledger)[0] == {"slug": "unrelated", "packet_sent": True}


def test_failure_detail_never_promotes_arbitrary_exception_content():
    private = "fixture-credential-must-never-appear"
    for error in (publication.PublicationError(private), OSError(private), ValueError(private)):
        assert private not in publication.failure_detail(error)


def test_legacy_source_without_quality_seal_never_creates_delivery_rows(run):
    publish(run, complete=False)
    manifest = json.loads(run["manifest"].read_text())
    manifest.pop("requires_quality_seal")  # Explicitly model a retained pre-seal legacy manifest.
    workspace.atomic_json(run["manifest"], manifest)
    workspace.complete(run["manifest"])
    with pytest.raises(publication.PublicationError, match="quality seal missing"):
        reconcile(run)
    assert not (run["owner"] / ".blog-syndication-ledger.json").exists()


def test_canary_never_creates_quality_or_delivery_state(run, monkeypatch):
    monkeypatch.setenv("BLOG_CANARY", "1")
    for action in (lambda: seal(run), lambda: reconcile(run)):
        with pytest.raises(publication.PublicationError, match="canary"):
            action()
    assert not (run["manifest"].parent / "quality-seal.json").exists()
    assert not (run["owner"] / ".blog-publication-state.lock").exists()


def test_shared_lock_refuses_overlap_and_releases_after_process_death(tmp_path):
    with publication.state_locked(tmp_path):
        with pytest.raises(publication.PublicationError, match="lock timed out"):
            with publication.state_locked(tmp_path, timeout=0.01):
                pytest.fail("overlapping lock admitted")
    with publication.state_locked(tmp_path, timeout=0.01):
        pass


def test_legacy_missing_delivery_is_visible_without_manufacturing_rows(run):
    with pytest.raises(publication.PublicationError, match="delivery identity"):
        publication.check_existing(run["manifest"], SLUG)
    assert not (run["owner"] / ".blog-syndication-ledger.json").exists()


def test_startup_recovers_pending_delivery_and_repeated_date_is_noop(run, monkeypatch):
    seal(run)
    publish(run)
    # Production proves canonical inherited FD9; this isolated registry test
    # patches that boundary only, never touching the actual host pipeline lock.
    monkeypatch.setattr(workspace, "verify_pipeline_lock", lambda: None)
    actual = publication.reconcile_delivery
    monkeypatch.setattr(
        publication, "reconcile_delivery", lambda path: actual(path, public_check=lambda _url: None)
    )
    assert publication.recover_deliveries(run["manifest"])["runs"] == 1
    ledger = run["owner"] / ".blog-syndication-ledger.json"
    queue = run["owner"] / ".crosspost-queue.json"
    before = ledger.read_bytes(), queue.read_bytes()
    assert publication.recover_deliveries(run["manifest"])["runs"] == 0
    assert (ledger.read_bytes(), queue.read_bytes()) == before
    assert (
        publication.check_existing(run["manifest"], SLUG)["outcome"] == "existing-delivery-present"
    )


@pytest.mark.parametrize(
    "contents",
    ['[{"slug":"x","packet_sent":false,"packet_sent":true}]', '[{"slug":"x","attempts":NaN}]'],
)
def test_corrupt_state_is_preserved_and_never_treated_as_empty(tmp_path, contents):
    path = tmp_path / ".blog-syndication-ledger.json"
    path.write_text(contents)
    with pytest.raises(publication.PublicationError):
        publication.update_row(path, "x", {"packet_sent": True})
    assert path.read_text() == contents


def test_canary_direct_shared_writer_apis_cannot_mutate(tmp_path, monkeypatch):
    path = tmp_path / ".blog-syndication-ledger.json"
    path.write_text('[{"slug":"fixture","packet_sent":false}]')
    before = path.read_bytes()
    monkeypatch.setenv("BLOG_CANARY", "1")
    with pytest.raises(publication.PublicationError, match="canary"):
        publication.update_row(path, "fixture", {"packet_sent": True})
    with pytest.raises(publication.PublicationError, match="canary"):
        publication.atomic_state(path, [])
    with pytest.raises(publication.PublicationError, match="canary"):
        with publication.state_locked(tmp_path):
            pytest.fail("canary acquired mutating transaction")
    assert path.read_bytes() == before
    assert not (tmp_path / ".blog-publication-state.lock").exists()


def test_sealed_run_refuses_second_producer_and_genuine_candidate_passes(run):
    seal(run)
    before = (run["root"] / POST).read_bytes()
    with pytest.raises(workspace.WorkspaceError, match="sealed"):
        workspace.run_producer(run["manifest"], ["/bin/sh", "-c", f"echo changed >> {POST}"])
    assert (run["root"] / POST).read_bytes() == before
    git(run["root"], "add", POST, contract.DECISIONS)
    git(run["root"], "commit", "-m", "sealed candidate")
    assert workspace.publication_check(workspace.load(run["manifest"]))["push_refspec"] == (
        "HEAD:refs/heads/master"
    )


@pytest.mark.parametrize("artifact", ["post", "decisions", "sentinel"])
def test_sealed_revision_tampering_is_rejected_before_push(run, artifact):
    seal(run)
    if artifact == "post":
        path = run["root"] / POST
        path.write_text(path.read_text() + "Changed after seal.\n")
    elif artifact == "decisions":
        with (run["root"] / contract.DECISIONS).open("a") as stream:
            stream.write(
                json.dumps({"date": DATE, "slug": SLUG, "run_id": RUN, "unreviewed": True}) + "\n"
            )
    else:
        path = run["root"] / f".blog-staging/{DATE}.intent.json"
        value = json.loads(path.read_text())
        value["ready"] = False
        path.write_text(json.dumps(value))
    git(run["root"], "add", POST, contract.DECISIONS)
    git(run["root"], "commit", "-m", "tampered candidate")
    remote_before = git(run["root"], "ls-remote", "origin", "refs/heads/master")
    with pytest.raises(workspace.WorkspaceError, match="quality seal"):
        workspace.publication_check(workspace.load(run["manifest"]))
    assert git(run["root"], "ls-remote", "origin", "refs/heads/master") == remote_before


def test_new_unsealed_candidate_cannot_use_publication_helper(run):
    assert json.loads(run["manifest"].read_text())["requires_quality_seal"] is True
    git(run["root"], "add", POST, contract.DECISIONS)
    git(run["root"], "commit", "-m", "unsealed candidate")
    for action in (
        lambda: workspace.publication_check(workspace.load(run["manifest"])),
        lambda: workspace.complete(run["manifest"]),
    ):
        with pytest.raises(workspace.WorkspaceError, match="quality seal"):
            action()


@pytest.mark.parametrize(
    "failure", ["partial-ledger", "conflicting-ledger", "partial-queue", "state-typo"]
)
def test_incomplete_or_conflicting_target_rows_never_mark_delivery_complete(run, failure):
    seal(run)
    publish(run)
    reconcile(run)
    path = run["owner"] / (
        ".crosspost-queue.json" if failure == "partial-queue" else ".blog-syndication-ledger.json"
    )
    rows = publication.load_state(path)
    if failure.startswith("partial"):
        rows = [{"slug": SLUG, "packet_sent": False, "image": {"fixture": True}}]
    elif failure == "conflicting-ledger":
        rows[0]["date"] = "2026-09-15"
    else:
        rows[0]["syndication"]["x"]["status"] = "pending-typo"
    path.write_text(json.dumps(rows))
    before = path.read_bytes()
    with pytest.raises(publication.PublicationError):
        reconcile(run)
    assert path.read_bytes() == before
    assert json.loads(run["manifest"].read_text())["delivery_status"] == "pending"


def test_old_changed_publication_does_not_pause_new_date_producer(run, monkeypatch):
    seal(run)
    publish(run)
    post = run["root"] / POST
    post.write_text(post.read_text() + "Legitimate separately published correction.\n")
    git(run["root"], "add", POST)
    git(run["root"], "commit", "-m", "separate correction after original publication")
    git(run["root"], "push", "origin", "HEAD:refs/heads/master")
    old = json.loads(run["manifest"].read_text())
    args = type(
        "Args",
        (),
        {
            "repo": run["owner"],
            "expected_remote": old["remote_url"],
            "date": "2026-09-17",
            "run_id": "new-independent-date",
            "state_dir": run["manifest"].parents[4],
            "recover_abandoned": False,
        },
    )()
    new = workspace.create(args)
    monkeypatch.setattr(workspace, "verify_pipeline_lock", lambda: None)
    result = publication.recover_deliveries(Path(new["manifest"]))
    assert result["outcome"] == "degraded" and result["failures"][0]["run_id"] == RUN
    assert json.loads(run["manifest"].read_text())["delivery_status"] == "pending"
    assert (
        workspace.run_producer(Path(new["manifest"]), ["/bin/sh", "-c", "exit 0"])["exit_code"] == 0
    )
    assert not (run["owner"] / ".blog-syndication-ledger.json").exists()
