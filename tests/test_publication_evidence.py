"""Publication evidence is separate from packet delivery and from assumed statuses.

Hermetic: synthetic .eml messages served by a fake IMAP class, a ledger COPY in a temp
directory, no mailbox, no network, no real ledger. Covers blogpipe/evidence.py, the
reply ingester (receipts, sender allowlist, sender authentication, weekly paste,
dead-man baseline and re-alert floor), the reconciler's held-packet rule, the generic
CLI patch guard and its reserved keys, and the packet's held marker.

The authentication fixtures mirror what our mail host (MXroute) actually writes,
checked read-only against the live INBOX on 2026-10-03: no Authentication-Results;
internal mail enters `with esmtpsa`; external mail gets an appended
`X-DKIM: signer='<d>' status='pass'` verdict after the sender's own headers.
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
MX = "imap.example.invalid"  # the fixture SMTP_HOST, so the default trusted MX

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
        # Packeted since receipts began (mark-packet stamped it): may raise the alarm.
        post("fresh-pending-post", "2026-09-20", ALL_PENDING,
             packet_status="sent", packet_tagging=evidence.PACKET_TAGGING),
        # Packeted before this deploy: historical, never pages.
        post("historical-assumed-post", "2026-08-19", ALL_ASSUMED),
        post("held-pii-post", "2026-08-07", ALL_PENDING, packet_status="held"),
    ]
    path = tmp_path / ".blog-syndication-ledger.json"
    path.write_text(json.dumps(rows, indent=2) + "\n")
    return path


def rows(path):
    return json.loads(path.read_text())


def eml(sender, subject, body, message_id, date="Sat, 19 Sep 2026 17:26:00 +0000",
        auth="submission", extra=(), trailing=()):
    """A message as our MX stores it. `auth`: "submission" (internal, esmtpsa), "dkim"
    (external with a passing appended verdict), or None (entered unauthenticated)."""
    addr = sender.split("<")[-1].rstrip(">")
    msg = EmailMessage()
    # Hops our MX prepends, newest first: final delivery, content scan, then the entry.
    msg["Received"] = f"from {MX} by {MX} with LMTP id abc (envelope-from <{addr}>)"
    msg["Received"] = f"from mail by {MX} with spam-scanned (Exim 4.99.1) id def"
    if auth == "submission":
        msg["Received"] = (f"from client.example.invalid ([192.0.2.7]) by {MX} with esmtpsa "
                           f"(TLS1.3) (Exim 4.99.1) (envelope-from <{addr}>) id ghi")
    else:
        msg["Received"] = (f"from relay.example.invalid ([198.51.100.9]) by {MX} with esmtps "
                           f"(TLS1.3) (Exim 4.99.1) (envelope-from <{addr}>) id jkl")
    if auth == "dkim":
        msg["DKIM-Signature"] = f"v=1; a=rsa-sha256; d={addr.split('@')[1]}; s=sel; b=xyz"
    for key, value in extra:  # the sender's own headers (forgeable)
        msg[key] = value
    msg["From"] = sender
    msg["To"] = "packets@example.invalid"
    msg["Subject"] = subject
    msg["Date"] = date
    msg["Message-ID"] = message_id
    msg.set_content(body)
    if auth == "dkim":  # our MX appends its verdict after everything the sender wrote
        msg["X-DKIM"] = f"signer='{addr.split('@')[1]}' status='pass' reason=''"
    for key, value in trailing:
        msg[key] = value
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
    for key in ("SYNDICATION_RECEIPT_AUTH", "SYNDICATION_TRUSTED_MX", "SYNDICATION_AUTHSERV_IDS"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("SMTP_HOST", MX)
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
        # The right platform, but a page of it rather than a post (path shape).
        ("x", "https://x.com/home"),
        ("x", "https://x.com/handle"),
        ("medium", "https://medium.com/p/import"),
        ("medium", "https://medium.com/me/stories"),
        ("substack", "https://someone.substack.com/publish/posts"),
        ("li_personal", "https://www.linkedin.com/in/someone"),
        ("li_company", "https://www.linkedin.com/company/someco"),
        ("li_personal", "https://www.linkedin.com/feed/"),
        ("buymeacoffee", "https://www.buymeacoffee.com/someone"),
    ]:
        with pytest.raises(PublicationError):
            observe(row, surface, url)
    assert "publication_evidence" not in row or not any(row["publication_evidence"].values())
    assert row["syndication"]["x"]["status"] == "pending"
    for surface, url in [
        ("x", "https://twitter.com/i/web/status/12/"),
        ("x_article", "https://x.com/i/articles/444"),
        ("li_company", "https://lnkd.in/gAbc12"),
        ("li_personal", "https://www.linkedin.com/posts/someone_a-post-activity-1-abcd"),
        ("substack", "https://someone.substack.com/p/a-story"),
        ("medium", "https://medium.com/@someone/a-story-1a2b3c4d5e6f"),
        ("medium", "https://medium.com/p/1a2b3c4d5e6f"),
    ]:
        assert evidence.receipt_url_ok(surface, url), url
    assert not evidence.receipt_url_ok("li_company", "https://www.linkedin.com/abcd1234"), \
        "a bare code is a lnkd.in short link only"


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
        eml(f"Poster <{POSTER}>", "weekly URLs", auth="dkim", body=
            ("2026-08-19 x https://x.com/handle/status/333\n"
            "historical-assumed-post x_article https://x.com/i/articles/444\n"
            "2026-08-19 buymeacoffee https://www.buymeacoffee.com/someone/p/555\n"
            "2026-08-19 li_company https://startaitools.com/posts/historical-assumed-post/\n"
            "1999-01-01 x https://x.com/handle/status/999\n"),
            message_id="<poster-1@mail.example.invalid>", date="Mon, 21 Sep 2026 09:00:00 +0000"),
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
    paste.write_text("fresh-pending-post medium https://someone.medium.com/a-story-1a2b3c4d5e6f\n"
                     "- 2026-09-20 substack: https://someone.substack.com/p/a-story\n")
    assert ingest.cmd_ingest(ingest_args(paste_file=str(paste), no_mail=True)) == 0
    fresh = {r["slug"]: r for r in rows(ledger)}["fresh-pending-post"]
    assert fresh["syndication"]["medium"]["status"] == "posted"
    assert fresh["syndication"]["substack"]["status"] == "posted"
    assert fresh["publication_evidence"]["medium"][0]["evidence_ref"].startswith("paste:sha256:")
    assert FakeIMAP.calls == []


# --- the dead-man ------------------------------------------------------------------

def check_args(**kw):
    base = dict(stale_hours=48, utm_days=30, no_utm=False, stateless=False,
                realert_days=7, realert_jump=10)
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
    assert "UNRECORDED: 1 packeted post(s)" in out
    assert f"UTM corroboration: {word}" in out
    assert "held: 1 packet(s)" in out
    assert "historical-unverified: 1 packeted post(s)" in out
    assert "uninstrumented" in out
    assert "OFF-RAMPS:" in out and "--mark-missed" in out and "weekly URL paste" in out
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
    assert "every post packeted since receipts began has a publication receipt" \
        in capsys.readouterr().out


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


# --- review fixes (PR #114): sender auth, packet subject, reserved keys, dead-man ---

RECEIPT = "posted 2026-09-20\nX: https://x.com/handle/status/777\n"


def fresh_x(ledger):
    return {r["slug"]: r for r in rows(ledger)}["fresh-pending-post"]["syndication"]["x"]


@pytest.mark.parametrize("label, kwargs", [
    # Allow-listed From, but it entered our MX unauthenticated with no DKIM at all.
    ("no auth", dict(auth=None)),
    # ...plus a forged verdict in the sender's own headers and no signature to check.
    ("forged verdict, no signature",
     dict(auth=None, extra=[("X-DKIM", "signer='example.invalid' status='pass' reason=''"),
                            ("X-DMARC-Status", "pass")])),
    # A forged passing verdict above the MX's own appended FAIL for the same signature.
    ("forged verdict above the MX fail",
     dict(auth=None,
          extra=[("DKIM-Signature", "v=1; d=example.invalid; s=sel; b=forged"),
                 ("X-DKIM", "signer='example.invalid' status='pass' reason=''")],
          trailing=[("X-DKIM", "signer='example.invalid' status='fail' reason='bad sig'")])),
    # A forged Authentication-Results naming our MX is not trusted unless configured.
    ("forged Authentication-Results",
     dict(auth=None, extra=[("Authentication-Results", f"{MX}; dkim=pass "
                                                        "header.d=example.invalid")])),
])
def test_a_spoofed_allow_listed_from_is_not_recorded(ingest, ledger, monkeypatch, capsys,
                                                    label, kwargs):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    snapshot = ledger.read_bytes()
    FakeIMAP.messages = [eml(f"Owner <{OWNER}>", "Re: packet", RECEIPT, "<spoof@x>", **kwargs)]
    assert ingest.cmd_ingest(ingest_args()) == 0
    out = capsys.readouterr().out
    assert "UNAUTHENTICATED message claiming an allow-listed sender" in out, label
    assert ledger.read_bytes() == snapshot, f"{label}: a spoofed receipt was recorded"


@pytest.mark.parametrize("auth", ["submission", "dkim"])
def test_an_authenticated_receipt_is_recorded(ingest, ledger, monkeypatch, auth):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    FakeIMAP.messages = [eml(f"Owner <{OWNER}>", "Re: packet", RECEIPT, "<ok@x>", auth=auth)]
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert fresh_x(ledger)["url"] == "https://x.com/handle/status/777"


def test_authentication_results_is_trusted_only_for_a_configured_authserv_id(ingest, ledger,
                                                                              monkeypatch):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    monkeypatch.setenv("SYNDICATION_AUTHSERV_IDS", "auth.example.invalid")
    header = "auth.example.invalid; dkim=pass header.d=example.invalid; spf=pass"
    FakeIMAP.messages = [eml(f"Owner <{OWNER}>", "Re: packet", RECEIPT, "<ar@x>", auth=None,
                             extra=[("Authentication-Results", header)])]
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert fresh_x(ledger)["status"] == "posted"


def test_submission_from_another_domain_through_our_mx_is_refused(ingest, monkeypatch):
    msg = __import__("email").message_from_bytes(eml(f"Owner <{OWNER}>", "Re: packet",
                                                     RECEIPT, "<d@x>"))
    hops = msg.get_all("Received")
    del msg["Received"]
    for hop in hops:
        msg["Received"] = hop.replace(f"<{OWNER}>", f"<{STRANGER}>") if "esmtpsa" in hop else hop
    ok, why = ingest.sender_authenticated(msg, {MX})
    assert not ok and "off-domain" in why


def test_auth_can_be_switched_off_by_config_with_a_warning(ingest, ledger, monkeypatch, capsys):
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    monkeypatch.setenv("SYNDICATION_RECEIPT_AUTH", "off")
    FakeIMAP.messages = [eml(f"Owner <{OWNER}>", "Re: packet", RECEIPT, "<off@x>", auth=None)]
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert "WARN: SYNDICATION_RECEIPT_AUTH=off" in capsys.readouterr().out
    assert fresh_x(ledger)["status"] == "posted"


def test_our_own_packet_email_is_never_read_as_a_receipt(ingest, ledger, monkeypatch):
    """The packet is CC'd to an allow-listed address and is full of platform URLs."""
    monkeypatch.setenv("SYNDICATION_RECEIPT_SENDERS", OWNER)
    snapshot = ledger.read_bytes()
    FakeIMAP.messages = [
        eml(f"Owner <{OWNER}>", "📣 POST THIS — X + LinkedIn — The fresh pending post story",
            RECEIPT, "<packet@x>"),
        eml(f"Owner <{OWNER}>", "📣 POST THESE — 2 articles — ...", RECEIPT, "<packet2@x>"),
    ]
    assert ingest.cmd_ingest(ingest_args()) == 0
    assert ledger.read_bytes() == snapshot


