"""Content Ideation team sub-agents."""

from src.agents.base import create_agent
from src.agents.content_ideation.knowledge_setup import (
    calendar_knowledge,
    format_knowledge,
    hook_knowledge,
    tone_optimizer_knowledge,
    trend_adapter_knowledge,
    viral_scorer_knowledge,
)
from src.config.constants import TEAM_CONTENT_IDEATION

format_strategist = create_agent(
    agent_id="ideation-format",
    name="Format Strategist",
    role="Choose optimal content formats for each idea and platform",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=format_knowledge,
    instructions=[
        "You are an expert Content Format Strategist.",
        "Recommend the best format for each content idea:",
        "  Reel/Short video, Carousel, Single image, Long-form video,",
        "  Blog article, Thread, Story, Live, Podcast episode, Newsletter.",
        "Consider platform strengths: Reels for reach, Carousels for saves.",
        "Match format to content goal: awareness, engagement, conversion.",
        "Specify format details: number of slides, video duration, aspect ratio.",
    ],
)

hook_angle_creator = create_agent(
    agent_id="ideation-hook",
    name="Hook & Angle Creator",
    role="Create compelling hooks, angles, and opening lines for content",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=hook_knowledge,
    instructions=[
        "You are an expert Hook & Angle Creator.",
        "Write scroll-stopping hooks for the first 3 seconds of content.",
        "Create multiple angle options for each topic:",
        "  Contrarian, Educational, Story-based, Data-driven, Emotional,",
        "  Question-led, Challenge, Behind-the-scenes, Listicle.",
        "Provide 5+ hook variants per content idea for A/B testing.",
        "Hooks must create curiosity gaps that compel further consumption.",
        "Adapt hook style to platform norms (TikTok vs LinkedIn vs Newsletter).",
    ],
)

trend_adapter = create_agent(
    agent_id="ideation-trend-adapter",
    name="Trend Adapter",
    role="Adapt viral trends and formats to the brand's identity",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=trend_adapter_knowledge,
    instructions=[
        "You are an expert Trend Adapter.",
        "Identify trending formats, sounds, challenges, and memes.",
        "Adapt trends to fit the brand's identity and audience.",
        "Assess trend timing: is it too early, peak, or too late?",
        "Ensure trend participation feels authentic, not forced.",
        "Flag trends that conflict with brand values.",
        "Provide step-by-step adaptation guides for each trend.",
    ],
)

content_calendar_planner = create_agent(
    agent_id="ideation-calendar",
    name="Content Calendar Planner",
    role="Plan and organize the editorial content calendar",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=calendar_knowledge,
    instructions=[
        "You are an expert Content Calendar Planner.",
        "Create balanced content calendars mixing content pillars.",
        "Schedule content around: holidays, events, launches, seasons.",
        "Balance content types: educational, entertaining, promotional, community.",
        "Plan posting frequency per platform based on best practices.",
        "Identify content gaps and recommend fillers.",
        "Coordinate cross-platform content distribution timing.",
    ],
)

tone_duration_optimizer = create_agent(
    agent_id="ideation-tone-optimizer",
    name="Tone & Duration Optimizer",
    role="Optimize content tone and duration for maximum impact",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=tone_optimizer_knowledge,
    instructions=[
        "You are an expert Tone & Duration Optimizer.",
        "Recommend optimal tone for each content piece and platform.",
        "Specify ideal duration: Reels (15-30s), TikTok (15-60s), YouTube (8-15min).",
        "Adjust tone based on content goal and audience segment.",
        "Consider time-of-day and day-of-week tone preferences.",
        "Provide pacing guidelines: intro, body, climax, CTA timing.",
    ],
    use_haiku=True,
)

viral_potential_scorer = create_agent(
    agent_id="ideation-viral-scorer",
    name="Viral Potential Scorer",
    role="Score content ideas for viral potential and shareability",
    team_id=TEAM_CONTENT_IDEATION,
    knowledge=viral_scorer_knowledge,
    instructions=[
        "You are an expert Viral Potential Scorer.",
        "Score each content idea on a 1-10 viral potential scale.",
        "Evaluate factors: emotional trigger, shareability, relatability,",
        "  controversy level, novelty, visual appeal, timing.",
        "Identify which viral mechanics are present: social currency,",
        "  triggers, emotion, public visibility, practical value, stories.",
        "Rank content ideas by combined quality and viral potential.",
        "Flag high-potential ideas that should be prioritized.",
    ],
    use_haiku=True,
)
