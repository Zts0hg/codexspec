"""Run pytest without inheriting repository-local Git state from a hook."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tests.automation_test_support import sanitized_git_env


def _pytest_command(arguments: list[str]) -> list[str]:
    """Select how to run pytest in the environment that owns the dev dependencies.

    The hook's `python` can be any interpreter (a system Anaconda, a pip-based CI
    environment), and CI ships two different shapes: test jobs install pytest with
    pip and have no `uv`, while the lint job has `uv` and no direct pytest install.
    Order: the project's own `.venv` when it exists (what `uv run` selects locally);
    the current interpreter when pytest is importable (pip-based CI test jobs);
    `uv run` as the bootstrap of last resort (CI lint jobs).
    """
    for candidate in (Path(".venv/bin/python"), Path(".venv/Scripts/python.exe")):
        if candidate.is_file():
            return [str(candidate), "-m", "pytest", *arguments]
    if importlib.util.find_spec("pytest") is not None:
        return [sys.executable, "-m", "pytest", *arguments]
    if shutil.which("uv") is None:
        raise SystemExit("pytest is unavailable: no .venv, no pytest in the current interpreter, and no uv on PATH")
    return ["uv", "run", "--extra", "dev", "pytest", *arguments]


def main(arguments: list[str] | None = None) -> int:
    pytest_arguments = sys.argv[1:] if arguments is None else arguments
    command = _pytest_command(pytest_arguments)
    environment = sanitized_git_env()
    if command[0] != "uv":
        # Match child CLI tools to the selected interpreter even from a plain git hook.
        scripts = subprocess.check_output(
            [command[0], "-c", "import sysconfig; print(sysconfig.get_path('scripts'))"],
            text=True,
            env=environment,
        ).strip()
        environment["PATH"] = scripts + os.pathsep + environment.get("PATH", "")
    result = subprocess.run(command, check=False, env=environment)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
