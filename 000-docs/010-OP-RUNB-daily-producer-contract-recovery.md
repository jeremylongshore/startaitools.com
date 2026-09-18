# Daily blog contract, isolated scheduling and recovery

Owner issues #73/#76/#78/#79/#81/#82; methodology migration #74; parent intent-os#619. Source cron
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

Claude2.1.274 may return native `isAsync=true/status=async_launched` even when
the call omitted `run_in_background`. This is dispatch, not completion. The
shared checker waits for a later same-session SDK-origin `task-notification`
with exact original tool call, Agent ID and output-file binding and status
`completed`; its result supplies the actual Agent output and hard-gate receipt.
Quoted notifications, wrong origin/session/IDs, ambiguous fields, pending or
failed/cancelled work cannot attest completion. A later pending invocation
invalidates that Agent's earlier pass. Explicit background launches also require
genuine bound completion. Normal synchronous tool results remain supported.
Read the actual completed result before proceeding; never manufacture notification
or gate text. Launch-only verification and duplicate appends fail without changing
authority. Regression: `tests/test_native_async_agent_completion.py` and the
native verify/duplicate-append cases in `tests/test_blog_producer_contract.py`.

Scoped appends use `blog-producer-contract.py append` with a file lock, fsync,
exact target identity, identical-duplicate no-op and conflicting-duplicate refusal.
Keep classifier/audit candidates staged while the writer, SEO and voice gates can
still change the slug or draft. Only after genuine final gates and Hugo/voice pass,
freeze the final identity, stage the classifier and audit with actual final
post hash/gate receipts, and run `check-staged` with both records and the real
session transcript. Each `append` requires that same complete pair, transcript,
date/slug/run identity and, for manifest-bound production, the actual held producer lease; it revalidates under the
append lock before writing, including duplicate delivery. The helper
rejects a second date/slug within the same run and checks the active manifest's
workspace/date/UUID and final target post before writing. A renamed staged
candidate is harmless; a renamed committed identity stops the run without editing
history. Undispatched mandatory Agents are pending work to execute before authority
writes. Actual BLOCK/REVISE or tool failure remains blocking. Complete required
SEO before freezing metadata and final hard reviews. Normal verification and
preflight both require explicit Boolean `draft=false` and exact slug/date;
missing fields or a quoted false string do not attest publishability.
Build a ready:false sentinel, run `verify --preflight` (all other checks
remain mandatory), then attest ready:true and run normal verification. Preflight
success cannot authorize landing. Any failure retains evidence and fails production.

Global producer instructions come from claude-skills-private PR2/PR3 plus the
publishable-front-matter correction PR5, completion-before-authority PR7,
full-pattern-output preservation PR8 and native async completion-wait PR9.
These paired changes must be deployed with the application
contract. Never invent Agent calls,
readiness or classifiers to clear quarantine. The lander may retain defensive
pattern healing only in the explicit legacy unbound path. Bound runs never
rewrite validated authority: absent/stale true classifier receipts fail. Audit
addenda may also carry tiers, so classifier/pattern/tier selectors exclude them
and match the exact run. Original log warnings remain historical, not replayed
as new results. Preserve the entire actual engine output (including provisional
tier, final tier, evaluated/matched rules and applied_patterns). Shared validation
executes deterministic apply read-only and compares its complete output before
append and normal/preflight completion; it preserves exact numeric/Boolean types and rejects contradictions without repair.

## Checkout retention and capacity

The external registry contains full isolated source trees and Hugo output, not
only small manifests. Admission estimates twice the allocated tracked source plus
a minimum 500 MiB transaction reserve on the registry filesystem. A refusal records
available, required, registry and protected bytes and fails before allocating
another checkout. The existing 500 MiB emergency floor remains separate.

Under canonicalFD9, registry and per-run producer locks, normal creation attempts
verified retirement of completed published/delivered or unchanged no-op checkouts.
Defaults retain two newest eligible checkouts and require 24 hours since latest
completion/publication (`BLOG_WORKSPACE_KEEP_CHECKOUTS`,
`BLOG_WORKSPACE_MIN_AGE_HOURS`). Durable journals and bounded private evidence
archives precede removal; branches, logs, manifests and immutable native quality
proof remain. Clean initialized submodules require Git's specific single-force
checkout-removal guard after complete owned module bytes/history are archived and
reverified. No deinit or general dirty/locked override is allowed. Prepared file
inventories permit only unchanged owned remnants to resume interrupted removal;
unexpected changes remain protected and visible. Inventories include checkout and private Git-admin files/directories and are bounded to16MiB,100,000 entries and8GiB content; evidence archives include actual tar headers/padding within64MiB. No common refs/config are removed. Retirement Git children inherit only the three held canonical/registry/producer lock descriptions, including read-only remote-ref checks. A killed parent cannot release those locks while its Git child still runs; generic calls inherit no unrelated descriptors.

