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

A date never passes a gate on its own. Two operator levers and one alarm:

- `BLOG_BRIEF_ENFORCE_FROM=YYYY-MM-DD` moves the switch, `=off` disables it, without
  a code change. Set it in the cron environment of blog-backfill-daily.sh (the
  producer's contract commands inherit it). Any other value refuses loudly.
- `readiness()` (CLI: `python3 -B -m blogpipe contract-readiness`, which also covers
  the record-schema switch in blogpipe/schema.py) runs in the daily wrapper. From
  three days before the switch it adds "brief enforcement in N days: ..." to the
  summary email; at or after the switch with fewer than seven
  consecutive complete runs (within seven days of it) it raises an URGENT alert to
  #cron-failures from the parent production run only (never a canary or a quiet
  failover/catch-up child). It does not quietly disable enforcement: the operator
  decides with the env lever.

The mechanism itself lives in blogpipe/switch.py (shared with the E07-T03 record-schema
contract); this module owns only its date, its lever and its gap list.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# READINESS_* are re-exported for callers that read them from here.
from .switch import (  # noqa: F401
    READINESS_LEAD_DAYS,
    READINESS_WINDOW,
    DatedSwitch,
    readiness_main,
)

# Proposed: first run date after seven consecutive daily runs (2026-10-07..13) can
# carry the fields, assuming the instruction change is live by 2026-10-06.
AMENDED_CONTRACT_ENFORCE_FROM = "2026-10-14"

T1_CONSISTENCY_AGENT = "blog-consistency-checker"
FINDING_TEXT_FIELDS = ("sentence", "reader", "problem", "outcome")
OUTSIDER_VERDICTS = ("PASS", "REVISE")


ENFORCE_ENV = "BLOG_BRIEF_ENFORCE_FROM"
# The mechanism is shared (blogpipe/switch.py); this module owns only its date, lever
# and wording. The lambda reads the constant at call time so tests can monkeypatch it.
SWITCH = DatedSwitch(
    name="brief",
    label="amended contract",
    env=ENFORCE_ENV,
    default=lambda: AMENDED_CONTRACT_ENFORCE_FROM,
)
LINE = SWITCH.line


def enforcement_date() -> str | None:
    """The effective switch date: env override, else the constant. None means off."""
    return SWITCH.enforcement_date()


def enforced(date: str) -> bool:
    return SWITCH.enforced(date)


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
    """Presence and shape only: a recorded REVISE is complete, never a failure.

    Each malformed field is named on its own. The 2026-10-09 run recorded
    `unknown_terms` as `{"term", "gloss"}` objects; the one catch-all wording read as
    "missing" to the producer, which had written the record and moved on.
    """
    record = audit.get("outsider_test")
    if not isinstance(record, dict):
        return ["agent_audit.outsider_test"]
    gaps = []
    if record.get("verdict") not in OUTSIDER_VERDICTS:
        gaps.append("agent_audit.outsider_test.verdict (PASS or REVISE)")
    rounds = record.get("rounds")
    if type(rounds) is not int or not 1 <= rounds <= 3:
        gaps.append("agent_audit.outsider_test.rounds (integer 1-3)")
    terms = record.get("unknown_terms")
    if not isinstance(terms, list):
        gaps.append("agent_audit.outsider_test.unknown_terms (a list)")
    elif any(not isinstance(term, str) for term in terms):
        gaps.append(
            "agent_audit.outsider_test.unknown_terms (plain strings only, "
            "found a non-string entry; put glosses in notes)"
        )
    return gaps


def brief_gaps(audit: dict[str, Any]) -> list[str]:
    return finding_gaps(audit) + outsider_gaps(audit)


def report(date: str, gaps: list[str]) -> None:
    """One stable line per validation; blog-backfill-daily.sh lifts it into the summary."""
    SWITCH.report(date, gaps)


def run_history(log_dir: Path, date: str) -> list[tuple[str, bool | None]]:
    return SWITCH.run_history(log_dir, date)


def readiness(log_dir: Path, date: str) -> tuple[str | None, bool]:
    """(summary text or None, urgent?) for the run of `date`."""
    return SWITCH.readiness(log_dir, date)


def main() -> int:
    return readiness_main([SWITCH], "Amended reader contract readiness")
