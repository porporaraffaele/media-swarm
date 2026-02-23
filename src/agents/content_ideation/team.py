"""Content Ideation Team assembly."""

from agno.team import Team, TeamMode

from src.agents.content_ideation.agents import (
    content_calendar_planner,
    format_strategist,
    hook_angle_creator,
    tone_duration_optimizer,
    trend_adapter,
    viral_potential_scorer,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

content_ideation_team = Team(
    name="Content Ideation Team",
    role="Generate content ideas with formats, hooks, angles, tone, duration, and viral scoring",
    model=get_claude_sonnet(),
    mode=TeamMode.coordinate,
    members=[
        format_strategist,
        hook_angle_creator,
        trend_adapter,
        content_calendar_planner,
        tone_duration_optimizer,
        viral_potential_scorer,
    ],
    db=db,
    instructions=[
        "You are the Content Ideation Team Orchestrator.",
        "For content ideation requests, coordinate specialists:",
        "1. Hook & Angle Creator generates ideas with compelling angles.",
        "2. Trend Adapter checks for relevant trend opportunities.",
        "3. Format Strategist recommends optimal formats per idea.",
        "4. Tone & Duration Optimizer fine-tunes delivery parameters.",
        "5. Viral Potential Scorer ranks ideas by potential impact.",
        "6. Calendar Planner schedules top ideas into the editorial calendar.",
        "Deliver a ranked list of content ideas with full specifications.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
