"""Offline inventory with independent Git working-directory identity."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from codexspec.commit_runtime import AutomationError, GitRunner

from .metadata import Inspection, inspect_installation


class ReadOnlyGit:
    def __init__(self):
        try:
            self.env = GitRunner().environment()
        except AutomationError as exc:
            raise ValueError(f"Git inspection unavailable: {exc}") from exc
        self.env.update(GIT_OPTIONAL_LOCKS="0", GIT_LITERAL_PATHSPECS="1", GIT_TERMINAL_PROMPT="0")

    def run(self, root: Path, *args: str, check: bool = True) -> bytes:
        result = subprocess.run(
            ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", str(root), *args],
            env=self.env,
            capture_output=True,
            timeout=30,
        )
        if check and result.returncode:
            raise ValueError(result.stderr.decode("utf-8", errors="replace").strip() or "Git inspection failed")
        return result.stdout if result.returncode == 0 else b""


@dataclass
class Installation:
    path: Path
    inspection: Inspection
    repository: str | None = None


@dataclass
class Discovery:
    installations: list[Installation] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


def discover(start: Path) -> Discovery:
    start = start.expanduser().absolute()
    if any(part.is_symlink() for part in (start, *start.parents)) or not start.is_dir():
        raise ValueError(f"scan root is not an accessible real directory: {start}")
    result = Discovery()
    try:
        git = ReadOnlyGit()
    except (OSError, ValueError, subprocess.SubprocessError):
        git = None
    pending = [start]
    while pending:
        current = pending.pop()
        try:
            with os.scandir(current) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
            for entry in entries:
                if entry.name == ".codexspec":
                    if entry.is_symlink() or not entry.is_dir(follow_symlinks=False):
                        result.issues.append(f"{entry.path}: .codexspec is not a real directory")
                        continue
                    repository = None
                    if git:
                        try:
                            common = git.run(current, "rev-parse", "--git-common-dir", check=False).decode().strip()
                            if common:
                                repository = str((current / common).resolve())
                        except (OSError, ValueError, subprocess.SubprocessError):
                            pass  # Lack of Git does not hide a discoverable installation.
                    result.installations.append(Installation(current, inspect_installation(current), repository))
                elif entry.name != ".git" and entry.is_dir(follow_symlinks=False):
                    pending.append(Path(entry.path))
        except OSError as exc:
            if current == start:
                raise ValueError(f"cannot read scan root {start}: {exc}") from exc
            result.issues.append(f"{current}: {exc}")
    result.installations.sort(key=lambda item: (item.repository or str(item.path), str(item.path)))
    return result
