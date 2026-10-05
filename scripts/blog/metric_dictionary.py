#!/usr/bin/env python3
"""Load and validate the blog metric dictionary (scripts/blog/metric-dictionary.json).

The dictionary is the single place a reported number gets its meaning: every
metric names its numerator, denominator, eligibility, window, filter version
and unit, plus the rule that turns an ineligible value into n/a instead of 0.
It carries definitions only. Measured values and baselines stay in the private
measurement store.

Usage:
  metric_dictionary.py check [--path PATH]   validate; prints version + sha256
  metric_dictionary.py stamp [--path PATH]   one-line version stamp for reports

Exit codes: 0 valid, 1 invalid, 2 usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

DEFAULT_PATH = Path(__file__).resolve().with_name("metric-dictionary.json")
REQUIRED_FIELDS = (
    "label",
    "unit",
    "numerator",
    "denominator",
    "eligibility",
    "window",
    "filter_version",
    "n_a",
)
REQUIRED_STATES = ("measured", "zero", "unavailable", "unknown", "n/a")
HEADLINE_KEYS = ("recovery", "pilot_primary", "pilot_secondary")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


class DictionaryError(ValueError):
    """The dictionary is missing, unreadable or violates its own contract."""


def load(path: Path | str | None = None) -> dict:
    p = Path(path) if path else DEFAULT_PATH
    try:
        raw = p.read_bytes()
        data = json.loads(raw)
    except (OSError, ValueError) as exc:
        raise DictionaryError(f"metric dictionary unreadable: {p}: {exc}") from exc
    validate(data)
    data["_sha256"] = hashlib.sha256(raw).hexdigest()
    return data


def validate(data: dict) -> None:
    problems: list[str] = []
    if data.get("schema") != "is-blog-metric-dictionary":
        problems.append("schema must be is-blog-metric-dictionary")
    if not SEMVER.match(str(data.get("version", ""))):
        problems.append("version must be MAJOR.MINOR.PATCH")
    rule = (data.get("filter") or {}).get("rule_version")
    if not rule:
        problems.append("filter.rule_version missing")
    states = data.get("value_states") or {}
    problems += [f"value_states.{s} missing" for s in REQUIRED_STATES if s not in states]
    metrics = data.get("metrics") or {}
    if not metrics:
        problems.append("no metrics defined")
    for mid, m in metrics.items():
        for field in REQUIRED_FIELDS:
            if not str(m.get(field, "")).strip():
                problems.append(f"metrics.{mid}.{field} missing")
    headline = data.get("headline") or {}
    for key in HEADLINE_KEYS:
        mid = headline.get(key)
        if mid not in metrics:
            problems.append(f"headline.{key} must name a defined metric (got {mid!r})")
    if not (data.get("comparison_rule") or {}).get("allowed_only_when"):
        problems.append("comparison_rule.allowed_only_when missing")
    if problems:
        raise DictionaryError("; ".join(problems))


def stamp(data: dict) -> str:
    return (
        f"metric dictionary v{data['version']} (sha256 {data['_sha256'][:12]}), "
        f"filter {data['filter']['rule_version']}, "
        f"measurement contract v{data['derived_from']['measurement_contract']['version']}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=("check", "stamp"))
    parser.add_argument("--path", type=Path, default=None)
    args = parser.parse_args(argv)
    try:
        data = load(args.path)
    except DictionaryError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    if args.command == "check":
        print(f"OK metric dictionary v{data['version']} sha256 {data['_sha256']} "
              f"({len(data['metrics'])} metrics)")
    else:
        print(stamp(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
