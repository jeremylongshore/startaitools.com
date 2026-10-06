"""Periodic blog jobs never mutate the primary checkout (authority map 000-docs/014 §4.4).

Hermetic: a bare origin, a deliberately dirty "primary checkout" clone, a stub HOME,
a fake `claude` producer and a fake `node` mailer. Each wrapper must publish its output
to origin from its own workspace and leave the primary checkout's HEAD, branch refs,
index, working tree and stash exactly as they were.
"""

import datetime as dt
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
METH = ".claude/skills/blog-backfill/methodology"

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "INTENT_RUNTIME": "/nonexistent",
}


def git(cwd, *args):
    return subprocess.run(
        ["git", "-C", str(cwd), *args], env=GIT_ENV, check=True, capture_output=True, text=True
    ).stdout.strip()


def executable(path, body):
    path.write_text("#!/usr/bin/env bash\n" + body)
    path.chmod(0o755)
    return path


@pytest.fixture
def estate(tmp_path):
    bare = tmp_path / "origin.git"
    git(tmp_path, "init", "-q", "--bare", "--initial-branch=master", str(bare))
    primary = tmp_path / "primary"
    git(tmp_path, "clone", "-q", str(bare), str(primary))
    (primary / METH).mkdir(parents=True)
    (primary / METH / "decisions.jsonl").write_text("")
    (primary / METH / "patterns.jsonl").write_text("{}\n")
    (primary / "content/monthly-recaps").mkdir(parents=True)
    (primary / "content/monthly-recaps/.keep").write_text("")
    (primary / "notes.md").write_text("seed\n")
    git(primary, "add", ".")
    git(primary, "commit", "-qm", "seed")
    git(primary, "push", "-q", "origin", "HEAD:master")
    # The owner's checkout as cron finds it: a local unpushed commit, a staged change,
    # an unstaged change, an untracked file and a stash. The old wrappers refused or
    # rewrote exactly this state.
    (primary / "notes.md").write_text("local commit\n")
    git(primary, "commit", "-qam", "owner local work")
    (primary / "staged.md").write_text("staged\n")
    git(primary, "add", "staged.md")
    (primary / "notes.md").write_text("unstaged edit\n")
    (primary / "scratch.txt").write_text("untracked\n")
    (primary / "stashed.md").write_text("x\n")
    git(primary, "stash", "push", "-q", "-u", "--", "stashed.md")
    home = tmp_path / "home"
    home.mkdir()
    bindir = tmp_path / "bin"
    bindir.mkdir()
    executable(bindir / "node", "exit 0\n")
    return bare, primary, home, bindir


def snapshot(primary):
    return {
        "head": git(primary, "rev-parse", "HEAD"),
        "branch": git(primary, "symbolic-ref", "-q", "HEAD"),
        "refs": git(primary, "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads"),
        "index": git(primary, "ls-files", "-s"),
        "status": git(primary, "status", "--porcelain=v1", "--untracked-files=all"),
        "stash": git(primary, "stash", "list", "--format=%H"),
        "notes": (primary / "notes.md").read_text(),
    }


def run(script, estate, extra_env, *args):
    bare, primary, home, bindir = estate
    env = {
        **GIT_ENV,
        "HOME": str(home),
        "PATH": f"{bindir}:{os.environ['PATH']}",
        "BLOG_MONTHLY_REPO": str(primary),
        "BLOG_TIER_CREEP_REPO": str(primary),
        "BLOG_TOS_REPO": str(home / "no-such-repo"),
        "BLOG_EMAIL_SCRIPT": str(home / "send-email.cjs"),
        **extra_env,
    }
    return subprocess.run(
        ["bash", str(SCRIPTS / script), *args],
        env=env, capture_output=True, text=True, timeout=120,
    )


def worktrees(primary):
    return [x for x in git(primary, "worktree", "list", "--porcelain").splitlines()
            if x.startswith("worktree ")]


