"""Execute the complete wrapper with real contracts/Git and offline producer doubles."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
REPLAY_PATH = ROOT / "scripts/blog/test-blog-contract-replay.py"
SPEC = importlib.util.spec_from_file_location("acceptance_replay", REPLAY_PATH)
REPLAY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPLAY)
DATE = "2030-12-20"


def command(argv, *, env, cwd=None):
    return subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=75)


def git(root, env, *args):
    result = command(["git", "-C", str(root), *args], env=env)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def executable(path, text):
    path.write_text(text)
    path.chmod(0o755)


@pytest.fixture
def pipeline(tmp_path):
    owner, home, remote = tmp_path / "owner", tmp_path / "home", tmp_path / "remote.git"
    owner.mkdir()
    binary = home / ".local/bin"
    binary.mkdir(parents=True)
    env = {
        "HOME": str(home),
        "PATH": f"{binary}:/usr/local/bin:/usr/bin:/bin",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_ALLOW_PROTOCOL": "file",
        "PYTHONDONTWRITEBYTECODE": "1",
        "TZ": "Etc/GMT+6",
        "LANG": "C.UTF-8",
        "BLOG_CANARY": "1",
        "BLOG_PRODUCER": "auto",
        "BLOG_CLOCK": "2030-12-30 12:00:00",
        "BLOG_REPO_DIR": str(owner),
        "BLOG_EXPECTED_REMOTE": str(remote),
        "BLOG_RUN_STATE_DIR": str(tmp_path / "state"),
        "BLOG_LOG_DIR": str(tmp_path / "logs"),
        "BLOG_LAND_LOG_DIR": str(tmp_path / "land-logs"),
        "BLOG_BACKFILL_TIMEOUT": "30",
        "BLOG_BACKFILL_DISK_WARN_MB": "500",
        "MINIMAX_API_KEY": "offline-fixture-only-not-a-secret",
        "ANTHROPIC_API_KEY": "offline-fixture-only-not-a-secret",
        "REPLAY_ROOT": str(tmp_path),
        "REPLAY_SCENARIO": "valid",
        "FIXTURE_SCENARIO": "valid",
        "FIXTURE_LAND_CALLS": str(tmp_path / "land-calls"),
        "FIXTURE_NOTIFICATIONS": str(tmp_path / "notifications"),
        "BLOG_PRODUCER_TRANSCRIPT": str(tmp_path / "bound-transcript.jsonl"),
        "FIXTURE_TRANSCRIPT": str(tmp_path / "bound-transcript.jsonl"),
        "FIXTURE_CONTRACT": str(tmp_path / "contract-before-exit.json"),
        "INTENT_RUNTIME": str(home / "bin/lib/intent-runtime.sh"),
    }
    lock = tmp_path / "fixture-pipeline.lock"
    REPLAY.copy_fixture_source(ROOT, owner, lock)
    wrapper_override = os.environ.get("BLOG_ACCEPTANCE_WRAPPER_UNDER_TEST")
    if wrapper_override:
        (owner / "scripts/blog/blog-backfill-daily.sh").write_text(
            Path(wrapper_override).read_text().replace("/tmp/blog-pipeline.lock", str(lock))
        )
    # Only the provider process and external services are doubles. The wrapper,
    # manifest ownership/quarantine and semantic verifier execute their real code.
    producer = binary / "claude"
    executable(
        producer,
        f"""#!/usr/bin/env python3
import json, os, pathlib, runpy, shutil, subprocess, sys, time
run_id = os.environ["BLOG_RUN_ID"]
os.environ.setdefault("BLOG_TARGET_DATE", json.loads(
    pathlib.Path(os.environ["BLOG_RUN_MANIFEST"]).read_text())["date"])
if "--session-id" not in sys.argv:
    sys.argv.extend(["--session-id", run_id])
if "--agents" not in sys.argv:
    sys.argv.extend(["--agents", json.dumps(dict.fromkeys(
        ["blog-classifier", "blog-consistency-checker", "blog-fact-checker"], {{}}))])
if os.environ["FIXTURE_SCENARIO"] == "missing-contract":
    os.environ["REPLAY_SCENARIO"] = "missing-sentinel"
fixture = runpy.run_path({str(REPLAY_PATH)!r})
fixture["fixture_producer"]()
native = pathlib.Path.home() / ".claude/projects/offline-fixture" / (run_id + ".jsonl")
shutil.copyfile(native, os.environ["FIXTURE_TRANSCRIPT"])
root = pathlib.Path(os.environ["BLOG_REPO_DIR"])
proof = subprocess.run([sys.executable, str(root / "scripts/blog/blog-producer-contract.py"),
    "verify", "--repo", str(root), "--date", os.environ["BLOG_TARGET_DATE"],
    "--run-id", run_id, "--transcript", str(native)], capture_output=True, text=True)
