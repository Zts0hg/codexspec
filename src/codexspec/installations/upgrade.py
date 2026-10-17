"""Explicit update plans checked against Git before any project writes."""

from __future__ import annotations

import os
import stat
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from packaging.version import Version

from .discovery import ReadOnlyGit
from .metadata import (
    BLOCK,
    CONTEXT_FILES,
    METADATA,
    atomic_write,
    checked_path,
    digest,
    managed_path,
    metadata_bytes,
    read_metadata,
)


class UnsafeProjectError(ValueError):
    """Safety inspection refused this project before application began."""


@dataclass(frozen=True)
class FileState:
    data: bytes | None
    mode: int | None


@dataclass
class Plan:
    root: Path
    version: str
    files: dict[str, bytes]
    changes: dict[str, bytes | None]
    originals: dict[str, FileState]
    inputs: dict[str, FileState] = field(default_factory=dict)


def state(root: Path, name: str) -> FileState:
    path = checked_path(root, name, writing=True)
    try:
        info = path.stat()
        return FileState(path.read_bytes(), stat.S_IMODE(info.st_mode))
    except FileNotFoundError:
        return FileState(None, None)


def project_options(root: Path) -> tuple[str, str]:
    from codexspec.i18n import normalize_locale

    config = checked_path(root, ".codexspec/config.yml")
    try:
        data = yaml.safe_load(config.read_text(encoding="utf-8")) if config.exists() else {}
    except RecursionError as exc:
        raise ValueError("project configuration nesting is too deep") from exc
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read project configuration: {exc}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("invalid project configuration")
    project = data.get("project", {})
    languages = data.get("language", {})
    if not isinstance(project, dict) or not isinstance(languages, dict):
        raise ValueError("invalid project/language configuration")
    ai = project.get("ai")
    if ai is None:
        claude = (root / ".claude/commands/codexspec").is_dir()
        codex = any((root / ".agents/skills").glob("codexspec-*/SKILL.md"))
        ai = "both" if claude and codex else "claude" if claude else "codex" if codex else None
    if not isinstance(ai, str) or ai not in {"claude", "codex", "both"}:
        raise ValueError("cannot determine existing Claude/Codex installation choice")
    language = languages.get("interaction", languages.get("output", "en"))
    if not isinstance(language, str) or not language.strip():
        raise ValueError("invalid interaction language")
    return ai, normalize_locale(language)


def user_body(data: bytes) -> str:
    text = data.decode("utf-8").replace("\r\n", "\n")
    text = BLOCK.sub("", text)
    return "\n".join(line for line in text.splitlines() if line != "@.codexspec/memory/constitution.md").strip()


def prepare_plan(root: Path, version: str, ai: str, language: str, files: dict[str, bytes]) -> Plan:
    """Make the entire proposed write set explicit without modifying the project."""
    root = root.absolute()
    target = Version(version)
    previous = read_metadata(root)
    if previous and previous.get("installed_version") and Version(previous["installed_version"]) > target:
        raise ValueError(f"recorded version is newer than target {version}")
    if not files or any(not managed_path(name) or not isinstance(data, bytes) for name, data in files.items()):
        raise ValueError("invalid target file inventory")
    changes: dict[str, bytes | None] = {}
    originals = {}
    for name, desired in files.items():
        original = state(root, name)
        if name in CONTEXT_FILES and original.data is not None and user_body(original.data) != user_body(desired):
            raise ValueError(f"target would replace project-owned context: {name}")
        if original.data != desired:
            changes[name] = desired
            originals[name] = original
    # Preserve the existing init migration for the one explicitly retired entry.
    retired = set((previous or {}).get("files", {}))
    for replacement, old in (
        (".claude/commands/codexspec/design-to-plan.md", ".claude/commands/codexspec/spec-to-plan.md"),
        (".agents/skills/codexspec-design-to-plan/SKILL.md", ".agents/skills/codexspec-spec-to-plan/SKILL.md"),
    ):
        if replacement in files:
            retired.add(old)
    # Other retirements require prior ownership evidence; custom extensions survive.
    for name in sorted(retired):
        if name not in files:
            if name in CONTEXT_FILES or name == ".codexspec/.gitignore":
                raise ValueError(f"target omits previously enabled project context: {name}")
            original = state(root, name)
            if original.data is not None:
                changes[name] = None
                originals[name] = original
    metadata = metadata_bytes(version, ai, language, files)
    original = state(root, METADATA)
    if original.data != metadata:
        changes[METADATA] = metadata
        originals[METADATA] = original
    inputs = {name: state(root, name) for name in (".codexspec/config.yml", "CLAUDE.md", "AGENTS.md")}
    return Plan(root, version, files, changes, originals, inputs)


def _entries(raw: bytes, *, index: bool) -> dict[str, tuple[str, str]]:
    result = {}
    for row in raw.split(b"\0"):
        if not row:
            continue
        attributes, name = row.split(b"\t", 1)
        mode, middle, last = attributes.decode("ascii").split()
        if index and last != "0":
            raise ValueError(f"unmerged affected file: {os.fsdecode(name)}")
        key = os.fsdecode(name)
        if key in result:
            raise ValueError(f"ambiguous Git entry: {key}")
        result[key] = (mode, middle if index else last)
    return result


