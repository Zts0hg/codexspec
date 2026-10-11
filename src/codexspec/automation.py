"""Deterministic repository automation used by blueprint and auto-dev."""

from __future__ import annotations

import base64
import errno
import json
import os
import re
import secrets
import stat
import tempfile
import time
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, Sequence

from .blueprint import apply_operation
from .commit_runtime import AutomationError as AutomationError
from .commit_runtime import GitRunner as GitRunner

FIXED_BRANCH = "codexspec/auto-dev"
WORKTREE_BASENAME = "worktree-for-codexspec-auto-dev"
BLUEPRINT_PATH = Path(".codexspec/blueprint.md")
AUTO_DEV_STALE_AFTER_SECONDS = 300.0
AUTO_DEV_HEARTBEAT_INTERVAL_SECONDS = 60
_COORDINATION_DIR = "codexspec-automation"
_LOCK_BUSY_ERRNOS = frozenset({errno.EAGAIN, errno.EWOULDBLOCK, errno.EACCES})
# Disable every whitespace-error class so `diff --check` only reports leftover
# conflict markers; legitimate resolutions may contain trailing whitespace.
_MARKER_CHECK_WHITESPACE = "-trailing-space,-space-before-tab,-tab-in-indent,-indent-with-non-tab"
_URL_CREDENTIAL_PATTERN = re.compile(r"([a-zA-Z][a-zA-Z0-9+.-]*://)([^@/\s]+)@")
_FEATURE_ID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}[a-z0-9]{2}$")
_COMMIT_TYPES = frozenset(
    {"build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"}
)


class OwnershipError(AutomationError):
    """Auto-dev run ownership was unavailable or lost."""


@dataclass(frozen=True)
class RepositoryContext:
    repository_root: Path
    common_git_dir: Path
    default_branch: str
    remote_name: str | None
    remote_default_ref: str | None
    worktree_path: Path

    @property
    def coordination_dir(self) -> Path:
        return self.common_git_dir / _COORDINATION_DIR


@dataclass(frozen=True)
class WorkspaceContext:
    repository: RepositoryContext
    path: Path
    branch: str = FIXED_BRANCH

    @property
    def blueprint_path(self) -> Path:
        return self.path / BLUEPRINT_PATH


def _redact_url_credentials(value: str) -> str:
    """Mask userinfo embedded in remote URLs before the text reaches logs."""
    return _URL_CREDENTIAL_PATTERN.sub(r"\1***@", value)


def _sweep_stale_blueprint_temporaries(blueprint_path: Path) -> None:
    """Remove orphaned atomic-write temporaries; every writer holds the write lock."""
    for leftover in blueprint_path.parent.glob(f".{blueprint_path.name}.*"):
        if leftover.is_file():
            leftover.unlink(missing_ok=True)


def locate_repository(cwd: Path | str, *, runner: GitRunner | None = None) -> RepositoryContext:
    """Resolve primary repository and fixed-workspace facts from any checkout."""
    git = runner or GitRunner()
    current = Path(cwd).resolve()
    top = git.run(current, "rev-parse", "--show-toplevel", check=False)
    if top.returncode != 0:
        bare = git.run(current, "rev-parse", "--is-bare-repository", check=False)
        if bare.returncode != 0 or bare.stdout.strip() != "true":
            raise AutomationError("not_git_repository")
        invoking_root = Path(git.run(current, "rev-parse", "--absolute-git-dir").stdout.strip()).resolve()
    else:
        invoking_root = Path(top.stdout.strip()).resolve()
    worktrees = _parse_worktrees(git.run(invoking_root, "worktree", "list", "--porcelain").stdout)
    if not worktrees:
        raise AutomationError("worktree_registry_empty")
    primary_root = worktrees[0]["path"]
    common_output = git.run(invoking_root, "rev-parse", "--git-common-dir").stdout.strip()
    common_git_dir = Path(common_output)
    if not common_git_dir.is_absolute():
        common_git_dir = (invoking_root / common_git_dir).resolve()

    remote_name, remote_ref, remote_branch = _remote_default(git, invoking_root)
    default_branch = remote_branch or _local_default_branch(git, primary_root, worktrees[0].get("branch"))
    if remote_name and remote_ref is None:
        remote_ref = f"refs/remotes/{remote_name}/{default_branch}"
    worktree_path = Path(f"{primary_root}-codexspec-worktrees") / WORKTREE_BASENAME
    return RepositoryContext(
        repository_root=primary_root,
        common_git_dir=common_git_dir,
        default_branch=default_branch,
        remote_name=remote_name,
        remote_default_ref=remote_ref,
        worktree_path=worktree_path,
    )