pathlib.Path(os.environ["FIXTURE_CONTRACT"]).write_text(json.dumps(
    {{"fixture_only": True, "exit_code": proof.returncode, "stdout": proof.stdout}}))
if os.environ["FIXTURE_SCENARIO"] == "nonzero":
    sys.exit(143)
if os.environ["FIXTURE_SCENARIO"] == "timeout":
    time.sleep(30)
sys.exit(0)
""",
    )
    env.update(GROK_BIN=str(producer), MINIMAX_AGENT=str(producer))
    executable(binary / "hugo", "#!/bin/sh\nexit 0\n")
    executable(
        binary / "node",
        """#!/usr/bin/env python3
import json, os, pathlib, sys
args = sys.argv[1:]
body = pathlib.Path(args[args.index("--body-file") + 1]).read_text()
with open(os.environ["FIXTURE_NOTIFICATIONS"], "a") as out:
    out.write(json.dumps({"fixture": True, "body": body}) + "\\n")
""",
    )
    for name in ("curl", "sops", "notify.sh"):
        executable(binary / name, "#!/bin/sh\nprintf '%s\\n' forbidden-service >&2\nexit 91\n")
    runtime = Path(env["INTENT_RUNTIME"])
    runtime.parent.mkdir(parents=True)
    runtime.write_text('cron_fail() { printf "%s\\n" "$*" >> "$FIXTURE_NOTIFICATIONS"; }\n')
    skill = home / ".claude/skills/blog-backfill"
    (skill / "agents").mkdir(parents=True)
    (skill / "references").mkdir()
    (skill / "SKILL.md").write_text("OFFLINE FIXTURE ONLY\n")
    (skill / "references/run-contract.md").write_text("OFFLINE FIXTURE ONLY\n")
    for name in ("blog-classifier", "blog-consistency-checker", "blog-fact-checker"):
        (skill / "agents" / f"{name}.md").write_text(
            f"---\nname: {name}\ndescription: Offline fixture only\n---\nFixture.\n"
        )
    lander = owner / "scripts/blog/blog-land.sh"
    shutil.copyfile(lander, lander.with_name("blog-land-fixture-original.sh"))
    executable(
        lander,
        """#!/usr/bin/env bash
