+++
title = 'CodeQL Caught the Race I Dismissed'
slug = 'codeql-caught-the-race-i-dismissed'
date = 2026-05-25T10:00:00-05:00
draft = false
tags = ["security", "typescript", "debugging", "ci-cd", "testing"]
categories = ["Technical Deep-Dive"]
description = "Static analyzer caught a real TOCTOU race in audit-trail code I'd dismissed. How FD-based patterns beat suppression and lock-free approaches."
toc = true
tldr = "I dismissed a CodeQL file-system-race alert with false reasoning — syscall atomicity isn't sequence atomicity. A review caught it. The fix layered a SQLite EXCLUSIVE transaction under a same-FD openSync/fstatSync/writeSync pattern with O_APPEND."
+++

CodeQL accumulated 31 security alerts across the ICOS codebase. Most were correct dismissals—SHA-1 in UUID v5 (mandated by RFC), regex bounds-checking on slugs, format-specific escapers that don't need backslash handling. Triaging all 31 meant documenting each dismissal so someone could review the reasoning. That discipline caught the one dismissal that was wrong.

Alert #13: `js/file-system-race` in `writeTrace`. The function writes append-only audit envelopes whose integrity is a hash chain—each envelope stores `prev_hash = sha256(last line of the file)`. The sequence was:

```ts
const lastLine = readLastLine(absoluteFilePath);
const prev_hash = sha256Hex(lastLine);
// ... build envelope ...
appendFileSync(absoluteFilePath, jsonLine + '\n');
```

I'd dismissed it: "appendFileSync is kernel-atomic per append, safe." But Gemini's PR review flagged the reasoning in the *dismissal doc itself*, not the code. The analyzer was right. The race lives between the read (step 1) and the append (step 4), not in the append itself. Two concurrent processes both read the same last line, compute the identical prev_hash, and both append. The hash chain forks. `verifyAuditChain` flags the discontinuity—a forked chain means the audit trail cannot prove it wasn't tampered with.

Syscall atomicity ≠ sequence atomicity. That's the subtle correctness error—a textbook time-of-check-to-time-of-use bug (TOCTOU, CWE-367) hiding behind a true statement about one syscall.

In the ICOS audit-trail kernel, this isn't a reliability nit. Each envelope's `prev_hash` link is the tamper-evidence substrate—the proof that nobody rewrote history. A forked chain breaks that proof. The security finding was real.

## Why not the obvious fixes?

The surface fix: after iteration 1's SQLite EXCLUSIVE lock made the sequence genuinely race-free, suppress the residual alert with `// codeql[js/file-system-race]` at the callsite. The code is correct at that point—the analyzer just can't see the cross-process lock, so the suppression would be technically defensible. I didn't take it. Suppression hides a correctness class from the next reader and the next file that hits the same shape. You silence one alert and teach nobody. The FD-based rewrite (iteration 3 below) fixes the entire *class* and costs no suppression—the next person who writes a read-then-write sees the canonical pattern in the codebase, not a magic comment.

The second temptation: add a `flock` or lockfile dependency to the read-then-write outside SQLite. SQLite was already a dependency, `writeTrace` already does `INSERT INTO traces` inside the same path, WAL + `busy_timeout=5000` were already configured—so `.exclusive()` costs zero marginal complexity. A new lockfile crate adds a dependency, a new failure mode (stale locks after a crash), and a second source of truth for "who's writing." The SQLite-as-lock decision paid for itself by reusing existing structure.

## Triage discipline

