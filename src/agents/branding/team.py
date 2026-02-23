"""Branding Team assembly."""

from agno.team import Team, TeamMode

from src.agents.branding.agents import (
    brand_auditor,
    brand_positioning_analyst,
    brand_storyteller,
    brand_strategist,
    cultural_sensitivity_reviewer,
    naming_specialist,
    tone_of_voice_specialist,
    visual_identity_designer,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

branding_team = Team(
    name="Branding Team",
    role="Handle all brand strategy, identity, naming, positioning, and cultural review",
    model=get_claude_sonnet(),
    mode=TeamMode.coordinate,
    members=[
        brand_strategist,
        visual_identity_designer,
        tone_of_voice_specialist,
        brand_storyteller,
        brand_auditor,
        naming_specialist,
        brand_positioning_analyst,
        cultural_sensitivity_reviewer,
    ],
    db=db,
    instructions=[
        "You are the Branding Team Orchestrator.",
        "Decompose branding requests and delegate to the right specialist(s).",
        "For comprehensive brand projects, involve multiple specialists.",
        "Always have the Cultural Sensitivity Reviewer check final output.",
        "Synthesize results into a unified branding deliverable.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
