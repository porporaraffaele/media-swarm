"""Tavily search tools helper.

TavilyTools uses os.getenv("TAVILY_API_KEY") internally, but pydantic-settings
reads .env into the Settings object without exporting to process env vars.
This module exports the key to os.environ so TavilyClient can find it,
and also passes it explicitly in the helper function.
"""

import os

from agno.tools.tavily import TavilyTools

from src.config.settings import settings

# Export to process env so TavilyClient finds it via os.getenv()
if settings.tavily_api_key:
    os.environ["TAVILY_API_KEY"] = settings.tavily_api_key


def get_tavily_tools() -> TavilyTools:
    """Create TavilyTools with the API key from settings."""
    return TavilyTools(api_key=settings.tavily_api_key)
