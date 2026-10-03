#!/usr/bin/env python3
"""Close the syndication loop: read Ezekiel's packet replies, record what shipped.

THE GAP THIS FIXES
------------------
`references/ezekiel/02-daily-sop.md` tells the poster to reply to the packet
email with the resulting URLs. Nothing ever read those replies, so every
`syndication.*.status` in `.blog-syndication-ledger.json` stayed "pending"
forever regardless of what actually got posted, and the Monday team rollup
reported zero syndication as if nobody had done the work. The loop was
open-ended by construction: packet out, nothing back in.

WHAT COUNTS AS A RECEIPT (2026-10-03, audit 226f §3.2)
-----------------------------------------------------
Only a URL on the platform it claims. Each one is appended to
`publication_evidence.<surface>` (blogpipe/evidence.py) as
{status: posted, url, source: reply|paste, observed_at, recorded_at, evidence_ref}.
The legacy `syndication.<surface>.status` is only upgraded from `pending`; an
`assumed_posted` belief is never rewritten into `posted`, it gains an observation
beside it. A reply with no URL ("I already knocked out 5-7!") is a claim, not a
receipt, and is reported but not recorded.

Receipts are accepted from a CONFIGURED list of internal senders, not one
hardcoded address. The old FROM filter named only the poster, so the only two
receipts in six months (both from the owner, 2026-08-19/20) were never read.
The list is `SYNDICATION_RECEIPT_SENDERS` (comma-separated) from the process
environment or the blog/.env the posting packet already reads; when unset it
falls back to that file's packet recipients (EZEKIEL_EMAIL, PACKET_CC). With no
list at all, ingest refuses rather than accepting mail from anyone.

From is only a claim, so an allow-listed From must also be AUTHENTICATED before
anything is recorded (sender_authenticated). MXroute, our mailbox host, adds no
Authentication-Results header (checked read-only against the live INBOX on
2026-10-03); it leaves two other marks, and either one is accepted:
  * internal mail: the hop where the message entered our MX is an authenticated
    submission (`by <MX> with esmtpsa|esmtpa`, RFC 3848) and its envelope sender
    is on the From domain;
  * external mail (e.g. a Gmail reply): the MX's appended `X-DKIM: signer='<d>'
    status='pass'` verdict for a DKIM-Signature the message carries, aligned with
    the From domain.
The trusted MX defaults to SMTP_HOST (override: SYNDICATION_TRUSTED_MX). A host
that does emit RFC 8601 Authentication-Results can be trusted by listing its
authserv-id in SYNDICATION_AUTHSERV_IDS (off by default, because a header our MX
never writes is a header it may also never strip). SYNDICATION_RECEIPT_AUTH=off
disables the requirement; default on. Our own packet emails are skipped by subject.

Two receipt formats are read:
  * the packet-reply format (label lines, e.g. "LinkedIn personal: <url>"), tied
    to a post by "posted YYYY-MM-DD", the canonical URL, or the title;
  * the WEEKLY URL PASTE, one self-identifying line per post and surface:
        2026-09-21 li_personal https://www.linkedin.com/feed/update/...
        some-post-slug x https://x.com/handle/status/123
    in any message from an internal sender, or locally via --paste-file.

Two modes:

  ingest   Parse replies over IMAP (and/or a paste file) and append receipts.
  check    Dead-man switch over publication EVIDENCE. Exit contract mirrors
           blog-tier-creep-guard: 0 silent, 1 onset/worsening, 3 recovered.
           `--stateless` is the exception: it reports without touching the
           hysteresis mark and returns 2 when a gap exists, 0 when clean, so
           a human can inspect mid-incident without disarming the scheduled
           guard. Cron must therefore never pass --stateless.

WHAT `check` ACTUALLY MEASURES
------------------------------
The ledger measures BOOKKEEPING (did a reply email arrive). UTM measures WORK
(did a reader actually arrive from a syndicated link). These are not the same
signal, and conflating them is dangerous: on 2026-08-06 the ledger showed 29
posts with nothing recorded while Umami showed 32 UTM-tagged arrivals, 16 of
them carrying LinkedIn's `trk=public_post_comment-text` marker, which is proof
the poster was placing links in the first comment exactly as the SOP requires.

A ledger-only guard would have paged "poster inactive" about someone doing the
job correctly, so `check` never accuses anyone: its alarm says publication is
UNVERIFIED, which is a statement about our evidence, not about the poster.

What it no longer does (2026-10-03, audit 226d §e): let that site-wide UTM count
SATISFY the check. A 30-day count of every tagged arrival on the site cannot be
attributed to any one post, so it was permanently positive (~87) and silenced the
dead-man for good. The count is still printed, labelled `unverified`, and the
gap goes through the normal onset/hysteresis path. Held packets (packet_status
"held", a do-not-post instruction) are excluded: nothing should be live for them.

Baseline and re-alert floor (2026-10-03): only rows whose packet carries the
`packet_tagging` marker (written by `mark-packet` since receipts existed) can raise
the alarm. Older packeted rows without a receipt are printed as one
historical-unverified figure and never page. And because every new daily post
without a receipt raises the count by one, a worsening gap re-alerts at most once
per --realert-days (7) unless it jumps by --realert-jump (10) since the last alert;
onset always alerts. Every alert names its off-ramps: reply with URLs, the weekly
paste, or `syndication-reconcile.py --mark-missed`.

Deterministic and side-effect-light: stdlib only, read-only on the mailbox
(never deletes or flags mail), atomic ledger writes, it never downgrades a
destination that is already recorded, and a failed UTM query degrades to
ledger-only reasoning rather than inventing a verdict.
"""

