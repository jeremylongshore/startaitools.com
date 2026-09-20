"""Which bytes decided a publication: one digest over the verifier's whole source.

The quality seal records this as `verifier_sha256`. While the contract was a single
file, hashing that file was enough. It is now a shim plus this package, and hashing the
shim alone would record a constant that never moves when the real logic changes.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
SHIM = PACKAGE.parent / "blog-producer-contract.py"


def verifier_sources() -> list[Path]:
    """The shim and every module of this package, in a stable order."""
    return [SHIM, *sorted(PACKAGE.rglob("*.py"))]


def verifier_sha256() -> str:
    """Name-framed so moving bytes between files cannot leave the digest unchanged."""
    digest = hashlib.sha256()
    for path in verifier_sources():
        digest.update(path.relative_to(PACKAGE.parent).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()
