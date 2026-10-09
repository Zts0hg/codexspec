"""Checkout-local configuration and deterministic isolated feature workspaces."""

from __future__ import annotations

import json
import re
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from .automation import (
    FIXED_BRANCH,
    AutomationError,
    FileLock,
    GitRunner,
    _atomic_bytes,
    _atomic_json,
    _parse_worktrees,
    _redact_url_credentials,
    _select_initial_refs,
    locate_repository,
)

FEATURE_RE = re.compile(r"^\d{4}-\d{4}-\d{4}[a-z0-9]{2}-[a-z0-9][a-z0-9-]*$")
MAINTENANCE_BRANCH = "codexspec/maintenance"
MAINTENANCE_NAME = "worktree-for-codexspec-maintenance"


def _document(config: Path, invalid_code: str = "invalid_worktree_config") -> tuple[str, Any]:
    content = config.read_bytes().decode("utf-8") if config.exists() else ""
    try:
        node = yaml.compose(content)
    except yaml.YAMLError as exc:
        raise AutomationError(invalid_code, str(config)) from exc
    if node is not None and not isinstance(node, yaml.MappingNode):
        raise AutomationError(invalid_code, str(config))
    return content, node


def _field(node: Any, name: str) -> Any:
    if not isinstance(node, yaml.MappingNode):
        return None
    matches = [value for key, value in node.value if key.value == name]
    if len(matches) > 1:
        raise AutomationError("duplicate_config_key", name)
    return matches[0] if matches else None


def read_worktrees(config: Path) -> bool:
    """Default on; only an unquoted literal false in workflow disables isolation."""
    _, node = _document(config)
    value = _field(_field(node, "workflow"), "worktrees")
    return not (isinstance(value, yaml.ScalarNode) and value.tag == "tag:yaml.org,2002:bool" and value.value == "false")


class _AliasLoader(yaml.SafeLoader):
    """Retain the source ranges of aliases before composition resolves their identity."""

    def __init__(self, content: str):
        super().__init__(content)
        self.alias_ranges: list[tuple[int, int, Any]] = []

    def compose_node(self, parent: Any, index: Any) -> Any:
        event = self.peek_event()
        node = super().compose_node(parent, index)
        if isinstance(event, yaml.AliasEvent):
            self.alias_ranges.append((event.start_mark.index, event.end_mark.index, node))
        return node


class _FlowDumper(yaml.SafeDumper):
    pass


# Quoted strings keep multiline values on a single physical line in an alias replacement.
_FlowDumper.add_representer(
    str, lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:str", value, style='"')
)


def _expand_aliases(content: str) -> str:
    loader = _AliasLoader(content)
    try:
        loader.get_single_node()
        replacements = []
        for start, end, node in loader.alias_ranges:
            value = loader.construct_object(node, deep=True)
            rendered = yaml.dump(value, Dumper=_FlowDumper, default_flow_style=True, width=10**9).rstrip()
            if rendered.endswith("\n..."):
                rendered = rendered[:-4]
            replacements.append((start, end, rendered))
        for start, end, rendered in sorted(replacements, reverse=True):
            content = content[:start] + rendered + content[end:]
        return content
    finally:
        loader.dispose()


