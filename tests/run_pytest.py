"""Run pytest without inheriting repository-local Git state from a hook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tests.automation_test_support import sanitized_git_env


def _project_interpreter() -> str:
    """The interpreter that owns the project's dev dependencies.

    The hook's `python` can be any interpreter (a system Anaconda, a pip-based CI
    environment); the project's own environment is what must run the suite. `uv run`
    used to select it, but `uv` does not exist on pip-based CI runners.
    """
    for candidate in (Path(".venv/bin/python"), Path(".venv/Scripts/python.exe")):
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def main(arguments: list[str] | None = None) -> int:
    pytest_arguments = sys.argv[1:] if arguments is None else arguments
    result = subprocess.run(
        [_project_interpreter(), "-m", "pytest", *pytest_arguments],
        check=False,
        env=sanitized_git_env(),
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
