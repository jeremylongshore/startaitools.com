"""The blogpipe package move must be invisible to every caller of the old script path."""

import ast
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from test_blog_producer_contract import DATE, RUN, produced  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
SHIM = ROOT / "scripts/blog/blog-producer-contract.py"
PACKAGE = ROOT / "scripts/blog/blogpipe"
# The last revision where the contract was one file; its public names are the API.
MONOLITH = "b70a357b"


def public_names(source):
    names = set()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return {n for n in names if not n.startswith("_")}


def load_shim():
    spec = importlib.util.spec_from_file_location("contract_shim_under_test", SHIM)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_shim_exposes_every_public_name_the_single_file_contract_had():
    before = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{MONOLITH}:scripts/blog/blog-producer-contract.py"],
        text=True,
    )
    missing = sorted(n for n in public_names(before) if not hasattr(load_shim(), n))
    assert missing == []


def test_shim_stays_a_shim():
    body = [
        node
        for node in ast.parse(SHIM.read_text()).body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    ]
    assert body == [], "logic belongs in the blogpipe package, not the entry-point shim"
    assert "sys.dont_write_bytecode = True" in SHIM.read_text().split("from blogpipe", 1)[0]


def test_module_entry_point_matches_the_script_path(produced):  # noqa: F811
    repo, _, _, transcript = produced
    arguments = ["verify", "--repo", str(repo), "--date", DATE, "--run-id", RUN]
    arguments += ["--transcript", str(transcript)]
    script = subprocess.run([sys.executable, str(SHIM), *arguments], capture_output=True, text=True)
    module = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "contract", *arguments],
        capture_output=True,
        text=True,
        cwd=PACKAGE.parent,
    )
    assert script.returncode == module.returncode == 0, script.stderr + module.stderr
    assert json.loads(script.stdout) == json.loads(module.stdout)
    assert json.loads(module.stdout)["outcome"] == "complete"


def test_unknown_module_command_is_a_usage_error():
    result = subprocess.run(
        [sys.executable, "-B", "-m", "blogpipe", "publish-everything"],
        capture_output=True,
        text=True,
        cwd=PACKAGE.parent,
    )
    assert result.returncode == 64
    assert "usage:" in result.stderr


def test_transcript_parsing_stays_deletable_as_one_file():
    """Only contract.py may import it, and only the advisory logger."""
    importers = {}
    for path in PACKAGE.glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom) and node.module == "transcript":
                importers[path.name] = sorted(alias.name for alias in node.names)
    assert importers == {"contract.py": ["transcript_advisory"]}
    # And it may lean only on primitives, never on a gate, so removing it breaks nothing.
    own = {
        node.module
        for node in ast.walk(ast.parse((PACKAGE / "transcript.py").read_text()))
        if isinstance(node, ast.ImportFrom) and node.level == 1
    }
    assert own <= {"errors", "jsonio"}


def copied_verifier(tmp_path):
    import shutil

    target = tmp_path / "verifier"
    target.mkdir()
    shutil.copyfile(SHIM, target / SHIM.name)
    shutil.copytree(PACKAGE, target / "blogpipe", ignore=shutil.ignore_patterns("__pycache__"))
    return target


def digest_of(directory):
    code = (
        "import importlib.util,sys;"
        "s=importlib.util.spec_from_file_location('c',sys.argv[1]);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.verifier_sha256())"
    )
    shim = str(directory / SHIM.name)
    return subprocess.check_output([sys.executable, "-B", "-c", code, shim], text=True).strip()


def test_verifier_digest_moves_when_any_module_of_the_package_changes(tmp_path):
    """The seal's verifier_sha256 hashed contract.__file__: after the split that is the
    shim, a constant. It must cover the logic that actually decides publication."""
    copy = copied_verifier(tmp_path)
    baseline = digest_of(copy)
    assert baseline == digest_of(copy) and len(baseline) == 64
    modules = sorted(p.name for p in (copy / "blogpipe").glob("*.py"))
    assert {"contract.py", "roles.py", "jsonio.py", "transcript.py"} <= set(modules)
    for name in modules:
        path = copy / "blogpipe" / name
        original = path.read_bytes()
        path.write_bytes(original + b"\n# changed\n")
        assert digest_of(copy) != baseline, f"{name} is outside the verifier digest"
        path.write_bytes(original)
    assert digest_of(copy) == baseline
    (copy / SHIM.name).write_bytes((copy / SHIM.name).read_bytes() + b"\n# changed\n")
    assert digest_of(copy) != baseline, "the entry-point shim is outside the verifier digest"


def test_quality_seal_records_the_whole_verifier_digest():
    source = (ROOT / "scripts/blog/blog_publication_state.py").read_text()
    assert '"verifier_sha256": contract.verifier_sha256()' in source
    assert "contract.__file__" not in source


def test_shim_refuses_a_blogpipe_cached_from_another_checkout(tmp_path):
    """`import blogpipe` is process-global; two checkouts in one process must not mix."""
    copy = copied_verifier(tmp_path)
    code = (
        "import importlib.util,sys\n"
        "def load(p):\n"
        "    s=importlib.util.spec_from_file_location('c',p)\n"
        "    m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n"
        "load(sys.argv[1])\n"
        "load(sys.argv[2])\n"
    )
    result = subprocess.run(
        [sys.executable, "-B", "-c", code, str(SHIM), str(copy / SHIM.name)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "mixed checkouts" in result.stderr
