"""Toolkit for the Production Monitor to evaluate agents across all teams.

Provides cross-team access to reports, RAG knowledge, and quality scoring.
"""

import json
import logging

from agno.tools import Toolkit

from src.config.constants import KB_TABLES
from src.db.tables import get_connection

logger = logging.getLogger(__name__)


class AgentEvaluatorTools(Toolkit):
    """Cross-team agent evaluation and RAG querying toolkit."""

    def __init__(self):
        super().__init__(name="agent_evaluator")
        self.register(self.get_all_team_stats)
        self.register(self.get_agent_reports)
        self.register(self.search_agent_knowledge)
        self.register(self.calculate_agent_score)
        self.register(self.get_quality_trends)

    def get_all_team_stats(self) -> str:
        """Get aggregate stats for all teams: report count, avg quality, cost.

        Returns:
            JSON with per-team statistics.
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT team_id,
                               COUNT(*) as total_reports,
                               AVG(quality_score) as avg_quality,
                               SUM(cost_usd) as total_cost,
                               SUM(tokens_used) as total_tokens,
                               MAX(created_at) as last_activity
                        FROM reports
                        GROUP BY team_id
                        ORDER BY team_id
                        """
                    )
                    rows = cur.fetchall()
            stats = []
            for r in rows:
                stats.append(
                    {
                        "team_id": r[0],
                        "total_reports": r[1],
                        "avg_quality": round(float(r[2]), 2) if r[2] else 0,
                        "total_cost": round(float(r[3]), 4) if r[3] else 0,
                        "total_tokens": r[4] or 0,
                        "last_activity": r[5].isoformat() if r[5] else None,
                    }
                )
            return json.dumps(stats)
        except Exception as e:
            logger.error("Failed to get team stats: %s", e)
            return json.dumps({"error": str(e)})

    def get_agent_reports(self, agent_id: str, limit: int = 10) -> str:
        """Get recent reports for any agent (cross-team access).

        Args:
            agent_id: Agent ID to query.
            limit: Number of recent reports (default 10).

        Returns:
            JSON with the agent's recent reports.
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, team_id, task_type,
                               quality_score, cost_usd,
                               created_at, report_data
                        FROM reports
                        WHERE agent_id = %s
                        ORDER BY created_at DESC
                        LIMIT %s
                        """,
                        (agent_id, limit),
                    )
                    rows = cur.fetchall()
            reports = []
            for r in rows:
                reports.append(
                    {
                        "id": str(r[0]),
                        "team_id": r[1],
                        "task_type": r[2],
                        "quality_score": r[3],
                        "cost_usd": r[4],
                        "created_at": r[5].isoformat() if r[5] else None,
                        "report_data": r[6] if isinstance(r[6], dict) else {},
                    }
                )
            return json.dumps(reports)
        except Exception as e:
            logger.error("get_agent_reports(%s): %s", agent_id, e)
            return json.dumps({"error": str(e)})

    def search_agent_knowledge(self, agent_id: str, query: str, max_results: int = 5) -> str:
        """Search any agent's RAG knowledge base.

        Args:
            agent_id: Agent whose KB to search.
            query: Search query.
            max_results: Max results (default 5).

        Returns:
            JSON with search results.
        """
        if agent_id not in KB_TABLES:
            return json.dumps({"error": f"Unknown agent: {agent_id}"})
        try:
            from src.services.knowledge_loader import KnowledgeLoader

            loader = KnowledgeLoader()
            results = loader.search(agent_id=agent_id, query=query, max_results=max_results)
            return json.dumps(
                {
                    "agent_id": agent_id,
                    "query": query,
                    "results": results,
                }
            )
        except Exception as e:
            logger.error("search_agent_knowledge(%s): %s", agent_id, e)
            return json.dumps({"error": str(e)})

    def calculate_agent_score(self, agent_id: str) -> str:
        """Calculate a composite evaluation score for an agent.

        Dimensions: avg quality, consistency, improvement trend, cost.

        Args:
            agent_id: Agent to evaluate.

        Returns:
            JSON with detailed scoring breakdown (1-10 each).
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT quality_score, cost_usd,
                               execution_time_seconds
                        FROM reports
                        WHERE agent_id = %s
                        ORDER BY created_at DESC
                        LIMIT 50
                        """,
                        (agent_id,),
                    )
                    rows = cur.fetchall()

            if not rows:
                return json.dumps(
                    {
                        "agent_id": agent_id,
                        "error": "No reports found",
                    }
                )

            qualities = [r[0] for r in rows if r[0] is not None]
            costs = [r[1] for r in rows if r[1] is not None]

            avg_q = sum(qualities) / len(qualities) if qualities else 0
            consistency = 10 - ((max(qualities) - min(qualities)) if len(qualities) > 1 else 0)
            avg_cost = sum(costs) / len(costs) if costs else 0

            # Trend: recent half vs older half
            if len(qualities) >= 4:
                mid = len(qualities) // 2
                recent = sum(qualities[:mid]) / mid
                older = sum(qualities[mid:]) / (len(qualities) - mid)
                trend = min(10, max(1, 5 + (recent - older) * 2))
            else:
                trend = 5.0

            cost_score = min(10, max(1, 10 - avg_cost * 100))
            overall = avg_q * 0.4 + max(1, consistency) * 0.2 + trend * 0.2 + cost_score * 0.2

            return json.dumps(
                {
                    "agent_id": agent_id,
                    "total_reports": len(rows),
                    "avg_quality": round(avg_q, 2),
                    "consistency": round(max(1, consistency), 2),
                    "improvement_trend": round(trend, 2),
                    "cost_efficiency": round(cost_score, 2),
                    "overall_score": round(max(1, min(10, overall)), 2),
                }
            )
        except Exception as e:
            logger.error("calculate_agent_score(%s): %s", agent_id, e)
            return json.dumps({"error": str(e)})

    def get_quality_trends(self, days: int = 7) -> str:
        """Get quality trends across all agents over the last N days.

        Args:
            days: Lookback period (default 7).

        Returns:
            JSON with per-agent quality trends and anomalies.
        """
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT agent_id, team_id,
                               AVG(quality_score) as avg_q,
                               COUNT(*) as cnt,
                               MIN(quality_score) as min_q,
                               MAX(quality_score) as max_q
                        FROM reports
                        WHERE created_at >= NOW() - make_interval(days => %s)
                        GROUP BY agent_id, team_id
                        ORDER BY avg_q ASC
                        """,
                        (days,),
                    )
                    rows = cur.fetchall()
            trends = []
            for r in rows:
                avg = float(r[2]) if r[2] else 0
                trends.append(
                    {
                        "agent_id": r[0],
                        "team_id": r[1],
                        "avg_quality": round(avg, 2),
                        "report_count": r[3],
                        "min_quality": r[4],
                        "max_quality": r[5],
                        "needs_attention": avg < 5.0,
                    }
                )
            return json.dumps(trends)
        except Exception as e:
            logger.error("get_quality_trends: %s", e)
            return json.dumps({"error": str(e)})
