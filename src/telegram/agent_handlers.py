"""Telegram handlers for individual agent access and report monitoring.

Commands:
- /agent <agent_id> <message>  — Esegui un singolo agente
- /agents  — Lista tutti gli agenti per team
- /agent_info <agent_id>  — Info su un agente
- /reports <agent_id>  — Ultimi report di un agente
- /reports_team <team_key>  — Ultimi report di un team
"""

import importlib
import logging

from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.config.constants import ALL_TEAM_IDS
from src.config.settings import settings
from telegram import Update

logger = logging.getLogger(__name__)

# Registry: agent_id → "module.path:variable_name"
AGENT_REGISTRY: dict[str, str] = {
    # Branding
    "branding-strategist": "src.agents.branding.agents:brand_strategist",
    "branding-visual-identity": "src.agents.branding.agents:visual_identity_designer",
    "branding-tone-of-voice": "src.agents.branding.agents:tone_of_voice_specialist",
    "branding-storyteller": "src.agents.branding.agents:brand_storyteller",
    "branding-auditor": "src.agents.branding.agents:brand_auditor",
    "branding-naming": "src.agents.branding.agents:naming_specialist",
    "branding-positioning": "src.agents.branding.agents:brand_positioning_analyst",
    "branding-cultural-sensitivity": "src.agents.branding.agents:cultural_sensitivity_reviewer",
    # Copywriting
    "copywriting-seo": "src.agents.copywriting.agents:seo_copywriter",
    "copywriting-social-media": "src.agents.copywriting.agents:social_media_copywriter",
    "copywriting-email": "src.agents.copywriting.agents:email_writer",
    "copywriting-ad-copy": "src.agents.copywriting.agents:ad_copy_specialist",
    "copywriting-script": "src.agents.copywriting.agents:script_writer",
    "copywriting-ux": "src.agents.copywriting.agents:ux_writer",
    "copywriting-proofreader": "src.agents.copywriting.agents:proofreader",
    # Graphic Design
    "design-social-media": "src.agents.graphic_design.agents:social_media_graphics_creator",
    "design-template": "src.agents.graphic_design.agents:brand_template_designer",
    "design-infographic": "src.agents.graphic_design.agents:infographic_creator",
    "design-thumbnail": "src.agents.graphic_design.agents:thumbnail_cover_designer",
    "design-motion": "src.agents.graphic_design.agents:motion_graphics_director",
    "design-photo-editor": "src.agents.graphic_design.agents:photo_editor",
    # Competitors & Market
    "competitors-intelligence": "src.agents.competitors.agents:competitive_intelligence_analyst",
    "competitors-trends": "src.agents.competitors.agents:market_trend_researcher",
    "competitors-swot": "src.agents.competitors.agents:swot_analyst",
    "competitors-pricing": "src.agents.competitors.agents:pricing_strategist",
    "competitors-benchmarker": "src.agents.competitors.agents:industry_benchmarker",
    "competitors-segmentation": "src.agents.competitors.agents:audience_segmentation_analyst",
    # News
    "news-aggregator": "src.agents.news.agents:news_aggregator",
    "news-trend-detector": "src.agents.news.agents:trend_detector",
    "news-fact-checker": "src.agents.news.agents:fact_checker",
    "news-summarizer": "src.agents.news.agents:news_summarizer",
    "news-relevance": "src.agents.news.agents:relevance_scorer",
    "news-alert": "src.agents.news.agents:alert_manager",
    # Community
    "community-engagement": "src.agents.community.agents:engagement_strategist",
    "community-responder": "src.agents.community.agents:comment_dm_responder",
    "community-ugc": "src.agents.community.agents:ugc_curator",
    "community-growth": "src.agents.community.agents:growth_hacker",
    "community-analytics": "src.agents.community.agents:community_analytics_agent",
    "community-crisis": "src.agents.community.agents:crisis_manager",
    "community-influencer": "src.agents.community.agents:influencer_outreach",
    "community-events": "src.agents.community.agents:event_coordinator",
    "community-ambassador": "src.agents.community.agents:ambassador_program_manager",
    # Content Ideation
    "ideation-format": "src.agents.content_ideation.agents:format_strategist",
    "ideation-hook": "src.agents.content_ideation.agents:hook_angle_creator",
    "ideation-trend-adapter": "src.agents.content_ideation.agents:trend_adapter",
    "ideation-calendar": "src.agents.content_ideation.agents:content_calendar_planner",
    "ideation-tone-optimizer": "src.agents.content_ideation.agents:tone_duration_optimizer",
    "ideation-viral-scorer": "src.agents.content_ideation.agents:viral_potential_scorer",
    # Content Finder
    "finder-social-scout": "src.agents.content_finder.agents:social_media_scout",
    "finder-web-scout": "src.agents.content_finder.agents:web_content_scout",
    "finder-niche-scout": "src.agents.content_finder.agents:niche_platform_scout",
    "finder-relevance": "src.agents.content_finder.agents:content_relevance_analyzer",
    "finder-rights": "src.agents.content_finder.agents:rights_license_checker",
    "finder-trend-correlation": "src.agents.content_finder.agents:trend_correlation_analyzer",
    # Content Creator
    "creator-image-gen": "src.agents.content_creator.agents:image_generator",
    "creator-video-gen": "src.agents.content_creator.agents:video_generator",
    "creator-prompt-crafter": "src.agents.content_creator.agents:prompt_crafter",
    "creator-quality-reviewer": "src.agents.content_creator.agents:quality_reviewer",
    "creator-format-optimizer": "src.agents.content_creator.agents:format_optimizer",
    "creator-post-production": "src.agents.content_creator.agents:post_production_editor",
    # Master Orchestrator
    "orchestrator-decomposer": "src.agents.master_orchestrator.agents:task_decomposer",
    "orchestrator-assembler": "src.agents.master_orchestrator.agents:output_assembler",
    "orchestrator-workflow": "src.agents.master_orchestrator.agents:workflow_optimizer",
    "orchestrator-cost": "src.agents.master_orchestrator.agents:cost_tracker",
    "orchestrator-progress": "src.agents.master_orchestrator.agents:progress_monitor",
    # Analyst
    "analyst-performance": "src.agents.analyst.agents:performance_analyst",
    "analyst-quality": "src.agents.analyst.agents:quality_auditor",
    "analyst-pattern": "src.agents.analyst.agents:pattern_recognition_engine",
    "analyst-ab-testing": "src.agents.analyst.agents:ab_testing_manager",
    "analyst-benchmark": "src.agents.analyst.agents:benchmark_comparator",
    "analyst-learning-loop": "src.agents.analyst.agents:learning_loop_manager",
    "analyst-report-aggregator": "src.agents.analyst.agents:report_aggregator",
    "analyst-rag-improvement": "src.agents.analyst.agents:rag_improvement_suggester",
    "analyst-production-monitor": "src.agents.analyst.agents:production_monitor",
    # Sales
    "sales-web-scraper": "src.agents.sales.agents:web_scraper",
    "sales-lead-generator": "src.agents.sales.agents:lead_generator",
    "sales-lead-qualifier": "src.agents.sales.agents:lead_qualifier",
    "sales-outreach-specialist": "src.agents.sales.agents:outreach_specialist",
    "sales-strategist": "src.agents.sales.agents:sales_strategist",
    "sales-technical-consultant": "src.agents.sales.agents:technical_consultant",
    "sales-crm-manager": "src.agents.sales.agents:crm_manager",
    # Ads Expert
    "ads-fb-instagram": "src.agents.ads_expert.agents:fb_instagram_specialist",
    "ads-google": "src.agents.ads_expert.agents:google_ads_specialist",
    "ads-tiktok": "src.agents.ads_expert.agents:tiktok_ads_specialist",
    "ads-linkedin": "src.agents.ads_expert.agents:linkedin_ads_specialist",
    "ads-youtube": "src.agents.ads_expert.agents:youtube_ads_specialist",
    "ads-creative": "src.agents.ads_expert.agents:ad_creative_specialist",
    "ads-ab-optimization": "src.agents.ads_expert.agents:ab_optimization_specialist",
    "ads-budget-roi": "src.agents.ads_expert.agents:budget_roi_analyst",
    # Web/Blog Management
    "web-seo-technical": "src.agents.web_blog.agents:seo_technical_specialist",
    "web-blog-writer": "src.agents.web_blog.agents:blog_content_writer",
    "web-landing-page": "src.agents.web_blog.agents:landing_page_specialist",
    "web-cms-manager": "src.agents.web_blog.agents:cms_manager",
    "web-analytics": "src.agents.web_blog.agents:web_analytics_specialist",
    "web-email-marketing": "src.agents.web_blog.agents:email_marketing_specialist",
    "web-site-performance": "src.agents.web_blog.agents:site_performance_monitor",
    "web-content-calendar": "src.agents.web_blog.agents:content_calendar_manager",
}

