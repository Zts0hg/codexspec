"""Unit tests for the profile-consumption module (src/codexspec/profile.py).

Scenario numbers refer to T-001 in
.codexspec/specs/2026-0812-14054p-profile-consumption/tasks.md.
"""

from pathlib import Path

import pytest

from codexspec.profile import (
    PROFILE_BLOCK_END,
    PROFILE_BLOCK_START,
    PROFILE_FILES,
    ensure_profile_scaffold,
    inject_profile_block,
    render_profile_block,
)

# --- ensure_profile_scaffold ---


def test_scaffold_creates_dir_and_four_header_only_files(tmp_path: Path) -> None:
    """Scenario 1."""
    ensure_profile_scaffold(tmp_path)
    profile_dir = tmp_path / ".codexspec" / "profile"
    assert profile_dir.is_dir()
    assert set(PROFILE_FILES) == {"constraints.md", "conventions.md", "pitfalls.md", "decisions.md"}
    for name in PROFILE_FILES:
        f = profile_dir / name
        assert f.exists() and f.read_text(encoding="utf-8").strip() != ""


def test_scaffold_is_idempotent_and_non_destructive(tmp_path: Path) -> None:
    """Scenario 2: an existing file with distilled records is left byte-identical."""
    profile_dir = tmp_path / ".codexspec" / "profile"
    profile_dir.mkdir(parents=True)
    record = "# Pitfalls\n\n## P-001: real record\n- claim: something\n"
    (profile_dir / "pitfalls.md").write_text(record, encoding="utf-8")

    ensure_profile_scaffold(tmp_path)

    assert (profile_dir / "pitfalls.md").read_text(encoding="utf-8") == record
    # the missing ones are created
    assert (profile_dir / "constraints.md").exists()


# --- render_profile_block ---


def test_render_claude_uses_import_and_lists_pointers() -> None:
    """Scenario 3."""
    block = render_profile_block("claude")
    assert "@.codexspec/profile/constraints.md" in block
    for name in ("conventions.md", "pitfalls.md", "decisions.md"):
        assert f".codexspec/profile/{name}" in block


def test_render_codex_uses_pointer_and_no_import() -> None:
    """Scenario 4."""
    block = render_profile_block("codex")
    assert "constraints.md" in block
    assert "MUST read" in block
    assert "@import" not in block
    assert "@.codexspec" not in block


def test_render_both_channels_instruct_status_aware_ondemand_read() -> None:
    """Scenario 5 (REQ-007)."""
    for channel in ("claude", "codex"):
        block = render_profile_block(channel)
        assert "status" in block.lower()
        assert "candidate" in block and "vetted" in block


def test_render_rejects_unknown_channel() -> None:
    """Scenario 9."""
    with pytest.raises(ValueError):
        render_profile_block("gemini")


# --- inject_profile_block ---


def test_inject_appends_one_bounded_block(tmp_path: Path) -> None:
    """Scenario 6."""
    ctx = tmp_path / "CLAUDE.md"
    ctx.write_text("# CLAUDE.md\n\nexisting user content\n", encoding="utf-8")
    inject_profile_block(ctx, "claude")
    content = ctx.read_text(encoding="utf-8")
    assert content.count(PROFILE_BLOCK_START) == 1
    assert content.count(PROFILE_BLOCK_END) == 1
    assert "existing user content" in content


def test_inject_is_idempotent(tmp_path: Path) -> None:
    """Scenario 7."""
    ctx = tmp_path / "AGENTS.md"
    ctx.write_text("# AGENTS.md\n\nbody\n", encoding="utf-8")
    inject_profile_block(ctx, "codex")
    once = ctx.read_text(encoding="utf-8")
    inject_profile_block(ctx, "codex")
    twice = ctx.read_text(encoding="utf-8")
    assert once == twice
    assert twice.count(PROFILE_BLOCK_START) == 1


def test_inject_only_touches_within_markers(tmp_path: Path) -> None:
    """Scenario 8: content outside the markers is byte-identical before/after."""
    ctx = tmp_path / "CLAUDE.md"
    head = "# CLAUDE.md\n\nuser preamble line\n"
    ctx.write_text(head, encoding="utf-8")
    inject_profile_block(ctx, "claude")
    after = ctx.read_text(encoding="utf-8")
    # the preamble (everything before the block) is preserved verbatim
    assert after.startswith(head)
    # a second inject must not alter the outside region either
    outside_before = after.split(PROFILE_BLOCK_START, 1)[0]
    inject_profile_block(ctx, "claude")
    outside_after = ctx.read_text(encoding="utf-8").split(PROFILE_BLOCK_START, 1)[0]
    assert outside_before == outside_after
