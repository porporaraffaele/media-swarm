"""Community Builder Team assembly."""

from agno.team import Team, TeamMode

from src.agents.community.agents import (
    ambassador_program_manager,
    comment_dm_responder,
    community_analytics_agent,
    crisis_manager,
    engagement_strategist,
    event_coordinator,
    growth_hacker,
    influencer_outreach,
    ugc_curator,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

community_team = Team(
    name="Community Builder Team",
    role="Build and manage the brand community: engagement, growth, crisis, influencers, events",
    model=get_claude_sonnet(),
    mode=TeamMode.route,
    members=[
        engagement_strategist,
        comment_dm_responder,
        ugc_curator,
        growth_hacker,
        community_analytics_agent,
        crisis_manager,
        influencer_outreach,
        event_coordinator,
        ambassador_program_manager,
    ],
    db=db,
    instructions=[
        "You are the Community Builder Team Orchestrator.",
        "Route community requests to the most appropriate specialist:",
        "- Engagement plans -> Engagement Strategist",
        "- Reply drafts -> Comment & DM Responder",
        "- UGC campaigns -> UGC Curator",
        "- Growth strategies -> Growth Hacker",
        "- Community data -> Community Analytics",
        "- Negative situations -> Crisis Manager",
        "- Influencer work -> Influencer Outreach",
        "- Event planning -> Event Coordinator",
        "- Ambassador programs -> Ambassador Program Manager",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