from __future__ import annotations

import argparse
import email
import hashlib
import imaplib
import json
import os
import re
import ssl
import sys
import tempfile
from datetime import UTC, datetime, timedelta
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path

# No __pycache__ beside the gate package (see blogpipe/__init__.py), set before import.
sys.dont_write_bytecode = True
# Support direct CLI execution and importlib-loaded hyphenated script tests.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import blog_publication_state as publication_state  # noqa: E402
from blogpipe import evidence  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / ".blog-syndication-ledger.json"
ENV_FILE = Path.home() / "000-projects" / "intent-mail" / ".env"
# The posting packet's own config file (EZEKIEL_EMAIL / PACKET_CC live here), which is
# where the internal receipt-sender list belongs too. Addresses are config, never code.
BLOG_ENV_FILE = REPO.parent / ".env"

# Label -> ledger key. The SOP's example reply uses exactly these labels. Order
# matters: "X article" must be tried before the bare "X" label.
LABEL_KEYS = [
    (re.compile(r"^\s*[-*]?\s*linkedin\s+personal\b", re.I), "li_personal"),
    (re.compile(r"^\s*[-*]?\s*linkedin\s+company\b", re.I), "li_company"),
    (re.compile(r"^\s*[-*]?\s*(x|twitter)\s+(long[- ]form\s+)?article\b", re.I), "x_article"),
    (re.compile(r"^\s*[-*]?\s*(x|twitter)\b", re.I), "x"),
    (re.compile(r"^\s*[-*]?\s*substack\b", re.I), "substack"),
    (re.compile(r"^\s*[-*]?\s*medium\b", re.I), "medium"),
    (re.compile(r"^\s*[-*]?\s*(buy\s*me\s*a\s*coffee|bmc)\b", re.I), "buymeacoffee"),
]

# Weekly URL paste: "<YYYY-MM-DD|slug> <surface> <url>", one receipt per line.
PASTE_RE = re.compile(
    r"^\s*[-*]?\s*(?P<post>\d{4}-\d{2}-\d{2}|[a-z0-9][a-z0-9-]{2,199})\s+"
    r"(?P<surface>" + "|".join(evidence.SURFACES) + r")\s*[:=]?\s+(?P<url>https?://\S+)\s*$"
)

# Fallback when a reply omits labels: sniff the URL's host. LinkedIn is
# deliberately absent here because /feed/update/ URLs do not distinguish a
# personal post from a company one; guessing would write a wrong record, and a
# wrong record is worse than an unrecorded one.
HOST_KEYS = [
    (re.compile(r"https?://(www\.)?(x|twitter)\.com/(i/)?[\w/]*articles?/", re.I), "x_article"),
    (re.compile(r"https?://(www\.)?(x|twitter)\.com/", re.I), "x"),
    (re.compile(r"https?://[\w.-]*substack\.com/", re.I), "substack"),
    (re.compile(r"https?://(www\.)?medium\.com/", re.I), "medium"),
    (re.compile(r"https?://(www\.)?buymeacoffee\.com/", re.I), "buymeacoffee"),
]

URL_RE = re.compile(r"https?://[^\s<>\)\]\"']+")
POSTED_DATE_RE = re.compile(r"\bposted\s+(\d{4}-\d{2}-\d{2})", re.I)
DESTINATIONS = ("x", "li_personal", "li_company", "substack", "medium")
SENDER_KEYS = ("SYNDICATION_RECEIPT_SENDERS", "EZEKIEL_EMAIL", "PACKET_CC",
               "SYNDICATION_RECEIPT_AUTH", "SYNDICATION_TRUSTED_MX", "SYNDICATION_AUTHSERV_IDS")
# Our own outgoing packet ("📣 POST THIS — ..."/"📣 POST THESE — ..."), not a reply to it.
PACKET_SUBJECT_RE = re.compile(r"^\s*\U0001F4E3\s*POST\s+TH(?:IS|ESE)\b", re.I)
OFF_RAMPS = ("close it by replying to the packet with the post URLs, sending the weekly URL "
             "paste (<YYYY-MM-DD|slug> <surface> <url>, one per line), or recording a known "
             "miss with syndication-reconcile.py --mark-missed YYYY-MM-DD [--surface S]")


def read_env_file(path: Path) -> dict:
    env = {}
    if path.exists():
        for line in path.read_text(errors="replace").splitlines():
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line.strip())
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return env


