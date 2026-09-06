"""Maintain literal shared fragments for opted-in command template sources.

This module is maintainer tooling. Distributed CodexSpec code and ``codexspec
init`` intentionally know nothing about fragment directives.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import stat
import sys
import tempfile
import unicodedata
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

import yaml

DIRECTIVE_PATTERN = re.compile(rb"^<!-- CODEXSPEC:INCLUDE ([^\t\r\n ]+) -->$")
DIRECTIVE_NAMESPACE_PATTERN = re.compile(rb"([^\t\r\n :]+)")
DIRECTIVE_NAMESPACE = b"codexspec"
UTF8_BOM = b"\xef\xbb\xbf"
COMMAND_SOURCE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*\.md$")
CODEX_SKILL_ARTIFACT_PATTERN = re.compile(r"^codexspec-[A-Za-z0-9][A-Za-z0-9_-]*$")
WINDOWS_FORBIDDEN_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
WINDOWS_DEVICE_NAME = re.compile(
    r"^(?:CON|PRN|AUX|NUL|CLOCK\$|CONIN\$|CONOUT\$|COM[1-9¹²³]|LPT[1-9¹²³])(?:\..*)?$",
    re.IGNORECASE,
)
INTERNAL_CLAUDE_COMMANDS = frozenset({"check-i18n-semantics.md", "translate-docs.md"})
# These pre-existing plugin-only commands are still advertised to maintainers.
# Keep them outside template-derived comparison without deleting or rewriting them.
COMPATIBILITY_CLAUDE_COMMANDS = frozenset({"review-python-code.md", "review-react-code.md"})
ALLOWED_EXTRA_CLAUDE_COMMANDS = INTERNAL_CLAUDE_COMMANDS | COMPATIBILITY_CLAUDE_COMMANDS

StatSignature = tuple[int, int, int, int, int, int]
TreeSnapshot = tuple[tuple[str, StatSignature, bytes | None], ...]


class FragmentError(ValueError):
    """Report an invalid fragment source or stale generated output."""


def _line_body(line: bytes) -> bytes:
    if line.endswith(b"\r\n"):
        return line[:-2]
    if line.endswith(b"\n"):
        return line[:-1]
    return line


def _parse_directive(line: bytes, source_name: Path, line_number: int) -> bytes | None:
    body = _line_body(line)
    if not _has_directive_candidate(body):
        return None
    match = DIRECTIVE_PATTERN.fullmatch(body)
    if match is None:
        raise FragmentError(f"{source_name}:{line_number}: malformed fragment directive")
    return match.group(1)


def has_fragment_directive_line(content: bytes) -> bool:
    """Return whether bytes contain a valid or malformed standalone directive line."""
    return any(_has_directive_candidate(_line_body(line)) for line in content.splitlines(keepends=True))


def _edit_distance_at_most_one(left: bytes, right: bytes) -> bool:
    if left == right:
        return True
    if abs(len(left) - len(right)) > 1:
        return False
    if len(left) == len(right):
        return sum(a != b for a, b in zip(left, right, strict=True)) == 1
    if len(left) > len(right):
        left, right = right, left
    index_left = index_right = edits = 0
    while index_left < len(left) and index_right < len(right):
        if left[index_left] == right[index_right]:
            index_left += 1
            index_right += 1
            continue
        edits += 1
        if edits > 1:
            return False
        index_right += 1
    return True


def _has_directive_candidate(body: bytes) -> bool:
    stripped = body.lstrip(b" \t")
    if stripped.startswith(UTF8_BOM):
        # A UTF-8 BOM before a directive-like line must stay a candidate so that the
        # renderer fails loudly and the packaging guard flags it, instead of the line
        # silently passing through every guard as ordinary prose.
        stripped = stripped[len(UTF8_BOM) :].lstrip(b" \t")
    if not stripped.startswith(b"<!--"):
        return False
    comment = stripped[4:].lstrip(b" \t")
    match = DIRECTIVE_NAMESPACE_PATTERN.match(comment)
    if match is None:
        return False
    namespace = match.group(1).lower()
    return namespace.startswith(DIRECTIVE_NAMESPACE) or _edit_distance_at_most_one(namespace, DIRECTIVE_NAMESPACE)


def _absolute_path(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _common_boundary(*paths: Path) -> Path:
    return Path(os.path.commonpath([_absolute_path(path) for path in paths]))


def _stable_directory(
    path: Path,
    display: str,
    *,
    boundary: Path | None = None,
) -> tuple[Path, StatSignature]:
    absolute = _absolute_path(path)
    _reject_symlink_components(absolute, _absolute_path(boundary or absolute), display)
    try:
        metadata = absolute.stat(follow_symlinks=False)
    except OSError as exc:
        raise FragmentError(f"{display}: cannot access directory: {exc}") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise FragmentError(f"{display}: not a directory")
    return absolute, _stat_signature(metadata)


def _verify_directory_identity(
    path: Path,
    identity: StatSignature,
    display: str,
    *,
    boundary: Path | None = None,
) -> None:
    _reject_symlink_components(path, _absolute_path(boundary or path), display)
    try:
        metadata = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise FragmentError(f"{display}: directory changed during operation: {exc}") from exc
    if not stat.S_ISDIR(metadata.st_mode) or _stat_signature(metadata) != identity:
        raise FragmentError(f"{display}: directory changed during operation")


def _refresh_directory_identity(
    path: Path,
    identity: StatSignature,
    display: str,
    *,
    boundary: Path | None = None,
) -> StatSignature:
    _, refreshed = _stable_directory(path, display, boundary=boundary)
    if refreshed[:3] != identity[:3]:
        raise FragmentError(f"{display}: directory changed during operation")
    return refreshed


def _verify_directory_physical_identity(
    path: Path,
    identity: StatSignature,
    display: str,
    *,
    boundary: Path | None = None,
) -> None:
    _reject_symlink_components(path, _absolute_path(boundary or path), display)
    try:
        metadata = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise FragmentError(f"{display}: directory changed during operation: {exc}") from exc
    if not stat.S_ISDIR(metadata.st_mode) or _stat_signature(metadata)[:3] != identity[:3]:
        raise FragmentError(f"{display}: directory changed during operation")


def _reject_symlink_components(path: Path, root: Path, display: str) -> None:
    current = path
    while True:
        if current.is_symlink():
            raise FragmentError(f"{display}: symbolic links are forbidden")
        if current == root:
            return
        if current == current.parent:
            raise FragmentError(f"{display}: path is outside its declared root")
        current = current.parent


def _portable_segment_is_safe(name: str) -> bool:
    try:
        name.encode("utf-8")
    except UnicodeEncodeError:
        return False
    windows_path = PureWindowsPath(name)
    return not (
        not name
        or name in {".", ".."}
        or WINDOWS_FORBIDDEN_CHARACTERS.search(name)
        or name.endswith((" ", "."))
        or windows_path.drive
        or windows_path.root
        or windows_path.is_reserved()
        or WINDOWS_DEVICE_NAME.fullmatch(name)
    )


def portable_name_key(name: str) -> str:
    """Return the cross-platform comparison key for a portable filename."""
    return unicodedata.normalize("NFC", name).casefold()


def _stat_signature(metadata: os.stat_result) -> StatSignature:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_ctime_ns,
    )


def _stat_identity(metadata: os.stat_result) -> tuple[int, int]:
    """Return the mutation fields that compare reliably across path-stat and fstat.

    On Windows, os.stat(path) and os.fstat(fd) can disagree on st_dev, st_ino,
    and the timestamp fields for the same untouched file, so cross-source checks
    compare only the mode and size; timestamp drift is caught by the same-source
    full-signature pairs inside _read_stable_file_snapshot.
    """
    return (metadata.st_mode, metadata.st_size)


def _validate_fragment_tree(directory: Path, fragments_root: Path) -> None:
    seen_names: dict[str, str] = {}
    for entry in sorted(directory.iterdir(), key=lambda path: path.name):
        if not _portable_segment_is_safe(entry.name):
            display = entry.relative_to(fragments_root)
            raise FragmentError(f"unsafe fragment entry name: {display}")
        folded = portable_name_key(entry.name)
        if folded in seen_names:
            display = directory.relative_to(fragments_root)
            raise FragmentError(
                f"case-colliding fragment names under {display}: {seen_names[folded]!r} and {entry.name!r}"
            )
        seen_names[folded] = entry.name
        _reject_symlink_components(entry, fragments_root, str(entry.relative_to(fragments_root)))
        metadata = entry.stat(follow_symlinks=False)
        if stat.S_ISDIR(metadata.st_mode):
            _validate_fragment_tree(entry, fragments_root)
        elif not stat.S_ISREG(metadata.st_mode):
            display = entry.relative_to(fragments_root)
            raise FragmentError(f"fragment entry is not a regular file: {display}")
        elif entry.name != ".gitkeep":
            if not COMMAND_SOURCE_PATTERN.fullmatch(entry.name):
                display = entry.relative_to(fragments_root)
                raise FragmentError(f"unsafe fragment entry name: {display}")
            display = entry.relative_to(fragments_root)
            fragment = _read_stable_file(entry, fragments_root, str(display))
            for line_number, line in enumerate(fragment.splitlines(keepends=True), start=1):
                nested = _parse_directive(line, display, line_number)
                if nested is not None:
                    raise FragmentError(f"{display}: nested fragment directives are forbidden")


def _read_stable_file_snapshot(path: Path, root: Path, display: str) -> tuple[bytes, StatSignature]:
    _reject_symlink_components(path, root, display)
    try:
        before = path.stat(follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise FragmentError(f"{display}: file is not a regular file")
        with path.open("rb") as handle:
            opened_before = os.fstat(handle.fileno())
            if _stat_identity(before) != _stat_identity(opened_before):
                raise FragmentError(f"{display}: file changed while being opened")
            content = handle.read()
            opened_after = os.fstat(handle.fileno())
        after = path.stat(follow_symlinks=False)
    except FragmentError:
        raise
    except OSError as exc:
        raise FragmentError(f"{display}: cannot read stable file: {exc}") from exc
    _reject_symlink_components(path, root, display)
    identities = {
        _stat_identity(before),
        _stat_identity(opened_before),
        _stat_identity(opened_after),
        _stat_identity(after),
    }
    if (
        not stat.S_ISREG(opened_after.st_mode)
        or len(identities) != 1
        or _stat_signature(before) != _stat_signature(after)
        or _stat_signature(opened_before) != _stat_signature(opened_after)
    ):
        raise FragmentError(f"{display}: file changed while being read")
    return content, _stat_signature(after)


def _verify_file_identity(path: Path, root: Path, display: str, identity: StatSignature) -> None:
    _reject_symlink_components(path, root, display)
    try:
        metadata = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise FragmentError(f"{display}: file changed during operation: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode) or _stat_signature(metadata) != identity:
        raise FragmentError(f"{display}: file changed during operation")


def _read_stable_file(path: Path, root: Path, display: str) -> bytes:
    return _read_stable_file_snapshot(path, root, display)[0]


def _tree_snapshot(root: Path) -> TreeSnapshot:
    entries: list[tuple[str, StatSignature, bytes | None]] = []

    def visit(directory: Path) -> None:
        for entry in sorted(directory.iterdir(), key=lambda path: path.name):
            relative = entry.relative_to(root).as_posix()
            _reject_symlink_components(entry, root, relative)
            metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(metadata.st_mode):
                entries.append((relative + "/", _stat_signature(metadata), None))
                visit(entry)
            elif stat.S_ISREG(metadata.st_mode):
                content, signature = _read_stable_file_snapshot(entry, root, relative)
                entries.append((relative, signature, hashlib.sha256(content).digest()))
            else:
                entries.append((relative, _stat_signature(metadata), None))

    visit(root)
    return tuple(entries)


def _authoring_snapshot(sources_root: Path, fragments_root: Path) -> tuple[TreeSnapshot, TreeSnapshot]:
    return _tree_snapshot(sources_root), _tree_snapshot(fragments_root)


def _fragment_path(fragment_name: bytes, fragments_root: Path, source_name: Path, line_number: int) -> Path:
    try:
        name = fragment_name.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise FragmentError(f"{source_name}:{line_number}: fragment path must be UTF-8") from exc

    segments = name.split("/")
    if (
        not name
        or name.startswith("/")
        or "\\" in name
        or any(not _portable_segment_is_safe(segment) for segment in segments)
        or not COMMAND_SOURCE_PATTERN.fullmatch(segments[-1])
    ):
        raise FragmentError(f"{source_name}:{line_number}: unsafe fragment path {name!r}")

    candidate = fragments_root
    for segment in segments:
        if not candidate.is_dir():
            raise FragmentError(f"{source_name}:{line_number}: fragment {name!r} does not exist")
        entries = {entry.name: entry for entry in candidate.iterdir()}
        if segment not in entries:
            aliases = [name for name in entries if portable_name_key(name) == portable_name_key(segment)]
            if aliases:
                raise FragmentError(
                    f"{source_name}:{line_number}: fragment {name!r} must use exact stored spelling {aliases[0]!r}"
                )
            raise FragmentError(f"{source_name}:{line_number}: fragment {name!r} does not exist")
        candidate = entries[segment]
    _reject_symlink_components(candidate, fragments_root, f"{source_name}:{line_number}: fragment {name!r}")
    if not candidate.exists() or not candidate.is_file():
        raise FragmentError(f"{source_name}:{line_number}: fragment {name!r} does not exist")

    resolved_root = fragments_root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        message = f"{source_name}:{line_number}: fragment {name!r} resolves outside the fragment root"
        raise FragmentError(message) from exc
    return candidate


def _render_source(source_path: Path, sources_root: Path, fragments_root: Path) -> bytes:
    source_name = Path(source_path.name)
    rendered: list[bytes] = []
    source = _read_stable_file(source_path, sources_root, str(source_name))
    for line_number, line in enumerate(source.splitlines(keepends=True), start=1):
        fragment_name = _parse_directive(line, source_name, line_number)
        if fragment_name is None:
            rendered.append(line)
            continue

        fragment_path = _fragment_path(fragment_name, fragments_root, source_name, line_number)
        display = fragment_path.relative_to(fragments_root)
        fragment = _read_stable_file(fragment_path, fragments_root, str(display))
        for fragment_line_number, fragment_line in enumerate(fragment.splitlines(keepends=True), start=1):
            nested = _parse_directive(fragment_line, display, fragment_line_number)
            if nested is not None:
                raise FragmentError(f"{display}: nested fragment directives are forbidden")
        rendered.append(fragment)
    return b"".join(rendered)


def _render_sources_with_snapshot(
    sources_root: Path,
    fragments_root: Path,
) -> tuple[dict[Path, bytes], tuple[TreeSnapshot, TreeSnapshot]]:
    boundary = _common_boundary(sources_root, fragments_root)
    sources_root, sources_identity = _stable_directory(sources_root, "source root", boundary=boundary)
    fragments_root, fragments_identity = _stable_directory(fragments_root, "fragment root", boundary=boundary)
    snapshot_before = _authoring_snapshot(sources_root, fragments_root)

    rendered: dict[Path, bytes] = {}
    seen_source_names: dict[str, str] = {}
    for source in sorted(sources_root.iterdir(), key=lambda path: path.name):
        if source.name == ".gitkeep":
            continue
        if not COMMAND_SOURCE_PATTERN.fullmatch(source.name) or not _portable_segment_is_safe(source.name):
            raise FragmentError(f"unsafe command source name: {source.name!r}")
        folded = portable_name_key(source.name)
        if folded in seen_source_names:
            raise FragmentError(
                f"case-colliding command source names: {seen_source_names[folded]!r} and {source.name!r}"
            )
        seen_source_names[folded] = source.name
        if source.is_symlink():
            raise FragmentError(f"{source.name}: symbolic links are forbidden")
        metadata = source.stat(follow_symlinks=False)
        if not stat.S_ISREG(metadata.st_mode):
            raise FragmentError(f"{source.name}: command source is not a regular file")
        rendered[Path(source.name)] = _render_source(source, sources_root, fragments_root)
    _validate_fragment_tree(fragments_root, fragments_root)
    _verify_directory_identity(sources_root, sources_identity, "source root", boundary=boundary)
    _verify_directory_identity(fragments_root, fragments_identity, "fragment root", boundary=boundary)
    snapshot_after = _authoring_snapshot(sources_root, fragments_root)
    if snapshot_before != snapshot_after:
        raise FragmentError("sources or fragments changed while rendering")
    return rendered, snapshot_after


def render_sources(sources_root: Path, fragments_root: Path) -> dict[Path, bytes]:
    """Render every opted-in top-level Markdown command source."""
    return _render_sources_with_snapshot(sources_root, fragments_root)[0]


def _inspect_output(
    output: Path,
    outputs_root: Path,
    relative_path: Path,
) -> tuple[bytes, int, StatSignature] | None:
    _reject_symlink_components(output, outputs_root, str(relative_path))
    try:
        metadata = output.stat(follow_symlinks=False)
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise FragmentError(f"{relative_path}: cannot inspect generated output: {exc}") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise FragmentError(f"{relative_path}: generated output is not a regular file")
    content, signature = _read_stable_file_snapshot(output, outputs_root, str(relative_path))
    try:
        verified = output.stat(follow_symlinks=False)
    except OSError as exc:
        raise FragmentError(f"{relative_path}: generated output changed during prevalidation") from exc
    if _stat_signature(verified) != signature:
        raise FragmentError(f"{relative_path}: generated output changed during prevalidation")
    return content, stat.S_IMODE(signature[2]), signature


def _validate_output_namespace(outputs_root: Path, source_names: set[Path]) -> None:
    outputs_by_key: dict[str, str] = {}
    for output in sorted(outputs_root.iterdir(), key=lambda path: path.name):
        if not COMMAND_SOURCE_PATTERN.fullmatch(output.name) or not _portable_segment_is_safe(output.name):
            raise FragmentError(f"unsafe command output name: {output.name!r}")
        _reject_symlink_components(output, outputs_root, output.name)
        metadata = output.stat(follow_symlinks=False)
        if not stat.S_ISREG(metadata.st_mode):
            raise FragmentError(f"{output.name}: command output is not a regular file")
        key = portable_name_key(output.name)
        if key in outputs_by_key:
            raise FragmentError(f"portable command output names collide: {outputs_by_key[key]!r} and {output.name!r}")
        outputs_by_key[key] = output.name

    for source_name in source_names:
        existing = outputs_by_key.get(portable_name_key(source_name.name))
        if existing is not None and existing != source_name.name:
            raise FragmentError(f"{source_name.name} collides with unmanaged command output {existing}")


def check_outputs(sources_root: Path, fragments_root: Path, outputs_root: Path) -> None:
    """Fail without writing when any opted-in generated output is missing or stale."""
    rendered = render_sources(sources_root, fragments_root)
    boundary = _common_boundary(sources_root, fragments_root, outputs_root)
    outputs_root, outputs_identity = _stable_directory(outputs_root, "output root", boundary=boundary)
    _validate_output_namespace(outputs_root, set(rendered))
    failures: list[str] = []
    for relative_path, expected in rendered.items():
        output = outputs_root / relative_path
        current = _inspect_output(output, outputs_root, relative_path)
        if current is None:
            failures.append(f"{relative_path}: generated output is missing")
        elif current[0] != expected:
            failures.append(f"{relative_path}: generated output is stale")
    _verify_directory_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
    if failures:
        raise FragmentError("\n".join(failures))


def _atomic_write(
    path: Path,
    content: bytes,
    outputs_root: Path,
    mode: int,
    expected_identity: StatSignature | None,
    outputs_identity: StatSignature,
    boundary: Path,
) -> None:
    temporary: Path | None = None
    try:
        _verify_directory_physical_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
        with tempfile.NamedTemporaryFile(prefix=f".{path.name}.", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.chmod(mode)
        _verify_directory_physical_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
        _reject_symlink_components(path, outputs_root, path.name)
        try:
            current = path.stat(follow_symlinks=False)
        except FileNotFoundError:
            current = None
        if expected_identity is None and current is not None:
            raise FragmentError(f"{path.name}: generated output changed after prevalidation")
        if expected_identity is not None and (
            current is None or not stat.S_ISREG(current.st_mode) or _stat_signature(current) != expected_identity
        ):
            raise FragmentError(f"{path.name}: generated output changed after prevalidation")
        os.replace(temporary, path)
    except FragmentError:
        raise
    except OSError as exc:
        raise FragmentError(f"{path.name}: cannot atomically replace generated output: {exc}") from exc
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def write_outputs(sources_root: Path, fragments_root: Path, outputs_root: Path) -> list[Path]:
    """Prevalidate all sources, then atomically update changed opted-in outputs."""
    rendered, authoring_snapshot = _render_sources_with_snapshot(sources_root, fragments_root)
    boundary = _common_boundary(sources_root, fragments_root, outputs_root)
    outputs_root, outputs_identity = _stable_directory(outputs_root, "output root", boundary=boundary)
    _validate_output_namespace(outputs_root, set(rendered))
    inspected = {
        relative_path: _inspect_output(outputs_root / relative_path, outputs_root, relative_path)
        for relative_path in rendered
    }
    _verify_directory_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
    current_rendered, current_snapshot = _render_sources_with_snapshot(sources_root, fragments_root)
    if current_rendered != rendered or current_snapshot != authoring_snapshot:
        raise FragmentError("sources or fragments changed before writing")

    changed: list[Path] = []
    for relative_path, expected in rendered.items():
        output = outputs_root / relative_path
        current = inspected[relative_path]
        if current is not None and current[0] == expected:
            continue
        mode = current[1] if current is not None else 0o644
        identity = current[2] if current is not None else None
        _verify_directory_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
        _atomic_write(output, expected, outputs_root, mode, identity, outputs_identity, boundary)
        changed.append(relative_path)
        outputs_identity = _refresh_directory_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
    _verify_directory_identity(outputs_root, outputs_identity, "output root", boundary=boundary)
    return changed


def _compare_artifacts(
    label: str,
    expected: dict[str, bytes],
    actual: dict[str, bytes | None],
    *,
    allowed_extra: frozenset[str] = frozenset(),
) -> list[str]:
    failures: list[str] = []
    expected_names = set(expected)
    actual_names = set(actual)
    present_names = {name for name, content in actual.items() if content is not None}
    missing = sorted(expected_names - present_names)
    unexpected = sorted(actual_names - expected_names - allowed_extra)
    stale = sorted(name for name in expected_names & present_names if actual[name] != expected[name])
    if missing:
        failures.append(f"{label} artifacts missing: {', '.join(missing)}")
    if unexpected:
        failures.append(f"{label} artifacts unexpected: {', '.join(unexpected)}")
    if stale:
        failures.append(f"{label} artifacts stale: {', '.join(stale)}")
    return failures


def _claude_artifacts(
    commands_root: Path,
    *,
    canonical_generated: bool = False,
    boundary: Path | None = None,
) -> dict[str, bytes]:
    if not commands_root.is_dir():
        return {}
    commands_root, root_identity = _stable_directory(commands_root, "Claude artifact root", boundary=boundary)
    artifacts: dict[str, bytes] = {}
    identities: dict[str, StatSignature] = {}
    seen_names: dict[str, str] = {}
    for path in sorted(commands_root.iterdir(), key=lambda item: item.name):
        if not COMMAND_SOURCE_PATTERN.fullmatch(path.name) or not _portable_segment_is_safe(path.name):
            raise FragmentError(f"unsafe Claude artifact name: {path.name!r}")
        key = portable_name_key(path.name)
        if key in seen_names:
            raise FragmentError(f"portable Claude artifact names collide: {seen_names[key]!r} and {path.name!r}")
        seen_names[key] = path.name
        content, signature = _read_stable_file_snapshot(path, commands_root, f"Claude artifact {path.name}")
        artifacts[path.name] = content
        identities[path.name] = signature
    for name, identity in identities.items():
        _verify_file_identity(commands_root / name, commands_root, f"Claude artifact {name}", identity)
    _verify_directory_identity(commands_root, root_identity, "Claude artifact root", boundary=boundary)
    if canonical_generated:
        return {name: content.replace(b"\r\n", b"\n") for name, content in artifacts.items()}
    return artifacts


def _codex_artifacts(
    skills_root: Path,
    *,
    canonical_generated: bool = False,
    boundary: Path | None = None,
) -> dict[str, bytes | None]:
    if not skills_root.is_dir():
        return {}
    skills_root, root_identity = _stable_directory(skills_root, "Codex artifact root", boundary=boundary)
    artifacts: dict[str, bytes | None] = {}
    skill_identities: dict[str, StatSignature] = {}
    skill_file_identities: dict[str, StatSignature] = {}
    seen_names: dict[str, str] = {}
    for skill_dir in sorted(skills_root.iterdir(), key=lambda item: item.name):
        if not CODEX_SKILL_ARTIFACT_PATTERN.fullmatch(skill_dir.name) or not _portable_segment_is_safe(skill_dir.name):
            raise FragmentError(f"unsafe Codex artifact name: {skill_dir.name!r}")
        key = portable_name_key(skill_dir.name)
        if key in seen_names:
            raise FragmentError(f"portable Codex artifact names collide: {seen_names[key]!r} and {skill_dir.name!r}")
        seen_names[key] = skill_dir.name
        _reject_symlink_components(skill_dir, skills_root, f"Codex artifact {skill_dir.name}")
        metadata = skill_dir.stat(follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode):
            raise FragmentError(f"Codex artifact {skill_dir.name}: not a directory")
        skill_dir, skill_identity = _stable_directory(skill_dir, f"Codex artifact {skill_dir.name}")
        skill_identities[skill_dir.name] = skill_identity
        for entry in sorted(skill_dir.iterdir(), key=lambda item: item.name):
            entry_display = f"Codex artifact {skill_dir.name}/{entry.name}"
            _reject_symlink_components(entry, skill_dir, entry_display)
            if entry.name != "SKILL.md":
                raise FragmentError(f"{entry_display}: unexpected entry")
        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_symlink():
            raise FragmentError(f"Codex artifact {skill_dir.name}/SKILL.md: symbolic links are forbidden")
        if skill_file.is_file():
            content, skill_file_identity = _read_stable_file_snapshot(
                skill_file,
                skill_dir,
                f"Codex artifact {skill_dir.name}/SKILL.md",
            )
            skill_file_identities[skill_dir.name] = skill_file_identity
        else:
            content = None
        if canonical_generated and content is not None:
            content = content.replace(b"\r\n", b"\n")
        artifacts[skill_dir.name] = content
        _verify_directory_identity(skill_dir, skill_identity, f"Codex artifact {skill_dir.name}")
    for name, identity in skill_file_identities.items():
        _verify_file_identity(
            skills_root / name / "SKILL.md", skills_root / name, f"Codex artifact {name}/SKILL.md", identity
        )
    for name, identity in skill_identities.items():
        _verify_directory_identity(skills_root / name, identity, f"Codex artifact {name}", boundary=skills_root)
    _verify_directory_identity(skills_root, root_identity, "Codex artifact root", boundary=boundary)
    return artifacts


def check_self_bootstrap(root: Path, *, language: str) -> None:
    """Compare tracked Claude/Codex artifacts with fresh existing-generator output."""
    from codexspec.integrations.claude import ClaudeIntegration
    from codexspec.integrations.codex import CodexIntegration

    root, root_identity = _stable_directory(root, "repository root")
    templates, templates_identity = _stable_directory(
        root / "templates" / "commands", "distributed command template root", boundary=root
    )
    templates_snapshot = _tree_snapshot(templates)

    with tempfile.TemporaryDirectory(prefix="codexspec-command-distribution-") as temporary:
        target = Path(temporary)
        with patch("codexspec.integrations.codex.sys.platform", "linux"):
            ClaudeIntegration().install(target, templates, force=True, language=language)
            CodexIntegration().install_skills(target, templates, force=True, language=language)

        expected_claude = _claude_artifacts(
            target / ".claude" / "commands" / "codexspec",
            canonical_generated=True,
            boundary=target,
        )
        expected_codex = _codex_artifacts(target / ".agents" / "skills", canonical_generated=True, boundary=target)

    actual_claude = _claude_artifacts(root / ".claude" / "commands" / "codexspec", boundary=root)
    actual_codex = _codex_artifacts(root / ".agents" / "skills", boundary=root)
    failures = _compare_artifacts(
        "Claude",
        expected_claude,
        actual_claude,
        allowed_extra=ALLOWED_EXTRA_CLAUDE_COMMANDS,
    )
    failures.extend(_compare_artifacts("Codex", expected_codex, actual_codex))
    if _tree_snapshot(templates) != templates_snapshot:
        failures.append("distributed command templates changed during operation")
    _verify_directory_identity(templates, templates_identity, "distributed command template root", boundary=root)
    _verify_directory_identity(root, root_identity, "repository root")
    if failures:
        raise FragmentError("\n".join(failures))


def _repository_roots(root: Path) -> tuple[Path, Path, Path]:
    authoring = root / "internal" / "command_templates"
    return authoring / "sources", authoring / "fragments", root / "templates" / "commands"


def _interaction_language(root: Path) -> str:
    config_path = root / ".codexspec" / "config.yml"
    if not config_path.is_file():
        return "en"
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise FragmentError(f"cannot read interaction language from {config_path}: {exc}") from exc
    language = config.get("language") if isinstance(config, dict) else None
    if not isinstance(language, dict):
        return "en"
    value = language.get("interaction") or language.get("output") or "en"
    return str(value)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="verify opted-in outputs without writing")
    modes.add_argument("--write", action="store_true", help="synchronize opted-in complete command outputs")
    modes.add_argument(
        "--check-distribution",
        action="store_true",
        help="verify opted-in outputs and tracked Claude/Codex distribution artifacts",
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the explicit maintainer check or write workflow."""
    args = _parser().parse_args(argv)
    repository_root = _absolute_path(args.root)
    sources, fragments, outputs = _repository_roots(repository_root)
    try:
        if args.write:
            changed = write_outputs(sources, fragments, outputs)
            for relative_path in changed:
                print(f"updated {relative_path}")
        else:
            check_outputs(sources, fragments, outputs)
            if args.check_distribution:
                check_self_bootstrap(repository_root, language=_interaction_language(repository_root))
    except FragmentError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
