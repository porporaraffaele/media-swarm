"""Telegram command handlers for Media Swarm teams.

Each handler:
1. Checks authorization (only the configured chat_id can use the bot)
2. Sends a "processing" message
3. Runs the appropriate team asynchronously
4. Returns the response (split if > 4096 chars)
"""

import logging

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.config.settings import settings

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096


def _is_authorized(update: Update) -> bool:
    """Check if the sender is the authorized user."""
    chat_id = str(update.effective_chat.id)
    return chat_id == settings.telegram_chat_id


async def _send_long_message(update: Update, text: str) -> None:
    """Send a message, splitting it if it exceeds Telegram's limit."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        return

    # Split on newlines to avoid breaking mid-sentence
    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > MAX_MESSAGE_LENGTH:
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
            # Fallback without markdown if parsing fails
            await update.message.reply_text(chunk)


async def _run_team(update: Update, team_name: str, team_module: str, user_text: str) -> None:
    """Generic handler: run a team and send the response."""
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return

    if not user_text:
        await update.message.reply_text(f"Scrivi qualcosa dopo il comando.\nEs: /{team_module} la tua richiesta")
        return

    await update.effective_chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text(f"Sto elaborando con il team {team_name}...")

    try:
        team = _get_team(team_module)
        response = await team.arun(message=user_text)

        # Extract the text content from the RunResponse
        result = _extract_response_text(response)
        await processing.delete()
        await _send_long_message(update, result)

    except Exception as e:
        logger.exception("Error running team %s", team_name)
        await processing.edit_text(f"Errore con il team {team_name}: {e}")


def _get_team(team_key: str):
    """Lazy-import a team by key to avoid circular imports."""
    teams = {
        "ask": "src.agents.master_orchestrator.team:master_orchestrator",
        "branding": "src.agents.branding.team:branding_team",
        "copy": "src.agents.copywriting.team:copywriting_team",
        "design": "src.agents.graphic_design.team:graphic_design_team",
        "competitors": "src.agents.competitors.team:competitors_team",
        "news": "src.agents.news.team:news_team",
        "community": "src.agents.community.team:community_team",
        "ideation": "src.agents.content_ideation.team:content_ideation_team",
        "find": "src.agents.content_finder.team:content_finder_team",
        "create": "src.agents.content_creator.team:content_creator_team",
        "analyst": "src.agents.analyst.team:analyst_team",
    }

    module_path, attr_name = teams[team_key].rsplit(":", 1)

    import importlib

    module = importlib.import_module(module_path)
    return getattr(module, attr_name)


def _extract_response_text(response) -> str:
    """Extract text from an Agno RunResponse."""
    if response is None:
        return "Nessuna risposta dal team."

    # RunResponse has a .content attribute
    if hasattr(response, "content"):
        return str(response.content)

    # TeamRunResponse may have .messages
    if hasattr(response, "messages") and response.messages:
        parts = []
        for msg in response.messages:
            if hasattr(msg, "content") and msg.content:
                parts.append(str(msg.content))
        return "\n\n".join(parts) if parts else str(response)

    return str(response)


# ─── Command Handlers ──────────────────────────────────────────────────────


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return

    await update.message.reply_text(
        "Benvenuto in *Media Swarm*!\n\n"
        "Sono la tua AI media company con 11 team specializzati.\n\n"
        "Usa /help per vedere i comandi disponibili.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not _is_authorized(update):
        return

    await update.message.reply_text(
        "*Comandi disponibili:*\n\n"
        "/ask `domanda` - Domanda libera (Master Orchestrator)\n"
        "/branding `richiesta` - Team Branding\n"
        "/copy `richiesta` - Team Copywriting\n"
        "/design `richiesta` - Team Graphic Design\n"
        "/competitors `richiesta` - Team Competitors\n"
        "/news `richiesta` - Team News\n"
        "/community `richiesta` - Team Community\n"
        "/ideation `richiesta` - Team Content Ideation\n"
        "/find `richiesta` - Team Content Finder\n"
        "/create `richiesta` - Team Content Creator\n"
        "/analyst `richiesta` - Team Analyst\n"
        "/status - Stato del sistema\n\n"
        "Puoi anche scrivere senza comando per parlare con il Master Orchestrator.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    if not _is_authorized(update):
        return

    await update.message.reply_text(
        "*Media Swarm Status*\n\n"
        "Teams: 11\n"
        "Sub-agents: 73\n"
        "API: http://localhost:7777\n"
        "Agent UI: http://localhost:3000\n"
        "Status: Running",
        parse_mode=ParseMode.MARKDOWN,
    )


async def ask_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ask command - Master Orchestrator."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Master Orchestrator", "ask", user_text)


async def branding_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /branding command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Branding", "branding", user_text)


async def copy_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /copy command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Copywriting", "copy", user_text)


async def design_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /design command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Graphic Design", "design", user_text)


async def competitors_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /competitors command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Competitors", "competitors", user_text)


async def news_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /news command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "News", "news", user_text)


async def community_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /community command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Community", "community", user_text)


async def ideation_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ideation command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Content Ideation", "ideation", user_text)


async def find_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /find command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Content Finder", "find", user_text)


async def create_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /create command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Content Creator", "create", user_text)


async def analyst_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /analyst command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Analyst", "analyst", user_text)


async def free_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free text messages (no command) - routes to Master Orchestrator."""
    if not _is_authorized(update):
        return

    user_text = update.message.text
    if user_text:
        await _run_team(update, "Master Orchestrator", "ask", user_text)
