"""Publication evidence: what a URL receipt proves, kept apart from what we believe.

Three different facts used to share one field, and the ledger could not tell them apart:

* the posting packet was DELIVERED (SMTP accepted an email to the poster),
* a surface is BELIEVED posted (`assumed_posted`, aged in by syndication-reconcile.py
  from an owner standing instruction), and
* a surface is PROVEN posted (someone handed us the URL of the live post).

`packet_sent` answers the first and nothing else. The legacy `syndication.<surface>.status`
holds the second. This module owns the third: an append-only list of observations per
surface under `row["publication_evidence"]`, written ONLY from a URL receipt. It never
rewrites a historical row's status and never turns a belief into a receipt: an
`assumed_posted` row that later gets a URL keeps its status and gains an observation
beside it, so the history of what we believed and when stays readable.

Status vocabularies, deliberately disjoint so one can never be read as another:

PACKET_STATUSES (row["packet_status"], what the delivered email told the poster to do)
    sent        a distribution packet was delivered
    held        a HOLD ("do not post yet") packet was delivered; nothing should be live

EVIDENCE_STATUSES (derived per surface by publication_status())
    posted      at least one URL receipt exists for this surface
    not_posted  the owner explicitly reported it was not posted
    unknown     no receipt. Includes every `pending` and `assumed_posted` row: a belief
                is not evidence in either direction
    n/a         the surface does not apply to this post's tier

MEASUREMENT_STATUSES (what an analytics corroboration attempt can honestly say)
    verified        attributable tagged arrivals exist for this post
    verified_zero   the query succeeded and found zero tagged arrivals
    unverified      tagged traffic exists but cannot be attributed to this post
    unavailable     the analytics query failed, was disabled, or had no credentials
    uninstrumented  the surface carried no tagged link, so zero is not a measurement
"""

from __future__ import annotations

import datetime as dt
import re
from urllib.parse import urlsplit

from .errors import PublicationError

PACKET_STATUSES = ("sent", "held")
EVIDENCE_STATUSES = ("posted", "not_posted", "unknown", "n/a")
MEASUREMENT_STATUSES = ("verified", "verified_zero", "unverified", "unavailable", "uninstrumented")
EVIDENCE_SOURCES = ("reply", "paste", "api")

# Every surface the packet distributes to. The ledger's legacy `syndication` block only
# ever carried the first five; the X article and Buy Me a Coffee have evidence rows only.
SURFACES = ("x", "x_article", "li_personal", "li_company", "substack", "medium", "buymeacoffee")
LEGACY_SURFACES = ("x", "li_personal", "li_company", "substack", "medium")

# A receipt must point at the platform it claims. Without this an "X:" line carrying the
# startaitools canonical (the link the poster was asked to share) recorded the BLOG as
# the X post. Substack is limited to *.substack.com; a custom domain is refused rather
# than guessed, and is a config change, not a parser change.
SURFACE_HOSTS = {
    "x": (r"(www\.)?(x|twitter)\.com",),
    "x_article": (r"(www\.)?(x|twitter)\.com",),
    "li_personal": (r"([\w-]+\.)?linkedin\.com", r"lnkd\.in"),
    "li_company": (r"([\w-]+\.)?linkedin\.com", r"lnkd\.in"),
    "substack": (r"[\w-]+\.substack\.com",),
    "medium": (r"([\w-]+\.)?medium\.com",),
    "buymeacoffee": (r"(www\.)?buymeacoffee\.com",),
}


def receipt_url_ok(surface: str, url: str) -> bool:
    """True when `url` is an https/http link on the platform `surface` names."""
    if surface not in SURFACE_HOSTS or not isinstance(url, str):
        return False
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https") or not parts.hostname or not parts.path.strip("/"):
        return False
    return any(re.fullmatch(pattern, parts.hostname, re.I) for pattern in SURFACE_HOSTS[surface])


def _iso(value: str) -> str:
    moment = dt.datetime.fromisoformat(value)
    if moment.tzinfo is None:
        raise PublicationError("evidence timestamps must carry a UTC offset")
    return moment.isoformat()


