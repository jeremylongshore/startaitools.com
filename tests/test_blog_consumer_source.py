"""Real isolated Git handoff; packet/queue scripts execute with offline providers."""

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from test_blog_publication_state import POST, SLUG, git, publication, publish, reconcile, seal
from test_blog_publication_state import run as run

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
RESOLVER = SCRIPTS / "blog_consumer_source.py"
QUEUE = ROOT / ".claude/skills/blog-backfill/scripts/check-crosspost-queue.sh"


@pytest.fixture
def delivery(run):
    seal(run)
    publish(run)
    reconcile(run)
    ledger = run["owner"] / ".blog-syndication-ledger.json"
    queue = run["owner"] / ".crosspost-queue.json"
    rows = publication.load_state(queue)
    rows[0]["devto"]["publish_after"] = "1970-01-01T00:00:00Z"
    rows[0]["hashnode"]["status"] = "skipped"
    with publication.state_locked(run["owner"]):
        publication.atomic_state(queue, rows)
    run.update(ledger=ledger, queue=queue)
    return run


def environment(run):
    return {
        **os.environ,
        "BLOG_DIR": str(run["owner"]),
        "BLOG_CANARY": "0",
        "BLOG_RUN_STATE_DIR": str(run["manifest"].parents[4]),
        "BLOG_EXPECTED_REMOTE": git(run["owner"], "remote", "get-url", "origin"),
        "CONSUMER_SOURCE_HELPER": str(RESOLVER),
        "INTENT_RUNTIME": "/offline/nonexistent",
        "DEVTO_API_KEY": "offline-fixture",
    }


def packet(run, tmp_path, entry=None):
    text = (SCRIPTS / "blog-posting-packet.sh").read_text()
    function = text[text.index("build_payload() {") : text.index("\nmark_sent() {")]
    disclaimer = tmp_path / "disclaimer.json"
    disclaimer.write_text('{"default_footer":"Offline footer"}')
    prelude = f"""
set -uo pipefail
DRY_RUN=1
POSTS_DIR="$BLOG_DIR/content/posts"
DISCLAIMER_LIB={shlex.quote(str(disclaimer))}
RECENT_LI_OPENERS={shlex.quote(str(tmp_path / "openers"))}
VOICE_FAIL_FILE={shlex.quote(str(tmp_path / "voice-fail"))}
log() {{ printf '%s\\n' "$*" >&2; }}
post_body() {{ awk 'f{{print}} /^\\+\\+\\+|^---/{{c++}} c==2 && !f {{f=1}}' "$1"; }}
select_disclaimers() {{ return 0; }}
utm() {{ printf '%s' "$1"; }}
lint_voice_fields() {{ return 0; }}
generate_voice() {{
  jq -n --arg body "$(post_body "$1")" '{{x_post:$body,li_personal:"fixture",li_company:"fixture"}}'
}}
{function}
build_payload "$FIXTURE_ENTRY"
"""
    env = {
        **environment(run),
        "FIXTURE_ENTRY": json.dumps(entry or publication.load_state(run["ledger"])[0]),
    }
    return subprocess.run(
        ["bash", "-c", prelude], env=env, capture_output=True, text=True, timeout=20
    )


def queue(run, tmp_path):
    helpers = run["owner"] / "scripts/blog"
    helpers.mkdir(parents=True, exist_ok=True)
    (helpers / "lib-cron-common.sh").write_bytes((SCRIPTS / "lib-cron-common.sh").read_bytes())
    provider = tmp_path / "provider"
    provider.write_text(
        '#!/bin/sh\ncat "$1" > "$DELIVERY_CAPTURE"\n'
        'printf "called\\n" >> "$DELIVERY_COUNT"\n'
        'printf "https://external.example/offline-fixture\\n"\n'
    )
    provider.chmod(0o755)
    env = {
        **environment(run),
        "DEVTO_SCRIPT": str(provider),
        "ASTRO_SCRIPT": "/missing",
        "DELIVERY_CAPTURE": str(tmp_path / "delivered.md"),
        "DELIVERY_COUNT": str(tmp_path / "calls"),
    }
    return subprocess.run(["bash", str(QUEUE)], env=env, capture_output=True, text=True, timeout=20)


