"""Knowledge bases for each Copywriting sub-agent."""

from src.knowledge.factory import create_agent_knowledge

seo_knowledge = create_agent_knowledge("copywriting-seo")
social_media_knowledge = create_agent_knowledge("copywriting-social-media")
email_knowledge = create_agent_knowledge("copywriting-email")
ad_copy_knowledge = create_agent_knowledge("copywriting-ad-copy")
script_knowledge = create_agent_knowledge("copywriting-script")
ux_knowledge = create_agent_knowledge("copywriting-ux")
proofreader_knowledge = create_agent_knowledge("copywriting-proofreader")
