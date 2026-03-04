"""Tests for the command installer module."""

from pathlib import Path

from codexspec.commands.installer import (
    COMMANDS_SUBDIR,
    OLD_COMMAND_PREFIX,
    detect_old_structure,
    get_commands_metadata,
    install_commands_to_subdir,
    migrate_old_commands,
    should_update_commands,
)


class TestConstants:
    """Tests for module constants."""

    def test_commands_subdir_value(self) -> None:
        """COMMANDS_SUBDIR should be 'codexspec'."""
        assert COMMANDS_SUBDIR == "codexspec"

    def test_old_command_prefix_value(self) -> None:
        """OLD_COMMAND_PREFIX should be 'codexspec.'."""
        assert OLD_COMMAND_PREFIX == "codexspec."


class TestGetCommandsMetadata:
    """Tests for get_commands_metadata function."""

    def test_returns_list(self) -> None:
        """Should return a list."""
        result = get_commands_metadata()
        assert isinstance(result, list)

    def test_returns_correct_count(self) -> None:
        """Should return 16 commands (9 core + 4 enhanced + 3 git)."""
        result = get_commands_metadata()
        assert len(result) == 16

    def test_core_commands_count(self) -> None:
        """Should have 9 core commands."""
        result = get_commands_metadata()
        core_commands = [c for c in result if c["category"] == "core"]
        assert len(core_commands) == 9

    def test_enhanced_commands_count(self) -> None:
        """Should have 4 enhanced commands."""
        result = get_commands_metadata()
        enhanced_commands = [c for c in result if c["category"] == "enhanced"]
        assert len(enhanced_commands) == 4

    def test_git_commands_count(self) -> None:
        """Should have 3 git commands."""
        result = get_commands_metadata()
        git_commands = [c for c in result if c["category"] == "git"]
        assert len(git_commands) == 3

    def test_metadata_structure(self) -> None:
        """Each command should have all required fields."""
        result = get_commands_metadata()
        required_fields = {"name", "display_name", "description", "category", "file_name"}
        for cmd in result:
            assert set(cmd.keys()) == required_fields

    def test_display_name_format(self) -> None:
        """Display names should start with /codexspec."""
        result = get_commands_metadata()
        for cmd in result:
            assert cmd["display_name"].startswith("/codexspec.")

    def test_sorted_by_category(self) -> None:
        """Commands should be sorted core -> enhanced -> git."""
        result = get_commands_metadata()
        categories = [c["category"] for c in result]
        # Find the index of each category section
        core_idx = categories.index("core")
        enhanced_idx = categories.index("enhanced")
        git_idx = categories.index("git")
        # Core should come before enhanced, enhanced before git
        assert core_idx < enhanced_idx < git_idx