def test_the_generic_patch_cannot_touch_reserved_fields(ledger):
    snapshot = ledger.read_bytes()
    for patch in (
        {"publication_evidence": {}},  # deep_merge would REPLACE the evidence list
        {"publication_evidence": {"x": []}},
        {"packet_status": "sent"},
        {"packet_status_at": "2026-10-03T05:00:00-06:00"},
        {"packet_tagging": evidence.PACKET_TAGGING},  # would move the dead-man baseline
    ):
        result = cli_patch(ledger, "historical-assumed-post", patch)
        assert result.returncode == 1, patch
        assert '"category": "PublicationError"' in result.stderr
        with pytest.raises(PublicationError, match="cannot be set by a generic patch"):
            evidence.guard_status_patch({}, patch)
    assert ledger.read_bytes() == snapshot
    bad = subprocess.run(
        [sys.executable, str(STATE_SCRIPT), "mark-packet", "--file", str(ledger),
         "--slug", "historical-assumed-post", "--status", "posted"],
        capture_output=True, text=True, timeout=20,
        env={**os.environ, "BLOG_CANARY": "0", "PYTHONDONTWRITEBYTECODE": "1"})
    assert bad.returncode == 2 and ledger.read_bytes() == snapshot
    with pytest.raises(PublicationError):
        evidence.packet_patch("posted", "2026-10-03T05:00:00-06:00")


