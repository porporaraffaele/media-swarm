"""LLM model factory for all agents.

Exports API keys to os.environ because pydantic-settings loads .env into the
Settings object but does NOT set them as environment variables. The Anthropic
SDK resolves credentials from os.environ, so we must bridge the gap here.
"""

import os

from agno.models.anthropic import Claude

from src.config.settings import settings

# ─── Export API keys to os.environ (same pattern as src/tools/search.py) ──────
if settings.anthropic_api_key:
    os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key
if settings.openai_api_key:
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key
if settings.google_api_key:
    os.environ["GOOGLE_API_KEY"] = settings.google_api_key


def get_claude_sonnet() -> Claude:
    """Primary model for most agents - high quality reasoning and generation."""
    return Claude(
        id="claude-sonnet-4-20250514",
        api_key=settings.anthropic_api_key or None,
    )


def get_claude_haiku() -> Claude:
    """Faster/cheaper model for simple sub-tasks (classification, scoring, routing)."""
    return Claude(
        id="claude-haiku-4-5-20251001",
        api_key=settings.anthropic_api_key or None,
    )
