"""The versioned slim writer context: what the writer agent is handed, and nothing else.

Blog Recovery Phase I, E01-T05 (startaitools-9a8.1.4, governing contract intent-os
000-docs/228 S05/S08). Before this module the producer filled a 14 KB instruction
template by hand and pasted in the day's whole git log, PR bodies, beads list and the
first 200 lines of several CLAUDE.md files. Nothing recorded which instructions a
writer received, so a change to them could not be tied to the posts it produced.

The writer context is now one versioned file, `scripts/blog/writer-context/
writer-context-vN.md`, rendered deterministically from a small slot object:

    finding (the step 1b brief), sources (only the excerpts that back the
    finding), tier, voice facet, title/slug/date metadata, models and a short
    collaboration note, related posts.

`render` refuses unknown slots, so the context cannot quietly grow back. It writes the
run-scoped record `.blog-staging/DATE.RUNID.writer-context.json` (version, template
hash, brief hash and size, the brief itself) and prints the brief for the Agent call.
The producer copies the record's `audit` object into `agent_audit.writer_context`.

A version is immutable: VERSIONS pins each template's sha256 and a test fails if the
file changes, so an edit means a new file and a new version.

The contract check (`gaps`) is NEW and runs in OBSERVATION mode through the shared dated
switch (blogpipe/switch.py): before WRITER_CONTEXT_ENFORCE_FROM a gap is one
`PRODUCER-CONTRACT: ADVISORY: writer context (...)` line and never a refusal; on and
after it the same gap refuses. `BLOG_WRITER_CONTEXT_ENFORCE_FROM=YYYY-MM-DD|off` moves
or disables the switch without a code change. Every validation also prints one
`PRODUCER-CONTRACT: WRITER-CONTEXT: version=... brief_bytes=...` line: the per-run
manifest of which context version each run used and how large it was.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from .switch import DatedSwitch

CURRENT_VERSION = "writer-context/v1"
# version -> (file name, sha256 of its bytes). Never edit a released file: add v2.
VERSIONS = {
    "writer-context/v1": (
        "writer-context-v1.md",
        "83cbab5b4d84f437921da27822890f426b5b81491ef34fc1354c80efd9b60dc9",
    ),
}
RECORD_SCHEMA = "writer-context-record/v1"
CONTEXT_DIR = Path(__file__).resolve().parent.parent / "writer-context"
STAGING_SUFFIX = "writer-context"

# Proposed: the instructions are live for run date 2026-10-07; seven consecutive
# complete runs fit inside 2026-10-07..2026-10-20 with a week of slack, and the date sits
# after the brief (10-14) and record-schema (10-17) switches so no two flip together.
WRITER_CONTEXT_ENFORCE_FROM = "2026-10-21"
ENFORCE_ENV = "BLOG_WRITER_CONTEXT_ENFORCE_FROM"
SWITCH = DatedSwitch(
    name="writer context",
    label="writer context",
    env=ENFORCE_ENV,
    default=lambda: WRITER_CONTEXT_ENFORCE_FROM,
)

TIERS = {
    1: ("Field Note", "80 to 140 lines", "the Field facet (snark 2, depth 3)"),
    2: ("Technical Deep-Dive", "150 to 250 lines", "the Architect facet (snark 1, depth 5)"),
    3: ("Case Study", "300 to 500 lines", "the Architect facet (snark 1, depth 5)"),
}
REQUIRED = ("tier", "slug", "date", "time", "title", "description", "tags", "category",
            "finding", "sources")
OPTIONAL = ("models_used", "collaboration", "related_posts", "rhetorical_structure")
MAX_SOURCES = 12
MAX_EXCERPT = 2000
MAX_COLLABORATION = 1200
MAX_RELATED = 8
_SLOT = re.compile(r"\{\{([A-Z_]+)\}\}")
_TIER_BLOCK = re.compile(r"<!-- tier (\d) -->\n(.*?)(?=\n<!-- )", re.S)


class SlotError(ValueError):
    """The slot object cannot be rendered; the producer falls back and records why."""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def template_path(version: str = CURRENT_VERSION) -> Path:
    return CONTEXT_DIR / VERSIONS[version][0]


def template_bytes(version: str = CURRENT_VERSION) -> bytes:
    return template_path(version).read_bytes()


def manifest(version: str = CURRENT_VERSION) -> dict[str, Any]:
    data = template_bytes(version)
    return {
        "version": version,
        "template": f"scripts/blog/writer-context/{VERSIONS[version][0]}",
        "template_sha256": _sha(data),
        "template_bytes": len(data),
    }


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _clip(text: str, limit: int) -> tuple[str, bool]:
    text = text.strip()
    if len(text) <= limit:
        return text, False
    return text[:limit].rstrip() + " [truncated]", True


def _slots(raw: Any, workspace: str) -> tuple[dict[str, str], int, int]:
    """Validated slot values, the number of truncations, and the source count."""
    if not isinstance(raw, dict):
        raise SlotError("slots must be a JSON object")
    unknown = sorted(set(raw) - set(REQUIRED) - set(OPTIONAL))
    if unknown:
        raise SlotError(f"unknown slot(s) {', '.join(unknown)}: the writer context is fixed")
    missing = [key for key in REQUIRED if key not in raw]
    if missing:
        raise SlotError(f"missing slot(s) {', '.join(missing)}")
    tier = raw["tier"]
    if type(tier) is not int or tier not in TIERS:
        raise SlotError("tier must be 1, 2 or 3")
    for key in ("slug", "date", "time", "title", "description", "category"):
        if not _text(raw[key]):
            raise SlotError(f"{key} must be a non-empty string")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw["date"]):
        raise SlotError("date must be YYYY-MM-DD")
    if not re.fullmatch(r"\d{2}:\d{2}:\d{2}", raw["time"]):
        raise SlotError("time must be HH:MM:SS")
    tags = raw["tags"]
    if not isinstance(tags, list) or not tags or not all(_text(t) for t in tags):
        raise SlotError("tags must be a non-empty list of strings")
    if not isinstance(raw["finding"], dict) or not _text(raw["finding"].get("sentence")):
        raise SlotError("finding must be the step 1b brief object with a sentence")
    sources = raw["sources"]
    if not isinstance(sources, list) or not sources:
        raise SlotError("sources must be a non-empty list of {ref, excerpt}")
    truncated = 0
    lines = []
    for item in sources[:MAX_SOURCES]:
        if not isinstance(item, dict) or set(item) != {"ref", "excerpt"}:
            raise SlotError("each source is exactly {ref, excerpt}")
        if not _text(item["ref"]) or not _text(item["excerpt"]):
            raise SlotError("each source needs a non-empty ref and excerpt")
        excerpt, cut = _clip(item["excerpt"], MAX_EXCERPT)
        truncated += cut
        lines.append(f"--- {item['ref'].strip()} ---\n{excerpt}")
    truncated += max(0, len(sources) - MAX_SOURCES)
    collaboration, cut = _clip(str(raw.get("collaboration") or ""), MAX_COLLABORATION)
    truncated += cut
    related = raw.get("related_posts") or []
    if not isinstance(related, list) or not all(
        isinstance(r, dict) and set(r) == {"slug", "summary"} and _text(r["slug"])
        for r in related
    ):
        raise SlotError("related_posts must be a list of {slug, summary}")
    truncated += max(0, len(related) - MAX_RELATED)
    name, target, facet = TIERS[tier]
    values = {
        "TIER": str(tier),
        "TIER_NAME": name,
        "TIER_TARGET": target,
        "VOICE_FACET": facet,
        "WORKSPACE": workspace,
        "SLUG": raw["slug"].strip(),
        "DATE": raw["date"],
        "TIME": raw["time"],
        "TITLE": raw["title"].strip().replace("'", "’"),
        "DESCRIPTION": raw["description"].strip().replace('"', "'"),
        "TAGS": json.dumps([t.strip() for t in tags], ensure_ascii=False),
        "CATEGORY": raw["category"].strip(),
        "FINDING_JSON": json.dumps(raw["finding"], ensure_ascii=False, indent=2, sort_keys=True),
        "SOURCES": "\n\n".join(lines),
        "MODELS_USED": str(raw.get("models_used") or "none recorded").strip(),
        "COLLABORATION": collaboration or "(none)",
        "RELATED_POSTS": "\n".join(
            f"- {r['slug'].strip()}: {str(r['summary']).strip()}" for r in related[:MAX_RELATED]
        ) or "(none)",
        "RHETORICAL_STRUCTURE": str(raw.get("rhetorical_structure") or "as classified").strip(),
    }
    return values, truncated, len(lines)


def render(raw: Any, workspace: str, version: str = CURRENT_VERSION) -> tuple[str, dict]:
    """(brief, stats). Pure: same slots and template bytes give the same brief."""
    template = template_bytes(version).decode("utf-8")
    values, truncated, sources = _slots(raw, workspace)
    body, _, tail = template.partition("<!-- tier 1 -->")
    blocks = {int(n): text.strip() for n, text in _TIER_BLOCK.findall("<!-- tier 1 -->" + tail)}
    values["TIER_STRUCTURE"] = blocks[int(values["TIER"])]

    def fill(match: re.Match[str]) -> str:
        return values[match.group(1)]

    # Two passes: the tier block itself carries {{RHETORICAL_STRUCTURE}}.
    brief = _SLOT.sub(fill, _SLOT.sub(fill, body)).rstrip() + "\n"
    left = sorted(set(_SLOT.findall(brief)))
    if left:
        raise SlotError(f"unfilled slot(s) {', '.join(left)}")
    return brief, {"sources": sources, "truncated": truncated}


def staged_path(repo: Path, date: str, run_id: str) -> Path:
    return repo / ".blog-staging" / f"{date}.{run_id}.{STAGING_SUFFIX}.json"


def build_record(brief: str, stats: dict, date: str, run_id: str, slug: str, tier: int) -> dict:
    data = brief.encode("utf-8")
    audit = {
        "version": CURRENT_VERSION,
        "template_sha256": _sha(template_bytes()),
        "brief_sha256": _sha(data),
        "brief_bytes": len(data),
    }
    return {
        "schema": RECORD_SCHEMA,
        "date": date,
        "run_id": run_id,
        "slug": slug,
        "tier": tier,
        **audit,
        "sources": stats["sources"],
        "truncated": stats["truncated"],
        "audit": audit,
        "brief": brief,
    }


# --- contract side ---------------------------------------------------------------


def gaps(repo: Path, identity: dict[str, Any], audit: dict[str, Any]) -> list[str]:
    """Name every way the run's writer-context record is missing or inconsistent."""
    ctx = audit.get("writer_context")
    if not isinstance(ctx, dict):
        return ["agent_audit.writer_context"]
    version = ctx.get("version")
    if version != CURRENT_VERSION:
        return [f"agent_audit.writer_context.version (got {str(version)[:40]!r}; "
                f"current {CURRENT_VERSION})"]
    found = []
    if ctx.get("template_sha256") != VERSIONS[version][1]:
        found.append("agent_audit.writer_context.template_sha256 (not the pinned template)")
    path = staged_path(repo, str(identity["date"]), str(identity["run_id"]))
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return found + [f"staged {path.name}"]
    brief = record.get("brief") if isinstance(record, dict) else None
    if not isinstance(brief, str):
        return found + [f"staged {path.name} (no brief)"]
    data = brief.encode("utf-8")
    if (
        record.get("version") != version
        or ctx.get("brief_sha256") != _sha(data)
        or ctx.get("brief_bytes") != len(data)
    ):
        found.append("agent_audit.writer_context (does not match the staged brief)")
    return found