def _normalizes_crlf(git: ReadOnlyGit, repository: Path, name: str) -> bool:
    """Read Git's conversion policy without invoking user-configured clean filters."""
    fields = git.run(repository, "check-attr", "-z", "text", "eol", "--", name).split(b"\0")
    if len(fields) != 7 or fields[-1] or fields[0] != os.fsencode(name) or fields[3] != os.fsencode(name):
        raise ValueError(f"cannot determine Git text policy: {name}")
    attributes = dict(zip(fields[1::3], fields[2::3]))
    text = attributes.get(b"text")
    if text == b"unset":
        return False
    if text == b"set":
        return True
    if text not in {b"unspecified", b"auto"}:
        return False
    if text == b"unspecified" and attributes.get(b"eol") in {b"lf", b"crlf"}:
        return True
    if text == b"unspecified":
        autocrlf = git.run(repository, "config", "--get", "core.autocrlf", check=False).strip().lower()
        enabled = (
            autocrlf == b"input"
            or git.run(repository, "config", "--bool", "--get", "core.autocrlf", check=False).strip() == b"true"
        )
        if not enabled:
            return False
    # Auto conversion excludes binary content; observed layout is evidence only
    # after an effective conversion policy has been established above.
    layout = git.run(repository, "ls-files", "--eol", "-z", "--", name).split(b"\t", 1)[0].split()
    return len(layout) >= 2 and layout[0] == b"i/lf" and layout[1] in {b"w/crlf", b"w/mixed"}


def preflight(plan: Plan) -> None:
    """Prove affected files clean, including edits hidden by index optimization flags."""
    git = ReadOnlyGit()
    root = plan.root
    repository = Path(os.fsdecode(git.run(root, "rev-parse", "--show-toplevel")).strip()).resolve()
    try:
        prefix = root.resolve().relative_to(repository).as_posix()
    except ValueError as exc:
        raise ValueError("installation does not belong to the inspected repository") from exc
    paths = {name: name if prefix == "." else f"{prefix}/{name}" for name in plan.changes}
    git.run(repository, "rev-parse", "--verify", "HEAD")
    for name, original in {**plan.inputs, **plan.originals}.items():
        if state(root, name) != original:
            raise ValueError(f"file changed after preparation: {name}")
    if not paths:
        return
    index = _entries(git.run(repository, "ls-files", "--stage", "-z", "--", *paths.values()), index=True)
    head = _entries(git.run(repository, "ls-tree", "-r", "-z", "HEAD", "--", *paths.values()), index=False)
    for name, git_name in paths.items():
        original = plan.originals[name]
        staged = index.get(git_name)
        committed = head.get(git_name)
        if staged != committed:
            raise ValueError(f"staged local modification: {name}")
        if staged is None:
            if original.data is not None:
                raise ValueError(f"untracked or ignored affected file: {name}")
            continue
        if staged[0] not in {"100644", "100755"}:
            raise ValueError(f"unsupported Git file type: {name}")
        if original.data is None:
            raise ValueError(f"locally deleted affected file: {name}")
        committed_data = git.run(repository, "cat-file", "blob", staged[1])
        # Observed CRLF bytes alone do not establish a clean Git conversion.
        actual = original.data
        if actual != committed_data and b"\r\n" in actual and _normalizes_crlf(git, repository, git_name):
            actual = actual.replace(b"\r\n", b"\n")
        if actual != committed_data:
            raise ValueError(f"unstaged local modification: {name}")
        filemode = git.run(repository, "config", "--get", "core.filemode", check=False).strip()
        if filemode == b"true" and bool(original.mode & 0o111) != (staged[0] == "100755"):
            raise ValueError(f"local executable-mode modification: {name}")


def apply_plan(plan: Plan) -> None:
    try:
        preflight(plan)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        raise UnsafeProjectError(str(exc)) from exc
    written = 0
    try:
        for name, desired in plan.changes.items():
            if name == METADATA:
                continue
            if state(plan.root, name) != plan.originals[name]:
                raise ValueError(f"file changed during application: {name}")
            path = checked_path(plan.root, name, writing=True)
            if desired is None:
                path.unlink()
            else:
                mode = plan.originals[name].mode
                if mode is None and name.startswith(".codexspec/scripts/") and name.endswith(".sh"):
                    mode = 0o755
                atomic_write(path, desired, mode)
            written += 1
        for name, expected in plan.files.items():
            current = checked_path(plan.root, name).read_bytes()
            if digest(name, current) != digest(name, expected):
                raise ValueError(f"final content does not match target: {name}")
        if METADATA in plan.changes:
            if state(plan.root, METADATA) != plan.originals[METADATA]:
                raise ValueError("installation metadata changed during application")
            atomic_write(checked_path(plan.root, METADATA, writing=True), plan.changes[METADATA])
    except (OSError, ValueError) as exc:
        if written:
            raise RuntimeError(f"partial upgrade; successful metadata not published: {exc}") from exc
        raise
