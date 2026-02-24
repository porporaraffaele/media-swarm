"""Knowledge bases for Sales & Lead Generation team agents."""

from src.knowledge.factory import create_agent_knowledge

web_scraper_knowledge = create_agent_knowledge("sales-web-scraper")
lead_generator_knowledge = create_agent_knowledge("sales-lead-generator")
lead_qualifier_knowledge = create_agent_knowledge("sales-lead-qualifier")
outreach_knowledge = create_agent_knowledge("sales-outreach-specialist")
strategist_knowledge = create_agent_knowledge("sales-strategist")
technical_consultant_knowledge = create_agent_knowledge("sales-technical-consultant")
crm_manager_knowledge = create_agent_knowledge("sales-crm-manager")