def report(repo: Path, identity: dict[str, Any], audit: dict[str, Any]) -> list[str]:
    """Print the per-run context line and the switch's advisory line; return the gaps."""
    found = gaps(repo, identity, audit)
    ctx = audit.get("writer_context") if isinstance(audit.get("writer_context"), dict) else {}
    size = ctx.get("brief_bytes")
    print(
        f"PRODUCER-CONTRACT: WRITER-CONTEXT: version={ctx.get('version') or 'none'} "
        f"brief_bytes={size if type(size) is int else 'unknown'}",
        file=sys.stderr,
    )
    SWITCH.report(str(identity["date"]), found)
    return found


def enforced(date: str) -> bool:
    return SWITCH.enforced(date)


# --- CLI -------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python3 -B -m blogpipe writer-context",
        description="Render the versioned slim writer brief, or print the template manifest.",
    )
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("manifest", help="print the current version, template path, hash and size")
    r = sub.add_parser("render", help="render the brief and write the run-scoped record")
    r.add_argument("--slots", required=True, help="JSON file holding the slot object")
    r.add_argument("--run-id", required=True)
    r.add_argument("--repo", default=os.environ.get("BLOG_REPO_DIR") or ".",
                   help="the run workspace (default $BLOG_REPO_DIR)")
    args = ap.parse_args(argv)
    if args.command == "manifest":
        json.dump(manifest(), sys.stdout, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    repo = Path(args.repo).resolve()
    try:
        raw = json.loads(Path(args.slots).read_text(encoding="utf-8"))
        brief, stats = render(raw, str(repo))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, SlotError) as exc:
        print(f"WRITER-CONTEXT: REFUSED: {exc}", file=sys.stderr)
        return 2
    record = build_record(brief, stats, raw["date"], args.run_id, raw["slug"].strip(), raw["tier"])
    out = staged_path(repo, raw["date"], args.run_id)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Written in place: a stray temp name would fail the workspace's staging-name rule.
    out.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    sys.stdout.write(brief)
    print(f"WRITER-CONTEXT: {json.dumps(record['audit'], sort_keys=True)}", file=sys.stderr)
    return 0
