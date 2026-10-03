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
- `readiness()` (CLI: `python3 -B -m blogpipe brief-readiness`) runs in the daily
  wrapper. From three days before the switch it adds "brief enforcement in N days:
  ..." to the summary email; at or after the switch with fewer than seven
  consecutive complete runs it raises an URGENT alert to #cron-failures. It does
  not quietly disable enforcement: the operator decides with the env lever.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from typing import Any

from .errors import ContractError

# Proposed: first run date after seven consecutive daily runs (2026-10-07..13) can
# carry the fields, assuming the instruction change is live by 2026-10-06.
AMENDED_CONTRACT_ENFORCE_FROM = "2026-10-14"

T1_CONSISTENCY_AGENT = "blog-consistency-checker"
FINDING_TEXT_FIELDS = ("sentence", "reader", "problem", "outcome")
OUTSIDER_VERDICTS = ("PASS", "REVISE")


ENFORCE_ENV = "BLOG_BRIEF_ENFORCE_FROM"
READINESS_WINDOW = 7
READINESS_LEAD_DAYS = 3
LINE = re.compile(r"ADVISORY: amended contract \((?P<mode>[^)]*)\): (?P<status>.*)$")


def enforcement_date() -> str | None:
    """The effective switch date: env override, else the constant. None means off."""
    value = os.environ.get(ENFORCE_ENV, "").strip()
    if not value:
        return AMENDED_CONTRACT_ENFORCE_FROM
    if value == "off":
        return None
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        raise ContractError(f"{ENFORCE_ENV} must be YYYY-MM-DD or 'off', got {value!r}") from None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ContractError(f"{ENFORCE_ENV} must be YYYY-MM-DD or 'off', got {value!r}")
    return value


def enforced(date: str) -> bool:
    switch = enforcement_date()
    return switch is not None and date >= switch


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
    switch = enforcement_date()
    if switch is None:
        mode = f"observation, enforcement off via {ENFORCE_ENV}"
    else:
        mode = "enforced" if enforced(date) else f"observation until {switch}"
    status = "complete" if not gaps else "missing " + ", ".join(gaps)
    print(f"PRODUCER-CONTRACT: ADVISORY: amended contract ({mode}): {status}", file=sys.stderr)


def run_history(log_dir: Path, date: str) -> list[tuple[str, bool | None]]:
    """(run date, complete?) for each daily log up to `date`, newest first.

    Reads the last amended-contract line of `run-YYYY-MM-DD.log`; None when a run
    logged no line at all (the producer never reached verification), which breaks
    a streak exactly like an incomplete run.
    """
    history = []
    for path in log_dir.glob("run-????-??-??.log"):
        day = path.stem[4:]
        if day > date:
            continue
        status = None
        try:
            lines = path.read_text(errors="replace").splitlines()
        except OSError:
            lines = []
        for line in lines:
            match = LINE.search(line)
            if match:
                status = match.group("status").strip() == "complete"
        history.append((day, status))
    return sorted(history, reverse=True)


def readiness(log_dir: Path, date: str) -> tuple[str | None, bool]:
    """(summary text or None, urgent?) for the run of `date`."""
    switch = enforcement_date()
    if switch is None:
        return f"brief enforcement off ({ENFORCE_ENV}=off)", False
    days = (dt.date.fromisoformat(switch) - dt.date.fromisoformat(date)).days
    if days > READINESS_LEAD_DAYS:
        return None, False
    recent = run_history(log_dir, date)[:READINESS_WINDOW]
    streak = 0
    for _, complete in recent:
        if complete is not True:
            break
        streak += 1
    complete_runs = sum(1 for _, complete in recent if complete is True)
    tally = (
        f"last {len(recent)} runs: {complete_runs} complete, "
        f"{len(recent) - complete_runs} incomplete; consecutive complete {streak}/"
        f"{READINESS_WINDOW}"
    )
    if days > 0:
        return f"brief enforcement in {days} day(s) (run date {switch}): {tally}", False
    if streak >= READINESS_WINDOW:
        return f"brief enforcement active since {switch}: {tally}", False
    return (
        f"URGENT: brief enforcement active since {switch} with only {streak}/"
        f"{READINESS_WINDOW} consecutive complete runs ({tally}). Incomplete runs are "
        f"now refused. To pause, set {ENFORCE_ENV} to a later date or 'off'.",
        True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Amended reader contract readiness")
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    try:
        message, urgent = readiness(args.log_dir, args.date)
    except (ContractError, ValueError) as exc:
        print(f"URGENT: brief readiness check failed: {exc}")
        return 2
    if message:
        print(message)
    return 2 if urgent else 0
