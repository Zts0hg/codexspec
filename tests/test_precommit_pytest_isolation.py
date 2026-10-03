import os
import shlex
import subprocess
from pathlib import Path

import pytest  # type: ignore[import-untyped]
import yaml  # type: ignore[import-untyped]

from tests.automation_test_support import make_repo


def _pytest_hook_entry(repository_root: Path) -> list[str]:
    config = yaml.safe_load((repository_root / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    for repository in config["repos"]:
        for hook in repository["hooks"]:
            if hook["id"] == "pytest":
                return shlex.split(hook["entry"])
    raise AssertionError("pytest pre-commit hook is missing")


def test_pytest_hook_clears_caller_git_environment(tmp_path: Path) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    outer = make_repo(tmp_path / "outer")
    inner = make_repo(tmp_path / "inner")
    (inner / "inner.txt").write_text("inner\n", encoding="utf-8")
    probe = tmp_path / "test_nested_git_probe.py"
    probe.write_text(
        "import subprocess\n"
        "\n"
        "def test_nested_git_uses_temporary_repository():\n"
        f"    subprocess.run(['git', '-C', {str(inner)!r}, 'add', 'inner.txt'], check=True)\n",
        encoding="utf-8",
    )

    outer_index = outer / ".git/index"
    index_before = outer_index.read_bytes()
    poisoned_environment = os.environ.copy()
    poisoned_environment["GIT_INDEX_FILE"] = str(outer_index)
    result = subprocess.run(
        [*_pytest_hook_entry(repository_root), "-q", str(probe)],
        cwd=repository_root,
        env=poisoned_environment,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert outer_index.read_bytes() == index_before
    assert (
        "A  inner.txt"
        in subprocess.run(
            ["git", "-C", str(inner), "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )


def test_pytest_hook_runs_without_uv_on_path(tmp_path: Path, monkeypatch) -> None:
    """CI installs the development dependencies with pip and has no `uv` binary, so the
    hook must rerun pytest with its own interpreter; dropping uv from PATH must not
    break the hook. (Regression: FileNotFoundError 'uv' on every CI platform.)"""
    import shutil

    import tests.run_pytest as run_pytest

    if shutil.which("uv") is None:  # the condition only occurs where uv was never installed
        pytest.skip("uv is not installed here; nothing to remove from PATH")

    def has_uv(directory: str) -> bool:
        return (Path(directory) / "uv").exists() or (Path(directory) / "uv.exe").exists()

    remaining = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p and not has_uv(p)]
    monkeypatch.setenv("PATH", os.pathsep.join(remaining))

    probe = tmp_path / "test_no_uv_probe.py"
    probe.write_text("def test_probe_passes():\n    assert True\n", encoding="utf-8")
    assert run_pytest.main(["-q", str(probe)]) == 0


def test_unconfigured_repository_cannot_inherit_or_guess_commit_identity(tmp_path: Path) -> None:
    from tests.automation_test_support import git

    repo = tmp_path / "unconfigured"
    git(tmp_path, "init", "-b", "main", str(repo))
    (repo / "file.txt").write_text("content\n", encoding="utf-8")
    git(repo, "add", "file.txt")
    result = git(repo, "commit", "-m", "must require explicit fixture identity", check=False)
    assert result.returncode != 0, "Tests must not inherit or auto-detect the developer's Git identity"
    assert git(repo, "rev-parse", "--verify", "HEAD", check=False).returncode != 0


def test_bare_fixture_worktree_has_explicit_commit_identity(tmp_path: Path) -> None:
    from tests.automation_test_support import git, make_bare_remote

    repo = make_repo(tmp_path / "source")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    peer = tmp_path / "peer"
    git(remote, "worktree", "add", str(peer), "main")
    assert git(peer, "config", "--local", "--get", "user.name", check=False).stdout.strip() == "CodexSpec Tests"
    assert (
        git(peer, "config", "--local", "--get", "user.email", check=False).stdout.strip() == "tests@codexspec.invalid"
    )
    (peer / "remote.txt").write_text("remote change\n", encoding="utf-8")
    git(peer, "add", "remote.txt")
    git(peer, "commit", "-m", "remote change")
    assert git(peer, "log", "-1", "--format=%an <%ae>").stdout.strip() == "CodexSpec Tests <tests@codexspec.invalid>"


def test_pytest_hook_uses_cli_from_selected_python_environment(tmp_path: Path, monkeypatch) -> None:
    import sysconfig

    import tests.run_pytest as run_pytest

    script_name = "codexspec.exe" if os.name == "nt" else "codexspec"
    scripts = Path(sysconfig.get_path("scripts")).absolute()
    assert (scripts / script_name).is_file()
    remaining = [
        directory
        for directory in os.environ.get("PATH", "").split(os.pathsep)
        if directory and Path(directory).absolute() != scripts
    ]
    monkeypatch.setenv("PATH", os.pathsep.join(remaining))
    probe = tmp_path / "test_cli_environment_probe.py"
    probe.write_text(
        "import pathlib, shutil\n"
        "def test_cli_belongs_to_selected_environment():\n"
        "    assert pathlib.Path(shutil.which('codexspec')).absolute() == "
        f"pathlib.Path({str(scripts / script_name)!r})\n",
        encoding="utf-8",
    )
    # The probe runs outside the repository, so no repository conftest can repair PATH.
    assert run_pytest.main(["-q", str(probe), "-o", "addopts="]) == 0