def locate_dedicated_workspace(context: RepositoryContext, *, runner: GitRunner | None = None) -> WorkspaceContext:
    """Validate fixed branch/worktree without changing repository state."""
    git = runner or GitRunner()
    branch_ref = f"refs/heads/{FIXED_BRANCH}"
    if git.run(context.repository_root, "show-ref", "--verify", "--quiet", branch_ref, check=False).returncode != 0:
        raise AutomationError("missing_fixed_branch")
    registrations = _parse_worktrees(git.run(context.repository_root, "worktree", "list", "--porcelain").stdout)
    expected = context.worktree_path.resolve()
    match = next((entry for entry in registrations if entry["path"] == expected), None)
    if match is None:
        branch_match = next((entry for entry in registrations if entry.get("branch") == branch_ref), None)
        if branch_match is not None:
            raise AutomationError("worktree_path_mismatch", str(branch_match["path"]))
        raise AutomationError("missing_fixed_worktree")
    if match.get("branch") != branch_ref:
        raise AutomationError("worktree_branch_mismatch")
    return WorkspaceContext(context, expected)


def ensure_dedicated_workspace(context: RepositoryContext, *, runner: GitRunner | None = None) -> WorkspaceContext:
    """Create missing fixed branch/worktree and validate existing state."""
    git = runner or GitRunner()
    with _git_write_lock(context):
        return _ensure_dedicated_workspace_locked(context, git)


def _ensure_dedicated_workspace_locked(context: RepositoryContext, git: GitRunner) -> WorkspaceContext:
    branch_ref = f"refs/heads/{FIXED_BRANCH}"
    branch_exists = (
        git.run(context.repository_root, "show-ref", "--verify", "--quiet", branch_ref, check=False).returncode == 0
    )
    registrations = _parse_worktrees(git.run(context.repository_root, "worktree", "list", "--porcelain").stdout)
    expected = context.worktree_path.resolve()
    registered = next((entry for entry in registrations if entry["path"] == expected), None)
    if registered is not None and registered.get("branch") != branch_ref:
        raise AutomationError("worktree_branch_mismatch")
    branch_registration = next((entry for entry in registrations if entry.get("branch") == branch_ref), None)
    if branch_registration is not None and branch_registration["path"] != expected:
        raise AutomationError("worktree_path_mismatch", str(branch_registration["path"]))
    if expected.exists() and registered is None:
        raise AutomationError("worktree_path_occupied")

    merge_ref: str | None = None
    if not branch_exists:
        if context.remote_name:
            git.run(context.repository_root, "fetch", context.remote_name, check=False)
        start_ref, merge_ref = _select_initial_refs(context, git)
        git.run(context.repository_root, "branch", FIXED_BRANCH, start_ref)
    if registered is None:
        expected.parent.mkdir(parents=True, exist_ok=True)
        git.run(context.repository_root, "worktree", "add", str(expected), FIXED_BRANCH)
    initial_record = context.coordination_dir / "initial-merge.json"
    if merge_ref is not None:
        baselines = [git.run(expected, "rev-parse", ref).stdout.strip() for ref in ("HEAD", merge_ref)]
        _atomic_json(initial_record, {"baselines": baselines, "merge_hook": True})
    if initial_record.exists():
        initial = _initial_merge_state(initial_record)
        baselines = initial["baselines"]
        merging = git.run(expected, "rev-parse", "--verify", "MERGE_HEAD", check=False).returncode == 0
        head = git.run(expected, "rev-parse", "HEAD").stdout.strip()
        if not merging and head == baselines[0]:
            if git.run(expected, "status", "--porcelain").stdout:
                raise AutomationError("initial_merge_workspace_dirty")
            git.run(expected, "merge", "--no-edit", "--no-commit", baselines[1], check=False)
        conflicts = git.run(expected, "diff", "--name-only", "--diff-filter=U").stdout.splitlines()
        if conflicts:
            initial["merge_hook"] = False
            _atomic_json(initial_record, initial)
        state = "merge_requires_resolution" if conflicts else "merge_requires_verification"
        raise AutomationError(
            "initial_merge_requires_verification",
            json.dumps(
                {
                    "status": state,
                    "workspace": str(expected),
                    "conflict_paths": conflicts,
                    "finish_action": "codexspec _worktree-helper finish-initial --verification <json-file>",
                }
            ),
        )
    return locate_dedicated_workspace(context, runner=git)


def _initial_merge_state(record: Path) -> dict[str, Any]:
    value = json.loads(record.read_text(encoding="utf-8"))
    if (
        not isinstance(value, dict)
        or set(value) not in ({"baselines"}, {"baselines", "merge_hook"})
        or type(value.get("merge_hook", False)) is not bool
        or not isinstance(value["baselines"], list)
        or len(value["baselines"]) != 2
        or not all(isinstance(item, str) and re.fullmatch(r"[0-9a-f]{40,64}", item) for item in value["baselines"])
    ):
        raise AutomationError("invalid_initial_merge_record")
    return value