Those two reasons had to be written down before the fix shipped. Among the 31 CodeQL alerts triaged across the codebase, 30 dismissals were correct engineering judgment: SHA-1 in UUID v5 (mandated by RFC 4122 §4.3, SHA-256 would produce a non-conformant UUID and CodeQL's own docs acknowledge the spec requirement); the `js/incomplete-sanitization` alerts on markdown and YAML escapers (neither format escapes backslash, so the escaper is correct for its target); the polynomial-regex-dos case (bounded `.slice(0,80)` input fed to the pattern, no nested quantifiers, safe). Documenting those decisions meant the 31st dismissal—the one that was actually wrong—became reviewable. Triage discipline caught the error.

## Fix iteration 1: SQLite EXCLUSIVE transaction

Wrap steps 1–5 in `db.transaction(...).exclusive()`. better-sqlite3 holds SQLite's cross-process EXCLUSIVE file lock for the duration of the wrapped function. SQLite was already a dependency, already in the write path. Multi-process integration test: spawn 5 child processes, each writes 10 trace events to the same DB, verify `verifyAuditChain` finds zero chain breaks and exactly 50 events. Passed. (~674ms.)

### Iteration 2 — why iteration 1 wasn't enough

The code was now race-free, but CodeQL still flagged it. I'd removed the old `existsSync`+`statSync` pair, yet CodeQL flagged the remaining `statSync`→`appendFileSync` as check-then-use. The analyzer can't model the SQLite EXCLUSIVE transaction's locking semantics—it sees a path-based stat followed by a path-based write and reports the gap it can prove, not the lock it can't. Your code can be actually-safe and still fail the check. That's not a reason to suppress; it's a reason to write code the analyzer can verify locally.

### Fix iteration 3 — the canonical pattern

```ts
const fd = openSync(
  absoluteFilePath,
  fsConstants.O_CREAT | fsConstants.O_APPEND | fsConstants.O_WRONLY,
  0o600,
);
let line_offset: number;
try {
  line_offset = fstatSync(fd).size;
  writeSync(fd, jsonLine + '\n');
} finally {
  closeSync(fd);
}
```

`writeSync` on an `O_APPEND` fd is the functional equivalent of `appendFileSync`, but it operates on the *same* fd that `fstatSync` just measured—which is the whole point. `fstat` + `write` on one fd: no second path resolution, no check-then-use window. CodeQL-safe. `O_APPEND` means the kernel sets the write position to EOF immediately before each write—atomic relative to the fd's offset. `O_CREAT` with mode `0o600` handles first-event-of-day.

This does not replace iteration 1—it layers inside it. The FD pattern still runs within the SQLite EXCLUSIVE transaction. SQLite serializes writers across processes (so two processes can't interleave their read-compute-write sequences); `O_APPEND` guarantees the write itself lands atomically at EOF even in the narrow window where two processes race on `openSync` before the lock is acquired. Both layers ship. Kernel tests: 325/325 pass. Integration: 5 workers × 10 events → chain intact, zero breaks.

## Three transferable lessons

1. **Write dismissal reasons down.** "Dismissed because X" is falsifiable. Silent dismissals hide flawed reasoning. The discipline of documenting caught the error.

2. **Syscall atomicity ≠ sequence atomicity.** "This one call is atomic" is not an argument that a read-compute-write sequence is race-free.

3. **Satisfy both correctness AND the static analyzer's local model.** Don't suppress the alert; adopt the pattern the rule docs recommend. The FD-based rewrite is genuinely safer (no path re-resolution) AND it fits CodeQL's model. It needs no suppression.

Before you promote a scanner to a required gate, clear the backlog honestly. Some real bugs hide among the false positives.

---

**Also shipped:** Locked the Stryker mutation-testing baseline at 55% floor and wired it as a required PR check (ICOS). Compile-then-govern vs RAG v1 experiment results landed (ICOS). gastown-viewer-intent TUI tier-1 build-out: focus enum, key registry, Memories/Triage views, plus daemon hardening (Origin allowlist, session token, loopback bind, THREAT_MODEL.md).

**Related:** [The Unicode layer your validator can't see](/posts/unicode-hygiene-gate-same-day-trapdoor-defense/) · [Self-expiring report-only CI gates](/posts/self-expiring-report-only-ci-gates/) · [Five tags, zero ships](/posts/five-tags-zero-ships/)
