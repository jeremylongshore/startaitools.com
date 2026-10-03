"""decisions.jsonl record kinds, the producer field enums, and the classifier/shipped ledger.

ONE SOURCE OF TRUTH. The producer instructions (blog-backfill content-tier-classification.md,
classify-day.md, agents/blog-classifier.md) point at the tuples below instead of restating
them, the producer contract (blogpipe/schema.py) enforces them, and every reader of
decisions.jsonl (tier-creep guard, feedback sweep, methodology index, pattern backfill,
calibration ledger) selects records through `record_type()`.

STDLIB ONLY, NO PACKAGE-RELATIVE IMPORTS: the skill-side readers load this file by path
(`load_records()` in each of them), outside the package, so it must stand alone.

Record types (E07-T02, startaitools.com#127):

- `classifier`   the day's tier decision (tier, dimensions, pattern_engine receipt).
- `audit`        the agent_audit addendum. Still also carries `audit_addendum: true`, so the
                 lander's older jq selectors keep working unchanged.
- `shipped_tier` appended by the lander when its length gate ships a LOWER tier than the
                 classifier chose. It deliberately has no `tier` key: every legacy reader that
                 tests `"tier" in record` ignores it instead of counting a second decision.

A recovered decision (re-landed from quarantine) is a `classifier` record that also carries
`recovery_from_quarantine: true`; recovery is provenance, not a different kind of decision.

Historical records (before record_type existed) are classified by the fallback in
`record_type()`. The fallback is what makes the recovered 2026-09-12 decision count: it was
written with `audit_addendum: true` but carries tier + dimensions, so it is that day's
classifier decision. Filtering on `audit_addendum` alone loses it (29 decisions, not 30).
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from typing import Any

# --- Field enums: the producer boundary validates against exactly these. -----------------

ANTI_INFLATION_FLAGS = (
    "volume-not-quality",
    "busy-not-distinguished",
    "first-time-for-me-not-novel",
    "high-scope-not-escalating",
    "flat-wall-of-threes",
    "linear-narrative-scored-as-drama",
    "no-named-artifact",
    "distribution-pressure",
)
CADENCE_TYPES = ("daily", "weekly", "monthly", "on-demand", "manual_reconciliation")
RHETORICAL_STRUCTURES = (
    # Tier 1
    "chronological-narrative",
    "thematic-grouping",
    # Tier 2
    "problem-solution",
    "before-after",
    "debugging-journey",
    # Tier 3
    "thesis-driven",
    "comparative-analysis",
    "design-rationale",
)

# --- Record kinds. ---------------------------------------------------------------------

CLASSIFIER = "classifier"
AUDIT = "audit"
SHIPPED_TIER = "shipped_tier"
RECORD_TYPES = (CLASSIFIER, AUDIT, SHIPPED_TIER)
# Historical explicit values that predate the closed set.
LEGACY_ALIASES = {"agent_audit": AUDIT}
# Fallback-only kinds for history; never written going forward.
RECONCILIATION = "reconciliation"
UNKNOWN = "unknown"

LENGTH_GATE = "length_gate"
LEGACY_LENGTH_GATE_SOURCE = "length_gate_downgrade"  # the lander's feedback.jsonl source


def record_type(record: Any) -> str:
    """The record's kind: explicit `record_type` first, else the historical-shape fallback."""
    if not isinstance(record, dict):
        return UNKNOWN
    explicit = record.get("record_type")
    if isinstance(explicit, str) and explicit:
        return LEGACY_ALIASES.get(explicit, explicit)
    if record.get("event") == "agent_audit":
        return AUDIT
    if "publication_status" in record:
        return RECONCILIATION
    if "tier" in record and (
        record.get("audit_addendum") is not True or isinstance(record.get("dimensions"), dict)
    ):
        return CLASSIFIER
    if record.get("audit_addendum") is True or "agent_audit" in record:
        return AUDIT
    return UNKNOWN


def is_classifier(record: Any) -> bool:
    return record_type(record) == CLASSIFIER


def shipped_record(
    *,
    date: str,
    slug: str,
    run_id: str,
    source_run: str | None,
    classifier_tier: int,
    shipped_tier: int,
    body_lines: int,
    tier1_max_lines: int,
    tier2_max_lines: int,
) -> dict[str, Any]:
    """The lander's append when the length gate ships a lower tier than the classifier."""
    if not (type(classifier_tier) is int and type(shipped_tier) is int):
        raise ValueError("tiers must be integers")
    if not 1 <= shipped_tier < classifier_tier <= 3:
        raise ValueError("a shipped_tier record exists only for a downgrade")
    return {
        "record_type": SHIPPED_TIER,
        "date": date,
        "slug": slug,
        "run_id": run_id,
        "source_run": source_run or None,
        "classifier_tier": classifier_tier,
        "shipped_tier": shipped_tier,
        "downgrade_reason": LENGTH_GATE,
        "body_lines": body_lines,
        "thresholds": {"tier1_max_lines": tier1_max_lines, "tier2_max_lines": tier2_max_lines},
    }


def tier_ledger(
    decisions: Iterable[dict[str, Any]],
    feedback: Iterable[dict[str, Any]] = (),
    *,
    start: str | None = None,
    end: str | None = None,
) -> list[dict[str, Any]]:
    """One row per classifier decision in [start, end): classifier tier and shipped tier.

    Shipped tier, by precedence: the last `shipped_tier` record for the slug; else (history
    before E07-T02) the lander's `length_gate_downgrade` feedback row for the slug; else the
    classifier tier, because the gate only ever downgrades and did not fire.
    """
    decisions = list(decisions)
    shipped: dict[str, dict[str, Any]] = {}
    for record in decisions:
        if record_type(record) == SHIPPED_TIER and isinstance(record.get("slug"), str):
            shipped[record["slug"]] = record
    legacy: dict[str, dict[str, Any]] = {}
    for row in feedback:
        if (
            isinstance(row, dict)
            and row.get("source") == LEGACY_LENGTH_GATE_SOURCE
            and isinstance(row.get("slug"), str)
        ):
            legacy[row["slug"]] = row
    rows: dict[str, dict[str, Any]] = {}
    for record in decisions:
        if not is_classifier(record):
            continue
        day = str(record.get("date", ""))[:10]
        if (start and day < start) or (end and day >= end):
            continue
        slug = record.get("slug")
        tier = record.get("tier")
        source = "classifier"
        shipped_tier = tier
        if slug in shipped:
            shipped_tier, source = shipped[slug].get("shipped_tier"), SHIPPED_TIER
        elif slug in legacy and legacy[slug].get("correct_tier") is not None:
            shipped_tier, source = legacy[slug]["correct_tier"], "legacy_feedback_length_gate"
        rows[slug] = {
            "date": day,
            "slug": slug,
            "classifier_tier": tier,
            "shipped_tier": shipped_tier,
            "shipped_source": source,
            "recovered": record.get("recovery_from_quarantine") is True,
        }
    return sorted(rows.values(), key=lambda row: (row["date"], str(row["slug"])))


def distribution(rows: Iterable[dict[str, Any]], key: str) -> tuple[int, int, int]:
    counts = Counter(row[key] for row in rows)
    return counts[1], counts[2], counts[3]
