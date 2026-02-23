"""Master Orchestrator Team assembly - top-level coordinator with all teams nested."""

from agno.team import Team, TeamMode

from src.agents.branding.team import branding_team
from src.agents.community.team import community_team
from src.agents.competitors.team import competitors_team
from src.agents.content_creator.team import content_creator_team
from src.agents.content_finder.team import content_finder_team
from src.agents.content_ideation.team import content_ideation_team
from src.agents.copywriting.team import copywriting_team
from src.agents.graphic_design.team import graphic_design_team
from src.agents.master_orchestrator.agents import (
    cost_controller,
    progress_tracker,
    task_decomposer,
    team_assembler,
    workflow_manager,
)
from src.agents.news.team import news_team
from src.config.models import get_claude_sonnet
from src.db.connection import db

master_orchestrator = Team(
    name="Master Orchestrator",
    role=(
        "Top-level coordinator that receives user requests, decomposes tasks, "
        "and delegates to specialized teams"
    ),
    model=get_claude_sonnet(),
    mode=TeamMode.coordinate,
    members=[
        # Internal orchestration agents
        task_decomposer,
        team_assembler,
        workflow_manager,
        cost_controller,
        progress_tracker,
        # All domain teams as nested members
        branding_team,
        copywriting_team,
        graphic_design_team,
        competitors_team,
        news_team,
        community_team,
        content_ideation_team,
        content_finder_team,
        content_creator_team,
    ],
    db=db,
    instructions=[
        "You are the Master Orchestrator of a complete AI media company.",
        "When you receive a user request:",
        "1. Use Task Decomposer to break it into discrete sub-tasks.",
        "2. Use Team Assembler to identify which teams are needed.",
        "3. Delegate sub-tasks to the appropriate domain teams.",
        "4. Use Workflow Manager to track execution flow.",
        "5. Use Cost Controller to monitor costs.",
        "6. Use Progress Tracker to report on completion.",
        "7. Synthesize all team outputs into a final deliverable.",
        "",
        "Available domain teams:",
        "- Branding Team: brand strategy, identity, naming, tone",
        "- Copywriting Team: SEO, social, email, ads, scripts",
        "- Graphic Design Team: social graphics, templates, infographics",
        "- Competitors Team: market analysis, SWOT, benchmarks",
        "- News Team: news aggregation, trends, fact-checking",
        "- Community Team: engagement, growth, crisis, influencers",
        "- Content Ideation Team: ideas, hooks, formats, calendar",
        "- Content Finder Team: find relevant content across platforms",
        "- Content Creator Team: generate images and videos with AI",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
