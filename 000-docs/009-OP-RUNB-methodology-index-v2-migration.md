# Methodology index v2: atomic rebuild and historical provenance

The append-only `decisions.jsonl`, `feedback.jsonl`, and `patterns.jsonl` remain
unchanged. The SQLite index is derived state. Schema v2 replaces the previous
rebuild that deleted the last-good database, skipped invalid feedback, and printed
success despite missing source records. Owner incident: GitHub issue #74; producer integration #73.

## Migration and honest unknowns

`legacy-index-migration-v2.json` is an explicit, reviewed migration manifest.
Each exception is limited to the exact SHA-256 of one historical source line;
its source name, original line number, and introducing commit are recorded.
Reordering the source does not change permission; editing or appending a new
malformed record does not inherit permission. Expanding this manifest requires a
separate provenance review. Missing original tiers are never guessed.

The September 17 baseline contains 243 classifications, 243 feedback records,
three patterns, and 612 physical source lines. Seven feedback records imported
in commit `6ac16a49` lack both the original tier and correctness assessment. They
remain SQL `NULL`, with `original_tier_status=legacy_unknown`. Eight feedback
records lack a primary classifier and are labeled
`classification_status=legacy_unclassified`. The eighth is the genuine tracked
post `sealing-a-168-bead-planning-graph-took-three-reviews-and-a-seven-seat-council`
(first feedback in `608b7bae`). Its current title differs from its slug; title
matching would be incorrect.

Unclassified feedback references `post_identities`, verified from the committed
`content/posts/SLUG.md` at the captured Git HEAD: front-matter slug, filename, and
publication date must be unambiguous. The index records content path, SHA-256,
and commit. Working-tree or untracked imitations cannot establish identity.
The evidence proves a content identity, not that any absent classifier ran.
No synthetic classifier, confidence, tier, or agent verdict is generated.

Ten historical audit addenda lack slug identity. Their exact hashes are allowed
only as `legacy_unlinked_audit` source records; their identity is not inferred
from date or adjacent records. They cannot attest a current producer run.
Eight additional historical list-shaped audits have exact-hash permissions and
are counted separately as `legacy_audit_lists`; they also cannot attest a current
producer run. Other recognized historical auxiliary decision records remain source records,
not classifications. The producer/lander completion contract is independently
strict and is not relaxed by these analytics migration exceptions.

`source_records` retains every physical source line, including blanks and line
terminators, with source/line/digest/kind. `source_accounting` records complete
file digests and JSON/blank/total counts. `index_metadata` records schema version,
manifest digest, captured content commit, and summary counts. Calibration views
include only actual classifiers joined to known matching original tiers;
unclassified feedback is excluded rather than assigned an invented tier.
`v_legacy_unclassified` makes those exclusions queryable.

## Offline verification

From the repository root:

```bash
python3 -m pytest tests/test_methodology_index.py -q
ruff check .claude/skills/blog-backfill/scripts/rebuild-methodology-index.py tests/test_methodology_index.py
shellcheck -S style .claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh
```

To inspect an isolated candidate without changing the canonical index:

```bash
scratch_index=$(mktemp -d)
.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh --output "$scratch_index/index.db"
sqlite3 "$scratch_index/index.db" 'PRAGMA user_version; PRAGMA integrity_check; PRAGMA foreign_key_check; SELECT * FROM v_legacy_unclassified;'
```

The helper uses Python's SQLite library and Unix `flock`; `sqlite3` CLI is only
needed for the optional inspection command. Read-only Git access is required to
capture and verify committed legacy post identity. No network or credentials
are needed.

## Rebuild, recovery, and rollback

The established entry point remains
`.claude/skills/blog-backfill/scripts/rebuild-methodology-index.sh`.
It produces a JSON `methodology_index_published` receipt containing counts only
after a successful validated replacement. Any missing/malformed source,
non-finite or ambiguous JSON, unapproved exception, duplicate classifier,
invalid constraint, or source/revision change aborts the candidate. Such errors
retain the prior index byte-for-byte and return nonzero with source/line context.
No source line is silently skipped.

Rebuilds use a nonblocking per-output file lock. The lock file is persistent;
the kernel releases the actual lock on process exit, including crashes. Do not
delete a lock file to bypass a running rebuild. Reattempt after the owner exits.
Publication creates a candidate in the destination directory, commits and checks
SQLite integrity/foreign keys, rechecks source snapshots and Git revision,
fsyncs the file, atomically replaces the index, then fsyncs the directory.
Interrupted pre-publication work leaves the previous index in place; retrying
builds a new candidate. Crash leftovers named `.index.db.candidate-*` are derived
scratch state and may be removed only after confirming no rebuild owns the lock.

No other process may write the derived index. Ordinary read-only queries can
continue against the old inode while publication replaces it. Existing SQLite
WAL/SHM/journal sidecars block publication; stop the writer and close/checkpoint
its database safely before retrying. Never delete its journal to force a pass.
Consumers must reopen connections to observe a newly published index.

Before a production rebuild, retain a copy of the previous index and deploy the
matching helper, schema, and manifest together. Rollback stops rebuild writers,
restores that saved derived database atomically, and restores the prior code.
The JSONL source remains intact throughout. Running the old rebuilder is not a
safe rollback: it reintroduces destructive partial rebuilding and loses the
legacy feedback. A directory fsync error after replacement is a durability
failure requiring inspection; it does not mean an invalid candidate was
published or that the previous inode is still canonical.

The offline migration verifies historical accounting and recovery logic. It
does not prove a future unattended producer completed or a post was published.
