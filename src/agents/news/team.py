"""News Agent Team assembly."""

from agno.team import Team, TeamMode

from src.agents.news.agents import (
    alert_manager,
    fact_checker,
    news_aggregator,
    news_summarizer,
    relevance_scorer,
    trend_detector,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

news_team = Team(
    name="News Team",
    role="Aggregate, analyze, verify, and summarize news for the brand",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=6,
    members=[
        news_aggregator,
        trend_detector,
        fact_checker,
        news_summarizer,
        relevance_scorer,
        alert_manager,
    ],
    db=db,
    instructions=[
        "You are the News Team Orchestrator.",
        "Run the news pipeline iteratively:",
        "1. Aggregator collects raw news from sources.",
        "2. Relevance Scorer filters by brand relevance.",
        "3. Fact Checker verifies key claims.",
        "4. Trend Detector identifies patterns.",
        "5. Summarizer creates the final briefing.",
        "6. Alert Manager flags urgent items.",
        "Produce a structured daily briefing with actionable insights.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
