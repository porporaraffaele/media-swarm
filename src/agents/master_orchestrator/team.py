"""Master Orchestrator Team assembly - top-level coordinator with all teams nested."""

from agno.team import Team, TeamMode

from src.agents.ads_expert.team import ads_expert_team
from src.agents.analyst.team import analyst_team
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
from src.agents.sales.team import sales_team
from src.agents.web_blog.team import web_blog_team
from src.config.models import get_claude_sonnet
from src.db.connection import db

master_orchestrator = Team(
    name="Master Orchestrator",
    role=(
        "Top-level coordinator that receives user requests, decomposes tasks, "
        "and delegates to all 14 specialized teams"
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
        # All 13 domain teams as nested members
        branding_team,
        copywriting_team,
        graphic_design_team,
        competitors_team,
        news_team,
        community_team,
        content_ideation_team,
        content_finder_team,
        content_creator_team,
        analyst_team,
        sales_team,
        ads_expert_team,
        web_blog_team,
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
        "IMPORTANT workflow rules:",
        "- For branding projects: ALWAYS start with the Branding Team first.",
        "  Branding output (name, values, visual identity, tone) must be ready",
        "  BEFORE other teams (Copywriting, Graphic Design, Ads, Web) can work.",
        "- For content campaigns: Competitors analysis → Content Ideation → then",
        "  Content Creator, Copywriting, and Graphic Design in parallel.",
        "- Pass upstream team outputs as context to downstream teams.",
        "",
        "Available domain teams (14):",
        "- Branding Team: brand strategy, identity, naming, tone, positioning",
        "- Copywriting Team: SEO, social, email, ads, scripts, UX copy",
        "- Graphic Design Team: social graphics, templates, infographics, motion",
        "- Competitors Team: market analysis, SWOT, benchmarks, segmentation",
        "- News Team: news aggregation, trends, fact-checking, alerts",
        "- Community Team: engagement, growth, crisis, influencers, events",
        "- Content Ideation Team: ideas, hooks, formats, calendar, viral scoring",
        "- Content Finder Team: find content across social, web, niche platforms",
        "- Content Creator Team: generate images and videos with AI tools",
        "- Analyst Team: performance analysis, quality audit, self-improvement",
        "- Sales Team: lead generation, qualification, outreach, CRM pipeline",
        "- Ads Expert Team: Facebook, Google, TikTok, LinkedIn, YouTube campaigns",
        "- Web/Blog Team: SEO, blog content, landing pages, email, analytics",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
