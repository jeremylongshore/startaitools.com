"""Durable producer outcome gates, using real children and disposable Git runs."""

import importlib.util
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest
from test_blog_publication_state import ROOT, publication, publish, seal, workspace
from test_blog_publication_state import run as run


def failed_child(run):
    result = workspace.run_producer(run["manifest"], [sys.executable, "-c", "exit(143)"])
    assert result["exit_code"] == 143


def assert_seal_refused_unchanged(run):
    before = run["manifest"].read_bytes()
    with pytest.raises(publication.PublicationError, match="producer|terminal|ready"):
        seal(run)
    assert run["manifest"].read_bytes() == before
    assert not (run["manifest"].parent / "quality-proof").exists()
    assert not (run["manifest"].parent / "quality-seal.json").exists()


def test_nonzero_completion_before_quarantine_cannot_seal_valid_artifacts(run):
    failed_child(run)
    assert json.loads(run["manifest"].read_text())["status"] == "ready"
    assert_seal_refused_unchanged(run)


def test_direct_seal_cannot_replace_rejected_quarantine(run):
    failed_child(run)
    workspace.quarantine(run["manifest"], "offline rejected producer fixture")
    manifest = json.loads(run["manifest"].read_text())
    saved = sorted((p.relative_to(Path(manifest["quarantine"])).as_posix(), p.read_bytes())
                   for p in Path(manifest["quarantine"]).rglob("*") if p.is_file())
    assert_seal_refused_unchanged(run)
    assert sorted((p.relative_to(Path(manifest["quarantine"])).as_posix(), p.read_bytes())
                  for p in Path(manifest["quarantine"]).rglob("*") if p.is_file()) == saved


@pytest.mark.parametrize("field,value", [
    ("exit_code", False), ("exit_code", 0.0), ("exit_code", "0"),
    ("schema_version", True), ("state", "running"), ("attempt_id", "wrong"),
    ("run_id", "other-run"), ("date", "2026-09-15"),
    ("baseline_sha", "0" * 40), ("finished_at", None),
])
def test_malformed_or_unbound_completion_cannot_seal(run, field, value):
    manifest = json.loads(run["manifest"].read_text())
    # Historical runners recorded no outcome. Supplying a corrupt fixture here
    # also proves the old seal ignored the entire boundary.
    attempt = manifest.setdefault("producer_attempt", {})
    attempt[field] = value
    workspace.atomic_json(run["manifest"], manifest)
    assert_seal_refused_unchanged(run)


def test_missing_completion_is_not_inferred_from_valid_artifacts(run):
    manifest = json.loads(run["manifest"].read_text())
    manifest.pop("producer_attempt", None)
    workspace.atomic_json(run["manifest"], manifest)
    assert_seal_refused_unchanged(run)


def test_successful_process_still_requires_complete_contract(run):
    path = run["root"] / ".blog-staging/2026-09-16.intent.json"
    value = json.loads(path.read_text())
    value["ready"] = False
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="ready"):
        seal(run)
    assert not (run["manifest"].parent / "quality-seal.json").exists()


def test_runner_crash_replaces_prior_success_with_unfinished_attempt(run):
    started = run["manifest"].parent / "child-started-fixture"
    child = f"from pathlib import Path;import time;Path({str(started)!r}).touch();time.sleep(0.8)"
    previous = json.loads(run["manifest"].read_text()).get("producer_attempt")
    process = subprocess.Popen([
        sys.executable, str(ROOT / "scripts/blog/blog-run-workspace.py"), "run",
        "--manifest", str(run["manifest"]), "--", sys.executable, "-c", child,
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    try:
        deadline = time.monotonic() + 5
        while not started.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        assert started.exists()
        process.kill()
        process.communicate(timeout=5)
        assert process.returncode == -signal.SIGKILL
        deadline = time.monotonic() + 5
        while True:
            try:
                with workspace.producer_lock(run["manifest"].parent):
                    break
            except workspace.WorkspaceError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.02)
        manifest = json.loads(run["manifest"].read_text())
        assert manifest["producer_attempt"]["state"] == "running"
        assert manifest["producer_attempt"]["attempt_id"] != previous["attempt_id"]
        assert_seal_refused_unchanged(run)
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate(timeout=5)


@pytest.mark.parametrize("state", ["sealed", "published"])
def test_old_verified_seal_remains_idempotent_without_inventing_process_history(
    run, state, tmp_path
):
    legacy = tmp_path / "exact-pre-receipt-source"
    legacy.mkdir()
    for name in ("blog_publication_state.py", "blog-run-workspace.py", "blog-producer-contract.py"):
        blob = subprocess.run([
            "git", "-C", str(ROOT), "show",
            f"0df8cc16c14f0a2326ef7c455cb7cb3a4fb83b19:scripts/blog/{name}",
        ], check=True, capture_output=True).stdout
        (legacy / name).write_bytes(blob)
    spec = importlib.util.spec_from_file_location(
        "pre_receipt_publication", legacy / "blog_publication_state.py"
    )
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    manifest = json.loads(run["manifest"].read_text())
    manifest.pop("producer_attempt", None)
    workspace.atomic_json(run["manifest"], manifest)
    # Execute the actual prior gates/serializer, not a hand-written seal receipt.
    result = prior.seal_quality(run["manifest"], run["transcript"], run["hugo"])
    assert result["outcome"] == "sealed"
    seal_path = run["manifest"].parent / "quality-seal.json"
    assert "producer_attempt" not in json.loads(seal_path.read_text())
    if state == "published":
        publish(run)
    run["transcript"].unlink()
    before = run["manifest"].read_bytes()
    proof = (run["manifest"].parent / "quality-seal.json").read_bytes()
    assert seal(run)["outcome"] == "sealed"
    assert run["manifest"].read_bytes() == before
    assert (run["manifest"].parent / "quality-seal.json").read_bytes() == proof
