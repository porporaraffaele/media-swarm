"""Shared database connection for all agents and teams."""

from agno.storage.postgres import PostgresStorage

from src.config.settings import settings

# Shared storage instance for agent/team sessions and memory
storage = PostgresStorage(table_name="agent_sessions", db_url=settings.database_url)
