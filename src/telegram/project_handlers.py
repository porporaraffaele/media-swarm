"""Telegram handlers for project management.

Commands:
- /project_new <name>  — Crea un nuovo progetto
- /projects  — Lista progetti attivi
- /project_teams <id> <team1> <team2>...  — Assegna team al progetto
- /project_set <id>  — Imposta progetto attivo
- /project_info <id>  — Dettagli progetto
"""

import logging

from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.config.constants import ALL_TEAM_IDS
from src.config.settings import settings
from src.telegram.context_manager import get_active_project, set_active_project
from telegram import Update

logger = logging.getLogger(__name__)


def _is_authorized(update: Update) -> bool:
    return str(update.effective_chat.id) == settings.telegram_chat_id


async def project_new_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /project_new <name> [description]."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /project\\_new `<nome>` `[descrizione]`\n"
            "Es: /project\\_new Skincare Brand X Progetto per brand skincare",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    name = context.args[0]
    description = " ".join(context.args[1:]) if len(context.args) > 1 else None

    try:
        from src.services.project_service import ProjectService

        svc = ProjectService()
        result = svc.create_project(name=name, description=description)

        # Auto-set as active
        chat_id = str(update.effective_chat.id)
        set_active_project(chat_id, result["id"])

        await update.message.reply_text(
            f"Progetto creato e impostato come attivo!\n\n"
            f"*{result['name']}*\n"
            f"ID: `{result['id']}`\n\n"
            f"Usa /project\\_teams `{result['id'][:8]}...` per assegnare team.",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.exception("Failed to create project")
        await update.message.reply_text(f"Errore: {e}")


async def projects_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /projects — list active projects."""
    if not _is_authorized(update):
        return

    try:
        from src.services.project_service import ProjectService

        svc = ProjectService()
        projects = svc.list_projects()

        if not projects:
            await update.message.reply_text(
                "Nessun progetto attivo.\nUsa /project\\_new per crearne uno.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        active_id = get_active_project(str(update.effective_chat.id))
        lines = ["*Progetti attivi:*\n"]
        for p in projects:
            marker = " ← ATTIVO" if p["id"] == active_id else ""
            teams = ", ".join(p["team_ids"]) if p["team_ids"] else "nessun team"
            lines.append(f"*{p['name']}*{marker}\n  ID: `{p['id'][:8]}...`\n  Team: {teams}\n")

        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.exception("Failed to list projects")
        await update.message.reply_text(f"Errore: {e}")


async def project_teams_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /project_teams <project_id> <team1> <team2>..."""
    if not _is_authorized(update):
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /project\\_teams `<project_id>` `<team1>` `<team2>`...\n"
            "Es: /project\\_teams abc123 branding copywriting design\n\n"
            "Team disponibili: " + ", ".join(f"`{t}`" for t in ALL_TEAM_IDS),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    project_id = context.args[0]
    team_ids = context.args[1:]

    try:
        from src.services.project_service import ProjectService

        svc = ProjectService()

        # Try to find project by partial ID
        projects = svc.list_projects()
        match = None
        for p in projects:
            if p["id"].startswith(project_id):
                match = p
                break

        if not match:
            await update.message.reply_text(f"Progetto '{project_id}' non trovato.")
            return

        result = svc.update_teams(match["id"], team_ids)
        await update.message.reply_text(
            f"Team aggiornati per *{match['name']}*:\n{', '.join(result['team_ids'])}",
            parse_mode=ParseMode.MARKDOWN,
        )
    except ValueError as e:
        await update.message.reply_text(f"Errore: {e}")
    except Exception as e:
        logger.exception("Failed to update project teams")
        await update.message.reply_text(f"Errore: {e}")


async def project_set_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /project_set <project_id> — set active project."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /project\\_set `<project_id>`\nEs: /project\\_set abc123",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    project_id = context.args[0]

    try:
        from src.services.project_service import ProjectService

        svc = ProjectService()
        projects = svc.list_projects()
        match = None
        for p in projects:
            if p["id"].startswith(project_id):
                match = p
                break

        if not match:
            await update.message.reply_text(f"Progetto '{project_id}' non trovato.")
            return

        chat_id = str(update.effective_chat.id)
        set_active_project(chat_id, match["id"])
        await update.message.reply_text(
            f"Progetto attivo: *{match['name']}*\n"
            f"Tutte le richieste ai team verranno loggate sotto questo progetto.",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.exception("Failed to set active project")
        await update.message.reply_text(f"Errore: {e}")


async def project_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /project_info <project_id> — show project details."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /project\\_info `<project_id>`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    project_id = context.args[0]

    try:
        from src.services.project_service import ProjectService

        svc = ProjectService()
        projects = svc.list_projects()
        match = None
        for p in projects:
            if p["id"].startswith(project_id):
                match = p
                break

        if not match:
            await update.message.reply_text(f"Progetto '{project_id}' non trovato.")
            return

        sessions = svc.get_project_sessions(match["id"], limit=5)
        teams = ", ".join(match["team_ids"]) if match["team_ids"] else "nessun team assegnato"

        lines = [
            f"*{match['name']}*\n",
            f"ID: `{match['id']}`",
            f"Stato: {match['status']}",
            f"Team: {teams}",
            f"Descrizione: {match.get('description') or 'N/A'}",
            f"Creato: {match['created_at']}\n",
        ]

        if sessions:
            lines.append("*Ultime interazioni:*")
            for s in sessions:
                team = s["team_id"] or s["agent_id"] or "?"
                prompt_preview = s["prompt"][:80] + "..." if len(s["prompt"]) > 80 else s["prompt"]
                lines.append(f"  • [{team}] {prompt_preview}")

        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.exception("Failed to get project info")
        await update.message.reply_text(f"Errore: {e}")
