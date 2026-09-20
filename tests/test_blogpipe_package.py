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
PUBLICATION_SHIM = ROOT / "scripts/blog/blog_publication_state.py"
# The last revisions where each entry point was one file; their public names are the API.
MONOLITH = "b70a357b"
PUBLICATION_MONOLITH = "c31d537e"


def public_names(source):
    names = set()
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return {n for n in names if not n.startswith("_")}


def load_shim(path=SHIM):
    spec = importlib.util.spec_from_file_location("shim_under_test", path)
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


def test_publication_shim_exposes_every_public_name_the_single_file_had():
    before = subprocess.check_output(
        [
            "git",
            "-C",
            str(ROOT),
            "show",
            f"{PUBLICATION_MONOLITH}:{PUBLICATION_SHIM.relative_to(ROOT)}",
        ],
        text=True,
    )
    shim = load_shim(PUBLICATION_SHIM)
    assert sorted(n for n in public_names(before) if not hasattr(shim, n)) == []


def test_both_shims_stay_shims():
    for shim in (SHIM, PUBLICATION_SHIM):
        source = shim.read_text()
        body = [
            node
            for node in ast.parse(source).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))
        ]
        assert body == [], f"{shim.name}: logic belongs in the blogpipe package"
        assert "sys.dont_write_bytecode = True" in source.split("import blogpipe", 1)[0]
        assert "mixed checkouts" in source


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
    shutil.copyfile(PUBLICATION_SHIM, target / PUBLICATION_SHIM.name)
    shutil.copytree(PACKAGE, target / "blogpipe", ignore=shutil.ignore_patterns("__pycache__"))
    return target


def digest_of(directory, shim=SHIM, function="verifier_sha256"):
    code = (
        "import importlib.util,sys;"
        "s=importlib.util.spec_from_file_location('c',sys.argv[1]);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "print(getattr(m,sys.argv[2])())"
    )
    path = str(directory / shim.name)
    output = subprocess.check_output([sys.executable, "-B", "-c", code, path, function], text=True)
    return output.strip()


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


def test_publication_helper_digest_covers_its_shim_and_the_package(tmp_path):
    copy = copied_verifier(tmp_path)

    def helper():
        return digest_of(copy, PUBLICATION_SHIM, "publication_helper_sha256")

    baseline = helper()
    assert baseline != digest_of(copy), "the two seal digests must name different entry points"
    for name in ("publication.py", "state.py", "frontmatter.py"):
        path = copy / "blogpipe" / name
        original = path.read_bytes()
        path.write_bytes(original + b"\n# changed\n")
        assert helper() != baseline, f"{name} is outside the publication helper digest"
        path.write_bytes(original)
    shim = copy / PUBLICATION_SHIM.name
    shim.write_bytes(shim.read_bytes() + b"\n# changed\n")
    assert helper() != baseline


def test_quality_seal_never_hashes_a_single_file_again():
    source = (PACKAGE / "publication.py").read_text()
    assert '"verifier_sha256": contract.verifier_sha256()' in source
    assert '"publication_helper_sha256": publication_helper_sha256()' in source
    assert "contract.__file__" not in source
    assert "sha(Path(__file__)" not in source


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
