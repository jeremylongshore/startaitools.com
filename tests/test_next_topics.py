"""Tests for the topic-queue cluster support in scripts/blog/next-topics.py.

A cluster folds repeated near-duplicate rows into one row with child questions.
The merged rows stay in the file (status "merged", pointing at the cluster), and
a child is consumed only with its published URL. Offline; uses a temp queue.

Run:  pytest tests/test_next_topics.py -q
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "blog" / "next-topics.py"


def _load():
    spec = importlib.util.spec_from_file_location("next_topics", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _row(i: str, slug: str, status: str = "open") -> dict:
    return {"id": i, "generated_at": "2026-07-01T00:00:00+00:00", "topic": f"t {i}",
            "slug_hint": slug, "angle": "", "rationale": f"evidence for {i}",
            "source_signals": {}, "score": 0.8, "target_tier": 2, "status": status,
            "consumed_by": None, "consumed_at": None}


@pytest.fixture()
def nt(tmp_path, monkeypatch):
    mod = _load()
    q = tmp_path / ".next-topics.jsonl"
    rows = [_row("nt-a-001", "dup-one"), _row("nt-a-002", "dup-two"),
            _row("nt-a-003", "dup-three"), _row("nt-a-004", "partly-related"),
            _row("nt-a-005", "unrelated")]
    q.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    monkeypatch.setattr(mod, "QUEUE", q)
    return mod, q, tmp_path


def _spec(tmp_path: Path, **over) -> Path:
    spec = {
        "topic": "One cluster", "slug_hint": "one-cluster", "score": 0.9, "target_tier": 2,
        "merged_from": ["nt-a-001", "nt-a-002", "nt-a-003"],
        "children": [
            {"key": "q1", "question": "first?", "source_ids": ["nt-a-001", "nt-a-002"]},
            {"key": "q2", "question": "second?", "source_ids": ["nt-a-003"],
             "partial_source_ids": ["nt-a-004"]},
        ],
    }
    spec.update(over)
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(spec), encoding="utf-8")
    return p


def _rows(q: Path) -> dict:
    return {r["id"]: r for r in map(json.loads, q.read_text().splitlines())}


def test_cluster_merges_rows_and_preserves_sources(nt):
    mod, q, tmp = nt
    assert mod.main(["cluster", "--spec", str(_spec(tmp))]) == 0
    rows = _rows(q)
    cluster = next(r for r in rows.values() if r.get("kind") == "cluster")
    assert cluster["merged_from"] == ["nt-a-001", "nt-a-002", "nt-a-003"]
    assert [k["key"] for k in cluster["children"]] == ["q1", "q2"]
    for i in ("nt-a-001", "nt-a-002", "nt-a-003"):
        assert rows[i]["status"] == "merged"
        assert rows[i]["merged_into"] == cluster["id"]
        assert rows[i]["rationale"] == f"evidence for {i}"  # source evidence kept
    assert rows["nt-a-004"]["status"] == "open"  # partial source stays open
    assert len(rows) == 6
    assert mod.main(["validate"]) == 0


def test_top_skips_merged_rows(nt, capsys):
    mod, q, tmp = nt
    mod.main(["cluster", "--spec", str(_spec(tmp))])
    capsys.readouterr()
    mod.main(["list"])
    out = capsys.readouterr().out
    assert "nt-a-001" not in out and "cluster 0/2" in out


def test_dry_run_writes_nothing(nt):
    mod, q, tmp = nt
    before = q.read_text()
    assert mod.main(["cluster", "--spec", str(_spec(tmp)), "--dry-run"]) == 0
    assert q.read_text() == before


@pytest.mark.parametrize("over,needle", [
    ({"merged_from": ["nt-a-001", "nt-zzz"]}, "unknown queue ids"),
    ({"children": []}, "children"),
    ({"children": [{"key": "q1", "question": "a"}, {"key": "q1", "question": "b"}]}, "unique"),
    ({"merged_from": ["nt-a-001", "nt-a-004"]}, "partial sources must stay open"),
])
def test_cluster_refuses_bad_specs(nt, capsys, over, needle):
    mod, q, tmp = nt
    before = q.read_text()
    assert mod.main(["cluster", "--spec", str(_spec(tmp, **over))]) == 1
    assert needle in capsys.readouterr().err
    assert q.read_text() == before


def test_cannot_merge_a_row_twice(nt, capsys):
    mod, q, tmp = nt
    assert mod.main(["cluster", "--spec", str(_spec(tmp))]) == 0
    assert mod.main(["cluster", "--spec", str(_spec(tmp, slug_hint="again"))]) == 1
    assert "only open rows can be merged" in capsys.readouterr().err


def test_child_consume_requires_published_url(nt, capsys):
    mod, q, tmp = nt
    mod.main(["cluster", "--spec", str(_spec(tmp))])
    cid = next(r["id"] for r in _rows(q).values() if r.get("kind") == "cluster")
    assert mod.main(["consume", cid, "--by", "post-1"]) == 1
    assert mod.main(["consume", cid, "--by", "post-1", "--child", "q1"]) == 1
    assert mod.main(["consume", cid, "--by", "post-1", "--child", "q1",
                     "--url", "draft/local"]) == 1
    assert mod.main(["consume", cid, "--by", "post-1", "--child", "q9",
                     "--url", "https://example.com/p1/"]) == 1
    assert _rows(q)[cid]["children"][0]["status"] == "open"


def test_children_consume_one_at_a_time_then_cluster(nt):
    mod, q, tmp = nt
    mod.main(["cluster", "--spec", str(_spec(tmp))])
    cid = next(r["id"] for r in _rows(q).values() if r.get("kind") == "cluster")
    assert mod.main(["consume", cid, "--by", "p1", "--child", "q1",
                     "--url", "https://example.com/p1/"]) == 0
    c = _rows(q)[cid]
    assert c["status"] == "open" and c["children"][0]["url"] == "https://example.com/p1/"
    assert mod.main(["consume", cid, "--by", "p2", "--child", "q2",
                     "--url", "https://example.com/p2/"]) == 0
    assert _rows(q)[cid]["status"] == "consumed"
    assert mod.main(["validate"]) == 0


def test_consuming_a_merged_row_is_redirected(nt, capsys):
    mod, q, tmp = nt
    mod.main(["cluster", "--spec", str(_spec(tmp))])
    assert mod.main(["consume", "nt-a-001", "--by", "p1"]) == 1
    assert "merged into" in capsys.readouterr().err
    assert _rows(q)["nt-a-001"]["status"] == "merged"


def test_ingest_does_not_readd_a_merged_slug(nt, tmp_path):
    mod, q, tmp = nt
    mod.main(["cluster", "--spec", str(_spec(tmp))])
    staging = tmp_path / "staging.jsonl"
    staging.write_text(json.dumps({"topic": "x", "slug_hint": "dup-one", "score": 0.5}) + "\n")
    assert mod.main(["ingest", "--staging", str(staging)]) == 0
    assert sum(1 for r in _rows(q).values() if r["slug_hint"] == "dup-one") == 1


def test_validate_flags_broken_links(nt, capsys):
    mod, q, tmp = nt
    rows = list(_rows(q).values())
    rows[0].update(status="merged", merged_into="nt-missing")
    rows[1].update(status="bogus")
    q.write_text("".join(json.dumps(r) + "\n" for r in rows))
    assert mod.main(["validate"]) == 1
    err = capsys.readouterr().err
    assert "is not a cluster row" in err and "unknown status" in err


def test_plain_consume_unchanged(nt):
    mod, q, tmp = nt
    assert mod.main(["consume", "nt-a-005", "--by", "p5"]) == 0
    assert _rows(q)["nt-a-005"]["status"] == "consumed"
