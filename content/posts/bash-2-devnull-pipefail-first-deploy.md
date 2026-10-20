+++
title = 'Bash 2>/dev/null Hides stderr, Not the Exit Code'
slug = 'bash-2-devnull-pipefail-first-deploy'
date = 2026-10-19T10:00:00-06:00
draft = false
tags = ["bash", "shell", "install-scripts", "deploy", "pipefail", "set-e", "regression-test", "radicale"]
categories = ["DevOps"]
description = "Bash 2>/dev/null hides the message but not the exit code. Under set -euo pipefail, the suppressed exit still aborts a substitution, killing first deploys."
tldr = "Under `set -euo pipefail`, `2>/dev/null` hides stderr but not the exit code; a missing file in a command substitution aborts the script silently. Wrap the failing read in `|| true` BEFORE the pipe boundary. Test by extracting the real line from the script and running it in a separate bash with the same shell options."
+++

First deploy of a config or rights file is when bash scripts lie. The file does not exist yet, the script tries to read it, the redirect to `/dev/null` silences the error message, the pipe stays in `pipefail` mode (any pipeline step failing aborts the whole pipeline), and `set -e` mode (the script exits on the first error) walks out of the script before the next install line runs. The deploy log ends with exit 1 and no error message. Nothing is applied at all, and the deploy log looks clean.

That's what happened on the calendar rights deploy in intent-os (the company's internal operations and documentation repo). The intent was to make the shared Team calendar view-only for the leads on Radicale (an open-source CalDAV server): ship a new config bundle, drop a permissions rights file next to it, take write access away from the leads. The first deploy attempt exited 1 with no output. The VPS (virtual private server) state stayed exactly as it had been before the run. The permissions file was missing, the link was missing, and the container was not restarted. The leads kept write access on Team because nothing had moved.

The pattern looks fine in this form:

```bash
CFG_BEFORE="$(sudo cat "$CFG_DIR/config" "$CFG_DIR/rights" 2>/dev/null | sha256sum)"
```

`2>/dev/null` sends stderr to the void. Bash happily reports no error. But `cat` still exits non-zero when the file is missing, and the non-zero exit propagates through the pipe. `pipefail` is on, `set -e` is on, the substitution fails, the script exits. The diff that introduced this was small, with a new rights file, a new CFG_BEFORE, a new CFG_AFTER, and two install lines. None of them read like a bug.

The fix is one line of grouping:

```bash
CFG_BEFORE="$({ sudo cat "$CFG_DIR/config" "$CFG_DIR/rights" 2>/dev/null || true; } | sha256sum)"
```

The `{ ... || true; }` group catches the failing `cat` and substitutes a successful exit. The pipe then completes and the substitution returns a hash. The two `install` lines below still fail closed on a write error. The intent was never "swallow real failures"; the intent was "first deploy has no rights file, that is the normal case."

The test that catches this has to run the line, not grep for it. A grep check that confirms the line exists, or a static analyzer that says it parses, is not enough. The test has to run the actual line from install.sh in a separate bash with the same shell options, against a config folder that has no rights file. `$CAL` and `$TMP` are the drill's own variables (the ops/calendar directory and its scratch directory):

```bash
cfg_line="$(grep -E '^CFG_BEFORE=' "$CAL/install.sh")"
[ -n "$cfg_line" ] || fail "install.sh has no CFG_BEFORE line"
mkdir -p "$TMP/first-deploy-cfg" && echo '[rights]' > "$TMP/first-deploy-cfg/config"
CFG_DIR="$TMP/first-deploy-cfg" bash -euo pipefail -c 'sudo() { "$@"; }; eval "$1"; [ -n "$CFG_BEFORE" ]' _ "$cfg_line" \
  || fail "install.sh stops on a first deploy: its CFG_BEFORE line fails when the rights file is missing"
```

Two design choices in that test. The first (run the line in a separate `bash -euo pipefail`) came from getting it wrong the first time. `set -e` does not apply on the left side of `||`, and the original check ran the line in a subshell there, where `set -e` is ignored, so the drill printed PASS against the very bug it was written to catch. Hand-running the line against `2a9c9f61`'s install.sh surfaced that. The second (grep the live line and pass it through `eval`) keeps the test honest with the script; a copy of the line in the test drifts the first time install.sh is edited.

The drill now fails on the unfixed line ("install.sh stops on a first deploy") and passes on the grouped line. The whole drill is 38 checks, both planted faults trigger as designed, and the failed deploy is recorded in the evidence folder. The lesson is not "add more logging." Adding `set -x` would have surfaced the cat failure, but the underlying install is still broken and the next operator gets the same surprise on a different missing file. The lesson is "the missing-file case has to be in the install path or the test has to run the install path."

`2>/dev/null` is a useful tool. Under `set -euo pipefail` it is not an exit-code suppressor. If a command's failure is normal, the code has to say so: `|| true`, an `if`, an `until`, anything that makes the exit expected to bash. If the failure is not normal, the group has to fail closed. The middle case, "silently fall through", does not exist under strict mode. Either the failure is normal or it is fatal; bash wants to know which.

## Use this

- Replace any `cmd 2>/dev/null` inside a `$(...)` substitution under `set -euo pipefail` with `({ cmd 2>/dev/null || true; } | next)`. The grouping has to be before the pipe, not at the end.
- For install scripts that ship new files, add a regression test that extracts the real line from the script with `grep` and runs it under `bash -euo pipefail -c '...'` against a fresh config dir. A grep that says the line exists is not a test.
- Run the check in a separate bash, not a subshell. `set -e` is ignored on the left of `||`, so a subshell run of the same line will pass against the bug it is supposed to catch.

The fix landed in `ops/calendar/install.sh` (in the intent-os repository, not public) and the drill that locks it in `ops/calendar/tests/calendar-rights-drill.sh`.

## Related Posts

- [when-third-party-ci-credentials-expire-the-deploy-fallback-lives-on-the-vps](/posts/when-third-party-ci-credentials-expire-the-deploy-fallback-lives-on-the-vps/): A VPS-resident deploy script needs no third-party key, and a SHA-pin guard proves the manual path cannot ship content the merged PR did not introduce.
- [a-green-recovery-drill-can-still-be-lying](/posts/a-green-recovery-drill-can-still-be-lying/): A recovery drill that prints PASS while the underlying recovery is broken teaches nothing; what got checked matters more than what got answered.
- [five-silent-failures-one-day](/posts/five-silent-failures-one-day/): Five classes of failure that exit 0 and say nothing; each has a probe that catches it, and none of them is "add more logging".