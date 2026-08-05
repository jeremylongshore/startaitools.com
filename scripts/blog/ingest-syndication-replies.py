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

Two modes:

  ingest   Parse replies over IMAP and write recorded posts into the ledger.
  check    Dead-man switch. Exit 2 if any post was packeted more than
           --stale-hours ago and still has zero recorded destinations. This is
           the alarm that would have caught the open loop weeks earlier.

Deterministic and side-effect-light: stdlib only, read-only on the mailbox
(never deletes or flags mail), atomic ledger writes, and it never downgrades a
destination that is already recorded.
"""

from __future__ import annotations

import argparse
import email
import imaplib
import json
import os
import re
import ssl
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from email.header import decode_header, make_header
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LEDGER = REPO / ".blog-syndication-ledger.json"
ENV_FILE = Path.home() / "000-projects" / "intent-mail" / ".env"

# Label -> ledger key. The SOP's example reply uses exactly these labels.
LABEL_KEYS = [
    (re.compile(r"^\s*[-*]?\s*linkedin\s+personal\b", re.I), "li_personal"),
    (re.compile(r"^\s*[-*]?\s*linkedin\s+company\b", re.I), "li_company"),
    (re.compile(r"^\s*[-*]?\s*(x|twitter)\b", re.I), "x"),
    (re.compile(r"^\s*[-*]?\s*substack\b", re.I), "substack"),
    (re.compile(r"^\s*[-*]?\s*medium\b", re.I), "medium"),
]

# Fallback when a reply omits labels: sniff the URL's host. LinkedIn is
# deliberately absent here because /feed/update/ URLs do not distinguish a
# personal post from a company one; guessing would write a wrong record, and a
# wrong record is worse than an unrecorded one.
HOST_KEYS = [
    (re.compile(r"https?://(www\.)?(x|twitter)\.com/", re.I), "x"),
    (re.compile(r"https?://[\w.-]*substack\.com/", re.I), "substack"),
    (re.compile(r"https?://(www\.)?medium\.com/", re.I), "medium"),
]

URL_RE = re.compile(r"https?://[^\s<>\)\]\"']+")
POSTED_DATE_RE = re.compile(r"\bposted\s+(\d{4}-\d{2}-\d{2})", re.I)
DESTINATIONS = ("x", "li_personal", "li_company", "substack", "medium")


def load_env() -> dict:
    """Read SMTP_* from intent-mail's .env. Values never printed."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(errors="replace").splitlines():
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", line.strip())
            if m:
                env[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def load_ledger() -> list:
    if not LEDGER.exists():
        return []
    with LEDGER.open() as fh:
        return json.load(fh)


def write_ledger(entries: list) -> None:
    """Atomic write. A half-written ledger would strand every future sweep."""
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(LEDGER.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(entries, fh, indent=2)
            fh.write("\n")
        json.loads(Path(tmp).read_text())  # parse-gate before it goes live
        os.replace(tmp, LEDGER)
    except Exception:
        Path(tmp).unlink(missing_ok=True)
        raise


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


def match_entry(entries: list, subject: str, text: str) -> dict | None:
    """Tie a reply to a ledger post: explicit date, then canonical URL, then title."""
    m = POSTED_DATE_RE.search(text)
    if m:
        for e in entries:
            if e.get("date") == m.group(1):
                return e
    for e in entries:
        canonical = e.get("canonical_url")
        if canonical and canonical.rstrip("/") in text:
            return e
    hay = f"{subject} {text}".lower()
    best = None
    for e in entries:
        title = (e.get("title") or "").lower()
        if len(title) > 12 and title in hay:
            if best is None or len(title) > len(best.get("title") or ""):
                best = e
    return best


def fetch_replies(env: dict, days: int, sender: str) -> list:
    host = env.get("SMTP_HOST")
    user = env.get("SMTP_USER")
    password = env.get("SMTP_PASS")
    if not (host and user and password):
        raise SystemExit("FATAL: SMTP_HOST/SMTP_USER/SMTP_PASS unavailable")

    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%d-%b-%Y")
    out = []
    conn = imaplib.IMAP4_SSL(host, 993, ssl_context=ssl.create_default_context())
    try:
        conn.login(user, password)
        conn.select("INBOX", readonly=True)  # readonly: never mutate the mailbox
        criteria = ["SINCE", since]
        if sender:
            criteria += ["FROM", sender]
        typ, data = conn.search(None, *criteria)
        if typ != "OK":
            return out
        for num in (data[0].split() if data and data[0] else []):
            typ, raw = conn.fetch(num, "(RFC822)")
            if typ != "OK" or not raw or not raw[0]:
                continue
            msg = email.message_from_bytes(raw[0][1])
            subject = str(make_header(decode_header(msg.get("Subject") or "")))
            out.append({"subject": subject, "from": msg.get("From") or "", "text": body_text(msg)})
    finally:
        try:
            conn.logout()
        except Exception:
            pass
    return out


def cmd_ingest(args) -> int:
    entries = load_ledger()
    if not entries:
        print("ledger empty; nothing to reconcile")
        return 0

    replies = fetch_replies(load_env(), args.days, args.sender)
    print(f"scanned {len(replies)} message(s) from {args.sender or 'anyone'} in the last {args.days}d")

    updated, unmatched = 0, 0
    now = datetime.now(timezone.utc).isoformat()
    for reply in replies:
        found = parse_reply(reply["text"])
        if not found:
            continue
        entry = match_entry(entries, reply["subject"], reply["text"])
        if entry is None:
            unmatched += 1
            print(f"  UNMATCHED reply: {reply['subject'][:70]}")
            continue
        syn = entry.setdefault("syndication", {})
        for key, url in found.items():
            slot = syn.setdefault(key, {})
            if slot.get("status") == "posted":
                continue  # never overwrite an existing record
            if slot.get("status") == "n/a":
                continue  # tier says this destination does not apply
            slot.update({
                "status": "posted",
                "posted_at": now,
                "url": url,
                "by": (reply["from"] or "").split("<")[-1].rstrip(">") or "reply",
            })
            updated += 1
            print(f"  {entry.get('date')} {key} -> posted")

    if updated and not args.dry_run:
        write_ledger(entries)
        print(f"ledger updated: {updated} destination(s) recorded")
    elif updated:
        print(f"DRY-RUN: would record {updated} destination(s)")
    else:
        print("no new destinations to record")
    if unmatched:
        print(f"NOTE: {unmatched} reply/replies could not be tied to a post")
    return 0


def cmd_check(args) -> int:
    """Dead-man switch: packeted long ago, still nothing recorded."""
    entries = load_ledger()
    cutoff = datetime.now(timezone.utc) - timedelta(hours=args.stale_hours)
    stale = []
    for e in entries:
        if not e.get("packet_sent"):
            continue
        published = e.get("published_at") or ""
        try:
            when = datetime.fromisoformat(published)
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if when > cutoff:
            continue
        syn = e.get("syndication") or {}
        live = [k for k in DESTINATIONS
                if (syn.get(k) or {}).get("status") not in (None, "pending", "n/a")]
        if not live:
            stale.append(e)

    if not stale:
        print("syndication loop healthy: every packeted post has at least one recorded destination")
        return 0

    print(f"SYNDICATION GAP: {len(stale)} packeted post(s) with nothing recorded "
          f"after {args.stale_hours}h")
    for e in stale:
        print(f"  {e.get('date')}  {e.get('slug')}")
    print("Either the poster is not posting, or replies are not reaching the ingester.")
    return 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    ing = sub.add_parser("ingest", help="parse packet replies and record posted URLs")
    ing.add_argument("--days", type=int, default=14)
    ing.add_argument("--sender", default="ezekiel@intentsolutions.io",
                     help="restrict to this sender; empty string scans all")
    ing.add_argument("--dry-run", action="store_true")
    ing.set_defaults(func=cmd_ingest)

    chk = sub.add_parser("check", help="alert when packeted posts have nothing recorded")
    chk.add_argument("--stale-hours", type=int, default=48)
    chk.set_defaults(func=cmd_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
