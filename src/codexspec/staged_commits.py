"""Explicit staging snapshots for agent-generated commit messages.

This module never generates a message. Callers use commit-staged against the
returned index, then submit that message with the exact analyzed tree.
"""

from __future__ import annotations

import json
import re
import secrets
import shutil
from pathlib import Path
from typing import Any, Sequence

from .automation import (
    BLUEPRINT_PATH,
    AutomationError,
    GitRunner,
    WorkspaceContext,
    _atomic_json,
    _validate_commit_path,
)
from .commit_runtime import (
    commit_snapshot as commit_snapshot,
)
from .commit_runtime import (
    guarded_commit as guarded_commit,
)
from .commit_runtime import (
    snapshot as snapshot,
)
from .commit_runtime import (
    validate_message as validate_message,
)

_RECORD_KEYS = {"version", "preparation_id", "workspace", "kind", "scope", "token", "head", "tree", "paths", "payload"}
_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


def _safe_file(path: Path, root: Path) -> None:
    if not path.resolve().is_relative_to(root.resolve()):
        raise AutomationError("invalid_preparation", "path escapes its owner")
    for part in (path, *path.parents):
        if part.is_symlink():
            raise AutomationError("invalid_preparation", "linked path")
        if part == root:
            break
    if path.exists() and (not path.is_file() or path.stat().st_nlink != 1):
        raise AutomationError("invalid_preparation", "non-regular or shared file")


class PreparedCommits:
    """Keep helper-created indexes separate from caller-owned staging."""

    def __init__(self, workspace: WorkspaceContext, *, runner: GitRunner | None = None) -> None:
        self.workspace = workspace
        self.git = runner or GitRunner()
        self.root = workspace.repository.coordination_dir / "commit-preparations"

    def prepare(
        self,
        paths: Sequence[str],
        *,
        kind: str,
        scope: str,
        token: str | None = None,
        content: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if kind not in {"feature", "blueprint"} or not scope or not paths:
            raise AutomationError("invalid_preparation")
        selected = list(paths)
        if kind == "blueprint":
            if selected != [BLUEPRINT_PATH.as_posix()] or content is None or scope != "blueprint":
                raise AutomationError("invalid_preparation")
        else:
            selected = [_validate_commit_path(path) for path in selected]
        head = self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip()
        identifier = secrets.token_hex(16)
        directory = self.root / identifier
        _safe_file(directory / "index", self.workspace.repository.common_git_dir)
        directory.mkdir(parents=True, mode=0o700)
        index = directory / "index"
        try:
            self.git.run(self.workspace.path, "read-tree", head, index_file=index)
            if kind == "blueprint":
                blob = self.git.run(
                    self.workspace.path,
                    "hash-object",
                    "-w",
                    f"--path={BLUEPRINT_PATH.as_posix()}",
                    "--stdin",
                    input_text=content,
                ).stdout.strip()
                mode = "100644"
                blueprint = self.workspace.blueprint_path
                if blueprint.exists():
                    tracks_mode = (
                        self.git.run(
                            self.workspace.path,
                            "config",
                            "--bool",
                            "--get",
                            "core.filemode",
                            check=False,
                        ).stdout.strip()
                        != "false"
                    )
                    if tracks_mode:
                        mode = "100755" if blueprint.stat().st_mode & 0o100 else "100644"
                    else:
                        entry = self.git.run(
                            self.workspace.path,
                            "ls-files",
                            "--stage",
                            "--",
                            BLUEPRINT_PATH.as_posix(),
                            index_file=index,
                        ).stdout.split()
                        if entry:
                            mode = entry[0]
                self.git.run(
                    self.workspace.path,
                    "update-index",
                    "--add",
                    "--cacheinfo",
                    mode,
                    blob,
                    BLUEPRINT_PATH.as_posix(),
                    index_file=index,
                )
            else:
                self.git.run(self.workspace.path, "--literal-pathspecs", "add", "--", *selected, index_file=index)
            tree = self.git.run(self.workspace.path, "write-tree", index_file=index).stdout.strip()
            if tree == self.git.run(self.workspace.path, "rev-parse", f"{head}^{{tree}}").stdout.strip():
                raise AutomationError("empty_staged_changes")
            record = {
                "version": 1,
                "preparation_id": identifier,
                "workspace": str(self.workspace.path.resolve()),
                "kind": kind,
                "scope": scope,
                "token": token,
                "head": head,
                "tree": tree,
                "paths": selected,
                "payload": payload or {},
            }
            _atomic_json(directory / "record.json", record)
            (directory / "record.json").chmod(0o600)
            return self.response(record)
        except Exception:
            shutil.rmtree(directory)
            raise

    def response(self, record: dict[str, Any]) -> dict[str, Any]:
        return {
            "state": "prepared",
            "preparation_id": record["preparation_id"],
            "workspace": record["workspace"],
            "index_file": str(self.root / record["preparation_id"] / "index"),
            "head": record["head"],
            "tree": record["tree"],
            "required_scope": record["scope"],
        }

    def load(
        self,
        identifier: str,
        *,
        kind: str,
        token: str | None = None,
        validate_current: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(identifier, str) or not re.fullmatch(r"[0-9a-f]{32}", identifier):
            raise AutomationError("invalid_preparation")
        directory = self.root / identifier
        index = directory / "index"
        record_file = directory / "record.json"
        for path in (index, record_file):
            _safe_file(path, self.workspace.repository.common_git_dir)
        try:
            record = json.loads(record_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise AutomationError("invalid_preparation", str(exc)) from exc
        if (
            not isinstance(record, dict)
            or set(record) != _RECORD_KEYS
            or type(record["version"]) is not int
            or record["version"] != 1
            or record["preparation_id"] != identifier
            or record["kind"] != kind
            or record["workspace"] != str(self.workspace.path.resolve())
            or not isinstance(record["scope"], str)
            or not record["scope"]
            or not isinstance(record["payload"], dict)
            or not isinstance(record["paths"], list)
            or not record["paths"]
            or not all(isinstance(p, str) for p in record["paths"])
            or not all(isinstance(record[k], str) and _OBJECT_ID.fullmatch(record[k]) for k in ("head", "tree"))
            or not index.is_file()
        ):
            raise AutomationError("invalid_preparation")
        if record["token"] != token:
            raise AutomationError("preparation_owner")
        if kind == "feature":
            for selected_path in record["paths"]:
                _validate_commit_path(selected_path)
        elif record["paths"] != [BLUEPRINT_PATH.as_posix()] or record["scope"] != "blueprint":
            raise AutomationError("invalid_preparation")
        if validate_current and (
            self.git.run(self.workspace.path, "rev-parse", "HEAD").stdout.strip() != record["head"]
            or self.git.run(self.workspace.path, "write-tree", index_file=index).stdout.strip() != record["tree"]
        ):
            raise AutomationError("stale_analysis", "prepare and analyze the staged changes again")
        return record

    def discard(self, identifier: str, *, kind: str, token: str | None = None) -> None:
        self.load(identifier, kind=kind, token=token, validate_current=False)
        directory = self.root / identifier
        # Only these known files belong to this protocol; never recursively delete
        # an externally modified preparation directory.
        for name in ("index", "record.json"):
            (directory / name).unlink()
        directory.rmdir()
