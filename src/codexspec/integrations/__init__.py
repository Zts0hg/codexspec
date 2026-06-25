"""AI coding tool integrations for CodexSpec."""

from .base import Integration
from .claude import ClaudeIntegration
from .codex import CodexIntegration


def get_integrations(ai: str) -> list[Integration]:
    """Resolve the requested AI target into concrete integrations."""
    normalized = ai.strip().lower()
    if normalized == "claude":
        return [ClaudeIntegration()]
    if normalized == "codex":
        return [CodexIntegration()]
    if normalized == "both":
        return [ClaudeIntegration(), CodexIntegration()]
    raise ValueError(f"Unsupported AI assistant: {ai}")


__all__ = ["ClaudeIntegration", "CodexIntegration", "Integration", "get_integrations"]
