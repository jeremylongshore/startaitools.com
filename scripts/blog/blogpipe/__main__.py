"""`python3 -B -m blogpipe <command> ...` (the -B is load-bearing; see __init__)."""

from __future__ import annotations

import sys

from . import (
    brief,
    contract,
    ledger,
    phrasing,
    phrasing_cost,
    publication,
    records,
    roles,
    schema,
    writer,
)

COMMANDS = {
    "contract": contract.main,
    "publication": publication.main,
    "brief-readiness": brief.main,
    # Every dated contract switch (brief, record schema, writer context); the daily
    # wrapper calls this.
    "contract-readiness": schema.main,
    "tier-ledger": ledger.main,
    "shipped-tier": ledger.append_main,
    # E03: optional search-phrasing record; always exits 0 on content outcomes.
    "search-phrasing": phrasing.main,
    # E03-T05: tokens, wall time and tool calls of the search-phrasing subagent.
    "search-phrasing-cost": phrasing_cost.main,
    # E01-T05: render the versioned slim writer brief, or print its manifest.
    "writer-context": writer.main,
    # The enum manifest the skill pins (records.enum_manifest); read-only, exits 0.
    "record-enums": records.manifest_main,
    # Who must run / PASS per tier (roles.role_manifest); the skill's gate table pins it.
    "required-roles": roles.manifest_main,
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(f"usage: python3 -B -m blogpipe {{{'|'.join(COMMANDS)}}} ...", file=sys.stderr)
        return 64
    command = sys.argv.pop(1)
    return COMMANDS[command]()


if __name__ == "__main__":
    sys.exit(main())
