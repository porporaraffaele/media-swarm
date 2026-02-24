"""Background scheduler for automated agent tasks.

Runs periodic tasks like daily production briefings via the Analyst team.
Uses the `schedule` library in a daemon thread so it doesn't block FastAPI.
"""

import asyncio
import logging
import threading
import time

import schedule

logger = logging.getLogger(__name__)


class AgentScheduler:
    """Scheduler for running periodic agent tasks."""

    def __init__(self):
        self._running = False
        self._thread: threading.Thread | None = None

    def schedule_daily_briefing(self, time_str: str = "09:00") -> None:
        """Schedule daily production briefing at specified time (HH:MM)."""
        schedule.every().day.at(time_str).do(self._trigger_daily_briefing)
        logger.info("Scheduled daily briefing at %s", time_str)

    def _trigger_daily_briefing(self) -> None:
        """Trigger the daily briefing (runs in scheduler thread)."""
        logger.info("Running scheduled daily briefing...")
        try:
            from src.services.telegram_notifier import TelegramNotifier

            notifier = TelegramNotifier()

            # Run analyst team with briefing prompt
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Import team lazily
                import importlib

                module = importlib.import_module("src.agents.analyst.team")
                analyst_team = getattr(module, "analyst_team")

                response = loop.run_until_complete(
                    analyst_team.arun(
                        message=(
                            "Generate a daily production briefing:\n"
                            "1. Summary of all agent activity in the last 24 hours\n"
                            "2. Top 3 improvement suggestions per sector\n"
                            "3. Pending tasks requiring user attention\n"
                            "4. Quality and cost trends\n"
                            "Keep it concise and actionable for Telegram."
                        )
                    )
                )

                # Extract text from response
                if hasattr(response, "content"):
                    briefing = str(response.content)
                elif hasattr(response, "messages") and response.messages:
                    parts = []
                    for msg in response.messages:
                        if hasattr(msg, "content") and msg.content:
                            parts.append(str(msg.content))
                    briefing = "\n\n".join(parts) if parts else str(response)
                else:
                    briefing = str(response)

                # Send via Telegram
                loop.run_until_complete(
                    notifier.send_notification(f"*Daily Production Briefing*\n\n{briefing}")
                )
                logger.info("Daily briefing sent successfully")
            finally:
                loop.close()

        except Exception:
            logger.exception("Failed to run daily briefing")

    def start(self) -> None:
        """Start the scheduler in a background daemon thread."""

        def _run_loop():
            self._running = True
            while self._running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        self._thread = threading.Thread(target=_run_loop, daemon=True)
        self._thread.start()
        logger.info("Agent scheduler started (daemon thread)")

    def stop(self) -> None:
        """Stop the scheduler."""
        self._running = False
        logger.info("Agent scheduler stopped")
