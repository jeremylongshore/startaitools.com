"""Exercise actual no-op shell paths without locks, providers, mail, or publication."""

import json
import os
import shlex
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
ARTICLE = "https://startaitools.com/posts/existing-fixture/"


def shell(source, tmp_path):
    return subprocess.run(
        ["/bin/bash", "-c", source],
        cwd=tmp_path,
        env={**os.environ, "INTENT_RUNTIME": "/nonexistent-offline-runtime"},
        capture_output=True,
        text=True,
        timeout=10,
    )


@pytest.mark.parametrize("canary,live", [(False, True), (False, False), (True, False)])
def test_wrapper_existing_post_requires_public_verification(tmp_path, canary, live):
    source = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    block = source[source.index("if EXISTING=$(published_post_for_date") :]
    block = block.split("# Hugo theme", 1)[0]
    sweep = tmp_path / "scripts/blog/blog-crosspost-sweep.sh"
    sweep.parent.mkdir(parents=True)
    sweep.write_text('#!/bin/bash\nprintf "crosspost\\n" >> "$EVENTS"\n')
    sweep.chmod(0o755)
    events = tmp_path / "events"
    log = tmp_path / "run.log"
    result = shell(
        f"""
set -uo pipefail
export EVENTS={shlex.quote(str(events))}
BLOG_DIR=/fixture
POSTS_DIR=/fixture/content/posts
BLOG_SOURCE_DIR={shlex.quote(str(tmp_path))}
BLOG_CANARY={int(canary)}
RECOVERY_DEGRADED=0
YESTERDAY=2026-09-15
WORKSPACE_HELPER=/offline/helper.py
PUBLICATION_HELPER=/offline/publication.py
BLOG_RUN_MANIFEST=/offline/manifest.json
LOG={shlex.quote(str(log))}
log() {{ printf '%s\\n' "$*" >> "$LOG"; }}
published_post_for_date() {{ printf '/fixture/content/posts/existing-fixture.md\\n'; }}
python3() {{ printf '%s\\n' "$2" >> "$EVENTS"; }}
remote_live_check() {{ printf 'public:%s\\n' "$1" >> "$EVENTS"; return {0 if live else 1}; }}
rebuild_canonical_index() {{ printf 'canonical-index\\n' >> "$EVENTS"; }}
{block}
""",
        tmp_path,
    )
    observed = events.read_text().splitlines() if events.exists() else []
    if canary:
        assert result.returncode == 0
        assert observed == ["complete-noop"]
    elif live:
        assert result.returncode == 0
        assert observed == [
            f"public:{ARTICLE}",
            "check-existing",
            "crosspost",
            "canonical-index",
            "complete-noop",
        ]
    else:
        assert result.returncode != 0
        assert observed == [f"public:{ARTICLE}"]
        assert "public" in log.read_text().lower()


