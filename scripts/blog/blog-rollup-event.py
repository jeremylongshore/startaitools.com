#!/usr/bin/env python3
"""Fixed blog-rollup entrypoint; install beside Intent OS activity_spool.py."""

from activity_spool import main

if __name__ == "__main__":
    raise SystemExit(main("blog-rollup", {"sent": "sent"}, deduplicate=True))
