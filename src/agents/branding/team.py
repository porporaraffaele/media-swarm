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
        "",
        "For a COMPLETE brand project, follow this exact workflow:",
        "1. Brand Strategist gathers a brief from the user (sector, target, values).",
        "2. Naming Specialist proposes 5 names and ASKS the user to choose.",
        "3. Brand Positioning Analyst defines competitive positioning.",
        "4. Brand Storyteller crafts the brand narrative using the chosen name.",
        "5. Visual Identity Designer creates colors, typography, logo direction.",
        "6. Tone of Voice Specialist defines communication guidelines.",
        "7. Brand Auditor checks consistency across all deliverables.",
        "8. Cultural Sensitivity Reviewer does the final review.",
        "",
        "For partial requests, involve only the relevant specialists.",
        "Your outputs serve downstream teams: Copywriting, Graphic Design,",
        "Ads Expert, Web/Blog, Community, and Content Ideation.",
        "Synthesize all specialist outputs into a unified brand guide.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
