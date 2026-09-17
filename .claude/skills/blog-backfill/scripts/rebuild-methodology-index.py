#!/usr/bin/env python3
"""Build a fully accounted schema-v2 candidate; publish only after validation."""

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = 2
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def fail(message):
    raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(raw):
    return json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_constant=lambda value: fail(f"non-finite JSON: {value}"),
    )


def date(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        fail("expected YYYY-MM-DD")
    dt.date.fromisoformat(value)
    return value


def slug(value):
    if not isinstance(value, str) or not SLUG.fullmatch(value):
        fail("invalid or missing slug")
    return value


def tier(value, nullable=False):
    if value is None and nullable:
        return value
    if type(value) is not int or not 1 <= value <= 4:
        fail("tier must be an integer 1..4")
    return value


def flag(value, nullable=False):
    if value is None and nullable:
        return None
    if type(value) not in (bool, int) or value not in (0, 1):
        fail("flag must be boolean or 0/1")
    return int(value)


def text(value):
    return json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else value


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE).decode(
        "utf-8"
    )


def verified_post(repo, commit, value):
    """Use the committed post, not an untracked/edited working-tree imitation."""
    path = f"content/posts/{slug(value)}.md"
    raw = git(repo, "show", f"{commit}:{path}")
    # These two legacy front-matter formats are the repository's canonical forms.
    lines = raw.splitlines()
    if not lines or lines[0] not in ("+++", "---"):
        fail(f"no front matter in tracked post {path}")
    try:
        end = lines.index(lines[0], 1)
    except ValueError:
        fail(f"unterminated front matter in {path}")
    fm = "\n".join(lines[1:end])
    separator = "=" if lines[0] == "+++" else ":"
    identities = re.findall(
        rf"^slug\s*{separator}\s*['\"]?([a-z0-9-]+)['\"]?\s*$", fm, re.MULTILINE
    )
    dates = re.findall(
        rf"^date\s*{separator}\s*['\"]?(\d{{4}}-\d{{2}}-\d{{2}})[^\n]*$", fm, re.MULTILINE
    )
    if identities != [value] or len(dates) != 1:
        fail(f"ambiguous/mismatched tracked post identity: {path}")
    return (value, "tracked_content", path, digest(raw.encode()), commit, date(dates[0]))


def insert(conn, table, values):
    columns = ",".join(values)
    marks = ",".join("?" for _ in values)
    conn.execute(f"INSERT INTO {table} ({columns}) VALUES ({marks})", tuple(values.values()))


