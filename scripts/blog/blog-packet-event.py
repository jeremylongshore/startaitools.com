#!/usr/bin/env python3
"""Fixed blog-packet entrypoint; install beside Intent OS activity_spool.py."""

from activity_spool import main

if __name__ == "__main__":
    raise SystemExit(
        main("blog-packet", {"sent": "sent", "nothing_due": "nothing_due"}, deduplicate=True)
    )