Retirement-only Git runs under canonical `/usr/bin/timeout`: 60 seconds before
TERM, then 5 seconds before group KILL. A Linux child-subreaper keeper retains the
same three leases and reaps descendants even after Git exits successfully; ignored
TERM cannot outlive the external deadline when the Python parent is killed. Parent
capture allows a further 5 seconds for watchdog completion (70 seconds total); no
environment switch disables this bound. Expiration fails closed and leaves the
prepared journal/proof for the next verified retirement. This is a defensive lease
invariant, not a demonstrated production-hang cause.

Quarantined, unfinished publication/delivery, active, dirty, locked or uncertain
local Beads work cannot become eligible merely because the disk is full. Canary
mode performs no retirement. Inspect without changes:

```bash
python3 scripts/blog/blog-run-workspace.py census \
  --repo /home/jeremy/000-projects/blog/startaitools \
  --state-dir "$HOME/.local/state/blog-run-workspaces"
```

The daily summary includes original owner and external run quarantine, total
registry/checkout/protected bytes and retirement reasons. Invalid census fails
overall status and withholds `.ok`. Backup stores and other sessions' work are
outside this cleanup. For restoration, retain the run branch/commit, journal and
evidence archive, verify their hashes and reconstruct into a new isolated path;
never overwrite owner files.

Landing requires a bound manifest, stages only returned publish_paths, uses normal
commit hooks and pushes HEAD explicitly to master after an FF/publication check.
Before commit, the publication helper independently verifies the actual producer
contract and runs bounded Hugo/voice gates. A durable quality seal retains hashes,
trusted native session evidence and readiness outside the workspace. Sealed runs
refuse another producer; publication checks compare exact committed artifacts
against that seal before push. Source publication and delivery completion are
separate persisted states; remote inclusion alone cannot mark delivery complete.
It verifies remote inclusion before later image work. Asset races rebase only unpublished asset commits inside that isolated
run, with bounded attempts and no autostash. An image failure cannot dirty or
diverge the next day's source checkout. Invalid production snapshots run-owned
artifacts into quarantine and retains evidence; no shared decision reset occurs.

Release workflow now depends on the repository's actual reusable scripts-lint
checks. Test failures, tag-push or GitHub-release failures cannot be called success.
A successful source push still requires separate deploy/public and packet evidence.

## Runtime ownership and durable state

| Component / entry point | Trigger / process | Persistent output | Failure signal / recovery |
|---|---|---|---|
| `blog-backfill-daily.sh` | Established daily cron, canonicalFD9 | Date/UUID logs and run manifest | Nonzero overall status, correlated notifications; fresh next-date work remains independent of old delivery failures |
| `blog-run-workspace.py create/run/validate` | Wrapper and producer child | Isolated workspace, bounded run ownership, quarantine | Reject foreign writes; retain abandoned evidence; never reset owner files |
| `blog-producer-contract.py verify/append` | Producer append and wrapper/lander checks | Target-scoped append-only decisions and versioned readiness | Missing/invalid Agent/hash/pattern/schema proof fails before producerOK |
| `blog_publication_state.py seal/reconcile/recover` | Lander before commit and recurring wrapper | External quality proof, source/delivery status, canonical ledger/queue | Changed proof or required write failure remains pending; safe replay preserves latest statuses |
| `blog_consumer_source.py` | Packet/API consumer before generation or dispatch | Private temporary committed post bytes | Missing/changed proof, wrong identity or unavailable authoritative source fails before delivery; never use owner working files |
| `blog_crosspost_dispatch.py dispatch/recover` | Queue consumer with provenFD8 | Dispatch identity/deadline/outcome in queue | Watchdog releases ownership; uncertain acceptance becomes held ambiguous |
| `blog-crosspost-sweep.sh` / queue helper | Existing independent sweep | Sweep logs and retained terminal queue rows | Preserve processor exit; held/failed or due missing source/credentials returns nonzero |
| `blog-posting-packet.sh` | Existing packet sweep/operator send | Packet state in canonical ledger | Required valid ledger first; mark targeted sent status transactionally |
| Methodology schema2 rebuilder | Daily derived-index stage | Atomic SQLite index with all physical source lines | Invalid source/failed publication preserves last-good index and fails overall status |
| `blog-methodology-published-index.py` | Daily wrapper after landing, inherited FD9 | Canonical derived index from authoritative committed snapshots | Published rows must reach the canonical index; unpublished worktree changes cannot; failures preserve last-good DB and owner checkout |
| Existing Actions / VPS forced deploy | Normal master push | Reviewed source, pinned Hugo build, public static files | CI/source success separate from exact public article and delivery success |

