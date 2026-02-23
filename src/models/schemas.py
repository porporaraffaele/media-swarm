"""Shared Pydantic schemas used across multiple agents and API routes."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ContentItem(BaseModel):
    """A piece of content found or created by agents."""

    title: str
    url: str = ""
    platform: str = ""
    content_type: str = ""  # article, video, image, post
    description: str = ""
    relevance_score: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)


class KnowledgeDocumentInfo(BaseModel):
    """Information about a document in an agent's knowledge base."""

    id: UUID
    agent_id: str
    team_id: str
    table_name: str
    source_type: str
    source_path: str
    title: str | None = None
    description: str | None = None
    chunk_count: int = 0
    status: str = "active"
    added_at: datetime


class AgentConfigInfo(BaseModel):
    """Agent configuration for the admin API."""

    agent_id: str
    team_id: str
    custom_instructions: list[str] = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 4096
    enabled: bool = True
    metadata: dict = Field(default_factory=dict)


class ImprovementSuggestion(BaseModel):
    """An improvement suggestion from the Analyst team."""

    id: UUID
    source_report_ids: list[UUID]
    target_team_id: str
    target_agent_id: str | None = None
    suggestion_type: str  # instruction, knowledge, tool, workflow
    suggestion_data: dict
    status: str = "pending"
    created_at: datetime
