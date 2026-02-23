"""LLM model factory for all agents."""

from agno.models.anthropic import Claude


def get_claude_sonnet() -> Claude:
    """Primary model for most agents - high quality reasoning and generation."""
    return Claude(id="claude-sonnet-4-20250514")


def get_claude_haiku() -> Claude:
    """Faster/cheaper model for simple sub-tasks (classification, scoring, routing)."""
    return Claude(id="claude-haiku-4-5-20251001")
