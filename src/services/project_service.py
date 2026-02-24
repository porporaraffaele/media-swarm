"""Project management service for creating and tracking projects."""

import logging

from src.config.constants import ALL_TEAM_IDS
from src.db.tables import get_connection

logger = logging.getLogger(__name__)


class ProjectService:
    """CRUD operations for projects."""

    def create_project(self, name: str, description: str | None = None) -> dict:
        """Create a new project."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO projects (name, description)
                    VALUES (%s, %s) RETURNING id, name, status, created_at
                    """,
                    (name, description),
                )
                row = cur.fetchone()
            conn.commit()
        return {
            "id": str(row[0]),
            "name": row[1],
            "status": row[2],
            "created_at": row[3].isoformat(),
        }

    def list_projects(self, status: str = "active") -> list[dict]:
        """List all projects with given status."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, description, team_ids, status, created_at
                    FROM projects
                    WHERE status = %s
                    ORDER BY created_at DESC
                    """,
                    (status,),
                )
                rows = cur.fetchall()
        return [
            {
                "id": str(r[0]),
                "name": r[1],
                "description": r[2],
                "team_ids": r[3] or [],
                "status": r[4],
                "created_at": r[5].isoformat() if r[5] else None,
            }
            for r in rows
        ]

    def get_project(self, project_id: str) -> dict | None:
        """Get a single project by ID."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, description, team_ids, status, created_at
                    FROM projects WHERE id = %s
                    """,
                    (project_id,),
                )
                row = cur.fetchone()
        if not row:
            return None
        return {
            "id": str(row[0]),
            "name": row[1],
            "description": row[2],
            "team_ids": row[3] or [],
            "status": row[4],
            "created_at": row[5].isoformat() if row[5] else None,
        }

    def update_teams(self, project_id: str, team_ids: list[str]) -> dict | None:
        """Set the teams assigned to a project."""
        # Validate team IDs
        invalid = [t for t in team_ids if t not in ALL_TEAM_IDS]
        if invalid:
            raise ValueError(f"Team non validi: {', '.join(invalid)}")

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE projects SET team_ids = %s, updated_at = NOW()
                    WHERE id = %s RETURNING id, name, team_ids
                    """,
                    (team_ids, project_id),
                )
                row = cur.fetchone()
            conn.commit()
        if not row:
            return None
        return {"id": str(row[0]), "name": row[1], "team_ids": row[2] or []}

    def archive_project(self, project_id: str) -> bool:
        """Archive a project."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE projects SET status = 'archived', "
                    "updated_at = NOW() WHERE id = %s RETURNING id",
                    (project_id,),
                )
                result = cur.fetchone()
            conn.commit()
        return result is not None

    def log_session(
        self,
        project_id: str,
        team_id: str | None,
        agent_id: str | None,
        prompt: str,
        response: str | None,
    ) -> None:
        """Log an interaction under a project."""
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO project_sessions
                            (project_id, team_id, agent_id, prompt, response)
                        VALUES (%s, %s, %s, %s, %s)
                        """,
                        (project_id, team_id, agent_id, prompt, response),
                    )
                conn.commit()
        except Exception:
            logger.exception("Failed to log project session")

    def get_project_sessions(self, project_id: str, limit: int = 10) -> list[dict]:
        """Get recent sessions for a project."""
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT team_id, agent_id, prompt, response, created_at
                    FROM project_sessions
                    WHERE project_id = %s
                    ORDER BY created_at DESC LIMIT %s
                    """,
                    (project_id, limit),
                )
                rows = cur.fetchall()
        return [
            {
                "team_id": r[0],
                "agent_id": r[1],
                "prompt": r[2][:200] if r[2] else "",
                "response": r[3][:200] if r[3] else "",
                "created_at": r[4].isoformat() if r[4] else None,
            }
            for r in rows
        ]
