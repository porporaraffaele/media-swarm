"""Shared database connection for all agents and teams."""

from agno.db.postgres import PostgresDb

from src.config.settings import settings

# Shared database instance for agent/team sessions and memory
db = PostgresDb(db_url=settings.database_url)