class TestDetectOldStructure:
    """Tests for detect_old_structure function."""

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Should return empty list if no commands directory exists."""
        result = detect_old_structure(tmp_path)
        assert result == []

    def test_no_old_commands(self, tmp_path: Path) -> None:
        """Should return empty list if no old structure files exist."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        # Create a non-codexspec file
        (commands_dir / "custom.md").write_text("# Custom")
        # Create a subdirectory (should be ignored)
        (commands_dir / "codexspec").mkdir()

        result = detect_old_structure(tmp_path)
        assert result == []

    def test_detects_old_commands(self, tmp_path: Path) -> None:
        """Should detect files with codexspec. prefix."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        # Create old structure files
        old_file1 = commands_dir / "codexspec.constitution.md"
        old_file2 = commands_dir / "codexspec.specify.md"
        old_file1.write_text("# Constitution")
        old_file2.write_text("# Specify")

        result = detect_old_structure(tmp_path)
        assert len(result) == 2
        assert old_file1 in result
        assert old_file2 in result

    def test_ignores_subdirectory_files(self, tmp_path: Path) -> None:
        """Should not detect files in subdirectories."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        subdir = commands_dir / "codexspec"
        subdir.mkdir()
        # Create file in subdirectory
        (subdir / "codexspec.test.md").write_text("# Test")
        # Create old structure file in root
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text("# Constitution")

        result = detect_old_structure(tmp_path)
        assert len(result) == 1
        assert old_file in result

    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        """Should return sorted list of paths."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        # Create files in non-alphabetical order
        (commands_dir / "codexspec.z-spec.md").write_text("# Z")
        (commands_dir / "codexspec.a-spec.md").write_text("# A")

        result = detect_old_structure(tmp_path)
        names = [p.name for p in result]
        assert names == sorted(names)


class TestMigrateOldCommands:
    """Tests for migrate_old_commands function."""

    def test_empty_list_returns_true(self, tmp_path: Path) -> None:
        """Should return True if no files to migrate."""
        result = migrate_old_commands(tmp_path, [])
        assert result is True

    def test_migrates_files(self, tmp_path: Path) -> None:
        """Should move old files to new subdirectory."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        # Create old files
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text("# Old Constitution")

        result = migrate_old_commands(tmp_path, [old_file])

        assert result is True
        # Old file should be gone
        assert not old_file.exists()
        # New file should exist
        new_file = commands_dir / COMMANDS_SUBDIR / "constitution.md"
        assert new_file.exists()
        assert new_file.read_text() == "# Old Constitution"

    def test_preserves_content(self, tmp_path: Path) -> None:
        """Should preserve file content during migration."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        original_content = "# My Custom Constitution\n\nCustom content here."
        old_file = commands_dir / "codexspec.constitution.md"
        old_file.write_text(original_content)

        migrate_old_commands(tmp_path, [old_file])

        new_file = commands_dir / COMMANDS_SUBDIR / "constitution.md"
        assert new_file.read_text() == original_content

    def test_creates_target_directory(self, tmp_path: Path) -> None:
        """Should create target directory if it doesn't exist."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        old_file = commands_dir / "codexspec.test.md"
        old_file.write_text("# Test")

        result = migrate_old_commands(tmp_path, [old_file])

        assert result is True
        assert (commands_dir / COMMANDS_SUBDIR).exists()

    def test_handles_multiple_files(self, tmp_path: Path) -> None:
        """Should migrate multiple files."""
        commands_dir = tmp_path / "commands"
        commands_dir.mkdir()
        files = []
        for name in ["constitution", "specify", "plan-to-tasks"]:
            f = commands_dir / f"codexspec.{name}.md"
            f.write_text(f"# {name}")
            files.append(f)

        result = migrate_old_commands(tmp_path, files)

        assert result is True
        for name in ["constitution", "specify", "plan-to-tasks"]:
            assert not (commands_dir / f"codexspec.{name}.md").exists()
            assert (commands_dir / COMMANDS_SUBDIR / f"{name}.md").exists()


class TestInstallCommandsToSubdir:
    """Tests for install_commands_to_subdir function."""

    def test_returns_zero_if_no_templates(self, tmp_path: Path) -> None:
        """Should return 0 if templates directory doesn't exist."""
        result = install_commands_to_subdir(tmp_path, tmp_path / "nonexistent")
        assert result == 0

    def test_installs_templates(self, tmp_path: Path) -> None:
        """Should copy template files to target directory."""
        # Create mock templates
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "constitution.md").write_text("# Constitution")
        (templates_dir / "specify.md").write_text("# Specify")

        target_dir = tmp_path / "target"
        result = install_commands_to_subdir(target_dir, templates_dir)

        assert result == 2
        assert (target_dir / "constitution.md").exists()
        assert (target_dir / "specify.md").exists()

    def test_skips_existing_without_force(self, tmp_path: Path) -> None:
        """Should skip existing files if force=False."""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "constitution.md").write_text("# New Constitution")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "constitution.md").write_text("# Old Constitution")

        result = install_commands_to_subdir(target_dir, templates_dir, force=False)

        assert result == 0
        assert (target_dir / "constitution.md").read_text() == "# Old Constitution"

    def test_overwrites_with_force(self, tmp_path: Path) -> None:
        """Should overwrite existing files if force=True."""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "constitution.md").write_text("# New Constitution")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        (target_dir / "constitution.md").write_text("# Old Constitution")

        result = install_commands_to_subdir(target_dir, templates_dir, force=True)

        assert result == 1
        assert (target_dir / "constitution.md").read_text() == "# New Constitution"

    def test_creates_target_directory(self, tmp_path: Path) -> None:
        """Should create target directory if it doesn't exist."""
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "test.md").write_text("# Test")

        target_dir = tmp_path / "new" / "target"
        result = install_commands_to_subdir(target_dir, templates_dir)

        assert result == 1
        assert target_dir.exists()


class TestShouldUpdateCommands:
    """Tests for should_update_commands function."""

    def test_returns_false_if_not_exists(self, tmp_path: Path) -> None:
        """Should return False if subdirectory doesn't exist."""
        # tmp_path is .codexspec, need to check .claude/commands/codexspec
        result = should_update_commands(tmp_path)
        assert result is False

    def test_returns_true_if_exists(self, tmp_path: Path) -> None:
        """Should return True if subdirectory exists."""
        # Create the expected directory structure
        claude_dir = tmp_path.parent / ".claude" / "commands" / COMMANDS_SUBDIR
        claude_dir.mkdir(parents=True)

        result = should_update_commands(tmp_path)
        assert result is True
