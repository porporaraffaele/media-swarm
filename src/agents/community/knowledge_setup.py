"""Knowledge bases for each Community Builder sub-agent."""

from src.knowledge.factory import create_agent_knowledge

engagement_knowledge = create_agent_knowledge("community-engagement")
responder_knowledge = create_agent_knowledge("community-responder")
ugc_knowledge = create_agent_knowledge("community-ugc")
growth_knowledge = create_agent_knowledge("community-growth")
community_analytics_knowledge = create_agent_knowledge("community-analytics")
crisis_knowledge = create_agent_knowledge("community-crisis")
influencer_knowledge = create_agent_knowledge("community-influencer")
events_knowledge = create_agent_knowledge("community-events")
ambassador_knowledge = create_agent_knowledge("community-ambassador")