def test_calibrate_publishes_from_a_workspace_and_leaves_the_primary_checkout_alone(
        estate, tmp_path):
    bare, primary, home, bindir = estate
    claude = executable(tmp_path / "claude", f"""
[ "$PWD" = "$BLOG_REPO_DIR" ] || {{ echo "not in workspace: $PWD" >&2; exit 9; }}
case "$BLOG_REPO_DIR" in "{primary}"*) exit 8 ;; esac
printf '# Calibration 2026-09\\n%0120d\\n' 0 > "$BLOG_REPO_DIR/{METH}/calibration-2026-09.md"
echo '{{"pattern_id":"p"}}' >> "$BLOG_REPO_DIR/{METH}/patterns.jsonl"
echo stray > "$BLOG_REPO_DIR/notes.md"
printf 'report %0200d\\n' 0
""")
    before = snapshot(primary)
    proc = run("blog-monthly-calibrate.sh", estate, {
        "BLOG_CLAUDE_BIN": str(claude),
        "BLOG_CALIBRATE_STATE_DIR": str(home / "state"),
    }, "2026-09")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert snapshot(primary) == before
    published = git(bare, "show", f"master:{METH}/calibration-2026-09.md")
    assert published.startswith("# Calibration 2026-09")
    assert "pattern_id" in git(bare, "show", f"master:{METH}/patterns.jsonl")
    # Only the job's own outputs are published; the stray edit stays in the workspace.
    assert git(bare, "show", "master:notes.md") == "seed"
    assert len(worktrees(primary)) == 1
    assert (home / ".local/state/intent-os/liveness/blog-monthly-calibrate.ok").exists()


def test_calibrate_push_failure_keeps_the_workspace_and_the_next_run_republishes(
        estate, tmp_path):
    bare, primary, home, bindir = estate
    claude = executable(tmp_path / "claude", f"""
printf '# Calibration 2026-08\\n%0120d\\n' 0 > "$BLOG_REPO_DIR/{METH}/calibration-2026-08.md"
printf 'report %0200d\\n' 0
""")
    hook = executable(bare / "hooks" / "pre-receive", "exit 1\n")
    env = {"BLOG_CLAUDE_BIN": str(claude), "BLOG_CALIBRATE_STATE_DIR": str(home / "state")}
    before = snapshot(primary)
    proc = run("blog-monthly-calibrate.sh", estate, env, "2026-08")
    assert proc.returncode == 1
    assert "calibrate output NOT published" in proc.stdout, proc.stdout
    assert (home / "state/workspace-2026-08").is_dir()
    assert snapshot(primary) == before
    hook.unlink()
    executable(tmp_path / "claude", "exit 1\n")   # a second generation must not be needed
    proc = run("blog-monthly-calibrate.sh", estate, env, "2026-07")
    assert "workspace-2026-08: pushed" in proc.stdout
    assert git(bare, "show", f"master:{METH}/calibration-2026-08.md").startswith("# Calibration")
    assert not (home / "state/workspace-2026-08").exists()
    assert snapshot(primary) == before


def test_calibrate_refuses_to_publish_paths_outside_its_outputs(estate, tmp_path):
    bare, primary, home, bindir = estate
    claude = executable(tmp_path / "claude", f"""
printf '# Calibration 2026-09\\n' > "$BLOG_REPO_DIR/{METH}/calibration-2026-09.md"
echo hijack > "$BLOG_REPO_DIR/notes.md"
git -C "$BLOG_REPO_DIR" commit -qam "producer committed an unrelated file"
printf 'report %0200d\\n' 0
""")
    tip = git(bare, "rev-parse", "master")
    proc = run("blog-monthly-calibrate.sh", estate, {
        "BLOG_CLAUDE_BIN": str(claude), "BLOG_CALIBRATE_STATE_DIR": str(home / "state"),
    }, "2026-09")
    assert proc.returncode == 1
    assert "refused: commits touch paths outside" in proc.stdout
    assert git(bare, "rev-parse", "master") == tip


