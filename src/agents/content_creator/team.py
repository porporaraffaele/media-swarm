"""Content Creator Team assembly (visual content generation)."""

from agno.team import Team, TeamMode

from src.agents.content_creator.agents import (
    format_optimizer,
    image_generator,
    post_production_editor,
    prompt_crafter,
    quality_reviewer,
    video_generator,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

content_creator_team = Team(
    name="Content Creator Team",
    role="Generate visual content: images and videos with AI models",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=6,
    members=[
        prompt_crafter,
        image_generator,
        video_generator,
        quality_reviewer,
        format_optimizer,
        post_production_editor,
    ],
    db=db,
    instructions=[
        "You are the Content Creator Team Orchestrator.",
        "Run the content creation pipeline sequentially:",
        "1. Prompt Crafter transforms the brief into optimized generation prompts.",
        "2. Image Generator or Video Generator creates the visual content.",
        "3. Quality Reviewer evaluates the output quality.",
        "4. If quality < 7/10, regenerate with revised prompts.",
        "5. Format Optimizer creates platform-specific variants.",
        "6. Post-Production Editor adds final touches and brand elements.",
        "Always report which models were used and any fallbacks triggered.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
