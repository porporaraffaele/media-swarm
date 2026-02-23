"""Knowledge bases for each Graphic Design sub-agent."""

from src.knowledge.factory import create_agent_knowledge

social_media_design_knowledge = create_agent_knowledge("design-social-media")
template_knowledge = create_agent_knowledge("design-template")
infographic_knowledge = create_agent_knowledge("design-infographic")
thumbnail_knowledge = create_agent_knowledge("design-thumbnail")
motion_knowledge = create_agent_knowledge("design-motion")
photo_editor_knowledge = create_agent_knowledge("design-photo-editor")
