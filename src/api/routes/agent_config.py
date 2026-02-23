"""Admin routes for dynamic agent configuration."""

import json
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from src.config.constants import KB_TABLES
from src.db.tables import get_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/agents", tags=["Agent Config"])


class AgentConfigUpdate(BaseModel):
    """Request body for updating agent configuration."""

    custom_instructions: list[str] | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, ge=100, le=16384)
    enabled: bool | None = None
    metadata: dict | None = None


@router.get("")
async def list_agents():
    """List all registered agents with their configuration status."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT agent_id, team_id, enabled, updated_at FROM agent_configs")
                rows = cur.fetchall()

        configured = {row[0]: row for row in rows}
        agents = []
        for agent_id in KB_TABLES:
            team_id = agent_id.rsplit("-", 1)[0] if "-" in agent_id else agent_id
            if agent_id in configured:
                row = configured[agent_id]
                agents.append(
                    {
                        "agent_id": agent_id,
                        "team_id": row[1],
                        "enabled": row[2],
                        "has_custom_config": True,
                        "updated_at": row[3].isoformat() if row[3] else None,
                    }
                )
            else:
                agents.append(
                    {
                        "agent_id": agent_id,
                        "team_id": team_id,
                        "enabled": True,
                        "has_custom_config": False,
                        "updated_at": None,
                    }
                )
        return {"agents": agents, "total": len(agents)}
    except Exception as e:
        logger.error(f"Failed to list agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{agent_id}/config")
async def get_agent_config(agent_id: str):
    """Get configuration for a specific agent."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT agent_id, team_id, custom_instructions, temperature,
                           max_tokens, enabled, metadata, updated_at
                    FROM agent_configs WHERE agent_id = %s
                    """,
                    (agent_id,),
                )
                row = cur.fetchone()
        if not row:
            return {
                "agent_id": agent_id,
                "team_id": agent_id.rsplit("-", 1)[0],
                "custom_instructions": [],
                "temperature": 0.7,
                "max_tokens": 4096,
                "enabled": True,
                "metadata": {},
                "has_custom_config": False,
            }
        return {
            "agent_id": row[0],
            "team_id": row[1],
            "custom_instructions": row[2] or [],
            "temperature": row[3],
            "max_tokens": row[4],
            "enabled": row[5],
            "metadata": row[6] or {},
            "has_custom_config": True,
            "updated_at": row[7].isoformat() if row[7] else None,
        }
    except Exception as e:
        logger.error(f"Failed to get config for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{agent_id}/config")
async def update_agent_config(agent_id: str, config: AgentConfigUpdate):
    """Update configuration for a specific agent."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    team_id = agent_id.rsplit("-", 1)[0] if "-" in agent_id else agent_id

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO agent_configs (agent_id, team_id, custom_instructions,
                        temperature, max_tokens, enabled, metadata, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, NOW())
                    ON CONFLICT (agent_id) DO UPDATE SET
                        custom_instructions = COALESCE(%s, agent_configs.custom_instructions),
                        temperature = COALESCE(%s, agent_configs.temperature),
                        max_tokens = COALESCE(%s, agent_configs.max_tokens),
                        enabled = COALESCE(%s, agent_configs.enabled),
                        metadata = COALESCE(%s::jsonb, agent_configs.metadata),
                        updated_at = NOW()
                    RETURNING agent_id
                    """,
                    (
                        agent_id,
                        team_id,
                        config.custom_instructions,
                        config.temperature or 0.7,
                        config.max_tokens or 4096,
                        config.enabled if config.enabled is not None else True,
                        json.dumps(config.metadata) if config.metadata else "{}",
                        config.custom_instructions,
                        config.temperature,
                        config.max_tokens,
                        config.enabled,
                        json.dumps(config.metadata) if config.metadata else None,
                    ),
                )
            conn.commit()
        return {"status": "updated", "agent_id": agent_id}
    except Exception as e:
        logger.error(f"Failed to update config for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
