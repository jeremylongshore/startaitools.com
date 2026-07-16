#!/usr/bin/env python3
"""apply-patterns.py: deterministically apply learned tier-classification patterns.

Thread B2 (2026-07-16). Before this, methodology/patterns.jsonl was inert: the
calibration loop "learned" a rule, a human hand-copied it into the classifier
prompt, and patterns.jsonl sat with times_applied:0 forever (reading like a
silent failure). This script makes patterns.jsonl LIVE:

  * The classify flow pipes the classifier's scored JSON through `--apply`, which
    evaluates each active pattern's machine-readable `rule` against the six
    dimension scores and caps the tier accordingly (a downgrade rule can only
    lower a tier, never raise it). It records which patterns fired in an
    `applied_patterns` list on the decision. This is a DETERMINISTIC backstop to
    the LLM classifier: the same arithmetic rule, evaluated by code, not prose.
  * `--backfill` recomputes each pattern's `times_applied` as the real count of
    historical decisions whose scores match the rule. That is the honest signal
    the zero was hiding.

A pattern is applied only if it is active, not superseded by another active
pattern, and carries a `rule`. Patterns without a `rule` are documentation-only
(historical record) and are never applied.

Rule schema (per pattern):
  "rule": {
    "all": [ {"feature": <name>, "op": <op>, "value": <int>}, ... ],
    "action": {"type": "cap_tier", "tier": <int>}
  }
Features: nov arc nar tch scp rpr (raw 0-5), max_all, max_nov_tch_nar,
count_ge3 (dims >= 3), provisional_tier. Ops: >= <= == != < >.
Action cap_tier caps the tier at the target (min); it can only downgrade.

Exit 0 on success. Never raises on bad data: on any load/parse error it warns to
stderr and passes the classification through UNCHANGED, because this runs on the
land path where a crash would quarantine the post.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

METH_DIR = Path(__file__).resolve().parent.parent / "methodology"
PATTERNS_PATH = METH_DIR / "patterns.jsonl"
DECISIONS_PATH = METH_DIR / "decisions.jsonl"

TIER_NAMES = {1: "Field Note", 2: "Technical Deep-Dive", 3: "Case Study", 4: "Distinguished Paper"}
_DIMS = ("novelty", "arc", "nar", "tch", "scp", "rpr")
_OPS = {
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
}


def _warn(msg: str) -> None:
    print(f"apply-patterns: WARNING: {msg}", file=sys.stderr)


def features(dimensions: dict, provisional_tier: int | None) -> dict:
    """Compute the evaluable feature set from a dimensions dict."""
    nov = int(dimensions.get("novelty", 0))
    arc = int(dimensions.get("arc", 0))
    nar = int(dimensions.get("nar", 0))
    tch = int(dimensions.get("tch", 0))
    scp = int(dimensions.get("scp", 0))
    rpr = int(dimensions.get("rpr", 0))
    allv = [nov, arc, nar, tch, scp, rpr]
    return {
        "nov": nov, "arc": arc, "nar": nar, "tch": tch, "scp": scp, "rpr": rpr,
        "max_all": max(allv),
        "max_nov_tch_nar": max(nov, tch, nar),
        "count_ge3": sum(1 for d in allv if d >= 3),
        "provisional_tier": provisional_tier if provisional_tier is not None else 0,
    }


def load_patterns(path: Path = PATTERNS_PATH) -> list[dict]:
    """Return applicable patterns: active, carry a rule, not superseded by an active one.

    Never raises. On error returns [] (the caller then passes classifications
    through unchanged).
    """
    try:
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    except Exception as e:  # noqa: BLE001
        _warn(f"could not load {path} ({e}); no patterns will be applied")
        return []

    active = [p for p in rows if p.get("active") is True]
    superseded = {
        p.get("supersedes", "").split(" ")[0]
        for p in active
        if p.get("supersedes")
    }
    out = []
    for p in active:
        if p.get("pattern_id") in superseded:
            continue  # an active pattern supersedes this one
        if not isinstance(p.get("rule"), dict):
            continue  # documentation-only pattern, never applied
        out.append(p)
    return out


def rule_matches(rule: dict, feats: dict) -> bool:
    conds = rule.get("all")
    if not isinstance(conds, list) or not conds:
        return False
    for c in conds:
        feat = feats.get(c.get("feature"))
        op = _OPS.get(c.get("op"))
        val = c.get("value")
        if feat is None or op is None or not isinstance(val, (int, float)):
            return False  # malformed condition -> do not fire
        if not op(feat, val):
            return False
    return True


def apply_to(classification: dict) -> dict:
    """Apply active patterns to one classification dict. Returns a new dict with
    the tier possibly capped and an `applied_patterns` list added."""
    dims = classification.get("dimensions") or {}
    tier = classification.get("tier")
    result = dict(classification)
    applied: list[str] = []
    if not isinstance(tier, int):
        result.setdefault("applied_patterns", [])
        return result
    feats = features(dims, tier)
    for p in load_patterns():
        rule = p["rule"]
        if not rule_matches(rule, features(dims, result["tier"])):
            continue
        action = rule.get("action") or {}
        if action.get("type") == "cap_tier":
            target = int(action.get("tier", result["tier"]))
            if target < result["tier"]:
                result["tier"] = target
                result["tier_name"] = TIER_NAMES.get(target, result.get("tier_name", ""))
        applied.append(p.get("pattern_id"))
    result["applied_patterns"] = applied
    return result


def cmd_apply(args) -> int:
    raw = (Path(args.file).read_text(encoding="utf-8") if args.file else sys.stdin.read())
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        _warn(f"input is not valid JSON ({e}); echoing unchanged")
        sys.stdout.write(raw)
        return 0
    out = apply_to(data)
    json.dump(out, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


def cmd_backfill(args) -> int:
    """Recompute times_applied for every rule-carrying pattern from real decision
    scores, then rewrite patterns.jsonl in place (only times_applied changes)."""
    try:
        prows = [json.loads(l) for l in PATTERNS_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    except Exception as e:  # noqa: BLE001
        _warn(f"cannot read patterns.jsonl ({e})")
        return 1
    try:
        drows = [json.loads(l) for l in DECISIONS_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    except Exception as e:  # noqa: BLE001
        _warn(f"cannot read decisions.jsonl ({e})")
        return 1

    counts: dict[str, int] = {}
    for p in prows:
        rule = p.get("rule")
        if not isinstance(rule, dict):
            continue
        pid = p.get("pattern_id")
        n = 0
        for d in drows:
            dims = d.get("dimensions") or {}
            if rule_matches(rule, features(dims, d.get("tier"))):
                n += 1
        counts[pid] = n

    changed = 0
    for p in prows:
        pid = p.get("pattern_id")
        if pid in counts and p.get("times_applied") != counts[pid]:
            p["times_applied"] = counts[pid]
            changed += 1

    if changed and not args.dry_run:
        with PATTERNS_PATH.open("w", encoding="utf-8") as f:
            for p in prows:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")

    for pid, n in counts.items():
        print(f"{pid}: matches {n} of {len(drows)} decisions")
    print(f"({'would update' if args.dry_run else 'updated'} times_applied on {changed} pattern(s))")
    return 0


def cmd_list(args) -> int:
    pats = load_patterns()
    if not pats:
        print("No applicable patterns (active + rule + not superseded).")
        return 0
    for p in pats:
        print(f"{p.get('pattern_id')}: {p.get('name')}  [times_applied={p.get('times_applied')}]")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("apply", help="apply patterns to a classification JSON (stdin or --file)")
    a.add_argument("--file", help="read classification JSON from this file instead of stdin")
    a.set_defaults(func=cmd_apply)

    b = sub.add_parser("backfill", help="recompute times_applied from decisions.jsonl and rewrite patterns.jsonl")
    b.add_argument("--dry-run", action="store_true", help="report counts without writing")
    b.set_defaults(func=cmd_backfill)

    l = sub.add_parser("list", help="list the patterns that would be applied")
    l.set_defaults(func=cmd_list)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
