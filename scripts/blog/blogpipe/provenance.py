"""Which bytes decided a publication: digests over an entry point plus this whole package.

The quality seal records `verifier_sha256` and `publication_helper_sha256`. While each
was a single file, hashing that file was enough. Each is now a shim over this package,
and hashing the shim alone would record a constant that never moves when the real
logic changes.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
SHIM = PACKAGE.parent / "blog-producer-contract.py"
PUBLICATION_SHIM = PACKAGE.parent / "blog_publication_state.py"


def sources(shim: Path) -> list[Path]:
    """One entry-point shim and every module of this package, in a stable order."""
    return [shim, *sorted(PACKAGE.rglob("*.py"))]


def digest(shim: Path) -> str:
    """Name-framed so moving bytes between files cannot leave the digest unchanged."""
    value = hashlib.sha256()
    for path in sources(shim):
        value.update(path.relative_to(PACKAGE.parent).as_posix().encode() + b"\0")
        value.update(path.read_bytes() + b"\0")
    return value.hexdigest()


def verifier_sources() -> list[Path]:
    return sources(SHIM)


def verifier_sha256() -> str:
    return digest(SHIM)


def publication_helper_sha256() -> str:
    return digest(PUBLICATION_SHIM)