def write_config_scalar(
    config: Path,
    section: str,
    key: str,
    token: str,
    expected: Any,
    *,
    error_prefix: str = "worktree",
    invalid_section_code: str = "invalid_workflow_section",
) -> None:
    """Surgically set ``section.key`` to ``token`` without normalizing unrelated YAML.

    Preserves comments, line endings, and every other value; handles block and
    flow mappings, anchors, and an empty value. The edited document must parse to
    the original with only ``section.key`` replaced by ``expected``; otherwise an
    ``AutomationError`` is raised and the file is left untouched. The write is
    atomic. Error codes are ``invalid_<prefix>_config``, ``unsupported_<prefix>_config``,
    ``unrelated_config_change``, ``duplicate_config_key``, and ``invalid_section_code``.
    """
    original, node = _document(config, f"invalid_{error_prefix}_config")
    newline = "\r\n" if "\r\n" in original else "\n"
    try:
        content = _expand_aliases(original)
        node = yaml.compose(content)
    except (yaml.YAMLError, RecursionError) as exc:
        raise AutomationError(f"unsupported_{error_prefix}_config", str(config)) from exc
    mapping = _field(node, section)
    value = _field(mapping, key)
    if value is not None:
        start, end = value.start_mark.index, value.end_mark.index
        replacement = token
        if start == end and isinstance(value, yaml.ScalarNode) and value.value == "":
            # An empty value: keep a separator between the colon and the new token.
            replacement = token if content[start - 1 : start] == " " else " " + token
        content = content[:start] + replacement + content[end:]
    elif isinstance(mapping, yaml.MappingNode):
        if mapping.flow_style:
            offset = mapping.end_mark.index - 1
            addition = (", " if mapping.value else "") + f"{key}: {token}"
        else:
            offset = mapping.value[0][0].start_mark.index
            # Use the first actual key, not a preceding mapping anchor.
            indent = mapping.value[0][0].start_mark.column
            addition = f"{key}: {token}{newline}" + " " * indent
        content = content[:offset] + addition + content[offset:]
    elif mapping is not None:
        raise AutomationError(invalid_section_code, str(config))
    elif isinstance(node, yaml.MappingNode) and node.flow_style:
        offset = node.end_mark.index - 1
        addition = (", " if node.value else "") + f"{section}: {{{key}: {token}}}"
        content = content[:offset] + addition + content[offset:]
    else:
        end_event = next((event for event in yaml.parse(content) if isinstance(event, yaml.DocumentEndEvent)), None)
        offset = end_event.start_mark.index if end_event is not None and end_event.explicit else len(content)
        prefix = content[:offset].rstrip("\r\n")
        content = (
            prefix + (newline if prefix else "") + f"{section}:{newline}  {key}: {token}{newline}" + content[offset:]
        )
    try:
        before = yaml.safe_load(original) or {}
        expected_document = {**before, section: {**(before.get(section) or {}), key: expected}}
        if yaml.safe_load(content) != expected_document:
            raise AutomationError("unrelated_config_change", str(config))
    except (yaml.YAMLError, RecursionError, TypeError) as exc:
        raise AutomationError(f"unsupported_{error_prefix}_config", str(config)) from exc
    _atomic_bytes(config, content.encode("utf-8"))


def write_worktrees(config: Path, enabled: bool) -> None:
    """Surgically write one boolean without normalizing unrelated YAML or comments."""
    write_config_scalar(config, "workflow", "worktrees", str(enabled).lower(), enabled)


def feature_name(short_name: str) -> str:
    suffix = re.sub(r"[^a-z0-9]+", "-", short_name.lower()).strip("-")
    if not suffix:
        raise AutomationError("invalid_feature_name", "Use an ASCII short name, for example user-auth.")
    return (
        datetime.now().strftime("%Y-%m%d-%H%M")
        + "".join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(2))
        + "-"
        + suffix[:225].rstrip("-")
    )


