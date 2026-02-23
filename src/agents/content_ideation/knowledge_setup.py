"""Knowledge bases for each Content Ideation sub-agent."""

from src.knowledge.factory import create_agent_knowledge

format_knowledge = create_agent_knowledge("ideation-format")
hook_knowledge = create_agent_knowledge("ideation-hook")
trend_adapter_knowledge = create_agent_knowledge("ideation-trend-adapter")
calendar_knowledge = create_agent_knowledge("ideation-calendar")
tone_optimizer_knowledge = create_agent_knowledge("ideation-tone-optimizer")
viral_scorer_knowledge = create_agent_knowledge("ideation-viral-scorer")
