"""Telegram handlers for RAG knowledge base management.

Commands:
- /kb_upload <agent_id>  — Istruzioni per caricare un file
- /kb_url <agent_id> <url>  — Carica URL nel RAG
- /kb_list <agent_id>  — Lista documenti caricati
- /kb_search <agent_id> <query>  — Ricerca semantica
- Document handler  — Riceve file dopo /kb_upload
"""

import logging

from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from src.config.constants import KB_TABLES
from src.config.settings import settings
from telegram import Update

logger = logging.getLogger(__name__)

# Track pending uploads: chat_id → agent_id
_pending_uploads: dict[str, str] = {}


def _is_authorized(update: Update) -> bool:
    return str(update.effective_chat.id) == settings.telegram_chat_id


async def kb_upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /kb_upload <agent_id> — set pending upload state."""
    if not _is_authorized(update):
        await update.message.reply_text("Non sei autorizzato.")
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /kb\\_upload `<agent_id>`\n\n"
            "Poi invia il file (PDF, DOCX, CSV, TXT).\n"
            "Es: /kb\\_upload branding-strategist",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    if agent_id not in KB_TABLES:
        await update.message.reply_text(
            f"Agente '{agent_id}' non trovato.\nUsa /agents per la lista completa."
        )
        return

    chat_id = str(update.effective_chat.id)
    _pending_uploads[chat_id] = agent_id
    await update.message.reply_text(
        f"Pronto per ricevere un file per *{agent_id}*.\nInvia un file (PDF, DOCX, CSV, TXT) ora.",
        parse_mode=ParseMode.MARKDOWN,
    )


async def kb_document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle file uploads after /kb_upload."""
    if not _is_authorized(update):
        return

    chat_id = str(update.effective_chat.id)
    agent_id = _pending_uploads.pop(chat_id, None)

    if not agent_id:
        await update.message.reply_text(
            "Nessun upload in sospeso. Usa /kb\\_upload `<agent_id>` prima.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    document = update.message.document
    if not document:
        await update.message.reply_text(
            "File non valido. Invia un documento (PDF, DOCX, CSV, TXT)."
        )
        _pending_uploads[chat_id] = agent_id  # Re-set pending
        return

    await update.effective_chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text(
        f"Caricamento di *{document.file_name}* nel RAG di *{agent_id}*...",
        parse_mode=ParseMode.MARKDOWN,
    )

    try:
        from src.services.knowledge_loader import KnowledgeLoader

        # Download file bytes from Telegram
        tg_file = await document.get_file()
        file_bytes = await tg_file.download_as_bytearray()

        loader = KnowledgeLoader()
        result = await loader.aload_file_bytes(
            agent_id=agent_id,
            data=bytes(file_bytes),
            filename=document.file_name or "file",
        )

        await processing.edit_text(
            f"File caricato nel RAG di *{agent_id}*\n"
            f"Chunks: {result['chunk_count']}\n"
            f"Doc ID: `{result['document_id']}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.exception("Failed to load file for %s", agent_id)
        await processing.edit_text(f"Errore nel caricamento: {e}")


async def kb_url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /kb_url <agent_id> <url> — load URL into RAG."""
    if not _is_authorized(update):
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /kb\\_url `<agent_id>` `<url>`\n"
            "Es: /kb\\_url branding-strategist https://example.com",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    url = context.args[1]

    if agent_id not in KB_TABLES:
        await update.message.reply_text(f"Agente '{agent_id}' non trovato.")
        return

    await update.effective_chat.send_action(ChatAction.TYPING)
    processing = await update.message.reply_text(
        f"Caricamento URL nel RAG di *{agent_id}*...",
        parse_mode=ParseMode.MARKDOWN,
    )

    try:
        from src.services.knowledge_loader import KnowledgeLoader

        loader = KnowledgeLoader()
        result = await loader.aload_url(agent_id=agent_id, url=url)

        await processing.edit_text(
            f"URL caricato nel RAG di *{agent_id}*\n"
            f"URL: {url}\n"
            f"Chunks: {result['chunk_count']}\n"
            f"Doc ID: `{result['document_id']}`",
            parse_mode=ParseMode.MARKDOWN,
        )
    except Exception as e:
        logger.exception("Failed to load URL for %s", agent_id)
        await processing.edit_text(f"Errore nel caricamento URL: {e}")


async def kb_list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /kb_list <agent_id> — list documents in an agent's KB."""
    if not _is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text(
            "Uso: /kb\\_list `<agent_id>`\nEs: /kb\\_list branding-strategist",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    if agent_id not in KB_TABLES:
        await update.message.reply_text(f"Agente '{agent_id}' non trovato.")
        return

    try:
        from src.db.tables import get_connection

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT title, source_type, chunk_count, status, added_at
                    FROM knowledge_documents
                    WHERE agent_id = %s AND status != 'archived'
                    ORDER BY added_at DESC LIMIT 20
                    """,
                    (agent_id,),
                )
                rows = cur.fetchall()

        if not rows:
            await update.message.reply_text(
                f"Nessun documento nel RAG di *{agent_id}*.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        lines = [f"*Documenti di {agent_id}:*\n"]
        for row in rows:
            title, source_type, chunks, status, added_at = row
            date_str = added_at.strftime("%d/%m %H:%M") if added_at else "?"
            lines.append(f"• {title} ({source_type}, {chunks} chunks, {status}) - {date_str}")

        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.exception("Failed to list KB for %s", agent_id)
        await update.message.reply_text(f"Errore: {e}")


async def kb_search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /kb_search <agent_id> <query> — semantic search."""
    if not _is_authorized(update):
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /kb\\_search `<agent_id>` `<query>`\n"
            "Es: /kb\\_search branding-strategist brand positioning",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    agent_id = context.args[0]
    query = " ".join(context.args[1:])

    if agent_id not in KB_TABLES:
        await update.message.reply_text(f"Agente '{agent_id}' non trovato.")
        return

    await update.effective_chat.send_action(ChatAction.TYPING)

    try:
        from src.services.knowledge_loader import KnowledgeLoader

        loader = KnowledgeLoader()
        results = await loader.asearch(agent_id=agent_id, query=query, max_results=5)

        if not results:
            await update.message.reply_text(
                f"Nessun risultato per '{query}' nel RAG di *{agent_id}*.",
                parse_mode=ParseMode.MARKDOWN,
            )
            return

        lines = [f"*Ricerca in {agent_id}:* '{query}'\n"]
        for i, r in enumerate(results, 1):
            c = r["content"]
            content_preview = c[:200] + "..." if len(c) > 200 else c
            lines.append(f"*{i}.* {r['name']}\n{content_preview}\n")

        text = "\n".join(lines)
        if len(text) > 4000:
            text = text[:4000] + "\n\n_...troncato_"

        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.exception("Failed to search KB for %s", agent_id)
        await update.message.reply_text(f"Errore nella ricerca: {e}")
