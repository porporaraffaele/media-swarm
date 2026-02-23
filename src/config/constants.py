"""Team and agent IDs, knowledge base table names, and other constants."""

# ─── Team IDs ───────────────────────────────────────────────────────────────

TEAM_BRANDING = "branding"
TEAM_COPYWRITING = "copywriting"
TEAM_GRAPHIC_DESIGN = "graphic-design"
TEAM_COMPETITORS = "competitors"
TEAM_NEWS = "news"
TEAM_COMMUNITY = "community"
TEAM_CONTENT_IDEATION = "content-ideation"
TEAM_CONTENT_FINDER = "content-finder"
TEAM_CONTENT_CREATOR = "content-creator"
TEAM_MASTER_ORCHESTRATOR = "master-orchestrator"
TEAM_ANALYST = "analyst"

ALL_TEAM_IDS = [
    TEAM_BRANDING,
    TEAM_COPYWRITING,
    TEAM_GRAPHIC_DESIGN,
    TEAM_COMPETITORS,
    TEAM_NEWS,
    TEAM_COMMUNITY,
    TEAM_CONTENT_IDEATION,
    TEAM_CONTENT_FINDER,
    TEAM_CONTENT_CREATOR,
    TEAM_MASTER_ORCHESTRATOR,
    TEAM_ANALYST,
]

# ─── Knowledge Base Table Names (one per sub-agent) ─────────────────────────

KB_TABLES = {
    # Branding
    "branding-strategist": "kb_branding_strategist",
    "branding-visual-identity": "kb_branding_visual_identity",
    "branding-tone-of-voice": "kb_branding_tone_of_voice",
    "branding-storyteller": "kb_branding_storyteller",
    "branding-auditor": "kb_branding_auditor",
    "branding-naming": "kb_branding_naming",
    "branding-positioning": "kb_branding_positioning",
    "branding-cultural-sensitivity": "kb_branding_cultural_sensitivity",
    # Copywriting
    "copywriting-seo": "kb_copywriting_seo",
    "copywriting-social-media": "kb_copywriting_social_media",
    "copywriting-email": "kb_copywriting_email",
    "copywriting-ad-copy": "kb_copywriting_ad_copy",
    "copywriting-script": "kb_copywriting_script",
    "copywriting-ux": "kb_copywriting_ux",
    "copywriting-proofreader": "kb_copywriting_proofreader",
    # Graphic Design
    "design-social-media": "kb_design_social_media",
    "design-template": "kb_design_template",
    "design-infographic": "kb_design_infographic",
    "design-thumbnail": "kb_design_thumbnail",
    "design-motion": "kb_design_motion",
    "design-photo-editor": "kb_design_photo_editor",
    # Competitors & Market
    "competitors-intelligence": "kb_competitors_intelligence",
    "competitors-trends": "kb_competitors_trends",
    "competitors-swot": "kb_competitors_swot",
    "competitors-pricing": "kb_competitors_pricing",
    "competitors-benchmarker": "kb_competitors_benchmarker",
    "competitors-segmentation": "kb_competitors_segmentation",
    # News
    "news-aggregator": "kb_news_aggregator",
    "news-trend-detector": "kb_news_trend_detector",
    "news-fact-checker": "kb_news_fact_checker",
    "news-summarizer": "kb_news_summarizer",
    "news-relevance": "kb_news_relevance",
    "news-alert": "kb_news_alert",
    # Community
    "community-engagement": "kb_community_engagement",
    "community-responder": "kb_community_responder",
    "community-ugc": "kb_community_ugc",
    "community-growth": "kb_community_growth",
    "community-analytics": "kb_community_analytics",
    "community-crisis": "kb_community_crisis",
    "community-influencer": "kb_community_influencer",
    "community-events": "kb_community_events",
    "community-ambassador": "kb_community_ambassador",
    # Content Ideation
    "ideation-format": "kb_ideation_format",
    "ideation-hook": "kb_ideation_hook",
    "ideation-trend-adapter": "kb_ideation_trend_adapter",
    "ideation-calendar": "kb_ideation_calendar",
    "ideation-tone-optimizer": "kb_ideation_tone_optimizer",
    "ideation-viral-scorer": "kb_ideation_viral_scorer",
    # Content Finder
    "finder-social-scout": "kb_finder_social_scout",
    "finder-web-scout": "kb_finder_web_scout",
    "finder-niche-scout": "kb_finder_niche_scout",
    "finder-relevance": "kb_finder_relevance",
    "finder-rights": "kb_finder_rights",
    "finder-trend-correlation": "kb_finder_trend_correlation",
    # Content Creator
    "creator-image-gen": "kb_creator_image_gen",
    "creator-video-gen": "kb_creator_video_gen",
    "creator-prompt-crafter": "kb_creator_prompt_crafter",
    "creator-quality-reviewer": "kb_creator_quality_reviewer",
    "creator-format-optimizer": "kb_creator_format_optimizer",
    "creator-post-production": "kb_creator_post_production",
    # Master Orchestrator
    "orchestrator-decomposer": "kb_orchestrator_decomposer",
    "orchestrator-assembler": "kb_orchestrator_assembler",
    "orchestrator-workflow": "kb_orchestrator_workflow",
    "orchestrator-cost": "kb_orchestrator_cost",
    "orchestrator-progress": "kb_orchestrator_progress",
    # Analyst
    "analyst-performance": "kb_analyst_performance",
    "analyst-quality": "kb_analyst_quality",
    "analyst-pattern": "kb_analyst_pattern",
    "analyst-ab-testing": "kb_analyst_ab_testing",
    "analyst-benchmark": "kb_analyst_benchmark",
    "analyst-learning-loop": "kb_analyst_learning_loop",
    "analyst-report-aggregator": "kb_analyst_report_aggregator",
    "analyst-rag-improvement": "kb_analyst_rag_improvement",
}


def get_kb_table(agent_id: str) -> str:
    """Get the knowledge base table name for a given agent ID."""
    if agent_id not in KB_TABLES:
        raise ValueError(f"Unknown agent ID: {agent_id}. Valid IDs: {list(KB_TABLES.keys())}")
    return KB_TABLES[agent_id]
