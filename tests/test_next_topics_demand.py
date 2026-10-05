"""E03 weekly demand check: `next-topics.py annotate` (startaitools.com#123).

Search evidence may be attached to rows a person already queued. It may never add
a row, remove one, reorder, rescore or re-topic one, or choose what gets written.
Every refusal leaves the queue bytes unchanged. Offline; uses a temp queue.

Run:  pytest tests/test_next_topics_demand.py -q
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "blog" / "next-topics.py"


def _load():
    spec = importlib.util.spec_from_file_location("next_topics_demand", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _row(i: str, slug: str, score: float, status: str = "open") -> dict:
    return {"id": i, "generated_at": "2026-07-01T00:00:00+00:00", "topic": f"topic {i}",
            "slug_hint": slug, "angle": f"angle {i}", "rationale": f"evidence for {i}",
            "source_signals": {}, "score": score, "target_tier": 2, "status": status,
            "consumed_by": None, "consumed_at": None}


def _check(qid: str, **over) -> dict:
    obj = {
        "queue_id": qid, "checked_at": "2026-10-05T00:00:00+00:00",
        "query_forms": [{"q": "claude code hook timeout", "source": "serp",
                         "evidence_url": "https://code.claude.com/docs/en/hooks"}],
        "serp_top": [{"title": "Hooks reference", "url": "https://code.claude.com/docs/en/hooks"}],
        "intent": "troubleshooting", "gap": "no post covers the timeout case",
        "demand": "observed", "merge_of": [], "recommended_title_form": None,
        "uncertainty": "Ranking pages observed; autocomplete not visible.",
    }
    obj.update(over)
    return obj


@pytest.fixture()
def nt(tmp_path, monkeypatch):
    mod = _load()
    q = tmp_path / ".next-topics.jsonl"
    rows = [_row("nt-a-001", "hook-timeout", 0.4), _row("nt-a-002", "hook-timeouts", 0.9),
            _row("nt-a-003", "unrelated", 0.7), _row("nt-a-004", "done", 0.8, "consumed")]
    q.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    monkeypatch.setattr(mod, "QUEUE", q)
    return mod, q, tmp_path


def _stage(tmp_path: Path, objs: list) -> str:
    p = tmp_path / "demand.staging.jsonl"
    p.write_text("".join(json.dumps(o) + "\n" for o in objs), encoding="utf-8")
    return str(p)


def _rows(q: Path) -> list[dict]:
    return [json.loads(line) for line in q.read_text(encoding="utf-8").splitlines()]


def test_annotate_touches_only_the_demand_key_of_existing_rows(nt):
    mod, q, tmp = nt
    before = _rows(q)
    staged = [_check("nt-a-001", merge_of=["nt-a-002"]),
              _check("nt-a-003", demand="estimated", query_forms=[{"q": "x", "source": "guess"}])]
    assert mod.main(["annotate", "--staging", _stage(tmp, staged)]) == 0
    after = _rows(q)
    # Same rows, same order, and every field except `demand` byte-identical.
    assert [r["id"] for r in after] == [r["id"] for r in before]
    for b, a in zip(before, after, strict=True):
        assert {k: v for k, v in a.items() if k != "demand"} == b
    assert after[0]["demand"]["demand"] == "observed"
    assert after[0]["demand"]["merge_of"] == ["nt-a-002"]
    assert "queue_id" not in after[0]["demand"]
    assert "demand" not in after[1] and after[2]["demand"]["demand"] == "estimated"
    # Search evidence never re-ranks: the top open row is still chosen by score alone.
    assert mod._open_ranked(after)[0]["id"] == "nt-a-002"
    assert mod.main(["validate"]) == 0


def test_dry_run_writes_nothing(nt):
    mod, q, tmp = nt
    raw = q.read_bytes()
    assert mod.main(["annotate", "--staging", _stage(tmp, [_check("nt-a-001")]),
                     "--dry-run"]) == 0
    assert q.read_bytes() == raw


@pytest.mark.parametrize(
    "objs",
    [
        [_check("nt-z-999")],                                    # unknown id: never adds rows
        [_check("nt-a-004")],                                    # consumed row
        [_check("nt-a-001", topic="A new subject")],             # re-topic attempt
        [_check("nt-a-001", score=1.0)],                         # rescore attempt
        [_check("nt-a-001", query_forms=[{"q": "x", "source": "serp"}])],  # no source url
        [_check("nt-a-001", query_forms=[])],                    # observed without evidence
        [_check("nt-a-001", uncertainty="")],                    # no uncertainty
        [_check("nt-a-001", demand="huge")],                     # unknown level
        [_check("nt-a-001", merge_of=["nt-a-004"])],             # merge into a closed row
        [_check("nt-a-001", merge_of=["nt-a-001"])],             # merge into itself
        [_check("nt-a-001", serp_top=[{"title": "t", "url": "ftp://x"}])],
        [_check("nt-a-001"), _check("nt-a-001")],                # same row twice
        [_check("nt-a-001"), _check("nt-z-999")],                # one bad object refuses all
        [_check("nt-a-001")] * 6,                                # over the 5-row bound
    ],
)
def test_any_invalid_object_refuses_the_batch_and_leaves_the_queue_bytes(nt, objs):
    mod, q, tmp = nt
    raw = q.read_bytes()
    assert mod.main(["annotate", "--staging", _stage(tmp, objs)]) == 1
    assert q.read_bytes() == raw


def test_empty_staging_is_a_no_op(nt):
    mod, q, tmp = nt
    raw = q.read_bytes()
    assert mod.main(["annotate", "--staging", _stage(tmp, [])]) == 0
    assert q.read_bytes() == raw
