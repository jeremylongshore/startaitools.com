"""Tests for scripts/blog/native-metrics-devto.py (bead bhn.12).

Offline only: every test injects a fake fetcher fed from a recorded-shape
fixture, so no test reaches dev.to and no key is needed. The contract under
test is that failures are recorded as explicit statuses, never as zeros, and
that the key is never echoed.

Run:  pytest tests/test_native_metrics_devto.py -q
"""

from __future__ import annotations

import importlib.util
import json
import urllib.error
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "blog" / "native-metrics-devto.py"
FIXTURE = REPO / "tests" / "fixtures" / "native-metrics" / "devto-published-page1.json"
FAKE_KEY = "fixture-key-do-not-print-7f3a"


def _load():
    spec = importlib.util.spec_from_file_location("native_metrics_devto", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


nm = _load()


class FakeFetch:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, url, headers):
        self.calls.append((url, headers))
        item = self.responses.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


@pytest.fixture(autouse=True)
def _no_env_key(monkeypatch):
    monkeypatch.delenv("DEVTO_API_KEY", raising=False)


def _run(tmp_path, fetch, key=FAKE_KEY, capsys=None):
    env = tmp_path / "blog.env"
    env.write_text(f"OTHER=1\nDEVTO_API_KEY={key}\n" if key else "OTHER=1\n")
    out = tmp_path / "obs.jsonl"
    code = nm.main(["--out", str(out), "--env-file", str(env)], fetch=fetch)
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    return code, rows


def test_success_writes_one_row_per_article_with_contract_fields(tmp_path):
    fetch = FakeFetch([(200, FIXTURE.read_bytes())])
    code, rows = _run(tmp_path, fetch)
    assert code == 0
    devto = [r for r in rows if r["surface"] == "devto"]
    assert [r["article_id"] for r in devto] == [3001001, 3001002, 3001003]
    first = devto[0]
    for field in ("surface", "article_id", "url", "canonical_url", "page_views",
                  "reactions", "comments", "observed_at", "source"):
        assert field in first
    assert first["page_views"] == 412 and first["reactions"] == 7 and first["comments"] == 2
    assert first["source"] == "devto_api"
    assert first["canonical_url"] == "https://startaitools.com/posts/fixture-article-one/"
    # The request carried the key in the header and asked for the published list.
    url, headers = fetch.calls[0]
    assert url.startswith("https://dev.to/api/articles/me/published?")
    assert headers["api-key"] == FAKE_KEY


def test_absent_metric_is_null_not_zero_and_real_zero_stays_zero(tmp_path):
    code, rows = _run(tmp_path, FakeFetch([(200, FIXTURE.read_bytes())]))
    by_id = {r["article_id"]: r for r in rows if r["surface"] == "devto"}
    assert by_id[3001003]["page_views"] is None
    assert by_id[3001002]["page_views"] == 0


@pytest.mark.parametrize("status", [401, 403])
def test_auth_failure_is_one_status_row_never_zeros(tmp_path, status):
    code, rows = _run(tmp_path, FakeFetch([(status, b"")]))
    devto = [r for r in rows if r["surface"] == "devto"]
    assert code == 2
    assert devto == [{"surface": "devto", "status": "auth_failed", "http_status": status,
                      "observed_at": devto[0]["observed_at"], "source": "devto_api"}]
    assert not any("page_views" in r for r in rows)


def test_server_error_and_network_error_are_unavailable(tmp_path):
    code, rows = _run(tmp_path, FakeFetch([(503, b"")]))
    assert code == 3
    assert [r["status"] for r in rows if r["surface"] == "devto"] == ["unavailable"]
    code, rows = _run(tmp_path, FakeFetch([urllib.error.URLError("dns")]))
    assert code == 3
    last = [r for r in rows if r["surface"] == "devto"][-1]
    assert last["status"] == "unavailable" and last["reason"].startswith("network_error")


def test_missing_key_never_calls_the_api(tmp_path):
    fetch = FakeFetch([])
    code, rows = _run(tmp_path, fetch, key=None)
    assert code == 3 and fetch.calls == []
    devto = [r for r in rows if r["surface"] == "devto"]
    assert devto[0]["status"] == "unavailable" and devto[0]["reason"] == "missing_api_key"


def test_invalid_json_is_unavailable(tmp_path):
    code, rows = _run(tmp_path, FakeFetch([(200, b"<html>")]))
    assert code == 3
    assert [r for r in rows if r["surface"] == "devto"][0]["reason"] == "invalid_json"


def test_pagination_continues_on_full_page(tmp_path, monkeypatch):
    monkeypatch.setattr(nm, "PER_PAGE", 2)
    page1 = json.dumps(json.loads(FIXTURE.read_text())[:2]).encode()
    page2 = json.dumps(json.loads(FIXTURE.read_text())[2:]).encode()
    fetch = FakeFetch([(200, page1), (200, page2)])
    code, rows = _run(tmp_path, fetch)
    assert code == 0 and len(fetch.calls) == 2
    assert "page=2" in fetch.calls[1][0]
    assert len([r for r in rows if r["surface"] == "devto"]) == 3


def test_registry_marks_every_other_surface_without_numbers(tmp_path):
    _, rows = _run(tmp_path, FakeFetch([(200, FIXTURE.read_bytes())]))
    reg = {r["surface"]: r for r in rows if r["source"] == "registry"}
    assert set(reg) == {"hashnode", "substack", "medium", "linkedin_company",
                        "linkedin_personal", "x"}
    assert reg["hashnode"]["status"] == "paid_api"
    for name in ("substack", "medium", "linkedin_company", "linkedin_personal", "x"):
        assert reg[name]["status"] == "unavailable_without_dashboard"
    assert not any(k in r for r in reg.values() for k in ("page_views", "reactions", "comments"))


def test_log_is_append_only(tmp_path):
    _run(tmp_path, FakeFetch([(200, FIXTURE.read_bytes())]))
    _, rows = _run(tmp_path, FakeFetch([(401, b"")]))
    statuses = [r["status"] for r in rows if r["surface"] == "devto"]
    assert statuses == ["ok", "ok", "ok", "auth_failed"]


def test_key_never_reaches_output_or_log(tmp_path, capsys):
    _, rows = _run(tmp_path, FakeFetch([(200, FIXTURE.read_bytes())]))
    captured = capsys.readouterr()
    assert FAKE_KEY not in captured.out + captured.err
    assert FAKE_KEY not in (tmp_path / "obs.jsonl").read_text()


def test_summary_totals_skip_nulls(tmp_path, capsys):
    _run(tmp_path, FakeFetch([(200, FIXTURE.read_bytes())]))
    summary = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert summary == {"devto_status": "ok", "articles": 3, "page_views_total": 412,
                       "reactions_total": 8, "comments_total": 2}


def test_env_key_wins_and_quoted_values_parse(tmp_path, monkeypatch):
    env = tmp_path / "e.env"
    env.write_text("export DEVTO_API_KEY='quoted-value'\n")
    assert nm.read_key(env) == "quoted-value"
    monkeypatch.setenv("DEVTO_API_KEY", "from-env")
    assert nm.read_key(env) == "from-env"


def test_runtime_log_is_gitignored():
    assert ".native-metrics.jsonl" in (REPO / ".gitignore").read_text().splitlines()
