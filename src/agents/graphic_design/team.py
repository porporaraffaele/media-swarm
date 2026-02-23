"""Graphic Design Team assembly."""

from agno.team import Team, TeamMode

from src.agents.graphic_design.agents import (
    brand_template_designer,
    infographic_creator,
    motion_graphics_director,
    photo_editor,
    social_media_graphics_creator,
    thumbnail_cover_designer,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

graphic_design_team = Team(
    name="Graphic Design Team",
    role="Create all visual assets: social graphics, templates, infographics, thumbnails, motion",
    model=get_claude_sonnet(),
    mode=TeamMode.coordinate,
    members=[
        social_media_graphics_creator,
        brand_template_designer,
        infographic_creator,
        thumbnail_cover_designer,
        motion_graphics_director,
        photo_editor,
    ],
    db=db,
    instructions=[
        "You are the Graphic Design Team Orchestrator.",
        "Route design requests to the appropriate specialist.",
        "For complex projects, coordinate multiple designers.",
        "Ensure all output follows brand visual guidelines.",
        "Provide detailed generation prompts for AI image tools.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
