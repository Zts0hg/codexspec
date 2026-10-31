"""Raw descriptor ownership regressions for the POSIX review writers."""

import errno
import json
import os
import stat
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

from codexspec.distill_review.models import ReviewDraft
from codexspec.distill_review.session import AtomicWriteConflictError, SessionStore
from codexspec.distill_review.transaction import ProfileTransaction

pytestmark = pytest.mark.skipif(
    os.name != "posix" or not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW"),
    reason="requires POSIX pinned directory descriptors",
)

WRITERS = {"session": SessionStore._atomic_at, "profile": ProfileTransaction._install_exclusive_at}


def _is_open(fd: int) -> bool:
    try:
        os.fstat(fd)
    except OSError as exc:
        if exc.errno != errno.EBADF:
            raise
        return False
    return True


@contextmanager
def _tracked_writer(tmp_path, monkeypatch, kind):
    directory = os.open(tmp_path, os.O_RDONLY | os.O_DIRECTORY)
    real_open, real_close = os.open, os.close
    owned, closed = [], []

    def tracked_open(*args, **kwargs):
        fd = real_open(*args, **kwargs)
        owned.append(fd)
        return fd

    def tracked_close(fd):
        closed.append(fd)
        return real_close(fd)

    try:
        with monkeypatch.context() as patch:
            patch.setattr(os, "open", tracked_open)
            patch.setattr(os, "close", tracked_close)
            yield WRITERS[kind], directory, owned, closed, patch
    finally:
        # Even a red test must not leak its probe-owned descriptor into pytest.
        for fd in owned:
            if fd not in closed and _is_open(fd):
                real_close(fd)
        real_close(directory)


@pytest.mark.parametrize("kind", WRITERS)
@pytest.mark.parametrize("stage", ["fdopen", "fchmod", "write", "flush", "file_sync", "install", "dir_sync"])
def test_writer_failure_releases_raw_fd(tmp_path, monkeypatch, kind, stage):
    real_fdopen, real_fsync = os.fdopen, os.fsync
    failure = OSError(errno.EIO, stage)

    def fail(*args, **kwargs):
        raise failure

    class BorrowedStream:
        def __init__(self, *args, **kwargs):
            self.stream = real_fdopen(*args, **kwargs)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return self.stream.__exit__(*args)

        def write(self, content):
            if stage == "write":
                raise failure
            return self.stream.write(content)

        def flush(self):
            if stage == "flush":
                raise failure
            return self.stream.flush()

    with _tracked_writer(tmp_path, monkeypatch, kind) as (writer, directory, owned, closed, patch):
        if stage in {"fdopen", "fchmod"}:
            patch.setattr(os, stage, fail)
        elif stage in {"write", "flush"}:
            patch.setattr(os, "fdopen", BorrowedStream)
        elif stage in {"file_sync", "dir_sync"}:

            def fsync(fd):
                if (fd == directory) == (stage == "dir_sync"):
                    raise failure
                return real_fsync(fd)

            patch.setattr(os, "fsync", fsync)
        else:
            patch.setattr(os, "replace" if kind == "session" else "link", fail)
        with pytest.raises(OSError) as caught:
            writer(directory, "target", b"content")
        assert caught.value is failure
        assert len(owned) == 1
        assert closed == owned
        assert not _is_open(owned[0])
        assert _is_open(directory)
        assert not list(tmp_path.glob(".*.tmp"))
        assert (tmp_path / "target").exists() == (stage == "dir_sync")
        if stage == "dir_sync":
            assert (tmp_path / "target").read_bytes() == b"content"


@pytest.mark.parametrize("kind", WRITERS)
def test_failed_open_does_not_close_unowned_fd(tmp_path, monkeypatch, kind):
    with _tracked_writer(tmp_path, monkeypatch, kind) as (writer, directory, owned, closed, patch):

        def fail(*args, **kwargs):
            raise OSError(errno.EMFILE, "injected open failure")

        patch.setattr(os, "open", fail)
        with pytest.raises(OSError, match="injected open failure"):
            writer(directory, "target", b"content")
        assert owned == closed == []
        assert _is_open(directory)
        assert list(tmp_path.iterdir()) == []


def test_exclusive_conflict_releases_fd_without_overwrite(tmp_path, monkeypatch):
    (tmp_path / "target").write_bytes(b"original")
    with _tracked_writer(tmp_path, monkeypatch, "profile") as (writer, directory, owned, closed, _):
        with pytest.raises(AtomicWriteConflictError):
            writer(directory, "target", b"replacement")
        assert len(owned) == 1
        assert closed == owned
        assert not _is_open(owned[0])
        assert _is_open(directory)
        assert (tmp_path / "target").read_bytes() == b"original"
        assert not list(tmp_path.glob(".*.tmp"))


@pytest.mark.parametrize("kind", WRITERS)
@pytest.mark.parametrize("operation_fails", [False, True])
def test_unlink_failure_follows_close_and_preserves_context(tmp_path, monkeypatch, kind, operation_fails):
    operation_error = OSError(errno.EIO, "operation failed")
    cleanup_error = OSError(errno.EACCES, "unlink failed")
    with _tracked_writer(tmp_path, monkeypatch, kind) as (writer, directory, owned, closed, patch):

        def fail_sync(fd):
            raise operation_error

        def fail_unlink(*args, **kwargs):
            assert closed == owned
            assert not _is_open(owned[0])
            raise cleanup_error

        patch.setattr(os, "unlink", fail_unlink)
        if operation_fails:
            patch.setattr(os, "fsync", fail_sync)
        with pytest.raises(OSError) as caught:
            writer(directory, "target", b"content")
        assert caught.value is cleanup_error
        if operation_fails:
            assert caught.value.__context__ is operation_error
        assert closed == owned
        assert _is_open(directory)


