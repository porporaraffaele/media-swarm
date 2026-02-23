"""Knowledge bases for each Content Finder sub-agent."""

from src.knowledge.factory import create_agent_knowledge

social_scout_knowledge = create_agent_knowledge("finder-social-scout")
web_scout_knowledge = create_agent_knowledge("finder-web-scout")
niche_scout_knowledge = create_agent_knowledge("finder-niche-scout")
relevance_analyzer_knowledge = create_agent_knowledge("finder-relevance")
rights_knowledge = create_agent_knowledge("finder-rights")
trend_correlation_knowledge = create_agent_knowledge("finder-trend-correlation")
