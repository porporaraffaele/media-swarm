"""Knowledge base setup for Web/Blog Management Team agents."""

from src.knowledge.factory import create_agent_knowledge

seo_technical_knowledge = create_agent_knowledge("web-seo-technical")
blog_writer_knowledge = create_agent_knowledge("web-blog-writer")
landing_page_knowledge = create_agent_knowledge("web-landing-page")
cms_manager_knowledge = create_agent_knowledge("web-cms-manager")
web_analytics_knowledge = create_agent_knowledge("web-analytics")
email_marketing_knowledge = create_agent_knowledge("web-email-marketing")
site_performance_knowledge = create_agent_knowledge("web-site-performance")
content_calendar_knowledge = create_agent_knowledge("web-content-calendar")
