"""Byte-stable Git input and UTF-8 fixture output across host text modes."""

import io
import subprocess
import sys
from pathlib import Path

import pytest

from codexspec.automation import BlueprintStore, GitRunner, ensure_dedicated_workspace, locate_repository
from codexspec.blueprint import blueprint_hash
from tests.automation_test_support import git, make_repo, sanitized_git_env
from tests.test_blueprint import FEATURE_ID
from tests.test_blueprint_store import append_request


def windows_text_transport(monkeypatch):
    """Emulate Windows TextIOWrapper writes while still executing real Git."""
    run = subprocess.run

    def translated_run(*args, **kwargs):
        text_mode = kwargs.get("text") or kwargs.get("encoding") or kwargs.get("universal_newlines")
        if not text_mode:
            return run(*args, **kwargs)
        encoding = kwargs.pop("encoding", None) or "utf-8"
        kwargs.pop("text", None)
        kwargs.pop("universal_newlines", None)
        if isinstance(kwargs.get("input"), str):
            buffer = io.BytesIO()
            stream = io.TextIOWrapper(buffer, encoding=encoding, newline="\r\n")
            stream.write(kwargs["input"])
            stream.flush()
            kwargs["input"] = buffer.getvalue()
        result = run(*args, **kwargs)
        for name in ("stdout", "stderr"):
            data = getattr(result, name)
            if data is not None:
                setattr(result, name, data.decode(encoding).replace("\r\n", "\n").replace("\r", "\n"))
        return result

    monkeypatch.setattr(subprocess, "run", translated_run)


@pytest.mark.parametrize("windows", [False, True])
@pytest.mark.parametrize("content", ["修正\nsecond line\n", "修正\r\nsecond line\r"])
def test_git_stdin_preserves_exact_utf8_bytes(tmp_path, monkeypatch, windows, content):
    repo = make_repo(tmp_path / "repo")
    if windows:
        windows_text_transport(monkeypatch)
    runner = GitRunner()
    blob = runner.run(repo, "hash-object", "-w", "--no-filters", "--stdin", input_text=content).stdout.strip()
    actual = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", blob],
        env=runner.environment(),
        capture_output=True,
        check=True,
    ).stdout
    assert actual == content.encode("utf-8")


@pytest.mark.parametrize("autocrlf", ["false", "true"])
def test_blueprint_preparation_matches_publication_with_windows_text_io(tmp_path, monkeypatch, autocrlf):
    repo = make_repo(tmp_path / "repo")
    git(repo, "config", "core.autocrlf", autocrlf)
    workspace = ensure_dedicated_workspace(locate_repository(repo))
    windows_text_transport(monkeypatch)
    store = BlueprintStore(workspace)
    prepared = store.prepare(append_request(blueprint_hash(b"")), feature_id_factory=lambda: FEATURE_ID)
    result = store.apply_and_commit(prepared["preparation_id"], prepared["tree"], "docs(blueprint): record requirement")
    assert result["result"] == "applied"
    assert git(workspace.path, "rev-parse", "HEAD^{tree}").stdout.strip() == prepared["tree"]
    assert git(workspace.path, "show", "HEAD:.codexspec/blueprint.md").stdout.encode("utf-8") == (
        workspace.blueprint_path.read_bytes()
    )


def test_git_fixture_reads_utf8_under_non_utf8_locale(tmp_path):
    repo = make_repo(tmp_path / "repo")
    data = "完整说明。\n".encode("utf-8")
    (repo / "utf8.txt").write_bytes(data)
    git(repo, "add", "utf8.txt")
    git(repo, "commit", "-m", "test: UTF-8 fixture")
    root = Path(__file__).resolve().parents[1]
    code = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from pathlib import Path; from tests.automation_test_support import git; "
        "sys.stdout.buffer.write(git(Path(sys.argv[2]), 'show', 'HEAD:utf8.txt').stdout.encode('utf-8'))"
    )
    env = sanitized_git_env()
    env["LC_ALL"] = "C"
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-X", "utf8=0", "-c", code, str(root), str(repo)],
        env=env,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == data
