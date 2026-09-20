"""`python3 -B -m blogpipe <command> ...` (the -B is load-bearing; see __init__)."""

from __future__ import annotations

import sys

from . import contract, publication

COMMANDS = {"contract": contract.main, "publication": publication.main}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: python3 -B -m blogpipe {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 64
    command = sys.argv.pop(1)
    return COMMANDS[command]()


if __name__ == "__main__":
    sys.exit(main())
