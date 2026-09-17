"""Offline atomic migration regressions; never rebuild the owner's live index."""

import hashlib
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
METH = ROOT / ".claude/skills/blog-backfill/methodology"
SPEC = importlib.util.spec_from_file_location(
    "methodology_index", METH.parent / "scripts/rebuild-methodology-index.py"
)
INDEX = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INDEX)
CLASSIFIER = {
    "date": "2026-09-12",
    "slug": "fixture-post",
    "tier": 1,
    "tier_name": "Field Note",
    "confidence": 0.8,
}


@pytest.fixture
def source(tmp_path):
    meth = tmp_path / "methodology"
    meth.mkdir()
    (meth / "rebuild-index.sql").write_bytes((METH / "rebuild-index.sql").read_bytes())
    (meth / "decisions.jsonl").write_text(json.dumps(CLASSIFIER) + "\n")
    for name in ("feedback", "patterns"):
        (meth / (name + ".jsonl")).write_text("")
    (meth / "legacy-index-migration-v2.json").write_text(
        json.dumps({"schema_version": 2, "entries": []})
    )
    return meth, tmp_path / "index.db"


def run(source):
    meth, output = source
    return INDEX.build(meth, ROOT, output)


def append(meth, name, rec):
    with (meth / (name + ".jsonl")).open("a") as stream:
        stream.write(json.dumps(rec) + "\n")


def feedback(**updates):
    return {
        "date_assessed": "2026-09-13",
        "slug": "fixture-post",
        "original_tier": 1,
        "correct_tier": None,
        "was_correct": 1,
        **updates,
    }


def test_repeat_rebuild_idempotent_and_full_line_roundtrip(source):
    meth, output = source
    append(meth, "feedback", feedback())
    with (meth / "decisions.jsonl").open("a") as stream:
        stream.write("\n")
    first = run(source)
    with sqlite3.connect(output) as db:
        rows = db.execute("SELECT source,line_number,raw_line FROM source_records").fetchall()
        for name in ("decisions.jsonl", "feedback.jsonl", "patterns.jsonl"):
            actual = "".join(raw for src, _number, raw in rows if src == name)
            assert actual.encode() == (meth / name).read_bytes()
        assert db.execute("PRAGMA user_version").fetchone() == (2,)
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
    assert run(source) == first
    assert first["source_lines"] == 3


@pytest.mark.parametrize("name", ["decisions", "feedback", "patterns"])
def test_malformed_json_keeps_last_good_for_every_source(source, name):
    meth, output = source
    run(source)
    before = output.read_bytes()
    with (meth / (name + ".jsonl")).open("a") as stream:
        stream.write("{broken\n")
    with pytest.raises(ValueError, match="Expecting"):
        run(source)
    assert output.read_bytes() == before
    assert list(output.parent.glob(".index.db.candidate-*")) == []


@pytest.mark.parametrize(
    "rec", [feedback(original_tier=None, was_correct=None), feedback(slug="unregistered-orphan")]
)
def test_new_unknown_or_orphan_records_fail_closed(source, rec):
    meth, output = source
    run(source)
    before = output.read_bytes()
    append(meth, "feedback", rec)
    with pytest.raises(ValueError, match="approved migration provenance"):
        run(source)
    assert output.read_bytes() == before


def test_new_unlinked_audit_not_grandfathered(source):
    meth, _output = source
    append(
        meth,
        "decisions",
        {"date": "2026-09-16", "audit_addendum": True, "agent_audit": {"writer": "claimed"}},
    )
    with pytest.raises(ValueError, match="unlinked audit"):
        run(source)


def test_actual_legacy_migration_retains_seven_unknowns_and_eighth_orphan(tmp_path):
    output = tmp_path / "actual.db"
    before = {p.name: p.read_bytes() for p in METH.glob("*.jsonl")}
    summary = INDEX.build(METH, ROOT, output)
    assert summary["legacy_unknown_original_tier"] == 7
    assert summary["legacy_unclassified_feedback"] == 8
    assert summary["legacy_unlinked_audits"] == 10
    assert summary["legacy_audit_lists"] == 8
    with sqlite3.connect(output) as db:
        expected_feedback = len([x for x in before["feedback.jsonl"].splitlines() if x.strip()])
        assert db.execute("SELECT COUNT(*) FROM feedback").fetchone() == (expected_feedback,)
        assert db.execute(
            "SELECT COUNT(*) FROM feedback WHERE original_tier IS NULL"
        ).fetchone() == (7,)
        assert db.execute("SELECT COUNT(*) FROM feedback WHERE was_correct IS NULL").fetchone() == (
            7,
        )
        target = "sealing-a-168-bead-planning-graph-took-three-reviews-and-a-seven-seat-council"
        assert db.execute("SELECT COUNT(*) FROM decisions WHERE slug=?", (target,)).fetchone() == (
            0,
        )
        identity = db.execute(
            "SELECT provenance,content_path,content_sha256 FROM post_identities WHERE slug=?",
            (target,),
        ).fetchone()
        assert identity[0] == "tracked_content"
        assert identity[1] == f"content/posts/{target}.md"
        assert len(identity[2]) == 64
        assert db.execute("PRAGMA foreign_key_check").fetchall() == []
        assert (
            db.execute("SELECT COUNT(*) FROM source_records").fetchone()[0]
            == summary["source_lines"]
        )
    assert before == {p.name: p.read_bytes() for p in METH.glob("*.jsonl")}


