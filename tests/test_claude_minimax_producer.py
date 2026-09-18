"""Credential isolation and same-toolchain transport contract; no live requests."""

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

SOURCE = Path(os.environ.get("BLOG_MINIMAX_SOURCE_UNDER_TEST",
                             str(Path(__file__).resolve().parents[1]
                                 / "scripts/blog/claude-minimax-producer.py")))
spec = importlib.util.spec_from_file_location("blog_producer", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_existing_environment_is_not_mutated():
    parent = {
        "MINIMAX_API_KEY": "fixture-secret",
        "ANTHROPIC_AUTH_TOKEN": "expired-fixture",
        "PATH": "guard-first",
    }
    child = module.child_environment(parent)
    assert parent["ANTHROPIC_AUTH_TOKEN"] == "expired-fixture"
    assert child["ANTHROPIC_AUTH_TOKEN"] == ""
    assert child["ANTHROPIC_API_KEY"] == "fixture-secret"
    assert child["CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT"] == "1"
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
        module.child_environment({}, lambda *args, **kwargs: SimpleNamespace(stdout="{}"))


def test_custom_skill_agents_are_explicitly_registered(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    for name in ("blog-classifier", "blog-consistency-checker", "blog-fact-checker"):
        (agents / f"{name}.md").write_text(
            f'---\nname: {name}\ndescription: "Fixture gate"\n---\nReal configured prompt.\n'
        )
    result = module.agent_definitions(tmp_path)
    assert set(result) == {"blog-classifier", "blog-consistency-checker", "blog-fact-checker"}
    assert all(value["model"] == "inherit" for value in result.values())
    assert all(value["prompt"] == "Real configured prompt." for value in result.values())


def test_missing_agent_definition_refuses_instead_of_inline_fabrication(tmp_path):
    with pytest.raises(FileNotFoundError):
        module.agent_definitions(tmp_path)


def test_execution_contract_is_bound_without_secrets(tmp_path):
    context = module.execution_contract(
        tmp_path,
        {
            "BLOG_REPO_DIR": "/isolated/run",
            "BLOG_RUN_ID": "fixture-uuid",
            "BLOG_RUN_MANIFEST": "/isolated/manifest.json",
            "BLOG_RUN_DIAGNOSTICS_DIR": "/isolated/diagnostics",
            "BLOG_RUN_WORKSPACE_HELPER": "/trusted/scripts/blog-run-workspace.py",
            "MINIMAX_API_KEY": "fixture-secret",
        },
    )
    assert "/isolated/run" in context and "fixture-uuid" in context
    assert "fixture-secret" not in context
    assert "never invent receipts" in context
    with pytest.raises(ValueError):
        module.execution_contract(tmp_path, {})


def test_prompt_separates_publication_paths_from_registered_diagnostic_operation(tmp_path):
    environment = {
        "BLOG_REPO_DIR": "/isolated/run/workspace", "BLOG_RUN_ID": "fixture-uuid",
        "BLOG_RUN_MANIFEST": "/isolated/run/manifest.json",
        "BLOG_RUN_DIAGNOSTICS_DIR": "/isolated/run/diagnostics",
        "BLOG_RUN_WORKSPACE_HELPER": "/trusted/scripts/blog-run-workspace.py",
    }
    context = module.execution_contract(tmp_path, environment)
    assert "All writes and app helper paths MUST use the bound workspace" not in context
    assert "Publication writes and their app helper paths MUST use the bound workspace" in context
    assert "Do not redirect stderr or write files there directly" in context
    assert "BLOG_RUN_WORKSPACE_HELPER diagnostic" in context
    assert "DATE.RUN_ID.JSONLABEL.json" in context
    for value in environment.values():
        assert value in context
    for key in ("BLOG_RUN_MANIFEST", "BLOG_RUN_DIAGNOSTICS_DIR", "BLOG_RUN_WORKSPACE_HELPER"):
        incomplete = {k: value for k, value in environment.items() if k != key}
        with pytest.raises(ValueError, match="diagnostic context missing"):
            module.execution_contract(tmp_path, incomplete)
