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
  check    Dead-man switch, corroborated against UTM. Exit contract mirrors
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
job correctly. So `check` consults UTM before reaching any verdict, and only
treats the situation as an alarm when the ledger is empty AND the traffic is
too. Missing paperwork is a recording gap; missing traffic is an outage.

Deterministic and side-effect-light: stdlib only, read-only on the mailbox
(never deletes or flags mail), atomic ledger writes, it never downgrades a
destination that is already recorded, and a failed UTM query degrades to
ledger-only reasoning rather than inventing a verdict.
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
from datetime import UTC, datetime, timedelta
from email.header import decode_header, make_header
from email.utils import parseaddr
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


def fetch_replies(env: dict, days: int, sender: str) -> list:
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
    print(f"scanned {len(replies)} message(s) from "
          f"{args.sender or 'anyone'} in the last {args.days}d")

    updated, unmatched = 0, 0
    now = now_iso()
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
                "by": actor(reply["from"]),
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
    stale = []
    for e in entries:
        if not e.get("packet_sent"):
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
        syn = e.get("syndication") or {}
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
        NOT_A_RECEIPT = (None, "pending", "n/a", "assumed_posted")
        live = [k for k in DESTINATIONS
                if (syn.get(k) or {}).get("status") not in NOT_A_RECEIPT]
        if not live:
            stale.append(e)

    count = len(stale)
    if count:
        print(f"UNRECORDED: {count} packeted post(s) with no destination in the ledger "
              f"after {args.stale_hours}h")
        for e in stale:
            print(f"  {e.get('date')}  {e.get('slug')}")
    else:
        print("syndication loop healthy: every packeted post has at least one recorded destination")

    # Corroborate against UTM before drawing any conclusion about the poster.
    # The ledger measures BOOKKEEPING (did a reply arrive); UTM measures WORK
    # (did the internet arrive from a syndicated link). On 2026-08-06 those two
    # diverged completely: 29 posts unrecorded while 32 UTM-tagged arrivals
    # proved syndication was live and correct, including LinkedIn
    # first-comment placement. A guard that reads only the ledger would have
    # paged "poster inactive" about someone doing the job properly.
    utm = utm_arrivals(args.utm_days) if count and not args.no_utm else None
    utm_confirms = False
    if count and utm is not None:
        print(f"UTM corroboration: {utm} tagged arrival(s) in the last {args.utm_days}d")
        if utm > 0:
            utm_confirms = True
            print("VERDICT: recording gap only — syndication is demonstrably live. "
                  "The poster is working; the reply-to-ledger path is what is missing.")
        else:
            print("VERDICT: no ledger records AND no UTM arrivals — syndication may have stopped.")
    elif count and args.no_utm:
        print("UTM corroboration disabled by --no-utm; reasoning from the ledger alone. "
              "Absence of a record is not evidence that nothing was posted.")
    elif count:
        print("UTM corroboration UNAVAILABLE (Umami unreachable); reasoning from the "
              "ledger alone. Absence of a record is not evidence that nothing was posted.")

    # Stateless: report only, never read or write the high-water mark. This is
    # the mode for a human running it by hand mid-incident, so it answers the
    # literal question asked ("is anything unrecorded?") and is evaluated
    # BEFORE the UTM-informed returns below. Letting the UTM branch preempt it
    # made --stateless report 0 while a gap existed, contradicting its own
    # contract. Cron must never pass --stateless: it would disarm hysteresis.
    if args.stateless:
        return 2 if count else 0

    state = load_state()

    if utm_confirms:
        # Deliberately preserves the existing high_water instead of raising it
        # to `count`. That mark is the ALARM baseline; arming it from a
        # non-alarm would let this run mask the next one, because with Umami
        # unreachable and the same count the gap would read as "persistent"
        # and be silenced even though it could no longer be corroborated.
        # Corroboration is recorded alongside, so it stays visible in state
        # without suppressing anything.
        state["utm_confirmed_at"] = now_iso()
        state["utm_arrivals"] = utm
        save_state(state)
        return 0

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

    now = datetime.now(UTC).isoformat()

    if count == 0:
        if high_water > 0:
            save_state({"high_water": 0, "recovered_at": now})
            print("RECOVERED: the gap has cleared")
            return 3
        return 0

    if count > high_water:
        save_state({"high_water": count, "alerted_at": now})
        print(f"ALERT: gap onset/worsening ({high_water} -> {count})")
        return 1

    if count < high_water:
        # Ratchet the mark DOWN on improvement. Holding an all-time high would
        # mean a partial recovery (29 -> 3) silently swallows a real regression
        # back up to 10, because 10 < 29 still reads as "persistent".
        save_state({"high_water": count, "improved_at": now})
        print(f"silent: gap improved to {count} (mark lowered from {high_water})")
        return 0

    print(f"silent: gap persists at {count} (high-water {high_water}), suppressed by hysteresis")
    return 0


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
    chk.add_argument("--utm-days", type=int, default=30,
                     help="window for the UTM corroboration query")
    chk.add_argument("--no-utm", action="store_true",
                     help="skip UTM corroboration (ledger-only reasoning)")
    chk.add_argument("--stateless", action="store_true",
                     help="report only; do not read or update the hysteresis high-water mark")
    chk.set_defaults(func=cmd_check)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