def load_env() -> dict:
    """Read SMTP_* from intent-mail's .env and the sender keys from blog/.env.

    Values are never printed. The process environment wins over either file.
    """
    env = read_env_file(ENV_FILE)
    blog = read_env_file(BLOG_ENV_FILE)
    for k in SENDER_KEYS:
        if blog.get(k):
            env[k] = blog[k]
    for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", *SENDER_KEYS):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def receipt_senders(env: dict, override: list | None = None) -> list:
    """The internal sender allowlist, lowercased. Empty means "refuse", never "anyone".

    Explicit --sender flags win; then SYNDICATION_RECEIPT_SENDERS; then the packet's
    own recipients (EZEKIEL_EMAIL, PACKET_CC), because whoever the packet goes to is by
    definition someone whose reply about it we should read.
    """
    if override:
        raw = list(override)
    elif env.get("SYNDICATION_RECEIPT_SENDERS"):
        raw = [env["SYNDICATION_RECEIPT_SENDERS"]]
    else:
        raw = [env.get("EZEKIEL_EMAIL", ""), env.get("PACKET_CC", "")]
    out = []
    for chunk in raw:
        for addr in re.split(r"[,;\s]+", chunk or ""):
            addr = actor(addr).lower()
            if addr != "reply" and addr not in out:
                out.append(addr)
    return out


def load_ledger() -> list:
    if not LEDGER.is_file():
        raise FileNotFoundError(f"missing syndication ledger: {LEDGER}")
    return publication_state.load_state(LEDGER)


def write_ledger(entries: list) -> None:
    """Caller holds state_locked from its latest read through publication."""
    publication_state.atomic_state(LEDGER, entries)


def body_text(msg: email.message.Message) -> str:
    """Prefer text/plain; fall back to de-tagged HTML."""
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                parts.append(part.get_payload(decode=True) or b"")
    else:
        parts.append(msg.get_payload(decode=True) or b"")
    text = b"\n".join(parts).decode("utf-8", errors="replace")
    if text.strip():
        return text
    html = []
    for part in (msg.walk() if msg.is_multipart() else [msg]):
        if part.get_content_type() == "text/html":
            html.append((part.get_payload(decode=True) or b"").decode("utf-8", "replace"))
    return re.sub(r"<[^>]+>", " ", "\n".join(html))


def parse_reply(text: str) -> dict:
    """Extract {destination: url} from a reply body.

    Label lines win over host sniffing so an X link pasted on the LinkedIn line
    is recorded the way the human labelled it.
    """
    found = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        urls = URL_RE.findall(line)
        if not urls:
            continue
        url = urls[0].rstrip(".,;")
        for pattern, key in LABEL_KEYS:
            if pattern.search(line):
                found.setdefault(key, url)
                break
        else:
            for pattern, key in HOST_KEYS:
                if pattern.search(url):
                    found.setdefault(key, url)
                    break
    return found


def actor(from_header: str) -> str:
    """Bare address from a From header, or 'reply' if it is not a clean address.

    Splitting on '<' persisted whatever the header happened to contain: a
    display-name-only From ("Ezekiel Smith") stored the display name, and a
    malformed or spoofed header stored its raw text straight into the ledger.
    parseaddr does the RFC parse; the shape check refuses anything that is not
    recognisably an address rather than recording an attacker-controlled string.
    """
    _, addr = parseaddr(from_header or "")
    if addr and re.fullmatch(r"[^@\s<>\"]+@[^@\s<>\"]+\.[^@\s<>\"]+", addr):
        return addr
    return "reply"


def _aligned(signer: str, domain: str) -> bool:
    """Relaxed alignment: same domain, or one is a subdomain of the other."""
    signer, domain = signer.lower().lstrip("@").rstrip("."), domain.lower()
    return bool(signer) and (signer == domain or signer.endswith("." + domain)
                             or domain.endswith("." + signer))


def _flat(value) -> str:
    return " ".join(str(value).split())


def receipt_auth_config(env: dict) -> tuple[bool, set, set]:
    """-> (required, trusted MX hosts, trusted authserv-ids). Required unless set off."""
    required = (env.get("SYNDICATION_RECEIPT_AUTH") or "on").strip().lower() not in (
        "off", "0", "false", "no")
    split = lambda raw: {h.lower() for h in re.split(r"[,;\s]+", raw or "") if h}  # noqa: E731
    mx = split(env.get("SYNDICATION_TRUSTED_MX")) or split(env.get("SMTP_HOST"))
    return required, mx, split(env.get("SYNDICATION_AUTHSERV_IDS"))