def add_tagged(ledger, n, start=0):
    data = rows(ledger)
    for i in range(start, start + n):
        data.append(post(f"new-post-{i}", "2026-09-21", ALL_PENDING, packet_status="sent",
                         packet_tagging=evidence.PACKET_TAGGING))
    ledger.write_text(json.dumps(data))


def set_alerted(ingest, days_ago):
    import datetime as _dt
    state = json.loads(ingest.STATE_FILE.read_text())
    moment = _dt.datetime.now(_dt.UTC) - _dt.timedelta(days=days_ago)
    state["alerted_at"] = moment.isoformat()
    ingest.STATE_FILE.write_text(json.dumps(state))


def test_the_dead_man_re_alerts_weekly_not_daily(ingest, ledger, monkeypatch, capsys):
    monkeypatch.setattr(ingest, "utm_arrivals", lambda days: 87)
    assert ingest.cmd_check(check_args()) == 1, "onset always alerts"
    # One more unreceipted post a day: worse, but inside the weekly floor -> silent.
    for day in range(1, 4):
        add_tagged(ledger, 1, start=day)
        assert ingest.cmd_check(check_args()) == 0, f"day {day} re-paged"
    out = capsys.readouterr().out
    assert "inside the re-alert floor" in out
    assert json.loads(ingest.STATE_FILE.read_text())["high_water"] == 4
    # A week after the last alert, a still-worsening gap pages again.
    set_alerted(ingest, 8)
    add_tagged(ledger, 1, start=10)
    assert ingest.cmd_check(check_args()) == 1
    # Inside the floor, a jump of >= realert_jump since the last alert pages at once.
    add_tagged(ledger, 10, start=20)
    assert ingest.cmd_check(check_args()) == 1
    state = json.loads(ingest.STATE_FILE.read_text())
    assert state["alerted_count"] == state["high_water"] == 15


