"""Publication evidence is separate from packet delivery and from assumed statuses.

Hermetic: synthetic .eml messages served by a fake IMAP class, a ledger COPY in a temp
directory, no mailbox, no network, no real ledger. Covers blogpipe/evidence.py, the
reply ingester (receipts, sender allowlist, weekly paste, dead-man), the reconciler's
held-packet rule, the generic CLI patch guard, and the packet's held marker.
"""

import argparse
import copy
import importlib.util
import json
import os
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts/blog"
STATE_SCRIPT = SCRIPTS / "blog_publication_state.py"
OWNER = "owner@example.invalid"
POSTER = "poster@example.invalid"
STRANGER = "someone@elsewhere.invalid"

sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
from blogpipe import evidence  # noqa: E402
from blogpipe.errors import PublicationError  # noqa: E402


def module(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), SCRIPTS / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def slot(status):
    return {"status": status, "posted_at": None, "url": None, "by": None}


def post(slug, date, statuses, **extra):
    return {
        "slug": slug,
        "date": date,
        "title": f"The {slug.replace('-', ' ')} story",
        "canonical_url": f"https://startaitools.com/posts/{slug}/",
        "tier": 2,
        "published_at": f"{date}T08:00:00-06:00",
        "packet_sent": True,
        "syndication": {k: slot(v) for k, v in statuses.items()},
        **extra,
    }


ALL_PENDING = dict.fromkeys(("x", "li_personal", "li_company", "substack", "medium"), "pending")
ALL_ASSUMED = dict.fromkeys(ALL_PENDING, "assumed_posted")


@pytest.fixture
def ledger(tmp_path):
    rows = [
        post("fresh-pending-post", "2026-09-20", ALL_PENDING),
        post("historical-assumed-post", "2026-08-19", ALL_ASSUMED),
        post("held-pii-post", "2026-08-07", ALL_PENDING, packet_status="held"),
    ]
    path = tmp_path / ".blog-syndication-ledger.json"
    path.write_text(json.dumps(rows, indent=2) + "\n")
    return path


def rows(path):
    return json.loads(path.read_text())


def eml(sender, subject, body, message_id, date="Sat, 19 Sep 2026 17:26:00 +0000"):
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = "packets@example.invalid"
    msg["Subject"] = subject
    msg["Date"] = date
    msg["Message-ID"] = message_id
    msg.set_content(body)
    return bytes(msg)


class FakeIMAP:
    """Serves synthetic .eml bytes; records every call so tests can assert read-only."""

    messages: list = []
    calls: list = []

    def __init__(self, host, port, ssl_context=None):
        FakeIMAP.calls.append(("connect", host))

    def login(self, user, password):
        FakeIMAP.calls.append(("login",))

    def select(self, box, readonly=False):
        FakeIMAP.calls.append(("select", box, readonly))
        return "OK", [b"1"]

    def search(self, charset, *criteria):
        FakeIMAP.calls.append(("search", criteria))
        ids = " ".join(str(i + 1) for i in range(len(FakeIMAP.messages)))
        return "OK", [ids.encode()]

    def fetch(self, num, spec):
        return "OK", [(b"1 (RFC822)", FakeIMAP.messages[int(num) - 1])]

    def logout(self):
        pass