def sender_authenticated(msg: email.message.Message, trusted_mx: set,
                         authserv_ids: set = frozenset()) -> tuple[bool, str]:
    """Is the From domain authenticated by OUR mail host? -> (ok, how-or-why-not).

    Received headers are prepended, so the ones above the entry hop were written by our
    MX and cannot be forged by the sender; everything below the entry hop can be.
    """
    addr = actor(msg.get("From") or "").lower()
    if addr == "reply":
        return False, "From is not a clean address"
    domain = addr.rsplit("@", 1)[1]

    for header in msg.get_all("Authentication-Results") or []:
        text = _flat(header)
        if text.split(";", 1)[0].strip().lower() not in authserv_ids:
            continue
        for method, prop in (("dkim", "header.d"), ("dmarc", "header.from")):
            for m in re.finditer(rf"\b{method}=pass\b[^;]*?\b{re.escape(prop)}=([\w.-]+)", text,
                                 re.I):
                if _aligned(m.group(1), domain):
                    return True, f"authentication-results {method}=pass"

    hops = [_flat(r) for r in msg.get_all("Received") or []]
    entry = None
    for hop in hops:
        by = re.search(r"\bby\s+([\w.-]+)", hop)
        if not by or by.group(1).lower() not in trusted_mx:
            return False, "the top Received hop is not our mail host"
        proto = re.search(r"\bwith\s+([\w-]+)", hop)
        proto = proto.group(1).lower() if proto else ""
        # Delivery and content-scan hops inside the MX are not where the message entered.
        if proto in ("lmtp", "lmtpa", "local", "spam-scanned") or re.match(r"from mail by ", hop):
            continue
        entry = (hop, proto)
        break
    if entry is None:
        return False, "no entry hop by our mail host"
    hop, proto = entry
    if proto.endswith("a"):  # RFC 3848: ESMTPA / ESMTPSA = authenticated submission
        env_from = re.search(r"envelope-from <[^@<>]+@([\w.-]+)>", hop, re.I)
        if env_from and not _aligned(env_from.group(1), domain):
            return False, "authenticated submission, but the envelope sender is off-domain"
        return True, f"authenticated submission ({proto}) to our mail host"

    signed = [m.group(1) for sig in msg.get_all("DKIM-Signature") or []
              for m in [re.search(r"\bd=([\w.-]+)", _flat(sig))] if m]
    if not any(_aligned(d, domain) for d in signed):
        return False, "external mail with no DKIM signature for the From domain"
    # The MX appends one verdict per signature at the END of the header block, after
    # anything the sender wrote, so only the last len(signed) verdicts are its own.
    verdicts = [_flat(v) for v in msg.get_all("X-DKIM") or []][-len(signed):]
    for verdict in verdicts:
        m = re.search(r"signer='([^']*)'\s+status='([^']*)'", verdict)
        if m and m.group(2).lower() == "pass" and _aligned(m.group(1), domain):
            return True, "DKIM pass for the From domain (our mail host's verdict)"
    return False, "no passing DKIM verdict from our mail host for the From domain"


def match_entry(entries: list, subject: str, text: str) -> dict | None:
    """Tie a reply to a ledger post: explicit date, then canonical URL, then title."""
    m = POSTED_DATE_RE.search(text)
    if m:
        for e in entries:
            if e.get("date") == m.group(1):
                return e

    # Canonical match must be boundary-anchored and longest-wins. A plain
    # substring test mis-attributes whenever one slug prefixes another:
    # ".../posts/foo" is a substring of ".../posts/foo-part-2", so a reply
    # about part 2 would be recorded against post one. Requiring the next
    # character to be a non-slug character (not [A-Za-z0-9_-]) rejects that
    # while still allowing a trailing slash, query string, or end of line.
    best, best_len = None, -1
    for e in entries:
        canonical = (e.get("canonical_url") or "").rstrip("/")
        if not canonical:
            continue
        if re.search(re.escape(canonical) + r"(?![A-Za-z0-9_-])", text):
            if len(canonical) > best_len:
                best, best_len = e, len(canonical)
    if best is not None:
        return best
    hay = f"{subject} {text}".lower()
    best = None
    for e in entries:
        title = (e.get("title") or "").lower()
        if len(title) > 12 and title in hay:
            if best is None or len(title) > len(best.get("title") or ""):
                best = e
    return best


def fetch_replies(env: dict, days: int, senders: list) -> list:
    """Messages from the internal sender allowlist in the window (read-only).

    The allowlist is applied to the parsed From address after the fetch rather than
    as one IMAP FROM criterion, because IMAP FROM is a substring match on a single
    value and the list has several. An empty list is refused by the caller.
    """
    host = env.get("SMTP_HOST")
    user = env.get("SMTP_USER")
    password = env.get("SMTP_PASS")
    if not (host and user and password):
        raise SystemExit("FATAL: SMTP_HOST/SMTP_USER/SMTP_PASS unavailable")

    since = (datetime.now(UTC) - timedelta(days=days)).strftime("%d-%b-%Y")
    out = []
    conn = imaplib.IMAP4_SSL(host, 993, ssl_context=ssl.create_default_context())
    try:
        conn.login(user, password)
        conn.select("INBOX", readonly=True)  # readonly: never mutate the mailbox
        allowed = {s.lower() for s in senders}
        required, trusted_mx, authserv_ids = receipt_auth_config(env)
        typ, data = conn.search(None, "SINCE", since)
        if typ != "OK":
            return out
        for num in (data[0].split() if data and data[0] else []):
            typ, raw = conn.fetch(num, "(RFC822)")
            if typ != "OK" or not raw or not raw[0]:
                continue
            msg = email.message_from_bytes(raw[0][1])
            if actor(msg.get("From") or "").lower() not in allowed:
                continue
            record = message_record(msg, raw[0][1])
            if PACKET_SUBJECT_RE.match(record["subject"]):
                continue  # our own packet (a CC'd copy), not a reply to it
            if required:
                ok, why = sender_authenticated(msg, trusted_mx, authserv_ids)
                if not ok:
                    record["auth_failure"] = why
            out.append(record)
    finally:
        try:
            conn.logout()
        except Exception:
            pass
    return out


