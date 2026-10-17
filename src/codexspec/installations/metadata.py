"""Installation provenance and content checks; never infer permission to overwrite."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from packaging.version import InvalidVersion, Version

METADATA = ".codexspec/installation.json"
MAX_METADATA_BYTES = 4 * 1024 * 1024
MAX_ENTRIES = 10000
CONTEXT_FILES = {"AGENTS.md", "CLAUDE.md"}
PREFIXES = (".codexspec/scripts/", ".codexspec/templates/docs/", ".codexspec/review-code/")
BLOCK = re.compile(
    r"<!-- CODEXSPEC(?: (?:PROFILE|COMMITS|SPECS))? START -->.*?<!-- CODEXSPEC(?: (?:PROFILE|COMMITS|SPECS))? END -->",
    re.S,
)


@dataclass
class Inspection:
    version: str | None = None
    state: str = "no_baseline"
    differences: list[str] = field(default_factory=list)
    reason: str = ""


def managed_path(name: str) -> bool:
    """Admit only installation surfaces, never arbitrary project paths."""
    if not isinstance(name, str) or not name or "\\" in name or ":" in name or "\x00" in name:
        return False
    path = PurePosixPath(name)
    if path.is_absolute() or any(p in {".", ".."} for p in name.split("/")) or str(path) != name:
        return False
    return (
        name in CONTEXT_FILES | {".codexspec/.gitignore"}
        or name.startswith(PREFIXES)
        or name.startswith(".claude/commands/codexspec/")
        or (name.startswith(".agents/skills/codexspec-") and name.endswith("/SKILL.md"))
    )


def checked_path(root: Path, name: str, *, writing: bool = False) -> Path:
    if name not in {METADATA, ".codexspec/config.yml"} and not managed_path(name):
        raise ValueError(f"unsupported installation path: {name}")
    root = root.absolute()
    path = root / name
    for part in [
        *reversed(root.parents),
        root,
        *(root / Path(*Path(name).parts[:i]) for i in range(1, len(Path(name).parts) + 1)),
    ]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode):
            raise ValueError(f"symbolic link: {part}")
        if part != path and not stat.S_ISDIR(info.st_mode):
            raise ValueError(f"not a directory: {part}")
        if part == path and not stat.S_ISREG(info.st_mode):
            raise ValueError(f"not a regular file: {part}")
        if writing and part == path and info.st_nlink != 1:
            raise ValueError(f"shared hard link: {part}")
    return path


def projection(name: str, data: bytes) -> bytes:
    """Schema-1 text projection: UTF-8 with LF; context includes managed blocks only."""
    text = data.decode("utf-8").replace("\r\n", "\n")
    if name in CONTEXT_FILES:
        blocks = BLOCK.findall(text)
        # The constitution import is managed by the Claude installer.
        if "@.codexspec/memory/constitution.md" in text.splitlines():
            blocks.append("@.codexspec/memory/constitution.md")
        text = "\n".join(blocks)
    elif name == ".codexspec/.gitignore":
        text = "\n".join(line for line in text.splitlines() if line.strip() == ".runtime/")
    return text.encode("utf-8")


def digest(name: str, data: bytes) -> str:
    return hashlib.sha256(projection(name, data)).hexdigest()


def metadata_bytes(version: str, ai: str, language: str, files: dict[str, bytes]) -> bytes:
    Version(version)
    if ai not in {"claude", "codex", "both"} or not files or len(files) > MAX_ENTRIES:
        raise ValueError("invalid installation metadata")
    if any(not managed_path(name) for name in files):
        raise ValueError("unsupported installation path")
    data = {
        "schema_version": 1,
        "representation": "utf8-lf-managed-v1",
        "installed_version": version,
        "ai": ai,
        "interaction_language": language,
        "files": {name: digest(name, data) for name, data in sorted(files.items())},
    }
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate metadata key: {key}")
        result[key] = value
    return result


def read_metadata(root: Path) -> dict | None:
    path = checked_path(root, METADATA)
    if not path.exists():
        return None
    if path.stat().st_size > MAX_METADATA_BYTES:
        raise ValueError("installation metadata too large")
    try:
        data = json.loads(path.read_bytes(), object_pairs_hook=_unique_pairs)
    except RecursionError as exc:
        raise ValueError("installation metadata nesting is too deep") from exc
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("unsupported installation metadata schema")
    if data.get("representation") != "utf8-lf-managed-v1":
        raise ValueError("unsupported checksum representation")
    version = data.get("installed_version")
    if version is not None:
        if not isinstance(version, str):
            raise ValueError("invalid installation version")
        Version(version)
    files = data.get("files")
    if not isinstance(files, dict) or not 0 < len(files) <= MAX_ENTRIES:
        raise ValueError("invalid managed-file list")
    for name, checksum in files.items():
        if not managed_path(name) or not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError(f"invalid managed-file entry: {name}")
    return data


def inspect_installation(root: Path) -> Inspection:
    result = Inspection()
    try:
        metadata = read_metadata(root)
        if metadata is None:
            return result
        result.version = metadata.get("installed_version")
        for name, expected in metadata["files"].items():
            path = checked_path(root, name)
            if not path.exists() or digest(name, path.read_bytes()) != expected:
                result.differences.append(name)
        result.state = "inconsistent" if result.differences else "consistent"
    except (OSError, ValueError, InvalidVersion) as exc:
        result.state = "invalid"
        result.reason = str(exc)
    return result


def atomic_write(path: Path, data: bytes, mode: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".codexspec-install-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        if mode is not None:
            os.chmod(temporary, mode)
        else:
            os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def publish_metadata(root: Path, version: str, ai: str, language: str, files: dict[str, bytes]) -> None:
    for name, expected in files.items():
        path = checked_path(root, name)
        if not path.exists() or digest(name, path.read_bytes()) != digest(name, expected):
            raise ValueError(f"installed content does not match expected release: {name}")
    destination = checked_path(root, METADATA, writing=True)
    atomic_write(destination, metadata_bytes(version, ai, language, files))
