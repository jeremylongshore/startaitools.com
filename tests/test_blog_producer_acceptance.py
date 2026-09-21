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
scenario = os.environ["FIXTURE_SCENARIO"]
calls = pathlib.Path(os.environ["REPLAY_ROOT"]) / "producer-calls.jsonl"
with calls.open("a") as stream:
    stream.write(json.dumps({{"argv": sys.argv[1:], "mode": os.environ.get("BLOG_PRODUCER"),
                             "run_id": run_id}}) + chr(10))
REAL_429 = ("API Error: Request rejected (429) · Token Plan usage limit reached: Upgrade your "
            "Token Plan or purchase Credits for more usage. (2056)")
if scenario == "provider-dead" or (scenario == "provider-429"
                                   and os.environ.get("BLOG_PRODUCER") != "claude"):
    print(REAL_429)
    sys.exit(1)
held = pathlib.Path(os.environ["REPLAY_ROOT"]) / ("held-roles-" + run_id + ".json")
if scenario == "repairable" and "--resume" in sys.argv:
    # The repair round: the SAME session in the SAME workspace supplies what was missing.
    staging = pathlib.Path(os.environ["BLOG_REPO_DIR"]) / ".blog-staging"
    target = staging / (os.environ.get("BLOG_TARGET_DATE", "") + "." + run_id + ".roles.json")
    target.write_bytes(held.read_bytes())
    sys.exit(0)
if "--session-id" not in sys.argv:
    sys.argv.extend(["--session-id", run_id])
if "--agents" not in sys.argv:
    sys.argv.extend(["--agents", json.dumps(dict.fromkeys(
        ["blog-classifier", "blog-consistency-checker", "blog-fact-checker"], {{}}))])
if os.environ["FIXTURE_SCENARIO"] == "missing-contract":
    os.environ["REPLAY_SCENARIO"] = "missing-sentinel"
fixture = runpy.run_path({str(REPLAY_PATH)!r})
fixture["fixture_producer"]()
if scenario == "repairable":
    # A finished post with ONE nameable gap: the roles receipt is absent.
    staging = pathlib.Path(os.environ["BLOG_REPO_DIR"]) / ".blog-staging"
    receipt = staging / (os.environ["BLOG_TARGET_DATE"] + "." + run_id + ".roles.json")
    held.write_bytes(receipt.read_bytes())
    receipt.unlink()
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
    # gh too: deploy patience dispatches a workflow outside canary mode, and no test may
    # ever reach the real GitHub CLI.
    for name in ("curl", "sops", "notify.sh", "gh"):
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
# A scenario may dictate the lander's verdict without publishing anything.
if [ -n "${FIXTURE_LAND_RC:-}" ]; then
  echo "LAND-RESULT: FIXTURE rc=${FIXTURE_LAND_RC}" >> "${BLOG_LOG_DIR}/run-${1}.log"
  exit "$FIXTURE_LAND_RC"
fi
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
        # These tests pin what ONE attempt does. Repair rounds and failover are exercised
        # by the run_recovering tests below; with recovery on, a rejected producer
        # legitimately starts a second run and this helper's one-manifest check is wrong.
        "BLOG_RECOVERY": "0",
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


def run_recovering(pipeline, scenario, *, recovery="1", date=DATE, canary="1", extra=None):
    """Drive the real wrapper with recovery enabled; failover legitimately makes 2 runs."""
    env = {
        **pipeline["env"],
        "FIXTURE_SCENARIO": scenario,
        "BLOG_PRODUCER": "auto",
        "BLOG_CANARY": canary,
        "BLOG_RECOVERY": recovery,
        "BLOG_REPAIR_ROUNDS": "2",
        # Never wait on, or talk to, a real release pipeline from a test.
        "BLOG_CATCHUP_SETTLE_SECS": "0",
        "BLOG_CATCHUP_SETTLE_GRACE_SECS": "0",
        "BLOG_CATCHUP_BLIND_WAIT_SECS": "0",
        **(extra or {}),
    }
    if recovery is None:
        env.pop("BLOG_RECOVERY")
    result = command(
        ["bash", str(pipeline["owner"] / "scripts/blog/blog-backfill-daily.sh"), "--date", date],
        env=env,
    )
    manifests = [
        json.loads(p.read_text())
        for p in sorted((pipeline["root"] / "state").glob("*/runs/*/*/manifest.json"))
    ]
    log = (pipeline["root"] / "logs" / f"run-{date}.log").read_text()
    calls_file = pipeline["root"] / "producer-calls.jsonl"
    calls = [json.loads(line) for line in calls_file.read_text().splitlines()]
    assert REPLAY.owner_snapshot(pipeline["owner"], env) == pipeline["snapshot"]
    return result, manifests, log, calls