def message_record(msg: email.message.Message, raw: bytes) -> dict:
    """The fields a receipt needs: who, when, what it said, and how to find it again."""
    subject = str(make_header(decode_header(msg.get("Subject") or "")))
    message_id = (msg.get("Message-ID") or "").strip()
    try:
        sent = parsedate_to_datetime(msg.get("Date") or "")
        sent = sent if sent.tzinfo else sent.replace(tzinfo=UTC)
        observed = sent.astimezone(UTC).isoformat()
    except (TypeError, ValueError):
        observed = None
    return {
        "subject": subject,
        "from": msg.get("From") or "",
        "text": body_text(msg),
        "observed_at": observed,
        "evidence_ref": (f"message-id:{message_id}" if message_id
                         else f"sha256:{hashlib.sha256(raw).hexdigest()}"),
    }


def parse_paste(text: str) -> list:
    """Weekly URL paste lines -> [(post_key, surface, url, line_number)]."""
    out = []
    for number, raw in enumerate(text.splitlines(), 1):
        m = PASTE_RE.match(raw)
        if m:
            out.append((m.group("post"), m.group("surface"),
                        m.group("url").rstrip(".,;"), number))
    return out


def entry_for_key(entries: list, key: str) -> dict | None:
    """A paste line names its post by date (must be unique) or by slug."""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", key):
        hits = [e for e in entries if e.get("date") == key]
    else:
        hits = [e for e in entries if e.get("slug") == key]
    return hits[0] if len(hits) == 1 else None


def receipts_from_message(entries: list, message: dict, source: str) -> tuple[list, list]:
    """-> (receipts, problems). A receipt is (entry, surface, url, evidence_ref)."""
    receipts, problems = [], []
    # A message without a captured reference still gets a stable one: the content hash.
    ref = message.get("evidence_ref") or "sha256:" + hashlib.sha256(
        f"{message.get('subject', '')}\n{message['text']}".encode()).hexdigest()
    pasted = parse_paste(message["text"])
    if pasted:
        for key, surface, url, number in pasted:
            entry = entry_for_key(entries, key)
            if entry is None:
                problems.append(f"UNMATCHED paste line {number}: no unique post for {key!r}")
                continue
            receipts.append((entry, surface, url, f"{ref}#L{number}"))
        return receipts, problems
    found = parse_reply(message["text"])
    if not found:
        if URL_RE.search(message["text"]) is None:
            problems.append(
                f"NO-URL message from an internal sender ({message['subject'][:60]!r}): "
                "a claim without a post URL is not a receipt; not recorded")
        return receipts, problems
    entry = match_entry(entries, message["subject"], message["text"])
    if entry is None:
        problems.append(f"UNMATCHED reply: {message['subject'][:70]}")
        return receipts, problems
    for surface, url in found.items():
        receipts.append((entry, surface, url, ref))
    return receipts, problems


def apply_receipts(entries: list, messages: list, source: str) -> tuple[int, list]:
    """Append every valid receipt to its row. Never rewrites a belief into `posted`."""
    recorded, notes = 0, []
    now = now_iso()
    for message in messages:
        receipts, problems = receipts_from_message(entries, message, source)
        notes.extend(problems)
        for entry, surface, url, ref in receipts:
            if not evidence.receipt_url_ok(surface, url):
                notes.append(f"REJECTED {entry.get('date')} {surface}: {url[:80]} is not a "
                             f"{surface} post URL")
                continue
            outcome = evidence.record_observation(
                entry, surface, url, source=source,
                observed_at=message.get("observed_at") or now,
                evidence_ref=ref, recorded_at=now)
            if outcome != "duplicate":
                recorded += 1
            print(f"  {entry.get('date')} {surface} -> evidence {outcome}")
    return recorded, notes


def paste_message(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "subject": f"paste file {path.name}",
        "from": "",
        "text": data.decode("utf-8", errors="replace"),
        "observed_at": None,
        "evidence_ref": f"paste:sha256:{hashlib.sha256(data).hexdigest()}",
    }


