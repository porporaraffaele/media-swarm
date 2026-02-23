"""Toolkit for saving and retrieving micro-task reports.

Every sub-agent uses this toolkit to:
1. Save structured reports to the PostgreSQL `reports` table after each task
2. Query recent reports for self-reference and context
"""

import json
import logging
from datetime import datetime, timezone

from agno.tools.toolkit import Toolkit

from src.db.tables import get_connection

logger = logging.getLogger(__name__)


class ReportTools(Toolkit):
    """Toolkit for managing micro-task reports in the database."""

    def __init__(self, team_id: str, agent_id: str):
        self.team_id = team_id
        self.agent_id = agent_id
        super().__init__(name="report_tools")
        self.register(self.save_report)
        self.register(self.get_recent_reports)

    def save_report(self, report_json: str) -> str:
        """Save a micro-task report to the database.

        Args:
            report_json: JSON string of the report data following the BaseReport schema.

        Returns:
            Confirmation message with the report ID.
        """
        try:
            report_data = json.loads(report_json)
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO reports (
                            team_id, agent_id, task_type, report_data,
                            quality_score, tokens_used, cost_usd,
                            execution_time_seconds, session_id, user_id,
                            parent_report_id, created_at
                        ) VALUES (
                            %s, %s, %s, %s::jsonb,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s
                        ) RETURNING id
                        """,
                        (
                            self.team_id,
                            self.agent_id,
                            report_data.get("task_type", "unknown"),
                            json.dumps(report_data),
                            report_data.get("quality_score", 7.0),
                            report_data.get("tokens_used", 0),
                            report_data.get("cost_usd", 0.0),
                            report_data.get("execution_time_seconds", 0.0),
                            report_data.get("session_id"),
                            report_data.get("user_id"),
                            report_data.get("parent_report_id"),
                            datetime.now(timezone.utc),
                        ),
                    )
                    report_id = cur.fetchone()[0]
                conn.commit()
            return json.dumps({"status": "saved", "report_id": str(report_id)})
        except Exception as e:
            logger.error(f"Failed to save report: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    def get_recent_reports(self, limit: int = 10) -> str:
        """Get recent reports for this agent.

        Args:
            limit: Number of recent reports to retrieve (default: 10).

        Returns:
            JSON string with list of recent reports.
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, task_type, quality_score, cost_usd,
                               execution_time_seconds, created_at,
                               report_data->'status' as status,
                               report_data->'task_description' as description
                        FROM reports
                        WHERE team_id = %s AND agent_id = %s
                        ORDER BY created_at DESC
                        LIMIT %s
                        """,
                        (self.team_id, self.agent_id, limit),
                    )
                    rows = cur.fetchall()
            reports = [
                {
                    "id": str(row[0]),
                    "task_type": row[1],
                    "quality_score": row[2],
                    "cost_usd": row[3],
                    "execution_time_seconds": row[4],
                    "created_at": row[5].isoformat() if row[5] else None,
                    "status": row[6],
                    "description": row[7],
                }
                for row in rows
            ]
            return json.dumps(reports)
        except Exception as e:
            logger.error(f"Failed to get reports: {e}")
            return json.dumps({"status": "error", "message": str(e)})
