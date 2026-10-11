"""Managed context instructions for staged commit analysis."""

import json
import re
import shlex
from pathlib import Path

START = "<!-- CODEXSPEC COMMITS START -->"
END = "<!-- CODEXSPEC COMMITS END -->"


def render_commit_guidance(invocation: str) -> str:
    """Return the shared context rule for installed integrations and plugins."""
    return f"""{START}
## Commit Messages

Before creating an authorized Git commit, invoke `{invocation}` to analyze staged
changes and generate the message. This applies in plain conversation and SDD
workflows, including auto-dev feature commits and blueprint commits. Command
availability alone is not an invocation.

The calling workflow prepares staging. `commit-staged` must not choose or stage
files, and must not describe unstaged changes or conversation-only intent. Use a
body when needed to cover material staged changes accurately and completely.

For helper-owned commits, prepare the helper's explicit index first, invoke
`{invocation} -p` against that index, and pass the full message and analyzed tree
to the helper's finalization action. Keep ownership, path, locking, and recovery
checks. If content changes, prepare and analyze again before committing; never
fall back to a fixed message or direct Git execution to bypass a failed check.
This rule does not grant authorization to stage, commit, or push.
{END}"""


def inject_commit_guidance(path: Path, invocation: str) -> None:
    """Preserve project prose while updating the bounded commit trigger."""
    block = render_commit_guidance(invocation)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(existing):
        updated = pattern.sub(lambda _match: block, existing)
    else:
        updated = existing + ("\n" if existing.endswith("\n") else "\n\n") + block + "\n"
    path.write_text(updated, encoding="utf-8", newline="\n")


def install_plugin_commit_guidance(plugin: Path) -> Path:
    """Install SessionStart context without needing the CLI or project init.

    Git is already required for commits. Its shell alias provides printf on all
    Git platforms; exec-form hooks pass this static command without host-shell
    interpolation or dependencies on the plugin cache path.
    """
    from .commit_runtime import AutomationError

    destination = plugin.absolute() / "hooks" / "hooks.json"
    for part in (destination, *destination.parents):
        if part.is_symlink():
            raise AutomationError("linked_commit_guidance", str(part))
    if destination.exists() and (not destination.is_file() or destination.stat().st_nlink != 1):
        raise AutomationError("shared_commit_guidance", str(destination))
    guidance = render_commit_guidance("/codexspec:commit-staged")
    hook = {
        "type": "command",
        "command": "git",
        "args": [
            "-c",
            "alias.codexspec-commit-guidance=!printf '%s\\n' " + shlex.quote(guidance),
            "codexspec-commit-guidance",
        ],
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps({"hooks": {"SessionStart": [{"hooks": [hook]}]}}, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    return destination
