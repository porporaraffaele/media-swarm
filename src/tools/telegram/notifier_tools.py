"""Toolkit for agents to send proactive Telegram notifications.

Used by the Production Monitor agent to send briefings, reminders,
and improvement suggestions directly to the user via Telegram.
"""

import logging

from agno.tools import Toolkit

logger = logging.getLogger(__name__)


class TelegramNotifierTools(Toolkit):
    """Toolkit for sending Telegram notifications from agents."""

    def __init__(self):
        super().__init__(name="telegram_notifier")
        self._notifier = None
        self.register(self.send_telegram_notification)

    def _get_notifier(self):
        """Lazy-init notifier to avoid import errors when Telegram is not configured."""
        if self._notifier is None:
            from src.services.telegram_notifier import TelegramNotifier

            self._notifier = TelegramNotifier()
        return self._notifier

    def send_telegram_notification(self, message: str) -> str:
        """Send a notification message to the user via Telegram.

        Use this to send proactive updates, daily briefings, reminders,
        and improvement suggestions. Supports Markdown formatting.

        Args:
            message: The message text to send (supports Markdown).

        Returns:
            Confirmation message.
        """
        try:
            notifier = self._get_notifier()
            notifier.send_notification_sync(message)
            return "Notification sent successfully via Telegram."
        except Exception as e:
            logger.error("Failed to send notification: %s", e)
            return f"Error sending notification: {e}"
