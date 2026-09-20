#!/usr/bin/env python3
"""Validate scoped blog production; process exit alone is never completion.

Thin shim: the implementation lives in the `blogpipe` package beside this file. This
path is what cron, blog-backfill-daily.sh, blog-land.sh, the producer instructions and
blog_publication_state.module("blog-producer-contract") all use, so it stays.
"""

from __future__ import annotations

import sys
from pathlib import Path

# BEFORE the package import: this runs inside the isolated run workspace, where a
# written __pycache__ is a change outside the run write-set and fails the run.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import blogpipe as _blogpipe  # noqa: E402
from blogpipe.contract import *  # noqa: E402,F401,F403
from blogpipe.contract import main  # noqa: E402
from blogpipe.errors import ContractError  # noqa: E402,F401
from blogpipe.jsonio import *  # noqa: E402,F401,F403
from blogpipe.provenance import verifier_sha256, verifier_sources  # noqa: E402,F401
from blogpipe.roles import *  # noqa: E402,F401,F403
from blogpipe.transcript import *  # noqa: E402,F401,F403

# `import blogpipe` is cached process-wide. If another checkout's copy is already in
# sys.modules, this shim would silently run ITS logic: refuse a mixed contract.
if Path(_blogpipe.__file__).resolve().parent.parent != Path(__file__).resolve().parent:
    raise ImportError(
        f"blogpipe resolved from {_blogpipe.__file__}, not beside {__file__}: mixed checkouts"
    )

if __name__ == "__main__":
    sys.exit(main())
