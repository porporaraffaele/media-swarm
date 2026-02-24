-- Media Swarm - Migration v2
-- Run this on an existing DB to add new tables and constraints.
-- PowerShell: Get-Content docker/pgvector/migrate_v2.sql | docker exec -i media-swarm-pgvector psql -U ai -d ai

-- Extend knowledge_documents constraints
ALTER TABLE knowledge_documents DROP CONSTRAINT IF EXISTS knowledge_documents_source_type_check;
ALTER TABLE knowledge_documents ADD CONSTRAINT knowledge_documents_source_type_check
    CHECK (source_type IN ('pdf', 'url', 'text', 'file', 'directory', 'docx', 'csv', 'loaded'));

ALTER TABLE knowledge_documents DROP CONSTRAINT IF EXISTS knowledge_documents_status_check;
ALTER TABLE knowledge_documents ADD CONSTRAINT knowledge_documents_status_check
    CHECK (status IN ('active', 'archived', 'processing', 'error', 'loaded'));

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    team_ids TEXT[] DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'completed')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_created ON projects(created_at);

-- Project sessions table
CREATE TABLE IF NOT EXISTS project_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    team_id VARCHAR(100),
    agent_id VARCHAR(100),
    prompt TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_project_sessions_project ON project_sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_project_sessions_created ON project_sessions(created_at);