@pytest.mark.parametrize("kind", WRITERS)
@pytest.mark.parametrize("unlink_fails", [False, True])
def test_close_failure_is_not_retried_and_cleanup_still_runs(tmp_path, monkeypatch, kind, unlink_fails):
    real_close, real_open, real_unlink = os.close, os.open, os.unlink
    close_error = OSError(errno.EIO, "close failed")
    unlink_error = OSError(errno.EACCES, "unlink failed")
    operation_error = OSError(errno.EIO, "operation failed")
    sentinel = []
    attempts, unlinks = [], []
    with _tracked_writer(tmp_path, monkeypatch, kind) as (writer, directory, owned, closed, patch):

        def close_then_reuse(fd):
            attempts.append(fd)
            closed.append(fd)
            real_close(fd)
            replacement = real_open(os.devnull, os.O_RDONLY)
            if replacement != fd:
                os.dup2(replacement, fd)
                real_close(replacement)
            sentinel.append(fd)
            raise close_error

        def unlink(*args, **kwargs):
            unlinks.append(args[0])
            assert attempts == owned
            if unlink_fails:
                raise unlink_error
            return real_unlink(*args, **kwargs)

        def fail_sync(fd):
            raise operation_error

        patch.setattr(os, "close", close_then_reuse)
        patch.setattr(os, "unlink", unlink)
        patch.setattr(os, "fsync", fail_sync)
        try:
            with pytest.raises(OSError) as caught:
                writer(directory, "target", b"content")
            assert len(owned) == 1
            assert attempts == owned
            assert len(unlinks) == 1
            assert caught.value is (unlink_error if unlink_fails else close_error)
            assert close_error.__context__ is operation_error
            if unlink_fails:
                assert unlink_error.__context__ is close_error
            assert len(sentinel) == 1 and _is_open(sentinel[0])
            assert _is_open(directory)
            assert bool(list(tmp_path.glob(".*.tmp"))) == unlink_fails
        finally:
            for fd in sentinel:
                if _is_open(fd):
                    real_close(fd)


def _probe(mode: str, root: Path) -> None:
    """Called in a fresh interpreter, not in pytest's long-lived process."""
    import fcntl

    from tests.test_distill_review_persistence import (
        test_transaction_applies_mixed_batch_and_detects_hash_conflict,
        test_transaction_rolls_back_and_recovery_restores_old_bytes,
    )

    def descriptors():
        result = set()
        for fd in range(4096):
            try:
                fcntl.fcntl(fd, fcntl.F_GETFD)
            except OSError as exc:
                if exc.errno != errno.EBADF:
                    raise
            else:
                result.add(fd)
        return result

    baseline = descriptors()
    assert max(baseline, default=0) < 2048
    if mode == "primitives":
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            pinned_baseline = descriptors()
            for kind, writer in WRITERS.items():
                for index in range(16):
                    name = "draft" if kind == "session" else f"profile-{index}"
                    writer(directory, name, b"content")
                    assert (root / name).read_bytes() == b"content"
                    assert stat.S_IMODE((root / name).stat().st_mode) == (0o600 if kind == "session" else 0o644)
                    assert _is_open(directory)
                    assert descriptors() == pinned_baseline, (kind, index, descriptors() - pinned_baseline)
            assert not list(root.glob(".*.tmp"))
        finally:
            os.close(directory)
    elif mode == "store":
        (root / ".codexspec").mkdir()
        store = SessionStore(root)
        for index in range(16):
            store.save(ReviewDraft(revision=index))
            assert store.load().revision == index
            assert descriptors() == baseline, "draft persistence leaked"
            store.save_active({"iteration": index})
            assert store.load_active() == {"iteration": index}
            assert descriptors() == baseline, "active persistence leaked"
            store.save_transaction({"iteration": index})
            assert json.loads(store.load_transaction_bytes()) == {"iteration": index}
            assert descriptors() == baseline, "journal persistence leaked"
    elif mode == "transaction":
        apply_root, recover_root = root / "apply", root / "recover"
        apply_root.mkdir()
        recover_root.mkdir()
        test_transaction_applies_mixed_batch_and_detects_hash_conflict(apply_root)
        assert descriptors() == baseline, "transaction apply/conflict leaked"
        with pytest.MonkeyPatch.context() as patch:
            test_transaction_rolls_back_and_recovery_restores_old_bytes(recover_root, patch)
        assert descriptors() == baseline, "transaction prepare/rollback/recover leaked"
    else:
        raise AssertionError(mode)
    assert descriptors() == baseline
    print(f"{mode}: FD baseline restored")


@pytest.mark.parametrize("mode", ["primitives", "store", "transaction"])
def test_repeated_operations_restore_fd_baseline_in_subprocess(tmp_path, mode):
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join((str(root / "src"), str(root)))
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; from tests.test_distill_review_fd_lifetime import _probe; "
            "import sys; _probe(sys.argv[1], Path(sys.argv[2]).resolve())",
            mode,
            str(tmp_path),
        ],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"{mode}: FD baseline restored" in result.stdout
