"""Catch-up planner: which recent dates have no post, and is another attempt allowed?"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts/blog"))
from blogpipe import catchup  # noqa: E402

SCRIPT = ROOT / "scripts/blog/blog-catchup.py"


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    (root / "content/posts").mkdir(parents=True)
    git(root.parent, "init", "-q", "-b", "master", str(root))
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "user.name", "fixture")
    posts = {
        "toml-post": '+++\ntitle = "a"\ndate = 2026-09-19T08:00:00-06:00\n+++\nbody\n',
        "yaml-post": "---\ntitle: b\ndate: 2026-09-17T08:00:00-06:00\n---\nbody\n",
        "quoted": '+++\ntitle = "c"\ndate = "2026-09-16T08:00:00-06:00"\n+++\nbody\n',
        # A body line that merely MENTIONS a date must not count as a post for that date.
        "mentions": '+++\ntitle = "d"\ndate = 2026-09-10T08:00:00-06:00\n+++\nOn 2026-09-18 x.\n',
    }
    for name, text in posts.items():
        (root / "content/posts" / f"{name}.md").write_text(text)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "fixture posts")
    return root


def test_dates_are_read_from_front_matter_in_toml_yaml_and_quoted_forms(repo):
    window = ["2026-09-19", "2026-09-18", "2026-09-17", "2026-09-16"]
    assert catchup.published_dates(repo, "master", window) == {
        "2026-09-19",
        "2026-09-17",
        "2026-09-16",
    }


def test_the_window_looks_back_from_the_target_and_tries_the_newest_gap_first(repo):
    result = catchup.plan(repo, "master", "2026-09-20", 6, 3, {})
    assert result["attempt"] == ["2026-09-18", "2026-09-15", "2026-09-14"]
    assert result["gave_up"] == [] and "2026-09-20" not in result["published"]


def test_a_date_stops_costing_attempts_at_the_cap_and_is_reported_exactly_once(repo):
    state = {"2026-09-18": {"attempts": 3}}
    first = catchup.plan(repo, "master", "2026-09-20", 3, 3, state)
    assert first["attempt"] == [] and first["newly_gave_up"] == ["2026-09-18"]
    state = catchup.record(state, "2026-09-18", "gave-up-reported", "now")
    again = catchup.plan(repo, "master", "2026-09-20", 3, 3, state)
    assert again["gave_up"] == ["2026-09-18"] and again["newly_gave_up"] == []


def test_recording_an_attempt_counts_up_and_keeps_the_first_miss(repo):
    state = catchup.record({}, "2026-09-18", "attempt", "t1")
    state = catchup.record(state, "2026-09-18", "attempt", "t2")
    assert state["2026-09-18"] == {"attempts": 2, "last_attempt": "t2", "first_missed": "t1"}
    with pytest.raises(ValueError):
        catchup.record(state, "2026-09-18", "celebrate", "t3")


def test_old_state_is_pruned_so_the_file_cannot_grow_forever():
    state = {"2026-07-01": {"attempts": 3}, "2026-09-18": {"attempts": 1}}
    assert list(catchup.prune(state, "2026-09-20")) == ["2026-09-18"]


def test_a_corrupt_state_file_is_treated_as_empty_not_as_a_crash(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("{not json")
    assert catchup.load_state(path) == {}
    path.write_text("[1,2]")
    assert catchup.load_state(path) == {}


def test_planning_trouble_never_fails_the_night(repo, tmp_path):
    """A bad ref must yield an empty plan and exit 0: catch-up is a bonus, not a gate."""
    done = subprocess.run(
        [sys.executable, str(SCRIPT), "--state", str(tmp_path / "s.json"), "plan", "--repo"]
        + [str(repo), "--ref", "no-such-ref", "--target", "2026-09-20"],
        capture_output=True,
        text=True,
    )
    assert done.returncode == 0, done.stderr
    result = json.loads(done.stdout)
    assert result["attempt"] == [] and "error" in result


def test_the_command_line_round_trips_plan_record_plan(repo, tmp_path):
    state = tmp_path / "nested/dir/state.json"
    base = [sys.executable, str(SCRIPT), "--state", str(state)]
    planned = [*base, "plan", "--repo", str(repo), "--ref", "master", "--target", "2026-09-19"]
    planned += ["--days", "1", "--max-attempts", "2"]
    first = json.loads(subprocess.check_output(planned, text=True))
    assert first["attempt"] == ["2026-09-18"]
    for _ in range(2):
        subprocess.check_call([*base, "record", "--date", "2026-09-18", "--outcome", "attempt"])
    second = json.loads(subprocess.check_output(planned, text=True))
    assert second["attempt"] == [] and second["newly_gave_up"] == ["2026-09-18"]
    assert json.loads(state.read_text())["2026-09-18"]["attempts"] == 2