def finish_initial_workspace(context: RepositoryContext, verification: dict[str, Any]) -> dict[str, Any]:
    """Finish initial baseline preparation while excluding an active auto-dev run."""
    from .merge_commits import finish_verified_merge

    ownership = AutoDevOwnership(context)
    token = ownership.acquire()
    try:
        with _git_write_lock(context):
            with ownership.guard(token):
                workspace = locate_dedicated_workspace(context)
                record = context.coordination_dir / "initial-merge.json"
                initial = _initial_merge_state(record)
                finish_verified_merge(
                    workspace.path, verification, initial["baselines"], merge_hook=initial.get("merge_hook", False)
                )
                record.unlink()
                return {"status": "ready", "workspace": str(workspace.path)}
    finally:
        ownership.release(token)


def _select_initial_refs(context: RepositoryContext, git: GitRunner) -> tuple[str, str | None]:
    local_ref = f"refs/heads/{context.default_branch}"
    remote_ref = context.remote_default_ref
    local_exists = (
        git.run(context.repository_root, "show-ref", "--verify", "--quiet", local_ref, check=False).returncode == 0
    )
    remote_exists = (
        remote_ref
        and git.run(context.repository_root, "show-ref", "--verify", "--quiet", remote_ref, check=False).returncode == 0
    )
    if remote_ref and remote_exists and not local_exists:
        return remote_ref, None
    if not local_exists:
        raise AutomationError("default_branch_ref_not_found", local_ref)
    if remote_ref and remote_exists:
        local_is_ancestor = (
            git.run(
                context.repository_root, "merge-base", "--is-ancestor", local_ref, remote_ref, check=False
            ).returncode
            == 0
        )
        if local_is_ancestor:
            return remote_ref, None
        remote_is_ancestor = (
            git.run(
                context.repository_root, "merge-base", "--is-ancestor", remote_ref, local_ref, check=False
            ).returncode
            == 0
        )
        if not remote_is_ancestor:
            return local_ref, remote_ref
    return local_ref, None


def _remote_default(git: GitRunner, root: Path) -> tuple[str | None, str | None, str | None]:
    remotes = git.run(root, "remote", check=False).stdout.split()
    if not remotes:
        return None, None, None
    remote = "origin" if "origin" in remotes else remotes[0]
    symbolic = git.run(root, "symbolic-ref", "--quiet", f"refs/remotes/{remote}/HEAD", check=False)
    if symbolic.returncode != 0:
        return remote, None, None
    ref = symbolic.stdout.strip()
    return remote, ref, ref.removeprefix(f"refs/remotes/{remote}/")


def _local_default_branch(git: GitRunner, root: Path, primary_branch_ref: str | None) -> str:
    for candidate in ("main", "master"):
        if git.run(root, "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}", check=False).returncode == 0:
            return candidate
    configured = git.run(root, "config", "--get", "init.defaultBranch", check=False).stdout.strip()
    if (
        configured
        and git.run(root, "show-ref", "--verify", "--quiet", f"refs/heads/{configured}", check=False).returncode == 0
    ):
        return configured
    raise AutomationError(
        "default_branch_not_found", "Configure the remote default branch or a valid init.defaultBranch."
    )


def _parse_worktrees(output: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] = {}
    for line in output.splitlines() + [""]:
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        if key == "worktree":
            current["path"] = Path(value).resolve()
        elif key in {"HEAD", "branch"}:
            current[key.lower()] = value
        else:
            current[key] = value or True
    return entries


class FileLockBusyError(RuntimeError):
    """Raised by a non-blocking FileLock when another process holds the lock."""


class FileLock:
    """A short cross-process exclusive lock."""

    def __init__(self, path: Path, *, blocking: bool = True) -> None:
        self.path = path
        self.blocking = blocking
        self._file: Any = None

    def __enter__(self) -> FileLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self.path.open("a+b")
        if os.name == "nt":  # pragma: no cover - exercised on Windows CI
            import msvcrt

            if self._file.tell() == 0:
                self._file.write(b"\0")
                self._file.flush()
            self._file.seek(0)
            mode = msvcrt.LK_NBLCK if not self.blocking else msvcrt.LK_LOCK  # type: ignore[attr-defined]
            try:
                if self.blocking:
                    # LK_LOCK retries for only ~10 s before raising; keep waiting
                    # so Windows matches the indefinite blocking of POSIX flock.
                    while True:
                        try:
                            msvcrt.locking(self._file.fileno(), mode, 1)  # type: ignore[attr-defined]
                            break
                        except OSError:
                            time.sleep(0.1)
                else:
                    msvcrt.locking(self._file.fileno(), mode, 1)  # type: ignore[attr-defined]
            except OSError as exc:
                self._file.close()
                self._file = None
                raise FileLockBusyError(str(exc)) from exc
        else:
            import fcntl

            if self.blocking:
                fcntl.flock(self._file.fileno(), fcntl.LOCK_EX)
            else:
                try:
                    fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except OSError as exc:
                    self._file.close()
                    self._file = None
                    if exc.errno in _LOCK_BUSY_ERRNOS:
                        raise FileLockBusyError(str(exc)) from exc
                    raise
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> None:
        if self._file is None:
            return
        if os.name == "nt":  # pragma: no cover - exercised on Windows CI
            import msvcrt

            self._file.seek(0)
            msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)  # type: ignore[attr-defined]
        else:
            import fcntl

            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
        self._file.close()
        self._file = None


