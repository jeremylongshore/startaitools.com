"""Feedback-sweep outcome contract and two-writer feedback.jsonl persistence.

Hermetic: bare remotes and clones under tmp_path, a stub mailer and a stub alert
runtime. Never touches the primary checkout, a mailbox, Buzz, or GitHub.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
HELPER = SCRIPTS / "blog-feedback-records.py"
WRAPPER = SCRIPTS / "blog-feedback-sweep.sh"
LIB = SCRIPTS / "lib-cron-common.sh"
SWEEP_PY = ROOT / ".claude/skills/blog-backfill/scripts/feedback-sweep.py"
FEEDBACK_REL = ".claude/skills/blog-backfill/methodology/feedback.jsonl"
DECISIONS_REL = ".claude/skills/blog-backfill/methodology/decisions.jsonl"
SWEEP_REL = ".claude/skills/blog-backfill/scripts/feedback-sweep.py"
RECORDS_REL = "scripts/blog/blogpipe/records.py"

spec = importlib.util.spec_from_file_location("blog_feedback_records", HELPER)
records = importlib.util.module_from_spec(spec)
spec.loader.exec_module(records)

GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@example.invalid",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@example.invalid",
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
}


@pytest.fixture(autouse=True)
def _hermetic_git_identity(monkeypatch):
    """records.main() runs in-process and inherits os.environ, not GIT_ENV.

    A CI runner has no global git identity, so without this commit-tree fails
    with "Author identity unknown" (seen on PR #113's first CI run).
    """
    for key, value in GIT_ENV.items():
        if key.startswith("GIT_"):
            monkeypatch.setenv(key, value)


def git(cwd, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(cwd), *args], env=GIT_ENV, check=check, capture_output=True, text=True
    )


def row(slug, source="structural_auto_confirm", **extra):
    return {"slug": slug, "source": source, "date_assessed": "2026-10-04", **extra}


def line(record):
    return json.dumps(record)


def jsonl(*recs):
    return "".join(line(r) + "\n" for r in recs)


# --------------------------------------------------------------------------- #
# Outcome contract: the single status/exit mapping
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "grade,local,remote,notify,status,rc",
    [
        ("ok", "ok", "published", "ok", "OK", 0),
        ("ok", "ok", "nothing_pending", "ok", "OK", 0),
        ("ok", "ok", "already_present", "ok", "OK", 0),
        ("skipped", "ok", "published", "ok", "OK", 0),  # --publish-pending
        ("failed", "skipped", "skipped", "ok", "FAILED", 1),
        ("ok", "failed", "skipped", "ok", "FAILED", 1),
        ("ok", "ok", "deferred", "ok", "DEFERRED", 75),
        ("ok", "ok", "exhausted", "ok", "FAILED", 1),
        ("ok", "ok", "conflict", "ok", "FAILED", 1),
        ("ok", "ok", "invalid_base", "ok", "FAILED", 1),
        ("ok", "ok", "error", "ok", "FAILED", 1),
        ("ok", "ok", "published", "failed", "DEGRADED", 2),
        ("ok", "ok", "deferred", "failed", "DEFERRED", 75),
    ],
)
def test_outcome_mapping(grade, local, remote, notify, status, rc):
    result = records.outcome(grade, local, remote, notify, deferred_runs=1, max_deferred_runs=3)
    assert (result["status"], result["rc"]) == (status, rc)
    # .ok may be written only for a full success; never for a failed stage.
    assert result["write_ok"] is (rc == 0)
    if rc:
        assert result["reasons"]


# --------------------------------------------------------------------------- #
# Record-level merge
# --------------------------------------------------------------------------- #
def test_merge_dedupes_identical_and_keeps_distinct():
    base = jsonl(row("a"), row("b", source="length_gate_downgrade", run_id="r1"))
    pending = [
        (line(r), r)
        for r in (
            row("a"),  # identical -> dedupe
            row("b"),  # same slug, other source -> keep
            row("b", source="length_gate_downgrade", run_id="r2"),  # other run -> keep
            row("c"),
        )
    ]
    out = records.merge(base, pending)
    assert out["added"] == 3 and out["duplicates"] == 1
    assert out["text"].startswith(base)  # base bytes never rewritten
    assert len(out["text"].splitlines()) == 5


def test_merge_identical_ignores_key_order_and_whitespace():
    base = '{"source": "structural_auto_confirm", "slug": "a", "date_assessed": "2026-10-04"}\n'
    r = row("a")
    assert records.merge(base, [(line(r), r)])["duplicates"] == 1


def test_merge_same_key_different_content_is_a_conflict_not_a_drop():
    base = jsonl(row("a"))
    changed = row("a", date_assessed="2026-10-11")
    with pytest.raises(records.RecordConflict) as exc:
        records.merge(base, [(line(changed), changed)])
    assert exc.value.conflicts[0]["key"][0] == "a"


def test_merge_refuses_a_base_with_conflict_markers():
    base = jsonl(row("a")) + "<<<<<<< HEAD\n" + jsonl(row("b")) + "=======\n>>>>>>> x\n"
    with pytest.raises(records.InvalidJsonl):
        records.merge(base, [(line(row("c")), row("c"))])


def test_merge_adds_missing_trailing_newline():
    out = records.merge(line(row("a")), [(line(row("b")), row("b"))])
    assert out["text"].splitlines() == [line(row("a")), line(row("b"))]


def test_stage_rejects_a_grader_that_rewrote_history(tmp_path):
    seeded = tmp_path / "seed"
    graded = tmp_path / "graded"
    pending = tmp_path / "pending"
    seeded.write_text(jsonl(row("a")))
    graded.write_text(jsonl(row("z")))
    rc = records.main(
        ["stage", "--seeded", str(seeded), "--graded", str(graded), "--pending", str(pending)]
    )
    assert rc == records.EXIT_ERROR and not pending.exists()


def test_stage_local_persistence_failure_is_reported(tmp_path, capsys):
    seeded = tmp_path / "seed"
    graded = tmp_path / "graded"
    seeded.write_text(jsonl(row("a")))
    graded.write_text(jsonl(row("a"), row("b")))
    locked = tmp_path / "locked"
    locked.mkdir()
    locked.chmod(0o500)
    try:
        rc = records.main(
            [
                "stage",
                "--seeded",
                str(seeded),
                "--graded",
                str(graded),
                "--pending",
                str(locked / "pending.jsonl"),
            ]
        )
    finally:
        locked.chmod(0o700)
    assert rc == records.EXIT_ERROR
    assert json.loads(capsys.readouterr().out)["status"] == "error"


# --------------------------------------------------------------------------- #
# Git fixtures: a bare remote, the "sweep" clone, and a "lander" clone
# --------------------------------------------------------------------------- #
@pytest.fixture
def remote(tmp_path):
    bare = tmp_path / "remote.git"
    git(tmp_path, "init", "-q", "--bare", "--initial-branch=master", str(bare))
    seed = tmp_path / "seed"
    git(tmp_path, "clone", "-q", str(bare), str(seed))
    (seed / FEEDBACK_REL).parent.mkdir(parents=True)
    (seed / FEEDBACK_REL).write_text(jsonl(row("old")))
    git(seed, "add", ".")
    git(seed, "commit", "-qm", "seed")
    git(seed, "push", "-q", "origin", "HEAD:master")
    return bare


def clone(tmp_path, bare, name):
    path = tmp_path / name
    git(tmp_path, "clone", "-q", str(bare), str(path))
    return path


def lander_append(lander, record):
    git(lander, "pull", "-q", "--ff-only", "origin", "master")
    with (lander / FEEDBACK_REL).open("a") as handle:
        handle.write(line(record) + "\n")
    git(lander, "commit", "-qam", f"post: {record['slug']}")
    git(lander, "push", "-q", "origin", "HEAD:master")


def origin_rows(bare):
    text = subprocess.run(
        ["git", "--git-dir", str(bare), "show", f"master:{FEEDBACK_REL}"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [json.loads(x) for x in text.splitlines() if x.strip()]


def publish_args(repo, state, **kw):
    args = [
        "publish",
        "--repo",
        str(repo),
        "--branch",
        "master",
        "--pending",
        str(state / "pending.jsonl"),
        "--meta",
        str(state / "meta.json"),
        "--message",
        "chore(methodology): test sweep",
    ]
    kw.setdefault("backoff", 0)  # no real sleeping in tests unless asked for
    for key, value in kw.items():
        args += [f"--{key.replace('_', '-')}", str(value)]
    return args


def test_publish_backs_off_linearly_between_attempts(tmp_path, remote, monkeypatch, capsys):
    sweep = clone(tmp_path, remote, "sweep")
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending.jsonl").write_text(jsonl(row("s1")))
    hook = remote / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    slept = []
    monkeypatch.setattr(records.time, "sleep", slept.append)
    rc = records.main(publish_args(sweep, state, attempts=3, backoff=1.5))
    assert rc == records.EXIT_DEFERRED
    assert slept == [1.5, 3.0]  # before attempts 2 and 3, never after the last
    capsys.readouterr()


def test_publish_survives_a_lander_push_between_fetch_and_push(
    tmp_path, remote, monkeypatch, capsys
):
    sweep = clone(tmp_path, remote, "sweep")
    lander = clone(tmp_path, remote, "lander")
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending.jsonl").write_text(jsonl(row("s1"), row("s2")))
    head_before = git(sweep, "rev-parse", "HEAD").stdout
    status_before = git(sweep, "status", "--porcelain").stdout

    real_git = records.git
    raced = {"done": False}

    def racing_git(repo, *args, **kw):
        if args[:1] == ("push",) and not raced["done"]:
            raced["done"] = True
            lander_append(lander, row("s1", source="length_gate_downgrade", run_id="r9"))
        return real_git(repo, *args, **kw)

    monkeypatch.setattr(records, "git", racing_git)
    assert records.main(publish_args(sweep, state)) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "published" and report["attempt"] == 2
    keys = [(r["slug"], r["source"]) for r in origin_rows(remote)]
    assert keys == [
        ("old", "structural_auto_confirm"),
        ("s1", "length_gate_downgrade"),  # the lander's row survived
        ("s1", "structural_auto_confirm"),
        ("s2", "structural_auto_confirm"),
    ]
    assert not (state / "pending.jsonl").exists()  # cleared only after verify-back
    # The sweep never touched its clone's working tree, index or HEAD.
    assert git(sweep, "rev-parse", "HEAD").stdout == head_before
    assert git(sweep, "status", "--porcelain").stdout == status_before


def test_publish_is_idempotent_when_rows_already_landed(tmp_path, remote, capsys):
    sweep = clone(tmp_path, remote, "sweep")
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending.jsonl").write_text(jsonl(row("old")))
    assert records.main(publish_args(sweep, state)) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "already_present"
    assert len(origin_rows(remote)) == 1


def test_publish_conflict_publishes_nothing_and_keeps_the_queue(tmp_path, remote, capsys):
    sweep = clone(tmp_path, remote, "sweep")
    state = tmp_path / "state"
    state.mkdir()
    queued = jsonl(row("old", date_assessed="2026-10-11"), row("new"))
    (state / "pending.jsonl").write_text(queued)
    assert records.main(publish_args(sweep, state)) == records.EXIT_CONFLICT
    assert json.loads(capsys.readouterr().out)["status"] == "conflict"
    assert [r["slug"] for r in origin_rows(remote)] == ["old"]  # "new" NOT half-published
    assert (state / "pending.jsonl").read_text() == queued


def test_publish_push_failure_defers_then_exhausts_and_retry_recovers(tmp_path, remote, capsys):
    sweep = clone(tmp_path, remote, "sweep")
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending.jsonl").write_text(jsonl(row("s1")))
    hook = remote / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\necho rejected by test >&2\nexit 1\n")
    hook.chmod(0o755)

    assert (
        records.main(publish_args(sweep, state, attempts=2, max_deferred_runs=2))
        == records.EXIT_DEFERRED
    )
    first = json.loads(capsys.readouterr().out)
    assert (first["status"], first["deferred_runs"]) == ("deferred", 1)
    assert (
        records.main(publish_args(sweep, state, attempts=1, max_deferred_runs=2))
        == records.EXIT_DEFERRED
    )
    assert json.loads(capsys.readouterr().out)["status"] == "exhausted"
    assert (state / "pending.jsonl").exists()  # never dropped

    hook.unlink()  # remote healthy again
    assert records.main(publish_args(sweep, state)) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "published"
    assert [r["slug"] for r in origin_rows(remote)] == ["old", "s1"]
    assert not (state / "meta.json").exists()  # counter reset on success


def test_publish_commit_failure_defers_without_losing_rows(tmp_path, remote, capsys):
    sweep = clone(tmp_path, remote, "sweep")
    state = tmp_path / "state"
    state.mkdir()
    (state / "pending.jsonl").write_text(jsonl(row("s1")))
    objects = sweep / ".git/objects"
    dirs = [objects, *[p for p in objects.rglob("*") if p.is_dir()]]
    for d in dirs:
        d.chmod(0o555)
    try:
        rc = records.main(publish_args(sweep, state, attempts=1))
    finally:
        for d in dirs:
            d.chmod(0o755)
    assert rc == records.EXIT_DEFERRED
    assert json.loads(capsys.readouterr().out)["status"] in ("deferred", "exhausted")
    assert (state / "pending.jsonl").read_text() == jsonl(row("s1"))
    assert [r["slug"] for r in origin_rows(remote)] == ["old"]


def test_two_concurrent_publishers_lose_no_records(tmp_path, remote):
    """Two real processes from two clones race to the same bare remote."""
    procs = []
    for name in ("one", "two"):
        work = clone(tmp_path, remote, name)
        state = tmp_path / f"state-{name}"
        state.mkdir()
        (state / "pending.jsonl").write_text(
            jsonl(*[row(f"{name}-{i}") for i in range(5)], row("shared"))
        )
        procs.append(
            subprocess.Popen(
                [sys.executable, str(HELPER), *publish_args(work, state, attempts=20)],
                env=GIT_ENV,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        )
    for proc in procs:
        out, err = proc.communicate(timeout=120)
        assert proc.returncode == 0, (out, err)
    slugs = [r["slug"] for r in origin_rows(remote)]
    assert sorted(slugs) == sorted(
        ["old", "shared"] + [f"{n}-{i}" for n in ("one", "two") for i in range(5)]
    )
    assert slugs.count("shared") == 1  # identical row deduped


# --------------------------------------------------------------------------- #
# push_with_rebase (PR #109): a failed abort must be reported, not hidden
# --------------------------------------------------------------------------- #
def test_push_with_rebase_reports_a_failed_abort(tmp_path, remote):
    a = clone(tmp_path, remote, "a")
    lander = clone(tmp_path, remote, "lander")
    lander_append(lander, row("theirs"))
    with (a / FEEDBACK_REL).open("a") as handle:
        handle.write(line(row("ours")) + "\n")
    git(a, "commit", "-qam", "ours")
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    real = shutil.which("git")
    (fakebin / "git").write_text(
        "#!/bin/sh\n"
        'if [ "$1" = rebase ] && [ "$2" = --abort ]; then\n'
        "  echo simulated abort failure >&2; exit 1\n"
        "fi\n"
        f'exec {real} "$@"\n'
    )
    (fakebin / "git").chmod(0o755)
    log = tmp_path / "push.log"
    env = {**GIT_ENV, "PATH": f"{fakebin}:{os.environ['PATH']}", "INTENT_RUNTIME": "/nonexistent"}
    proc = subprocess.run(
        ["bash", "-c", f'source "{LIB}"; cd "{a}" && push_with_rebase master "{log}" 2'],
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "FATAL: could not abort the failed rebase" in log.read_text()


# --------------------------------------------------------------------------- #
# The wrapper end to end
# --------------------------------------------------------------------------- #
POST = "+++\ntitle = '{title}'\ndate = 2026-09-0{n}\n+++\n\n" + "body line\n" * 20


@pytest.fixture
def blog(tmp_path):
    bare = tmp_path / "blog.git"
    git(tmp_path, "init", "-q", "--bare", "--initial-branch=master", str(bare))
    seed = tmp_path / "blog-seed"
    git(tmp_path, "clone", "-q", str(bare), str(seed))
    (seed / SWEEP_REL).parent.mkdir(parents=True)
    shutil.copy(SWEEP_PY, seed / SWEEP_REL)
    # The sweep selects classifier decisions through the shared record-kind module.
    (seed / RECORDS_REL).parent.mkdir(parents=True)
    shutil.copy(ROOT / RECORDS_REL, seed / RECORDS_REL)
    (seed / "content/posts").mkdir(parents=True)
    decisions = []
    for n, slug in enumerate(("post-a", "post-b", "post-c"), start=1):
        (seed / f"content/posts/{slug}.md").write_text(POST.format(title=slug, n=n))
        decisions.append({"slug": slug, "tier": 1, "dimensions": {"tch": 2}})
    (seed / DECISIONS_REL).parent.mkdir(parents=True, exist_ok=True)
    (seed / DECISIONS_REL).write_text(jsonl(*decisions))
    (seed / FEEDBACK_REL).write_text(
        jsonl(row("post-a", source="length_gate_downgrade", run_id="r1"))
    )
    git(seed, "add", ".")
    git(seed, "commit", "-qm", "seed")
    git(seed, "push", "-q", "origin", "HEAD:master")
    primary = tmp_path / "primary"
    git(tmp_path, "clone", "-q", str(bare), str(primary))
    home = tmp_path / "home"
    home.mkdir()
    calls = tmp_path / "calls"
    calls.mkdir()
    runtime = tmp_path / "runtime.sh"
    runtime.write_text(f'cron_fail() {{ printf "%s|%s\\n" "$1" "$2" >> "{calls}/cron_fail"; }}\n')
    mailer = tmp_path / "mailer.cjs"
    mailer.write_text(
        "const fs=require('fs');const a=process.argv;\n"
        f"fs.appendFileSync('{calls}/mail', a[a.indexOf('--subject')+1]+'\\n');\n"
        "process.exit(process.env.MAIL_FAIL==='1'?1:0);\n"
    )
    return {
        "bare": bare,
        "primary": primary,
        "home": home,
        "calls": calls,
        "runtime": runtime,
        "mailer": mailer,
        "state": tmp_path / "sweep-state",
    }


def run_wrapper(blog, *args, **env):
    full = {
        **GIT_ENV,
        "HOME": str(blog["home"]),
        "INTENT_RUNTIME": str(blog["runtime"]),
        "BLOG_FEEDBACK_REPO": str(blog["primary"]),
        "BLOG_FEEDBACK_STATE_DIR": str(blog["state"]),
        "BLOG_FEEDBACK_EMAIL_SCRIPT": str(blog["mailer"]),
        "BLOG_FEEDBACK_PUSH_BACKOFF": "0",
        **env,
    }
    return subprocess.run(
        ["bash", str(WRAPPER), *args], env=full, capture_output=True, text=True, timeout=120
    )


def markers(blog):
    live = blog["home"] / ".local/state/intent-os/liveness"
    return (live / "blog-feedback-sweep.beat").exists(), (live / "blog-feedback-sweep.ok").exists()


def calls(blog, name):
    path = blog["calls"] / name
    return path.read_text().splitlines() if path.exists() else []


def test_wrapper_ok_publishes_and_never_touches_the_primary_checkout(blog):
    head = git(blog["primary"], "rev-parse", "HEAD").stdout
    proc = run_wrapper(blog)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    rows = origin_rows(blog["bare"])
    assert [(r["slug"], r["source"]) for r in rows] == [
        ("post-a", "length_gate_downgrade"),  # lander row: not regraded, kept
        ("post-b", "structural_auto_confirm"),
        ("post-c", "structural_auto_confirm"),
    ]
    assert markers(blog) == (True, True)
    assert calls(blog, "mail")[-1].endswith("— OK")
    assert calls(blog, "cron_fail") == []
    assert git(blog["primary"], "rev-parse", "HEAD").stdout == head
    assert git(blog["primary"], "status", "--porcelain").stdout == ""
    # Second run: nothing new, still OK, nothing duplicated.
    assert run_wrapper(blog).returncode == 0
    assert len(origin_rows(blog["bare"])) == 3


def test_wrapper_push_failure_is_deferred_not_ok_then_recovers(blog):
    hook = blog["bare"] / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    proc = run_wrapper(blog, BLOG_FEEDBACK_PUSH_ATTEMPTS="1")
    assert proc.returncode == 75, proc.stdout
    assert markers(blog) == (True, False)  # no .ok for a deferral
    assert calls(blog, "mail")[-1].endswith("— DEFERRED")
    assert "DEFERRED" in calls(blog, "cron_fail")[-1]
    pending = blog["state"] / "pending-feedback.jsonl"
    assert len(pending.read_text().splitlines()) == 2
    # A later grading run must not mint conflicting duplicates of queued rows.
    proc = run_wrapper(blog, BLOG_FEEDBACK_PUSH_ATTEMPTS="1")
    assert proc.returncode == 75
    assert len(pending.read_text().splitlines()) == 2
    hook.unlink()
    proc = run_wrapper(blog, "--publish-pending")
    assert proc.returncode == 0, proc.stdout
    assert markers(blog) == (True, True)
    assert not pending.exists()
    assert len(origin_rows(blog["bare"])) == 3


def test_wrapper_deferral_cap_escalates_to_failed(blog):
    hook = blog["bare"] / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o755)
    proc = run_wrapper(blog, BLOG_FEEDBACK_PUSH_ATTEMPTS="1", BLOG_FEEDBACK_MAX_DEFERRED_RUNS="1")
    assert proc.returncode == 1
    assert markers(blog) == (True, False)
    assert calls(blog, "mail")[-1].endswith("— FAILED")


def test_wrapper_email_failure_is_degraded(blog):
    proc = run_wrapper(blog, MAIL_FAIL="1")
    assert proc.returncode == 2
    assert markers(blog) == (True, False)
    assert "DEGRADED" in calls(blog, "cron_fail")[-1]
    assert len(origin_rows(blog["bare"])) == 3  # records still persisted


def test_wrapper_grade_failure_is_failed(blog):
    seed = blog["primary"]
    (seed / DECISIONS_REL).unlink()
    git(seed, "commit", "-qam", "drop decisions")
    git(seed, "push", "-q", "origin", "HEAD:master")
    proc = run_wrapper(blog)
    assert proc.returncode == 1
    assert markers(blog) == (True, False)
    assert calls(blog, "mail")[-1].endswith("— FAILED")


def test_wrapper_names_the_missing_path_when_origin_lacks_an_input(blog, tmp_path):
    other = tmp_path / "remover"
    git(tmp_path, "clone", "-q", str(blog["bare"]), str(other))
    git(other, "rm", "-q", FEEDBACK_REL)
    git(other, "commit", "-qm", "drop feedback")
    git(other, "push", "-q", "origin", "HEAD:master")
    proc = run_wrapper(blog)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    log = "".join(p.read_text() for p in blog["state"].glob("sweep-*.log"))
    assert f"is missing: {FEEDBACK_REL}" in log
    assert "snapshot or seed failed" not in log
    assert markers(blog) == (True, False)


def test_wrapper_reaps_snapshot_dirs_left_by_a_killed_run(blog):
    stale = blog["state"] / "snapshot.KILLED"
    (stale / "content").mkdir(parents=True)
    proc = run_wrapper(blog)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert not stale.exists()
    assert not list(blog["state"].glob("snapshot.*"))
