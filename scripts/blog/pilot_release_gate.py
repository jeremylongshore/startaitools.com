#!/usr/bin/env python3
"""Refuse to publish a pilot article until recovery gates RG0, RG1 and RG2 carry evidence.

The blog recovery plan of record (intent-os 000-docs/228, section 3) releases
the growth pilot only after three gates pass, and "a date never passes a gate
on its own". This check makes that mechanical in the publishing path:

  * A post is a PILOT article when its front matter has a non-empty, non-false
    `pilot` key, or a canonical URL on the pilot host (tonsofskills.com).
  * For a pilot article, each gate bead must be `closed` AND its close reason
    must cite evidence (a URL, an owner/repo#N or #N reference, a commit sha,
    or a file path). An automatic or staleness close is not evidence. Nothing
    here reads a clock, so no approval can be inferred from elapsed time.
  * Any failure to read a gate (bd missing, bad JSON, unknown id) refuses.

A post that is not a pilot article returns "not applicable" without running
bd, so the daily lane is unaffected.

Usage:
  pilot_release_gate.py check --post PATH [--beads-dir DIR] [--bd BIN]

Exit codes: 0 pass or not applicable, 3 refused, 2 usage error.
Env: PILOT_GATE_BEADS_DIR (default: the primary startaitools checkout),
     PILOT_GATE_BD_BIN (default: bd on PATH).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

GATES = (
    ("RG0", "startaitools-9a8.17"),
    ("RG1", "startaitools-9a8.18"),
    ("RG2", "startaitools-9a8.19"),
)
PILOT_HOST = "tonsofskills.com"
DEFAULT_BEADS_DIR = "/home/jeremy/000-projects/blog/startaitools"
EXIT_OK, EXIT_USAGE, EXIT_REFUSED = 0, 2, 3
MIN_REASON_CHARS = 20
EVIDENCE = re.compile(
    r"https?://\S+"  # a link to a record, run or PR
    r"|\b[\w.-]+/[\w.-]+#\d+\b"  # owner/repo#N
    r"|(?<![\w/])#\d+\b"  # #N
    r"|\b[0-9a-f]{7,40}\b"  # a commit sha
    r"|\b[\w.-]+/[\w./-]+\.\w+\b"  # a file path with an extension
)
# Closes made by a bot or a staleness sweep, not by a person recording evidence.
# Deliberately narrow: gate records legitimately mention "expired offer" or
# "seven clean days", so the clock is excluded by never reading one, not by
# guessing at wording.
NOT_EVIDENCE = re.compile(r"\bauto[- ]?closed\b|\bclosed as stale\b", re.IGNORECASE)
FALSE_VALUES = {"", "false", "no", "0", "none", "null", "~"}


@dataclass
class Verdict:
    applicable: bool
    passed: bool
    reasons: list[str]


def front_matter(text: str) -> dict[str, str]:
    """Top-level scalar keys of a TOML (+++) or YAML (---) front-matter block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() not in ("+++", "---"):
        return {}
    fence = lines[0].strip()
    sep = "=" if fence == "+++" else ":"
    out: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == fence:
            break
        if not line or line[0].isspace() or sep not in line:
            continue
        key, _, value = line.partition(sep)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        out[key.strip().lower()] = value.strip()
    return out


def pilot_marker(fm: dict[str, str]) -> str | None:
    """Why this post is a pilot article, or None when it is not one."""
    pilot = fm.get("pilot")
    if pilot is not None and pilot.strip().lower() not in FALSE_VALUES:
        return f"front matter pilot = {pilot!r}"
    for key in ("canonicalurl", "canonical_url", "canonical"):
        if PILOT_HOST in fm.get(key, "").lower():
            return f"canonical on the pilot host ({fm[key]})"
    return None


def evidence_problem(reason: str) -> str | None:
    reason = (reason or "").strip()
    if len(reason) < MIN_REASON_CHARS:
        return "close reason is missing or too short to record evidence"
    if NOT_EVIDENCE.search(reason):
        return "close reason records an automatic or staleness close, not evidence"
    if not EVIDENCE.search(reason):
        return "close reason cites no evidence (URL, repo#N, #N, commit sha or file path)"
    return None


def read_gate(bead_id: str, bd: str, beads_dir: str) -> dict:
    proc = subprocess.run(
        [bd, "show", bead_id, "--json"],
        cwd=beads_dir,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"bd show exited {proc.returncode}")
    data = json.loads(proc.stdout)
    if isinstance(data, list):
        data = data[0] if data else {}
    if not isinstance(data, dict) or data.get("id") != bead_id:
        raise RuntimeError("bd show returned a different or empty record")
    return data


def evaluate(post: Path, bd: str, beads_dir: str) -> Verdict:
    try:
        text = post.read_text(encoding="utf-8")
    except OSError as exc:
        return Verdict(True, False, [f"cannot read post ({type(exc).__name__}); refusing"])
    marker = pilot_marker(front_matter(text))
    if marker is None:
        return Verdict(False, True, ["not a pilot article; recovery gates not applicable"])
    reasons = [f"pilot article: {marker}"]
    passed = True
    for gate, bead_id in GATES:
        try:
            record = read_gate(bead_id, bd, beads_dir)
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            passed = False
            reasons.append(f"{gate} ({bead_id}): unreadable ({exc}); refusing")
            continue
        status = record.get("status")
        if status != "closed":
            passed = False
            reasons.append(f"{gate} ({bead_id}): status {status!r}, not closed")
            continue
        problem = evidence_problem(record.get("close_reason", ""))
        if problem:
            passed = False
            reasons.append(f"{gate} ({bead_id}): closed but {problem}")
        else:
            reasons.append(f"{gate} ({bead_id}): closed with evidence")
    return Verdict(True, passed, reasons)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("check")
    c.add_argument("--post", type=Path, required=True)
    c.add_argument("--beads-dir", default=os.environ.get("PILOT_GATE_BEADS_DIR", DEFAULT_BEADS_DIR))
    c.add_argument("--bd", default=os.environ.get("PILOT_GATE_BD_BIN", ""))
    args = parser.parse_args(argv)
    bd = args.bd or shutil.which("bd") or "bd"
    verdict = evaluate(args.post, bd, args.beads_dir)
    label = "PASS" if verdict.passed else "REFUSED"
    if not verdict.applicable:
        label = "NOT-APPLICABLE"
    print(f"PILOT-GATE: {label} — " + "; ".join(verdict.reasons))
    return EXIT_OK if verdict.passed else EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main())
