"""Knowledge loading service for ingesting documents into per-agent RAG.

Supports: PDF, DOCX, CSV, TXT files, URLs, and inline text.
Each document is loaded into the correct agent's PgVector table
and registered in the knowledge_documents tracking table.
"""

import logging
import tempfile
from pathlib import Path

from src.config.constants import KB_TABLES
from src.db.tables import get_connection
from src.knowledge.factory import create_agent_knowledge

logger = logging.getLogger(__name__)


class KnowledgeLoader:
    """Load documents into agent knowledge bases."""

    def load_url(self, agent_id: str, url: str, title: str | None = None) -> dict:
        """Load a URL into an agent's knowledge base.

        Args:
            agent_id: Target agent ID (must exist in KB_TABLES).
            url: The URL to crawl and load.
            title: Optional title for the document.

        Returns:
            Dict with status, doc_id, and chunk_count.
        """
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        logger.info("Loading URL '%s' into %s", url, agent_id)
        kb.insert(url=url, name=title)

        # Count chunks loaded
        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type="url",
            source_path=url,
            title=title or url,
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    def load_text(self, agent_id: str, text: str, title: str | None = None) -> dict:
        """Load inline text into an agent's knowledge base."""
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        logger.info("Loading text (%d chars) into %s", len(text), agent_id)
        kb.insert(text_content=text, name=title or "inline_text")

        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type="text",
            source_path=title or "inline_text",
            title=title or "Inline Text",
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    def load_file(self, agent_id: str, file_path: str, title: str | None = None) -> dict:
        """Load a file (PDF, DOCX, CSV, TXT) into an agent's knowledge base.

        Args:
            agent_id: Target agent ID.
            file_path: Path to the file to load.
            title: Optional title override.

        Returns:
            Dict with status, doc_id, and chunk_count.
        """
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        source_type = self._ext_to_source_type(ext)

        logger.info("Loading %s file '%s' into %s", source_type, path.name, agent_id)
        kb.insert(path=str(path), name=title or path.stem)

        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type=source_type,
            source_path=str(path),
            title=title or path.name,
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    def load_file_bytes(
        self, agent_id: str, data: bytes, filename: str, title: str | None = None
    ) -> dict:
        """Load file bytes (from Telegram upload) into an agent's knowledge base.

        Writes bytes to a temp file, then loads via the standard path.
        """
        ext = Path(filename).suffix.lower()
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            return self.load_file(agent_id, tmp_path, title=title or filename)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    async def aload_url(self, agent_id: str, url: str, title: str | None = None) -> dict:
        """Async version of load_url."""
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        logger.info("Loading URL '%s' into %s (async)", url, agent_id)
        await kb.ainsert(url=url, name=title)

        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type="url",
            source_path=url,
            title=title or url,
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    async def aload_text(self, agent_id: str, text: str, title: str | None = None) -> dict:
        """Async version of load_text."""
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        logger.info("Loading text (%d chars) into %s (async)", len(text), agent_id)
        await kb.ainsert(text_content=text, name=title or "inline_text")

        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type="text",
            source_path=title or "inline_text",
            title=title or "Inline Text",
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    async def aload_file(self, agent_id: str, file_path: str, title: str | None = None) -> dict:
        """Async version of load_file."""
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        source_type = self._ext_to_source_type(path.suffix.lower())

        logger.info("Loading %s file '%s' into %s (async)", source_type, path.name, agent_id)
        await kb.ainsert(path=str(path), name=title or path.stem)

        chunk_count = self._count_chunks(agent_id)
        doc_id = self._register_document(
            agent_id=agent_id,
            source_type=source_type,
            source_path=str(path),
            title=title or path.name,
            chunk_count=chunk_count,
        )
        return {"status": "loaded", "document_id": doc_id, "chunk_count": chunk_count}

    async def aload_file_bytes(
        self, agent_id: str, data: bytes, filename: str, title: str | None = None
    ) -> dict:
        """Async version of load_file_bytes."""
        ext = Path(filename).suffix.lower()
        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            return await self.aload_file(agent_id, tmp_path, title=title or filename)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def search(self, agent_id: str, query: str, max_results: int = 5) -> list[dict]:
        """Search an agent's knowledge base.

        Args:
            agent_id: Target agent ID.
            query: Search query string.
            max_results: Maximum number of results.

        Returns:
            List of dicts with 'content', 'name', and 'meta_data'.
        """
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        docs = kb.search(query=query, max_results=max_results)
        return [
            {
                "content": doc.content[:500] if doc.content else "",
                "name": doc.name or "",
                "meta_data": doc.meta_data or {},
            }
            for doc in docs
        ]

    async def asearch(self, agent_id: str, query: str, max_results: int = 5) -> list[dict]:
        """Async version of search."""
        self._validate_agent(agent_id)
        kb = create_agent_knowledge(agent_id)

        docs = await kb.asearch(query=query, max_results=max_results)
        return [
            {
                "content": doc.content[:500] if doc.content else "",
                "name": doc.name or "",
                "meta_data": doc.meta_data or {},
            }
            for doc in docs
        ]

    # ─── Internal helpers ─────────────────────────────────────────────────

    @staticmethod
    def _validate_agent(agent_id: str) -> None:
        if agent_id not in KB_TABLES:
            raise ValueError(
                f"Unknown agent ID: '{agent_id}'. Valid: {', '.join(sorted(KB_TABLES.keys()))}"
            )

    @staticmethod
    def _ext_to_source_type(ext: str) -> str:
        return {
            ".pdf": "pdf",
            ".docx": "docx",
            ".doc": "docx",
            ".csv": "csv",
            ".txt": "text",
            ".md": "text",
            ".json": "text",
        }.get(ext, "file")

    @staticmethod
    def _count_chunks(agent_id: str) -> int:
        """Count total rows in the agent's PgVector table."""
        table = KB_TABLES[agent_id]
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")  # noqa: S608
                    row = cur.fetchone()
                    return row[0] if row else 0
        except Exception:
            logger.warning("Could not count chunks in %s", table)
            return -1

    @staticmethod
    def _register_document(
        agent_id: str,
        source_type: str,
        source_path: str,
        title: str,
        chunk_count: int,
    ) -> str:
        """Register document metadata in the knowledge_documents table."""
        team_id = agent_id.rsplit("-", 1)[0] if "-" in agent_id else agent_id
        table_name = KB_TABLES[agent_id]

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO knowledge_documents (
                            agent_id, team_id, table_name, source_type,
                            source_path, title, chunk_count, status
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'loaded')
                        RETURNING id
                        """,
                        (
                            agent_id,
                            team_id,
                            table_name,
                            source_type,
                            source_path,
                            title,
                            chunk_count,
                        ),
                    )
                    doc_id = cur.fetchone()[0]
                conn.commit()
            return str(doc_id)
        except Exception:
            logger.exception("Failed to register document for %s", agent_id)
            return "unknown"