@pytest.mark.parametrize(
    "historical,index_ok,canary,expected",
    [
        (True, False, False, 0),
        (False, False, False, 1),
        (False, True, False, 0),
        (False, False, True, 0),
    ],
)
def test_existing_post_cannot_bypass_canonical_index(
    tmp_path, historical, index_ok, canary, expected
):
    """Execute old/new no-op branches with an independently failing index consumer."""
    source = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    function = source.split("rebuild_canonical_index() {", 1)[1].split("\nPUBLICATION_HELPER=", 1)[
        0
    ]
    if historical:
        old = subprocess.run(
            ["git", "show", "d471768c:scripts/blog/blog-backfill-daily.sh"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        source = old.stdout
    block = source[source.index("if EXISTING=$(published_post_for_date") :].split(
        "# Hugo theme", 1
    )[0]
    owner = tmp_path / "owner"
    (owner / "scripts/blog").mkdir(parents=True)
    unrelated = owner / "unrelated-user-draft.md"
    unrelated.write_bytes(b"preserve owner work exactly\n")
    sweep = owner / "scripts/blog/blog-crosspost-sweep.sh"
    sweep.write_text('#!/bin/bash\nprintf "crosspost\\n" >> "$EVENTS"\n')
    sweep.chmod(0o755)
    helper = tmp_path / "immutable-helpers/blog-methodology-published-index.py"
    helper.parent.mkdir()
    helper.write_text(
        "import argparse, os\nfrom pathlib import Path\n"
        "p=argparse.ArgumentParser()\np.add_argument('--repo')\n"
        "p.add_argument('--output')\np.add_argument('--expected-remote')\n"
        "a=p.parse_args()\n"
        f"assert a.repo == {str(owner)!r}\n"
        "assert a.expected_remote == 'offline-authoritative-remote'\n"
        "assert a.output == str(Path(a.repo)/'.claude/skills/blog-backfill/methodology/index.db')\n"
        "with open(os.environ['EVENTS'], 'a') as f: f.write('canonical-index\\n')\n"
        f"if not {index_ok!r}: raise SystemExit(1)\n"
        "out=Path(a.output)\nout.parent.mkdir(parents=True)\nout.write_bytes(b'verified-derived-index')\n"
    )
    events = tmp_path / "events"
    log = tmp_path / "run.log"
    result = shell(
        f"""
set -uo pipefail
export EVENTS={shlex.quote(str(events))}
SELF={shlex.quote(str(helper.parent / "blog-backfill-daily.sh"))}
BLOG_DIR=/isolated-producer-workspace
POSTS_DIR=/isolated-producer-workspace/content/posts
BLOG_SOURCE_DIR={shlex.quote(str(owner))}
BLOG_EXPECTED_REMOTE=offline-authoritative-remote
BLOG_CANARY={int(canary)}
RECOVERY_DEGRADED=0
YESTERDAY=2026-09-15
WORKSPACE_HELPER=/offline/workspace.py
PUBLICATION_HELPER=/offline/publication.py
BLOG_RUN_MANIFEST=/offline/manifest.json
LOG={shlex.quote(str(log))}
log() {{ printf '%s\\n' "$*" >> "$LOG"; }}
published_post_for_date() {{ printf '/fixture/content/posts/existing-fixture.md\\n'; }}
remote_live_check() {{ return 0; }}
python3() {{
  case "$1" in
    *blog-methodology-published-index.py) command python3 "$@" ;;
    *) printf '%s\\n' "$2" >> "$EVENTS" ;;
  esac
}}
rebuild_canonical_index() {{{function}
{block}
""",
        tmp_path,
    )
    assert result.returncode == expected, (result.stdout, result.stderr)
    observed = events.read_text().splitlines()
    index = owner / ".claude/skills/blog-backfill/methodology/index.db"
    assert index.exists() == (index_ok and not canary and not historical)
    assert unrelated.read_bytes() == b"preserve owner work exactly\n"
    assert ("complete-noop" in observed) == (expected == 0)
    assert ("canonical-index" in observed) == (not historical and not canary)
    if expected:
        assert "unreconciled canonical methodology index" in log.read_text()


@pytest.mark.parametrize(
    "canary,live,dry_run",
    [(False, True, 0), (False, False, 0), (True, False, 0), (False, True, 1), (False, False, 1)],
)
def test_lander_never_returns_already_landed_when_public_missing(tmp_path, canary, live, dry_run):
    source = (SCRIPTS / "blog-land.sh").read_text()
    block = source.split("# ---- Idempotency: already committed?", 1)[1]
    block = block[block.index("POST_REL=") :].split("# ---- Precondition gate", 1)[0]
    sentinel = tmp_path / "2026-09-15.intent.json"
    sentinel.write_text(json.dumps({"evidence": "preserve until verified"}))
    queue = tmp_path / "check-crosspost-queue.sh"
    queue.write_text('#!/bin/bash\nprintf "crosspost\\n" >> "$EVENTS"\n')
    queue.chmod(0o755)
    events = tmp_path / "events"
    result = shell(
        f"""
set -uo pipefail
export EVENTS={shlex.quote(str(events))}
BLOG_DIR=/fixture
POST=/fixture/content/posts/existing-fixture.md
SLUG=existing-fixture
TARGET_DATE=2026-09-15
BLOG_CANARY={int(canary)}
DRY_RUN={dry_run}
CANONICAL={shlex.quote(ARTICLE)}
LOG={shlex.quote(str(tmp_path / "run.log"))}
SKILL_SCRIPTS={shlex.quote(str(tmp_path))}
STAGING_DIR={shlex.quote(str(tmp_path))}
PUBLICATION_HELPER=/offline/publication.py
BLOG_RUN_MANIFEST=/offline/manifest.json
python3() {{ printf '%s\\n' "$2" >> "$EVENTS"; }}
log() {{ printf '%s\\n' "$*"; }}
git() {{ return 0; }}
remote_live_check() {{ printf 'public:%s\\n' "$1" >> "$EVENTS"; return {0 if live else 1}; }}
urgent_alert() {{ printf 'alert\\n' >> "$EVENTS"; }}
{block}
""",
        tmp_path,
    )
    observed = events.read_text().splitlines() if events.exists() else []
    if canary:
        assert result.returncode == 21
        assert observed == []
        assert sentinel.exists()
    elif live:
        assert result.returncode == 21
        assert observed == [f"public:{ARTICLE}"] + (
            ["check-existing"] if dry_run else ["recover", "check-existing", "crosspost"]
        )
        assert sentinel.exists() == bool(dry_run)
    else:
        assert result.returncode == 13
        assert observed == [f"public:{ARTICLE}"] + ([] if dry_run else ["alert"])
        assert sentinel.exists()
        assert "LAND-RESULT: FAILED" in result.stdout


@pytest.mark.parametrize(
    "code,effective,transport,expected",
    [
        (200, ARTICLE, 0, 0),
        (404, ARTICLE, 22, 1),
        (200, "https://startaitools.com/", 0, 1),
        (204, ARTICLE, 0, 1),
        (0, ARTICLE, 28, 1),
    ],
)
def test_public_probe_requires_successful_article_response(
    tmp_path, code, effective, transport, expected
):
    result = shell(
        f"""
source {shlex.quote(str(SCRIPTS / "lib-cron-common.sh"))}
_log() {{ printf '%s\\n' "$2"; }}
sleep() {{ SECONDS=$((SECONDS + $1)); }}
curl() {{ printf '%s\\n%s' {shlex.quote(str(code))} {shlex.quote(effective)}; return {transport}; }}
remote_live_check {shlex.quote(ARTICLE)} 1 /offline/log
""",
        tmp_path,
    )
    assert result.returncode == expected


def test_missing_curl_fails_closed(tmp_path):
    result = shell(
        f"""
source {shlex.quote(str(SCRIPTS / "lib-cron-common.sh"))}
_log() {{ printf '%s\\n' "$2"; }}
PATH=/nonexistent-offline-bin
remote_live_check {shlex.quote(ARTICLE)} 1 /offline/log
""",
        tmp_path,
    )
    assert result.returncode == 1
    assert "FAILED" in result.stdout


@pytest.mark.parametrize("max_secs", ["0", "-1", "invalid"])
def test_invalid_public_probe_budget_fails_closed(tmp_path, max_secs):
    result = shell(
        f"""
source {shlex.quote(str(SCRIPTS / "lib-cron-common.sh"))}
_log() {{ printf '%s\\n' "$2"; }}
curl() {{ printf 'must-not-probe\\n'; return 0; }}
remote_live_check {shlex.quote(ARTICLE)} {shlex.quote(max_secs)} /offline/log
""",
        tmp_path,
    )
    assert result.returncode == 1
    assert "must-not-probe" not in result.stdout


def test_real_curl_accepts_article_and_rejects_missing_redirect_and_empty(tmp_path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/redirect/":
                self.send_response(302)
                self.send_header("Location", "/")
            else:
                self.send_response({"/missing/": 404, "/empty/": 204}.get(self.path, 200))
            self.end_headers()
            self.wfile.write(b"<html><article>Offline fixture</article></html>")

        def log_message(self, *_args):
            pass  # Fixture HTTP access logs contain no production evidence.

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        cases = [("/article/", 0), ("/missing/", 1), ("/redirect/", 1), ("/empty/", 1)]
        for path, expected in cases:
            url = f"http://127.0.0.1:{server.server_port}{path}"
            result = shell(
                f"""
source {shlex.quote(str(SCRIPTS / "lib-cron-common.sh"))}
_log() {{ printf '%s\\n' "$2"; }}
sleep() {{ SECONDS=$((SECONDS + $1)); }}
remote_live_check {shlex.quote(url)} 1 /offline/log
""",
                tmp_path,
            )
            assert result.returncode == expected, (path, result.stdout, result.stderr)
    finally:
        server.shutdown()
        worker.join(timeout=2)
        server.server_close()


@pytest.mark.parametrize("land_rc", [3, 13])
def test_wrapper_maps_unavailable_public_post_to_failure(tmp_path, land_rc):
    source = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    block = source.split('case "$LAND_RC" in', 1)[1].split("\nesac", 1)[0]
    result = shell(
        f'LAND_RC={land_rc}\nPRODUCER_STATUS=OK\ncase "$LAND_RC" in'
        + block
        + '\nesac\nprintf "%s\\n" "$STATUS"\n',
        tmp_path,
    )
    assert result.returncode == 0
    assert result.stdout.startswith("FAILED (")
    assert "public" in result.stdout.lower()


def test_final_public_check_cannot_warn_success_after_delivery(tmp_path):
    source = (SCRIPTS / "blog-land.sh").read_text()
    block = source.split("# ---- Liveness gate:", 1)[1]
    block = block[block.index("if remote_live_check") :]
    result = shell(
        f"""
CANONICAL={shlex.quote(ARTICLE)}
LIVENESS_MAX_SECS=1
TARGET_DATE=2026-09-15
LOG=/offline/log
log() {{ printf '%s\\n' "$*"; }}
remote_live_check() {{ return 1; }}
urgent_alert() {{ printf 'alert\\n'; }}
{block}
""",
        tmp_path,
    )
    assert result.returncode == 13
    assert "LAND-RESULT: FAILED" in result.stdout
    assert "alert" in result.stdout
    assert "OK-WARNING" not in result.stdout


def test_old_pending_delivery_allows_current_work_but_keeps_overall_failure(tmp_path):
    source = (SCRIPTS / "blog-backfill-daily.sh").read_text()
    recovery = source.split("RECOVERY_DEGRADED=0", 1)[1].split("if EXISTING=$(", 1)[0]
    status = source.split('case "$LAND_RC" in', 1)[1].split('if [ "$LAND_RC" -eq 20 ]', 1)[0]
    result = shell(
        f"""
BLOG_CANARY=0
RECOVERY_DEGRADED=0
PUBLICATION_HELPER=/offline/helper
BLOG_RUN_MANIFEST=/offline/manifest
LOG={shlex.quote(str(tmp_path / "run.log"))}
log() {{ printf '%s\\n' "$*"; }}
python3() {{
  printf '{{"outcome":"degraded","failures":[{{"category":"PublicationError"}}]}}\\n'
  return 2
}}
{recovery}
printf 'current target safely produced and landed\\n'
LAND_RC=0
PRODUCER_STATUS=OK
case "$LAND_RC" in{status}
printf '%s\\n' "$STATUS"
case "$STATUS" in FAILED*) exit 1 ;; *) exit 0 ;; esac
""",
        tmp_path,
    )
    assert result.returncode == 1
    assert "current target safely produced and landed" in result.stdout
    assert "FAILED (older delivery recovery pending; current target: OK)" in result.stdout
