"""Claude Code integration."""

from pathlib import Path

from codexspec.commands.installer import COMMANDS_SUBDIR, install_commands_to_subdir


class ClaudeIntegration:
    """Installs CodexSpec as Claude Code slash commands."""

    key = "claude"
    display_name = "Claude Code"
    context_file = "CLAUDE.md"

    def invocation_for(self, command_name: str) -> str:
        """Return the Claude slash command invocation."""
        return f"/codexspec:{command_name}"

    def commands_dir(self, target_dir: Path) -> Path:
        """Return the Claude command destination."""
        return target_dir / ".claude" / "commands" / COMMANDS_SUBDIR

    def install(self, target_dir: Path, templates_dir: Path, *, force: bool = False, language: str = "en") -> int:
        """Install Claude slash command templates."""
        return install_commands_to_subdir(self.commands_dir(target_dir), templates_dir, force=force, language=language)