def test_a_post_the_contract_refused_is_repaired_in_the_same_run_without_a_human(pipeline):
    result, manifests, log, calls = run_recovering(pipeline, "repairable")
    assert result.returncode == 0, log
    assert "roles: staging record missing" in log
    assert "RECOVERY: repair round 1/2" in log and "RECOVERY: repaired in round 1" in log
    assert "PRODUCER-CONTRACT: complete" in log and "LAND-RESULT: OK (dry-run)" in log
    assert len(manifests) == 1, "a repair reuses the run; it must not start another"
    assert len(calls) == 2
    assert "--session-id" in calls[0]["argv"] and "--resume" in calls[1]["argv"]
    resumed = calls[1]["argv"][calls[1]["argv"].index("--resume") + 1]
    assert resumed == calls[0]["run_id"] == calls[1]["run_id"]
    prompt = calls[1]["argv"][calls[1]["argv"].index("-p") + 1]
    assert "roles: staging record missing" in prompt and "REPAIR ROUND 1 of 2" in prompt
    assert "may NOT edit anything under scripts/" in prompt
    assert "FAILOVER:" not in log


def test_recovery_stays_off_in_canary_mode_unless_asked_for(pipeline):
    result, manifests, log, calls = run_recovering(pipeline, "repairable", recovery=None)
    assert result.returncode != 0
    assert len(calls) == 1 and "RECOVERY:" not in log and "FAILOVER:" not in log
    assert manifests[0]["status"] == "quarantined"


def test_a_provider_out_of_quota_fails_over_once_to_the_other_provider(pipeline):
    result, manifests, log, calls = run_recovering(pipeline, "provider-429")
    assert result.returncode == 0, log
    assert '"action": "failover"' in log and "usage limit reached" in log
    assert "FAILOVER: auto did not produce" in log and "published by 'claude'" in log
    assert "LOCK: inherited from the parent run (failover child)" in log
    assert [c["mode"] for c in calls] == ["auto", "claude"]
    assert calls[0]["run_id"] != calls[1]["run_id"], "the other provider needs a fresh session"
    assert sorted(m["status"] for m in manifests)[-1] == "quarantined"
    assert len(manifests) == 2
    assert "recovered by failover" in log


def test_when_both_providers_are_down_it_pages_once_and_never_loops(pipeline):
    """Outside canary mode, so the real alert path runs: two failed runs, ONE page."""
    notifications = Path(pipeline["env"]["FIXTURE_NOTIFICATIONS"])
    run_recovering(pipeline, "nonzero", recovery="0", canary="0")
    single_failure = len(notifications.read_text().splitlines())
    assert single_failure >= 1
    (pipeline["root"] / "producer-calls.jsonl").unlink()
    result, manifests, log, calls = run_recovering(
        pipeline, "provider-dead", canary="0", date="2030-12-21"
    )
    assert result.returncode != 0
    assert [c["mode"] for c in calls] == ["auto", "claude"], "depth is capped at one failover"
    mine = [m for m in manifests if m["date"] == "2030-12-21"]
    assert len(mine) == 2 and {m["status"] for m in mine} == {"quarantined"}
    assert "failover to 'claude' also failed" in log
    assert "QUIET-CHILD: failed quietly; the parent run owns alerting for this date" in log
    assert log.count("FAILOVER: ") == 1
    paged = len(notifications.read_text().splitlines()) - single_failure
    assert paged == single_failure, "a double failure must page exactly like a single one"


def test_an_explicit_date_run_never_starts_catch_up(pipeline):
    _, _, log, calls = run_recovering(pipeline, "valid")
    assert "CATCH-UP" not in log and len(calls) == 1


