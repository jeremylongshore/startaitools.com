# Daily blog contract, isolated scheduling and recovery

Owner issue #73; methodology migration #74; parent intent-os#619. Source cron
remains the established04:00 host-time daily wrapper. No parallel scheduler or
periodic restarts are introduced. Producer process status and validated completion
are different signals; an exit0 child without required artifacts is FAILED.

## Run boundaries

`blog-backfill-daily.sh --date YYYY-MM-DD` holds the canonical
`/tmp/blog-pipeline.lock` onFD9, discovers the fresh authoritative origin/master,
and creates a dedicated `blog-run/DATE/UUID` worktree under
`~/.local/state/blog-run-workspaces`. The owner's primary checkout is never
normalized, stashed, restored or used for producer writes. Existing unrelated
schema edits, drafts and an August untracked post remain intact.

The durable manifest records source/common Git directory, approved remote,
baseline SHA, target date, Claude session UUID, workspace, allowed paths and
status. A per-run producer lock is inherited by children. Overlap and abandoned
recovery are proven using real locks, not an environment claim. After a crash,
next creation can snapshot/quarantine an abandoned uncommitted run while retaining
its entire workspace/logs. A live child blocks reuse. A committed unpublished
candidate remains visibly pending; it is never erased or marked published.
Published candidates reconcile against the authoritative remote. Inspect manifest
and run.log/producer.log before any operator recovery.

Producer writes permit one NEW target-date post, exact-identity append-only
classifier/audit decisions and ignored `DATE.UUID.label.json` staging candidates.
Existing posts, historical lines, unrelated changes or escaping/symlink paths
fail validation. Optional structural-tier feedback must append only for the same
slug/run. Canonical queue/ledger remain at the established source-repo state
paths via BLOG_STATE_DIR; they are not stranded in disposable workspaces.

## Completion and publication

The shared read-only `blog-producer-contract.py verify` requires versioned
readiness with date/slug/run/tier/final-draft SHA256, current deterministic pattern
receipt, exactly one scoped classifier and separate audit, actual mandatory Agent
completions and actual quality-gate PASS receipts bound to final bytes. Required
BLOCK/REVISE, missing gate, stale transcript/draft and malformed scope fail before
producerOK and before landing. Tier3 requires docs-architect; Tier4 remains a
separate manual research workflow. Backtick/tilde/indented code requires review.

Scoped appends use `blog-producer-contract.py append` with a file lock, fsync,
exact target identity, identical-duplicate no-op and conflicting-duplicate refusal.
Global producer instructions come from claude-skills-private PR2; this paired
change must be deployed with the application contract. Never invent Agent calls,
readiness or classifiers to clear quarantine. The lander may retain defensive
pattern healing, but that cannot erase a failed producer contract.

Landing requires a bound manifest, stages only returned publish_paths, uses normal
commit hooks and pushes HEAD explicitly to master after an FF/publication check.
It verifies remote inclusion and terminalizes canonical publication before later
image work. Asset races rebase only unpublished asset commits inside that isolated
run, with bounded attempts and no autostash. An image failure cannot dirty or
diverge the next day's source checkout. Invalid production snapshots run-owned
artifacts into quarantine and retains evidence; no shared decision reset occurs.

Release workflow now depends on the repository's actual reusable scripts-lint
checks. Test failures, tag-push or GitHub-release failures cannot be called success.
A successful source push still requires separate deploy/public and packet evidence.

## Detection and diagnosis

All three consequence emails carry `[blog-daily-DATE]`: quarantine, daily summary
and missing-ledger packet sweep. Detailed logs identify the session UUID/source
SHA. Coverage remains intact; failures are not suppressed. Check process exit,
PRODUCER-CONTRACT completion, run write-set status, landRC, remote publication,
index integrity, ledger and packet independently. Methodology rebuild failures
make overall pipeline status nonzero and preserve the last-good index.

Exact incident logs: ~/.local/state/blog-backfill-daily/run-DATE.log and
~/.local/state/blog-land/land-DATE.log. For the September15/16 content dates,
original quarantine/log evidence is preserved; recover only with genuine new
required reviews and a bound run. Never merely add missing fields to publish.

## Offline checks and canary

```bash
shellcheck -S style scripts/blog/*.sh .claude/skills/blog-*/scripts/*.sh verify_links.sh check_links.sh
bash scripts/blog/test-pipeline-invariants.sh
ruff check scripts/blog/*.py .claude/skills/blog-*/scripts/*.py tests/*.py check-links.py
python3 -m pytest tests/ -q
python3 scripts/blog/catalog-audit.py --start 2026-07-16 --end 2026-07-29 --article content/posts/after-14-days-of-daily-posts-here-is-what-i-notice.md
hugo --buildFuture --gc -d /tmp/hugo-verify
```

Use CI-pinned Hugo0.150.0 extended, initialize only the isolated worktree's theme
submodules, and run actionlint for workflow changes. The historical70e7feda
regression fixture demonstrates exit0→falseOK versus current contract failure.
Workspace tests cover owner dirt, scope, locks, crash/quarantine/idempotency and
verified FF publication; methodology tests cover complete atomic migration.

A provider canary uses a local test remote containing the exact repaired commit,
BLOG_REPO_DIR/BLOG_EXPECTED_REMOTE pointing to that clone, distinct run state and
BLOG_STATE_DIR, and BLOG_CANARY=1. It invokes the real configured provider but
runs the lander dry-run, preserves its workspace/evidence and sends no production
notification or heartbeat. It never publishes/creates a production ledger entry.
Simulation, live-provider dry-run, actual deployment and genuine publication are
separate verification claims.

## Rollout and rollback

Keep a backup/hash of original index and durable ledger/queue before migration.
No source JSONL rewriting or destructive schema operation is required. Review and
merge both paired source PRs normally, verify exact remote commits/checks, then
install only changed clean skill paths; preserve unrelated dirty references.
Use established repo deployment and safe primary fast-forward only if unrelated
owner changes cannot conflict; otherwise deployed immutable script copies are
preferable to changing the primary checkout. Record code/skill hashes and host
cron target. Keep the previous scripts/skill files and derived index backup for
rollback; leave new source JSONL and quarantined evidence intact. Do not reset,
force-push, bypass protection or delete owner worktrees/branches. See runbook009
for database-specific backup/restore and explicit historical-unknown semantics.
