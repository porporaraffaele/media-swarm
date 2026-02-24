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

    try:
        from src.services.knowledge_loader import KnowledgeLoader

        loader = KnowledgeLoader()

        if file:
            file_data = await file.read()
            result = await loader.aload_file_bytes(
                agent_id=agent_id,
                data=file_data,
                filename=file.filename or "uploaded_file",
                title=title,
            )
        elif url:
            result = await loader.aload_url(agent_id=agent_id, url=url, title=title)
        else:
            result = await loader.aload_text(agent_id=agent_id, text=text_content, title=title)

        return {
            "status": result["status"],
            "document_id": result["document_id"],
            "agent_id": agent_id,
            "chunk_count": result["chunk_count"],
            "message": f"Document loaded into {agent_id} knowledge base.",
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
async def search_knowledge(agent_id: str, query: str = Form(...), max_results: int = 5):
    """Search an agent's knowledge base using semantic search."""
    if agent_id not in KB_TABLES:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' not found")

    try:
        from src.services.knowledge_loader import KnowledgeLoader

        loader = KnowledgeLoader()
        results = await loader.asearch(agent_id=agent_id, query=query, max_results=max_results)
        return {
            "agent_id": agent_id,
            "query": query,
            "results": results,
            "total": len(results),
        }
    except Exception as e:
        logger.error(f"Failed to search knowledge for {agent_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
