#!/usr/bin/env python3
"""blog-plane-card.py: mirror ONE daily blog posting-packet into a Plane card.

WHY THIS EXISTS
  The 05:00 packet email delivers the words to Ezekiel. It cannot show whether the
  work got done: "reply with the URLs" depends on a reply, and a missing reply is
  indistinguishable from a missing post. A Plane card has a STATE, so "posted" is a
  fact on a board instead of a report in an inbox.

  Split: the email is the delivery, the card is the record. The card carries the
  post title, the canonical URL, and the syndication links, so Ezekiel can work the
  post from Plane alone and drag it To Do -> Done as he posts it.

IDEMPOTENCE
  Each card is stamped external_source=blog-packet and external_id=blog-<slug>.
  Re-running matches on that pair and updates rather than duplicating, so a second
  packet run for the same post never makes a second card.

FAIL-SOFT BY DESIGN
  This runs AFTER the email has already been sent. Plane being down must never cost
  Ezekiel his packet, so every failure path exits 0 with a logged warning. The email
  is the guarantee; the card is the upgrade.

Usage:
  blog-plane-card.py --slug S --title T --url U [--link "Label=https://..."]... [--dry-run]
"""
from __future__ import annotations
import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HOST = os.environ.get("PLANE_API_HOST_URL", "https://projects.intentsolutions.io")
SLUG = os.environ.get("PLANE_WORKSPACE_SLUG", "internal")
# CONTENT project + its "To Do" state — the same board the omarchy showcase used.
CONTENT_PROJECT = "b421236a-7a50-4e4b-b01f-6dd3a4cdfaf9"
TODO_STATE = "982586a3-370d-4899-b3f4-ce74bb4d25e3"
OPERATOR_EMAIL = "ezekiel@intentsolutions.io"
EXT_SOURCE = "blog-packet"


def api_key() -> str:
    k = os.environ.get("PLANE_API_KEY")
    if k:
        return k
    try:
        raw = Path("/home/jeremy/.claude.json").read_text()
        m = re.search(r'"PLANE_API_KEY"\s*:\s*"([^"]+)"', raw)
        if m:
            return m.group(1)
    except OSError:
        pass
    return ""


def call(key: str, method: str, path: str, body=None):
    req = urllib.request.Request(
        f"{HOST}/api/v1/workspaces/{SLUG}{path}",
        method=method,
        headers={"X-API-Key": key, "Content-Type": "application/json"},
        data=json.dumps(body).encode() if body is not None else None,
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read()
        return r.status, (json.loads(raw) if raw else None)


def find_operator(key: str):
    """Ezekiel's member uuid, or None while his invite is still pending."""
    try:
        _, members = call(key, "GET", "/members/")
    except Exception:
        return None
    rows = members.get("results", members) if isinstance(members, dict) else members
    for m in rows or []:
        if (m.get("email") or "").lower() == OPERATOR_EMAIL:
            return m.get("id")
    return None


def ensure_project_member(key: str, uid: str) -> bool:
    """Plane silently drops an assignee who is not a member of the PROJECT (not
    just the workspace). Ezekiel was a workspace member but never added to
    CONTENT, so every assign returned 200 and assigned nobody — the board looked
    empty and nothing flagged it (found 2026-08-29). Idempotently add him so the
    assignment below can actually stick. Returns True if he is (now) a member."""
    def member_id(r):
        m = r.get("member")
        if isinstance(m, dict):
            return m.get("id")
        return m or r.get("id")
    try:
        _, page = call(key, "GET", f"/projects/{CONTENT_PROJECT}/members/")
        rows = page.get("results", page) if isinstance(page, dict) else page
        if uid in [member_id(r) for r in (rows or [])]:
            return True
        st, _ = call(key, "POST", f"/projects/{CONTENT_PROJECT}/members/",
                    {"member": uid, "role": 15})
        # 200/201 = added; 400 typically means "already a member", also fine.
        return st in (200, 201, 400)
    except Exception:
        return False


def esc(s: str) -> str:
    return html.escape(s or "")


def card_html(title: str, url: str, links: list[tuple[str, str]]) -> str:
    p = [
        f"<p>Post is live: <a href=\"{esc(url)}\">{esc(url)}</a></p>",
        "<p>The full copy for each platform is in today's posting-packet email. "
        "Post it, then drag this card to <b>Done</b>.</p>",
    ]
    if links:
        p.append("<p><b>Links</b></p><ul>")
        for label, href in links:
            p.append(f"<li>{esc(label)}: <a href=\"{esc(href)}\">{esc(href)}</a></li>")
        p.append("</ul>")
    return "".join(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--url", default="")
    ap.add_argument("--link", action="append", default=[], help='"Label=https://..."')
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    links: list[tuple[str, str]] = []
    for item in a.link:
        if "=" in item:
            label, href = item.split("=", 1)
            links.append((label.strip(), href.strip()))

    key = api_key()
    if not key:
        print("PLANE-CARD: no PLANE_API_KEY (env or ~/.claude.json) — skipping, email already sent")
        return 0

    ext_id = f"blog-{a.slug}"
    name = f"Post: {a.title}"

    if a.dry_run:
        print(f"PLANE-CARD DRY-RUN: would upsert '{name}' (external_id={ext_id}) "
              f"in CONTENT, assign {OPERATOR_EMAIL}")
        return 0

    try:
        operator = find_operator(key)
        # find an existing card for this post so re-runs update, not duplicate
        _, page = call(key, "GET", f"/projects/{CONTENT_PROJECT}/issues/?per_page=100")
        rows = page.get("results", []) if isinstance(page, dict) else (page or [])
        existing = next((r for r in rows
                         if r.get("external_source") == EXT_SOURCE
                         and r.get("external_id") == ext_id), None)

        payload = {
            "name": name,
            "description_html": card_html(a.title, a.url, links),
            "state": TODO_STATE,
            "external_source": EXT_SOURCE,
            "external_id": ext_id,
        }

        if existing:
            issue_id = existing["id"]
            st, _ = call(key, "PATCH", f"/projects/{CONTENT_PROJECT}/issues/{issue_id}/", payload)
            verb = "updated"
        else:
            st, created = call(key, "POST", f"/projects/{CONTENT_PROJECT}/issues/", payload)
            issue_id = (created or {}).get("id")
            verb = "created"

        # Assignees must be set in their OWN PATCH: Plane's issue endpoint ignores
        # an `assignees` field mixed into a create/update payload. And the assignee
        # must be a PROJECT member first, or the PATCH returns 200 and assigns
        # nobody. Both are handled here.
        note = ""
        if operator and issue_id:
            if ensure_project_member(key, operator):
                call(key, "PATCH", f"/projects/{CONTENT_PROJECT}/issues/{issue_id}/",
                     {"assignees": [operator]})
            else:
                note = " — could not add Ezekiel to the CONTENT project; left unassigned"
        elif not operator:
            note = " — Ezekiel invite still pending, unassigned"
        print(f"PLANE-CARD: {verb} card for {a.slug} (HTTP {st}){note}")
        return 0
    except urllib.error.HTTPError as e:
        print(f"PLANE-CARD: Plane API HTTP {e.code} — skipping, email already sent")
        return 0
    except Exception as e:
        print(f"PLANE-CARD: {type(e).__name__}: {e} — skipping, email already sent")
        return 0


if __name__ == "__main__":
    sys.exit(main())