@pytest.fixture
def ingest(ledger, tmp_path, monkeypatch):
    mod = module("ingest-syndication-replies")
    monkeypatch.setattr(mod, "LEDGER", ledger)
    monkeypatch.setattr(mod, "ENV_FILE", tmp_path / "mail.env")
    monkeypatch.setattr(mod, "BLOG_ENV_FILE", tmp_path / "blog.env")
    monkeypatch.setattr(mod, "STATE_FILE", tmp_path / "state" / "state.json")
    monkeypatch.setattr(mod.imaplib, "IMAP4_SSL", FakeIMAP)
    for key in ("SYNDICATION_RECEIPT_SENDERS", "EZEKIEL_EMAIL", "PACKET_CC"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("SMTP_HOST", "imap.example.invalid")
    monkeypatch.setenv("SMTP_USER", "fixture")
    monkeypatch.setenv("SMTP_PASS", "fixture")
    FakeIMAP.messages, FakeIMAP.calls = [], []
    return mod


def ingest_args(**kw):
    base = dict(days=14, sender=None, dry_run=False, paste_file=None, no_mail=False)
    base.update(kw)
    return argparse.Namespace(**base)


# --- blogpipe/evidence.py --------------------------------------------------------

def observe(row, surface, url, ref="message-id:<a@b>"):
    return evidence.record_observation(
        row, surface, url, source="reply", observed_at="2026-09-19T17:26:00+00:00",
        evidence_ref=ref, recorded_at="2026-10-03T07:30:00+00:00")


def test_a_pending_row_upgrades_and_a_belief_never_does():
    fresh = post("a-post", "2026-09-20", ALL_PENDING)
    assert observe(fresh, "x", "https://x.com/h/status/1") == "upgraded"
    assert fresh["syndication"]["x"]["status"] == "posted"
    assert fresh["syndication"]["x"]["url"] == "https://x.com/h/status/1"

    believed = post("b-post", "2026-08-19", ALL_ASSUMED)
    before = copy.deepcopy(believed["syndication"])
    assert observe(believed, "x", "https://x.com/h/status/2") == "recorded"
    assert believed["syndication"] == before, "assumed_posted must never become posted"
    assert evidence.publication_status(believed, "x") == "posted"
    assert evidence.publication_status(believed, "medium") == "unknown"
    assert observe(believed, "x", "https://x.com/h/status/2") == "duplicate"
    assert len(believed["publication_evidence"]["x"]) == 1


def test_a_receipt_must_be_a_url_on_the_platform_it_claims():
    row = post("c-post", "2026-09-20", ALL_PENDING)
    for surface, url in [
        ("x", "https://startaitools.com/posts/c-post/"),  # the link he was asked to share
        ("li_personal", "https://x.com/h/status/1"),
        ("substack", "https://evil.example/substack.com/p/x"),
        ("medium", "https://medium.com/"),  # no post path
        ("x", "ftp://x.com/h/status/1"),
    ]:
        with pytest.raises(PublicationError):
            observe(row, surface, url)
    assert "publication_evidence" not in row or not any(row["publication_evidence"].values())
    assert row["syndication"]["x"]["status"] == "pending"


def test_status_vocabularies_stay_distinct():
    assert set(evidence.PACKET_STATUSES) == {"sent", "held"}
    assert set(evidence.EVIDENCE_STATUSES) == {"posted", "not_posted", "unknown", "n/a"}
    assert set(evidence.MEASUREMENT_STATUSES) == {
        "verified", "verified_zero", "unverified", "unavailable", "uninstrumented"}
    groups = (evidence.PACKET_STATUSES, evidence.EVIDENCE_STATUSES, evidence.MEASUREMENT_STATUSES)
    flat = [s for g in groups for s in g]
    assert len(flat) == len(set(flat)), "a status word means two things"
    legacy_posted_without_url = post("d-post", "2026-09-20", {"x": "posted"})
    assert evidence.publication_status(legacy_posted_without_url, "x") == "unknown"


# --- ingest-syndication-replies.py ----------------------------------------------

def test_owner_and_poster_receipts_are_appended_without_rewriting_history(ingest, ledger,
                                                                           monkeypatch):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", f"{POSTER}, {OWNER}")
    original = rows(ledger)
    FakeIMAP.messages = [
        # The owner reply shape the old POSTER-only filter dropped (audit 226f §3.2).
        eml(f"Owner <{OWNER}>", "Re: 📣 POST THIS — The fresh pending post story",
            "X: https://x.com/handle/status/111\n"
            "LinkedIn personal: https://www.linkedin.com/feed/update/urn:li:activity:222\n"
            "> https://startaitools.com/posts/fresh-pending-post/?utm_source=x\n",
            "<owner-1@mail.example.invalid>"),
        # A claim with no URL: reported, never recorded.
        eml(f"Owner <{OWNER}>", "Re: 📣 POST THIS — The historical assumed post story",
            "I already knocked out 5-7!\n", "<owner-2@mail.example.invalid>"),
        # The weekly paste, including one wrong-platform line that must be rejected.
        eml(f"Poster <{POSTER}>", "weekly URLs",
            "2026-08-19 x https://x.com/handle/status/333\n"
            "historical-assumed-post x_article https://x.com/i/articles/444\n"
            "2026-08-19 buymeacoffee https://www.buymeacoffee.com/someone/p/555\n"
            "2026-08-19 li_company https://startaitools.com/posts/historical-assumed-post/\n"
            "1999-01-01 x https://x.com/handle/status/999\n",
            "<poster-1@mail.example.invalid>", date="Mon, 21 Sep 2026 09:00:00 +0000"),
        # Not on the allowlist: ignored even though it carries perfect receipts.
        eml(f"Stranger <{STRANGER}>", "Re: 📣 POST THIS — The fresh pending post story",
            "posted 2026-09-20\nSubstack: https://spoof.substack.com/p/fake\n",
            "<stranger@mail.example.invalid>"),
    ]
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert ("select", "INBOX", True) in FakeIMAP.calls, "mailbox must be opened read-only"
    after = {r["slug"]: r for r in rows(ledger)}
    before = {r["slug"]: r for r in original}

    fresh = after["fresh-pending-post"]
    assert fresh["syndication"]["x"]["status"] == "posted"
    assert fresh["syndication"]["x"]["posted_at"] == "2026-09-19T17:26:00+00:00"
    assert fresh["syndication"]["li_personal"]["status"] == "posted"
    assert fresh["syndication"]["substack"]["status"] == "pending", "stranger was trusted"
    [x_receipt] = fresh["publication_evidence"]["x"]
    assert x_receipt["source"] == "reply"
    assert x_receipt["evidence_ref"] == "message-id:<owner-1@mail.example.invalid>"
    assert OWNER not in json.dumps(fresh), "a sender address leaked into the ledger"

    old = after["historical-assumed-post"]
    without_new = {k: v for k, v in old.items() if k != "publication_evidence"}
    assert without_new == before["historical-assumed-post"], "historical row was rewritten"
    assert set(old["publication_evidence"]) == {"x", "x_article", "buymeacoffee"}
    assert all(o["source"] == "paste" for v in old["publication_evidence"].values() for o in v)
    assert old["publication_evidence"]["x"][0]["observed_at"] == "2026-09-21T09:00:00+00:00"
    assert old["publication_evidence"]["x"][0]["evidence_ref"].endswith("#L1")
    assert after["held-pii-post"] == before["held-pii-post"]

    # Idempotent: the same mail again appends nothing.
    snapshot = ledger.read_bytes()
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert ledger.read_bytes() == snapshot


def test_ingest_reports_claims_rejections_and_unmatched_lines(ingest, monkeypatch, capsys):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    FakeIMAP.messages = [
        eml(OWNER, "Re: packet", "X and linked in posted plz post the rest\n", "<m1@x>"),
        eml(OWNER, "urls", "2026-08-19 li_company https://startaitools.com/posts/x/\n"
                           "1999-01-01 x https://x.com/handle/status/9\n", "<m2@x>"),
    ]
    assert ingest.cmd_ingest(ingest_args()) == 0
    out = capsys.readouterr().out
    assert "a claim without a post URL is not a receipt" in out
    assert "REJECTED 2026-08-19 li_company" in out
    assert "UNMATCHED paste line 2" in out
    assert "no new receipts to record" in out


def test_ingest_refuses_without_a_configured_sender_list(ingest, ledger, capsys):
    snapshot = ledger.read_bytes()
    assert ingest.cmd_ingest(ingest_args()) == 2
    assert "refusing to read receipts from anyone" in capsys.readouterr().err
    assert FakeIMAP.calls == [], "no mailbox connection without an allowlist"
    assert ledger.read_bytes() == snapshot


def test_sender_list_comes_from_config_files_not_code(ingest, tmp_path, monkeypatch):
    (tmp_path / "blog.env").write_text(f"EZEKIEL_EMAIL={POSTER}\nPACKET_CC=Owner <{OWNER}>\n")
    assert ingest.receipt_senders(ingest.load_env()) == [POSTER, OWNER]
    (tmp_path / "blog.env").write_text(
        f"EZEKIEL_EMAIL={POSTER}\nSYNDICATION_RECEIPT_SENDERS={OWNER};{POSTER}\n")
    assert ingest.receipt_senders(ingest.load_env()) == [OWNER, POSTER]
    assert ingest.receipt_senders({}, [STRANGER]) == [STRANGER]
    source = (SCRIPTS / "ingest-syndication-replies.py").read_text()
    assert "@intentsolutions.io" not in source, "a personal address is hardcoded"


def test_weekly_paste_file_works_without_the_mailbox(ingest, ledger, tmp_path):
    paste = tmp_path / "week.txt"
    paste.write_text("fresh-pending-post medium https://someone.medium.com/a-story-123\n"
                     "- 2026-09-20 substack: https://someone.substack.com/p/a-story\n")
    assert ingest.cmd_ingest(ingest_args(paste_file=str(paste), no_mail=True)) == 0
    fresh = {r["slug"]: r for r in rows(ledger)}["fresh-pending-post"]
    assert fresh["syndication"]["medium"]["status"] == "posted"
    assert fresh["syndication"]["substack"]["status"] == "posted"
    assert fresh["publication_evidence"]["medium"][0]["evidence_ref"].startswith("paste:sha256:")
    assert FakeIMAP.calls == []


# --- the dead-man ------------------------------------------------------------------

def check_args(**kw):
    base = dict(stale_hours=48, utm_days=30, no_utm=False, stateless=False)
    base.update(kw)
    return argparse.Namespace(**base)


@pytest.mark.parametrize(
    "utm, no_utm, word",
    [(87, False, "unverified"), (0, False, "verified_zero"),
     (None, False, "unavailable"), (None, True, "unavailable")],
)
def test_a_site_wide_utm_count_never_satisfies_the_dead_man(ingest, monkeypatch, capsys,
                                                            utm, no_utm, word):
    monkeypatch.setattr(ingest, "utm_arrivals", lambda days: utm)
    assert ingest.cmd_check(check_args(no_utm=no_utm)) == 1, "onset must alert"
    out = capsys.readouterr().out
    assert "UNRECORDED: 2 packeted post(s)" in out
    assert f"UTM corroboration: {word}" in out
    assert "held: 1 packet(s)" in out
    assert "measurement: uninstrumented for Substack/Medium on 2" in out
    # Hysteresis still applies: the same gap the next morning is quiet, not re-paged.
    assert ingest.cmd_check(check_args(no_utm=no_utm)) == 0


def test_a_url_receipt_clears_the_gap_and_a_belief_does_not(ingest, ledger, monkeypatch, capsys):
    monkeypatch.setattr(ingest, "utm_arrivals", lambda days: 87)
    data = rows(ledger)
    for row in data:
        if row["slug"] != "held-pii-post":
            observe(row, "li_company", "https://www.linkedin.com/feed/update/urn:li:activity:7")
    ledger.write_text(json.dumps(data))
    assert ingest.cmd_check(check_args()) == 0
    assert "every packeted post has a publication receipt" in capsys.readouterr().out


# --- syndication-reconcile.py ------------------------------------------------------

def test_reconcile_never_assumes_a_held_packet_or_an_evidenced_surface(ledger, monkeypatch):
    writer = module("syndication-reconcile")
    monkeypatch.setattr(writer, "LEDGER", ledger)
    data = rows(ledger)
    observe(data[0], "x", "https://x.com/h/status/1")
    ledger.write_text(json.dumps(data))
    before = {r["slug"]: r for r in rows(ledger)}
    assert writer.main([]) == 0
    after = {r["slug"]: r for r in rows(ledger)}
    assert after["held-pii-post"] == before["held-pii-post"]
    fresh = after["fresh-pending-post"]["syndication"]
    assert fresh["x"]["status"] == "posted"
    assert {fresh[k]["status"] for k in ("li_personal", "li_company", "substack", "medium")} \
        == {"assumed_posted"}
    assert after["historical-assumed-post"] == before["historical-assumed-post"]


# --- generic CLI patch guard -------------------------------------------------------

def cli_patch(ledger, slug, patch):
    return subprocess.run(
        [sys.executable, str(STATE_SCRIPT), "update", "--file", str(ledger), "--slug", slug,
         "--patch-json", json.dumps(patch)],
        capture_output=True, text=True, timeout=20,
        env={**os.environ, "BLOG_CANARY": "0", "PYTHONDONTWRITEBYTECODE": "1"},
    )


def test_the_generic_patch_cannot_claim_posted_without_a_receipt(ledger):
    snapshot = ledger.read_bytes()
    no_url = cli_patch(ledger, "fresh-pending-post", {"syndication": {"x": {"status": "posted"}}})
    belief = cli_patch(ledger, "historical-assumed-post",
                       {"syndication": {"x": {"status": "posted",
                                              "url": "https://x.com/h/status/1"}}})
    assert no_url.returncode == 1 and belief.returncode == 1
    assert ledger.read_bytes() == snapshot
    ok = cli_patch(ledger, "fresh-pending-post",
                   {"syndication": {"x": {"status": "posted", "url": "https://x.com/h/status/1"}}})
    assert ok.returncode == 0, ok.stderr


# --- the packet's held marker ------------------------------------------------------

def packet_text():
    return (SCRIPTS / "blog-posting-packet.sh").read_text()


def test_mark_sent_records_held_as_delivery_not_distribution(ledger):
    text = packet_text()
    function = text[text.index("mark_sent() {") : text.index("\nsend_packet() {")]
    env = {**os.environ, "BLOG_DIR": str(ROOT), "LEDGER_FILE": str(ledger),
           "BLOG_CANARY": "0", "PYTHONDONTWRITEBYTECODE": "1"}
    script = function + "\nmark_sent fresh-pending-post held && mark_sent historical-assumed-post"
    result = subprocess.run(["bash", "-c", script], env=env, capture_output=True, text=True,
                            timeout=20)
    assert result.returncode == 0, result.stderr
    after = {r["slug"]: r for r in rows(ledger)}
    assert after["fresh-pending-post"]["packet_sent"] is True
    assert after["fresh-pending-post"]["packet_status"] == "held"
    assert after["fresh-pending-post"]["syndication"]["x"]["status"] == "pending"
    assert after["historical-assumed-post"]["packet_status"] == "sent"
    assert after["historical-assumed-post"]["packet_tagging"] == "utm_campaign_v1"


def test_the_send_loop_marks_a_hold_payload_held(tmp_path):
    source = packet_text()
    block = source.split("# Build each post's HTML fragment;", 1)[1]
    block = block[block.index("TMP_HTML=") :]
    shell = f"""
set -uo pipefail
DRY_RUN=0
PACKET_PLANE_CARD=0
HTML_GEN=/offline/renderer
EZEKIEL_EMAIL=fixture@example.invalid
ENTRIES=('{{"slug":"held","title":"Held"}}' '{{"slug":"clean","title":"Clean"}}')
log() {{ printf '%s\\n' "$*"; }}
build_payload() {{
  if [[ "$1" == *'"held"'* ]]; then printf '{{"hold":true}}'; else printf '{{"hold":false}}'; fi
}}
node() {{ cat; }}
send_packet() {{ return 0; }}
mark_sent() {{ printf 'receipt:%s:%s\\n' "$1" "$2"; }}
{block}
"""
    result = subprocess.run(["bash", "-c", shell], cwd=tmp_path, capture_output=True,
                            text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    assert "receipt:held:held" in result.stdout
    assert "receipt:clean:sent" in result.stdout


def test_shims_and_entry_points_keep_bytecode_out_of_the_package():
    for name in ("ingest-syndication-replies.py", "syndication-reconcile.py"):
        text = (SCRIPTS / name).read_text()
        assert text.index("sys.dont_write_bytecode = True") < text.index("from blogpipe")