## Interrupted publication and delivery

`blog_publication_state.py` recovers only a retained quality-sealed run whose
unchanged artifacts and exact commit are verified against the authoritative
remote. A public article probe must also pass. Ledger and queue transactions use
`.blog-publication-state.lock`, reload the latest rows under a bounded30-second
lock and publish atomically. Existing packet, platform and image statuses are
preserved. Missing required state remains pending/nonzero; source-only reconstruction
is never an automatic recovery mechanism. An old unverifiable delivery run must
remain visibly failed without preventing independent next-date production.

### Published source handoff

The producer deliberately leaves the owner's primary checkout unchanged. Packet
and queue readers must therefore never infer publication from a file at that
checkout's `content/posts/<slug>.md`. Both delivery records now carry a `source`
reference with schema/provenance, published commit, exact path, SHA256, date/run
identity and the quality-seal digest. The same genuine sealed publication creates
both references. Ordinary status updates cannot replace this identity.

`blog_consumer_source.py` locates proof through the configured
`BLOG_RUN_STATE_DIR` (default `~/.local/state/blog-run-workspaces`) and the common
Git-directory hash. It verifies the retained manifest/seal/native-proof hashes,
configured owner/remote, publication ancestry, exact blob and current authoritative
article before materializing a private mode0600 file. It uses no owner working
post and needs no surviving producer worktree. Source reads have a total60-second
Git deadline, individual20-second operations and a1MiB post limit. Temporary
consumer directories are private and cleaned by the calling shell.

Rows from the immediately preceding sealed release may lack `source`. Their
run ID, post digest and exact retained proof can resolve the reference without
fabricating an audit. A normal verified reconciliation can insert only that
missing reference while preserving sent/image/platform statuses. An explicit
invalid reference never falls back. Truly historical rows with no seal identity
use a separate compatibility path reading a regular tracked blob from freshly
verified origin/master; this does not attest historical quality or create any
classification. Untracked imitations, modified owner files, drafts, empty bodies,
symlink blobs and mismatched dates/identities cannot supply content.

Missing proof, remote failure or later article changes stop that delivery and
remain nonzero/visible. Inspect the retained run and original committed content;
never fix this by advancing/resetting the owner checkout, stripping provenance,
or writing a new classifier. Keep retained manifests/quality-proof directories
until their delivery obligations are settled. Partial packet failures may allow
independently valid packets to complete, but the aggregate invocation fails and
only successfully delivered packets are marked sent. An email accepted before a
receipt write fails still needs reconciliation; no exactly-once email claim is
made by this source fix.

### Canonical methodology index

The canonical derived index must reflect published decisions even while the
owner's HEAD stays older. `blog-methodology-published-index.py` reads the three
committed JSONL sources and migration metadata at the freshly verified remote
commit into a bounded private snapshot. A private Git repository references the
existing object store read-only; no producer worktree is registered or normalized.
The existing schema2 validator atomically publishes the canonical index only after
complete validation. The inherited canonical FD9 remains required. Unpublished
or quarantined producer rows are excluded, and a failed snapshot/build preserves
the last-good canonical index. Compare actual canonical counts/source digests,
not an isolated workspace's successful rebuild exit, when verifying recovery. The existing-public-article no-op path also requires successful canonical reconciliation before completing.

The explicit legacy `reconcile-syndication-state.py --apply` manual command is
not part of automatic recovery. Its historical source-only restoration lacks the
new seal/run proof and can admit untracked drafts; do not use it to clear this
incident or claim audited delivery. Preserve existing manual behavior separately
until a reviewed migration defines its trusted historical recovery contract.

The dispatcher requires Linux `/proc/self/fdinfo/8` lock-ownership evidence and
Python3.12 with working pidfd
process ownership. The actual scheduler host was verified with Python3.12.3,
kernel6.8.0-110-generic and successful own-process pidfd signal0. Confirm these
capabilities before moving the worker to another host; workspace recovery also
uses `/proc/locks`. Do not weaken ownership
verification for a portability shortcut.