@contextmanager
def _git_write_lock(context: RepositoryContext) -> Iterator[None]:
    with FileLock(context.coordination_dir / "git-write.lock"):
        yield


class BlueprintStore:
    """Apply a blueprint operation as an atomic file and blueprint-only commit."""

    def __init__(self, workspace: WorkspaceContext, *, runner: GitRunner | None = None) -> None:
        self.workspace = workspace
        self.git = runner or GitRunner()
        self.recovery_path = workspace.repository.coordination_dir / "blueprint-transaction.json"

    def inspect(self) -> tuple[bytes, str]:
        content = self.workspace.blueprint_path.read_bytes() if self.workspace.blueprint_path.exists() else b""
        from .blueprint import blueprint_hash

        return content, blueprint_hash(content)

    def recover_pending_transaction(self, *, owner_token: str) -> None:
        """Recover an interrupted blueprint commit before auto-dev mutates Git."""
        context = self.workspace.repository
        with _git_write_lock(context):
            with FileLock(context.coordination_dir / "blueprint-modification.lock"):
                with AutoDevOwnership(context).guard(owner_token):
                    if any(
                        (context.coordination_dir / name).exists()
                        for name in ("merge-owner.json", "initial-merge.json")
                    ):
                        raise AutomationError("merge_in_progress")
                    self._recover()

    def prepare(
        self,
        request: bytes,
        *,
        feature_id_factory: Callable[[], str] | None = None,
        owner_token: str | None = None,
    ) -> dict[str, Any]:
        from .staged_commits import PreparedCommits

        context = self.workspace.repository
        with _git_write_lock(context):
            with FileLock(context.coordination_dir / "blueprint-modification.lock"):
                owner = AutoDevOwnership(context)
                guard = owner.guard(owner_token) if owner_token is not None else nullcontext()
                with guard:
                    if any(
                        (context.coordination_dir / name).exists()
                        for name in ("merge-owner.json", "initial-merge.json")
                    ):
                        raise AutomationError("merge_in_progress")
                    _sweep_stale_blueprint_temporaries(self.workspace.blueprint_path)
                    self._recover()
                    old_content, _ = self.inspect()
                    kwargs = {"feature_id_factory": feature_id_factory} if feature_id_factory is not None else {}
                    outcome = apply_operation(request, old_content, **kwargs)
                    if outcome.response["result"] != "applied":
                        return outcome.response
                    if outcome.response["operation"] == "update_status" and owner_token is None:
                        raise AutomationError("auto_dev_token_required")
                    if outcome.content == old_content:
                        return outcome.response
                    return PreparedCommits(self.workspace).prepare(
                        [BLUEPRINT_PATH.as_posix()],
                        kind="blueprint",
                        scope="blueprint",
                        token=owner_token,
                        content=outcome.content.decode("utf-8"),
                        payload={"request": request.decode("utf-8"), "feature_id": outcome.response["feature_id"]},
                    )

    def apply_and_commit(
        self,
        preparation_id: str,
        analyzed_tree: str,
        message: str,
        *,
        owner_token: str | None = None,
    ) -> dict[str, Any]:
        from .staged_commits import PreparedCommits, guarded_commit, validate_message

        validate_message(message, "blueprint")
        context = self.workspace.repository
        with _git_write_lock(context):
            with FileLock(context.coordination_dir / "blueprint-modification.lock"):
                guard = AutoDevOwnership(context).guard(owner_token) if owner_token is not None else nullcontext()
                with guard:
                    if any(
                        (context.coordination_dir / name).exists()
                        for name in ("merge-owner.json", "initial-merge.json")
                    ):
                        raise AutomationError("merge_in_progress")
                    self._recover()
                    preparations = PreparedCommits(self.workspace)
                    prepared = preparations.load(preparation_id, kind="blueprint", token=owner_token)
                    if prepared["tree"] != analyzed_tree:
                        raise AutomationError("stale_analysis")
                    payload = prepared["payload"]
                    if (
                        set(payload) != {"request", "feature_id"}
                        or not isinstance(payload["request"], str)
                        or not isinstance(payload["feature_id"], str)
                    ):
                        raise AutomationError("invalid_preparation")
                    old_content, _ = self.inspect()
                    outcome = apply_operation(
                        payload["request"].encode("utf-8"),
                        old_content,
                        feature_id_factory=lambda: payload["feature_id"],
                    )
                    if outcome.response["result"] != "applied":
                        raise AutomationError("stale_analysis", "blueprint operation must be prepared again")
                    if outcome.response["operation"] == "update_status" and owner_token is None:
                        raise AutomationError("auto_dev_token_required")
                    current = preparations.prepare(
                        [BLUEPRINT_PATH.as_posix()],
                        kind="blueprint",
                        scope="blueprint",
                        token=owner_token,
                        content=outcome.content.decode("utf-8"),
                    )
                    preparations.discard(current["preparation_id"], kind="blueprint", token=owner_token)
                    if current["tree"] != analyzed_tree:
                        raise AutomationError("stale_analysis")
                    pre_head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
                    record = {
                        "old_content": base64.b64encode(old_content).decode(),
                        "old_hash": outcome.response["previous_blueprint_hash"],
                        "new_hash": outcome.response["blueprint_hash"],
                        "pre_head": pre_head,
                        "operation": outcome.response["operation"],
                        "feature_id": outcome.response["feature_id"],
                    }
                    _atomic_json(self.recovery_path, record)
                    try:
                        _atomic_bytes(self.workspace.blueprint_path, outcome.content)
                        self.git.run(self.workspace.path, "add", "--", BLUEPRINT_PATH.as_posix())
                        guarded_commit(
                            self.workspace.path,
                            prepared["head"],
                            analyzed_tree,
                            message,
                            paths=[BLUEPRINT_PATH.as_posix()],
                        )
                    except Exception:
                        # A post-commit hook or the executor's final check can
                        # fail after Git has advanced HEAD. Preserve publication
                        # and its journal then; recovery must reconcile history.
                        if self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip() == pre_head:
                            self._restore_old(old_content)
                            self.recovery_path.unlink(missing_ok=True)
                        raise
                    self.recovery_path.unlink(missing_ok=True)
                    preparations.discard(preparation_id, kind="blueprint", token=owner_token)
                    return outcome.response

    def _recover(self) -> None:
        if not self.recovery_path.exists():
            return
        try:
            record = json.loads(self.recovery_path.read_text())
            expected_keys = {"old_content", "old_hash", "new_hash", "pre_head", "operation", "feature_id"}
            if not isinstance(record, dict) or set(record) != expected_keys:
                raise ValueError("unexpected transaction fields")
            old = base64.b64decode(record["old_content"], validate=True)
            current = self.workspace.blueprint_path.read_bytes() if self.workspace.blueprint_path.exists() else b""
            head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
            from .blueprint import blueprint_hash

            old_hash = blueprint_hash(old)
            current_hash = blueprint_hash(current)
            if record["old_hash"] != old_hash:
                raise AutomationError("unknown_blueprint_transaction", "old content hash mismatch")
            if head == record["pre_head"]:
                if current_hash == record["new_hash"]:
                    self._restore_old(old)
                elif current_hash != old_hash:
                    raise AutomationError("unknown_blueprint_transaction", "unexpected file content")
            else:
                parent = self.git.run(self.workspace.path, "rev-parse", "HEAD^", check=False).stdout.strip()
                changed_paths = self.git.run(
                    self.workspace.path, "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD", check=False
                ).stdout.splitlines()
                committed = (
                    current_hash == record["new_hash"]
                    and parent == record["pre_head"]
                    and changed_paths == [BLUEPRINT_PATH.as_posix()]
                )
                if not committed:
                    raise AutomationError("unknown_blueprint_transaction", "HEAD does not match blueprint commit")
            self.recovery_path.unlink()
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            raise AutomationError("invalid_blueprint_transaction", str(exc)) from exc

    def _restore_old(self, old: bytes) -> None:
        if old:
            _atomic_bytes(self.workspace.blueprint_path, old)
        else:
            self.workspace.blueprint_path.unlink(missing_ok=True)
        self.git.run(self.workspace.path, "reset", "--quiet", "HEAD", "--", BLUEPRINT_PATH.as_posix(), check=False)


