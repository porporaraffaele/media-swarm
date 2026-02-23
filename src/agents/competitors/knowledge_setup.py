"""Knowledge bases for each Competitors & Market sub-agent."""

from src.knowledge.factory import create_agent_knowledge

intelligence_knowledge = create_agent_knowledge("competitors-intelligence")
trends_knowledge = create_agent_knowledge("competitors-trends")
swot_knowledge = create_agent_knowledge("competitors-swot")
pricing_knowledge = create_agent_knowledge("competitors-pricing")
benchmarker_knowledge = create_agent_knowledge("competitors-benchmarker")
segmentation_knowledge = create_agent_knowledge("competitors-segmentation")
