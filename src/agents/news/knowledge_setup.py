"""Knowledge bases for each News sub-agent."""

from src.knowledge.factory import create_agent_knowledge

aggregator_knowledge = create_agent_knowledge("news-aggregator")
trend_detector_knowledge = create_agent_knowledge("news-trend-detector")
fact_checker_knowledge = create_agent_knowledge("news-fact-checker")
summarizer_knowledge = create_agent_knowledge("news-summarizer")
relevance_knowledge = create_agent_knowledge("news-relevance")
alert_knowledge = create_agent_knowledge("news-alert")
