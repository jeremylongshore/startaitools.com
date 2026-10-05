"""Estate activity inventory: one identity is counted once, on its remote default branch."""

import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("estate_activity",
                                              ROOT / "scripts/blog/estate-activity.py")
ea = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ea)


def git(repo, *args, env=None):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env={**os.environ, **(env or {})})


def commit(repo, msg, when, author="Jeremy Longshore", email="jeremy@example.invalid"):
    env = {"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when,
           "GIT_AUTHOR_NAME": author, "GIT_AUTHOR_EMAIL": email,
           "GIT_COMMITTER_NAME": author, "GIT_COMMITTER_EMAIL": email}
    git(repo, "commit", "-q", "--allow-empty", "-m", msg, env=env)


@pytest.fixture
def estate(tmp_path):
    origin = tmp_path / "remote" / "jeremylongshore" / "site.git"
    origin.parent.mkdir(parents=True)
    git(tmp_path, "init", "-q", "--bare", "-b", "master", str(origin))
    seed = tmp_path / "seed"
    git(tmp_path, "init", "-q", "-b", "master", str(seed))
    commit(seed, "august", "2026-08-31T23:30:00-06:00")
    commit(seed, "in window", "2026-09-10T12:00:00-06:00")
    commit(seed, "bot", "2026-09-11T12:00:00-06:00", "github-actions[bot]", "bot@example.invalid")
    commit(seed, "upper edge", "2026-10-01T00:00:00-06:00")
    git(seed, "remote", "add", "origin", f"git@github.com:{origin.parent.name}/site.git")
    git(seed, "push", "-q", str(origin), "master")

    projects = tmp_path / "projects"
    fresh = projects / "blog" / "site"
    stale = projects / "site-old"
    for clone, depth in ((fresh, None), (stale, "1")):
        clone.parent.mkdir(parents=True, exist_ok=True)
        args = ["clone", "-q", str(origin), str(clone)]
        if depth:
            args[1:1] = ["--depth", depth, "--branch", "master"]
        git(tmp_path, *args)
        git(clone, "remote", "set-url", "origin", "https://github.com/jeremylongshore/site.git")
    # The stale clone's remote ref stops at the first commit; the fresh one has all four.
    git(stale, "update-ref", "refs/remotes/origin/master",
        subprocess.run(["git", "-C", str(fresh), "rev-list", "--max-parents=0", "HEAD"],
                       capture_output=True, text=True, check=True).stdout.strip())
    git(stale, "reset", "-q", "--hard", "origin/master")
    git(fresh, "worktree", "add", "-q", str(projects / "site-wt"), "-b", "wt")

    third = projects / "upstream-thing"
    git(tmp_path, "init", "-q", "-b", "main", str(third))
    git(third, "remote", "add", "origin", "https://github.com/someone-else/thing.git")
    return projects


def run(projects):
    args = ea.argparse.Namespace(since="2026-09-01", until="2026-10-01", tz_hours=-6,
                                 root=str(projects), max_depth=3, owner=list(ea.DEFAULT_OWNERS),
                                 author=list(ea.DEFAULT_AUTHORS), fetch=False, github=False,
                                 extra=None)
    return ea.run(args)


def test_identity_normalizes_ssh_and_https():
    assert ea.identity_from_url("git@github.com:Owner/Repo.git") == "owner/repo"
    assert ea.identity_from_url("https://github.com/owner/repo") == "owner/repo"


def test_one_identity_counted_once_on_freshest_remote_ref(estate):
    res = run(estate)
    assert [r["identity"] for r in res["repos"]] == ["jeremylongshore/site"]
    row = res["repos"][0]
    assert row["path"].endswith("blog/site")  # nested canonical beats stale top-level clone
    assert row["ref"] == "refs/remotes/origin/master"
    # Half-open window: the August commit and the 10-01 00:00 commit are both outside.
    assert (row["commits"], row["non_merge"], row["authored_non_merge"]) == (2, 2, 1)


def test_exclusions_are_explicit(estate):
    reasons = {(Path(e["path"]).name, e["reason"]) for e in run(estate)["excluded"]}
    assert ("site-old", "duplicate") in reasons
    assert ("site-wt", "linked-worktree") in reasons
    assert ("upstream-thing", "third-party") in reasons


def test_output_is_deterministic(estate):
    a, b = run(estate), run(estate)
    for r in a["repos"] + b["repos"]:
        r.pop("fetch_age_hours")
    assert a == b
