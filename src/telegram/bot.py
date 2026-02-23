"""Telegram bot for Media Swarm.

Provides command-based access to all 11 agent teams via Telegram.
Runs alongside the FastAPI AgentOS server using PTB's async application.
"""

import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.config.settings import settings
from src.telegram.handlers import (
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
    start_handler,
    status_handler,
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

    # Register command handlers
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

    # Free text handler (no command) - routes to Master Orchestrator
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_text_handler))

    logger.info("Telegram bot configured with 14 commands + free text")
    return app


async def start_telegram_bot() -> None:
    """Start the Telegram bot in polling mode (non-blocking).

    Called from the FastAPI lifespan to run alongside the web server.
    """
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
