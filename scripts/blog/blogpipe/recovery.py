"""Decide what to do when a producer attempt fails: repair, fail over, or stop.

The daily run used to stop and email a human on any failure. Most failures are not
worth a human: a finished post the contract rejected for a nameable reason, or a
provider out of quota. This module turns one failed attempt into exactly one ACTION.

Routing is deterministic first. The contract's and the workspace helper's messages are
OURS, so they are matched exactly and no model is asked. Only a failure nothing here
recognises is handed to a cheap model, and its answer is accepted only if it names one
of the fixed actions. A model never widens what the loop may do.

HARD LIMIT, enforced by the caller and restated in every repair prompt: the loop may
fix the POST. It may never edit the pipeline, the gates, the skill or the contract,
never touch git, and never relabel a failing verdict as passing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Literal

Action = Literal["repair", "failover", "stop"]
ACTIONS: tuple[Action, ...] = ("repair", "failover", "stop")

# The provider is unusable right now; the work itself may be fine. Try the other one.
PROVIDER_FAULTS = (
    r"\b429\b",
    r"\b529\b",
    r"usage limit reached",
    r"rate.?limit",
    r"overloaded",
    r"payment required",
    r"\b402\b",
    r"insufficient (?:credit|balance|quota)",
    r"quota (?:exceeded|exhausted)",
    r"\b401\b.*(?:unauthor|invalid)",
    r"invalid api key",
    r"authentication_error",
    r"oauth token (?:has )?expired",
    r"connection (?:refused|reset|timed out)",
    r"could not resolve host",
    r"upstream connect error",
)
# Never repairable by rewriting a post: stop, keep the evidence, let catch-up retry later.
UNSAFE = (
    r"producer changed git head",
    r"historical decisions changed",
    r"append-only contract violated",
    r"decisions history was rewritten",
    r"run identity already committed",
    r"conflicting duplicate record",
    r"conflicting existing authority",
    r"mixed checkouts",
    r"sealed or terminal workspace",
    r"canary cannot",
)
# The contract's own complaints: a finished or nearly finished post with a nameable gap.
REPAIRABLE = (
    r"PRODUCER-CONTRACT: FAILED",
    r"PENDING WORK",
    r"staging record missing",
    r"roles receipt",
    r"staged role output",
    r"readiness sentinel",
    r"sentinel ",
    r"final post remains a draft",
    r"front matter",
    r"did not PASS",
    r"gate BLOCK/REVISE",
    r"genuine structured gate receipt required",
    r"pattern-engine",
    r"changes outside run write-set",
    r"run must own exactly one new flat post",
    r"post date differs from run target",
    r"run decisions must be complete appended JSONL records",
    r"staging records must",
    r"expected exactly one target post",
)


@dataclass(frozen=True)
class Decision:
    action: Action
    reason: str
    source: Literal["deterministic", "model", "default"]
    detail: str = ""


def _first(patterns: tuple[str, ...], text: str) -> str | None:
    for pattern in patterns:
        found = re.search(pattern, text, re.IGNORECASE)
        if found:
            return found.group(0)
    return None


def _last_contract_line(text: str) -> str:
    lines = [ln.strip() for ln in text.splitlines() if "PRODUCER-CONTRACT: FAILED" in ln]
    return lines[-1] if lines else ""


def classify(exit_code: int, evidence: str, *, ask_model: bool = False) -> Decision:
    """One failed attempt -> one action. `evidence` is the tail of the run log."""
    unsafe = _first(UNSAFE, evidence)
    if unsafe:
        return Decision("stop", "integrity failure a rewrite cannot fix", "deterministic", unsafe)
    # A process that exited 0 reached the contract: its complaint outranks stray log noise
    # such as a "429" that an earlier, recovered tool call happened to print.
    if exit_code == 0:
        detail = _last_contract_line(evidence) or _first(REPAIRABLE, evidence) or ""
        return Decision(
            "repair", "producer finished; contract named a gap", "deterministic", detail
        )
    fault = _first(PROVIDER_FAULTS, evidence)
    if fault:
        return Decision("failover", "provider unusable", "deterministic", fault)
    if exit_code == 124:
        return Decision("repair", "producer hit the wall-clock ceiling mid-work", "deterministic")
    gap = _first(REPAIRABLE, evidence)
    if gap:
        return Decision("repair", "contract named a gap", "deterministic", gap)
    if ask_model:
        verdict = ask_cheap_model(evidence)
        if verdict:
            return Decision(verdict, "unrecognised failure, classified by a cheap model", "model")
    # Unknown and unclassified: a different provider is the cheapest honest next move.
    return Decision("failover", "unrecognised failure", "default")


MODEL_BRIEF = (
    "A nightly job that writes one blog post failed. Below is the tail of its log. "
    "Answer with EXACTLY ONE WORD and nothing else:\n"
    "repair   = the writer finished or nearly finished and something about its OUTPUT is "
    "missing or invalid, so asking the same writer to fix it could work\n"
    "failover = the AI provider or network is the problem (quota, rate limit, auth, outage), "
    "so a different provider could work\n"
    "stop     = the job's own files, git history or integrity checks are damaged, so "
    "retrying would be unsafe\n\nLOG TAIL:\n"
)


def _one_word(text: str) -> Action | None:
    words = re.findall(r"[a-z]+", text.lower())
    named = [w for w in words if w in ACTIONS]
    return named[-1] if len(set(named)) == 1 else None  # type: ignore[return-value]


def ask_cheap_model(evidence: str, *, timeout: int = 90) -> Action | None:
    """grok -p, then the MiniMax shell agent. Any error or ambiguous answer is None."""
    prompt = MODEL_BRIEF + evidence[-4000:]
    home = __import__("os").path.expanduser
    commands = (
        [home("~/.grok/bin/grok"), "-p", prompt],
        [
            "python3",
            home("~/.local/bin/minimax-agent.py"),
            prompt,
            "--cwd",
            "/tmp",
            "--max-turns",
            "1",
        ],
    )
    for argv in commands:
        try:
            done = subprocess.run(
                argv, capture_output=True, text=True, timeout=timeout, check=False
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if done.returncode == 0:
            verdict = _one_word(done.stdout)
            if verdict:
                return verdict
    return None


NO_MESSAGE = "no message captured; run the verify command in run-contract.md and read it"


def repair_prompt(date: str, reason: str, round_number: int, rounds: int) -> str:
    """What the SAME producer session is told. Names the gap; restates the hard limit."""
    return (
        f"/blog-backfill {date} {date}\n\n"
        f"REPAIR ROUND {round_number} of {rounds}. You already produced the post for {date} in "
        f"this workspace; the deterministic verifier refused it. Its exact message:\n\n"
        f"    {reason or NO_MESSAGE}\n\n"
        "Fix ONLY what that message names, in this same workspace, following "
        "references/run-contract.md. Keep the existing post, classifier and audit unless the "
        "message is about them. If a required Agent result is missing, dispatch that Agent for "
        "real and stage its actual output; never write a role file, receipt, verdict or sentinel "
        "from your own words to make the check pass. If post bytes change, rerun the gates that "
        "bind to them and rewrite the roles receipt. Then run preflight and normal verification "
        "again. You may NOT edit anything under scripts/, .github/, or the skill, may not touch "
        "git, and may not mark a failing verdict as passing. If the message cannot be satisfied "
        "honestly, say so and stop; a later automatic run will try the day again."
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    decide = subs.add_parser("classify")
    decide.add_argument("--exit-code", type=int, required=True)
    decide.add_argument("--evidence-file", required=True)
    decide.add_argument("--ask-model", action="store_true")
    brief = subs.add_parser("repair-prompt")
    for flag in ("date", "reason"):
        brief.add_argument(f"--{flag}", required=True)
    brief.add_argument("--round", type=int, required=True)
    brief.add_argument("--rounds", type=int, required=True)
    args = parser.parse_args()
    if args.command == "classify":
        try:
            with open(args.evidence_file, encoding="utf-8", errors="replace") as handle:
                evidence = handle.read()[-20000:]
        except OSError:
            evidence = ""
        print(json.dumps(asdict(classify(args.exit_code, evidence, ask_model=args.ask_model))))
        return 0
    print(repair_prompt(args.date, args.reason, args.round, args.rounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
