#!/usr/bin/env python3
"""Remove <script ...>...</script> blocks from a markdown body before it is cross-posted.

The producer embeds a JSON-LD <script type="application/ld+json"> block in some posts for the
Hugo site (goldmark unsafe=true renders it as structured data). Dev.to and Hashnode do not
execute script tags: they escape them, so the block appeared as a wall of
`&quot;@context&quot;` text at the end of 18 of the latest 60 Dev.to articles (2026-08-12 ..
2026-11-03; bead startaitools-7l2). Cross-posts carry a canonical_url back to the site, which
already emits the schema, so nothing is lost by stripping.

Usage: strip-script-blocks.py < body.md > cleaned.md
Exit 0 always; prints the number of removed blocks on stderr.
"""
from __future__ import annotations

import re
import sys

SCRIPT_BLOCK = re.compile(r"[ \t]*<script\b[^>]*>.*?</script>[ \t]*\n?", re.IGNORECASE | re.DOTALL)


def strip_script_blocks(text: str) -> tuple[str, int]:
    cleaned, count = SCRIPT_BLOCK.subn("", text)
    # Collapse the blank lines a removed block leaves behind (never more than one empty line).
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned, count


def main() -> int:
    body = sys.stdin.read()
    cleaned, count = strip_script_blocks(body)
    sys.stdout.write(cleaned)
    print(f"strip-script-blocks: removed {count} block(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
