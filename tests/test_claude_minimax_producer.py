"""Credential isolation and same-toolchain transport contract; no live requests."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "scripts/blog/claude-minimax-producer.py"
spec = importlib.util.spec_from_file_location("blog_producer", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_existing_environment_is_not_mutated():
    parent = {"MINIMAX_API_KEY": "fixture-secret", "ANTHROPIC_AUTH_TOKEN": "expired-fixture",
              "PATH": "guard-first"}
    child = module.child_environment(parent)
    assert parent["ANTHROPIC_AUTH_TOKEN"] == "expired-fixture"
    assert child["ANTHROPIC_AUTH_TOKEN"] == ""
    assert child["ANTHROPIC_API_KEY"] == "fixture-secret"
    assert child["PATH"] == "guard-first"
    for model in ("SONNET", "OPUS", "HAIKU"):
        assert child[f"ANTHROPIC_DEFAULT_{model}_MODEL"] == "MiniMax-M3"


def test_sops_secret_never_enters_command_arguments():
    calls = []
    def decrypt(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(stdout='{"minimax":{"key":"fixture-secret"}}')
    child = module.child_environment({"API_PROVIDERS_SOPS": "/private/fixture.sops.json"}, decrypt)
    assert child["ANTHROPIC_API_KEY"] == "fixture-secret"
    assert "fixture-secret" not in repr(calls)
    assert calls[0][1]["timeout"] == 30


def test_missing_configured_key_refuses():
    with pytest.raises(ValueError):
        module.child_environment({}, lambda *args, **kwargs: SimpleNamespace(stdout='{}'))
