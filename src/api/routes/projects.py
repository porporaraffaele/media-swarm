"""REST API routes for project management."""

import logging

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/projects", tags=["Projects"])


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectTeamsUpdate(BaseModel):
    team_ids: list[str]


def _svc():
    from src.services.project_service import ProjectService

    return ProjectService()


@router.get("")
async def list_projects(status: str = Query("active")):
    """List projects by status."""
    try:
        return {"projects": _svc().list_projects(status=status)}
    except Exception as e:
        logger.error(f"Failed to list projects: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_project(body: ProjectCreate):
    """Create a new project."""
    try:
        result = _svc().create_project(name=body.name, description=body.description)
        return result
    except Exception as e:
        logger.error(f"Failed to create project: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{project_id}")
async def get_project(project_id: str):
    """Get a single project."""
    project = _svc().get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}/teams")
async def update_project_teams(project_id: str, body: ProjectTeamsUpdate):
    """Assign teams to a project."""
    try:
        result = _svc().update_teams(project_id, body.team_ids)
        if not result:
            raise HTTPException(status_code=404, detail="Project not found")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update project teams: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def archive_project(project_id: str):
    """Archive a project."""
    success = _svc().archive_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "archived", "project_id": project_id}


@router.get("/{project_id}/sessions")
async def get_project_sessions(project_id: str, limit: int = Query(20, ge=1, le=100)):
    """Get interaction history for a project."""
    try:
        sessions = _svc().get_project_sessions(project_id, limit=limit)
        return {"sessions": sessions, "project_id": project_id}
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
