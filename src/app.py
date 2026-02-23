"""Media Swarm - AgentOS Main Entrypoint.

Starts the FastAPI server with:
- All agent teams registered in AgentOS
- Custom admin routes for knowledge, reports, and agent configuration
- Agent UI frontend connects to this server at port 7777

Usage:
    uv run python -m src.app
"""

import logging

from fastapi import FastAPI

from src.api.routes import agent_config, health, knowledge_admin, reports
from src.config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ─── FastAPI App ────────────────────────────────────────────────────────────

app = FastAPI(
    title="Media Swarm",
    description="AI-powered media company with 11 specialized agent teams",
    version="0.1.0",
)

# Include custom admin routes
app.include_router(health.router)
app.include_router(knowledge_admin.router)
app.include_router(reports.router)
app.include_router(agent_config.router)


@app.get("/")
async def root():
    return {
        "name": "Media Swarm",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "agent_ui": f"http://localhost:3000",
    }


# ─── AgentOS Integration ───────────────────────────────────────────────────
# Teams will be registered here as they are built.
# For now, we expose the custom admin API on its own.
#
# When teams are ready:
#   from agno.playground import Playground
#   playground = Playground(teams=[master_orchestrator, ...])
#   app.include_router(playground.get_router())


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting Media Swarm on {settings.agent_os_host}:{settings.agent_os_port}")
    uvicorn.run(
        "src.app:app",
        host=settings.agent_os_host,
        port=settings.agent_os_port,
        reload=True,
    )
