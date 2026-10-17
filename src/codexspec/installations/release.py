"""Acquire a pinned target runtime without replacing the calling CLI."""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import httpx
from packaging.version import InvalidVersion, Version

from .metadata import MAX_ENTRIES, _unique_pairs, checked_path, managed_path

MAX_RESULT_BYTES = 64 * 1024 * 1024


def resolve_latest() -> str:
    response = httpx.get("https://pypi.org/pypi/codexspec/json", timeout=30)
    response.raise_for_status()
    try:
        data = response.json()
    except RecursionError as exc:
        raise ValueError("release metadata nesting is too deep") from exc
    if not isinstance(data, dict) or not isinstance(data.get("releases"), dict):
        raise ValueError("invalid release metadata")
    versions = []
    for version, distributions in data["releases"].items():
        try:
            parsed = Version(version)
        except InvalidVersion:
            continue
        if parsed.is_prerelease or parsed.is_devrelease or parsed.local:
            continue
        if isinstance(distributions, list) and any(
            isinstance(item, dict) and item.get("yanked") is False for item in distributions
        ):
            versions.append(parsed)
    if not versions:
        raise ValueError("no available stable CodexSpec release")
    return str(max(versions))


def clean_environment() -> dict[str, str]:
    env = {key: value for key, value in os.environ.items() if not key.startswith(("PYTHON", "PIP_", "GIT_"))}
    env.update(PIP_CONFIG_FILE=os.devnull, PIP_DISABLE_PIP_VERSION_CHECK="1", PYTHONNOUSERSITE="1")
    return env


def run_process(command: list[str], *, cwd: Path, timeout: int = 180) -> None:
    try:
        result = subprocess.run(command, cwd=cwd, env=clean_environment(), capture_output=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError(f"target runtime could not execute: {type(exc).__name__}") from exc
    if result.returncode:
        # Do not echo package-manager output which can contain local credentials/configuration.
        raise ValueError(f"target runtime command failed (exit {result.returncode}); no project files were installed")


def validate_worker_result(raw: bytes, version: str) -> dict[str, bytes]:
    if len(raw) > MAX_RESULT_BYTES:
        raise ValueError("target worker result is too large")
    try:
        data = json.loads(raw, object_pairs_hook=_unique_pairs)
    except RecursionError as exc:
        raise ValueError("target worker result nesting is too deep") from exc
    if not isinstance(data, dict) or set(data) != {"protocol", "version", "files"}:
        raise ValueError("invalid target worker result")
    if type(data["protocol"]) is not int or data["protocol"] != 1 or data["version"] != version:
        raise ValueError("target worker version/protocol mismatch")
    files = data["files"]
    if not isinstance(files, dict) or not 0 < len(files) <= MAX_ENTRIES:
        raise ValueError("invalid target file inventory")
    result = {}
    for name, encoded in files.items():
        if not managed_path(name) or not isinstance(encoded, str):
            raise ValueError("invalid target file entry")
        result[name] = base64.b64decode(encoded, validate=True)
    return result


@dataclass
class Release:
    version: str
    python: str

    def render(self, project: Path, ai: str, language: str) -> dict[str, bytes]:
        with tempfile.TemporaryDirectory(prefix="codexspec-prepare-") as temporary:
            directory = Path(temporary).resolve()
            snapshot = directory / "snapshot" / (project.resolve().name or "project")
            snapshot.mkdir(parents=True)
            for name in ("CLAUDE.md", "AGENTS.md", ".codexspec/.gitignore"):
                source = checked_path(project, name)
                if source.exists():
                    target = snapshot / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(source.read_bytes())
            result = directory / "result.json"
            run_process(
                [
                    self.python,
                    "-I",
                    "-m",
                    "codexspec.installations.worker",
                    str(snapshot),
                    str(result),
                    ai,
                    language,
                ],
                cwd=directory,
            )
            if result.is_symlink() or not result.is_file() or result.stat().st_size > MAX_RESULT_BYTES:
                raise ValueError("target worker did not produce a valid result")
            return validate_worker_result(result.read_bytes(), self.version)


@contextmanager
def acquire_release():
    version = resolve_latest()
    with tempfile.TemporaryDirectory(prefix="codexspec-release-") as temporary:
        directory = Path(temporary).resolve()
        environment = directory / "runtime"
        run_process([sys.executable, "-I", "-m", "venv", str(environment)], cwd=directory)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        run_process(
            [
                str(python),
                "-I",
                "-m",
                "pip",
                "--disable-pip-version-check",
                "--no-input",
                "install",
                "--index-url",
                "https://pypi.org/simple",
                f"codexspec=={version}",
            ],
            cwd=directory,
            timeout=300,
        )
        # A worker preflight validates protocol and exact runtime before any project write.
        release = Release(version, str(python))
        probe = directory / "probe"
        probe.mkdir()
        release.render(probe, "codex", "en")
        yield release
