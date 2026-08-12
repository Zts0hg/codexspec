"""Project-profile consumption.

Wires a user project's ``.codexspec/profile/`` into the AI context files so that
knowledge distilled by ``/codexspec:distill`` is consulted in later work.

Store layout: **one record per file** under a per-category directory
(``constraints/`` ``conventions/`` ``pitfalls/`` ``decisions/``). Because parallel
feature branches each add differently-named record files, their distilled
knowledge merges without conflict.

Two concerns live here:

- ``ensure_profile_scaffold`` — create the four category directories (each kept
  by a ``.gitkeep``) so every injected reference resolves, independent of whether
  any knowledge has been distilled yet.
- ``render_profile_block`` / ``inject_profile_block`` — render a bounded,
  channel-neutral managed block (pointers only, no ``@import``) and inject it
  idempotently into a context file (CLAUDE.md or AGENTS.md) without disturbing any
  other content.

See the feature record under
``.codexspec/specs/2026-0812-14054p-profile-consumption/``.
"""

import re
from pathlib import Path

# Ordered: constraints first (highest weight, honored first). Each is a directory
# holding one record per file.
PROFILE_CATEGORIES = ("constraints", "conventions", "pitfalls", "decisions")

PROFILE_BLOCK_START = "<!-- CODEXSPEC PROFILE START -->"
PROFILE_BLOCK_END = "<!-- CODEXSPEC PROFILE END -->"

# Channel-neutral: identical for CLAUDE.md and AGENTS.md. Constraints are a strong
# mandatory pointer (no @import), so the block depends on no tool-specific import
# mechanism and the store can be one-file-per-record directories. Assembled from
# short literals to keep each source line within the line-length limit.
_PROFILE_BLOCK = "".join(
    [
        f"{PROFILE_BLOCK_START}\n",
        "## CodexSpec Project Profile\n\n",
        "**Project constraints (highest priority — read these FIRST):** before any non-trivial work you MUST ",
        "read every record under `.codexspec/profile/constraints/` — the project's hard prohibitions ",
        "(严禁 / 仅允许). Honor them before anything else.\n\n",
        "**Project profile — consult on demand when relevant to the task** ",
        "(each directory holds one record per file):\n\n",
        "- `.codexspec/profile/conventions/` — cross-feature conventions / steering; ",
        "read before adopting a pattern, structure, or naming choice.\n",
        "- `.codexspec/profile/pitfalls/` — known traps and their workarounds; ",
        "read before implementing or debugging in an area that may have bitten before.\n",
        "- `.codexspec/profile/decisions/` — past cross-feature / architectural decisions; ",
        "read before deciding in the same area, to reuse prior rationale rather than re-litigate it.\n\n",
        "Read the full record — each carries a `status` of `candidate` or `vetted`; ",
        "weight `candidate` items with appropriate caution. A directory may be empty ",
        "until `/codexspec:distill` has captured knowledge.\n",
        f"{PROFILE_BLOCK_END}\n",
    ]
)


def ensure_profile_scaffold(target_dir: Path) -> Path:
    """Create ``.codexspec/profile/`` and its four category directories if absent.

    Each category is a directory of one-record-per-file entries; a ``.gitkeep``
    keeps an empty category tracked so every pointer resolves. Idempotent and
    non-destructive: existing records and directories are never overwritten.
    """
    profile_dir = target_dir / ".codexspec" / "profile"
    for category in PROFILE_CATEGORIES:
        category_dir = profile_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        keep = category_dir / ".gitkeep"
        if not keep.exists():
            keep.write_text("", encoding="utf-8")
    return profile_dir


def render_profile_block() -> str:
    """Render the bounded managed profile block.

    Identical for CLAUDE.md and AGENTS.md: constraints and the three on-demand
    categories are all delivered as pointers to their directories — no ``@import``
    anywhere — so the block is channel-neutral and the store can be
    one-file-per-record directories that merge without conflict.
    """
    return _PROFILE_BLOCK


def inject_profile_block(context_path: Path) -> None:
    """Idempotently inject/update the profile block in ``context_path``.

    Only the bounded ``<!-- CODEXSPEC PROFILE START/END -->`` region is written;
    any other content in the file is preserved verbatim. Creates the file if it
    does not exist.
    """
    block = render_profile_block().rstrip("\n")
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
