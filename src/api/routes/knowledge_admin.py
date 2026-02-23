"""Admin CRUD routes for managing per-agent RAG knowledge bases.

These routes allow adding, listing, and removing documents from any
sub-agent's isolated knowledge base via the admin API.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, UploadFile

from src.config.constants import KB_TABLES
from src.db.tables import get_connection

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/knowledge", tags=["Knowledge Admin"])


@router.get("/agents")
async def list_agents_with_knowledge():
    """List all agents and their knowledge base table names."""
    agents = [
        {"agent_id": agent_id, "table_name": table_name}
        for agent_id, table_name in KB_TABLES.items()
    ]
    return {"agents": agents, "total": len(agents)}


@router.get("/agents/{agent_id}/documents")
async def list_agent_documents(agent_id: str):
    """List all documents in a specific agent's knowledge base."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, source_type, source_path, title, description,
                           chunk_count, status, added_at
                    FROM knowledge_documents
                    WHERE agent_id = %s AND status != 'archived'
                    ORDER BY added_at DESC
                    """,
                    (agent_id,),
                )
                rows = cur.fetchall()
        documents = [
            {
                "id": str(row[0]),
                "source_type": row[1],
                "source_path": row[2],
                "title": row[3],
                "description": row[4],
                "chunk_count": row[5],
                "status": row[6],
                "added_at": row[7].isoformat() if row[7] else None,
            }
            for row in rows
        ]
        return {"agent_id": agent_id, "documents": documents, "total": len(documents)}
    except Exception as e:
        logger.error(f"Failed to list documents for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/documents")
async def add_document(
    agent_id: str,
    url: str | None = Form(None),
    text_content: str | None = Form(None),
    title: str | None = Form(None),
    description: str | None = Form(None),
    file: UploadFile | None = None,
):
    """Add a document to an agent's knowledge base.

    Provide one of: url, text_content, or file upload.
    The document will be registered in the knowledge_documents table
    and loaded into the agent's PgVector knowledge base.
    """
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    if not any([url, text_content, file]):
        raise HTTPException(
            status_code=400, detail="Provide at least one of: url, text_content, or file"
        )

    # Determine source type and path
    if file:
        source_type = "file"
        source_path = file.filename or "uploaded_file"
    elif url:
        source_type = "url"
        source_path = url
    else:
        source_type = "text"
        source_path = title or "inline_text"

    # Get team_id from agent_id prefix
    team_id = agent_id.rsplit("-", 1)[0] if "-" in agent_id else agent_id

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO knowledge_documents (
                        agent_id, team_id, table_name, source_type,
                        source_path, title, description, status
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'processing')
                    RETURNING id
                    """,
                    (
                        agent_id,
                        team_id,
                        KB_TABLES[agent_id],
                        source_type,
                        source_path,
                        title,
                        description,
                    ),
                )
                doc_id = cur.fetchone()[0]
            conn.commit()

        # TODO: Actually load the document into the PgVector knowledge base
        # This will be implemented when the knowledge loading pipeline is built.
        # For now, we register the document metadata.

        return {
            "status": "registered",
            "document_id": str(doc_id),
            "agent_id": agent_id,
            "message": "Document registered. Knowledge loading will be processed.",
        }
    except Exception as e:
        logger.error(f"Failed to add document for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/agents/{agent_id}/documents/{doc_id}")
async def remove_document(agent_id: str, doc_id: UUID):
    """Archive a document from an agent's knowledge base."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE knowledge_documents
                    SET status = 'archived', updated_at = NOW()
                    WHERE id = %s AND agent_id = %s
                    RETURNING id
                    """,
                    (str(doc_id), agent_id),
                )
                result = cur.fetchone()
            conn.commit()
        if not result:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"status": "archived", "document_id": str(doc_id)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to remove document {doc_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/agents/{agent_id}/search")
async def search_knowledge(agent_id: str, query: str = Form(...)):
    """Search an agent's knowledge base (placeholder for future implementation)."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    # TODO: Use the agent's Knowledge instance to perform semantic search
    return {
        "agent_id": agent_id,
        "query": query,
        "results": [],
        "message": "Search will be available once knowledge bases are populated.",
    }
