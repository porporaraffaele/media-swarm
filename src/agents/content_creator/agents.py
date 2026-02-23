"""Content Creator team sub-agents (visual content generation)."""

from src.agents.base import create_agent
from src.agents.content_creator.knowledge_setup import (
    format_optimizer_knowledge,
    image_gen_knowledge,
    post_production_knowledge,
    prompt_crafter_knowledge,
    quality_reviewer_knowledge,
    video_gen_knowledge,
)
from src.config.constants import TEAM_CONTENT_CREATOR
from src.tools.visual.flux import FluxTools
from src.tools.visual.nano_banana import NanoBananaTools
from src.tools.visual.runway import RunwayTools
from src.tools.visual.seedance import SeedanceTools

image_generator = create_agent(
    agent_id="creator-image-gen",
    name="Image Generator",
    role="Generate images using Nano Banana (primary) and Flux (fallback)",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=image_gen_knowledge,
    tools=[NanoBananaTools(), FluxTools()],
    instructions=[
        "You are an expert Image Generator.",
        "Generate images using available AI image generation tools.",
        "ALWAYS try nano_banana_tools first (primary model).",
        "If Nano Banana fails, use flux_tools as fallback.",
        "Craft detailed prompts: subject, style, composition, lighting, mood, colors.",
        "Generate at the correct dimensions for the target platform.",
        "Report which model was used and whether a fallback was needed.",
    ],
)

video_generator = create_agent(
    agent_id="creator-video-gen",
    name="Video Generator",
    role="Generate videos using Seedance 2.0 (primary) and Runway (fallback)",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=video_gen_knowledge,
    tools=[SeedanceTools(), RunwayTools()],
    instructions=[
        "You are an expert Video Generator.",
        "Generate videos using available AI video generation tools.",
        "ALWAYS try seedance_tools first (primary model).",
        "If Seedance fails, use runway_tools as fallback.",
        "Craft scene descriptions with: action, camera movement, lighting, mood.",
        "Specify duration, aspect ratio, and resolution for the target platform.",
        "For async generation, poll status until complete.",
        "Report which model was used and generation time.",
    ],
)

prompt_crafter = create_agent(
    agent_id="creator-prompt-crafter",
    name="Prompt Crafter",
    role="Craft optimized prompts for AI image and video generation models",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=prompt_crafter_knowledge,
    instructions=[
        "You are an expert AI Prompt Crafter for visual content generation.",
        "Transform content briefs into detailed generation prompts.",
        "For images include: subject, style, composition, lighting, color palette,",
        "  mood, perspective, background, texture, level of detail.",
        "For videos include: scene description, camera movement, action sequence,",
        "  transitions, timing, audio mood, pacing.",
        "Optimize prompts for each specific model's strengths.",
        "Provide 3 prompt variants from different creative angles.",
    ],
)

quality_reviewer = create_agent(
    agent_id="creator-quality-reviewer",
    name="Quality Reviewer",
    role="Review quality of generated visual content",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=quality_reviewer_knowledge,
    instructions=[
        "You are an expert Visual Content Quality Reviewer.",
        "Evaluate generated images and videos on quality criteria:",
        "  Technical: resolution, artifacts, consistency, clarity.",
        "  Creative: composition, color harmony, visual impact.",
        "  Brand: alignment with brand guidelines, tone, audience.",
        "Score quality on a 1-10 scale per dimension.",
        "Recommend: approve, revise prompt, regenerate, or switch model.",
    ],
    use_haiku=True,
)

format_optimizer = create_agent(
    agent_id="creator-format-optimizer",
    name="Format Optimizer",
    role="Optimize content formats and dimensions for each target platform",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=format_optimizer_knowledge,
    instructions=[
        "You are an expert Format Optimizer.",
        "Adapt generated content to platform-specific requirements:",
        "  Instagram Feed: 1080x1080, Story/Reel: 1080x1920",
        "  TikTok: 1080x1920, YouTube Thumb: 1280x720, Short: 1080x1920",
        "  LinkedIn: 1200x627, X: 1600x900, Pinterest: 1000x1500",
        "Specify cropping, padding, and safe zones for text overlays.",
        "Create platform variant specs from a single source asset.",
    ],
    use_haiku=True,
)

post_production_editor = create_agent(
    agent_id="creator-post-production",
    name="Post-Production Editor",
    role="Direct post-production editing and enhancement of visual content",
    team_id=TEAM_CONTENT_CREATOR,
    knowledge=post_production_knowledge,
    instructions=[
        "You are an expert Post-Production Editor.",
        "Direct post-production enhancements: color grading, cropping, overlays.",
        "Specify text overlay placement, font, size, and animation.",
        "Add branded elements: logos, watermarks, lower thirds.",
        "Create editing briefs for video: cuts, transitions, music sync.",
        "Ensure final output meets platform technical specifications.",
    ],
)
