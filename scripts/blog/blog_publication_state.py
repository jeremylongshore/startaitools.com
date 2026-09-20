#!/usr/bin/env python3
"""Durable publication handoff and shared ledger/queue transactions.

Thin shim: the implementation lives in the `blogpipe` package beside this file. This
path is what blog-land.sh, blog-posting-packet.sh, the workspace helper's raw-bytes
loaders and six sibling scripts (`import blog_publication_state`) all use, so it stays.
"""

from __future__ import annotations

import sys
from pathlib import Path

# BEFORE the package import: the workspace helper execs this file's bytes precisely so
# that loading it writes no __pycache__ inside a run checkout. Keep that true.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import blogpipe as _blogpipe  # noqa: E402
from blogpipe.errors import PublicationError  # noqa: E402,F401
from blogpipe.frontmatter import *  # noqa: E402,F401,F403
from blogpipe.provenance import publication_helper_sha256  # noqa: E402,F401
from blogpipe.publication import *  # noqa: E402,F401,F403
from blogpipe.publication import main  # noqa: E402
from blogpipe.state import *  # noqa: E402,F401,F403

# `import blogpipe` is cached process-wide. If another checkout's copy is already in
# sys.modules, this shim would silently run ITS logic: refuse a mixed handoff.
if Path(_blogpipe.__file__).resolve().parent.parent != Path(__file__).resolve().parent:
    raise ImportError(
        f"blogpipe resolved from {_blogpipe.__file__}, not beside {__file__}: mixed checkouts"
    )

if __name__ == "__main__":
    sys.exit(main())