# Team display names
TEAM_NAMES: dict[str, str] = {
    "branding": "Branding",
    "copywriting": "Copywriting",
    "graphic-design": "Graphic Design",
    "competitors": "Competitors & Market",
    "news": "News",
    "community": "Community",
    "content-ideation": "Content Ideation",
    "content-finder": "Content Finder",
    "content-creator": "Content Creator",
    "master-orchestrator": "Master Orchestrator",
    "analyst": "Analyst",
    "sales": "Sales & Lead Gen",
    "ads-expert": "Ads Expert",
    "web-blog": "Web/Blog Management",
}


def _is_authorized(update: Update) -> bool:
    return str(update.effective_chat.id) == settings.telegram_chat_id


def _get_agent(agent_id: str):
    """Lazy-import and return an agent by its ID."""
    if agent_id not in AGENT_REGISTRY:
        return None
    module_path, attr_name = AGENT_REGISTRY[agent_id].rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def _extract_text(response) -> str:
    """Extract text from an Agno RunResponse."""
    if response is None:
        return "Nessuna risposta."
    if hasattr(response, "content"):
        return str(response.content)
    if hasattr(response, "messages") and response.messages:
        parts = [str(m.content) for m in response.messages if hasattr(m, "content") and m.content]
        return "\n\n".join(parts) if parts else str(response)
    return str(response)


