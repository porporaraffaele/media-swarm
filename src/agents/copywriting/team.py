"""Copywriting Team assembly."""

from agno.team import Team, TeamMode

from src.agents.copywriting.agents import (
    ad_copy_specialist,
    email_writer,
    proofreader,
    script_writer,
    seo_copywriter,
    social_media_copywriter,
    ux_writer,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

copywriting_team = Team(
    name="Copywriting Team",
    role="Write all types of copy: SEO articles, social media, emails, ads, scripts, UX",
    model=get_claude_sonnet(),
    mode=TeamMode.coordinate,
    members=[
        seo_copywriter,
        social_media_copywriter,
        email_writer,
        ad_copy_specialist,
        script_writer,
        ux_writer,
        proofreader,
    ],
    db=db,
    instructions=[
        "You are the Copywriting Team Orchestrator.",
        "Route writing requests to the appropriate specialist copywriter.",
        "For multi-platform content, involve multiple writers.",
        "Always send final copy to the Proofreader for quality check.",
        "Ensure all output aligns with brand voice guidelines.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
