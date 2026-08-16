"""Unit tests for the profile-consumption module (src/codexspec/profile.py)."""

from pathlib import Path

from codexspec.profile import (
    PROFILE_BLOCK_END,
    PROFILE_BLOCK_START,
    PROFILE_CATEGORIES,
    ensure_profile_scaffold,
    inject_profile_block,
    render_profile_block,
)

# --- ensure_profile_scaffold ---


def test_scaffold_creates_six_category_dirs_with_gitkeep(tmp_path: Path) -> None:
    """T1.1-S1/S2: the store is the six categories, each scaffolded with a .gitkeep."""
    ensure_profile_scaffold(tmp_path)
    profile_dir = tmp_path / ".codexspec" / "profile"
    assert profile_dir.is_dir()
    assert set(PROFILE_CATEGORIES) == {
        "constraints",
        "conventions",
        "pitfalls",
        "decisions",
        "strategies",
        "runbooks",
    }
    for category in PROFILE_CATEGORIES:
        cat_dir = profile_dir / category
        assert cat_dir.is_dir()
        assert (cat_dir / ".gitkeep").exists()


def test_constraints_is_first_category(tmp_path: Path) -> None:
    """T1.1-S5: constraints stays the first element (highest weight, honored first)."""
    assert PROFILE_CATEGORIES[0] == "constraints"


def test_scaffold_migrates_existing_four_dir_store(tmp_path: Path) -> None:
    """T1.1-S4: a legacy four-directory profile gains strategies/ and runbooks/ on re-scaffold."""
    profile_dir = tmp_path / ".codexspec" / "profile"
    for legacy in ("constraints", "conventions", "pitfalls", "decisions"):
        (profile_dir / legacy).mkdir(parents=True)
    ensure_profile_scaffold(tmp_path)
    assert (profile_dir / "strategies").is_dir()
    assert (profile_dir / "strategies" / ".gitkeep").exists()
    assert (profile_dir / "runbooks").is_dir()
    assert (profile_dir / "runbooks" / ".gitkeep").exists()


def test_scaffold_is_idempotent_and_non_destructive(tmp_path: Path) -> None:
    """An existing record file is left byte-identical; scaffold only adds missing keeps."""
    profile_dir = tmp_path / ".codexspec" / "profile"
    (profile_dir / "pitfalls").mkdir(parents=True)
    record = "## P-2026-0812-14054p-1: real record\n- claim: something\n"
    (profile_dir / "pitfalls" / "P-2026-0812-14054p-1.md").write_text(record, encoding="utf-8")

    ensure_profile_scaffold(tmp_path)

    assert (profile_dir / "pitfalls" / "P-2026-0812-14054p-1.md").read_text(encoding="utf-8") == record
    # missing categories are created
    assert (profile_dir / "constraints").is_dir()


# --- render_profile_block (channel-neutral, pointers only) ---


def test_render_points_at_all_four_dirs_with_no_import() -> None:
    block = render_profile_block()
    for category in PROFILE_CATEGORIES:
        assert f".codexspec/profile/{category}/" in block
    # constraints are a strong mandatory pointer, not an @import
    assert "MUST read" in block
    assert "@import" not in block
    assert "@.codexspec" not in block


def test_render_is_status_aware() -> None:
    block = render_profile_block()
    assert "status" in block.lower()
    assert "candidate" in block and "vetted" in block


def test_render_points_at_strategies_and_runbooks() -> None:
    """T1.2-S1: the two new categories appear as pointers."""
    block = render_profile_block()
    assert ".codexspec/profile/strategies/" in block
    assert ".codexspec/profile/runbooks/" in block


def test_render_directs_active_recall() -> None:
    """T1.2-S2: the block instructs an active scan-and-match, not passive on-demand reading."""
    block = render_profile_block()
    # emphasis-free spans (pitfall P-2026-0813-1606fz-1)
    assert "scan the record headings and their" in block
    assert "read every record whose condition matches" in block


def test_render_carries_near_moment_distill_trigger() -> None:
    """T1.2-S3: the write-side near-moment distill trigger rule is present."""
    block = render_profile_block()
    assert "/codexspec:distill" in block
    assert "near that moment" in block
    assert "non-blocking and early-exits when there is nothing new" in block


def test_render_block_is_bounded_and_inlines_no_records() -> None:
    """T1.2-S4: the block is a fixed small directive (constraints first) that inlines no records."""
    block = render_profile_block()
    # constraints pointer precedes the on-demand pointers
    assert block.index("constraints/") < block.index("conventions/")
    # footprint is a fixed directive, independent of profile size
    assert len(block) < 2600
    # no distilled record content is inlined (record ids look like P-2026-…, Con-2026-…)
    assert "P-2026" not in block
    assert "Con-2026" not in block


# --- inject_profile_block (no channel param) ---


def test_inject_appends_one_bounded_block(tmp_path: Path) -> None:
    ctx = tmp_path / "CLAUDE.md"
    ctx.write_text("# CLAUDE.md\n\nexisting user content\n", encoding="utf-8")
    inject_profile_block(ctx)
    content = ctx.read_text(encoding="utf-8")
    assert content.count(PROFILE_BLOCK_START) == 1
    assert content.count(PROFILE_BLOCK_END) == 1
    assert "existing user content" in content


def test_inject_is_idempotent(tmp_path: Path) -> None:
    ctx = tmp_path / "AGENTS.md"
    ctx.write_text("# AGENTS.md\n\nbody\n", encoding="utf-8")
    inject_profile_block(ctx)
    once = ctx.read_text(encoding="utf-8")
    inject_profile_block(ctx)
    twice = ctx.read_text(encoding="utf-8")
    assert once == twice
    assert twice.count(PROFILE_BLOCK_START) == 1


def test_inject_only_touches_within_markers(tmp_path: Path) -> None:
    ctx = tmp_path / "CLAUDE.md"
    head = "# CLAUDE.md\n\nuser preamble line\n"
    ctx.write_text(head, encoding="utf-8")
    inject_profile_block(ctx)
    after = ctx.read_text(encoding="utf-8")
    assert after.startswith(head)
    outside_before = after.split(PROFILE_BLOCK_START, 1)[0]
    inject_profile_block(ctx)
    outside_after = ctx.read_text(encoding="utf-8").split(PROFILE_BLOCK_START, 1)[0]
    assert outside_before == outside_after


def test_claude_and_agents_get_identical_block(tmp_path: Path) -> None:
    """Uniform pointer: the injected block is identical across context files."""
    claude = tmp_path / "CLAUDE.md"
    agents = tmp_path / "AGENTS.md"
    claude.write_text("# CLAUDE.md\n", encoding="utf-8")
    agents.write_text("# AGENTS.md\n", encoding="utf-8")
    inject_profile_block(claude)
    inject_profile_block(agents)

    def block_of(p: Path) -> str:
        return p.read_text(encoding="utf-8").split(PROFILE_BLOCK_START, 1)[1].split(PROFILE_BLOCK_END, 1)[0]

    assert block_of(claude) == block_of(agents)
    assert "@import" not in block_of(claude)
