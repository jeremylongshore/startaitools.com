"""Hermetic shared-writer races: no mailbox, provider, production, or Git mutation."""

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from functools import partial
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
QUEUE_SCRIPT = ROOT / ".claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"
STATE_SCRIPT = SCRIPTS / "blog_publication_state.py"


def module(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / (name + ".py"))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def write(path, rows):
    path.write_text(json.dumps(rows) + "\n")


def read(path):
    return json.loads(path.read_text())


def row():
    return {
        "slug": "fixture-post",
        "date": "2020-01-01",
        "packet_sent": False,
        "canonical_url": "https://startaitools.com/posts/fixture-post/",
        "syndication": {
            "x": {"status": "pending"},
            "li_personal": {"status": "pending"},
            "medium": {"status": "n/a"},
        },
    }


def update_command(path, patch):
    return [
        sys.executable,
        str(STATE_SCRIPT),
        "update",
        "--file",
        str(path),
        "--slug",
        "fixture-post",
        "--patch-json",
        json.dumps(patch),
    ]


def pending_update(path, patch):
    """A second process signals import completion before trying the shared lock."""
    code = (
        "import sys,json; from pathlib import Path; "
        "sys.path.insert(0,sys.argv[1]); "
        "from blog_publication_state import update_row; "
        "print('ready',flush=True); "
        "update_row(Path(sys.argv[2]),'fixture-post',json.loads(sys.argv[3])); "
        "print('updated',flush=True)"
    )
    child = subprocess.Popen(
        [sys.executable, "-c", code, str(SCRIPTS), str(path), json.dumps(patch)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert child.stdout.readline().strip() == "ready"
    return child


def packet_function():
    text = (SCRIPTS / "blog-posting-packet.sh").read_text()
    return text[text.index("mark_sent() {") : text.index("\nsend_packet() {")]


def test_packet_marker_and_image_merge_preserve_latest_nested_fields(tmp_path):
    ledger = tmp_path / ".blog-syndication-ledger.json"
    write(
        ledger,
        [
            {**row(), "image": {"cards": {"square": "existing-square"}}},
            {"slug": "other-post", "packet_sent": True},
        ],
    )
    env = {**os.environ, "BLOG_DIR": str(ROOT), "LEDGER_FILE": str(ledger), "BLOG_CANARY": "0"}
    process = subprocess.Popen(
        ["bash", "-c", packet_function() + "\nmark_sent fixture-post"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    image = module("make-post-image")
    assert image.record_in_ledger("fixture-post", {"cards": {"og": "new-og"}}, str(ledger))
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode == 0, (stdout, stderr)
    result = read(ledger)
    assert result[0]["packet_sent"] is True
    assert result[0]["image"]["cards"] == {"square": "existing-square", "og": "new-og"}
    assert result[0]["syndication"] == row()["syndication"]
    assert result[1] == {"slug": "other-post", "packet_sent": True}


@pytest.mark.parametrize(
    "lane",
    [
        "make-post-image",
        "ingest-syndication-replies",
        "syndication-reconcile",
        "reconcile-syndication-state",
    ],
)
@pytest.mark.parametrize("content", [None, "{broken", "{}", '[{"slug":"same"},{"slug":"same"}]'])
def test_python_writers_reject_missing_invalid_state(tmp_path, monkeypatch, lane, content):
    writer = module(lane)
    ledger = tmp_path / ".blog-syndication-ledger.json"
    if content is not None:
        ledger.write_text(content)
    if lane == "make-post-image":
        call = partial(writer.record_in_ledger, "fixture-post", {"image": "fixture"}, str(ledger))
    elif lane == "ingest-syndication-replies":
        monkeypatch.setattr(writer, "LEDGER", ledger)
        call = writer.load_ledger
    elif lane == "syndication-reconcile":
        monkeypatch.setattr(writer, "LEDGER", ledger)
        call = writer.load
    else:
        call = partial(writer.load, ledger)
    with pytest.raises((ValueError, FileNotFoundError)):
        call()
    assert (ledger.read_text() if ledger.exists() else None) == content


def test_reply_fetch_outside_lock_then_matches_current_receipts(tmp_path, monkeypatch):
    ingest = module("ingest-syndication-replies")
    ledger = tmp_path / ".blog-syndication-ledger.json"
    write(ledger, [row()])
    monkeypatch.setattr(ingest, "LEDGER", ledger)
    monkeypatch.setattr(ingest, "load_env", lambda: {})

    def fake_fetch(_env, _days, _sender):
        # Independent process can transact during the external-fetch phase.
        result = subprocess.run(
            update_command(
                ledger,
                {
                    "packet_sent": True,
                    "image": {"cards": {"og": "concurrent"}},
                    "syndication": {"x": {"status": "posted", "url": "https://x.com/already"}},
                },
            ),
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        return [
            {
                "subject": "fixture receipt",
                "text": "posted 2020-01-01\n"
                "X: https://x.com/late\nLinkedIn personal: https://linkedin.com/fresh",
                "from": "Operator <operator@example.invalid>",
            }
        ]

    monkeypatch.setattr(ingest, "fetch_replies", fake_fetch)
    assert ingest.cmd_ingest(argparse.Namespace(days=7, sender=None, dry_run=False)) == 0
    current = read(ledger)[0]
    assert current["packet_sent"] is True
    assert current["image"]["cards"]["og"] == "concurrent"
    assert current["syndication"]["x"]["url"] == "https://x.com/already"
    assert current["syndication"]["li_personal"]["status"] == "posted"
    assert current["syndication"]["medium"]["status"] == "n/a"


def test_local_reconcile_holds_lock_from_read_to_rename(tmp_path, monkeypatch):
    writer = module("syndication-reconcile")
    ledger = tmp_path / ".blog-syndication-ledger.json"
    write(ledger, [{**row(), "packet_sent": True}])
    monkeypatch.setattr(writer, "LEDGER", ledger)
    original = writer.load
    child = None

    def paused_read():
        nonlocal child
        rows = original()
        child = pending_update(ledger, {"image": {"cards": {"og": "concurrent"}}})
        try:
            with pytest.raises(subprocess.TimeoutExpired):
                child.wait(timeout=0.3)
        except BaseException:
            child.communicate(timeout=5)
            raise
        return rows

    monkeypatch.setattr(writer, "load", paused_read)
    assert writer.main([]) == 0
    stdout, stderr = child.communicate(timeout=5)
    assert child.returncode == 0, (stdout, stderr)
    current = read(ledger)[0]
    assert current["image"]["cards"]["og"] == "concurrent"
    assert current["syndication"]["x"]["status"] == "assumed_posted"
    assert current["syndication"]["medium"]["status"] == "n/a"


def test_legacy_reconciliation_retains_existing_delivery_and_terminal_queue(tmp_path, monkeypatch):
    writer = module("reconcile-syndication-state")
    ledger = tmp_path / ".blog-syndication-ledger.json"
    queue = tmp_path / ".crosspost-queue.json"
    existing = {**row(), "packet_sent": True, "image": {"image": "keep"}}
    terminal = {"slug": "fixture-post", "devto": {"status": "published", "url": "keep"}}
    write(ledger, [existing])
    write(queue, [terminal])
    posts = tmp_path / "content/posts"
    posts.mkdir(parents=True)
    for slug in ("fixture-post", "missing-post"):
        (posts / (slug + ".md")).write_text(
            f"+++\ntitle = '{slug}'\nslug = '{slug}'\ndate = 2020-01-01T08:00:00-06:00\n+++\nBody"
        )
    monkeypatch.setattr(writer, "ROOT", tmp_path)
    monkeypatch.setattr(writer, "LEDGER", ledger)
    monkeypatch.setattr(writer, "QUEUE", queue)
    monkeypatch.setattr(writer, "tier_for", lambda _slug: 2)
    monkeypatch.setattr(
        writer,
        "parse_args",
        lambda: argparse.Namespace(slug=["fixture-post", "missing-post"], apply=True),
    )
    assert writer.main() == 0
    assert read(ledger)[0] == existing
    assert read(queue)[0] == terminal
    assert len(read(ledger)) == len(read(queue)) == 2
    before = (ledger.read_bytes(), queue.read_bytes())
    assert writer.main() == 0
    assert before == (ledger.read_bytes(), queue.read_bytes())


@pytest.fixture
def queue_fixture(tmp_path):
    blog = tmp_path / "blog"
    (blog / "content/posts").mkdir(parents=True)
    (blog / "scripts/blog").mkdir(parents=True)
    (blog / "scripts/blog/lib-cron-common.sh").write_bytes(
        (SCRIPTS / "lib-cron-common.sh").read_bytes()
    )
    (blog / "content/posts/fixture-post.md").write_text(
        "+++\ntitle='Fixture'\nslug='fixture-post'\ndate=2020-01-01T08:00:00Z\n+++\nBody"
    )
    remote = tmp_path / "source-remote.git"
    git_env = {**os.environ, "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
    for args in (
        ["init", "--bare", "--initial-branch=master", str(remote)],
        ["-C", str(blog), "init", "--initial-branch=master"],
        ["-C", str(blog), "config", "user.name", "Offline fixture"],
        ["-C", str(blog), "config", "user.email", "fixture@example.invalid"],
        ["-C", str(blog), "add", "content/posts"],
        ["-C", str(blog), "commit", "-m", "Committed legacy fixture"],
        ["-C", str(blog), "remote", "add", "origin", str(remote)],
        ["-C", str(blog), "push", "origin", "master"],
    ):
        subprocess.run(["git", *args], env=git_env, check=True, capture_output=True)
    path = blog / ".crosspost-queue.json"
    write(
        path,
        [
            {
                "slug": "fixture-post",
                "canonical_url": "https://startaitools.com/posts/fixture-post/",
                "devto": {"status": "pending", "publish_after": "1970-01-01T00:00:00Z"},
                "hashnode": {"status": "pending", "publish_after": "1970-01-01T00:00:00Z"},
                "medium": {"status": "skipped"},
            }
        ],
    )
    transform = tmp_path / "transform"
    transform.write_text('#!/bin/sh\ncp -f "$1" "$2"\n')
    transform.chmod(0o755)
    provider = tmp_path / "provider"
    provider.write_text("""#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
sys.path.insert(0, os.environ['WRITER_SCRIPT_DIR'])
from blog_publication_state import state_locked, load_state, atomic_state, deep_merge
path = Path(os.environ['QUEUE_FIXTURE'])
# Real second-process lock acquisition proves the API phase is not holding it.
with state_locked(path.parent, timeout=2):
    rows = load_state(path)
    rows[0] = deep_merge(rows[0], json.loads(os.environ['PROVIDER_PATCH']))
    rows.append({'slug': 'concurrent-post', 'devto': {'status': 'published'}})
    atomic_state(path, rows)
if os.environ.get('PROVIDER_FAIL') == '1':
    print('fixture transient failure', file=sys.stderr)
    if os.environ.get('PROVIDER_SAFE_REJECT') == '1':
        print('CROSSPOST_SAFE_REJECTION', file=sys.stderr)
        sys.exit(75)
    sys.exit(1)
print('https://external.example/fixture-post')
""")
    provider.chmod(0o755)
    hashnode = tmp_path / "hashnode"
    hashnode.write_text(
        '#!/bin/sh\nprintf called > "$HASHNODE_MARKER"\necho https://external.example/hashnode\n'
    )
    hashnode.chmod(0o755)
    env = {
        **os.environ,
        "BLOG_DIR": str(blog),
        "BLOG_EXPECTED_REMOTE": str(remote),
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "ASTRO_SCRIPT": str(transform),
        "DEVTO_SCRIPT": str(provider),
        "DEVTO_API_KEY": "test",
        "HASHNODE_SCRIPT": str(hashnode),
        "HASHNODE_PAT": "test",
        "HASHNODE_PUBLICATION_ID": "test",
        "HASHNODE_MARKER": str(tmp_path / "hashnode-called"),
        "QUEUE_FIXTURE": str(path),
        "WRITER_SCRIPT_DIR": str(SCRIPTS),
        "BLOG_CANARY": "0",
        "PROVIDER_PATCH": json.dumps(
            {"hashnode": {"status": "published", "url": "keep"}, "concurrent_field": "keep"}
        ),
    }
    return path, env


def queue_run(env):
    return subprocess.run(
        ["bash", str(QUEUE_SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=12,
        check=False,
    )


def test_queue_result_merges_latest_and_does_not_post_advanced_other_destination(queue_fixture):
    path, env = queue_fixture
    result = queue_run(env)
    assert result.returncode == 0, result.stderr
    rows = read(path)
    assert len(rows) == 2
    assert rows[0]["devto"]["status"] == "published"
    assert rows[0]["hashnode"] == {
        "status": "published",
        "url": "keep",
        "publish_after": "1970-01-01T00:00:00Z",
    }
    assert rows[0]["concurrent_field"] == "keep"
    assert rows[1]["slug"] == "concurrent-post"
    assert not Path(env["HASHNODE_MARKER"]).exists()


def test_queue_late_failure_cannot_revert_published_destination(queue_fixture):
    path, env = queue_fixture
    env.update(
        {
            "PROVIDER_FAIL": "1",
            "PROVIDER_PATCH": json.dumps(
                {
                    "devto": {"status": "published", "url": "concurrent-proof"},
                    "hashnode": {"status": "published"},
                }
            ),
        }
    )
    result = queue_run(env)
    assert result.returncode == 0, result.stderr
    assert read(path)[0]["devto"]["status"] == "published"
    assert read(path)[0]["devto"]["url"] == "concurrent-proof"
    assert "retry_after" not in read(path)[0]["devto"]


def test_queue_retry_increments_latest_attempt_count(queue_fixture):
    path, env = queue_fixture
    env.update(
        {
            "PROVIDER_FAIL": "1",
            "PROVIDER_SAFE_REJECT": "1",
            "PROVIDER_PATCH": json.dumps(
                {"devto": {"attempts": 3}, "hashnode": {"status": "published"}}
            ),
        }
    )
    result = queue_run(env)
    assert result.returncode == 0, result.stderr
    assert read(path)[0]["devto"]["attempts"] == 4
    assert read(path)[0]["devto"]["status"] == "pending"
    assert len(read(path)) == 2


@pytest.mark.parametrize("content", [None, "{broken", "{}", '[{"slug":"same"},{"slug":"same"}]'])
def test_queue_rejects_missing_invalid_without_clearing(queue_fixture, content):
    path, env = queue_fixture
    path.unlink()
    if content is not None:
        path.write_text(content)
    result = queue_run(env)
    assert result.returncode != 0
    assert (path.read_text() if path.exists() else None) == content


def test_legacy_reconcile_read_to_rename_blocks_competing_marker(tmp_path, monkeypatch):
    writer = module("reconcile-syndication-state")
    ledger = tmp_path / ".blog-syndication-ledger.json"
    queue = tmp_path / ".crosspost-queue.json"
    write(ledger, [row()])
    write(queue, [])
    posts = tmp_path / "content/posts"
    posts.mkdir(parents=True)
    (posts / "missing-post.md").write_text(
        "+++\ntitle='Missing'\nslug='missing-post'\ndate=2020-01-01T08:00:00-06:00\n+++\nBody"
    )
    monkeypatch.setattr(writer, "ROOT", tmp_path)
    monkeypatch.setattr(writer, "LEDGER", ledger)
    monkeypatch.setattr(writer, "QUEUE", queue)
    monkeypatch.setattr(writer, "tier_for", lambda _slug: 2)
    monkeypatch.setattr(
        writer, "parse_args", lambda: argparse.Namespace(slug=["missing-post"], apply=True)
    )
    native_load = writer.load
    child = None

    def paused_read(path):
        nonlocal child
        rows = native_load(path)
        if path == ledger:
            child = pending_update(ledger, {"packet_sent": True})
            try:
                with pytest.raises(subprocess.TimeoutExpired):
                    child.wait(timeout=0.3)
            except BaseException:
                child.communicate(timeout=5)
                raise
        return rows

    monkeypatch.setattr(writer, "load", paused_read)
    assert writer.main() == 0
    stdout, stderr = child.communicate(timeout=5)
    assert child.returncode == 0, (stdout, stderr)
    assert read(ledger)[0]["packet_sent"] is True
    assert read(ledger)[1]["slug"] == read(queue)[0]["slug"] == "missing-post"


def blocking_provider(queue_fixture, tmp_path):
    """A fake request blocks on a fixture FIFO, with its inherited lease alive."""
    path, env = queue_fixture
    fifo = tmp_path / "request-release"
    os.mkfifo(fifo)
    provider = tmp_path / "blocking-provider"
    provider.write_text("""#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
sys.path.insert(0, os.environ['WRITER_SCRIPT_DIR'])
from blog_publication_state import update_row
update_row(Path(os.environ['QUEUE_FIXTURE']), 'fixture-post',
           {'hashnode': {'status': 'published', 'url': 'fixture-existing'}})
Path(os.environ['PROVIDER_PID']).write_text(str(os.getpid()))
Path(os.environ['PROVIDER_READY']).write_text('ready')
with open(os.environ['PROVIDER_RELEASE']) as gate:
    gate.read()
print('https://external.example/fixture-post')
""")
    provider.chmod(0o755)
    env.update(
        {
            "DEVTO_SCRIPT": str(provider),
            "PROVIDER_RELEASE": str(fifo),
            "PROVIDER_READY": str(tmp_path / "provider-ready"),
            "PROVIDER_PID": str(tmp_path / "provider-pid"),
        }
    )
    return path, env, fifo


def await_ready(env):
    # Native fixture barrier; finite timeout fails instead of waiting indefinitely.
    import time

    deadline = time.monotonic() + 5
    ready = Path(env["PROVIDER_READY"])
    while not ready.exists():
        assert time.monotonic() < deadline, "fake request never reached barrier"
        time.sleep(0.01)


def release_request(fifo):
    descriptor = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
    os.close(descriptor)


def cleanup_owned_request(process, env):
    import signal

    pidfile = Path(env["PROVIDER_PID"])
    if pidfile.exists():
        pid = int(pidfile.read_text())
        handle = None
        try:
            handle = os.pidfd_open(pid)
            command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
            if env["DEVTO_SCRIPT"].encode() in command:
                signal.pidfd_send_signal(handle, signal.SIGKILL)
        except (ProcessLookupError, FileNotFoundError):
            pass
        finally:
            if handle is not None:
                os.close(handle)
    if process.poll() is None:
        process.kill()
    process.communicate(timeout=5)


def test_consumer_lease_skips_overlapping_outbound_processor(queue_fixture, tmp_path):
    path, env, fifo = blocking_provider(queue_fixture, tmp_path)
    first = subprocess.Popen(
        ["bash", str(QUEUE_SCRIPT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        await_ready(env)
        second = queue_run(env)
        assert second.returncode == 0
        assert "consumer busy" in second.stderr
        assert "performed no delivery" in second.stderr
        assert read(path)[0]["devto"]["status"] == "dispatching"
        release_request(fifo)
        stdout, stderr = first.communicate(timeout=5)
        assert first.returncode == 0, (stdout, stderr)
        assert read(path)[0]["devto"]["status"] == "published"
        unlocked = subprocess.run(
            ["flock", "-n", str(path.parent / ".blog-crosspost-consumer.lock"), "true"],
            capture_output=True,
            timeout=5,
            check=False,
        )
        assert unlocked.returncode == 0
    finally:
        cleanup_owned_request(first, env)


def test_killed_wrapper_lease_remains_until_surviving_request_exits(queue_fixture, tmp_path):
    path, env, fifo = blocking_provider(queue_fixture, tmp_path)
    first = subprocess.Popen(
        ["bash", str(QUEUE_SCRIPT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        await_ready(env)
        first.kill()
        first.wait(timeout=5)
        second = queue_run(env)
        assert second.returncode == 0
        assert "consumer busy" in second.stderr
        release_request(fifo)
        first.communicate(timeout=5)
        unlocked = subprocess.run(
            ["flock", "-w", "3", str(path.parent / ".blog-crosspost-consumer.lock"), "true"],
            capture_output=True,
            timeout=5,
            check=False,
        )
        assert unlocked.returncode == 0
        # Independent watchdog retains a genuine provider receipt after wrapper death.
        assert read(path)[0]["devto"]["status"] == "published"
    finally:
        cleanup_owned_request(first, env)


def test_killed_wrapper_hung_group_deadline_releases_lease_without_blind_replay(
    queue_fixture, tmp_path
):
    path, env, _fifo = blocking_provider(queue_fixture, tmp_path)
    provider = Path(env["DEVTO_SCRIPT"])
    code = provider.read_text().replace("import json, os, sys", "import json, os, sys, signal")
    code = code.replace(
        "Path(os.environ['PROVIDER_READY']).write_text('ready')",
        "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
        "if os.fork() == 0:\n"
        "    with open(os.environ['PROVIDER_RELEASE']) as gate: gate.read()\n"
        "    sys.exit(0)\n"
        "Path(os.environ['PROVIDER_READY']).write_text('ready')",
    )
    provider.write_text(code)
    env["CROSSPOST_PROVIDER_TIMEOUT_SECONDS"] = "1.5"
    first = subprocess.Popen(
        ["bash", str(QUEUE_SCRIPT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        await_ready(env)
        first.kill()
        first.wait(timeout=5)
        overlap = queue_run(env)
        assert overlap.returncode == 0
        assert "consumer busy" in overlap.stderr
        unlocked = subprocess.run(
            ["flock", "-w", "6", str(path.parent / ".blog-crosspost-consumer.lock"), "true"],
            timeout=7,
            check=False,
            capture_output=True,
        )
        assert unlocked.returncode == 0
        first.communicate(timeout=5)
        held = read(path)[0]["devto"]
        assert held["status"] == "ambiguous"
        assert held["dispatch_id"] and held["started_at"] and held["deadline_at"]
        assert held["attempts"] == 1
        before = path.read_bytes()
        again = queue_run(env)
        assert again.returncode == 1, again.stderr
        assert "Posting to Dev.to" not in again.stderr
        assert "Held entries" in again.stderr
        assert path.read_bytes() == before
    finally:
        cleanup_owned_request(first, env)


def test_abandoned_dispatch_recovery_holds_without_send(queue_fixture):
    path, env = queue_fixture
    rows = read(path)
    rows[0]["devto"].update(status="dispatching", dispatch_id="old-owned-attempt")
    rows[0]["hashnode"]["status"] = "published"
    write(path, rows)
    result = queue_run(env)
    assert result.returncode == 1, result.stderr
    assert read(path)[0]["devto"]["status"] == "ambiguous"
    assert len(read(path)) == 1
    assert "Posting to Dev.to" not in result.stderr


def test_unknown_provider_failure_is_held_not_retryable(queue_fixture):
    path, env = queue_fixture
    env["PROVIDER_FAIL"] = "1"
    result = queue_run(env)
    assert result.returncode == 1, result.stderr
    assert read(path)[0]["devto"]["status"] == "ambiguous"
    assert "retry_after" not in read(path)[0]["devto"]


def test_definitive_rejection_retry_exhaustion_visible(queue_fixture):
    path, env = queue_fixture
    env.update(
        PROVIDER_FAIL="1",
        PROVIDER_SAFE_REJECT="1",
        PROVIDER_PATCH=json.dumps({"devto": {"attempts": 4}, "hashnode": {"status": "published"}}),
    )
    result = queue_run(env)
    assert result.returncode == 1, result.stderr
    assert read(path)[0]["devto"]["status"] == "failed"
    assert read(path)[0]["devto"]["attempts"] == 5


def test_canary_dry_run_does_not_mutate_state(queue_fixture):
    path, env = queue_fixture
    env["BLOG_CANARY"] = "1"
    before = path.read_bytes()
    result = subprocess.run(
        ["bash", str(QUEUE_SCRIPT), "--dry-run"],
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "DRY RUN" in result.stderr
    assert path.read_bytes() == before


@pytest.mark.parametrize("value", ["0", "-1", "nan", "inf", "601", "bad"])
def test_invalid_provider_deadline_never_sends(queue_fixture, value):
    path, env = queue_fixture
    env["CROSSPOST_PROVIDER_TIMEOUT_SECONDS"] = value
    result = queue_run(env)
    assert result.returncode != 0
    assert read(path)[0]["devto"]["status"] == "pending"
    assert len(read(path)) == 1


def test_unleased_recovery_cannot_discard_active_provider_receipt(queue_fixture, tmp_path):
    path, env, fifo = blocking_provider(queue_fixture, tmp_path)
    first = subprocess.Popen(
        ["bash", str(QUEUE_SCRIPT)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        await_ready(env)
        before = path.read_bytes()
        unleased = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "blog_crosspost_dispatch.py"),
                "recover",
                "--queue",
                str(path),
            ],
            env=env,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert unleased.returncode != 0
        assert path.read_bytes() == before
        release_request(fifo)
        first.communicate(timeout=5)
        assert first.returncode == 0
        assert read(path)[0]["devto"]["status"] == "published"
    finally:
        cleanup_owned_request(first, env)


def test_watchdog_does_not_inherit_owner_lease(queue_fixture, tmp_path):
    path, env, _fifo = blocking_provider(queue_fixture, tmp_path)
    env["CROSSPOST_PROVIDER_TIMEOUT_SECONDS"] = "1"
    owner = tmp_path / "owner.lock"
    env["OWNER_FIXTURE_LOCK"] = str(owner)
    first = subprocess.Popen(
        [
            "bash",
            "-c",
            'exec 9>"$OWNER_FIXTURE_LOCK"; flock -n 9; exec bash "$1"',
            "fixture",
            str(QUEUE_SCRIPT),
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        await_ready(env)
        first.kill()
        first.wait(timeout=5)
        freed = subprocess.run(
            ["flock", "-n", str(owner), "true"], capture_output=True, timeout=5, check=False
        )
        assert freed.returncode == 0
        first.communicate(timeout=5)
        assert read(path)[0]["devto"]["status"] == "ambiguous"
    finally:
        cleanup_owned_request(first, env)


def test_locked_begin_rechecks_latest_future_deferral(tmp_path):
    path = tmp_path / ".crosspost-queue.json"
    write(
        path,
        [
            {
                "slug": "fixture",
                "devto": {"status": "pending", "retry_after": "2999-01-01T00:00:00Z"},
            }
        ],
    )
    dispatch = module("blog_crosspost_dispatch")
    before = path.read_bytes()
    assert dispatch.begin(path, "fixture", "devto", 1) is None
    assert path.read_bytes() == before


@pytest.mark.parametrize("platform", ["devto", "hashnode"])
@pytest.mark.parametrize("timeout_value", ["0", "-1", "601", "nan", "999999999999999999999999"])
def test_real_provider_invalid_request_timeout_never_calls_curl(
    queue_fixture, tmp_path, platform, timeout_value
):
    _path, env = queue_fixture
    fake = tmp_path / "curl"
    fake.write_text('#!/bin/sh\nprintf called > "$CURL_MARKER"\nexit 99\n')
    fake.chmod(0o755)
    env.update(
        PATH=f"{tmp_path}:{env['PATH']}",
        CURL_MARKER=str(tmp_path / "curl-called"),
        CROSSPOST_REQUEST_TIMEOUT_SECONDS=timeout_value,
    )
    script = QUEUE_SCRIPT.parent / f"post-to-{platform}.sh"
    source = Path(env["BLOG_DIR"]) / "content/posts/fixture-post.md"
    result = subprocess.run(
        ["bash", str(script), str(source)], env=env, capture_output=True, timeout=5, check=False
    )
    assert result.returncode != 0
    assert not Path(env["CURL_MARKER"]).exists()


@pytest.mark.parametrize("platform", ["devto", "hashnode"])
def test_real_provider_rejected_create_has_explicit_safe_contract_and_timeouts(
    queue_fixture, tmp_path, platform
):
    _path, env = queue_fixture
    fake = tmp_path / "curl"
    fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$CURL_MARKER"\nprintf \'{}\\n429\\n\'\n')
    fake.chmod(0o755)
    env.update(PATH=f"{tmp_path}:{env['PATH']}", CURL_MARKER=str(tmp_path / "curl-args"))
    source = Path(env["BLOG_DIR"]) / "content/posts/fixture-post.md"
    result = subprocess.run(
        ["bash", str(QUEUE_SCRIPT.parent / f"post-to-{platform}.sh"), str(source)],
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    assert result.returncode == 75, result.stderr
    assert result.stderr.strip().splitlines()[-1] == "CROSSPOST_SAFE_REJECTION"
    args = Path(env["CURL_MARKER"]).read_text().splitlines()
    assert args[args.index("--connect-timeout") + 1] == "10"
    assert args[args.index("--max-time") + 1] == "60"
    assert "--retry" not in args


@pytest.mark.parametrize("problem", ["missing_key", "missing_source"])
def test_due_queue_configuration_failure_not_false_healthy(queue_fixture, problem):
    path, env = queue_fixture
    rows = read(path)
    rows[0]["hashnode"]["status"] = "published"
    write(path, rows)
    if problem == "missing_key":
        env["DEVTO_API_KEY"] = ""
    else:
        (path.parent / "content/posts/fixture-post.md").unlink()
        # Removing an owner file must no longer destroy an immutable source.
        # This fixture represents actual removal from authoritative Git history.
        for args in (
            ["add", "content/posts"],
            ["commit", "-m", "Remove source fixture"],
            ["push", "origin", "master"],
        ):
            subprocess.run(
                ["git", "-C", str(path.parent), *args], env=env, check=True, capture_output=True
            )
    result = queue_run(env)
    assert result.returncode == 1, result.stderr
    assert read(path)[0]["devto"]["status"] == "pending"
    assert len(read(path)) == 1


def test_sweep_preserves_processor_failure_for_alert(tmp_path):
    blog = tmp_path / "blog"
    processor = blog / ".claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"
    processor.parent.mkdir(parents=True)
    processor.write_text("#!/bin/sh\necho fixtureheld >&2\nexit 17\n")
    processor.chmod(0o755)
    lib = blog / "scripts/blog/lib-cron-common.sh"
    lib.parent.mkdir(parents=True)
    lib.write_text(
        'liveness_markers() { printf "%s" "$2" > "$FIXTURE_RESULT"; }\n'
        'cron_fail() { printf "%s" "$*" > "$FIXTURE_ALERT"; }\n'
    )
    env = {
        **os.environ,
        "BLOG_DIR": str(blog),
        "BLOG_CANARY": "0",
        "BLOG_CROSSPOST_LOG_DIR": str(tmp_path / "logs"),
        "FIXTURE_RESULT": str(tmp_path / "status"),
        "FIXTURE_ALERT": str(tmp_path / "alert"),
    }
    # Replace just the owned fixture copy's prefix heartbeat path: no production writes.
    sweep = tmp_path / "sweep.sh"
    text = (
        (SCRIPTS / "blog-crosspost-sweep.sh")
        .read_text()
        .replace("$HOME/.local/state/intent-os/liveness", str(tmp_path / "liveness"))
    )
    sweep.write_text(text)
    result = subprocess.run(
        ["bash", str(sweep)], env=env, capture_output=True, text=True, timeout=5, check=False
    )
    assert result.returncode == 17
    assert Path(env["FIXTURE_RESULT"]).read_text() == "17"
    assert "queue processor failed" in Path(env["FIXTURE_ALERT"]).read_text()
    log = next((tmp_path / "logs").glob("run-*.log")).read_text()
    assert "processor exit 17" in log
    assert "sweep complete" not in log