class WorkspaceManager:
    """Create and resume registered workspaces without changing the invoking checkout."""

    def __init__(self, cwd: Path, *, runner: GitRunner | None = None):
        self.git = runner or GitRunner()
        self.context = locate_repository(cwd, runner=self.git)
        self.parent = self.context.worktree_path.parent
        self.records = self.context.common_git_dir / "codexspec-workspaces"

    def _identity(self, feature: str) -> tuple[str, Path, Path]:
        if feature == MAINTENANCE_NAME:
            branch = MAINTENANCE_BRANCH
        elif FEATURE_RE.fullmatch(feature):
            branch = feature
        else:
            raise AutomationError("invalid_feature_name", feature)
        return branch, self.parent / feature, self.records / f"{feature}.json"

    def _load(self, record: Path, branch: str, path: Path) -> dict[str, Any] | None:
        if not record.exists():
            return None
        try:
            data = json.loads(record.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise AutomationError("invalid_workspace_state", str(record)) from exc
        if not isinstance(data, dict) or data.get("branch") != branch or data.get("workspace") != str(path):
            raise AutomationError("workspace_state_mismatch", str(record))
        if data.get("status") not in {"creating", "merge_requires_resolution", "merge_requires_verification", "ready"}:
            raise AutomationError("invalid_workspace_state", str(record))
        if (
            not isinstance(data.get("baselines"), list)
            or len(data["baselines"]) not in (1, 2)
            or not all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{40,64}", v) for v in data["baselines"])
        ):
            raise AutomationError("invalid_workspace_state", str(record))
        return data

    def _registered(self, branch: str, path: Path) -> bool:
        if path.is_symlink() or self.parent.is_symlink():
            raise AutomationError("worktree_path_occupied", str(path))
        entries = _parse_worktrees(self.git.run(self.context.repository_root, "worktree", "list", "--porcelain").stdout)
        expected = f"refs/heads/{branch}"
        for entry in entries:
            if entry.get("branch") == expected and entry["path"] != path:
                raise AutomationError("worktree_path_mismatch", str(entry["path"]))
            if entry["path"] == path:
                if entry.get("branch") != expected or not path.is_dir():
                    raise AutomationError("worktree_branch_mismatch", str(path))
                top = self.git.run(path, "rev-parse", "--show-toplevel", check=False)
                common = self.git.run(path, "rev-parse", "--git-common-dir", check=False)
                actual_branch = self.git.run(path, "symbolic-ref", "--quiet", "HEAD", check=False)
                common_path = Path(common.stdout.strip())
                if not common_path.is_absolute():
                    common_path = path / common_path
                if (
                    top.returncode
                    or common.returncode
                    or actual_branch.returncode
                    or Path(top.stdout.strip()).resolve() != path
                    or common_path.resolve() != self.context.common_git_dir.resolve()
                    or actual_branch.stdout.strip() != expected
                ):
                    raise AutomationError("worktree_identity_mismatch", str(path))
                return True
        if path.exists():
            raise AutomationError("worktree_path_occupied", str(path))
        return False

    def _result(self, feature: str, data: dict[str, Any]) -> dict[str, Any]:
        result = dict(data)
        if feature != MAINTENANCE_NAME:
            target = self._artifact_path(feature, data)
            result.update(
                feature_id=feature[:16],
                feature_dir=str(target.parent),
                requirements_file=str(target),
            )
        return result

    def _artifact_path(self, feature: str, data: dict[str, Any]) -> Path:
        """Validate the same artifact boundary for creation, continuation and finish."""
        root = Path(data["workspace"])
        target = root / ".codexspec" / "specs" / feature / "requirements.md"
        try:
            validate_write_path(root, target)
        except AutomationError as exc:
            raise AutomationError("unsafe_feature_path", str(target)) from exc
        if target.exists() and not target.is_file():
            raise AutomationError("unsafe_feature_path", str(target))
        return target

    def _publish(self, feature: str, data: dict[str, Any]) -> None:
        if feature == MAINTENANCE_NAME:
            return
        target = self._artifact_path(feature, data)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            return
        from . import get_templates_dir

        template = get_templates_dir() / "docs" / "requirements-template.md"
        content = (
            template.read_text(encoding="utf-8")
            .replace("[FEATURE NAME]", feature[17:])
            .replace("[feature-id]", feature[:16])
        )
        with target.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content)

    def create(self, feature: str, *, reuse: bool = True) -> dict[str, Any]:
        branch, path, record = self._identity(feature)
        with FileLock(self.records / "create.lock"):
            registered = self._registered(branch, path)
            data = self._load(record, branch, path)
            if not reuse and (registered or data is not None):
                raise AutomationError("feature_identity_collision", feature)
            if registered and data is None:
                # Reuse an explicitly matching existing Git worktree; never reset its content.
                data = {
                    "workspace": str(path),
                    "branch": branch,
                    "status": "ready",
                    "warnings": [],
                    "baselines": [self.git.run(path, "rev-parse", "HEAD").stdout.strip()],
                }
                _atomic_json(record, data)
            if data is None:
                if (
                    self.git.run(
                        self.context.repository_root,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        f"refs/heads/{branch}",
                        check=False,
                    ).returncode
                    == 0
                ):
                    raise AutomationError("existing_feature_branch_without_workspace", branch)
                warnings = []
                if self.context.remote_name:
                    try:
                        fetched = self.git.run(
                            self.context.repository_root, "fetch", self.context.remote_name, check=False
                        )
                        if fetched.returncode != 0:
                            warnings.append(
                                "fetch_failed: remote information may be stale; "
                                + _redact_url_credentials(fetched.stderr.strip())
                            )
                    except AutomationError as exc:
                        warnings.append(
                            "fetch_failed: remote information may be stale; " + _redact_url_credentials(str(exc))
                        )
                start, merge = _select_initial_refs(self.context, self.git)
                refs = [start] + ([merge] if merge else [])
                baselines = [
                    self.git.run(self.context.repository_root, "rev-parse", ref + "^{commit}").stdout.strip()
                    for ref in refs
                ]
                data = {
                    "workspace": str(path),
                    "branch": branch,
                    "status": "creating",
                    "warnings": warnings,
                    "baselines": baselines,
                }
                _atomic_json(record, data)
            if not registered:
                if data["status"] != "creating":
                    raise AutomationError("missing_registered_workspace", str(path))
                exists = (
                    self.git.run(
                        self.context.repository_root,
                        "show-ref",
                        "--verify",
                        "--quiet",
                        f"refs/heads/{branch}",
                        check=False,
                    ).returncode
                    == 0
                )
                if exists:
                    actual = self.git.run(
                        self.context.repository_root, "rev-parse", f"refs/heads/{branch}"
                    ).stdout.strip()
                    if actual != data["baselines"][0]:
                        raise AutomationError("workspace_state_mismatch", branch)
                else:
                    self.git.run(self.context.repository_root, "branch", branch, data["baselines"][0])
                self.parent.mkdir(parents=True, exist_ok=True)
                self.git.run(self.context.repository_root, "worktree", "add", str(path), branch)
            if data["status"] == "creating":
                # An interrupted add may be resumed only at its recorded starting point.
                # Do not merge over another actor's work or silently certify its HEAD.
                head = self.git.run(path, "rev-parse", "HEAD").stdout.strip()
                dirty = self.git.run(path, "status", "--porcelain").stdout
                merging = self.git.run(path, "rev-parse", "--verify", "MERGE_HEAD", check=False).returncode == 0
                if head != data["baselines"][0] or dirty or merging:
                    raise AutomationError("workspace_state_mismatch", str(path))
                if len(data["baselines"]) == 2:
                    # Record the verification obligation before Git can leave a partial merge.
                    data["status"] = "merge_requires_verification"
                    _atomic_json(record, data)
                    result = self.git.run(path, "merge", "--no-edit", data["baselines"][1], check=False)
                    if result.returncode:
                        data["status"] = "merge_requires_resolution"
                        data["diagnostic"] = _redact_url_credentials(result.stderr.strip() or result.stdout.strip())
                else:
                    data["status"] = "ready"
                _atomic_json(record, data)
            if data["status"] == "ready":
                self._publish(feature, data)
            return self._result(feature, data)

    def resolve(self, feature: str) -> dict[str, Any]:
        branch, path, record = self._identity(feature)
        with FileLock(self.records / "create.lock"):
            if not self._registered(branch, path):
                raise AutomationError("missing_registered_workspace", str(path))
            data = self._load(record, branch, path)
            if data is None:
                data = {
                    "workspace": str(path),
                    "branch": branch,
                    "status": "ready",
                    "warnings": [],
                    "baselines": [self.git.run(path, "rev-parse", "HEAD").stdout.strip()],
                }
            return self._result(feature, data)

    def finish(self, feature: str, verification: dict[str, Any]) -> dict[str, Any]:
        branch, path, record = self._identity(feature)
        with FileLock(self.records / "create.lock"):
            if not self._registered(branch, path):
                raise AutomationError("missing_registered_workspace", str(path))
            data = self._load(record, branch, path)
            if data is None:
                raise AutomationError("missing_workspace_state", str(path))
            if feature != MAINTENANCE_NAME:
                self._artifact_path(feature, data)
            checks = verification.get("checks") if isinstance(verification, dict) else None
            head = self.git.run(path, "rev-parse", "HEAD").stdout.strip()
            tree = self.git.run(path, "rev-parse", "HEAD^{tree}").stdout.strip()
            clean = not self.git.run(path, "status", "--porcelain", "--untracked-files=no").stdout
            merging = self.git.run(path, "rev-parse", "--verify", "MERGE_HEAD", check=False).returncode == 0
            if (
                not isinstance(checks, list)
                or not checks
                or any(
                    not isinstance(check, dict)
                    or not check.get("command")
                    or type(check.get("exit_code")) is not int
                    or check["exit_code"] != 0
                    for check in checks
                )
            ):
                raise AutomationError("baseline_verification_failed", str(path))
            if verification.get("head") != head or verification.get("tree") != tree or not clean or merging:
                raise AutomationError("baseline_verification_stale_or_unresolved", str(path))
            for baseline in data["baselines"]:
                if self.git.run(path, "merge-base", "--is-ancestor", baseline, head, check=False).returncode:
                    raise AutomationError("baseline_history_not_integrated", baseline)
            data["status"] = "ready"
            data.pop("diagnostic", None)
            _atomic_json(record, data)
            self._publish(feature, data)
            return self._result(feature, data)


