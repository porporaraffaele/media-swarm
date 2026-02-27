"""API routes for running teams and agents via the web UI."""

import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/run", tags=["Run"])


class RunRequest(BaseModel):
    input: str


def _extract_text(response) -> str:
    """Extract text from an agno RunResponse."""
    if response is None:
        return "No response."
    if hasattr(response, "content") and response.content:
        return str(response.content)
    if hasattr(response, "messages") and response.messages:
        for msg in reversed(response.messages):
            if hasattr(msg, "content") and msg.content:
                return str(msg.content)
    return str(response)


# ─── Team endpoints ──────────────────────────────────────────────────────────

TEAM_REGISTRY: dict[str, str] = {
    "branding": "src.agents.branding.team:branding_team",
    "copywriting": "src.agents.copywriting.team:copywriting_team",
    "graphic-design": "src.agents.graphic_design.team:graphic_design_team",
    "competitors": "src.agents.competitors.team:competitors_team",
    "news": "src.agents.news.team:news_team",
    "community": "src.agents.community.team:community_team",
    "content-ideation": "src.agents.content_ideation.team:content_ideation_team",
    "content-finder": "src.agents.content_finder.team:content_finder_team",
    "content-creator": "src.agents.content_creator.team:content_creator_team",
    "analyst": "src.agents.analyst.team:analyst_team",
    "sales": "src.agents.sales.team:sales_team",
    "ads-expert": "src.agents.ads_expert.team:ads_expert_team",
    "web-blog": "src.agents.web_blog.team:web_blog_team",
    "master-orchestrator": "src.agents.master_orchestrator.team:master_orchestrator",
}


def _import_team(team_id: str):
    """Lazy import a team object."""
    path = TEAM_REGISTRY.get(team_id)
    if not path:
        raise HTTPException(status_code=404, detail=f"Team '{team_id}' not found")
    module_path, attr_name = path.rsplit(":", 1)
    import importlib

    mod = importlib.import_module(module_path)
    return getattr(mod, attr_name)


@router.post("/team/{team_id}")
async def run_team(team_id: str, body: RunRequest):
    """Run a team with user input."""
    try:
        team = _import_team(team_id)
        response = await team.arun(input=body.input)
        content = _extract_text(response)
        return {"content": content, "team_id": team_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error running team %s", team_id)
        raise HTTPException(status_code=500, detail=str(e))


# ─── Agent endpoints ─────────────────────────────────────────────────────────


# Import agent registry from telegram handlers (same lazy-import pattern)
def _import_agent(agent_id: str):
    """Lazy import an agent object."""
    from src.telegram.agent_handlers import AGENT_REGISTRY

    path = AGENT_REGISTRY.get(agent_id)
    if not path:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    module_path, attr_name = path.rsplit(":", 1)
    import importlib

    mod = importlib.import_module(module_path)
    return getattr(mod, attr_name)


@router.post("/agent/{agent_id}")
async def run_agent(agent_id: str, body: RunRequest):
    """Run an individual agent with user input."""
    try:
        agent = _import_agent(agent_id)
        response = await agent.arun(input=body.input)
        content = _extract_text(response)
        return {"content": content, "agent_id": agent_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error running agent %s", agent_id)
        raise HTTPException(status_code=500, detail=str(e))