def cmd_ingest(args) -> int:
    entries = load_ledger()
    if not entries:
        print("ledger empty; nothing to reconcile")
        return 0

    batches, unauthenticated = [], []
    paste_file = getattr(args, "paste_file", None)
    if paste_file:
        batches.append(("paste", [paste_message(Path(paste_file))]))
        print(f"read paste file {Path(paste_file).name}")
    if not getattr(args, "no_mail", False):
        env = load_env()
        senders = receipt_senders(env, getattr(args, "sender", None))
        if not senders:
            print("FATAL: no internal receipt senders configured "
                  "(SYNDICATION_RECEIPT_SENDERS or EZEKIEL_EMAIL/PACKET_CC in blog/.env); "
                  "refusing to read receipts from anyone", file=sys.stderr)
            return 2
        if not receipt_auth_config(env)[0]:
            print("WARN: SYNDICATION_RECEIPT_AUTH=off; an allow-listed From is trusted "
                  "without authentication")
        replies = fetch_replies(env, args.days, senders)
        print(f"scanned {len(replies)} message(s) from {len(senders)} configured "
              f"internal sender(s) in the last {args.days}d")
        # A pasted list inside an email is a paste; anything else is a packet reply.
        for reply in replies:
            if reply.get("auth_failure"):
                unauthenticated.append(
                    f"UNAUTHENTICATED message claiming an allow-listed sender "
                    f"({reply.get('subject', '')[:60]!r}): {reply['auth_failure']}; not recorded")
                continue
            batches.append(("paste" if parse_paste(reply["text"]) else "reply", [reply]))

    recorded, notes = 0, list(unauthenticated)
    # IMAP fetch is outside the lock; match and mutate the CURRENT ledger below.
    with publication_state.state_locked(LEDGER.parent):
        entries = load_ledger()
        for source, messages in batches:
            n, problems = apply_receipts(entries, messages, source)
            recorded += n
            notes.extend(problems)
        if recorded and not args.dry_run:
            write_ledger(entries)
    if recorded and not args.dry_run:
        print(f"ledger updated: {recorded} receipt(s) appended as publication evidence")
    elif recorded:
        print(f"DRY-RUN: would append {recorded} receipt(s)")
    else:
        print("no new receipts to record")
    for note in notes:
        print(f"NOTE: {note}")
    return 0


STATE_FILE = Path.home() / ".local" / "state" / "blog-syndication-ingest" / "state.json"
HOME_ENV = Path.home() / ".env"
UMAMI_SITE = "4071f4db-4249-4ce6-a929-665598975d67"  # startaitools.com
UMAMI_ROW_LIMIT = 500


def utm_arrivals(days: int) -> int | None:
    """Count UTM-tagged arrivals on startaitools.com over the window.

    This is the ground truth the ledger cannot see. The ledger records only
    what the poster emails back; UTM records what the internet actually did.
    Conflating the two is how an absent reply becomes an accusation that
    nobody posted.

    Returns None when Umami cannot be reached, so the caller degrades to
    ledger-only reasoning instead of inventing a verdict from a failed query.
    """
    try:
        import urllib.request

        env = {}
        if HOME_ENV.exists():
            for line in HOME_ENV.read_text(errors="replace").splitlines():
                m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line.strip())
                if m:
                    env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
        url = env.get("UMAMI_URL") or "https://analytics.intentsolutions.io"
        user, pw = env.get("UMAMI_USERNAME"), env.get("UMAMI_PASSWORD")
        if not (user and pw):
            return None

        def post_json(path, payload, token=None):
            req = urllib.request.Request(
                url.rstrip("/") + path,
                data=json.dumps(payload).encode() if payload is not None else None,
                headers={"Content-Type": "application/json",
                         **({"Authorization": f"Bearer {token}"} if token else {})},
                method="POST" if payload is not None else "GET")
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())

        token = post_json("/api/auth/login", {"username": user, "password": pw}).get("token")
        if not token:
            return None
        end = int(datetime.now(UTC).timestamp() * 1000)
        start = end - days * 86400 * 1000
        # type=query is deliberate and load-bearing. DO NOT "correct" this to
        # type=utm_source: that type returns HTTP 400 on this Umami version.
        # With type=query each row's `x` is the FULL query string, verified
        # live 2026-08-06:
        #     {"x": "trk=public_post_comment-text&utm_source=linkedin", "y": 16}
        #     {"x": "utm_source=x", "y": 7}
        # which is why the substring test below is correct rather than a bug.
        #
        # Umami returns one row per distinct query string, and UTM campaigns
        # multiply those fast (utm_source alone, +medium, +campaign, plus
        # LinkedIn's own trk= prefix all count separately). A low cap would
        # silently truncate and undercount the very number the verdict rests
        # on, so ask for far more rows than the tail can plausibly reach.
        rows = post_json(
            f"/api/websites/{UMAMI_SITE}/metrics"
            f"?startAt={start}&endAt={end}&type=query&limit={UMAMI_ROW_LIMIT}",
            None, token)
        if not isinstance(rows, list):
            return None
        if len(rows) >= UMAMI_ROW_LIMIT:
            # Truncated: the sum is a floor, not a total. It can only be an
            # undercount, so a positive verdict stays sound; say so rather
            # than report a number we cannot stand behind.
            print(f"NOTE: Umami returned {len(rows)} rows (cap reached); "
                  "UTM count below is a lower bound")
        return sum(r.get("y", 0) for r in rows if "utm_source" in (r.get("x") or ""))
    except Exception:
        return None


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


