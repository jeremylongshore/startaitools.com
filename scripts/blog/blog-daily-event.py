#!/usr/bin/env python3
"""Fixed blog-daily entrypoint; install beside Intent OS activity_spool.py."""

from activity_spool import main

if __name__ == "__main__":
    raise SystemExit(
        main(
            "blog-daily",
            {
                "published": "published",
                "pending": "pending",
                "failed": "failed",
                "nothing_due": "nothing_due",
            },
            deduplicate=True,
        )
    )