def test_the_first_run_after_deploy_does_not_page_for_history(ingest, ledger, monkeypatch,
                                                              capsys):
    """Every packet before this deploy lacks a receipt; that is a figure, not an alert."""
    monkeypatch.setattr(ingest, "utm_arrivals", lambda days: 87)
    data = [r for r in rows(ledger) if r["slug"] != "fresh-pending-post"]
    for i in range(89):
        data.append(post(f"old-post-{i}", "2026-07-01", ALL_ASSUMED))
    ledger.write_text(json.dumps(data))
    assert ingest.cmd_check(check_args()) == 0
    out = capsys.readouterr().out
    assert "historical-unverified: 90 packeted post(s)" in out
    assert "UNRECORDED" not in out
    # A state file left by the previous code (a high mark from the old all-rows count)
    # resolves as a one-time all-clear, never as a page.
    ingest.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ingest.STATE_FILE.write_text(json.dumps({"high_water": 89}))
    assert ingest.cmd_check(check_args()) == 3
    assert "historical-unverified figure" in capsys.readouterr().out


def test_mark_missed_is_a_real_off_ramp(ingest, ledger, monkeypatch, capsys):
    monkeypatch.setattr(ingest, "utm_arrivals", lambda days: 87)
    assert ingest.cmd_check(check_args()) == 1
    writer = module("syndication-reconcile")
    monkeypatch.setattr(writer, "LEDGER", ledger)
    assert writer.main(["--mark-missed", "2026-09-20", "--surface", "x"]) == 0
    assert ingest.cmd_check(check_args()) == 3, "an owner report answers the gap"


def test_the_wrapper_alert_names_the_off_ramps():
    text = (SCRIPTS / "blog-syndication-ingest.sh").read_text()
    alert = next(line for line in text.splitlines() if line.strip().startswith('alert "${STALE'))
    for ramp in ("post URLs", "weekly URL paste", "--mark-missed"):
        assert ramp in alert
