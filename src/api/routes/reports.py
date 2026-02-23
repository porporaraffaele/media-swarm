"""Admin routes for browsing and querying micro-task reports."""

import logging

from fastapi import APIRouter, HTTPException, Query

from src.db.tables import get_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/reports", tags=["Reports"])


@router.get("")
async def list_reports(
    team_id: str | None = Query(None, description="Filter by team ID"),
    agent_id: str | None = Query(None, description="Filter by agent ID"),
    task_type: str | None = Query(None, description="Filter by task type"),
    min_quality: float | None = Query(None, ge=0, le=10, description="Minimum quality score"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """List reports with optional filters."""
    try:
        conditions = []
        params = []

        if team_id:
            conditions.append("team_id = %s")
            params.append(team_id)
        if agent_id:
            conditions.append("agent_id = %s")
            params.append(agent_id)
        if task_type:
            conditions.append("task_type = %s")
            params.append(task_type)
        if min_quality is not None:
            conditions.append("quality_score >= %s")
            params.append(min_quality)

        where_clause = " AND ".join(conditions) if conditions else "TRUE"
        params.extend([limit, offset])

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT id, team_id, agent_id, task_type, quality_score,
                           tokens_used, cost_usd, execution_time_seconds,
                           created_at, report_data->'status' as status
                    FROM reports
                    WHERE {where_clause}
                    ORDER BY created_at DESC
                    LIMIT %s OFFSET %s
                    """,
                    params,
                )
                rows = cur.fetchall()

                cur.execute(
                    f"SELECT COUNT(*) FROM reports WHERE {where_clause}",
                    params[:-2],  # exclude limit/offset
                )
                total = cur.fetchone()[0]

        reports = [
            {
                "id": str(row[0]),
                "team_id": row[1],
                "agent_id": row[2],
                "task_type": row[3],
                "quality_score": row[4],
                "tokens_used": row[5],
                "cost_usd": row[6],
                "execution_time_seconds": row[7],
                "created_at": row[8].isoformat() if row[8] else None,
                "status": row[9],
            }
            for row in rows
        ]
        return {"reports": reports, "total": total, "limit": limit, "offset": offset}
    except Exception as e:
        logger.error(f"Failed to list reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Get a single report with full data."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, team_id, agent_id, task_type, report_data,
                           quality_score, tokens_used, cost_usd,
                           execution_time_seconds, session_id, user_id,
                           parent_report_id, created_at
                    FROM reports WHERE id = %s
                    """,
                    (report_id,),
                )
                row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Report not found")
        return {
            "id": str(row[0]),
            "team_id": row[1],
            "agent_id": row[2],
            "task_type": row[3],
            "report_data": row[4],
            "quality_score": row[5],
            "tokens_used": row[6],
            "cost_usd": row[7],
            "execution_time_seconds": row[8],
            "session_id": row[9],
            "user_id": row[10],
            "parent_report_id": str(row[11]) if row[11] else None,
            "created_at": row[12].isoformat() if row[12] else None,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get report {report_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/summary")
async def report_stats():
    """Get aggregate statistics across all reports."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        team_id,
                        COUNT(*) as total_reports,
                        AVG(quality_score) as avg_quality,
                        SUM(cost_usd) as total_cost,
                        SUM(tokens_used) as total_tokens,
                        AVG(execution_time_seconds) as avg_time
                    FROM reports
                    GROUP BY team_id
                    ORDER BY team_id
                    """
                )
                rows = cur.fetchall()
        stats = [
            {
                "team_id": row[0],
                "total_reports": row[1],
                "avg_quality": round(float(row[2]), 2) if row[2] else 0,
                "total_cost": round(float(row[3]), 4) if row[3] else 0,
                "total_tokens": row[4] or 0,
                "avg_time_seconds": round(float(row[5]), 2) if row[5] else 0,
            }
            for row in rows
        ]
        return {"stats": stats}
    except Exception as e:
        logger.error(f"Failed to get report stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
