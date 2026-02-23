"""Content Finder Team assembly."""

from agno.team import Team, TeamMode

from src.agents.content_finder.agents import (
    content_relevance_analyzer,
    niche_platform_scout,
    rights_license_checker,
    social_media_scout,
    trend_correlation_analyzer,
    web_content_scout,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

content_finder_team = Team(
    name="Content Finder Team",
    role="Find brand-relevant content across social, web, and niche platforms",
    model=get_claude_sonnet(),
    mode=TeamMode.broadcast,
    members=[
        social_media_scout,
        web_content_scout,
        niche_platform_scout,
        content_relevance_analyzer,
        rights_license_checker,
        trend_correlation_analyzer,
    ],
    db=db,
    instructions=[
        "You are the Content Finder Team Orchestrator.",
        "Broadcast search requests to all scouts simultaneously.",
        "All three scouts (Social, Web, Niche) search in parallel.",
        "Then analyze results with Relevance Analyzer and Rights Checker.",
        "Finally, Trend Correlation Analyzer identifies cross-platform patterns.",
        "Return a unified, ranked list of found content with rights status.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
