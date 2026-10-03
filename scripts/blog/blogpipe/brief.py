"""The amended reader contract: minimal brief, outsider record, Tier 1 consistency.

Blog Recovery Phase I, E01-T02/T03 (startaitools.com#121, governing contract
intent-os 000-docs/228 S05). Three additions to what a run must carry:

1. `agent_audit.finding`: the minimal reader brief chosen at SKILL step 1b,
   `{sentence, reader, problem, outcome, source_evidence[], destination}`.
   `destination` may be null only with a non-empty `destination_reason`.
2. `agent_audit.outsider_test`: the step 4b result. Its verdict never blocks
   (REVISE is an honest outcome); its PRESENCE is what becomes required.
3. Tier 1 runs dispatch `blog-consistency-checker` on the final bytes.

OBSERVATION MODE (E01-T05): for run dates before AMENDED_CONTRACT_ENFORCE_FROM a gap
is reported as a `PRODUCER-CONTRACT: ADVISORY:` line (and lifted into the daily
summary email), never a refusal. On and after that date the same gaps refuse.
The switch is keyed on the run's target DATE, not the wall clock, so fixtures and
historical replays stay deterministic and a backfill of an older date keeps the
contract it was written under. Moving the date is the rollback.

A date never passes a gate on its own: before the flip, confirm seven consecutive
daily audits carry the brief and the outsider record (the summary line reports
each run). If they do not, move this constant rather than letting it fire.
"""

from __future__ import annotations

import sys
from typing import Any

# Proposed: first run date after seven consecutive daily runs (2026-10-07..13) can
# carry the fields, assuming the instruction change is live by 2026-10-06.
AMENDED_CONTRACT_ENFORCE_FROM = "2026-10-14"

T1_CONSISTENCY_AGENT = "blog-consistency-checker"
FINDING_TEXT_FIELDS = ("sentence", "reader", "problem", "outcome")
OUTSIDER_VERDICTS = ("PASS", "REVISE")


def enforced(date: str) -> bool:
    return date >= AMENDED_CONTRACT_ENFORCE_FROM


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def finding_gaps(audit: dict[str, Any]) -> list[str]:
    """Name every missing or malformed brief field; empty means complete."""
    finding = audit.get("finding")
    if not isinstance(finding, dict):
        return ["agent_audit.finding"]
    gaps = [
        f"agent_audit.finding.{key}" for key in FINDING_TEXT_FIELDS if not _text(finding.get(key))
    ]
    evidence = finding.get("source_evidence")
    if not isinstance(evidence, list) or not evidence or any(not _text(item) for item in evidence):
        gaps.append("agent_audit.finding.source_evidence")
    if "destination" not in finding:
        gaps.append("agent_audit.finding.destination")
    elif finding["destination"] is None:
        if not _text(finding.get("destination_reason")):
            gaps.append("agent_audit.finding.destination_reason (destination is null)")
    elif not _text(finding["destination"]):
        gaps.append("agent_audit.finding.destination")
    return gaps


def outsider_gaps(audit: dict[str, Any]) -> list[str]:
    """Presence and shape only: a recorded REVISE is complete, never a failure."""
    record = audit.get("outsider_test")
    if not isinstance(record, dict):
        return ["agent_audit.outsider_test"]
    rounds = record.get("rounds")
    terms = record.get("unknown_terms")
    if (
        record.get("verdict") not in OUTSIDER_VERDICTS
        or type(rounds) is not int
        or not 1 <= rounds <= 3
        or not isinstance(terms, list)
        or any(not isinstance(term, str) for term in terms)
    ):
        return ["agent_audit.outsider_test (verdict PASS|REVISE, rounds 1-3, unknown_terms[])"]
    return []


def brief_gaps(audit: dict[str, Any]) -> list[str]:
    return finding_gaps(audit) + outsider_gaps(audit)


def report(date: str, gaps: list[str]) -> None:
    """One stable line per validation; blog-backfill-daily.sh lifts it into the summary."""
    mode = "enforced" if enforced(date) else f"observation until {AMENDED_CONTRACT_ENFORCE_FROM}"
    status = "complete" if not gaps else "missing " + ", ".join(gaps)
    print(f"PRODUCER-CONTRACT: ADVISORY: amended contract ({mode}): {status}", file=sys.stderr)
