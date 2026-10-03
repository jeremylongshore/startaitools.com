#!/usr/bin/env python3
"""Record-level persistence for the append-only methodology feedback.jsonl.

Why this exists
---------------
Two writers append to ``.claude/skills/blog-backfill/methodology/feedback.jsonl``
and push to master: the weekly feedback sweep and the daily lander (its
``length_gate_downgrade`` rows, written from an isolated run workspace). When the
sweep committed in the shared checkout and then ``git pull --rebase``-d onto a
master that the lander had appended to, git saw two edits at end-of-file and
stopped with a textual conflict. On 2026-09-27 that left the shared checkout
mid-rebase for six days and stranded four feedback rows.

An isolated worktree alone does not fix that: both writers still append to the
same line range. So the sweep no longer rebases text at all. It keeps its new
records in a durable pending queue outside the repository and, on every publish
attempt, rebuilds the file as ``fresh origin content + pending records`` and
pushes a commit built with git plumbing on that exact origin tip (no working
tree, no index of the shared checkout, no rebase). If origin moves between the
fetch and the push, the push is rejected and the merge is recomputed against the
new tip, so the result is deterministic whoever wins the race.

Merge semantics (record level, never "keep whichever is convenient")
--------------------------------------------------------------------
* Records are compared by canonical JSON (sorted keys, no whitespace).
* Identity key: ``(slug, source, run_id)``. A sweep row and a lander row for the
  same slug have different ``source`` values, so both survive.
* Identical record already on origin  -> duplicate, not re-appended.
* Distinct key                         -> appended.
* Same key, different content          -> CONFLICT. Nothing is published; the
  pending queue is retained and the run reports FAILED for a human to adjudicate.
* An origin file that is not valid JSONL (for example conflict markers) is never
  built upon: the publish refuses with ``invalid_base``.

Subcommands (all print one JSON object on stdout)
-------------------------------------------------
seed     write base + pending into the grading snapshot so the grader skips
         slugs whose records are still waiting to be pushed
stage    move the grader's newly appended rows into the pending queue
publish  merge pending onto fresh origin and push; bounded retries
outcome  map stage results to the wrapper's STATUS and exit code (pure)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FEEDBACK_REL = ".claude/skills/blog-backfill/methodology/feedback.jsonl"

EXIT_OK = 0
EXIT_ERROR = 2
EXIT_CONFLICT = 3
EXIT_DEFERRED = 4


class InvalidJsonl(ValueError):
    """A file that must be JSONL contains a line that is not a JSON object."""


class RecordConflict(ValueError):
    """Two records share an identity key but differ in content."""

    def __init__(self, conflicts):
        super().__init__(f"{len(conflicts)} conflicting record(s)")
        self.conflicts = conflicts


# --------------------------------------------------------------------------- #
# Pure record logic
# --------------------------------------------------------------------------- #
def canonical(record: dict) -> str:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def record_key(record: dict) -> tuple:
    slug = record.get("slug")
    if not slug:
        # No identity fields: identity is the content itself.
        return ("", "", canonical(record))
    return (str(slug), str(record.get("source") or ""), str(record.get("run_id") or ""))


def parse_jsonl(text: str, *, label: str) -> list[tuple[str, dict]]:
    """Return [(raw_line, record)] for every non-blank line, or raise."""
    rows = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise InvalidJsonl(f"{label}:{number}: not JSON ({exc.msg}): {line[:80]!r}") from exc
        if not isinstance(record, dict):
            raise InvalidJsonl(f"{label}:{number}: not a JSON object")
        rows.append((line.rstrip("\r"), record))
    return rows


def merge(base_text: str, pending: list[tuple[str, dict]]) -> dict:
    """Merge pending records onto base. Pure; raises InvalidJsonl/RecordConflict.

    Returns {"text", "added", "duplicates"} where text is base_text with the
    added raw lines appended (base bytes are never rewritten).
    """
    base = parse_jsonl(base_text, label="origin")
    by_key: dict[tuple, set[str]] = {}
    for _raw, record in base:
        by_key.setdefault(record_key(record), set()).add(canonical(record))

    added: list[str] = []
    duplicates = 0
    conflicts = []
    for raw, record in pending:
        key = record_key(record)
        body = canonical(record)
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = {body}
            added.append(raw)
        elif body in existing:
            duplicates += 1
        else:
            conflicts.append({"key": list(key), "pending": record})
    if conflicts:
        raise RecordConflict(conflicts)

    text = base_text
    if added:
        if text and not text.endswith("\n"):
            text += "\n"
        text += "".join(line + "\n" for line in added)
    return {"text": text, "added": len(added), "duplicates": duplicates}


def outcome(
    grade: str,
    local: str,
    remote: str,
    notify: str,
    deferred_runs: int = 0,
    max_deferred_runs: int = 3,
) -> dict:
    """Map stage results to (status, exit code). The single source of truth.

    grade/local: ok | failed | skipped
    remote:      published | already_present | nothing_pending | deferred |
                 exhausted | conflict | invalid_base | error | skipped
    notify:      ok | failed
    """
    reasons = []
    if grade == "failed":
        status, rc = "FAILED", 1
        reasons.append("grading failed")
    elif local == "failed":
        status, rc = "FAILED", 1
        reasons.append("local persistence (pending queue) failed")
    elif remote in ("published", "already_present", "nothing_pending"):
        status, rc = "OK", 0
    elif remote == "deferred":
        status, rc = "DEFERRED", 75
        reasons.append(
            f"push deferred (run {deferred_runs} of {max_deferred_runs}); records retained locally"
        )
    elif remote == "exhausted":
        status, rc = "FAILED", 1
        reasons.append(
            f"push still failing after {deferred_runs} runs (cap {max_deferred_runs}); "
            "records retained locally"
        )
    elif remote == "conflict":
        status, rc = "FAILED", 1
        reasons.append("record conflict: same key, different content; nothing published")
    elif remote == "invalid_base":
        status, rc = "FAILED", 1
        reasons.append("origin feedback.jsonl is not valid JSONL; nothing published")
    else:
        status, rc = "FAILED", 1
        reasons.append(f"remote persistence {remote}")
    if notify == "failed":
        reasons.append("digest email failed")
        if rc == 0:
            status, rc = "DEGRADED", 2
    return {"status": status, "rc": rc, "reasons": reasons, "write_ok": rc == 0}


# --------------------------------------------------------------------------- #
# File helpers
# --------------------------------------------------------------------------- #
def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def load_meta(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {"deferred_runs": 0}


# --------------------------------------------------------------------------- #
# seed / stage
# --------------------------------------------------------------------------- #
def cmd_seed(args) -> dict:
    target = Path(args.feedback)
    pending = parse_jsonl(read_text(Path(args.pending)), label="pending")
    result = merge(read_text(target), pending)
    atomic_write(target, result["text"])
    atomic_write(Path(args.seed_copy), result["text"])
    return {"seeded": result["added"], "already_on_origin": result["duplicates"]}


def cmd_stage(args) -> dict:
    seeded = read_text(Path(args.seeded))
    graded = read_text(Path(args.graded))
    if not graded.startswith(seeded):
        raise InvalidJsonl("grader rewrote existing feedback lines; it may only append")
    new = parse_jsonl(graded[len(seeded) :], label="graded")
    pending_path = Path(args.pending)
    pending_text = read_text(pending_path)
    result = merge(pending_text, new)
    if result["added"]:
        atomic_write(pending_path, result["text"])
    total = len(parse_jsonl(read_text(pending_path), label="pending"))
    return {"new": result["added"], "pending": total}


# --------------------------------------------------------------------------- #
# publish
# --------------------------------------------------------------------------- #
def git(repo: str, *args, input_text: str | None = None, env=None, check=True):
    proc = subprocess.run(
        ["git", "-C", repo, *args],
        input=input_text,
        capture_output=True,
        text=True,
        env=env,
    )
    if check and proc.returncode:
        raise subprocess.CalledProcessError(proc.returncode, proc.args, proc.stdout, proc.stderr)
    return proc


def publish_once(repo: str, branch: str, rel: str, pending, message: str, log) -> dict:
    """One fetch -> merge -> commit-tree -> push attempt. Never touches a worktree."""
    tracking = f"refs/remotes/origin/{branch}"
    fetch = git(repo, "fetch", "-q", "origin", f"+refs/heads/{branch}:{tracking}", check=False)
    if fetch.returncode:
        log(f"fetch of origin/{branch} failed: {fetch.stderr.strip()[:200]}")
        return {"result": "retry"}
    tip = git(repo, "rev-parse", "--verify", tracking).stdout.strip()
    shown = git(repo, "show", f"{tip}:{rel}", check=False)
    base_text = shown.stdout if shown.returncode == 0 else ""
    merged = merge(base_text, pending)  # raises InvalidJsonl / RecordConflict
    if merged["added"] == 0:
        return {"result": "already_present", "tip": tip, "duplicates": merged["duplicates"]}
    blob = git(repo, "hash-object", "-w", "--stdin", input_text=merged["text"]).stdout.strip()
    fd, index = tempfile.mkstemp(prefix="feedback-index.")
    os.close(fd)
    os.unlink(index)
    env = {**os.environ, "GIT_INDEX_FILE": index}
    try:
        git(repo, "read-tree", tip, env=env)
        git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}", env=env)
        tree = git(repo, "write-tree", env=env).stdout.strip()
    finally:
        Path(index).unlink(missing_ok=True)
    commit = git(repo, "commit-tree", tree, "-p", tip, "-m", message).stdout.strip()
    push = git(repo, "push", "-q", "origin", f"{commit}:refs/heads/{branch}", check=False)
    if push.returncode:
        log(f"push of {commit[:9]} onto {tip[:9]} rejected: {push.stderr.strip()[:200]}")
        return {"result": "retry"}
    return {
        "result": "published",
        "commit": commit,
        "tip": tip,
        "added": merged["added"],
        "duplicates": merged["duplicates"],
    }


def verify_present(repo: str, branch: str, rel: str, pending, log) -> bool:
    """Read-only: fetch origin again and confirm every pending record is there."""
    tracking = f"refs/remotes/origin/{branch}"
    if git(
        repo, "fetch", "-q", "origin", f"+refs/heads/{branch}:{tracking}", check=False
    ).returncode:
        log("verify-back fetch failed")
        return False
    shown = git(repo, "show", f"{tracking}:{rel}", check=False)
    try:
        return shown.returncode == 0 and merge(shown.stdout, pending)["added"] == 0
    except (InvalidJsonl, RecordConflict):
        return False


def cmd_publish(args) -> tuple[dict, int]:
    pending_path = Path(args.pending)
    meta_path = Path(args.meta)
    messages = []

    def log(text):
        messages.append(text)

    pending = parse_jsonl(read_text(pending_path), label="pending")
    meta = load_meta(meta_path)
    if not pending:
        if meta_path.exists():
            meta_path.unlink()
        return {"status": "nothing_pending", "pending": 0}, EXIT_OK

    report = {"pending": len(pending)}
    for attempt in range(1, args.attempts + 1):
        if attempt > 1 and args.backoff > 0:
            # Linear backoff: the usual loser of this race is the lander's push
            # landing a second earlier, so a short wait lets it finish.
            time.sleep(args.backoff * (attempt - 1))
        try:
            step = publish_once(args.repo, args.branch, args.path, pending, args.message, log)
        except RecordConflict as exc:
            return {
                **report,
                "status": "conflict",
                "conflicts": exc.conflicts,
                "log": messages,
            }, EXIT_CONFLICT
        except InvalidJsonl as exc:
            return {
                **report,
                "status": "invalid_base",
                "error": str(exc),
                "log": messages,
            }, EXIT_ERROR
        except subprocess.CalledProcessError as exc:
            log(f"git {' '.join(exc.cmd[3:5])} failed: {(exc.stderr or '').strip()[:200]}")
            step = {"result": "retry"}
        if step["result"] in ("published", "already_present"):
            # Verify-back: every pending record must now be on origin before the
            # local copy is discarded. Re-fetch rather than trusting the push.
            if step["result"] == "published" and not verify_present(
                args.repo, args.branch, args.path, pending, log
            ):
                log("verify-back did not find every pending record on origin")
                continue
            pending_path.unlink(missing_ok=True)
            meta_path.unlink(missing_ok=True)
            return {
                **report,
                **step,
                "status": step["result"],
                "attempt": attempt,
                "log": messages,
            }, EXIT_OK

    deferred_runs = int(meta.get("deferred_runs", 0)) + 1
    meta = {"deferred_runs": deferred_runs, "pending": len(pending)}
    atomic_write(meta_path, json.dumps(meta) + "\n")
    status = "exhausted" if deferred_runs >= args.max_deferred_runs else "deferred"
    return {
        **report,
        "status": status,
        "deferred_runs": deferred_runs,
        "max_deferred_runs": args.max_deferred_runs,
        "log": messages,
    }, EXIT_DEFERRED


# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    seed = sub.add_parser("seed")
    seed.add_argument("--feedback", required=True)
    seed.add_argument("--pending", required=True)
    seed.add_argument("--seed-copy", required=True)

    stage = sub.add_parser("stage")
    stage.add_argument("--seeded", required=True)
    stage.add_argument("--graded", required=True)
    stage.add_argument("--pending", required=True)

    pub = sub.add_parser("publish")
    pub.add_argument("--repo", required=True)
    pub.add_argument("--branch", required=True)
    pub.add_argument("--path", default=FEEDBACK_REL)
    pub.add_argument("--pending", required=True)
    pub.add_argument("--meta", required=True)
    pub.add_argument("--message", required=True)
    pub.add_argument("--attempts", type=int, default=3)
    pub.add_argument("--backoff", type=float, default=2.0, help="seconds x attempt between retries")
    pub.add_argument("--max-deferred-runs", type=int, default=3)

    out = sub.add_parser("outcome")
    out.add_argument("--grade", required=True)
    out.add_argument("--local", required=True)
    out.add_argument("--remote", required=True)
    out.add_argument("--notify", required=True)
    out.add_argument("--deferred-runs", type=int, default=0)
    out.add_argument("--max-deferred-runs", type=int, default=3)

    args = parser.parse_args(argv)
    rc = EXIT_OK
    try:
        if args.cmd == "seed":
            result = cmd_seed(args)
        elif args.cmd == "stage":
            result = cmd_stage(args)
        elif args.cmd == "publish":
            result, rc = cmd_publish(args)
        else:
            result = outcome(
                args.grade,
                args.local,
                args.remote,
                args.notify,
                args.deferred_runs,
                args.max_deferred_runs,
            )
    except RecordConflict as exc:
        result, rc = {"status": "conflict", "conflicts": exc.conflicts}, EXIT_CONFLICT
    except (InvalidJsonl, OSError) as exc:
        result, rc = {"status": "error", "error": str(exc)}, EXIT_ERROR
    print(json.dumps(result, sort_keys=True))
    return rc


if __name__ == "__main__":
    sys.exit(main())
