import os
import shlex
import subprocess
from pathlib import Path

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