def test_retro_publishes_from_a_workspace_and_leaves_the_primary_checkout_alone(
        estate, tmp_path):
    bare, primary, home, bindir = estate
    prev = dt.date.today().replace(day=1) - dt.timedelta(days=1)
    rel = f"content/monthly-recaps/{prev.strftime('%B').lower()}-{prev.year}.md"
    claude = executable(tmp_path / "claude", f"""
[ "$PWD" = "$BLOG_REPO_DIR" ] || exit 9
printf "+++\\ntitle = 'Retro'\\n+++\\nbody\\n" > "$BLOG_REPO_DIR/{rel}"
git -C "$BLOG_REPO_DIR" add {rel} && git -C "$BLOG_REPO_DIR" commit -qm "post: retro"
""")
    before = snapshot(primary)
    env = {"BLOG_CLAUDE_BIN": str(claude), "BLOG_RETRO_STATE_DIR": str(home / "state")}
    proc = run("blog-monthly-retro.sh", estate, env)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert snapshot(primary) == before
    assert "title = 'Retro'" in git(bare, "show", f"master:{rel}")
    assert len(worktrees(primary)) == 1
    # Second run: the retro is on origin, so it is a no-op that never opens a workspace.
    proc = run("blog-monthly-retro.sh", estate, env)
    assert proc.returncode == 0 and "Retro already on origin" in proc.stdout
    assert snapshot(primary) == before


def test_tier_creep_guard_reads_fresh_origin_not_the_primary_checkout(estate, tmp_path):
    bare, primary, home, bindir = estate
    # Commit the real guard and record-kind module to origin, then make the primary
    # checkout's copy of decisions.jsonl unreadable garbage: the guard must not see it.
    for rel in (".claude/skills/blog-backfill/scripts/tier-creep-guard.py",
                "scripts/blog/blogpipe/records.py"):
        clone = tmp_path / "pusher"
        if not clone.exists():
            git(tmp_path, "clone", "-q", str(bare), str(clone))
        (clone / rel).parent.mkdir(parents=True, exist_ok=True)
        (clone / rel).write_bytes((ROOT / rel).read_bytes())
    fixture = ROOT / "tests/fixtures/calibration-2026-09/decisions.jsonl"
    (clone / METH / "decisions.jsonl").write_bytes(fixture.read_bytes())
    git(clone, "add", ".")
    git(clone, "commit", "-qm", "guard + decisions")
    git(clone, "push", "-q", "origin", "HEAD:master")
    (primary / METH / "decisions.jsonl").write_text("this is not the data\n")
    before = snapshot(primary)
    proc = run("blog-tier-creep-guard.sh", estate, {
        "BLOG_TIER_CREEP_STATE_DIR": str(home / "state"),
        "TIER_CREEP_STATE": str(home / "state/state.json"),
    })
    assert proc.returncode in (0, 1), proc.stdout + proc.stderr
    assert "snapshot: origin/master @" in proc.stdout
    assert "Insufficient" not in proc.stdout and "FATAL" not in proc.stdout
    assert snapshot(primary) == before
    assert not list((home / "state").glob("snapshot.*"))


def test_no_periodic_wrapper_commits_or_normalizes_the_primary_checkout():
    for name in ("blog-monthly-calibrate.sh", "blog-monthly-retro.sh",
                 "blog-tier-creep-guard.sh", "blog-feedback-sweep.sh"):
        text = (SCRIPTS / name).read_text()
        code = "\n".join(x for x in text.splitlines() if not x.lstrip().startswith("#"))
        assert "preflight_branch_normalize" not in code, name
        assert 'git -C "$BLOG_DIR" commit' not in code, name
        assert 'git -C "$BLOG_DIR" push' not in code, name
        assert 'reconcile_repo "$BLOG_DIR"' not in code, name