def test_missed_recent_dates_are_caught_up_quietly_newest_first(pipeline):
    """Tonight's date first, then the gaps behind it, each as its own quiet child run."""
    state = pipeline["root"] / "catchup-state.json"
    result, manifests, log, calls = run_recovering(
        pipeline,
        "valid",
        date="2030-12-22",
        extra={
            "BLOG_CATCHUP_FORCE": "1",
            "BLOG_CATCHUP_DAYS": "2",
            "BLOG_CATCHUP_STATE": str(state),
        },
    )
    assert result.returncode == 0, log
    plan = json.loads(log.split("CATCH-UP: plan=", 1)[1].splitlines()[0])
    assert plan["attempt"] == ["2030-12-21", "2030-12-20"]
    assert "CATCH-UP: 2030-12-21 recovered; no human involved" in log
    assert "CATCH-UP: 2030-12-20 recovered; no human involved" in log
    dates = [
        json.loads(Path(m["workspace"]).parent.joinpath("manifest.json").read_text())["date"]
        for m in manifests
    ]
    assert sorted(dates) == ["2030-12-20", "2030-12-21", "2030-12-22"]
    assert len(calls) == 3, "one producer run per date; a child must never catch up again"
    for date in ("2030-12-21", "2030-12-20"):
        child = (pipeline["root"] / "logs" / f"run-{date}.log").read_text()
        assert "LOCK: inherited from the parent run" in child and "CATCH-UP: plan=" not in child
    recorded = json.loads(state.read_text())
    assert recorded["2030-12-21"]["attempts"] == 1 and "published" in recorded["2030-12-21"]


def test_a_date_that_cannot_be_written_is_given_up_on_once_not_retried_forever(pipeline):
    state = pipeline["root"] / "catchup-state.json"
    extra = {
        "BLOG_CATCHUP_FORCE": "1",
        "BLOG_CATCHUP_DAYS": "1",
        "BLOG_CATCHUP_MAX_ATTEMPTS": "1",
        "BLOG_CATCHUP_STATE": str(state),
        "BLOG_PRODUCER_FAILOVER": "0",
    }
    logs = []
    for _ in range(3):
        _, _, log, _ = run_recovering(pipeline, "provider-dead", date="2030-12-22", extra=extra)
        logs.append(log)
    first = logs[0]
    second = logs[1][len(logs[0]) :]
    third = logs[2][len(logs[1]) :]
    assert "CATCH-UP: 2030-12-21 still missing" in first and "GAVE UP" not in first
    assert "CATCH-UP: GAVE UP on 2030-12-21 after 1 attempts" in second
    assert "GAVE UP" not in third, "a given-up date is reported exactly once"
    assert json.loads(state.read_text())["2030-12-21"]["attempts"] == 1


def test_a_published_post_whose_page_is_not_live_yet_is_pending_not_failed(pipeline):
    """Outside canary mode: the real status mapping, exit code and alert path."""
    notifications = Path(pipeline["env"]["FIXTURE_NOTIFICATIONS"])
    result, _, log, _ = run_recovering(
        pipeline, "valid", canary="0", extra={"FIXTURE_LAND_RC": "13"}
    )
    assert "Overall STATUS: PENDING (published; page not live" in log
    assert result.returncode == 0, log
    assert "DEPLOY-PATIENCE:" in log
    paged = (
        [
            ln
            for ln in notifications.read_text().splitlines()
            if ln.startswith("blog-backfill-daily")
        ]
        if notifications.exists()
        else []
    )
    assert paged == [], "a slow deploy must not page"
    assert "FAILOVER:" not in log, "a published post must never be produced a second time"


def test_a_failover_child_that_published_but_is_still_deploying_counts_as_recovered(pipeline):
    """Independent review of #96: PENDING from the child must not read as a failed failover."""
    notifications = Path(pipeline["env"]["FIXTURE_NOTIFICATIONS"])
    result, manifests, log, calls = run_recovering(
        pipeline, "provider-429", canary="0", extra={"FIXTURE_LAND_RC": "13"}
    )
    assert [c["mode"] for c in calls] == ["auto", "claude"]
    assert "Overall STATUS: PENDING (published; page not live" in log
    assert "published by 'claude'" in log and "also failed" not in log
    assert result.returncode == 0, log
    paged = (
        [
            ln
            for ln in notifications.read_text().splitlines()
            if ln.startswith("blog-backfill-daily")
        ]
        if notifications.exists()
        else []
    )
    assert paged == [], "a published night must not page because the page was slow"
