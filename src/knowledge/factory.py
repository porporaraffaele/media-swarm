"""Knowledge base factory for creating per-agent RAG instances.

Each sub-agent gets its own isolated PgVector table for domain-specific knowledge.
Documents are loaded via the admin API or programmatically at startup.
"""

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType

from src.config.constants import get_kb_table
from src.config.settings import settings
from src.knowledge.embedder import get_embedder


def create_agent_knowledge(
    agent_id: str,
    search_type: SearchType = SearchType.hybrid,
) -> Knowledge:
    """Create a Knowledge instance for a specific sub-agent.

    Args:
        agent_id: The agent ID (must exist in KB_TABLES constants).
        search_type: Vector search strategy (hybrid, similarity, keyword).

    Returns:
        Knowledge instance with its own isolated PgVector table.
    """
    table_name = get_kb_table(agent_id)
    return Knowledge(
        vector_db=PgVector(
            table_name=table_name,
            db_url=settings.database_url,
            search_type=search_type,
            embedder=get_embedder(),
        ),
    )
