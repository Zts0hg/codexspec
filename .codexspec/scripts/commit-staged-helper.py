"""Shared, standalone staged-commit guard; requires only Python 3.11+ and Git.

The agent supplies the message. This module never selects or stages files.
CLI imports and installed byte-identical copies execute this same implementation.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Sequence

GIT_TIMEOUT_SECONDS = 600
GIT_COMMIT_TIMEOUT_SECONDS = 3600
_FALLBACK_LOCAL_ENV_VARS = {
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_COMMON_DIR",
    "GIT_CONFIG",
    "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS",
    "GIT_DIR",
    "GIT_GRAFT_FILE",
    "GIT_IMPLICIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_INTERNAL_SUPER_PREFIX",
    "GIT_NO_REPLACE_OBJECTS",
    "GIT_OBJECT_DIRECTORY",
    "GIT_PREFIX",
    "GIT_REPLACE_REF_BASE",
    "GIT_SHALLOW_FILE",
    "GIT_WORK_TREE",
}


class AutomationError(RuntimeError):
    """An automation operation could not safely continue."""

    def __init__(self, code: str, message: str | None = None) -> None:
        super().__init__(f"{code}: {message}" if message else code)
        self.code = code


class GitRunner:
    """Run Git against an explicit repository with caller-local state removed."""

    def __init__(self, *, preserve_configuration: bool = False) -> None:
        self.local_environment_variables = self._discover_local_environment_variables()
        if preserve_configuration:
            # Direct commits operate in the invoking repository. Its command-
            # scope configuration includes hook and signing policies. Foreign
            # repository callers retain the default fully sanitized environment.
            self.local_environment_variables -= {"GIT_CONFIG", "GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"}

    @staticmethod
    def _discover_local_environment_variables() -> frozenset[str]:
        env = os.environ.copy()
        for name in _FALLBACK_LOCAL_ENV_VARS:
            env.pop(name, None)
        result = _run_git_with_timeout(
            ["git", "rev-parse", "--local-env-vars"],
            env=env,
        )
        reported = set(result.stdout.split()) if result.returncode == 0 else set()
        return frozenset(_FALLBACK_LOCAL_ENV_VARS | reported)

    def environment(self) -> dict[str, str]:
        env = os.environ.copy()
        for name in self.local_environment_variables:
            env.pop(name, None)
        return env

    def run(
        self,
        repository: Path,
        *args: str,
        check: bool = True,
        input_text: str | None = None,
        index_file: Path | None = None,
        reflog_action: str | None = None,
        timeout_seconds: int = GIT_TIMEOUT_SECONDS,
    ) -> subprocess.CompletedProcess[str]:
        environment = self.environment()
        if reflog_action is not None:
            environment.setdefault("GIT_REFLOG_ACTION", reflog_action)
        if index_file is not None:
            environment["GIT_INDEX_FILE"] = str(index_file.resolve())
        result = _run_git_with_timeout(
            ["git", "-C", str(repository), *args],
            input=input_text,
            env=environment,
            timeout_seconds=timeout_seconds,
        )
        if check and result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise AutomationError("git_command_failed", f"git {' '.join(args)}: {detail}")
        return result


def _run_git_with_timeout(
    command: list[str],
    *,
    input: str | None = None,
    env: Mapping[str, str] | None = None,
    timeout_seconds: int = GIT_TIMEOUT_SECONDS,
) -> subprocess.CompletedProcess[str]:
    try:
        # Text-mode stdin rewrites LF to CRLF on Windows, changing prepared
        # blobs and commit messages. Encode explicitly to preserve input bytes.
        result = subprocess.run(
            command,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
            input=input.encode("utf-8") if input is not None else None,
            env=env,
        )
        stdout, stderr = (
            value.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n") for value in (result.stdout, result.stderr)
        )
        return subprocess.CompletedProcess(result.args, result.returncode, stdout, stderr)
    except subprocess.TimeoutExpired as exc:
        raise AutomationError("git_command_timeout", f"git {' '.join(command[1:])}") from exc


def validate_message(message: str, scope: str | None = None) -> None:
    if not isinstance(message, str) or not message.strip() or "\0" in message:
        raise AutomationError("invalid_commit_message")
    if scope is None:
        # Direct callers may follow a project-specific convention. Helpers own
        # their fixed feature/blueprint scope and validate it below.
        return
    subject = message.splitlines()[0]
    matched = re.fullmatch(
        r"(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(?:\(([^\n()]+)\))?!?: .+", subject
    )
    if matched is None or (scope is not None and matched.group(2) != scope):
        raise AutomationError("invalid_commit_message", "use the required Conventional Commits scope")


def _head(repository: Path, git: GitRunner) -> str | None:
    result = git.run(repository, "rev-parse", "--verify", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def _merge_heads(repository: Path, git: GitRunner) -> list[str]:
    path = Path(git.run(repository, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD").stdout.strip())
    return path.read_text(encoding="ascii").splitlines() if path.exists() else []


def snapshot(repository: Path, *, use_caller_index: bool = True) -> dict[str, Any]:
    """Capture caller index/configuration, or clean state for a managed workspace."""
    git = GitRunner(preserve_configuration=use_caller_index)
    repository = repository.resolve()
    caller_index = os.environ.get("GIT_INDEX_FILE") if use_caller_index else None
    index = (
        Path(caller_index).resolve()
        if caller_index
        else Path(git.run(repository, "rev-parse", "--path-format=absolute", "--git-path", "index").stdout.strip())
    )
    merge_heads = _merge_heads(repository, git)
    empty = git.run(repository, "diff", "--cached", "--quiet", check=False, index_file=index).returncode == 0
    if empty and not merge_heads:
        raise AutomationError("empty_staged_changes")
    result: dict[str, Any] = {
        "workspace": str(repository),
        "index_file": str(index),
        "head": _head(repository, git),
        "tree": git.run(repository, "write-tree", index_file=index).stdout.strip(),
    }
    if merge_heads:
        result["merge_heads"] = merge_heads
        if empty:
            message_path = Path(
                git.run(repository, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_MSG").stdout.strip()
            )
            result["default_message"] = message_path.read_text(encoding="utf-8")
    return result


def commit_snapshot(
    repository: Path,
    analyzed: dict[str, Any],
    message: str | None,
    *,
    use_caller_index: bool = True,
    merge_hook: bool = False,
) -> dict[str, Any]:
    if not isinstance(analyzed, dict) or not {"workspace", "index_file", "head", "tree"} <= set(analyzed):
        raise AutomationError("analysis_required")
    if message is not None:
        validate_message(message)
    current = snapshot(repository, use_caller_index=use_caller_index)
    if current != analyzed:
        raise AutomationError("stale_analysis", "analyze the current staging area again")
    if "default_message" in current:
        if message is not None:
            raise AutomationError("default_merge_message_required")
    else:
        validate_message(message)
    commit = guarded_commit(
        repository,
        analyzed["head"],
        analyzed["tree"],
        message,
        index_file=Path(analyzed["index_file"]),
        merge_heads=analyzed.get("merge_heads", []),
        merge_hook=merge_hook,
        preserve_configuration=use_caller_index,
    )
    return {"state": "committed", "commit": commit}


def _merge_commit_options(repository: Path, git: GitRunner) -> list[str]:
    """Carry native merge signing/trailer options into the deferred commit.

    Git parses mergeOptions with its alias tokenizer, not POSIX shell syntax.
    A non-shell rev-parse alias lets Git tokenize it without executing its data.
    Options that operate during merge preparation remain with git merge.
    """
    branch = git.run(repository, "symbolic-ref", "--quiet", "HEAD", check=False)
    if branch.returncode:
        return []
    name = branch.stdout.strip().removeprefix("refs/heads/")
    configured = git.run(repository, "config", "--get", f"branch.{name}.mergeOptions", check=False)
    if configured.returncode:
        return []
    quoted = git.run(
        repository,
        "-c",
        "alias.codexspec-merge-options=rev-parse --sq-quote " + configured.stdout.rstrip("\n"),
        "codexspec-merge-options",
    ).stdout
    arguments = iter(shlex.split(quoted))
    result = []
    carried = ("--gpg-sign", "--no-gpg-sign", "--signoff", "--no-signoff")
    takes_value = ("--message", "--file", "--strategy", "--strategy-option", "--into-name", "--cleanup")
    for argument in arguments:
        if argument == "--":
            break
        if argument.startswith("--"):
            option, separator, value = argument.partition("=")
            matches = [name for name in carried if name.startswith(option)]
            if len(matches) == 1:
                result.append(matches[0] + (separator + value if separator else ""))
            elif not separator and any(name.startswith(option) for name in takes_value):
                next(arguments, None)
        elif argument.startswith("-"):
            # Git accepts short bundles. Required arguments consume the rest
            # of the bundle or next argument; -S takes only an attached optional key.
            for offset, letter in enumerate(argument[1:], 2):
                if letter == "S":
                    result.append("-S" + argument[offset:])
                    break
                if letter in "mFsX":
                    if offset == len(argument):
                        next(arguments, None)
                    break
    return result


def guarded_commit(
    repository: Path,
    expected_head: str | None,
    expected_tree: str,
    message: str | None,
    *,
    merge_heads: Sequence[str] = (),
    merge_hook: bool = False,
    paths: Sequence[str] | None = None,
    index_file: Path | None = None,
    preserve_configuration: bool = False,
) -> str:
    """Delegate hooks and reject changes to the analyzed tree before committing."""
    git = GitRunner(preserve_configuration=preserve_configuration)
    if message is None:
        if not merge_heads or git.run(repository, "rev-parse", "HEAD^{tree}").stdout.strip() != expected_tree:
            raise AutomationError("invalid_default_merge_message")
    else:
        validate_message(message)
    if _head(repository, git) != expected_head or _merge_heads(repository, git) != list(merge_heads):
        raise AutomationError("stale_analysis")
    original_hooks = Path(
        git.run(repository, "rev-parse", "--path-format=absolute", "--git-path", "hooks").stdout.strip()
    )
    with tempfile.TemporaryDirectory(prefix="codexspec-commit-hooks-") as temporary:
        directory = Path(temporary)
        manifest = directory / "guard.json"
        manifest.write_text(
            json.dumps(
                {
                    "hooks": str(original_hooks),
                    "head": expected_head,
                    "tree": expected_tree,
                    "merge_heads": list(merge_heads),
                    "merge_hook": merge_hook,
                    "invocation_environment": {
                        key: git.environment().get(key)
                        for key in (
                            "GIT_LITERAL_PATHSPECS",
                            "GIT_EDITOR",
                            "GIT_INDEX_FILE",
                            "GIT_AUTHOR_NAME",
                            "GIT_AUTHOR_EMAIL",
                            "GIT_AUTHOR_DATE",
                        )
                    },
                    "merge_message": (
                        git.run(
                            repository, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_MSG"
                        ).stdout.strip()
                        if merge_hook
                        else None
                    ),
                }
            ),
            encoding="utf-8",
        )
        hook_names = {"pre-commit", "prepare-commit-msg", "commit-msg", "post-commit"}
        if original_hooks.is_dir():
            hook_names.update(p.name for p in original_hooks.iterdir() if p.is_file())
        for name in hook_names:
            if name == manifest.name:
                continue
            command = shlex.join(
                [sys.executable, "-I", "-S", str(Path(__file__).resolve()), "hook", str(manifest), name]
            )
            script = directory / name
            script.write_text("#!/bin/sh\nexec " + command + ' "$@"\n', encoding="utf-8", newline="\n")
            script.chmod(0o755)
        args = ["-c", f"core.hooksPath={directory}", "commit", "--cleanup=verbatim"]
        args.extend(["--no-edit"] if message is None else ["-F", "-"])
        if merge_hook:
            args.extend(_merge_commit_options(repository, git))
        if paths is not None:
            args.extend(["--only", "--", *paths])
        git.run(
            repository,
            "--literal-pathspecs",
            *args,
            input_text=message,
            index_file=index_file,
            reflog_action="merge " + " ".join(merge_heads) if merge_hook else None,
            timeout_seconds=GIT_COMMIT_TIMEOUT_SECONDS,
        )
    commit = git.run(repository, "rev-parse", "HEAD").stdout.strip()
    if git.run(repository, "rev-parse", "HEAD^{tree}").stdout.strip() != expected_tree:
        raise AutomationError("committed_tree_mismatch", f"commit {commit}; do not rewrite history automatically")
    if merge_heads:
        parents = git.run(repository, "show", "-s", "--format=%P", "HEAD").stdout.split()
        if parents != [expected_head, *merge_heads]:
            raise AutomationError(
                "committed_parents_mismatch", f"commit {commit}; do not rewrite history automatically"
            )
    return commit


def _hook_main(manifest_path: str, name: str, arguments: list[str]) -> int:
    """Run inside Git's own hook environment, including its actual commit index."""
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    # Automatic merges use pre-merge-commit; resolved conflicts and direct
    # git-commit callers use pre-commit. A pre-merge hook may itself delegate to
    # pre-commit, so do not invoke both independently.
    original_name = name
    original_arguments = list(arguments)
    message_file = None
    merge_message = None
    if manifest["merge_hook"]:
        if name == "pre-commit":
            original_name = "pre-merge-commit"
        elif name == "post-commit":
            original_name = "post-merge"
            original_arguments = ["0"]
        elif name in {"prepare-commit-msg", "commit-msg"}:
            message_file = Path(arguments[0])
            merge_message = Path(manifest["merge_message"])
            original_arguments = [str(merge_message)]
            if name == "prepare-commit-msg":
                original_arguments.append("merge")
    hook_environment = os.environ.copy()
    # Literal path handling belongs to our commit command, not original hooks:
    # leaking this option can turn wildcard validation into an empty selection.
    restore = ["GIT_LITERAL_PATHSPECS"]
    if manifest["merge_hook"]:
        # Git commit synthesizes an author environment; native merge does not.
        # Preserve explicit caller values, including their original date form.
        restore.extend(["GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_AUTHOR_DATE"])
        if name not in {"pre-commit", "prepare-commit-msg", "commit-msg"}:
            # Native merge overrides editor/index only for pre-creation hooks.
            restore.extend(["GIT_EDITOR", "GIT_INDEX_FILE"])
    for key in restore:
        value = manifest["invocation_environment"][key]
        if value is None:
            hook_environment.pop(key, None)
        else:
            hook_environment[key] = value
    hook = Path(manifest["hooks"]) / original_name
    if hook.is_file() and os.access(hook, os.X_OK):
        if merge_message is not None and message_file is not None:
            # Native automatic merge hooks receive MERGE_MSG. Git commit uses
            # COMMIT_EDITMSG internally, so propagate edits in both directions.
            merge_message.write_bytes(message_file.read_bytes())
        # Git's shell launcher handles hook scripts on every supported platform.
        # Unlike `git hook run`, a shell alias preserves stdin (including the
        # reference-transaction records). The shell program is constant; hook
        # paths and arguments remain quoted positional arguments. A nested Git
        # invocation recalculates GIT_PREFIX from the hook root, so restore the
        # original value (or absence) before executing the original hook.
        result = subprocess.run(
            [
                "git",
                "-c",
                f"core.hooksPath={manifest['hooks']}",
                "-c",
                'alias.codexspec-run-hook=!f() { if [ "$1" = set ]; then '
                'GIT_PREFIX="$2"; export GIT_PREFIX; else unset GIT_PREFIX; fi; '
                'shift 2; exec "$@"; }; f',
                "codexspec-run-hook",
                "set" if "GIT_PREFIX" in os.environ else "unset",
                os.environ.get("GIT_PREFIX", ""),
                str(hook),
                *original_arguments,
            ],
            env=hook_environment,
            check=False,
        )
        if merge_message is not None and message_file is not None:
            message_file.write_bytes(merge_message.read_bytes())
        if result.returncode:
            return result.returncode
    if name in {"pre-commit", "prepare-commit-msg", "commit-msg"}:
        tree = subprocess.run(["git", "write-tree"], capture_output=True, text=True, check=False)
        head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], capture_output=True, text=True, check=False)
        actual_head = head.stdout.strip() if head.returncode == 0 else None
        merge_path = subprocess.run(
            ["git", "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        path = Path(merge_path.stdout.strip())
        parents = path.read_text(encoding="ascii").splitlines() if path.is_file() else []
        if (
            tree.returncode
            or tree.stdout.strip() != manifest["tree"]
            or actual_head != manifest["head"]
            or merge_path.returncode
            or parents != manifest["merge_heads"]
        ):
            print("stale_analysis: commit content changed; prepare and analyze again", file=sys.stderr)
            return 1
    return 0


def dispatch(action: str, body: Any = None) -> dict[str, Any]:
    """Serve the same strict machine protocol through CLI and standalone entry."""
    if action == "snapshot":
        return snapshot(Path.cwd())
    if action == "commit":
        if not isinstance(body, dict) or set(body) != {"analysis", "message"} or not isinstance(body["analysis"], dict):
            raise AutomationError("analysis_required")
        return commit_snapshot(Path.cwd(), body["analysis"], body["message"])
    raise AutomationError("unsupported_commit_staged_action", action)


def install_helper(directory: Path) -> Path:
    """Install this complete stdlib-only module byte-for-byte."""
    destination = directory.absolute() / "commit-staged-helper.py"
    for part in (destination, *destination.parents):
        if part.is_symlink():
            raise AutomationError("linked_commit_helper", str(part))
    if destination.exists() and (not destination.is_file() or destination.stat().st_nlink != 1):
        raise AutomationError("shared_commit_helper", str(destination))
    directory.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(Path(__file__).read_bytes())
    return destination


def main(arguments: list[str]) -> int:
    """Run without importing CodexSpec or site packages, including inside hooks."""
    try:
        if arguments and arguments[0] == "hook" and len(arguments) >= 3:
            return _hook_main(arguments[1], arguments[2], arguments[3:])
        if len(arguments) != 1:
            raise AutomationError("invalid_arguments", "expected snapshot or commit")
        body = json.loads(sys.stdin.buffer.read().decode("utf-8")) if arguments[0] == "commit" else None
        print(json.dumps(dispatch(arguments[0], body)))
        return 0
    except (AutomationError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
