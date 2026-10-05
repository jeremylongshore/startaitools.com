"""Bounded search phrasing: validate the staged output, record it, never gate.

Blog Recovery Phase I, E03 (startaitools.com#123, governing contract intent-os
000-docs/228). The daily run may carry ONE optional, recorded step: search
phrasing evidence for the title of a post whose subject is already fixed by the
day's recorded finding. The research half (an LLM step run from a scratch
directory with a narrow brief) only PRODUCES a staged JSON file:

    .blog-staging/DATE.RUNID.search-phrasing.json

This module is the deterministic consumer. It turns that file, or its absence,
into the `agent_audit.search_phrasing` record. Three rules hold:

1. **The topic is immutable.** The staged `finding_sentence` must equal the
   recorded `agent_audit.finding.sentence`; every `named_terms` entry must occur in
   the finding itself; every kept candidate and the recommended title form must
   contain a named term. Unknown top-level keys (a `topic`, a `slug`) are refused.
   Search may shape how a real finding is phrased, never what the post is about.
2. **Evidence carries its source and its uncertainty.** A candidate without an
   http(s) `evidence_url` is dropped; a non-skipped output without an
   `uncertainty` statement is refused.
3. **It never blocks the writer.** Missing output, a timeout, an invalid document
   or zero usable candidates all become a skip record with a reason, and the CLI
   exits 0. Only a usage error exits non-zero.

The step is OFF unless the run sets BLOG_SEARCH_PHRASING=1 (see the blog-backfill
polish reference). Rollback: unset it; nothing else reads this record.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA = "search-phrasing/v1"
ENABLE_ENV = "BLOG_SEARCH_PHRASING"
MAX_WEB_CALLS = 6  # 226c §5: 3-6 searches per day
SKIP_REASONS = (
    "disabled",  # BLOG_SEARCH_PHRASING not set
    "timeout",  # the research step ran out of its time budget
    "no_web",  # web search unavailable
    "no_named_term",  # the finding names no tool, error or component to search for
    "no_result",  # searches ran, nothing usable survived validation
    "missing_output",  # no staged file (the producer never wrote one)
    "invalid_output",  # unreadable or malformed staged file
    "topic_drift",  # the output tried to change or widen the subject
    "no_finding",  # no recorded finding to bind the phrasing to
)
CONFIDENCE = ("observed", "inferred")
ALLOWED_KEYS = {
    "schema",
    "date",
    "finding_sentence",
    "named_terms",
    "candidates",
    "recommended_title_form",
    "saturation_note",
    "uncertainty",
    "skipped_reason",
    "web_calls",
}
CANDIDATE_KEYS = {"phrase", "evidence", "evidence_url", "contains_named_term", "confidence"}
_DASH = re.compile(r"[‒–—―]| - ")
_YEAR = re.compile(r"\b(19|20)\d{2}\b")
_URL = re.compile(r"^https?://\S+$")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _norm(value: str) -> str:
    return " ".join(value.lower().split())


def finding_text(finding: dict[str, Any]) -> str:
    """Everything the recorded finding says; named terms must come from here."""
    parts = [finding.get(k) for k in ("sentence", "reader", "problem", "outcome")]
    parts += list(finding.get("source_evidence") or [])
    return _norm(" ".join(p for p in parts if isinstance(p, str)))


def _has_term(text: str, terms: list[str]) -> bool:
    low = _norm(text)
    return any(_norm(t) in low for t in terms)


def skip(reason: str, detail: str | None = None) -> dict[str, Any]:
    assert reason in SKIP_REASONS, reason
    return {
        "ran": False,
        "skipped_reason": reason,
        "detail": detail,
        "candidates": 0,
        "dropped": 0,
        "recommended_title_form": None,
        "evidence_urls": [],
        "uncertainty": None,
        "web_calls": 0,
        "used": False,
    }


def _candidate_problem(c: Any, terms: list[str]) -> str | None:
    if not isinstance(c, dict) or set(c) - CANDIDATE_KEYS:
        return "malformed candidate"
    if not _text(c.get("phrase")) or not _text(c.get("evidence")):
        return "missing phrase or evidence"
    if not isinstance(c.get("evidence_url"), str) or not _URL.match(c["evidence_url"]):
        return "no source url"
    if c.get("confidence") not in CONFIDENCE:
        return "confidence must be observed|inferred"
    if not _has_term(c["phrase"], terms):
        return "names no term from the finding"
    if _DASH.search(c["phrase"]) or _YEAR.search(c["phrase"]):
        return "dash or year in phrase"
    return None


def evaluate(doc: Any, finding: dict[str, Any] | None, final_title: str | None = None) -> dict:
    """The `agent_audit.search_phrasing` record for one staged document. Never raises."""
    if not isinstance(finding, dict) or not _text(finding.get("sentence")):
        return skip("no_finding")
    if not isinstance(doc, dict):
        return skip("invalid_output", "staged document is not a JSON object")
    extra = sorted(set(doc) - ALLOWED_KEYS)
    if extra:
        return skip("topic_drift", f"unexpected keys: {', '.join(extra)}")
    if doc.get("schema") != SCHEMA:
        return skip("invalid_output", f"schema must be {SCHEMA}")
    if not isinstance(doc.get("finding_sentence"), str) or _norm(doc["finding_sentence"]) != _norm(
        finding["sentence"]
    ):
        return skip("topic_drift", "finding_sentence differs from the recorded finding")
    reason = doc.get("skipped_reason")
    if reason is not None:
        if reason not in SKIP_REASONS:
            return skip("invalid_output", f"unknown skipped_reason {reason!r}")
        return skip(reason, "recorded by the research step")

    calls = doc.get("web_calls")
    if type(calls) is not int or calls < 0:
        return skip("invalid_output", "web_calls must be a non-negative integer")
    if calls > MAX_WEB_CALLS:
        return skip("invalid_output", f"{calls} web calls exceeds the budget of {MAX_WEB_CALLS}")
    if not _text(doc.get("uncertainty")):
        return skip("invalid_output", "uncertainty statement is required")
    terms = doc.get("named_terms")
    if not isinstance(terms, list) or not terms or not all(_text(t) for t in terms):
        return skip("no_named_term")
    source = finding_text(finding)
    foreign = [t for t in terms if _norm(t) not in source]
    if foreign:
        return skip("topic_drift", f"named terms not in the finding: {', '.join(foreign)}")
    raw = doc.get("candidates")
    if not isinstance(raw, list):
        return skip("invalid_output", "candidates must be a list")

    kept = [c for c in raw if _candidate_problem(c, terms) is None]
    if not kept:
        return skip("no_result", f"0 of {len(raw)} candidates survived validation")
    title = doc.get("recommended_title_form")
    if title is not None and (
        not _text(title)
        or not _has_term(title, terms)
        or _DASH.search(title)
        or _YEAR.search(title)
    ):
        title = None  # a bad recommendation is dropped, the evidence is kept
    used = bool(title and final_title and _norm(title) == _norm(final_title))
    return {
        "ran": True,
        "skipped_reason": None,
        "detail": None,
        "candidates": len(kept),
        "dropped": len(raw) - len(kept),
        "recommended_title_form": title,
        "evidence_urls": sorted({c["evidence_url"] for c in kept}),
        "uncertainty": doc["uncertainty"].strip(),
        "web_calls": calls,
        "used": used,
    }


def enabled() -> bool:
    return os.environ.get(ENABLE_ENV) == "1"


def consume(
    staging: Path, finding: dict | None, final_title: str | None = None, on: bool = True
) -> dict:
    """Read the staged file and evaluate it. With the step off and no file, say so."""
    if not staging.exists():
        return skip("missing_output" if on else "disabled", staging.name)
    try:
        doc = json.loads(staging.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return skip("invalid_output", f"{type(exc).__name__}: {exc}"[:200])
    return evaluate(doc, finding, final_title)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -B -m blogpipe search-phrasing",
        description="Print the agent_audit.search_phrasing record. Exits 0 on every "
        "content outcome, including skips; the writer always proceeds.",
    )
    ap.add_argument("--staging", required=True, help="DATE.RUNID.search-phrasing.json")
    ap.add_argument("--finding", required=True, help="JSON file holding agent_audit.finding")
    ap.add_argument("--final-title", help="the title the post shipped with (sets `used`)")
    args = ap.parse_args(argv)
    try:
        finding = json.loads(Path(args.finding).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        finding = None
    record = consume(Path(args.staging), finding, args.final_title, enabled())
    json.dump(record, sys.stdout, ensure_ascii=False, sort_keys=True)
    sys.stdout.write("\n")
    if not record["ran"]:
        print(f"SEARCH-PHRASING: SKIP: {record['skipped_reason']}", file=sys.stderr)
    return 0