async def _send_long(update: Update, text: str) -> None:
    """Send text, splitting if > 4096 chars."""
    max_len = 4096
    if len(text) <= max_len:
        try:
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text(text)
        return
    chunks, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line
        else:
            current = f"{current}\n{line}" if current else line
    if current:
        chunks.append(current)
    for chunk in chunks:
        try:
            await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text(chunk)


async def agent_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /agent <agent_id> <message> — run a single agent."""
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /agent `<agent_id>` `<messaggio>`\n"
            "Es: /agent news-aggregator Ultime news su AI\n\n"
            "Usa /agents per la lista degli agent\\_id.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    message = " ".join(context.args[1:])

    agent = _get_agent(agent_id)
    if agent is None:
        await update.message.reply_text(
            f"Agente '{agent_id}' non trovato. Usa /agents per la lista."
        )
        return

    await update.effective_chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text(
        f"Esecuzione agente *{agent.name}*...",
        parse_mode=ParseMode.MARKDOWN,
    )

    try:
        response = await agent.arun(input=message)
        result = _extract_text(response)
        await processing.delete()
        await _send_long(update, result)
    except Exception as e:
        logger.exception("Error running agent %s", agent_id)
        await processing.edit_text(f"Errore con agente {agent_id}: {e}")


async def agents_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /agents — list all agents grouped by team."""
    if not _is_authorized(update):
        return

    # Group agents by team
    teams: dict[str, list[str]] = {}
    for agent_id in sorted(AGENT_REGISTRY.keys()):
        # Extract team prefix
        parts = agent_id.split("-")
        team_prefix = parts[0]
        if team_prefix not in teams:
            teams[team_prefix] = []
        teams[team_prefix].append(agent_id)

    lines = ["*Tutti gli agenti (97):*\n"]
    for team_id in ALL_TEAM_IDS:
        display_name = TEAM_NAMES.get(team_id, team_id)
        # Find agents matching this team
        team_agents = [aid for aid in AGENT_REGISTRY if aid.startswith(team_id.split("-")[0])]
        if not team_agents:
            continue
        lines.append(f"\n*{display_name}* ({len(team_agents)}):")
        for aid in sorted(team_agents):
            lines.append(f"  `{aid}`")

    text = "\n".join(lines)
    await _send_long(update, text)


