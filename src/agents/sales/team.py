"""Sales & Lead Generation Team assembly."""

from agno.team import Team, TeamMode

from src.agents.sales.agents import (
    crm_manager,
    lead_generator,
    lead_qualifier,
    outreach_specialist,
    sales_strategist,
    technical_consultant,
    web_scraper,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

sales_team = Team(
    name="Sales & Lead Generation Team",
    role="Find, qualify, and engage potential leads with personalized outreach",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=8,
    members=[
        web_scraper,
        lead_generator,
        lead_qualifier,
        sales_strategist,
        outreach_specialist,
        technical_consultant,
        crm_manager,
    ],
    db=db,
    instructions=[
        "You are the Sales Team Orchestrator.",
        "Run the sales pipeline iteratively:",
        "1. Web Scraper collects prospect data from target sources.",
        "2. Lead Generator identifies and enriches high-potential companies.",
        "3. Lead Qualifier scores and prioritizes leads using BANT.",
        "4. Sales Strategist designs the approach for each segment.",
        "5. Outreach Specialist drafts personalized messages and sequences.",
        "6. Technical Consultant prepares for technical questions.",
        "7. CRM Manager tracks all activities, pipeline, and next steps.",
        "",
        "Output: qualified lead list + outreach sequences + pipeline report.",
        "Focus on quality over quantity - personalization is key.",
        "",
        "INTER-TEAM AWARENESS:",
        "- Use market data from the Competitors Team to identify opportunities and",
        "  understand prospect pain points relative to competitor offerings.",
        "- Coordinate ad campaigns with the Ads Expert Team for lead generation funnels.",
        "- Request the Copywriting Team for personalized outreach copy that matches brand voice.",
        "- Leverage the Web/Blog Team for landing pages and lead magnets.",
        "- Share lead insights with the Community Team for nurturing through engagement.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
