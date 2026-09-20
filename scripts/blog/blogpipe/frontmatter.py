"""Parse a post's TOML or YAML front matter without importing anything heavy.

Shared by the producer contract (publishability checks) and the lander (seal, delivery).
"""

from __future__ import annotations

import re
import tomllib

from .errors import PublicationError


def frontmatter(text: str) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0] not in ("+++", "---") or lines[0] not in lines[1:]:
        raise PublicationError("sealed post needs complete front matter")
    end = lines.index(lines[0], 1)
    if lines[0] == "+++":
        fields = tomllib.loads("\n".join(lines[1:end]))
    else:
        fields = {}
        for line in lines[1:end]:
            match = re.fullmatch(r"(title|slug|draft|date):\s*(.*)", line)
            if match:
                fields[match[1]] = match[2].strip().strip("\"'")
    return fields, "\n".join(lines[end + 1 :])