def load_state() -> dict:
    """Always hand back a dict.

    json.loads happily returns a list, string or number for a file that is
    valid JSON but not an object, and every caller then does .get() on it and
    raises. A guard that crashes on its own state file is a guard that is
    silently absent, so anything not an object degrades to empty.
    """
    try:
        data = json.loads(STATE_FILE.read_text())
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(STATE_FILE.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(state, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, STATE_FILE)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


def cmd_check(args) -> int:
    """Dead-man switch: packeted long ago, still nothing recorded.

    Exit contract mirrors blog-tier-creep-guard (the estate's existing
    hysteresis precedent), so this can run daily without becoming a nag:

      0  silent   healthy, OR a breach that merely persists at its known size
      1  ALERT    breach onset, or worsening past the recorded high-water mark
      3  RECOVER  was breached, now clean (one-time all-clear)

    State lives outside the repo so a guard run never dirties the working tree
    and trips the lander's clean-tree precondition.
    """
    entries = load_ledger()
    cutoff = datetime.now(UTC) - timedelta(hours=args.stale_hours)
    stale, historical = [], []
    held = 0
    for e in entries:
        if not e.get("packet_sent"):
            continue
        if evidence.is_held(e):
            held += 1
            continue
        published = e.get("published_at") or ""
        try:
            when = datetime.fromisoformat(published)
            if when.tzinfo is None:
                when = when.replace(tzinfo=UTC)
        except ValueError:
            continue
        if when > cutoff:
            continue
        # `assumed_posted` is excluded ON PURPOSE. It is a BELIEF written by
        # syndication-reconcile.py from an owner standing instruction ("assume he
        # posted unless I say otherwise"), not a receipt. This dead-man exists to
        # detect that the reply-to-ledger path is not producing receipts, and a
        # belief must never be able to satisfy it.
        #
        # On 2026-08-11 the reconciler aged 187 rows to assumed_posted and this
        # check, which counted anything not pending/n-a as recorded, flipped from
        # a correct "UNRECORDED: 38 posts" to "loop healthy / RECOVERED: the gap
        # has cleared". Nothing had cleared. A working alarm was silenced by a
        # change made one layer above it, which is the exact failure this file was
        # written to catch.
        #
        # A receipt is a URL observation (publication_status == "posted") or an
        # explicit owner report (`not_posted`): either is an answer, not a gap.
        answered = [k for k in evidence.SURFACES
                    if evidence.publication_status(e, k) in ("posted", "not_posted")]
        if answered:
            continue
        # Baseline: a packet sent before receipts existed (no packet_tagging marker)
        # was never going to have one. It is history, reported as a figure, and must
        # not page on the first run after deploy or ever after.
        if e.get("packet_tagging") == evidence.PACKET_TAGGING:
            stale.append(e)
        else:
            historical.append(e)

    count = len(stale)
    if held:
        print(f"held: {held} packet(s) delivered as HOLD (do not post); not expected to be live")
    if historical:
        print(f"historical-unverified: {len(historical)} packeted post(s) predate publication "
              "receipts and have none. A fixed figure, not an alert; Substack/Medium were "
              "uninstrumented for them, so a zero there is not a measurement.")
    if count:
        print(f"UNRECORDED: {count} packeted post(s) with no publication evidence (URL receipt) "
              f"after {args.stale_hours}h. Publication is UNVERIFIED for these; that is a gap "
              "in our evidence, not evidence that nothing was posted.")
        for e in stale:
            print(f"  {e.get('date')}  {e.get('slug')}")
        print(f"OFF-RAMPS: {OFF_RAMPS}.")
    else:
        print("syndication loop healthy: every post packeted since receipts began has a "
              "publication receipt")

    # Corroborate against UTM before drawing any conclusion about the poster.
    # The ledger measures BOOKKEEPING (did a reply arrive); UTM measures WORK
    # (did the internet arrive from a syndicated link). On 2026-08-06 those two
    # diverged completely: 29 posts unrecorded while 32 UTM-tagged arrivals
    # proved syndication was live and correct, including LinkedIn
    # first-comment placement. A guard that reads only the ledger would have
    # paged "poster inactive" about someone doing the job properly.
    #
    # It is CONTEXT, never a verdict. The count is site-wide over a 30-day window, so
    # it cannot say which post (if any) the traffic belongs to: `unverified`. Only an
    # empty, successful query is a measurement (`verified_zero`), and an unreachable
    # or disabled query is `unavailable`. None of the three satisfies this check.
    utm = utm_arrivals(args.utm_days) if count and not args.no_utm else None
    measurement = None
    if count and args.no_utm:
        measurement = "unavailable"
        print("UTM corroboration: unavailable (disabled by --no-utm).")
    elif count and utm is None:
        measurement = "unavailable"
        print("UTM corroboration: unavailable (Umami unreachable or no credentials).")
    elif count and utm > 0:
        measurement = "unverified"
        print(f"UTM corroboration: unverified. {utm} site-wide tagged arrival(s) in the last "
              f"{args.utm_days}d show tagged links are in circulation, but they cannot be "
              "attributed to any of these posts and do not satisfy this check.")
    elif count:
        measurement = "verified_zero"
        print(f"UTM corroboration: verified_zero. No tagged arrivals at all in the last "
              f"{args.utm_days}d; syndication may have stopped.")

    # Stateless: report only, never read or write the high-water mark. This is
    # the mode for a human running it by hand mid-incident, so it answers the
    # literal question asked ("is anything unrecorded?") and is evaluated
    # BEFORE the UTM-informed returns below. Letting the UTM branch preempt it
    # made --stateless report 0 while a gap existed, contradicting its own
    # contract. Cron must never pass --stateless: it would disarm hysteresis.
    if args.stateless:
        return 2 if count else 0

    state = load_state()

    # A state file that is valid JSON but holds a non-integer marker (null, a
    # string, a hand-edit) must not wedge every future scheduled run. Degrade
    # to 0: the worst case is one re-alert, versus a guard that crashes daily
    # and is therefore silently absent, which is the failure class this whole
    # change exists to prevent.
    try:
        high_water = int(state.get("high_water", 0))
    except (TypeError, ValueError):
        print("WARN: unreadable high_water in state; treating as 0")
        high_water = 0
    high_water = max(high_water, 0)

    moment = datetime.now(UTC)
    now = moment.isoformat()

    if count == 0:
        if high_water > 0:
            save_state({"high_water": 0, "recovered_at": now})
            print("RECOVERED: the gap has cleared"
                  + (" (older packets are now the historical-unverified figure)"
                     if historical else ""))
            return 3
        return 0

    if count > high_water:
        # Re-alert floor. With no receipts arriving, every new daily post raises the
        # count by one, and "worsening" alone re-paged nearly every morning. Onset
        # always alerts; after that, at most once per realert_days unless the count
        # has jumped by realert_jump since the last alert. The mark still rises
        # silently in between, so improvement and recovery stay accurate.
        try:
            last_at = datetime.fromisoformat(str(state.get("alerted_at")))
            last_at = last_at if last_at.tzinfo else last_at.replace(tzinfo=UTC)
        except ValueError:
            last_at = None
        try:
            last_count = max(int(state.get("alerted_count", 0)), 0)
        except (TypeError, ValueError):
            last_count = 0
        due = last_at is None or moment - last_at >= timedelta(days=args.realert_days)
        jumped = count - last_count >= args.realert_jump
        if high_water == 0 or due or jumped:
            save_state({"high_water": count, "alerted_at": now, "alerted_count": count,
                        "measurement": measurement})
            print(f"ALERT: gap onset/worsening ({high_water} -> {count})")
            return 1
        save_state({**state, "high_water": count, "worsened_at": now})
        print(f"silent: gap worsened {high_water} -> {count}, inside the re-alert floor "
              f"(last alert at {last_count}, {state.get('alerted_at')}; next after "
              f"{args.realert_days}d or +{args.realert_jump})")
        return 0

    if count < high_water:
        # Ratchet the mark DOWN on improvement. Holding an all-time high would
        # mean a partial recovery (29 -> 3) silently swallows a real regression
        # back up to 10, because 10 < 29 still reads as "persistent".
        save_state({**state, "high_water": count, "improved_at": now})
        print(f"silent: gap improved to {count} (mark lowered from {high_water})")
        return 0

    print(f"silent: gap persists at {count} (high-water {high_water}), suppressed by hysteresis")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    ing = sub.add_parser("ingest", help="parse receipts and append publication evidence")
    ing.add_argument("--days", type=int, default=14)
    ing.add_argument("--sender", action="append", default=None,
                     help="internal sender to accept (repeatable); overrides the configured "
                          "SYNDICATION_RECEIPT_SENDERS list for this run")
    ing.add_argument("--paste-file", help="a weekly URL paste saved locally (source: paste)")
    ing.add_argument("--no-mail", action="store_true",
                     help="do not read the mailbox (use with --paste-file)")
    ing.add_argument("--dry-run", action="store_true")
    ing.set_defaults(func=cmd_ingest)

    chk = sub.add_parser("check", help="alert when packeted posts have nothing recorded")
    chk.add_argument("--stale-hours", type=int, default=48)
    chk.add_argument("--utm-days", type=int, default=30,
                     help="window for the UTM corroboration query")
    chk.add_argument("--no-utm", action="store_true",
                     help="skip UTM corroboration (ledger-only reasoning)")
    chk.add_argument("--realert-days", type=int, default=7,
                     help="after onset, re-alert a worsening gap at most this often")
    chk.add_argument("--realert-jump", type=int, default=10,
                     help="...unless it grew by at least this many posts since the last alert")
    chk.add_argument("--stateless", action="store_true",
                     help="report only; do not read or update the hysteresis high-water mark")
    chk.set_defaults(func=cmd_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
