"""Telegram bot for Media Swarm.

Provides full access to 14 teams, 97 agents, RAG knowledge, reports, and projects.
Runs alongside the FastAPI AgentOS server using PTB's async application.
"""

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from src.config.settings import settings

# Agent handlers
from src.telegram.agent_handlers import (
    agent_handler,
    agent_info_handler,
    agents_list_handler,
    reports_handler,
    reports_team_handler,
)

# Team handlers
from src.telegram.handlers import (
    ads_handler,
    analyst_handler,
    ask_handler,
    branding_handler,
    community_handler,
    competitors_handler,
    copy_handler,
    create_handler,
    design_handler,
    find_handler,
    free_text_handler,
    help_handler,
    ideation_handler,
    news_handler,
    sales_handler,
    start_handler,
    status_handler,
    unknown_command_handler,
    web_handler,
)

# Knowledge handlers
from src.telegram.knowledge_handlers import (
    kb_document_handler,
    kb_list_handler,
    kb_search_handler,
    kb_upload_handler,
    kb_url_handler,
)

# Project handlers
from src.telegram.project_handlers import (
    project_info_handler,
    project_new_handler,
    project_set_handler,
    project_teams_handler,
    projects_handler,
)

logger = logging.getLogger(__name__)


def create_telegram_app():
    """Create and configure the Telegram bot application.

    Returns the PTB Application instance ready to be started.
    Returns None if the bot token is not configured.
    """
    if not settings.telegram_bot_token:
        logger.warning("TELEGRAM_BOT_TOKEN not set - Telegram bot disabled")
        return None

    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    # ─── Team commands (12 teams + ask + status + help + start) ────────────
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("status", status_handler))
    app.add_handler(CommandHandler("ask", ask_handler))
    app.add_handler(CommandHandler("branding", branding_handler))
    app.add_handler(CommandHandler("copy", copy_handler))
    app.add_handler(CommandHandler("design", design_handler))
    app.add_handler(CommandHandler("competitors", competitors_handler))
    app.add_handler(CommandHandler("news", news_handler))
    app.add_handler(CommandHandler("community", community_handler))
    app.add_handler(CommandHandler("ideation", ideation_handler))
    app.add_handler(CommandHandler("find", find_handler))
    app.add_handler(CommandHandler("create", create_handler))
    app.add_handler(CommandHandler("analyst", analyst_handler))
    app.add_handler(CommandHandler("sales", sales_handler))
    app.add_handler(CommandHandler("ads", ads_handler))
    app.add_handler(CommandHandler("web", web_handler))

    # ─── Agent commands ────────────────────────────────────────────────────
    app.add_handler(CommandHandler("agent", agent_handler))
    app.add_handler(CommandHandler("agents", agents_list_handler))
    app.add_handler(CommandHandler("agent_info", agent_info_handler))
    app.add_handler(CommandHandler("reports", reports_handler))
    app.add_handler(CommandHandler("reports_team", reports_team_handler))

    # ─── Knowledge/RAG commands ────────────────────────────────────────────
    app.add_handler(CommandHandler("kb_upload", kb_upload_handler))
    app.add_handler(CommandHandler("kb_url", kb_url_handler))
    app.add_handler(CommandHandler("kb_list", kb_list_handler))
    app.add_handler(CommandHandler("kb_search", kb_search_handler))

    # ─── Project commands ──────────────────────────────────────────────────
    app.add_handler(CommandHandler("project_new", project_new_handler))
    app.add_handler(CommandHandler("projects", projects_handler))
    app.add_handler(CommandHandler("project_teams", project_teams_handler))
    app.add_handler(CommandHandler("project_set", project_set_handler))
    app.add_handler(CommandHandler("project_info", project_info_handler))

    # ─── Document upload handler (for /kb_upload file flow) ────────────────
    app.add_handler(MessageHandler(filters.Document.ALL, kb_document_handler))

    # ─── Unknown command handler (catch-all for unrecognized /commands) ────
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command_handler))

    # ─── Free text handler (no command) → Master Orchestrator ──────────────
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_text_handler))

    # ─── Global error handler ──────────────────────────────────────────────
    async def _error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.error("Telegram handler error: %s", context.error, exc_info=context.error)

    app.add_error_handler(_error_handler)

    logger.info("Telegram bot configured with 32 commands + file upload + free text")
    return app


async def start_telegram_bot() -> None:
    """Start the Telegram bot in polling mode (non-blocking)."""
    tg_app = create_telegram_app()
    if tg_app is None:
        return

    logger.info("Starting Telegram bot polling...")
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling(drop_pending_updates=True)
    logger.info("Telegram bot is running")


async def stop_telegram_bot(tg_app) -> None:
    """Stop the Telegram bot gracefully."""
    if tg_app is None:
        return

    logger.info("Stopping Telegram bot...")
    await tg_app.updater.stop()
    await tg_app.stop()
    await tg_app.shutdown()
    logger.info("Telegram bot stopped")
