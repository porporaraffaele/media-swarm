"""Telegram notification service for sending proactive messages.

Used by the Production Monitor agent and the scheduler to send
daily briefings, reminders, and alerts directly to the user.
"""

import asyncio
import logging

from telegram.constants import ParseMode

from src.config.settings import settings
from telegram import Bot

logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 4096


class TelegramNotifier:
    """Service for sending proactive Telegram notifications."""

    def __init__(self):
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID required for notifications")
        self.bot = Bot(token=settings.telegram_bot_token)
        self.chat_id = settings.telegram_chat_id

    async def send_notification(self, message: str, parse_mode: str = ParseMode.MARKDOWN) -> None:
        """Send a notification message to the configured chat."""
        try:
            # Split long messages
            if len(message) <= MAX_MESSAGE_LENGTH:
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=message,
                    parse_mode=parse_mode,
                )
            else:
                chunks = _split_message(message)
                for chunk in chunks:
                    try:
                        await self.bot.send_message(
                            chat_id=self.chat_id,
                            text=chunk,
                            parse_mode=parse_mode,
                        )
                    except Exception:
                        await self.bot.send_message(
                            chat_id=self.chat_id,
                            text=chunk,
                        )
            logger.info("Sent Telegram notification (%d chars)", len(message))
        except Exception as e:
            logger.error("Failed to send Telegram notification: %s", e)

    def send_notification_sync(self, message: str) -> None:
        """Synchronous wrapper - creates a new event loop if needed."""
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.send_notification(message))
        except RuntimeError:
            asyncio.run(self.send_notification(message))


def _split_message(text: str) -> list[str]:
    """Split a long message into Telegram-safe chunks."""
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
    return chunks
