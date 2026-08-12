"""Project-profile consumption.

Wires a user project's ``.codexspec/profile/`` into the AI context files so that
knowledge distilled by ``/codexspec:distill`` is consulted in later work. Two
concerns live here:

- ``ensure_profile_scaffold`` — create the profile directory and header-only
  placeholder files so every injected reference resolves (no dangling reference),
  independent of whether any knowledge has been distilled yet.
- ``render_profile_block`` / ``inject_profile_block`` — render a bounded,
  channel-adaptive managed block and inject it idempotently into a context file
  (CLAUDE.md or AGENTS.md) without disturbing any other content.

See the feature record under
``.codexspec/specs/2026-0812-14054p-profile-consumption/``.
"""

import re
from pathlib import Path

# Ordered: constraints first (highest weight, honored first).
PROFILE_FILES = ("constraints.md", "conventions.md", "pitfalls.md", "decisions.md")

PROFILE_BLOCK_START = "<!-- CODEXSPEC PROFILE START -->"
PROFILE_BLOCK_END = "<!-- CODEXSPEC PROFILE END -->"

_VALID_CHANNELS = ("claude", "codex")

# Header-only placeholders. distill appends records below the header on first
# write; pre-creating them makes the Claude @import and every pointer resolve.
_SCAFFOLD_HEADERS = {
    "constraints.md": (
        "# Constraints\n\n"
        "<!-- Negative constraints (严禁 / 仅允许); highest weight, honored first. "
        "Managed by /codexspec:distill. -->\n"
    ),
    "conventions.md": (
        "# Conventions\n\n<!-- Positive cross-feature conventions / steering. Managed by /codexspec:distill. -->\n"
    ),
    "pitfalls.md": (
        "# Pitfalls\n\n<!-- Cross-feature traps and their workarounds. Managed by /codexspec:distill. -->\n"
    ),
    "decisions.md": (
        "# Decisions\n\n<!-- Cross-feature / architectural decisions (ADR-lite). Managed by /codexspec:distill. -->\n"
    ),
}

_POINTER_INDEX = (
    "**Project profile — consult on demand when relevant to the task:**\n\n"
    "- `.codexspec/profile/conventions.md` — cross-feature conventions / steering; "
    "read before adopting a pattern, structure, or naming choice.\n"
    "- `.codexspec/profile/pitfalls.md` — known traps and their workarounds; "
    "read before implementing or debugging in an area that may have bitten before.\n"
    "- `.codexspec/profile/decisions.md` — past cross-feature / architectural decisions; "
    "read before deciding in the same area, to reuse prior rationale rather than re-litigate it.\n\n"
    "Read the full record — each carries a `status` of `candidate` or `vetted`; "
    "weight `candidate` items with appropriate caution. These files may be empty "
    "until `/codexspec:distill` has captured knowledge.\n"
)


def ensure_profile_scaffold(target_dir: Path) -> Path:
    """Create ``.codexspec/profile/`` and its header-only files if absent.

    Idempotent and non-destructive: an existing file (e.g. one already holding
    distilled records) is never overwritten.
    """
    profile_dir = target_dir / ".codexspec" / "profile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    for name in PROFILE_FILES:
        target = profile_dir / name
        if not target.exists():
            target.write_text(_SCAFFOLD_HEADERS[name], encoding="utf-8")
    return profile_dir


def render_profile_block(channel: str) -> str:
    """Render the bounded managed block for ``channel`` ('claude' or 'codex').

    Constraints are delivered channel-adaptively: Claude via ``@import`` (always
    present + auto-fresh from the live file); Codex via a strong mandatory pointer
    (auto-fresh, no ``@import`` dependency). Both then carry the same on-demand
    pointer index for conventions/pitfalls/decisions.
    """
    if channel not in _VALID_CHANNELS:
        raise ValueError(f"Unknown channel: {channel!r} (expected one of {_VALID_CHANNELS})")

    if channel == "claude":
        constraints = (
            "**Project constraints (highest priority — always honor these first):**\n\n"
            "@.codexspec/profile/constraints.md\n"
        )
    else:  # codex
        constraints = (
            "**Project constraints (highest priority — always honor these first):**\n\n"
            "Before any non-trivial work you MUST read `.codexspec/profile/constraints.md` — "
            "these are the project's hard prohibitions (严禁 / 仅允许). Honor them before anything else.\n"
        )

    return (
        f"{PROFILE_BLOCK_START}\n## CodexSpec Project Profile\n\n{constraints}\n{_POINTER_INDEX}{PROFILE_BLOCK_END}\n"
    )


def inject_profile_block(context_path: Path, channel: str) -> None:
    """Idempotently inject/update the profile block in ``context_path``.

    Only the bounded ``<!-- CODEXSPEC PROFILE START/END -->`` region is written;
    any other content in the file is preserved verbatim. Creates the file if it
    does not exist.
    """
    block = render_profile_block(channel).rstrip("\n")
    existing = context_path.read_text(encoding="utf-8") if context_path.exists() else ""

    pattern = re.compile(
        re.escape(PROFILE_BLOCK_START) + r".*?" + re.escape(PROFILE_BLOCK_END),
        re.DOTALL,
    )
    if pattern.search(existing):
        # Function replacement avoids backslash/group interpretation in `block`.
        updated = pattern.sub(lambda _match: block, existing)
    elif existing.strip():
        updated = existing.rstrip() + "\n\n" + block + "\n"
    else:
        updated = block + "\n"

    context_path.write_text(updated, encoding="utf-8")
