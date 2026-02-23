"""Media Swarm - AgentOS Main Entrypoint.

Starts the FastAPI server with:
- All 11 agent teams registered via Agno Playground
- Custom admin routes for knowledge, reports, and agent configuration
- Agent UI frontend connects to this server at port 7777

Usage:
    uv run python -m src.app

Prerequisites:
    docker compose -f docker/docker-compose.yml up -d
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import agent_config, health, knowledge_admin, reports
from src.config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _register_playground(app: FastAPI) -> None:
    """Register all teams with Agno Playground for Agent UI connectivity.

    This creates Knowledge instances that connect to PostgreSQL,
    so the database must be running before this is called.
    """
    from agno.playground import Playground

    from src.agents.analyst.team import analyst_team
    from src.agents.branding.team import branding_team
    from src.agents.community.team import community_team
    from src.agents.competitors.team import competitors_team
    from src.agents.content_creator.team import content_creator_team
    from src.agents.content_finder.team import content_finder_team
    from src.agents.content_ideation.team import content_ideation_team
    from src.agents.copywriting.team import copywriting_team
    from src.agents.graphic_design.team import graphic_design_team
    from src.agents.master_orchestrator.team import master_orchestrator
    from src.agents.news.team import news_team

    playground = Playground(
        teams=[
            master_orchestrator,
            branding_team,
            copywriting_team,
            graphic_design_team,
            competitors_team,
            news_team,
            community_team,
            content_ideation_team,
            content_finder_team,
            content_creator_team,
            analyst_team,
        ],
    )

    app.include_router(playground.get_router())
    logger.info("Playground registered with 11 teams (73 sub-agents)")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: register teams on startup."""
    logger.info("Starting Media Swarm...")
    try:
        _register_playground(app)
        logger.info(
            "Media Swarm ready at http://%s:%s",
            settings.agent_os_host,
            settings.agent_os_port,
        )
    except Exception:
        logger.exception(
            "Failed to register teams. Is PostgreSQL running? "
            "Run: docker compose -f docker/docker-compose.yml up -d"
        )
        raise
    yield
    logger.info("Shutting down Media Swarm...")


# ─── FastAPI App ────────────────────────────────────────────────────────────

app = FastAPI(
    title="Media Swarm",
    description="AI-powered media company with 11 specialized agent teams",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for Agent UI (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        "teams": 11,
        "sub_agents": 73,
        "docs": "/docs",
        "agent_ui": "http://localhost:3000",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host=settings.agent_os_host,
        port=settings.agent_os_port,
        reload=True,
    )