def test_packet_uses_quality_approved_post_when_owner_head_has_no_post(delivery, tmp_path):
    assert not (delivery["owner"] / POST).exists()
    before = git(delivery["owner"], "rev-parse", "HEAD")
    result = packet(delivery, tmp_path)
    assert result.returncode == 0, result.stderr
    assert "A recorded observation." in json.loads(result.stdout)["x_post"]
    assert git(delivery["owner"], "rev-parse", "HEAD") == before


def test_queue_uses_quality_approved_post_and_repeat_never_resends(delivery, tmp_path):
    assert not (delivery["owner"] / POST).exists()
    result = queue(delivery, tmp_path)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "delivered.md").read_bytes() == (delivery["root"] / POST).read_bytes()
    assert publication.load_state(delivery["queue"])[0]["devto"]["status"] == "published"
    assert queue(delivery, tmp_path).returncode == 0
    assert (tmp_path / "calls").read_text() == "called\n"


def resolve(run, tmp_path, entry=None):
    output_dir = tmp_path / "private"
    output_dir.mkdir(mode=0o700, exist_ok=True)
    output = output_dir / "resolved.md"
    output.unlink(missing_ok=True)
    result = subprocess.run(
        [sys.executable, str(RESOLVER), "--repo", str(run["owner"]), "--output", str(output)],
        input=json.dumps(entry or publication.load_state(run["ledger"])[0]),
        env=environment(run),
        capture_output=True,
        text=True,
        timeout=20,
    )
    return result, output


def test_references_match_genuine_publication_and_do_not_change_on_retry(delivery):
    ledger = publication.load_state(delivery["ledger"])[0]
    queued = publication.load_state(delivery["queue"])[0]
    assert ledger["source"] == queued["source"]
    assert ledger["source"]["commit"] == git(delivery["root"], "rev-parse", "HEAD")
    assert ledger["source"]["sha256"] == publication.sha((delivery["root"] / POST).read_bytes())
    with publication.state_locked(delivery["owner"]):
        ledger["packet_sent"] = True
        ledger["syndication"]["x"]["status"] = "posted"
        publication.atomic_state(delivery["ledger"], [ledger])
    reconcile(delivery)
    assert publication.load_state(delivery["ledger"])[0] == ledger
    assert publication.load_state(delivery["queue"])[0] == queued


def test_consumer_survives_removed_producer_workspace_and_dirty_owner(delivery, tmp_path):
    approved = (delivery["root"] / POST).read_bytes()
    (delivery["owner"] / POST).write_text("UNTRACKED IMITATION must never be sent")
    ignore = delivery["owner"] / ".gitignore"
    ignore.write_text(ignore.read_text() + "# unrelated owner change\n")
    git(delivery["owner"], "add", ".gitignore")
    before = (
        git(delivery["owner"], "status", "--porcelain"),
        git(delivery["owner"], "rev-parse", "HEAD"),
    )
    delivery["root"].rename(delivery["root"].with_name("retained-away-from-workspace"))
    result, output = resolve(delivery, tmp_path)
    assert result.returncode == 0, result.stderr
    assert output.read_bytes() == approved
    assert output.stat().st_mode & 0o777 == 0o600
    assert (
        git(delivery["owner"], "status", "--porcelain"),
        git(delivery["owner"], "rev-parse", "HEAD"),
    ) == before
    assert (delivery["owner"] / POST).read_text() == "UNTRACKED IMITATION must never be sent"
    assert packet(delivery, tmp_path).returncode == 0
    assert queue(delivery, tmp_path).returncode == 0
    assert (tmp_path / "delivered.md").read_bytes() == approved


