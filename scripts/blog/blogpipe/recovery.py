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


def verifier_message(text: str) -> str:
    """The repair reason, from the VERIFIER'S OWN captured output and nowhere else.

    The run log is a pty transcript: the producer can print anything into it, including a
    line that looks like a verifier complaint. Feeding that back as "the verifier said"
    would let a confused or adversarial producer write its own repair instruction. So the
    wrapper captures the verifier's and the write-set validator's stderr in a separate
    file, and only that file reaches here. Control characters are stripped and the length
    is capped, because this text is pasted into a prompt.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    chosen = next((ln for ln in reversed(lines) if "PRODUCER-CONTRACT: FAILED" in ln), "")
    if not chosen:
        chosen = next((ln for ln in reversed(lines) if '"error"' in ln or "error" in ln), "")
    chosen = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", chosen)
    return chosen[:400]


def classify(
    exit_code: int, evidence: str, *, verifier: str = "", ask_model: bool = False
) -> Decision:
    """One failed attempt -> one action.

    `evidence` (the run-log tail, partly producer-controlled) only ROUTES. `verifier` (the
    verifier's separately captured output) is the only source of the repair REASON.
    """
    unsafe = _first(UNSAFE, evidence + "\n" + verifier)
    if unsafe:
        return Decision("stop", "integrity failure a rewrite cannot fix", "deterministic", unsafe)
    message = verifier_message(verifier)
    fault = _first(PROVIDER_FAULTS, evidence)
    if exit_code == 0:
        # The producer finished. If the verifier spoke, that is the gap to repair. If it
        # said nothing and the log shows a provider fault, the "finished" run was hollow:
        # go straight to the other provider instead of burning repair rounds on it.
        if not message and fault:
            return Decision(
                "failover", "exited 0 but the provider failed mid-run", "deterministic", fault
            )
        return Decision(
            "repair", "producer finished; verifier named a gap", "deterministic", message
        )
    if fault:
        return Decision("failover", "provider unusable", "deterministic", fault)
    if exit_code == 124:
        return Decision("repair", "producer hit the wall-clock ceiling mid-work", "deterministic")
    if _first(REPAIRABLE, evidence):
        # Routed by the log, but the REASON stays empty: nothing here came from the verifier.
        return Decision(
            "repair", "log suggests an output gap; no verifier message", "deterministic"
        )
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
    decide.add_argument("--verifier-file", default="")
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
        verifier = ""
        if args.verifier_file:
            try:
                with open(args.verifier_file, encoding="utf-8", errors="replace") as handle:
                    verifier = handle.read()[-8000:]
            except OSError:
                verifier = ""
        decision = classify(args.exit_code, evidence, verifier=verifier, ask_model=args.ask_model)
        print(json.dumps(asdict(decision)))
        return 0
    print(repair_prompt(args.date, args.reason, args.round, args.rounds))
    return 0


if __name__ == "__main__":
    sys.exit(main())
