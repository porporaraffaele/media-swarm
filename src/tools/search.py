"""Tavily search tools helper.

TavilyTools uses os.getenv("TAVILY_API_KEY") internally, but pydantic-settings
reads .env into the Settings object without exporting to process env vars.
This helper passes the key explicitly.
"""

from agno.tools.tavily import TavilyTools

from src.config.settings import settings


def get_tavily_tools() -> TavilyTools:
    """Create TavilyTools with the API key from settings."""
    return TavilyTools(api_key=settings.tavily_api_key)
