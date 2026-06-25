"""Shared integration protocol."""

from pathlib import Path
from typing import Protocol


class Integration(Protocol):
    """Protocol implemented by each AI coding tool integration."""

    key: str
    display_name: str
    context_file: str

    def invocation_for(self, command_name: str) -> str:
        """Return the user-facing invocation for a CodexSpec command."""
        ...

    def install(self, target_dir: Path, templates_dir: Path, *, force: bool = False, language: str = "en") -> int:
        """Install this integration into target_dir."""
        ...