def build(methodology, repo, output, manifest_path=None):
    methodology, repo, output = map(Path, (methodology, repo, output))
    manifest_path = Path(manifest_path or methodology / "legacy-index-migration-v2.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = parse_json(manifest_bytes)
    if manifest.get("schema_version") != VERSION:
        fail("unsupported legacy migration manifest version")
    allowances = {}
    for entry in manifest["entries"]:
        key = (entry["source"], entry["sha256"])
        if key in allowances:
            fail("duplicate migration entry")
        allowances[key] = set(entry["allow"])
    commit = git(repo, "rev-parse", "HEAD").strip()
    snapshots, rows = {}, []
    for name in ("decisions.jsonl", "feedback.jsonl", "patterns.jsonl"):
        path = methodology / name
        if not path.exists():
            fail(f"required source missing: {name}")
        data = path.read_bytes()
        snapshots[path] = data
        for number, raw in enumerate(data.decode("utf-8").splitlines(keepends=True), 1):
            content = raw.rstrip("\r\n")
            try:
                rec = parse_json(content) if content.strip() else None
                if rec is not None and not isinstance(rec, dict):
                    fail("JSON source record must be an object")
            except (ValueError, TypeError) as exc:
                fail(f"{name}:{number}: {exc}")
            rows.append((name, number, raw, digest(content.encode()), rec))
    if not any(r[0] == "decisions.jsonl" and r[4] is not None for r in rows):
        fail("decisions source is empty")

    output.parent.mkdir(parents=True, exist_ok=True)
    with (output.parent / (output.name + ".rebuild.lock")).open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        sidecars = [Path(str(output) + suffix) for suffix in ("-wal", "-shm", "-journal")]
        if any(path.exists() for path in sidecars):
            fail("existing SQLite journal sidecar; stop index writers before rebuilding")
        fd, candidate = tempfile.mkstemp(prefix=f".{output.name}.candidate-", dir=output.parent)
        os.close(fd)
        conn = None
        try:
            conn = sqlite3.connect(candidate)
            conn.executescript((methodology / "rebuild-index.sql").read_text())
            if conn.execute("PRAGMA user_version").fetchone() != (VERSION,):
                fail("candidate schema version differs from helper")
            classified = set()
            summary = {
                "schema_version": VERSION,
                "classifications": 0,
                "feedback": 0,
                "patterns": 0,
                "legacy_unknown_original_tier": 0,
                "legacy_unclassified_feedback": 0,
                "legacy_unlinked_audits": 0,
                "legacy_audit_lists": 0,
            }
            for name, number, raw, sha, rec in rows:
                kind = "blank"
                if rec is not None:
                    try:
                        allowed = allowances.get((name, sha), set())
                        if name == "decisions.jsonl":
                            date(rec.get("date"))
                            if "audit_addendum" in rec and type(rec["audit_addendum"]) is not bool:
                                fail("audit_addendum must be boolean")
                            if "agent_audit" in rec and not isinstance(rec["agent_audit"], dict):
                                if "legacy_audit_list" not in allowed:
                                    fail("agent_audit must be an object")
                                summary["legacy_audit_lists"] += 1
                            if rec.get("audit_addendum") or "tier" not in rec:
                                kind = "auxiliary"
                                if "legacy_audit_list" in allowed:
                                    kind = "legacy_audit_list"
                                if not rec.get("slug"):
                                    if "unlinked_audit" not in allowed or not isinstance(
                                        rec.get("agent_audit"), dict
                                    ):
                                        fail("unlinked audit lacks approved migration provenance")
                                    kind = "legacy_unlinked_audit"
                                    summary["legacy_unlinked_audits"] += 1
                                else:
                                    slug(rec["slug"])
                                    if not any(
                                        k in rec
                                        for k in (
                                            "agent_audit",
                                            "agents_dispatched",
                                            "record_type",
                                            "event",
                                            "publication_status",
                                        )
                                    ):
                                        fail("unrecognized auxiliary decision record")
                            else:
                                kind = "classification"
                                value = slug(rec.get("slug"))
                                if value in classified:
                                    fail(f"duplicate classification slug: {value}")
                                tier(rec.get("tier"))
                                confidence = rec.get("confidence")
                                if (
                                    type(confidence) not in (int, float)
                                    or not math.isfinite(confidence)
                                    or not 0 <= confidence <= 1
                                ):
                                    fail("invalid classification confidence")
                                if (
                                    not isinstance(rec.get("tier_name"), str)
                                    or not rec["tier_name"]
                                ):
                                    fail("missing tier_name")
                                dims, signals = (
                                    rec.get("dimensions", {}),
                                    rec.get("source_signals", {}),
                                )
                                if not isinstance(dims, dict) or not isinstance(signals, dict):
                                    fail("dimensions/source_signals must be objects")
                                for score in dims.values():
                                    if type(score) is not int or not 0 <= score <= 5:
                                        fail("dimension score must be an integer 0..5")
                                insert(
                                    conn,
                                    "post_identities",
                                    {"slug": value, "provenance": "classification"},
                                )
                                values = {
                                    key: rec[key]
                                    for key in ("date", "slug", "tier", "tier_name", "confidence")
                                }
                                values.update(
                                    {
                                        f"dim_{k}": dims.get(k, 0)
                                        for k in ("novelty", "arc", "nar", "tch", "scp", "rpr")
                                    }
                                )
                                values.update(
                                    {
                                        k: text(rec.get(k, ""))
                                        for k in (
                                            "reasoning",
                                            "alternatives_considered",
                                            "thesis_candidate",
                                            "rhetorical_structure",
                                        )
                                    }
                                )
                                values.update(
                                    {
                                        f"sig_{k}": text(signals.get(k, "absent"))
                                        for k in ("git", "prs", "session", "beads", "email")
                                    }
                                )
                                values.update(
                                    {
                                        "cadence_type": rec.get("cadence_type", "daily"),
                                        "anti_inflation_flags": json.dumps(
                                            rec.get("anti_inflation_flags", [])
                                        ),
                                        "applied_patterns": json.dumps(
                                            rec.get("applied_patterns", [])
                                        ),
                                    }
                                )
                                insert(conn, "decisions", values)
                                classified.add(value)
                                summary["classifications"] += 1
                        elif name == "patterns.jsonl":
                            kind = "pattern"
                            if not isinstance(rec.get("pattern_id"), str) or not rec["pattern_id"]:
                                fail("missing pattern_id")
                            date(rec.get("discovered_date"))
                            values = {
                                key: text(rec.get(key, ""))
                                for key in (
                                    "pattern_id",
                                    "name",
                                    "description",
                                    "direction",
                                    "conditions",
                                    "evidence",
                                    "discovered_date",
                                    "last_validated",
                                )
                            }
                            count = rec.get("times_applied", 0)
                            if type(count) is not int or count < 0:
                                fail("invalid pattern times_applied")
                            values.update(
                                {"times_applied": count, "active": flag(rec.get("active", True))}
                            )
                            insert(conn, "patterns", values)
                            summary["patterns"] += 1
                        else:
                            # Feedback is imported after every classification, below.
                            kind = "feedback"
                    except (ValueError, TypeError, KeyError, sqlite3.Error) as exc:
                        fail(f"{name}:{number}: {exc}")
                insert(
                    conn,
                    "source_records",
                    {
                        "source": name,
                        "line_number": number,
                        "raw_line": raw,
                        "sha256": sha,
                        "kind": kind,
                    },
                )

            for name, number, _raw, sha, rec in rows:
                if name != "feedback.jsonl" or rec is None:
                    continue
                try:
                    allowed = allowances.get((name, sha), set())
                    value = slug(rec.get("slug"))
                    original = tier(rec.get("original_tier"), nullable=True)
                    if original is None and "unknown_original_tier" not in allowed:
                        fail("unknown original tier lacks approved migration provenance")
                    status = "classified" if value in classified else "legacy_unclassified"
                    if status == "legacy_unclassified":
                        if "unclassified_post" not in allowed:
                            fail("orphan feedback lacks approved migration provenance")
                        if not conn.execute(
                            "SELECT 1 FROM post_identities WHERE slug=?", (value,)
                        ).fetchone():
                            identity = verified_post(repo, commit, value)
                            conn.execute(
                                "INSERT INTO post_identities VALUES (?,?,?,?,?,?)", identity
                            )
                        summary["legacy_unclassified_feedback"] += 1
                    insert(
                        conn,
                        "feedback",
                        {
                            "slug": value,
                            "date_assessed": date(rec.get("date_assessed")),
                            "original_tier": original,
                            "original_tier_status": "known"
                            if original is not None
                            else "legacy_unknown",
                            "classification_status": status,
                            "source_line": number,
                            "correct_tier": tier(rec.get("correct_tier"), nullable=True),
                            "was_correct": flag(rec.get("was_correct"), nullable=original is None),
                            "reasoning": text(rec.get("reasoning", "")),
                            "year_from_now_useful": flag(
                                rec.get("year_from_now_useful"), nullable=True
                            ),
                            "engagement_data": text(rec.get("engagement_data")),
                        },
                    )
                    summary["feedback"] += 1
                    summary["legacy_unknown_original_tier"] += original is None
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    sqlite3.Error,
                    subprocess.CalledProcessError,
                ) as exc:
                    fail(f"{name}:{number}: {exc}")

            for path, data in snapshots.items():
                source_rows = [r for r in rows if r[0] == path.name]
                insert(
                    conn,
                    "source_accounting",
                    {
                        "source": path.name,
                        "sha256": digest(data),
                        "total_lines": len(source_rows),
                        "json_records": sum(r[4] is not None for r in source_rows),
                        "blank_lines": sum(r[4] is None for r in source_rows),
                    },
                )
            summary["source_lines"] = len(rows)
            for key, value in {
                "summary": json.dumps(summary, sort_keys=True),
                "migration_sha256": digest(manifest_bytes),
                "content_commit": commit,
            }.items():
                insert(conn, "index_metadata", {"key": key, "value": value})
            conn.commit()
            if conn.execute("PRAGMA foreign_key_check").fetchall():
                fail("candidate foreign key check failed")
            if conn.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                fail("candidate integrity check failed")
            conn.close()
            conn = None
            if any(path.read_bytes() != data for path, data in snapshots.items()):
                fail("source changed during rebuild; retry with a consistent snapshot")
            if (
                manifest_path.read_bytes() != manifest_bytes
                or git(repo, "rev-parse", "HEAD").strip() != commit
            ):
                fail("migration/content revision changed during rebuild")
            with open(candidate, "rb") as ready:
                os.fsync(ready.fileno())
            if any(path.exists() for path in sidecars):
                fail("SQLite writer appeared during rebuild; retry after stopping writers")
            os.replace(candidate, output)
            directory = os.open(output.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
            print(json.dumps({"event": "methodology_index_published", **summary}, sort_keys=True))
            return summary
        finally:
            if conn is not None:
                conn.close()
            if os.path.exists(candidate):
                os.unlink(candidate)


def main():
    here = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methodology", type=Path, default=here.parents[1] / "methodology")
    parser.add_argument("--repo", type=Path, default=here.parents[4])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        build(
            args.methodology, args.repo, args.output or args.methodology / "index.db", args.manifest
        )
    except (OSError, ValueError, sqlite3.Error, subprocess.CalledProcessError) as exc:
        print(
            f"ERROR: methodology rebuild failed; no unvalidated index published: {exc}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
