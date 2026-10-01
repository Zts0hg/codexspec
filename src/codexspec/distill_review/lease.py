"""Single-writer ownership for manual profile review."""

from __future__ import annotations

import errno
import os
import time
from pathlib import Path
from typing import Any, BinaryIO

from codexspec.automation import FileLock, FileLockBusyError

from .session import SessionStore


class ActiveSessionError(RuntimeError):
    def __init__(self, metadata: dict[str, Any]) -> None:
        super().__init__("active_review_session")
        self.metadata = metadata


class ReviewLease:
    def __init__(self, project_root: Path) -> None:
        self.store = SessionStore(project_root)
        self._lock: FileLock | None = None
        self._lock_file: BinaryIO | None = None

    def acquire(self, metadata: dict[str, Any]) -> None:
        self.store.prepare()
        if os.name == "nt":  # pragma: no cover - exercised on Windows CI
            lock = FileLock(self.store.lock_path, blocking=False)
            try:
                lock.__enter__()
            except FileLockBusyError as exc:
                raise ActiveSessionError(self.store.load_active()) from exc
            self._lock = lock
        else:
            import fcntl

            lock_file = self.store.open_lock_file()
            try:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                lock_file.close()
                if exc.errno in {errno.EACCES, errno.EAGAIN}:
                    raise ActiveSessionError(self.store.load_active()) from exc
                raise
            self._lock_file = lock_file
        try:
            self.store.save_active(
                {
                    "protocol_version": 1,
                    "pid": os.getpid(),
                    "started_at": time.time(),
                    **metadata,
                }
            )
        except Exception:
            self._release_lock()
            raise

    def release(self) -> None:
        if self._lock is None and self._lock_file is None:
            return
        try:
            self.store.discard_active()
        finally:
            self._release_lock()

    def _release_lock(self) -> None:
        if self._lock is not None:
            self._lock.__exit__(None, None, None)
            self._lock = None
        if self._lock_file is not None:
            import fcntl

            try:
                fcntl.flock(self._lock_file.fileno(), fcntl.LOCK_UN)
            finally:
                self._lock_file.close()
                self._lock_file = None

    def update(self, metadata: dict[str, Any]) -> None:
        """Replace active metadata while retaining the acquired OS lock."""
        if self._lock is None and self._lock_file is None:
            raise RuntimeError("review_lease_not_held")
        self.store.save_active(
            {
                "protocol_version": 1,
                "pid": os.getpid(),
                "started_at": time.time(),
                **metadata,
            }
        )

    def __enter__(self) -> ReviewLease:
        self.acquire({})
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.release()
