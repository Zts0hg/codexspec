"""Project-scoped persistence for recoverable distill-review state."""

from __future__ import annotations

import json
import os
import secrets
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, BinaryIO, Iterator

from codexspec.automation import GitRunner

from .models import ReviewDraft

RUNTIME_IGNORE_RULE = ".runtime/"
LEGACY_EXCLUDE_RULE = "/.codexspec/.runtime/"


class SessionError(RuntimeError):
    """Review runtime state is unavailable or invalid."""


class AtomicWriteConflictError(OSError):
    """The target changed after transaction preflight."""


_UNCONDITIONAL = object()


def _sync_directory(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        if os.name != "nt":
            raise
    finally:
        os.close(descriptor)


def atomic_bytes(
    path: Path,
    content: bytes,
    *,
    mode: int = 0o600,
    expected_content: bytes | None | object = _UNCONDITIONAL,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            if hasattr(os, "fchmod"):
                os.fchmod(stream.fileno(), mode)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if expected_content is not _UNCONDITIONAL:
            current = path.read_bytes() if path.exists() else None
            if current != expected_content:
                raise AtomicWriteConflictError(f"concurrent_write: {path}")
        os.replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())


def _append_unique_line(path: Path, line: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if line in {item.strip() for item in existing.splitlines()}:
        return
    prefix = existing
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    atomic_bytes(path, f"{prefix}{line}\n".encode("utf-8"), mode=0o644)


def ensure_runtime_ignored(project_root: Path, *, install_managed_file: bool) -> None:
    root = project_root.resolve()
    if install_managed_file:
        _append_unique_line(root / ".codexspec" / ".gitignore", RUNTIME_IGNORE_RULE)
        return
    git = GitRunner()
    inside = git.run(root, "rev-parse", "--is-inside-work-tree", check=False)
    if inside.returncode != 0:
        return
    ignored = git.run(root, "check-ignore", "-q", ".codexspec/.runtime/example", check=False)
    if ignored.returncode == 0:
        return
    result = git.run(root, "rev-parse", "--git-path", "info/exclude")
    exclude_path = Path(result.stdout.strip())
    if not exclude_path.is_absolute():
        exclude_path = root / exclude_path
    _append_unique_line(exclude_path, LEGACY_EXCLUDE_RULE)


class SessionStore:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root.resolve()
        self.runtime_dir = self.project_root / ".codexspec" / ".runtime" / "distill-review"
        self.draft_path = self.runtime_dir / "draft.json"
        self.active_path = self.runtime_dir / "active.json"
        self.lock_path = self.runtime_dir / "writer.lock"
        self.transaction_path = self.runtime_dir / "transaction.json"
        self._runtime_identity: tuple[int, int] | None = None

    def _validate_runtime_path(self) -> None:
        paths = (
            self.project_root / ".codexspec",
            self.project_root / ".codexspec" / ".runtime",
            self.runtime_dir,
            self.draft_path,
            self.active_path,
            self.lock_path,
            self.transaction_path,
        )
        for path in paths:
            if path.is_symlink():
                raise SessionError(f"runtime_symlink: {path}")
        try:
            self.runtime_dir.resolve().relative_to(self.project_root)
        except ValueError as exc:
            raise SessionError(f"runtime_outside_project: {self.runtime_dir}") from exc

    @property
    def _supports_pinned_runtime(self) -> bool:
        return os.name != "nt" and hasattr(os, "O_DIRECTORY") and hasattr(os, "O_NOFOLLOW")

    @contextmanager
    def _runtime_directory(self, *, create: bool) -> Iterator[int | None]:
        """Open the runtime directory without following a swapped path component."""
        if not self._supports_pinned_runtime:
            self._validate_runtime_path()
            if create:
                self.runtime_dir.mkdir(parents=True, exist_ok=True)
                self._validate_runtime_path()
            yield None
            return
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        descriptors: list[int] = []
        missing = False
        try:
            descriptor = os.open(self.project_root, flags)
            descriptors.append(descriptor)
            for component in (".codexspec", ".runtime", "distill-review"):
                if create and component != ".codexspec":
                    try:
                        os.mkdir(component, 0o700, dir_fd=descriptor)
                    except FileExistsError:
                        pass
                try:
                    descriptor = os.open(component, flags, dir_fd=descriptor)
                except FileNotFoundError:
                    if create:
                        raise
                    missing = True
                    break
                descriptors.append(descriptor)
            if not missing:
                opened = os.fstat(descriptors[-1])
                identity = (opened.st_dev, opened.st_ino)
                if self._runtime_identity is None:
                    self._runtime_identity = identity
                elif self._runtime_identity != identity:
                    raise SessionError(f"runtime_replaced: {self.runtime_dir}")
        except SessionError:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
            raise
        except OSError as exc:
            for descriptor in reversed(descriptors):
                os.close(descriptor)
            raise SessionError(f"runtime_symlink: {self.runtime_dir}") from exc
        try:
            yield None if missing else descriptors[-1]
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)

    @staticmethod
    def _read_at(directory: int, name: str) -> bytes | None:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        try:
            descriptor = os.open(name, flags, dir_fd=directory)
        except FileNotFoundError:
            return None
        try:
            with os.fdopen(descriptor, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(descriptor)

    @staticmethod
    def _atomic_at(directory: int, name: str, content: bytes, *, mode: int = 0o600) -> None:
        temporary = f".{name}.{secrets.token_hex(8)}.tmp"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(temporary, flags, mode, dir_fd=directory)
        try:
            with os.fdopen(descriptor, "wb", closefd=False) as stream:
                if hasattr(os, "fchmod"):
                    os.fchmod(descriptor, mode)
                stream.write(content)
                stream.flush()
                os.fsync(descriptor)
            os.replace(temporary, name, src_dir_fd=directory, dst_dir_fd=directory)
            os.fsync(directory)
        finally:
            try:
                os.unlink(temporary, dir_fd=directory)
            except FileNotFoundError:
                pass

    def _write_runtime(self, name: str, content: bytes) -> None:
        with self._runtime_directory(create=True) as directory:
            if directory is None:
                atomic_bytes(self.runtime_dir / name, content)
            else:
                self._atomic_at(directory, name, content)

    def _read_runtime(self, name: str) -> bytes | None:
        with self._runtime_directory(create=False) as directory:
            if directory is None:
                if self._supports_pinned_runtime:
                    return None
                path = self.runtime_dir / name
                return path.read_bytes() if path.exists() else None
            return self._read_at(directory, name)

    def _remove_runtime(self, name: str) -> None:
        with self._runtime_directory(create=False) as directory:
            if directory is None:
                if self._supports_pinned_runtime:
                    return
                (self.runtime_dir / name).unlink(missing_ok=True)
                return
            try:
                os.unlink(name, dir_fd=directory)
                os.fsync(directory)
            except FileNotFoundError:
                pass

    @staticmethod
    def _json_bytes(value: Any) -> bytes:
        return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()

    def prepare(self) -> None:
        self._validate_runtime_path()
        ensure_runtime_ignored(self.project_root, install_managed_file=False)
        with self._runtime_directory(create=True):
            pass

    def save(self, draft: ReviewDraft) -> None:
        self.prepare()
        self._write_runtime(self.draft_path.name, self._json_bytes(draft.to_dict()))

    def load(self) -> ReviewDraft | None:
        source = self._read_runtime(self.draft_path.name)
        if source is None:
            return None
        try:
            value = json.loads(source)
            if not isinstance(value, dict):
                raise ValueError("invalid_draft_shape")
            return ReviewDraft.from_dict(value)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            raise SessionError(
                f"invalid_draft: {self.draft_path}: {exc}; rerun with --discard-draft to remove it"
            ) from exc

    def discard(self) -> None:
        self._remove_runtime(self.draft_path.name)

    def save_active(self, metadata: dict[str, Any]) -> None:
        self.prepare()
        self._write_runtime(self.active_path.name, self._json_bytes(metadata))

    def load_active(self) -> dict[str, Any]:
        source = self._read_runtime(self.active_path.name)
        if source is None:
            return {}
        try:
            value = json.loads(source)
        except (OSError, json.JSONDecodeError):
            return {}
        return value if isinstance(value, dict) else {}

    def discard_active(self) -> None:
        self._remove_runtime(self.active_path.name)

    def save_transaction(self, value: Any) -> None:
        self.prepare()
        self._write_runtime(self.transaction_path.name, self._json_bytes(value))

    def load_transaction_bytes(self) -> bytes | None:
        return self._read_runtime(self.transaction_path.name)

    def transaction_exists(self) -> bool:
        return self.load_transaction_bytes() is not None

    def discard_transaction(self) -> None:
        self._remove_runtime(self.transaction_path.name)

    def open_lock_file(self) -> BinaryIO:
        """Open the writer lock through the pinned runtime directory on POSIX."""
        with self._runtime_directory(create=True) as directory:
            if directory is None:
                return self.lock_path.open("a+b")
            flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(self.lock_path.name, flags, 0o600, dir_fd=directory)
            return os.fdopen(descriptor, "a+b")
