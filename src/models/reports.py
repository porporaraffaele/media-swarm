"""Pydantic report models for every micro-task across all agent teams.

Every sub-agent produces a structured report after each task. These reports are:
1. Returned as structured output (output_model on the agent)
2. Saved to the `reports` PostgreSQL table via ReportTools
3. Analyzed by the Analyst team for continuous improvement
"""

from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ReportStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


# ─── Base Report ────────────────────────────────────────────────────────────


class BaseReport(BaseModel):
    """Base report model - all micro-task reports inherit from this."""

    report_id: UUID = Field(default_factory=uuid4)
    team_id: str
    agent_id: str
    task_type: str
    task_description: str
    status: ReportStatus = ReportStatus.SUCCESS
    quality_score: float = Field(
        default=7.0, ge=0.0, le=10.0, description="Self-assessed quality 0-10"
    )
    tokens_used: int = 0
    cost_usd: float = 0.0
    execution_time_seconds: float = 0.0
    errors: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ─── Team 1: Branding ──────────────────────────────────────────────────────


class BrandingReport(BaseReport):
    """Report from branding sub-agents."""

    brand_elements: list[str] = Field(default_factory=list)
    target_audience: str = ""
    competitive_positioning: str = ""
    key_messages: list[str] = Field(default_factory=list)
    visual_direction: str = ""
    tone_guidelines: str = ""
    naming_options: list[str] = Field(default_factory=list)
    cultural_notes: list[str] = Field(default_factory=list)


# ─── Team 2: Copywriting ───────────────────────────────────────────────────


class CopywritingReport(BaseReport):
    """Report from copywriting sub-agents."""

    content_type: str = ""  # social_post, email, ad_copy, script, seo_article, ux_copy
    word_count: int = 0
    seo_keywords: list[str] = Field(default_factory=list)
    readability_score: float = 0.0
    cta_included: bool = False
    platform: str = ""  # instagram, linkedin, twitter, newsletter, website
    content_draft: str = ""


# ─── Team 3: Graphic Design ────────────────────────────────────────────────


class DesignReport(BaseReport):
    """Report from graphic design sub-agents."""

    asset_type: str = ""  # social_graphic, infographic, thumbnail, template, motion
    dimensions: str = ""  # 1080x1080, 1920x1080, etc.
    file_format: str = ""  # png, jpg, mp4, gif
    generation_model: str = ""  # nano_banana, flux
    prompt_used: str = ""
    output_url: str = ""
    revision_notes: list[str] = Field(default_factory=list)


# ─── Team 4: Competitors & Market ──────────────────────────────────────────


class CompetitorReport(BaseReport):
    """Report from competitors & market analysis sub-agents."""

    competitors_analyzed: list[str] = Field(default_factory=list)
    market_trends: list[str] = Field(default_factory=list)
    swot_summary: dict = Field(default_factory=dict)
    opportunities: list[str] = Field(default_factory=list)
    threats: list[str] = Field(default_factory=list)
    pricing_insights: list[str] = Field(default_factory=list)
    audience_segments: list[dict] = Field(default_factory=list)


# ─── Team 5: News ──────────────────────────────────────────────────────────


class NewsReport(BaseReport):
    """Report from news agent sub-agents."""

    sources_checked: int = 0
    articles_found: int = 0
    trending_topics: list[str] = Field(default_factory=list)
    relevance_scores: dict[str, float] = Field(default_factory=dict)
    fact_check_results: list[dict] = Field(default_factory=list)
    alerts_triggered: list[str] = Field(default_factory=list)
    summary: str = ""


# ─── Team 6: Community ─────────────────────────────────────────────────────


class CommunityReport(BaseReport):
    """Report from community builder sub-agents."""

    engagement_metrics: dict = Field(default_factory=dict)
    responses_drafted: int = 0
    growth_suggestions: list[str] = Field(default_factory=list)
    sentiment_score: float = 0.0
    crisis_alerts: list[str] = Field(default_factory=list)
    influencer_leads: list[dict] = Field(default_factory=list)
    event_ideas: list[str] = Field(default_factory=list)
    ugc_highlights: list[str] = Field(default_factory=list)


# ─── Team 7: Content Ideation ──────────────────────────────────────────────


class ContentIdeationReport(BaseReport):
    """Report from content ideation sub-agents."""

    ideas_generated: int = 0
    content_ideas: list[dict] = Field(default_factory=list)
    # Each idea: {title, format, hook, angle, tone, duration, platform, score}
    calendar_entries: list[dict] = Field(default_factory=list)
    viral_potential_scores: list[float] = Field(default_factory=list)
    recommended_formats: list[str] = Field(default_factory=list)


# ─── Team 8: Content Finder ────────────────────────────────────────────────


class ContentFinderReport(BaseReport):
    """Report from content finder sub-agents."""

    platforms_searched: list[str] = Field(default_factory=list)
    content_found: int = 0
    top_results: list[dict] = Field(default_factory=list)
    # Each result: {url, platform, title, relevance_score, license_status}
    license_status: dict[str, str] = Field(default_factory=dict)
    trend_correlations: list[str] = Field(default_factory=list)


# ─── Team 9: Content Creator ───────────────────────────────────────────────


class ContentCreatorReport(BaseReport):
    """Report from content creator sub-agents."""

    content_type: str = ""  # image, video
    generation_model: str = ""  # nano_banana, seedance, flux, runway
    prompt_used: str = ""
    output_url: str = ""
    platform_variants: list[dict] = Field(default_factory=list)
    # Each variant: {platform, dimensions, format, url}
    quality_assessment: str = ""
    fallback_used: bool = False


# ─── Team 10: Master Orchestrator ──────────────────────────────────────────


class OrchestratorReport(BaseReport):
    """Report from the master orchestrator."""

    sub_tasks_created: int = 0
    teams_involved: list[str] = Field(default_factory=list)
    total_cost_usd: float = 0.0
    total_tokens: int = 0
    sub_report_ids: list[UUID] = Field(default_factory=list)
    workflow_summary: str = ""


# ─── Team 11: Analyst ──────────────────────────────────────────────────────


class AnalystReport(BaseReport):
    """Report from the analyst team."""

    reports_analyzed: int = 0
    time_period: str = ""  # e.g. "last_24h", "last_7d"
    patterns_found: list[str] = Field(default_factory=list)
    improvement_suggestions: list[dict] = Field(default_factory=list)
    # Each suggestion: {target_team, target_agent, type, description, priority}
    performance_trends: dict = Field(default_factory=dict)
    ab_test_results: list[dict] = Field(default_factory=list)
    cost_analysis: dict = Field(default_factory=dict)
    knowledge_gaps: list[dict] = Field(default_factory=list)
