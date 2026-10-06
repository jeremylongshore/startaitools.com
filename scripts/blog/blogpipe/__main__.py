"""`python3 -B -m blogpipe <command> ...` (the -B is load-bearing; see __init__)."""

from __future__ import annotations

import sys

from . import brief, contract, ledger, phrasing, publication, records, schema

COMMANDS = {
    "contract": contract.main,
    "publication": publication.main,
    "brief-readiness": brief.main,
    # Every dated contract switch (brief + record schema); the daily wrapper calls this.
    "contract-readiness": schema.main,
    "tier-ledger": ledger.main,
    "shipped-tier": ledger.append_main,
    # E03: optional search-phrasing record; always exits 0 on content outcomes.
    "search-phrasing": phrasing.main,
    # The enum manifest the skill pins (records.enum_manifest); read-only, exits 0.
    "record-enums": records.manifest_main,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: python3 -B -m blogpipe {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 64
    command = sys.argv.pop(1)
    return COMMANDS[command]()


if __name__ == "__main__":
    sys.exit(main())