def test_old_schema_reproduces_null_and_orphan_rejections(tmp_path):
    # The old NOT NULL/FK contract cannot represent these genuine legacy sources.
    with sqlite3.connect(tmp_path / "old.db") as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript(
            "CREATE TABLE decisions(slug TEXT UNIQUE);"
            "CREATE TABLE feedback(slug TEXT REFERENCES decisions(slug),"
            "original_tier INTEGER NOT NULL);"
        )
        db.execute("INSERT INTO decisions VALUES('fixture-post')")
        with pytest.raises(sqlite3.IntegrityError, match="NOT NULL"):
            db.execute("INSERT INTO feedback VALUES('fixture-post', NULL)")
        with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
            db.execute("INSERT INTO feedback VALUES('tracked-but-unclassified', 2)")


@pytest.mark.parametrize(
    "raw", ['{"date":"2026-09-12","date":"2026-09-13"}\n', '{"confidence":NaN}\n', "[]\n"]
)
def test_ambiguous_nonfinite_and_nonobject_json_rejected(source, raw):
    meth, _output = source
    (meth / "feedback.jsonl").write_text(raw)
    with pytest.raises(ValueError):
        run(source)


def test_source_change_during_build_keeps_last_good(source, monkeypatch):
    meth, output = source
    run(source)
    before = output.read_bytes()
    original = INDEX.insert

    def race(db, table, values):
        original(db, table, values)
        if table == "index_metadata":
            (meth / "feedback.jsonl").write_text("\n")

    monkeypatch.setattr(INDEX, "insert", race)
    with pytest.raises(ValueError, match="source changed"):
        run(source)
    assert output.read_bytes() == before


def test_publication_failure_keeps_last_good(source, monkeypatch):
    _meth, output = source
    run(source)
    before = output.read_bytes()

    def unavailable(_source, _destination):
        raise OSError("injected publication failure")

    monkeypatch.setattr(INDEX.os, "replace", unavailable)
    with pytest.raises(OSError, match="publication failure"):
        run(source)
    assert output.read_bytes() == before
    assert list(output.parent.glob(".index.db.candidate-*")) == []


def test_approved_orphan_requires_real_matching_tracked_content(source):
    meth, _output = source
    rec = feedback(slug="untracked-orphan")
    append(meth, "feedback", rec)
    raw = (meth / "feedback.jsonl").read_text().strip()
    (meth / "legacy-index-migration-v2.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "entries": [
                    {
                        "source": "feedback.jsonl",
                        "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                        "allow": ["unclassified_post"],
                    }
                ],
            }
        )
    )
    with pytest.raises(ValueError, match="feedback.jsonl:1"):
        run(source)


@pytest.mark.parametrize("suffix", ["-wal", "-shm", "-journal"])
def test_existing_sqlite_sidecar_keeps_last_good(source, suffix):
    _meth, output = source
    run(source)
    before = output.read_bytes()
    Path(str(output) + suffix).write_bytes(b"active SQLite writer")
    with pytest.raises(ValueError, match="sidecar"):
        run(source)
    assert output.read_bytes() == before


def test_schema_version_mismatch_keeps_last_good(source):
    meth, output = source
    run(source)
    before = output.read_bytes()
    schema = meth / "rebuild-index.sql"
    schema.write_text(schema.read_text().replace("user_version = 2", "user_version = 1"))
    with pytest.raises(ValueError, match="schema version"):
        run(source)
    assert output.read_bytes() == before


def test_new_duplicate_classifier_cannot_overwrite_source(source):
    meth, output = source
    run(source)
    before = output.read_bytes()
    append(meth, "decisions", {**CLASSIFIER, "tier": 2})
    with pytest.raises(ValueError, match="duplicate classification"):
        run(source)
    assert output.read_bytes() == before


def test_migration_hash_cannot_authorize_changed_legacy_record(source):
    meth, output = source
    run(source)
    before = output.read_bytes()
    rec = feedback(original_tier=None, was_correct=None)
    append(meth, "feedback", rec)
    raw = (meth / "feedback.jsonl").read_text().strip()
    (meth / "legacy-index-migration-v2.json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "entries": [
                    {
                        "source": "feedback.jsonl",
                        "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                        "allow": ["unknown_original_tier"],
                    }
                ],
            }
        )
    )
    (meth / "feedback.jsonl").write_text(json.dumps({**rec, "reasoning": "changed"}) + "\n")
    with pytest.raises(ValueError, match="approved migration provenance"):
        run(source)
    assert output.read_bytes() == before


def test_overlapping_rebuild_fails_promptly_keeps_last_good(source):
    _meth, output = source
    run(source)
    before = output.read_bytes()
    with Path(str(output) + ".rebuild.lock").open("a") as lock:
        INDEX.fcntl.flock(lock, INDEX.fcntl.LOCK_EX | INDEX.fcntl.LOCK_NB)
        with pytest.raises(BlockingIOError):
            run(source)
    assert output.read_bytes() == before
