"""Media Swarm - AgentOS Main Entrypoint.

Starts the FastAPI server with:
- All 11 agent teams registered via Agno AgentOS
- Custom admin routes for knowledge, reports, and agent configuration
- Agent UI frontend connects to this server at port 7777

Usage:
    uv run python -m src.app

Prerequisites:
    docker compose -f docker/docker-compose.yml up -d
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


def _create_app() -> FastAPI:
    """Create the full Media Swarm application.

    1. Creates a base FastAPI app with custom admin routes
    2. Imports all 11 teams (requires PostgreSQL running)
    3. Wraps everything in AgentOS which provides team/agent/session routes
    4. Returns the combined FastAPI app
    """
    from agno.os import AgentOS

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
    from src.db.connection import db

    # Base app with custom admin routes
    base_app = FastAPI(
        title="Media Swarm",
        description="AI-powered media company with 11 specialized agent teams",
        version="0.1.0",
    )
    base_app.include_router(health.router)
    base_app.include_router(knowledge_admin.router)
    base_app.include_router(reports.router)
    base_app.include_router(agent_config.router)

    @base_app.get("/")
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

    # AgentOS wraps the base app and adds team/agent/session routes
    agent_os = AgentOS(
        name="Media Swarm",
        description="AI-powered media company with 11 specialized agent teams",
        version="0.1.0",
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
        db=db,
        base_app=base_app,
        cors_allowed_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
    )

    logger.info("AgentOS initialized with 11 teams (73 sub-agents)")
    return agent_os.get_app()


# Create the app - requires PostgreSQL to be running
try:
    app = _create_app()
except Exception:
    logger.exception(
        "Failed to create app. Is PostgreSQL running? "
        "Run: docker compose -f docker/docker-compose.yml up -d"
    )
    raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host=settings.agent_os_host,
        port=settings.agent_os_port,
        reload=True,
    )
