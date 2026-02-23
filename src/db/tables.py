"""Database table name registry and raw connection helpers for custom queries."""

import psycopg

from src.config.settings import settings

# Convert the agno-style URL to psycopg-compatible format
# agno uses: postgresql+psycopg://...
# psycopg uses: postgresql://...
RAW_DB_URL = settings.database_url.replace("postgresql+psycopg://", "postgresql://")


def get_connection() -> psycopg.Connection:
    """Get a raw psycopg connection for custom queries (reports, configs, etc.)."""
    return psycopg.connect(RAW_DB_URL)


# Table names for custom application tables
TABLE_REPORTS = "reports"
TABLE_IMPROVEMENTS = "improvement_suggestions"
TABLE_AGENT_CONFIGS = "agent_configs"
TABLE_KNOWLEDGE_DOCS = "knowledge_documents"
