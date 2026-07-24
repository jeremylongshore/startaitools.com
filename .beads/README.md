# Beads Issue Tracking

This repository uses [Beads](https://github.com/steveyegge/beads) (`bd`) with an embedded Dolt database.

## Source of truth

- Issue state and history live in the local embedded Dolt store (`.beads/embeddeddolt/` in the current installation).
- `bd dolt pull` and `bd dolt push` synchronize that history through `refs/dolt/data` on the repository's configured Git remote.
- `.beads/issues.jsonl` is a passive recovery/interchange export. It is intentionally ignored by Git and must not be treated as the database.
- `.beads/backup/` provides local rolling backups; it does not replace remote synchronization.

## Daily workflow

```bash
bd prime                 # Full workflow for the installed bd version
bd ready                 # Find unblocked work
bd show <id>             # Read issue details
bd update <id> --claim   # Claim an issue
bd create "Title" --description "Context" --acceptance "Done when..."
bd close <id>            # Mark completed work done
```

At the start of a session, run `bd dolt pull`. At the end, update issue status and run `bd dolt pull` followed by `bd dolt push` before pushing the normal Git branch.

## Verification and maintenance

```bash
bd dolt remote list      # Confirm the issue-history remote
bd dolt status           # Inspect local Dolt state
bd backup status         # Inspect local backup health
bd hooks list            # Confirm Git hooks are installed
bd lint                  # Check issue templates and metadata
```

Do not use the retired `bd sync` command or the old SQLite/JSONL workflow. See `AGENTS.md` for this repository's mandatory session-completion protocol.