class AutoDevOwnership:
    """Renewable repository-level ownership with stale reclaim and fencing."""

    def __init__(
        self,
        context: RepositoryContext,
        *,
        clock: Callable[[], float] = time.time,
        stale_after: float = AUTO_DEV_STALE_AFTER_SECONDS,
    ) -> None:
        self.context = context
        self.clock = clock
        self.stale_after = stale_after
        self.record_path = context.coordination_dir / "auto-dev-owner.json"
        self.lock_path = context.coordination_dir / "auto-dev-owner.lock"

    def acquire(self) -> str:
        # The busy answer must not wait behind a lock the active run holds
        # during a mutation (REQ-018: a second run exits immediately).
        try:
            return self._acquire_locked()
        except FileLockBusyError as exc:
            raise OwnershipError("already_running") from exc

    def _acquire_locked(self) -> str:
        with FileLock(self.lock_path, blocking=False):
            record = self._read()
            now = self.clock()
            if record is not None and now - record["activity"] <= self.stale_after:
                raise OwnershipError("already_running")
            token = secrets.token_urlsafe(32)
            _atomic_json(self.record_path, {"token": token, "activity": now})
            return token

    def renew(self, token: str) -> None:
        with FileLock(self.lock_path):
            self._assert_record(token)
            _atomic_json(self.record_path, {"token": token, "activity": self.clock()})

    def assert_owner(self, token: str) -> None:
        with FileLock(self.lock_path):
            self._assert_record(token)

    @contextmanager
    def guard(self, token: str) -> Iterator[None]:
        """Keep ownership from being reclaimed across one repository mutation."""
        with FileLock(self.lock_path):
            self._assert_record(token)
            _atomic_json(self.record_path, {"token": token, "activity": self.clock()})
            try:
                yield
            finally:
                _atomic_json(self.record_path, {"token": token, "activity": self.clock()})

    def release(self, token: str) -> None:
        with FileLock(self.lock_path):
            self._assert_record(token)
            self.record_path.unlink(missing_ok=True)

    def _read(self) -> dict[str, Any] | None:
        if not self.record_path.exists():
            return None
        try:
            value = json.loads(self.record_path.read_text())
            if (
                set(value) != {"token", "activity"}
                or not isinstance(value["token"], str)
                or not isinstance(value["activity"], (int, float))
            ):
                raise ValueError
            return value
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise OwnershipError("invalid_owner_record") from exc

    def _assert_record(self, token: str) -> None:
        record = self._read()
        if record is None or not secrets.compare_digest(record["token"], token):
            raise OwnershipError("lost_ownership")