@pytest.mark.parametrize(
    "field,value",
    [
        ("path", "../../secret"),
        ("sha256", "0" * 64),
        ("commit", "0" * 40),
        ("date", "2026-09-17"),
        ("run_id", "different-run"),
        ("quality_seal_sha256", "0" * 64),
        ("schema_version", True),
    ],
)
def test_tampered_reference_never_materializes_or_calls_provider(delivery, tmp_path, field, value):
    entry = publication.load_state(delivery["ledger"])[0]
    entry["source"][field] = value
    result, output = resolve(delivery, tmp_path, entry)
    assert result.returncode != 0
    assert not output.exists()
    assert packet(delivery, tmp_path, entry).returncode != 0
    queued = publication.load_state(delivery["queue"])
    queued[0]["source"] = entry["source"]
    with publication.state_locked(delivery["owner"]):
        publication.atomic_state(delivery["queue"], queued)
    assert queue(delivery, tmp_path).returncode != 0
    assert not (tmp_path / "calls").exists()
    assert publication.load_state(delivery["queue"])[0]["devto"]["status"] == "pending"


@pytest.mark.parametrize("fault", ["slug", "date", "proof", "remote", "article-changed"])
def test_wrong_identity_proof_or_authority_fails_closed(delivery, tmp_path, fault):
    entry = publication.load_state(delivery["ledger"])[0]
    if fault == "slug":
        entry["slug"] = "foreign-post"
        entry["canonical_url"] = "https://startaitools.com/posts/foreign-post/"
    elif fault == "date":
        entry["date"] = "2026-09-17"
    elif fault == "proof":
        (delivery["manifest"].parent / "quality-proof/sentinel.json").write_text("{}")
    elif fault == "remote":
        # A local unpushed commit cannot become publication authority.
        git(
            delivery["owner"],
            "update-ref",
            "refs/remotes/origin/master",
            git(delivery["owner"], "rev-parse", "HEAD"),
        )
        original = environment(delivery)
        git(delivery["owner"], "remote", "set-url", "origin", "/missing-local-fixture")
        original["BLOG_EXPECTED_REMOTE"] = "/missing-local-fixture"
    else:
        (delivery["root"] / POST).write_text("+++\ntitle='Changed'\n+++\nDifferent content\n")
        git(delivery["root"], "add", POST)
        git(delivery["root"], "commit", "-m", "offline later correction")
        git(delivery["root"], "push", "origin", "HEAD:refs/heads/master")
    result, output = resolve(delivery, tmp_path, entry)
    assert result.returncode != 0
    assert not output.exists()


@pytest.mark.parametrize("kind", ["ledger", "queue"])
def test_older_sealed_row_without_reference_uses_retained_proof(delivery, tmp_path, kind):
    row = publication.load_state(delivery[kind])[0]
    del row["source"]
    result, output = resolve(delivery, tmp_path, row)
    assert result.returncode == 0, result.stderr
    assert output.read_bytes() == (delivery["root"] / POST).read_bytes()
    (delivery["manifest"].parent / "quality-seal.json").unlink()
    result, output = resolve(delivery, tmp_path, row)
    assert result.returncode != 0
    assert not output.exists()


def test_reference_upgrade_preserves_sent_and_queue_receipts(delivery):
    for kind in ("ledger", "queue"):
        rows = publication.load_state(delivery[kind])
        rows[0].pop("source")
        if kind == "ledger":
            rows[0]["packet_sent"] = True
        else:
            rows[0]["devto"] = {"status": "published", "url": "https://example.invalid/sent"}
        with publication.state_locked(delivery["owner"]):
            publication.atomic_state(delivery[kind], rows)
    reconcile(delivery)
    assert publication.load_state(delivery["ledger"])[0]["packet_sent"] is True
    assert publication.load_state(delivery["queue"])[0]["devto"]["status"] == "published"
    assert publication.load_state(delivery["queue"])[0]["source"]["path"] == POST


