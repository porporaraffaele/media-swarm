"""Competitors & Market Analysis Team assembly."""

from agno.team import Team, TeamMode

from src.agents.competitors.agents import (
    audience_segmentation_analyst,
    competitive_intelligence_analyst,
    industry_benchmarker,
    market_trend_researcher,
    pricing_strategist,
    swot_analyst,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

competitors_team = Team(
    name="Competitors & Market Team",
    role="Analyze competitors, market trends, pricing, benchmarks, and audience segments",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=6,
    members=[
        competitive_intelligence_analyst,
        market_trend_researcher,
        swot_analyst,
        pricing_strategist,
        industry_benchmarker,
        audience_segmentation_analyst,
    ],
    db=db,
    instructions=[
        "You are the Competitors & Market Analysis Team Orchestrator.",
        "For comprehensive market analysis, run agents iteratively:",
        "1. Start with Competitive Intelligence to map the landscape.",
        "2. Use Market Trend Researcher to identify opportunities.",
        "3. Run SWOT analysis combining internal and external data.",
        "4. Benchmark against industry standards.",
        "5. Segment audiences based on findings.",
        "Synthesize all analyses into a unified market intelligence report.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