def validate_write_path(root: Path, target: Path) -> None:
    """Reject redirected paths and shared file inodes before routed writes."""
    try:
        parts = target.relative_to(root).parts
    except ValueError as exc:
        raise AutomationError("unsafe_write_path", str(target)) from exc
    current = root
    for part in (*parts, None):
        if (
            current.is_symlink()
            or (current != target and current.exists() and not current.is_dir())
            or (current.is_file() and current.stat().st_nlink > 1)
        ):
            raise AutomationError("unsafe_write_path", str(current))
        if part is not None:
            current = current / part


def checkout_root(cwd: Path) -> Path:
    """Locate the invoking checkout without requiring a usable main baseline."""
    cwd = cwd.resolve()
    git = GitRunner()
    top = git.run(cwd, "rev-parse", "--show-toplevel", check=False)
    return Path(top.stdout.strip()).resolve() if top.returncode == 0 else cwd


def write_destination(cwd: Path) -> Path:
    """Resolve a project writer's target while preserving checkout-local opt-out."""
    root = checkout_root(cwd)
    git = GitRunner()
    if not read_worktrees(root / ".codexspec/config.yml"):
        return root
    manager = WorkspaceManager(root, runner=git)
    current = git.run(root, "branch", "--show-current").stdout.strip()
    if current == FIXED_BRANCH:
        from .automation import locate_dedicated_workspace

        return locate_dedicated_workspace(manager.context, runner=git).path
    if FEATURE_RE.fullmatch(current):
        result = manager.resolve(current)
    elif current == MAINTENANCE_BRANCH:
        result = manager.resolve(MAINTENANCE_NAME)
    else:
        result = manager.create(MAINTENANCE_NAME)
    if result["status"] != "ready":
        raise AutomationError("workspace_not_ready", json.dumps(result))
    return Path(result["workspace"])
