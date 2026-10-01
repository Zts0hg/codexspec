"""Run pytest without inheriting repository-local Git state from a hook."""

from __future__ import annotations

import subprocess
import sys

from tests.automation_test_support import sanitized_git_env


def main(arguments: list[str] | None = None) -> int:
    pytest_arguments = sys.argv[1:] if arguments is None else arguments
    result = subprocess.run(
        ["uv", "run", "--extra", "dev", "pytest", *pytest_arguments],
        check=False,
        env=sanitized_git_env(),
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
