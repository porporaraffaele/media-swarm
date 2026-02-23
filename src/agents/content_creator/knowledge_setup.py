"""Knowledge bases for each Content Creator sub-agent."""

from src.knowledge.factory import create_agent_knowledge

image_gen_knowledge = create_agent_knowledge("creator-image-gen")
video_gen_knowledge = create_agent_knowledge("creator-video-gen")
prompt_crafter_knowledge = create_agent_knowledge("creator-prompt-crafter")
quality_reviewer_knowledge = create_agent_knowledge("creator-quality-reviewer")
format_optimizer_knowledge = create_agent_knowledge("creator-format-optimizer")
post_production_knowledge = create_agent_knowledge("creator-post-production")
