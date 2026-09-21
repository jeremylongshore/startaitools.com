#!/usr/bin/env python3
"""Plan and record catch-up of recent dates that still have no post.

Thin shim over blogpipe.catchup so blog-backfill-daily.sh has a stable script path.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from blogpipe.catchup import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