Crosspost consumers hold `.blog-crosspost-consumer.lock` independently from short
state transactions. Each outbound attempt must persist dispatch identity before
sending and run under an independent bounded watchdog. The selected default is
150seconds for provider execution (`CROSSPOST_PROVIDER_TIMEOUT_SECONDS`, positive
and at most600), plus bounded2-second termination and2-second reap grace. Separate
state transactions each have their own30-second bound and can extend total lease
ownership beyond the provider execution deadline. Connect time defaults to
10 seconds (`CROSSPOST_CONNECT_TIMEOUT_SECONDS`) and request time to 60 seconds
(`CROSSPOST_REQUEST_TIMEOUT_SECONDS`, both integer1..600). A definitive initial
create HTTP429 response uses the explicit rejection protocol and permits at most
five attempts with exponential backoff from15minutes. Generic nonzero, timeout
and5xx outcomes do not qualify as safe rejection. Unknown outcomes and abandoned dispatches
are held as ambiguous rather than blindly resent. A remote accepted request can
outlive its caller; this design does not claim exactly-once external publication.
Resolve ambiguous results against the provider before a separately authorized
retry. Canary mode must refuse imported mutation APIs as well as the CLI; dry-run
consumption remains read-only.

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
python3 -m pytest tests/test_blog_consumer_source.py tests/test_methodology_published_source.py -q
python3 scripts/blog/catalog-audit.py --start 2026-07-16 --end 2026-07-29 --article content/posts/after-14-days-of-daily-posts-here-is-what-i-notice.md
hugo --buildFuture --gc -d /tmp/hugo-verify
python3 scripts/blog/test-blog-contract-replay.py --hugo "$(command -v hugo)" --start-date 2030-12-20 --output-root /tmp/blog-offline-replay
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
separate verification claims. Canary mode skips production heartbeat writes and
posting sweeps even on repeated-date no-ops; replay asserts these boundaries.
Existing-post normal runs require HTTP200 at the requested article URL (a
homepage redirect or missing curl is not success); unavailable existing posts
produce a nonzero result and alert. This availability probe does not prove
byte-for-byte deployed content, which remains separate deployment verification.

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

Before reverting a consumer, stop only that consumer's scheduled invocations and
wait for the bounded outbound watchdog to finish. Snapshot the latest queue and
ledger with all dispatch/ambiguous/published receipts. Never restore an older
queue/ledger backup over real delivery actions: that can resend accepted articles.
Keep the upgraded consumer or hold dispatching/ambiguous records until provider
acceptance is reconciled; historical consumers may treat these states as terminal
and discard their evidence. Derived SQLite rollback is separate and can use the
verified online index backup. Re-enable the consumer only after state compatibility
and the remote delivery outcomes are proved. No periodic restart is remediation.

## Release artifact integrity

The established release workflow runs the reusable repository checks before its
version/changelog steps. Commit rejection is fatal. Before creating a tag, the
workflow verifies clean tracked/index state, exact committed version.txt bytes,
the matching vVERSION tag and the first committed changelog release header.
Dry runs execute this artifact gate too. A failing hook or missing artifact is a
failed release; do not bypass the hook, manufacture outputs, or retag an old HEAD.

Run `python3 -m pytest -q tests/test_blog_release_workflow.py` and actionlint when
changing these steps. The regressions execute actual shell steps with isolated
Git and rejecting hooks; they never create tags, push, or contact GitHub. Owner
issue77 is independent of the original quarantines. Rollback is a reviewed source
revert, preserving all historical tags and persistent delivery state. Existing
best-effort branch push behavior remains visible; separately verify tag ancestry,
release revision and actual deployed revision rather than equating them.

## Publishability and notification boundaries

A completion receipt cannot authorize a draft. Both producer preflight and final
verification refuse a draft flag other than Booleanfalse or YAMLfalse. Producer
instructions must set `draft=false`, requesteddate and exactslug before freezing
postbytes, finalrevision reviews and classifier/audit append. A late manual flag
flip changes the approved hash and cannot repair a completed run. Preserve its
transcript/artifacts; generate a fresh genuinely reviewed run after correcting
the producer. The independent precommit seal remains a separate strict check.

Normal summary and unexpected-exit notification bodies are passed to the private
email sender through `--body-file` in a generated0700 temporary directory with
0600 source permissions. Shell cleanup removes only that directory on sender
success or failure. This avoids per-argument exec limits without truncating or
suppressing incident evidence. Install private sender body-file support BEFORE
this app wrapper; rollback the pair together. SMTP failures remain visible and
summary failure withholds healthy liveness status. A no-send transport verifies
200KiB/1MiB payload hashes and cleanup; it does not prove SMTP acceptance.