printf '%s\\n' "$*" >> "$FIXTURE_LAND_CALLS"
# No test may publish or call providers even if an acceptance assertion regresses.
[ "${BLOG_CANARY:-0}" = 1 ] || exit 92
exec bash "$(dirname "$0")/blog-land-fixture-original.sh" "$@"
""",
    )
    git(tmp_path, env, "init", "--bare", "--initial-branch=master", str(remote))
    git(owner, env, "init", "--initial-branch=master")
    git(owner, env, "config", "user.name", "Offline fixture")
    git(owner, env, "config", "user.email", "fixture@example.invalid")
    git(owner, env, "add", ".")
    git(owner, env, "commit", "-m", "offline producer acceptance fixture")
    git(owner, env, "remote", "add", "origin", str(remote))
    git(owner, env, "push", "origin", "master")
    git(owner, env, "remote", "set-head", "origin", "master")
    schema = owner / "layouts/partials/schema.html"
    schema.write_text(schema.read_text() + "\n<!-- staged owner fixture -->\n")
    git(owner, env, "add", "layouts/partials/schema.html")
    schema.write_text(schema.read_text() + "<!-- unstaged owner fixture -->\n")
    (owner / "content/posts/unrelated-august-14-fixture.md").write_text("owner draft\n")
    (owner / "drafts").mkdir(exist_ok=True)
    (owner / "drafts/owner-fixture.md").write_text("owner unfinished work\n")
    state_files = [owner / ".blog-syndication-ledger.json", owner / ".crosspost-queue.json"]
    for path in state_files:
        path.write_text('[{"slug":"unrelated-existing-receipt","packet_sent":true}]\n')
    return {
        "root": tmp_path,
        "owner": owner,
        "env": env,
        "home": home,
        "snapshot": REPLAY.owner_snapshot(owner, env),
        "state": {path: path.read_bytes() for path in state_files},
    }


def run_wrapper(pipeline, scenario, *, date=DATE, mode="auto", canary=True):
    env = {
        **pipeline["env"],
        "FIXTURE_SCENARIO": scenario,
        "BLOG_PRODUCER": mode,
        "BLOG_CANARY": "1" if canary else "0",
    }
    if scenario == "timeout":
        env["BLOG_BACKFILL_TIMEOUT"] = "4"
    prior = set((pipeline["root"] / "state").glob("*/runs/*/*/manifest.json"))
    result = command(
        ["bash", str(pipeline["owner"] / "scripts/blog/blog-backfill-daily.sh"), "--date", date],
        env=env,
    )
    manifests = set((pipeline["root"] / "state").glob("*/runs/*/*/manifest.json")) - prior
    assert len(manifests) == 1, result.stdout + result.stderr
    manifest = json.loads(manifests.pop().read_text())
    log = (pipeline["root"] / "logs" / f"run-{date}.log").read_text()
    assert REPLAY.owner_snapshot(pipeline["owner"], env) == pipeline["snapshot"]
    assert all(path.read_bytes() == before for path, before in pipeline["state"].items())
    markers = pipeline["home"] / ".local/state/intent-os/liveness"
    assert not (markers / "blog-backfill-daily.ok").exists()
    if canary:
        assert not (markers / "blog-backfill-daily.beat").exists()
        assert not Path(env["FIXTURE_NOTIFICATIONS"]).exists()
    return result, manifest, log


@pytest.mark.parametrize("scenario", ["nonzero", "timeout", "missing-contract"])
def test_failed_producer_never_calls_lander_even_with_ready_artifacts(pipeline, scenario):
    result, manifest, log = run_wrapper(pipeline, scenario)
    assert not Path(pipeline["env"]["FIXTURE_LAND_CALLS"]).exists(), log
    assert result.returncode == 1, log
    assert manifest["status"] == "quarantined"
    attempt = manifest["producer_attempt"]
    assert attempt["state"] == "completed"
    assert type(attempt["exit_code"]) is int
    assert attempt["exit_code"] == {"nonzero": 143, "timeout": 124, "missing-contract": 0}[scenario]
    assert all(attempt[key] == manifest[key] for key in ("run_id", "date", "baseline_sha"))
    root = Path(manifest["workspace"])
    assert root.is_dir() and Path(manifest["quarantine"]).is_dir()
    post = root / f"content/posts/offline-contract-fixture-{DATE}.md"
    assert post.read_bytes() == (Path(manifest["quarantine"]) / "posts" / post.name).read_bytes()
    assert (
        pipeline["home"] / ".claude/projects/offline-fixture" / f"{manifest['run_id']}.jsonl"
    ).is_file()
    proof = json.loads(Path(pipeline["env"]["FIXTURE_CONTRACT"]).read_text())
    assert proof["exit_code"] == (65 if scenario == "missing-contract" else 0)
    assert "LAND-SKIPPED" in log and "Overall STATUS: FAILED" in log
    assert "exit 143" in log if scenario == "nonzero" else True
    assert "timeout exit 124" in log if scenario == "timeout" else True


@pytest.mark.parametrize("mode", ["claude", "minimax", "grok"])
def test_each_explicit_mode_requires_producer_acceptance(pipeline, mode):
    result, manifest, log = run_wrapper(pipeline, "nonzero", mode=mode)
    assert result.returncode == 1, log
    assert not Path(pipeline["env"]["FIXTURE_LAND_CALLS"]).exists(), log
    assert manifest["status"] == "quarantined"
    assert manifest["producer_attempt"]["exit_code"] == 143


def test_rejected_producer_keeps_failure_alerts_and_withholds_ok(pipeline):
    result, manifest, log = run_wrapper(pipeline, "nonzero", canary=False)
    assert result.returncode == 1, log
    assert not Path(pipeline["env"]["FIXTURE_LAND_CALLS"]).exists(), log
    assert manifest["status"] == "quarantined"
    notifications = Path(pipeline["env"]["FIXTURE_NOTIFICATIONS"]).read_text()
    assert "FAILED" in notifications and "producer" in notifications.lower()
    assert (pipeline["home"] / ".local/state/intent-os/liveness/blog-backfill-daily.beat").exists()


def test_valid_two_dates_still_land_and_existing_remote_repeat_skips_producer(pipeline):
    for date in (DATE, "2030-12-21"):
        result, manifest, log = run_wrapper(pipeline, "valid", date=date)
        assert result.returncode == 0, log
        assert "PRODUCER-CONTRACT: complete" in log and "LAND-RESULT: OK (dry-run)" in log
        root = Path(manifest["workspace"])
        git(
            root,
            pipeline["env"],
            "add",
            f"content/posts/offline-contract-fixture-{date}.md",
            REPLAY.DECISIONS,
        )
        git(root, pipeline["env"], "commit", "-m", "offline fixture validated date")
        git(root, pipeline["env"], "push", "origin", "HEAD:refs/heads/master")
    calls = Path(pipeline["env"]["FIXTURE_LAND_CALLS"]).read_bytes()
    proof = Path(pipeline["env"]["FIXTURE_CONTRACT"]).read_bytes()
    result, manifest, _ = run_wrapper(pipeline, "nonzero", date=DATE)
    assert result.returncode == 0
    assert manifest["status"] == "noop"
    assert Path(pipeline["env"]["FIXTURE_LAND_CALLS"]).read_bytes() == calls
    assert Path(pipeline["env"]["FIXTURE_CONTRACT"]).read_bytes() == proof
