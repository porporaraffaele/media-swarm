"""Knowledge bases for each Branding sub-agent."""

from src.knowledge.factory import create_agent_knowledge

strategist_knowledge = create_agent_knowledge("branding-strategist")
visual_identity_knowledge = create_agent_knowledge("branding-visual-identity")
tone_knowledge = create_agent_knowledge("branding-tone-of-voice")
storyteller_knowledge = create_agent_knowledge("branding-storyteller")
auditor_knowledge = create_agent_knowledge("branding-auditor")
naming_knowledge = create_agent_knowledge("branding-naming")
positioning_knowledge = create_agent_knowledge("branding-positioning")
cultural_knowledge = create_agent_knowledge("branding-cultural-sensitivity")
