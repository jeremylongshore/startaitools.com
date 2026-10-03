"""The producer record schema: flag enum, cadence_type, rhetorical_structure, record_type.

Blog Recovery Phase I, E07-T03 (startaitools.com#127). The September calibration found
that when the producer path changed on 2026-09-15, official flag names fell from 93% to
41% of flags, `cadence_type` disappeared from every record and one record wrote
`rhetorical_structure` as an object. Nothing at the boundary noticed. This module checks
the run's OWN staged classifier and audit records against the enums in
blogpipe/records.py (the single source of truth the instructions point at):

- `record_type`: "classifier" on the classifier record, "audit" on the audit addendum.
- `anti_inflation_flags`: a list (empty when no flag applies) of exact enum strings, no
  annotations and no "none triggered" placeholder; explanations belong in `reasoning`.
- `cadence_type`: required, one of CADENCE_TYPES.
- `rhetorical_structure`: one string from RHETORICAL_STRUCTURES.

Historical records are never re-validated: the contract only ever reads the records of
the run it is verifying, and the switch is keyed on that run's target date.

ROLLOUT reuses the dated switch of the amended reader contract (blogpipe/switch.py):
observation before RECORD_SCHEMA_ENFORCE_FROM (one `ADVISORY: record schema (...)` line
per validation), refusal on and after it, `BLOG_RECORD_SCHEMA_ENFORCE_FROM=YYYY-MM-DD|off`
as the operator lever, and the same readiness countdown/URGENT alarm in the daily wrapper
(`python3 -B -m blogpipe contract-readiness`).
"""

from __future__ import annotations

from typing import Any

from .records import (
    ANTI_INFLATION_FLAGS,
    AUDIT,
    CADENCE_TYPES,
    CLASSIFIER,
    RHETORICAL_STRUCTURES,
)
from .switch import DatedSwitch, readiness_main

# Proposed: seven consecutive complete daily runs (2026-10-10..16) after the instruction
# change is live by 2026-10-09; the first enforced run date is the eighth.
RECORD_SCHEMA_ENFORCE_FROM = "2026-10-17"
ENFORCE_ENV = "BLOG_RECORD_SCHEMA_ENFORCE_FROM"

SWITCH = DatedSwitch(
    name="record schema",
    label="record schema",
    env=ENFORCE_ENV,
    default=lambda: RECORD_SCHEMA_ENFORCE_FROM,
)


def _allowed(values: tuple[str, ...]) -> str:
    return "|".join(values)


def _got(value: Any) -> str:
    return "absent" if value is None else repr(value)[:60]


# Each gap names the field first, then what was found and what is allowed. The advisory
# line reads "missing <gap>, <gap>"; a refusal reads "record schema invalid: <gap>; <gap>".
def classifier_gaps(record: dict[str, Any]) -> list[str]:
    """Name every malformed classifier field; empty means the record is schema-valid."""
    gaps = []
    if record.get("record_type") != CLASSIFIER:
        gaps.append(f"classifier.record_type (got {_got(record.get('record_type'))}; "
                    f"must be {CLASSIFIER!r})")
    flags = record.get("anti_inflation_flags")
    if not isinstance(flags, list):
        gaps.append(f"classifier.anti_inflation_flags (got {_got(flags)}; must be a list, "
                    "[] when no flag applies)")
    else:
        unknown = [
            flag for flag in flags if not isinstance(flag, str) or flag not in ANTI_INFLATION_FLAGS
        ]
        if unknown:
            shown = " ".join(_got(flag) for flag in unknown)
            gaps.append(f"classifier.anti_inflation_flags (off-enum {shown}; allowed: "
                        f"{_allowed(ANTI_INFLATION_FLAGS)})")
        elif len(set(flags)) != len(flags):
            gaps.append("classifier.anti_inflation_flags (repeats a flag)")
    cadence = record.get("cadence_type")
    if not isinstance(cadence, str) or cadence not in CADENCE_TYPES:
        gaps.append(f"classifier.cadence_type (got {_got(cadence)}; allowed: "
                    f"{_allowed(CADENCE_TYPES)})")
    structure = record.get("rhetorical_structure")
    if not isinstance(structure, str) or structure not in RHETORICAL_STRUCTURES:
        gaps.append(f"classifier.rhetorical_structure (got {_got(structure)}; allowed: "
                    f"{_allowed(RHETORICAL_STRUCTURES)})")
    return gaps


def audit_gaps(record: dict[str, Any]) -> list[str]:
    if record.get("record_type") != AUDIT:
        return [f"audit.record_type (got {_got(record.get('record_type'))}; must be {AUDIT!r})"]
    return []


def schema_gaps(classifier: dict[str, Any], audit: dict[str, Any]) -> list[str]:
    return classifier_gaps(classifier) + audit_gaps(audit)


def enforcement_date() -> str | None:
    return SWITCH.enforcement_date()


def enforced(date: str) -> bool:
    return SWITCH.enforced(date)


def report(date: str, gaps: list[str]) -> None:
    SWITCH.report(date, gaps)


def main() -> int:
    """`contract-readiness`: every dated producer-contract switch, one line each."""
    from . import brief

    return readiness_main([brief.SWITCH, SWITCH], "Producer contract enforcement readiness")