async def agent_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /agent_info <agent_id> — show agent details."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /agent\\_info `<agent_id>`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    agent = _get_agent(agent_id)
    if agent is None:
        await update.message.reply_text(f"Agente '{agent_id}' non trovato.")
        return

    # Count KB docs
    kb_count = 0
    try:
        from src.db.tables import get_connection

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) FROM knowledge_documents "
                    "WHERE agent_id = %s AND status != 'archived'",
                    (agent_id,),
                )
                row = cur.fetchone()
                kb_count = row[0] if row else 0
    except Exception:
        pass

    tools_list = ", ".join(t.name for t in agent.tools) if agent.tools else "Nessuno"

    text = (
        f"*Agente: {agent.name}*\n\n"
        f"ID: `{agent_id}`\n"
        f"Ruolo: {agent.role}\n"
        f"Tools: {tools_list}\n"
        f"Documenti RAG: {kb_count}\n"
        f"Modello: {getattr(agent.model, 'id', 'unknown')}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def reports_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reports <agent_id> — show recent agent reports."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /reports `<agent_id>`\nEs: /reports news-aggregator",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    if agent_id not in AGENT_REGISTRY:
        await update.message.reply_text(f"Agente '{agent_id}' non trovato.")
        return

    try:
        from src.db.tables import get_connection

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT task_type, quality_score, cost_usd,
                           execution_time_seconds, created_at, report_data
                    FROM reports
                    WHERE agent_id = %s
                    ORDER BY created_at DESC LIMIT 5
                    """,
                    (agent_id,),
                )
                rows = cur.fetchall()

        if not rows:
            await update.message.reply_text(
                f"Nessun report per *{agent_id}*.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        lines = [f"*Ultimi report di {agent_id}:*\n"]
        for row in rows:
            task_type, quality, cost, time_s, created, data = row
            date_str = created.strftime("%d/%m %H:%M") if created else "?"
            report_data = data if isinstance(data, dict) else {}
            approach = report_data.get("approach", "N/A")
            if len(approach) > 150:
                approach = approach[:150] + "..."
            lines.append(
                f"*{task_type}* — {date_str}\n"
                f"  Qualità: {quality}/10 | Costo: ${cost:.4f} | Tempo: {time_s:.1f}s\n"
                f"  Approccio: {approach}\n"
            )

        await _send_long(update, "\n".join(lines))
    except Exception as e:
        logger.exception("Failed to get reports for %s", agent_id)
        await update.message.reply_text(f"Errore: {e}")


async def reports_team_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /reports_team <team_id> — show recent reports for a team."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /reports\\_team `<team_id>`\n"
            "Es: /reports\\_team news\n\n"
            "Team: " + ", ".join(f"`{t}`" for t in ALL_TEAM_IDS),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    team_id = context.args[0]
    if team_id not in ALL_TEAM_IDS:
        await update.message.reply_text(f"Team '{team_id}' non trovato.")
        return

    try:
        from src.db.tables import get_connection

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT agent_id, task_type, quality_score, cost_usd, created_at,
                           report_data->'result_summary' as summary
                    FROM reports
                    WHERE team_id = %s
                    ORDER BY created_at DESC LIMIT 10
                    """,
                    (team_id,),
                )
                rows = cur.fetchall()

        if not rows:
            await update.message.reply_text(
                f"Nessun report per il team *{team_id}*.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        display_name = TEAM_NAMES.get(team_id, team_id)
        lines = [f"*Ultimi report del team {display_name}:*\n"]
        for row in rows:
            agent_id, task_type, quality, cost, created, summary = row
            date_str = created.strftime("%d/%m %H:%M") if created else "?"
            s = str(summary) if summary else "N/A"
            summary_text = s[:100] + "..." if len(s) > 100 else s
            lines.append(
                f"`{agent_id}` — *{task_type}* ({date_str})\n"
                f"  Q: {quality}/10 | ${cost:.4f} | {summary_text}\n"
            )

        await _send_long(update, "\n".join(lines))
    except Exception as e:
        logger.exception("Failed to get team reports for %s", team_id)
        await update.message.reply_text(f"Errore: {e}")
