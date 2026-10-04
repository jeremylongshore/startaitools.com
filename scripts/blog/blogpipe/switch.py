"""The dated observation-to-enforcement switch every amended producer contract uses.

Introduced by the amended reader contract (blogpipe/brief.py, E01-T02/T03, #138) and
lifted here unchanged so a second contract (blogpipe/schema.py, E07-T03) reuses the same
mechanism instead of growing its own. Behaviour, per switch:

- Keyed on the run's target DATE, never the wall clock: fixtures and historical replays
  stay deterministic, and a backfill of an older date keeps the contract it was written
  under. Moving the date is the rollback.
- Before the date a gap is one `PRODUCER-CONTRACT: ADVISORY: <label> (<mode>): <status>`
  line on stderr (the daily wrapper lifts the last one into its summary email). On and
  after it the same gap refuses.
- `<ENV>=YYYY-MM-DD` moves the switch and `<ENV>=off` disables it, without a code change.
  Any other value refuses loudly.
- `readiness()` is silent until READINESS_LEAD_DAYS before the switch, then counts down
  in the summary email; within READINESS_WINDOW days after it, fewer than seven
  consecutive complete runs is URGENT. It never disables enforcement on its own: the
  operator decides with the env lever.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .errors import ContractError

READINESS_WINDOW = 7
READINESS_LEAD_DAYS = 3


@dataclass(frozen=True)
class DatedSwitch:
    name: str  # readiness wording: "<name> enforcement in N day(s) ..."
    label: str  # advisory wording: "ADVISORY: <label> (<mode>): <status>"
    env: str  # operator lever
    default: Callable[[], str]  # read at call time, so the module constant stays patchable

    @property
    def line(self) -> re.Pattern[str]:
        return re.compile(
            rf"ADVISORY: {re.escape(self.label)} \((?P<mode>[^)]*)\): (?P<status>.*)$"
        )

    def enforcement_date(self) -> str | None:
        """The effective switch date: env override, else the constant. None means off."""
        value = os.environ.get(self.env, "").strip()
        if not value:
            return self.default()
        if value == "off":
            return None
        problem = f"{self.env} must be YYYY-MM-DD or 'off', got {value!r}"
        try:
            dt.date.fromisoformat(value)
        except ValueError:
            raise ContractError(problem) from None
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ContractError(problem)
        return value

    def enforced(self, date: str) -> bool:
        switch = self.enforcement_date()
        return switch is not None and date >= switch

    def report(self, date: str, gaps: list[str]) -> None:
        """One stable line per validation; blog-backfill-daily.sh lifts it into the summary."""
        switch = self.enforcement_date()
        if switch is None:
            mode = f"observation, enforcement off via {self.env}"
        else:
            mode = "enforced" if self.enforced(date) else f"observation until {switch}"
        status = "complete" if not gaps else "missing " + ", ".join(gaps)
        print(f"PRODUCER-CONTRACT: ADVISORY: {self.label} ({mode}): {status}", file=sys.stderr)

    def run_history(self, log_dir: Path, date: str) -> list[tuple[str, bool | None]]:
        """(run date, complete?) for each daily log up to `date`, newest first.

        Reads the last advisory line of this switch in `run-YYYY-MM-DD.log`; None when a
        run logged no line at all (the producer never reached verification), which breaks
        a streak exactly like an incomplete run.
        """
        line = self.line
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
            for text in lines:
                match = line.search(text)
                if match:
                    status = match.group("status").strip() == "complete"
            history.append((day, status))
        return sorted(history, reverse=True)

    def readiness(self, log_dir: Path, date: str) -> tuple[str | None, bool]:
        """(summary text or None, urgent?) for the run of `date`."""
        switch = self.enforcement_date()
        if switch is None:
            return f"{self.name} enforcement off ({self.env}=off)", False
        days = (dt.date.fromisoformat(switch) - dt.date.fromisoformat(date)).days
        # The alarm covers the transition only: from READINESS_LEAD_DAYS before the switch
        # to READINESS_WINDOW days after it. Later, an incomplete run is an ordinary
        # contract refusal and pages through the normal failure path.
        if days > READINESS_LEAD_DAYS or days <= -READINESS_WINDOW:
            return None, False
        recent = self.run_history(log_dir, date)[:READINESS_WINDOW]
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
            return f"{self.name} enforcement in {days} day(s) (run date {switch}): {tally}", False
        if streak >= READINESS_WINDOW:
            return f"{self.name} enforcement active since {switch}: {tally}", False
        return (
            f"URGENT: {self.name} enforcement active since {switch} with only {streak}/"
            f"{READINESS_WINDOW} consecutive complete runs ({tally}). Incomplete runs are "
            f"now refused. To pause, set {self.env} to a later date or 'off'.",
            True,
        )


def readiness_main(switches: list[DatedSwitch], description: str) -> int:
    """CLI over one or more switches: one line per switch with something to say.

    Exit 2 when any switch is urgent (or a switch's env lever is malformed), else 0.
    """
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    urgent_any = False
    lines = []
    for switch in switches:
        try:
            message, urgent = switch.readiness(args.log_dir, args.date)
        except (ContractError, ValueError) as exc:
            message, urgent = f"URGENT: {switch.name} readiness check failed: {exc}", True
        urgent_any = urgent_any or urgent
        if message:
            lines.append(message)
    # One line, urgent notices first: the wrapper folds this output into a summary
    # line, a subject prefix or the run's single failure page.
    lines.sort(key=lambda text: not text.startswith("URGENT"))
    if lines:
        print(" | ".join(lines))
    return 2 if urgent_any else 0