def test_legacy_reads_only_remote_committed_bytes_never_owner_imitation(delivery, tmp_path):
    legacy = {
        key: value
        for key, value in publication.load_state(delivery["ledger"])[0].items()
        if key not in ("source", "run_id", "post_sha256")
    }
    (delivery["owner"] / POST).write_text("private untracked imitation")
    result, output = resolve(delivery, tmp_path, legacy)
    assert result.returncode == 0
    assert output.read_bytes() == (delivery["root"] / POST).read_bytes()
    legacy.update(slug="untracked", canonical_url="https://startaitools.com/posts/untracked/")
    (delivery["owner"] / "content/posts/untracked.md").write_bytes(
        (delivery["root"] / POST).read_bytes()
    )
    result, output = resolve(delivery, tmp_path, legacy)
    assert result.returncode != 0
    assert not output.exists()


def test_source_reference_cannot_be_changed_by_status_writer(delivery):
    with pytest.raises(publication.PublicationError, match="identity"):
        publication.update_row(delivery["ledger"], SLUG, {"source": None})


@pytest.mark.parametrize(
    "fault", ["empty", "draft", "draft-int", "draft-string", "symlink", "too-large"]
)
def test_legacy_committed_invalid_article_cannot_be_consumed(delivery, tmp_path, fault):
    post = delivery["root"] / POST
    if fault == "symlink":
        post.unlink()
        post.symlink_to("../../../private-file")
    else:
        header = "+++\ntitle='Invalid fixture'\ndate=2026-09-16T08:00:00Z\n"
        header += {
            "draft": "draft=true\n",
            "draft-int": "draft=1\n",
            "draft-string": 'draft="true"\n',
        }.get(fault, "")
        post.write_text(
            header
            + "+++\n"
            + (
                ""
                if fault == "empty"
                else ("x" * (1024 * 1024 + 1) if fault == "too-large" else "Body")
            )
        )
    git(delivery["root"], "add", POST)
    git(delivery["root"], "commit", "-m", "Invalid legacy source fixture")
    git(delivery["root"], "push", "origin", "HEAD:refs/heads/master")
    legacy = {"slug": SLUG, "canonical_url": f"https://startaitools.com/posts/{SLUG}/"}
    result, output = resolve(delivery, tmp_path, legacy)
    assert result.returncode != 0
    assert not output.exists()


@pytest.mark.parametrize("failure", ["none", "source", "receipt"])
def test_packet_sweep_preserves_independent_success_but_fails_incomplete_work(tmp_path, failure):
    source = (SCRIPTS / "blog-posting-packet.sh").read_text()
    block = source.split("# Build each post's HTML fragment;", 1)[1]
    block = block[block.index("TMP_HTML=") :]
    shell = f"""
set -uo pipefail
DRY_RUN=0
PACKET_PLANE_CARD=0
HTML_GEN=/offline/renderer
EZEKIEL_EMAIL=fixture@example.invalid
FAILURE={shlex.quote(failure)}
ENTRIES=('{{"slug":"first","title":"First"}}' '{{"slug":"second","title":"Second"}}')
log() {{ printf '%s\\n' "$*"; }}
build_payload() {{
  if [[ "$FAILURE" == source && "$1" == *second* ]]; then return 1; fi
  printf '{{"content":"approved body"}}'
}}
node() {{ cat; }}
send_packet() {{ printf 'offline email fixture accepted\\n'; }}
mark_sent() {{
  printf 'receipt:%s\\n' "$1"
  if [[ "$FAILURE" == receipt && "$1" == second ]]; then return 1; fi
}}
{block}
"""
    result = subprocess.run(
        ["bash", "-c", shell], cwd=tmp_path, capture_output=True, text=True, timeout=10
    )
    assert result.returncode == (0 if failure == "none" else 1), result.stderr
    assert "receipt:first" in result.stdout
    assert ("receipt:second" in result.stdout) == (failure != "source")
