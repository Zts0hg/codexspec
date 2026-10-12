"""Install the shared runtime review standards into a selected project."""

from pathlib import Path

from .automation import AutomationError
from .worktrees import validate_write_path


def install_review_standards(source: Path, project: Path, *, force: bool = False) -> int:
    """Copy distributed Markdown bytes, preserving existing edits unless updating.

    All destinations are checked before the first copy. Unrelated extension
    files remain project-owned; no source/development mechanism is interpreted.
    """
    if not source.is_dir():
        raise AutomationError("missing_review_standards", str(source))
    files = sorted(source.rglob("*.md"))
    if not files:
        raise AutomationError("missing_review_standards", str(source))
    destination = project / ".codexspec" / "review-code"
    copies = [(path, destination / path.relative_to(source)) for path in files]
    for _, target in copies:
        validate_write_path(project, target)
        if target.exists() and not target.is_file():
            raise AutomationError("unsafe_write_path", f"Review standard destination is not a regular file: {target}")
    count = 0
    for path, target in copies:
        if target.exists() and not force:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
        count += 1
    return count