class AutoDevGit:
    """Token-fenced Git synchronization and feature commits."""

    def __init__(
        self,
        workspace: WorkspaceContext,
        ownership: AutoDevOwnership,
        *,
        runner: GitRunner | None = None,
    ) -> None:
        self.workspace = workspace
        self.ownership = ownership
        self.git = runner or GitRunner()
        self.merge_record = workspace.repository.coordination_dir / "merge-owner.json"

    def recover_merge_ownership(self, token: str) -> dict[str, Any]:
        """Fence an interrupted merge to the current auto-dev owner."""
        self.ownership.assert_owner(token)
        with _git_write_lock(self.workspace.repository):
            with self.ownership.guard(token):
                if not self.merge_record.exists():
                    return {"state": "none"}
                record = self._read_merge_record()
                if record["token"] != token:
                    record["token"] = token
                    _atomic_json(self.merge_record, record)
                return self._recover_merge_state(record)

    def sync_default(self, token: str) -> dict[str, Any]:
        self.ownership.assert_owner(token)
        context = self.workspace.repository
        fetch_warning: str | None = None
        with _git_write_lock(context):
            with self.ownership.guard(token):
                if self.merge_record.exists():
                    record = self._assert_merge_owner(token)
                    state = self._recover_merge_state(record)
                    if state["state"] != "none":
                        state.update({"attempted_refs": [record["target"]], "fetch_warning": None})
                        return state
                if (context.coordination_dir / "blueprint-transaction.json").exists():
                    raise AutomationError("blueprint_recovery_required")
                _sweep_stale_blueprint_temporaries(self.workspace.blueprint_path)
                if self.git.run(self.workspace.path, "status", "--porcelain").stdout.strip():
                    raise AutomationError("workspace_not_clean")
                if context.remote_name:
                    fetched = self.git.run(self.workspace.path, "fetch", context.remote_name, check=False)
                    if fetched.returncode != 0:
                        fetch_warning = _redact_url_credentials(fetched.stderr.strip()) or "fetch failed"
                targets = [f"refs/heads/{context.default_branch}"]
                if context.remote_default_ref:
                    targets.append(context.remote_default_ref)
                attempted: list[str] = []
                for target in targets:
                    target_exists = (
                        self.git.run(
                            self.workspace.path, "show-ref", "--verify", "--quiet", target, check=False
                        ).returncode
                        == 0
                    )
                    if not target_exists:
                        continue
                    attempted.append(target)
                    already_merged = (
                        self.git.run(
                            self.workspace.path, "merge-base", "--is-ancestor", target, "HEAD", check=False
                        ).returncode
                        == 0
                    )
                    if already_merged:
                        continue
                    pre_head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
                    target_commit = self.git.run(self.workspace.path, "rev-parse", target + "^{commit}").stdout.strip()
                    record = {
                        "token": token,
                        "pre_head": pre_head,
                        "target": target_commit,
                        "phase": "merging",
                        "merge_hook": True,
                    }
                    _atomic_json(self.merge_record, record)
                    merged = self.git.run(
                        self.workspace.path, "merge", "--no-edit", "--no-commit", target_commit, check=False
                    )
                    if merged.returncode != 0:
                        conflicts = self._conflict_paths()
                        if conflicts or self._merge_in_progress():
                            record["merge_hook"] = False
                            _atomic_json(self.merge_record, record)
                            return {
                                "state": "needs_resolution",
                                "attempted_refs": attempted,
                                "fetch_warning": fetch_warning,
                                "conflict_paths": conflicts,
                            }
                        self._rollback_sync(record)
                        return {
                            "state": "failed",
                            "attempted_refs": attempted,
                            "fetch_warning": fetch_warning,
                            "error": merged.stderr.strip(),
                        }
                    record["phase"] = "resolved" if self._merge_in_progress() else "verification"
                    _atomic_json(self.merge_record, record)
                    return {
                        "state": "needs_verification",
                        "attempted_refs": attempted,
                        "fetch_warning": fetch_warning,
                        "target": target,
                    }
                return {"state": "clean", "attempted_refs": attempted, "fetch_warning": fetch_warning}

    def continue_sync(
        self, token: str, *, checks_passed: bool, analysis: dict[str, Any] | None = None, message: str | None = None
    ) -> dict[str, Any]:
        self.ownership.assert_owner(token)
        with _git_write_lock(self.workspace.repository):
            with self.ownership.guard(token):
                record = self._assert_merge_owner(token)
                if not checks_passed:
                    self._rollback_sync(record)
                    return {"state": "aborted", "pre_head": record["pre_head"]}
                unresolved = self._conflict_paths()
                if unresolved:
                    raise AutomationError("merge_conflicts_unresolved")
                if record["phase"] == "merging":
                    raise AutomationError("sync_verification_not_prepared")
                if record["phase"] == "resolved":
                    if not self._merge_in_progress():
                        raise AutomationError("merge_state_missing")
                    from .commit_runtime import commit_snapshot

                    if not isinstance(analysis, dict):
                        raise AutomationError("analysis_required")
                    target = self.git.run(
                        self.workspace.path, "rev-parse", record["target"] + "^{commit}"
                    ).stdout.strip()
                    if analysis.get("head") != record["pre_head"] or analysis.get("merge_heads") != [target]:
                        raise AutomationError("stale_analysis", "merge no longer matches the synchronization target")
                    if self.git.run(self.workspace.path, "diff", "--quiet", check=False).returncode:
                        raise AutomationError("unstaged_merge_changes")
                    commit_snapshot(
                        self.workspace.path,
                        analysis,
                        message,
                        use_caller_index=False,
                        merge_hook=record.get("merge_hook", False),
                    )
                self.merge_record.unlink()
                return {"state": "clean"}

    def prepare_sync_verification(self, token: str, resolved_paths: Sequence[str]) -> dict[str, Any]:
        """Stage an agent-resolved merge under the shared Git and ownership locks."""
        self.ownership.assert_owner(token)
        with _git_write_lock(self.workspace.repository):
            with self.ownership.guard(token):
                record = self._assert_merge_owner(token)
                if record["phase"] != "merging" or not self._merge_in_progress():
                    raise AutomationError("merge_resolution_not_available")
                conflicts = self._conflict_paths()
                normalized = [_validate_relative_path(path) for path in resolved_paths]
                if len(normalized) != len(set(normalized)) or set(normalized) != set(conflicts):
                    raise AutomationError("resolved_paths_mismatch")
                marker_check = self.git.run(
                    self.workspace.path,
                    "--literal-pathspecs",
                    "-c",
                    f"core.whitespace={_MARKER_CHECK_WHITESPACE}",
                    "diff",
                    "--check",
                    "--",
                    *normalized,
                    check=False,
                )
                if marker_check.returncode != 0:
                    detail = marker_check.stdout.strip() or marker_check.stderr.strip()
                    raise AutomationError("merge_resolution_check_failed", detail)
                self.git.run(self.workspace.path, "--literal-pathspecs", "add", "--", *normalized)
                unresolved = self._conflict_paths()
                if unresolved:
                    raise AutomationError("merge_conflicts_unresolved", ", ".join(unresolved))
                record["phase"] = "resolved"
                record["merge_hook"] = False
                _atomic_json(self.merge_record, record)
                return {"state": "needs_verification", "target": record["target"]}

    def abort_sync(self, token: str) -> dict[str, Any]:
        return self.continue_sync(token, checks_passed=False)

    def _assert_commit_ready(self) -> None:
        if self.merge_record.exists():
            raise AutomationError("merge_in_progress")
        if (self.workspace.repository.coordination_dir / "blueprint-transaction.json").exists():
            raise AutomationError("blueprint_recovery_required")

    def prepare_feature(self, token: str, feature_id: str, paths: Sequence[str]) -> dict[str, Any]:
        from .staged_commits import PreparedCommits

        self.ownership.assert_owner(token)
        if not _FEATURE_ID_RE.fullmatch(feature_id):
            raise AutomationError("invalid_feature_id")
        normalized = [_validate_commit_path(path) for path in paths]
        if not normalized:
            raise AutomationError("empty_commit_paths")
        with _git_write_lock(self.workspace.repository):
            with self.ownership.guard(token):
                self._assert_commit_ready()
                return PreparedCommits(self.workspace).prepare(
                    normalized,
                    kind="feature",
                    scope=feature_id,
                    token=token,
                )

    def commit_feature(
        self,
        token: str,
        preparation_id: str,
        analyzed_tree: str,
        message: str,
    ) -> dict[str, Any]:
        from .staged_commits import PreparedCommits, guarded_commit, validate_message

        self.ownership.assert_owner(token)
        with _git_write_lock(self.workspace.repository):
            with self.ownership.guard(token):
                self._assert_commit_ready()
                store = PreparedCommits(self.workspace)
                record = store.load(preparation_id, kind="feature", token=token)
                if not _FEATURE_ID_RE.fullmatch(record["scope"]):
                    raise AutomationError("invalid_feature_id")
                validate_message(message, record["scope"])
                if record["tree"] != analyzed_tree:
                    raise AutomationError("stale_analysis")
                current = store.prepare(record["paths"], kind="feature", scope=record["scope"], token=token)
                store.discard(current["preparation_id"], kind="feature", token=token)
                if current["tree"] != analyzed_tree:
                    raise AutomationError("stale_analysis", "prepare and analyze current changes again")
                self.git.run(self.workspace.path, "--literal-pathspecs", "add", "--", *record["paths"])
                commit = guarded_commit(
                    self.workspace.path,
                    record["head"],
                    analyzed_tree,
                    message,
                    paths=record["paths"],
                )
                store.discard(preparation_id, kind="feature", token=token)
                return {"state": "committed", "commit": commit, "paths": record["paths"]}

    def _assert_merge_owner(self, token: str) -> dict[str, Any]:
        record = self._read_merge_record()
        if record["token"] != token:
            raise OwnershipError("lost_merge_ownership")
        return record

    def _read_merge_record(self) -> dict[str, Any]:
        if not self.merge_record.exists():
            raise AutomationError("no_merge_in_progress")
        try:
            record = json.loads(self.merge_record.read_text())
        except json.JSONDecodeError as exc:
            raise AutomationError("invalid_merge_record") from exc
        if (
            not isinstance(record, dict)
            or set(record)
            not in ({"token", "pre_head", "target", "phase"}, {"token", "pre_head", "target", "phase", "merge_hook"})
            or not all(isinstance(record[key], str) and record[key] for key in ("token", "pre_head", "target", "phase"))
            or type(record.get("merge_hook", False)) is not bool
            or record["phase"] not in {"merging", "resolved", "verification"}
        ):
            raise AutomationError("invalid_merge_record")
        return record

    def _recover_merge_state(self, record: dict[str, Any]) -> dict[str, Any]:
        if record["phase"] == "verification":
            return {"state": "needs_verification", "target": record["target"]}
        if record["phase"] == "resolved" and self._merge_in_progress():
            return {"state": "needs_verification", "target": record["target"]}
        if self._merge_in_progress():
            conflicts = self._conflict_paths()
            if not conflicts:
                record["phase"] = "resolved"
                _atomic_json(self.merge_record, record)
                return {"state": "needs_verification", "target": record["target"]}
            record["merge_hook"] = False
            _atomic_json(self.merge_record, record)
            return {
                "state": "needs_resolution",
                "target": record["target"],
                "conflict_paths": conflicts,
            }
        head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
        if head == record["pre_head"] and not self._tracked_changes_present():
            self.merge_record.unlink()
            return {"state": "none"}
        if head != record["pre_head"]:
            record["phase"] = "verification"
            _atomic_json(self.merge_record, record)
            return {"state": "needs_verification", "target": record["target"]}
        # HEAD is back at the pre-merge commit but resolution edits remain: restore
        # the recorded baseline instead of dead-ending in an underivable state.
        self._rollback_sync(record)
        return {"state": "none"}

    def _tracked_changes_present(self) -> bool:
        return bool(
            self.git.run(
                self.workspace.path, "status", "--porcelain", "--untracked-files=no", check=False
            ).stdout.strip()
        )

    def _rollback_sync(self, record: dict[str, str]) -> None:
        if self._merge_in_progress():
            self.git.run(self.workspace.path, "merge", "--abort")
        self.git.run(self.workspace.path, "reset", "--hard", record["pre_head"])
        head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
        if head != record["pre_head"] or self._tracked_changes_present():
            raise AutomationError("merge_abort_incomplete")
        self.merge_record.unlink()

    def _merge_in_progress(self) -> bool:
        return (
            self.git.run(self.workspace.path, "rev-parse", "--verify", "--quiet", "MERGE_HEAD", check=False).returncode
            == 0
        )

    def _conflict_paths(self) -> list[str]:
        output = self.git.run(
            self.workspace.path,
            "-c",
            "core.quotePath=false",
            "diff",
            "--name-only",
            "--diff-filter=U",
            "-z",
            check=False,
        ).stdout
        return [path for path in output.split("\0") if path]


def _validate_commit_path(value: str) -> str:
    normalized = _validate_relative_path(value)
    path = Path(normalized)
    try:
        BLUEPRINT_PATH.relative_to(path)
    except ValueError:
        pass
    else:
        raise AutomationError("blueprint_path_forbidden")
    return normalized


def _validate_relative_path(value: str) -> str:
    path = Path(value)
    if not value or value.startswith(":") or path.is_absolute() or ".." in path.parts or path == Path("."):
        raise AutomationError("invalid_commit_path", value)
    normalized = Path(path.as_posix())
    return normalized.as_posix()


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        mode = stat.S_IMODE(path.stat().st_mode)
    except OSError:
        mode = 0o644
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as output:
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _atomic_json(path: Path, value: Any) -> None:
    _atomic_bytes(path, (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode())
