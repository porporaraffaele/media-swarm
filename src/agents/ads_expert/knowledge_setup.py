"""Knowledge bases for Ads Expert team agents."""

from src.knowledge.factory import create_agent_knowledge

fb_instagram_knowledge = create_agent_knowledge("ads-fb-instagram")
google_ads_knowledge = create_agent_knowledge("ads-google")
tiktok_ads_knowledge = create_agent_knowledge("ads-tiktok")
linkedin_ads_knowledge = create_agent_knowledge("ads-linkedin")
youtube_ads_knowledge = create_agent_knowledge("ads-youtube")
ad_creative_knowledge = create_agent_knowledge("ads-creative")
ab_optimization_knowledge = create_agent_knowledge("ads-ab-optimization")
budget_roi_knowledge = create_agent_knowledge("ads-budget-roi")
