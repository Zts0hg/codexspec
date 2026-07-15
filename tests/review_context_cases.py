"""Shared Git fixtures for review-context resolver contract tests."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

FEATURE = "2026-0714-1200ab-review-context"
REQUIRED_ARTIFACTS = ("requirements.md", "spec.md", "plan.md", "tasks.md")


def git(repo: Path, *args: str, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run Git with deterministic test identity and no global config dependency."""

    command = [
        "git",
        "-c",
        "user.name=CodexSpec Tests",
        "-c",
        "user.email=tests@codexspec.invalid",
        *args,
    ]
    return subprocess.run(
        command,
        cwd=repo,
        input=input_text,
        text=True,
        capture_output=True,
        check=check,
    )


def write(repo: Path, relative: str, content: str | bytes) -> Path:
    """Write one fixture file beneath the repository."""

    path = repo / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def init_repository(tmp_path: Path, *, branch: str = "main") -> Path:
    """Create a repository with one committed baseline and CodexSpec directory."""

    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", branch)
    write(repo, "src/base.txt", "base\n")
    write(repo, ".gitignore", "ignored.tmp\n")
    (repo / ".codexspec" / "specs").mkdir(parents=True)
    git(repo, "add", ".")
    git(repo, "commit", "-m", "baseline")
    return repo


def create_feature_artifacts(repo: Path, feature: str = FEATURE) -> Path:
    """Create the complete authoritative artifact set for one feature."""

    feature_dir = repo / ".codexspec" / "specs" / feature
    feature_dir.mkdir(parents=True, exist_ok=True)
    for artifact in REQUIRED_ARTIFACTS:
        (feature_dir / artifact).write_text(f"# {artifact}\n", encoding="utf-8")
    return feature_dir


def create_feature_change(repo: Path, feature: str = FEATURE) -> Path:
    """Create committed, staged, unstaged, untracked, and ignored changes."""

    git(repo, "switch", "-c", feature)
    feature_dir = create_feature_artifacts(repo, feature)
    write(repo, "src/committed.txt", "committed\n")
    write(repo, "src/layered.txt", "committed layer\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "feature commit")

    write(repo, "src/staged.txt", "staged\n")
    write(repo, "src/layered.txt", "staged layer\n")
    git(repo, "add", "src/staged.txt", "src/layered.txt")

    write(repo, "src/base.txt", "unstaged\n")
    write(repo, "src/layered.txt", "unstaged layer\n")
    write(repo, "src/untracked.txt", "untracked\n")
    write(repo, "ignored.tmp", "ignored\n")
    return feature_dir


def repository_snapshot(repo: Path) -> dict[str, Any]:
    """Capture state that a read-only resolver must preserve."""

    tracked = git(repo, "ls-files", "-z").stdout.split("\0")
    tracked_hashes: dict[str, str] = {}
    for relative in tracked:
        if not relative:
            continue
        path = repo / relative
        if path.is_file() and not path.is_symlink():
            tracked_hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif path.is_symlink():
            tracked_hashes[relative] = f"symlink:{os.readlink(path)}"
        else:
            tracked_hashes[relative] = "missing"

    return {
        "head": git(repo, "rev-parse", "HEAD").stdout.strip(),
        "branch": git(repo, "branch", "--show-current").stdout.strip(),
        "refs": git(repo, "for-each-ref", "--format=%(refname) %(objectname)").stdout,
        "status": git(repo, "status", "--porcelain=v2", "--untracked-files=all", "-z").stdout,
        "tracked_hashes": tracked_hashes,
    }


def parse_manifest(stdout: str) -> dict[str, Any]:
    """Parse and minimally validate one resolver JSON document."""

    manifest = json.loads(stdout)
    assert manifest["schema_version"] == "1"
    assert manifest["status"] in {"ok", "error"}
    if manifest["status"] == "ok":
        for key in ("mode", "selector", "arguments", "repository", "target", "feature", "inventory", "counts"):
            assert key in manifest
    else:
        assert set(manifest["error"]) >= {"code", "message", "hint"}
    return manifest


def inventory_by_path(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Index inventory records by normalized repository-relative path."""

    return {entry["path"]: entry for entry in manifest["inventory"]}


def normalize_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    """Normalize ordering and platform path separators for parity assertions."""

    normalized = json.loads(json.dumps(manifest))
    if normalized.get("status") != "ok":
        return normalized
    normalized["repository"]["root"] = "<repo>"
    feature_path = normalized["feature"].get("path")
    if feature_path:
        normalized["feature"]["path"] = feature_path.replace("\\", "/")
    for entry in normalized["inventory"]:
        entry["path"] = entry["path"].replace("\\", "/")
        if entry.get("old_path"):
            entry["old_path"] = entry["old_path"].replace("\\", "/")
        entry["segments"] = sorted(entry["segments"])
    normalized["inventory"] = sorted(normalized["inventory"], key=lambda item: item["path"])
    normalized["feature"]["artifacts"] = sorted(
        normalized["feature"].get("artifacts", []), key=lambda item: item["name"]
    )
    return normalized
