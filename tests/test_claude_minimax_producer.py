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


def _run_context(tmp_path):
    agents = tmp_path / "agents"
    agents.mkdir()
    for name in ("blog-classifier", "blog-consistency-checker", "blog-fact-checker"):
        (agents / f"{name}.md").write_text(
            f'---\nname: {name}\ndescription: "Fixture gate"\n---\nReal configured prompt.\n'
        )
    return {
        "BLOG_SKILL_DIR": str(tmp_path),
        "BLOG_REPO_DIR": "/isolated/run/workspace", "BLOG_RUN_ID": "fixture-uuid",
        "BLOG_RUN_MANIFEST": "/isolated/run/manifest.json",
        "BLOG_RUN_DIAGNOSTICS_DIR": "/isolated/run/diagnostics",
        "BLOG_RUN_WORKSPACE_HELPER": "/trusted/scripts/blog-run-workspace.py",
        "PATH": "guard-first",
    }


def _capture_main(monkeypatch, environment):
    for key in list(os.environ):
        monkeypatch.delenv(key, raising=False)
    for key, value in environment.items():
        monkeypatch.setenv(key, value)
    calls = []

    def fake_exec(program, argv, env):
        calls.append((program, argv, env))
        return 0

    return module.main(execvpe=fake_exec), calls


def test_claude_provider_registers_agents_and_contract_without_minimax(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"BLOG_PRODUCER_PROVIDER": "claude"}

    def no_decrypt(*args, **kwargs):
        raise AssertionError("the claude provider must never decrypt the MiniMax key")

    monkeypatch.setattr(module, "child_environment", no_decrypt)
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 0 and len(calls) == 1
    program, argv, env = calls[0]
    assert program == "claude"
    agents = __import__("json").loads(argv[argv.index("--agents") + 1])
    assert set(agents) == {"blog-classifier", "blog-consistency-checker", "blog-fact-checker"}
    assert "fixture-uuid" in argv[argv.index("--append-system-prompt") + 1]
    assert "ANTHROPIC_BASE_URL" not in env and "ANTHROPIC_API_KEY" not in env
    assert env["PATH"] == "guard-first"


def test_default_provider_is_still_minimax(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"MINIMAX_API_KEY": "fixture-secret"}
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 0
    env = calls[0][2]
    assert env["ANTHROPIC_BASE_URL"] == "https://api.minimax.io/anthropic"
    assert "fixture-secret" not in repr(calls[0][1])


def test_unknown_provider_refuses(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"BLOG_PRODUCER_PROVIDER": "grok"}
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 64 and calls == []


def test_claude_provider_without_agents_refuses(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"BLOG_PRODUCER_PROVIDER": "claude"}
    environment["BLOG_SKILL_DIR"] = str(tmp_path / "missing")
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 69 and calls == []


def test_wrapper_routes_plain_claude_through_the_agent_registering_launcher():
    wrapper = (SOURCE.parent / "blog-backfill-daily.sh").read_text()
    body = wrapper.split("run_claude_producer() {", 1)[1].split("\n}\n", 1)[0]
    launcher = "python3 '$BLOG_DIR/scripts/blog/claude-minimax-producer.py'"
    assert f"BLOG_PRODUCER_PROVIDER=claude {launcher}" in body
    # No branch of the producer may launch a bare `claude` without registered agents.
    declaration = "local t0 exitc wall command_prefix=claude provider=claude"
    assert "command_prefix=claude " not in body.replace(declaration, "")


# --- isolated producer context (2026-11-13) ---

def test_minimax_provider_runs_bare_without_mcp_servers(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"MINIMAX_API_KEY": "fixture-secret"}
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 0
    argv = calls[0][1]
    assert "--bare" in argv
    assert "--strict-mcp-config" in argv
    assert argv[argv.index("--mcp-config") + 1] == '{"mcpServers":{}}'
    assert argv.index("--bare") < argv.index("--agents")      # flags precede the passthrough args


def test_claude_provider_drops_mcp_but_never_runs_bare(tmp_path, monkeypatch):
    # --bare never reads the OAuth login the claude provider depends on.
    environment = _run_context(tmp_path) | {"BLOG_PRODUCER_PROVIDER": "claude"}
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 0
    argv = calls[0][1]
    assert "--bare" not in argv
    assert "--strict-mcp-config" in argv


def test_full_context_switch_restores_the_old_launch(tmp_path, monkeypatch):
    environment = _run_context(tmp_path) | {"MINIMAX_API_KEY": "fixture-secret",
                                            "BLOG_PRODUCER_FULL_CONTEXT": "1"}
    status, calls = _capture_main(monkeypatch, environment)
    assert status == 0
    argv = calls[0][1]
    assert "--bare" not in argv and "--strict-mcp-config" not in argv


def test_telemetry_keys_are_copied_from_user_settings_but_never_override(tmp_path):
    settings = tmp_path / "settings.json"
    settings.write_text(__import__("json").dumps({"env": {
        "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
        "OTEL_EXPORTER_OTLP_ENDPOINT": "http://127.0.0.1:14318",
        "OTEL_METRICS_EXPORTER": "otlp",
        "UNRELATED": "not-copied",
    }}))
    env = module.telemetry_environment({"OTEL_METRICS_EXPORTER": "none", "PATH": "p"}, settings)
    assert env["CLAUDE_CODE_ENABLE_TELEMETRY"] == "1"
    assert env["OTEL_EXPORTER_OTLP_ENDPOINT"] == "http://127.0.0.1:14318"
    assert env["OTEL_METRICS_EXPORTER"] == "none"          # caller's value wins
    assert "UNRELATED" not in env
    assert module.telemetry_environment({"PATH": "p"}, tmp_path / "missing.json") == {"PATH": "p"}
