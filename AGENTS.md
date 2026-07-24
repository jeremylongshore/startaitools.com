# Agent Instructions

This project uses **bd (Beads)** for all task tracking. Run `bd prime` at the start of each session; its generated guidance is authoritative for the installed CLI.

## Quick Reference

```bash
bd ready                 # Find available work
bd show <id>             # View issue details
bd update <id> --claim   # Claim work atomically
bd close <id>            # Complete work
bd dolt pull             # Pull issue history from the configured Dolt remote
bd dolt push             # Push issue history to the configured Dolt remote
```

## Rules

- Use `bd` for all task tracking; do not create markdown TODO lists or memory files.
- Use `bd remember` for durable project knowledge.
- Issues live in the local embedded Dolt database. The configured Git remote stores that history under `refs/dolt/data`.
- `.beads/issues.jsonl` is a passive, ignored export—not the source of truth and not a file to commit.

## Landing the Plane

When ending a work session, complete every step below. Work is not complete until both Beads history and Git changes are pushed successfully.

1. File Beads issues for remaining work.
2. Run relevant tests, linters, and builds when code or content changed.
3. Close finished issues and update any continuing issue.
4. Synchronize and push:

   ```bash
   bd dolt pull
   bd dolt push
   git pull --rebase
   git push
   git status --branch --short
   ```

5. Clear obsolete stashes and prune stale remote branches when safe.
6. Verify all intended changes are committed, `bd dolt push` succeeds, and Git reports the branch up to date with its upstream.
7. Hand off remaining context through Beads.

If either push fails, resolve the failure and retry. Never leave completed work stranded locally.
