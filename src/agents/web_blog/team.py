"""Web/Blog Management Team assembly."""

from agno.team import Team, TeamMode

from src.agents.web_blog.agents import (
    blog_content_writer,
    cms_manager,
    content_calendar_manager,
    email_marketing_specialist,
    landing_page_specialist,
    seo_technical_specialist,
    site_performance_monitor,
    web_analytics_specialist,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

web_blog_team = Team(
    name="Web/Blog Management Team",
    role="Manage the company website, blog content, SEO, email marketing, and web analytics",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=8,
    members=[
        seo_technical_specialist,
        blog_content_writer,
        landing_page_specialist,
        cms_manager,
        web_analytics_specialist,
        email_marketing_specialist,
        site_performance_monitor,
        content_calendar_manager,
    ],
    db=db,
    instructions=[
        "You are the Web/Blog Management Team Orchestrator.",
        "Coordinate the web and content workflow:",
        "1. SEO Technical Specialist audits and optimizes the site structure.",
        "2. Blog Content Writer creates SEO-optimized articles and posts.",
        "3. Landing Page Specialist designs high-converting campaign pages.",
        "4. CMS Manager handles publishing workflows and site organization.",
        "5. Web Analytics Specialist tracks performance and generates insights.",
        "6. Email Marketing Specialist designs campaigns and automation flows.",
        "7. Site Performance Monitor ensures speed and Core Web Vitals health.",
        "8. Content Calendar Manager plans the editorial schedule.",
        "",
        "Output: actionable web strategy with content, SEO, and performance plans.",
        "Focus on data-driven decisions and measurable outcomes.",
        "",
        "INTER-TEAM AWARENESS:",
        "- All blog content MUST follow the Branding Team's tone of voice and visual identity.",
        "- Use the editorial calendar from Content Ideation for publishing schedules.",
        "- Request article copy from the Copywriting Team's SEO Copywriter.",
        "- Use visual assets from the Content Creator Team and Graphic Design Team.",
        "- Coordinate landing pages with the Ads Expert Team for campaign alignment.",
        "- Share web analytics insights with the Analyst Team for optimization.",
        "- Collaborate with the Sales Team for lead magnet and conversion pages.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
