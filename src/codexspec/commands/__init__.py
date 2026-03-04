"""Commands module for CodexSpec.

This module contains command installation and migration logic.
"""

from .installer import (
    COMMANDS_SUBDIR,
    OLD_COMMAND_PREFIX,
    CommandMetadata,
    detect_old_structure,
    get_commands_metadata,
    install_commands_to_subdir,
    migrate_old_commands,
    should_update_commands,
)

__all__ = [
    "COMMANDS_SUBDIR",
    "OLD_COMMAND_PREFIX",
    "CommandMetadata",
    "detect_old_structure",
    "get_commands_metadata",
    "install_commands_to_subdir",
    "migrate_old_commands",
    "should_update_commands",
]