def record_observation(
    row: dict,
    surface: str,
    url: str,
    *,
    source: str,
    observed_at: str,
    evidence_ref: str,
    recorded_at: str,
) -> str:
    """Append one URL receipt to `row`. Returns "recorded", "duplicate" or "upgraded".

    "upgraded" means the legacy status was `pending` (no belief recorded yet) and now
    reads `posted` with the receipt's URL. Any other legacy status is left exactly as it
    was: `assumed_posted` stays a belief with its provenance, `not_posted` stays the
    owner's report (a contradicting receipt sits beside it for a human to resolve), and
    `n/a` stays the tier's verdict.
    """
    if surface not in SURFACES:
        raise PublicationError(f"unknown publication surface: {surface}")
    if source not in EVIDENCE_SOURCES:
        raise PublicationError(f"unknown evidence source: {source}")
    if not receipt_url_ok(surface, url):
        raise PublicationError(f"receipt URL is not a {surface} post URL")
    if not isinstance(evidence_ref, str) or not evidence_ref.strip():
        raise PublicationError("a receipt must name the evidence it came from")
    observation = {
        "status": "posted",
        "url": url,
        "source": source,
        "observed_at": _iso(observed_at),
        "recorded_at": _iso(recorded_at),
        "evidence_ref": evidence_ref,
    }
    evidence = row.setdefault("publication_evidence", {})
    if not isinstance(evidence, dict):
        raise PublicationError("publication_evidence must be an object")
    observations = evidence.setdefault(surface, [])
    if any(item.get("url") == url for item in observations):
        return "duplicate"
    observations.append(observation)

    legacy = (row.get("syndication") or {}).get(surface)
    if isinstance(legacy, dict) and legacy.get("status") == "pending":
        legacy.update(
            status="posted",
            url=url,
            posted_at=observation["observed_at"],
            by=source,
            evidence_ref=evidence_ref,
        )
        return "upgraded"
    return "recorded"


def publication_status(row: dict, surface: str) -> str:
    """The evidence verdict for one surface (see EVIDENCE_STATUSES)."""
    if (row.get("publication_evidence") or {}).get(surface):
        return "posted"
    legacy = (row.get("syndication") or {}).get(surface) or {}
    status = legacy.get("status")
    # A legacy `posted` written before this module existed counts only if it carries the
    # URL it claims; a bare "posted" with no URL is exactly the unbacked claim this
    # vocabulary exists to stop.
    if status == "posted" and isinstance(legacy.get("url"), str) and legacy["url"]:
        return "posted"
    if status in ("not_posted", "n/a"):
        return status
    return "unknown"


def has_receipt(row: dict) -> bool:
    return any(publication_status(row, surface) == "posted" for surface in SURFACES)


def is_held(row: dict) -> bool:
    return row.get("packet_status") == "held"


def guard_status_patch(row: dict, patch: dict) -> None:
    """Refuse a generic row patch that would claim `posted` without a receipt.

    The publication CLI's `update --patch-json` is a general-purpose merge, so it could
    set `posted` with no URL, or overwrite an `assumed_posted` belief with a receipt
    nobody holds. A receipt goes through record_observation, which needs a URL on the
    right platform and names its evidence.
    """
    syndication = patch.get("syndication") if isinstance(patch, dict) else None
    if not isinstance(syndication, dict):
        return
    current = row.get("syndication") or {}
    for surface, slot in syndication.items():
        if not isinstance(slot, dict) or slot.get("status") != "posted":
            continue
        before = (current.get(surface) or {}).get("status")
        if before not in (None, "pending", "posted"):
            raise PublicationError(
                f"{surface}: a {before} row cannot be patched to posted; "
                "append publication evidence instead"
            )
        url = slot.get("url") or (current.get(surface) or {}).get("url")
        if not receipt_url_ok(surface, url or ""):
            raise PublicationError(f"{surface}: posted requires a {surface} post URL")
