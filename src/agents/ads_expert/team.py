"""Ads Expert Team assembly."""

from agno.team import Team, TeamMode

from src.agents.ads_expert.agents import (
    ab_optimization_specialist,
    ad_creative_specialist,
    budget_roi_analyst,
    fb_instagram_specialist,
    google_ads_specialist,
    linkedin_ads_specialist,
    tiktok_ads_specialist,
    youtube_ads_specialist,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

ads_expert_team = Team(
    name="Ads Expert Team",
    role=(
        "Plan, create, optimize, and analyze paid advertising campaigns across all major platforms"
    ),
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=8,
    members=[
        fb_instagram_specialist,
        google_ads_specialist,
        tiktok_ads_specialist,
        linkedin_ads_specialist,
        youtube_ads_specialist,
        ad_creative_specialist,
        ab_optimization_specialist,
        budget_roi_analyst,
    ],
    db=db,
    instructions=[
        "You are the Ads Expert Team Orchestrator.",
        "Coordinate the advertising workflow:",
        "1. Understand the campaign goal, target audience, and budget.",
        "2. Select the right platform specialists based on the request.",
        "3. Ad Creative Specialist produces copy and visual briefs.",
        "4. Platform specialists build campaign plans with targeting and bidding.",
        "5. A/B Testing Specialist designs test variants.",
        "6. Budget & ROI Analyst allocates budget and forecasts performance.",
        "",
        "Output: complete campaign plan with creatives, targeting, budget, and KPIs.",
        "Always recommend measurable goals and clear attribution.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
