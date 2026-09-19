#!/usr/bin/env python3
"""Retained OFFLINE fixture replay of the actual daily wrapper and dry-run lander.

No provider, mail, public publication, or production-state evidence is claimed.
The disposable copy changes ONLY lock literals, flattens the checked-out theme,
and uses a fixture Claude CLI/session transcript. Hugo and enforcement are real.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

DECISIONS = ".claude/skills/blog-backfill/methodology/decisions.jsonl"
REQUIRED = (
    "scripts/blog/blog-producer-contract.py", "scripts/blog/blog-run-workspace.py",
    ".claude/skills/blog-backfill/scripts/rebuild-methodology-index.py",
    ".claude/skills/blog-backfill/methodology/legacy-index-migration-v2.json",
)


def execute(argv, *, cwd=None, env=None, input=None, expected=0):
    result = subprocess.run(argv, cwd=cwd, env=env, input=input, capture_output=True, text=True,
                            timeout=240, check=False)
    if expected is not None and result.returncode != expected:
        raise RuntimeError(f"exit {result.returncode}, expected {expected}: {argv[0]}\n"
                           f"{result.stdout[-3500:]}\n{result.stderr[-3500:]}")
    return result


def git(repo, env, *args):
    return execute(["git", "-C", str(repo), *args], env=env).stdout.strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_producer():
    """Explicit test double, not evidence of real Agent/provider execution."""
    root = Path(os.environ["BLOG_REPO_DIR"])
    date = os.environ["BLOG_TARGET_DATE"]
    run_id = os.environ["BLOG_RUN_ID"]
    uuid.UUID(run_id)
    if sys.argv[sys.argv.index("--session-id") + 1] != run_id:
        raise RuntimeError("fixture session was not bound by actual wrapper")
    if os.environ.get("ANTHROPIC_API_KEY") != "offline-fixture-only-not-a-secret":
        raise RuntimeError("fixture CLI did not receive fixture-only child transport")
    definitions = json.loads(sys.argv[sys.argv.index("--agents") + 1])
    if set(definitions) != {"blog-classifier", "blog-consistency-checker", "blog-fact-checker"}:
        raise RuntimeError("actual producer failed to register its required fixture agents")
    slug = f"offline-contract-fixture-{date}"
    post = root / "content/posts" / f"{slug}.md"
    post.write_text(
        f"+++\ntitle = 'Checking an isolated daily workspace'\nslug = '{slug}'\n"
        f"date = {date}T08:00:00-06:00\ndraft = false\n"
        "categories = ['Development Journey']\ntags = ['testing']\n"
        "description = 'A disposable Git worktree keeps owner edits intact while a dated post "
        "passes deterministic checks.'\n"
        "tldr = 'This is an offline test fixture, never a public article.'\n+++\n\n"
        "Offline fixture. This file stays inside a disposable replay repository.\n\n"
        "I checked the dated post, append boundary, and build result in an isolated worktree.\n"
        "The owner checkout kept its staged edit, unstaged edit, and unfinished draft.\n\n"
        "```sh\nprintf '%s\\n' 'offline fixture'\n```\n\n"
        "The local bare remote is a test fixture. No public site received this file.\n"
    )
    evidence = Path(os.environ["REPLAY_ROOT"]) / "fixture-builds"
    evidence.mkdir(exist_ok=True)
    commands = [
        ["python3", str(root / ".claude/skills/blog-backfill/scripts/lint-post-voice.py"),
         str(post)],
        ["hugo", "--buildFuture", "--gc", "--minify", "--cleanDestinationDir", "--quiet"],
    ]
    for index, argv in enumerate(commands):
        result = execute(argv, cwd=root, env=os.environ)
        (evidence / f"{run_id}-{index}.log").write_text(result.stdout + result.stderr)
    identity = {"date": date, "slug": slug, "run_id": run_id}
    classifier = {
        **identity, "tier": 1, "tier_name": "Field Note", "confidence": .8,
        "dimensions": {key: 1 for key in ("novelty", "arc", "nar", "tch", "scp", "rpr")},
        "fixture": True,
    }
    engine = root / ".claude/skills/blog-backfill/scripts/apply-patterns.py"
    classifier = json.loads(execute(
        ["python3", str(engine), "apply"], cwd=root, env=os.environ,
        input=json.dumps(classifier),
    ).stdout)
    audit = {**identity, "audit_addendum": True, "fixture": True,
             "agent_audit": {"writer": "content-marketer", "offline_fixture": True}}
    scenario = os.environ["REPLAY_SCENARIO"]
    if scenario == "missing-pattern":
        classifier.pop("pattern_engine", None)
    if scenario == "wrong-scope":
        classifier["date"] = (dt.date.fromisoformat(date) - dt.timedelta(days=1)).isoformat()
    with (root / DECISIONS).open("a") as stream:
        stream.write(json.dumps(classifier) + "\n")
        if scenario != "missing-audit":
            stream.write(json.dumps(audit) + "\n")
    staging = root / ".blog-staging"
    staging.mkdir(exist_ok=True)
    (staging / f"{date}.{run_id}.classifier.json").write_text(json.dumps(classifier))
    if scenario != "missing-sentinel":
        sentinel = {
            **identity, "schema_version": 1, "ready": True, "tier": 1,
            "post_sha256": digest(post), "fixture": True,
            "gates": {"build": "pass", "voice_lint": "pass", "code_review": "pass"},
        }
        (staging / f"{date}.intent.json").write_text(json.dumps(sentinel))
    transcript = Path.home() / ".claude/projects/offline-fixture" / f"{run_id}.jsonl"
    transcript.parent.mkdir(parents=True, exist_ok=True)
    rows, roles = [], {}
    agents = ("blog-classifier", "content-marketer", "seo-meta-optimizer", "code-reviewer")
    for index, agent in enumerate(agents):
        receipt = {"blog_gate_receipt": {
            **identity, "agent": agent, "verdict": "PASS", "post_sha256": digest(post),
            "fixture": True,
        }}
        receipt_text = "OFFLINE TEST DOUBLE. " + json.dumps(receipt)
        # Completion authority: what the role produced, staged and hash-bound.
        body = json.dumps({"agent": agent, "date": date, "run_id": run_id,
                           "output": receipt_text, "fixture": True})
        (staging / f"{date}.{run_id}.role-{agent}.json").write_text(body)
        roles[agent] = {"status": "completed",
                        "output_sha256": hashlib.sha256(body.encode()).hexdigest()}
        rows.extend([
            {"type": "assistant", "sessionId": run_id, "fixture": True,
             "message": {"content": [{"type": "tool_use", "name": "Agent", "id": str(index),
                                      "input": {"subagent_type": agent}}]}},
            {"type": "user", "sessionId": run_id, "fixture": True,
             "message": {"content": [{"type": "tool_result", "tool_use_id": str(index),
                                      "content": [{"type": "text", "text": receipt_text}]}]}},
        ])
    transcript.write_text("\n".join(map(json.dumps, rows)) + "\n")
    (staging / f"{date}.{run_id}.roles.json").write_text(json.dumps({
        **identity, "schema_version": 1, "post_sha256": digest(post), "roles": roles,
        "fixture": True,
    }))
    print(f"OFFLINE-FIXTURE-PRODUCER: scenario={scenario} date={date} session={run_id}")
    return 0


def copy_fixture_source(source, owner, lock):
    listed = execute(["git", "-C", str(source), "ls-files", "-z"]).stdout.split("\0")
    omitted = {"fixture_only": True, "paths": [], "bytes": 0}
    for relative in sorted(set(listed) | set(REQUIRED)):
        if not relative or relative == ".gitmodules" or relative.startswith(".beads/"):
            continue
        original = source / relative
        target = owner / relative
        if not original.exists():
            continue
        # Historical page-bundle media is unnecessary for contract replay. Keep
        # every post's source/frontmatter and actual templates/assets/static; a
        # real Hugo failure on an omitted required resource is still fatal.
        if (relative.startswith("content/") and original.is_file()
                and original.suffix.lower() in {
                    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif",
                    ".mp4", ".mov", ".webm", ".mp3", ".wav",
                }):
            omitted["paths"].append(relative)
            omitted["bytes"] += original.stat().st_size
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if original.is_dir():
            shutil.copytree(original, target, ignore=shutil.ignore_patterns(".git"),
                            dirs_exist_ok=True)
        else:
            shutil.copy2(original, target)
    patched = []
    for relative in ("scripts/blog/blog-backfill-daily.sh", "scripts/blog/blog-land.sh",
                     "scripts/blog/blog-run-workspace.py"):
        target = owner / relative
        text = target.read_text()
        count = text.count("/tmp/blog-pipeline.lock")
        if count != 1:
            raise RuntimeError(f"fixture lock literal drift in {relative}: "
                               f"expected one, got {count}")
        target.write_text(text.replace("/tmp/blog-pipeline.lock", str(lock)))
        patched.append({"file": relative, "old": "/tmp/blog-pipeline.lock", "new": str(lock)})
    return patched, omitted


def owner_snapshot(owner, env):
    paths = ("layouts/partials/schema.html", "content/posts/unrelated-august-14-fixture.md",
             "drafts/owner-fixture.md")
    return {"head": git(owner, env, "rev-parse", "HEAD"),
            "status": git(owner, env, "status", "--porcelain=v1"),
            "staged": git(owner, env, "diff", "--cached", "--binary"),
            "unstaged": git(owner, env, "diff", "--binary"),
            "file_hashes": {path: digest(owner / path) for path in paths}}


def replay(args):
    source = args.repo.resolve()
    source_commit = execute(["git", "-C", str(source), "rev-parse", "HEAD"]).stdout.strip()
    wrapper_text = (source / "scripts/blog/blog-backfill-daily.sh").read_text()
    noop_path = wrapper_text.split("if EXISTING=$(published_post_for_date", 1)[-1]
    noop_path = noop_path.split("# Hugo theme", 1)[0]
    if "BLOG_CANARY" not in noop_path:
        raise RuntimeError("actual wrapper no-op path must honor BLOG_CANARY "
                           "before crosspost sweep")
    root = (args.output_root.resolve() if args.output_root else
            Path(tempfile.mkdtemp(prefix="startaitools-offline-contract-replay-")))
    root.mkdir(parents=True, exist_ok=True)
    if list(root.iterdir()):
        raise RuntimeError("output-root must be empty: evidence is never overwritten")
    home, owner, remote = root / "home", root / "owner", root / "remote.git"
    home.mkdir()
    owner.mkdir()
    environment = {
        "HOME": str(home), "PATH": f"{home}/.local/bin:/usr/local/bin:/usr/bin:/bin",
        "TZ": "Etc/GMT+6", "LANG": "C.UTF-8", "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_ALLOW_PROTOCOL": "file",
        "BLOG_CANARY": "1", "BLOG_PRODUCER": "auto", "BLOG_CLOCK": "2030-12-30 12:00:00",
        "BLOG_REPO_DIR": str(owner), "BLOG_EXPECTED_REMOTE": str(remote),
        "BLOG_RUN_STATE_DIR": str(root / "workspace-state"), "BLOG_LOG_DIR": str(root / "logs"),
        "BLOG_LAND_LOG_DIR": str(root / "land-logs"), "BLOG_BACKFILL_TIMEOUT": "180",
        "MINIMAX_API_KEY": "offline-fixture-only-not-a-secret", "REPLAY_ROOT": str(root),
        "INTENT_RUNTIME": str(home / "bin/lib/intent-runtime.sh"),
    }
    version = execute([str(args.hugo), "version"], env=environment).stdout.strip()
    if not re.match(r"^hugo v0\.150\.0(?:[-+\s])", version) or "extended" not in version:
        raise RuntimeError(f"pinned extended Hugo 0.150.0 required, found {version}")
    patched, omitted = copy_fixture_source(source, owner, root / "offline-pipeline.lock")
    (root / "fixture-source-omissions.json").write_text(json.dumps(omitted, indent=2) + "\n")
    dates = [(args.start_date + dt.timedelta(days=i)).isoformat() for i in range(6)]
    for post in (owner / "content/posts").glob("*.md"):
        if any(re.search(r"^date\s*[=:]\s*['\"]?" + date, post.read_text(), re.M)
               for date in dates):
            raise RuntimeError("choose an absent date pair; fixture baseline already has "
                               f"{post.name}")
    binary = home / ".local/bin"
    binary.mkdir(parents=True)
    (binary / "hugo").symlink_to(args.hugo.resolve())
    mock = binary / "claude"
    mock.write_text(f"#!/bin/sh\nexec /usr/bin/python3 '{Path(__file__).resolve()}' "
                    ' --fixture-producer "$@"\n')
    mock.chmod(0o755)
    for executable in ("node", "curl", "sops", "notify.sh"):
        denial = binary / executable
        denial.write_text("#!/bin/sh\nprintf '%s\\n' 'FORBIDDEN-SERVICE: " + executable
                          + f"' >> '{root}/forbidden-services.log'\nexit 91\n")
        denial.chmod(0o755)
    runtime = Path(environment["INTENT_RUNTIME"])
    runtime.parent.mkdir(parents=True)
    runtime.write_text("cron_fail() { printf '%s\\n' 'FORBIDDEN-SERVICE: cron_fail' "
                       f">> '{root}/forbidden-services.log'; return 91; }}\n")
    skill = home / ".claude/skills/blog-backfill"
    (skill / "agents").mkdir(parents=True)
    (skill / "references").mkdir()
    (skill / "SKILL.md").write_text("OFFLINE FIXTURE ONLY. Never publish these test articles.\n")
    (skill / "references/run-contract.md").write_text("OFFLINE fixture dispatch contract.\n")
    for agent in ("blog-classifier", "blog-consistency-checker", "blog-fact-checker"):
        (skill / "agents" / f"{agent}.md").write_text(
            f"---\nname: {agent}\ndescription: Offline replay fixture agent\n---\n"
            "This definition is a test double. It provides no production review evidence.\n"
        )
    git(root, environment, "init", "--bare", "--initial-branch=master", str(remote))
    git(remote, environment, "config", "core.compression", "0")
    git(owner, environment, "init", "--initial-branch=master")
    git(owner, environment, "config", "core.compression", "0")
    git(owner, environment, "config", "user.name", "Offline contract replay fixture")
    git(owner, environment, "config", "user.email", "fixture@example.invalid")
    git(owner, environment, "add", ".")
    git(owner, environment, "commit", "-m", "fixture: copy current source for offline replay")
    fixture_baseline_commit = git(owner, environment, "rev-parse", "HEAD")
    enforcement_hashes = {
        relative: digest(owner / relative)
        for relative in (*REQUIRED, "scripts/blog/blog-backfill-daily.sh",
                         "scripts/blog/blog-land.sh", "scripts/blog/lib-cron-common.sh")
    }
    git(owner, environment, "remote", "add", "origin", str(remote))
    git(owner, environment, "push", "origin", "master")
    git(owner, environment, "remote", "set-head", "origin", "master")
    schema = owner / "layouts/partials/schema.html"
    schema.write_text(schema.read_text() + "\n<!-- staged owner fixture -->\n")
    git(owner, environment, "add", "layouts/partials/schema.html")
    schema.write_text(schema.read_text() + "<!-- unstaged owner fixture -->\n")
    (owner / "content/posts/unrelated-august-14-fixture.md").write_text("owner untracked fixture\n")
    (owner / "drafts").mkdir(exist_ok=True)
    (owner / "drafts/owner-fixture.md").write_text("unfinished owner fixture\n")
    before = owner_snapshot(owner, environment)
    results = []

    def run(date, scenario, expected):
        label = f"{len(results):02}-{date}-{scenario}"
        print(f"OFFLINE-FIXTURE-REPLAY: {label}", flush=True)
        prior = set((root / "workspace-state").glob("*/runs/*/*/manifest.json"))
        result = execute(["bash", str(owner / "scripts/blog/blog-backfill-daily.sh"),
                          "--date", date], env={**environment, "REPLAY_SCENARIO": scenario},
                         expected=expected)
        (root / f"{label}.stdout.log").write_text(result.stdout + result.stderr)
        fresh = set((root / "workspace-state").glob("*/runs/*/*/manifest.json")) - prior
        if len(fresh) != 1:
            raise RuntimeError(f"{label}: expected one actual-wrapper run manifest, "
                               f"found {len(fresh)}")
        manifest_path = fresh.pop()
        manifest = json.loads(manifest_path.read_text())
        log = (root / "logs" / f"run-{date}.log").read_text()
        if scenario == "repeat":
            remote_master = git(owner, environment, "ls-remote", "origin",
                                "refs/heads/master").split()[0]
            if (manifest["status"] != "noop"
                    or manifest.get("verified_remote_master") != remote_master
                    or manifest.get("baseline_sha") != remote_master
                    or manifest.get("existing_posts") != [
                        f"content/posts/offline-contract-fixture-{date}.md"]):
                raise RuntimeError("repeat did not prove remote-backed idempotency")
        elif manifest["status"] != "quarantined":
            raise RuntimeError(f"{label}: canary did not retain quarantined workspace")
        if scenario == "valid" and "LAND-RESULT: OK (dry-run)" not in log:
            raise RuntimeError("valid fixture never passed actual lander checks")
        if scenario not in {"valid", "repeat"} and (
            "land_rc=22" not in log or "Invoking blog-land.sh" in log
        ):
            raise RuntimeError(
                f"{label}: rejected producer entered landing or lacked failure state"
            )
        if owner_snapshot(owner, environment) != before:
            raise RuntimeError(f"{label}: owner staged/unstaged/untracked state changed")
        if (root / "forbidden-services.log").exists():
            raise RuntimeError("unexpected mail/network/notification path attempted in canary")
        heartbeat = home / ".local/state/intent-os/liveness/blog-backfill-daily.beat"
        if heartbeat.exists():
            raise RuntimeError("BLOG_CANARY wrote a liveness heartbeat: " + str(heartbeat))
        receipt = {"fixture": True, "scenario": scenario, "date": date,
                   "exit_code": result.returncode,
                   "manifest": str(manifest_path), "run_id": manifest["run_id"],
                   "status": manifest["status"], "owner_unchanged": True}
        receipt["heartbeat_absent"] = True
        results.append(receipt)
        return manifest

    for date in dates[:2]:
        manifest = run(date, "valid", 0)
        workspace = Path(manifest["workspace"])
        if git(workspace, environment, "remote", "get-url", "origin") != str(remote):
            raise RuntimeError("fixture source advancement remote escaped replay")
        post = f"content/posts/offline-contract-fixture-{date}.md"
        git(workspace, environment, "add", post, DECISIONS)
        git(workspace, environment, "commit", "-m",
            f"fixture: retain validated dry-run date {date}")
        git(workspace, environment, "push", "origin", "HEAD:refs/heads/master")
        results[-1]["fixture_only_remote_commit"] = git(workspace, environment, "rev-parse", "HEAD")
    run(dates[0], "repeat", 0)
    for date, scenario in zip(dates[2:], (
        "missing-sentinel", "missing-audit", "missing-pattern", "wrong-scope",
    ), strict=True):
        run(date, scenario, 1)
    report = {"fixture_only": True, "production_verified": False, "output_root": str(root),
              "hugo": version, "source_commit_at_start": source_commit,
              "fixture_baseline_commit": fixture_baseline_commit,
              "enforcement_sha256": enforcement_hashes,
              "fixture_lock_substitutions": patched, "runs": results,
              "omitted_historical_media_count": len(omitted["paths"]),
              "omitted_historical_media_bytes": omitted["bytes"],
              "omissions_manifest": str(root / "fixture-source-omissions.json"),
              "owner_state_unchanged": owner_snapshot(owner, environment) == before,
              "limitations": [
                  "Claude/Agent receipts are explicit test doubles; no provider execution.",
                  "Publication is dry-run; normal Git advancement is to a local bare fixture.",
                  "Canonical lock literal is changed only in disposable source copies.",
                  "Historical page-bundle media is omitted; all source posts/templates remain.",
                  "No public deploy, external mail, or production heartbeat is exercised.",
              ]}
    (root / "replay-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


def main():
    if "--fixture-producer" in sys.argv:
        return fixture_producer()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--hugo", type=Path, default=Path("/tmp/hugo-0.150.0/usr/local/bin/hugo"))
    parser.add_argument("--start-date", type=dt.date.fromisoformat, default=dt.date(2026, 9, 16))
    args = parser.parse_args()
    try:
        return replay(args)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f"OFFLINE-CONTRACT-REPLAY: FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
