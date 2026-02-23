"""Embedder configuration for RAG knowledge bases.

Uses OpenAI's text-embedding-3-small for vector embeddings.
Anthropic does not provide native embeddings through Agno,
so OpenAI is the recommended choice for quality/cost ratio.

Requires OPENAI_API_KEY in environment.
"""

from agno.knowledge.embedder.openai import OpenAIEmbedder


def get_embedder() -> OpenAIEmbedder:
    """Get the shared embedder instance for all knowledge bases."""
    return OpenAIEmbedder(id="text-embedding-3-small")
