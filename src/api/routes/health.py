"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "ok", "service": "media-swarm"}
