"""Telegram command handlers for Media Swarm teams.

Each handler:
1. Checks authorization (only the configured chat_id can use the bot)
2. Sends a "processing" message
3. Runs the appropriate team asynchronously
4. Returns the response (split if > 4096 chars)
5. Logs interaction under active project if set
"""

import logging

from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.config.settings import settings
from telegram import Update

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096


def _is_authorized(update: Update) -> bool:
    """Check if the sender is the authorized user."""
    chat_id = str(update.effective_chat.id)
    authorized = chat_id == settings.telegram_chat_id
    if not authorized:
        logger.warning(
            "Unauthorized access: chat_id=%s, expected=%s",
            chat_id,
            settings.telegram_chat_id,
        )
    return authorized


async def _send_long_message(update: Update, text: str) -> None:
    """Send a message, splitting it if it exceeds Telegram's limit."""
    if len(text) <= MAX_MESSAGE_LENGTH:
        try:
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception:
            await update.message.reply_text(text)
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
            await update.message.reply_text(chunk)


def _log_to_project(chat_id: str, team_key: str, user_text: str, result: str) -> None:
    """Log interaction to active project if set."""
    try:
        from src.telegram.context_manager import get_active_project

        project_id = get_active_project(chat_id)
        if project_id:
            from src.services.project_service import ProjectService

            svc = ProjectService()
            svc.log_session(
                project_id=project_id,
                team_id=team_key,
                agent_id=None,
                prompt=user_text,
                response=result[:1000] if result else None,
            )
    except Exception:
        logger.debug("Could not log to project", exc_info=True)


async def _run_team(update: Update, team_name: str, team_module: str, user_text: str) -> None:
    """Generic handler: run a team and send the response."""
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return

    if not user_text:
        await update.message.reply_text(
            f"Scrivi qualcosa dopo il comando.\nEs: /{team_module} la tua richiesta"
        )
        return

    await update.effective_chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text(f"Sto elaborando con il team {team_name}...")

    try:
        team = _get_team(team_module)
        response = await team.arun(input=user_text)

        # Extract the text content from the RunResponse
        result = _extract_response_text(response)
        await processing.delete()
        await _send_long_message(update, result)

        # Log to active project
        chat_id = str(update.effective_chat.id)
        _log_to_project(chat_id, team_module, user_text, result)

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
        "sales": "src.agents.sales.team:sales_team",
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
    logger.info("start_handler called by chat_id=%s", update.effective_chat.id)
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato a usare questo bot.")
        return

    await update.message.reply_text(
        "Benvenuto in *Media Swarm*! 🚀\n\n"
        "Sono la tua AI media company con *12 team* e *81 agenti* specializzati.\n\n"
        "Usa /help per vedere tutti i comandi disponibili.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    if not _is_authorized(update):
        return

    await update.message.reply_text(
        "*TEAM (12):*\n"
        "/ask `msg` — Master Orchestrator\n"
        "/branding `msg` — Branding\n"
        "/copy `msg` — Copywriting\n"
        "/design `msg` — Graphic Design\n"
        "/competitors `msg` — Competitors & Market\n"
        "/news `msg` — News\n"
        "/community `msg` — Community\n"
        "/ideation `msg` — Content Ideation\n"
        "/find `msg` — Content Finder\n"
        "/create `msg` — Content Creator\n"
        "/analyst `msg` — Analyst\n"
        "/sales `msg` — Sales & Lead Gen\n\n"
        "*AGENTI SINGOLI:*\n"
        "/agent `id` `msg` — Esegui un agente\n"
        "/agents — Lista tutti gli agenti\n"
        "/agent\\_info `id` — Info agente\n\n"
        "*KNOWLEDGE (RAG):*\n"
        "/kb\\_upload `id` — Carica file (poi invia)\n"
        "/kb\\_url `id` `url` — Carica URL\n"
        "/kb\\_list `id` — Lista documenti\n"
        "/kb\\_search `id` `query` — Cerca nel RAG\n\n"
        "*REPORT & MONITORING:*\n"
        "/reports `id` — Report di un agente\n"
        "/reports\\_team `team` — Report di un team\n\n"
        "*PROGETTI:*\n"
        "/project\\_new `nome` — Crea progetto\n"
        "/projects — Lista progetti\n"
        "/project\\_teams `id` `t1 t2` — Assegna team\n"
        "/project\\_set `id` — Progetto attivo\n"
        "/project\\_info `id` — Dettagli\n\n"
        "/status — Stato sistema\n\n"
        "_Scrivi senza comando per il Master Orchestrator._",
        parse_mode=ParseMode.MARKDOWN,
    )


async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    if not _is_authorized(update):
        return

    # Count KB docs
    kb_count = 0
    report_count = 0
    try:
        from src.db.tables import get_connection

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM knowledge_documents WHERE status != 'archived'")
                row = cur.fetchone()
                kb_count = row[0] if row else 0
                cur.execute("SELECT COUNT(*) FROM reports")
                row = cur.fetchone()
                report_count = row[0] if row else 0
    except Exception:
        pass

    # Check active project
    active_project = "Nessuno"
    try:
        from src.services.project_service import ProjectService
        from src.telegram.context_manager import get_active_project

        pid = get_active_project(str(update.effective_chat.id))
        if pid:
            svc = ProjectService()
            p = svc.get_project(pid)
            if p:
                active_project = p["name"]
    except Exception:
        pass

    await update.message.reply_text(
        "*Media Swarm Status*\n\n"
        "Team: 12\n"
        "Sub-agenti: 81\n"
        f"Documenti RAG: {kb_count}\n"
        f"Report salvati: {report_count}\n"
        f"Progetto attivo: {active_project}\n"
        "API: http://localhost:7777\n"
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


async def sales_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /sales command."""
    user_text = " ".join(context.args) if context.args else ""
    await _run_team(update, "Sales & Lead Generation", "sales", user_text)


async def unknown_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unrecognized commands."""
    logger.info(
        "Unknown command from chat_id=%s: %s",
        update.effective_chat.id,
        update.message.text,
    )
    if not _is_authorized(update):
        return
    await update.message.reply_text("Comando non riconosciuto. Usa /help per la lista.")


async def free_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free text messages (no command) - routes to Master Orchestrator."""
    logger.info(
        "Free text from chat_id=%s: %s",
        update.effective_chat.id,
        update.message.text[:50] if update.message.text else "",
    )
    if not _is_authorized(update):
        return

    user_text = update.message.text
    if user_text:
        await _run_team(update, "Master Orchestrator", "ask", user_text)
