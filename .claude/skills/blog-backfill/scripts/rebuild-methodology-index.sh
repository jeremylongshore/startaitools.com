#!/usr/bin/env bash
# Atomic, accounted rebuild; sources remain untouched and failures retain last-good.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$SKILL_DIR/scripts/rebuild-methodology-index.py" "$@"
