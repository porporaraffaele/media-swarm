-- Media Swarm - Custom Tables
-- These tables extend the Agno-managed tables (agent_sessions, team_sessions, kb_* vector tables)

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Reports: stores every micro-task report from every sub-agent
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id VARCHAR(100) NOT NULL,
    agent_id VARCHAR(100) NOT NULL,
    task_type VARCHAR(200) NOT NULL,
    report_data JSONB NOT NULL,
    quality_score FLOAT,
    tokens_used INTEGER,
    cost_usd FLOAT,
    execution_time_seconds FLOAT,
    session_id VARCHAR(200),
    user_id VARCHAR(200),
    parent_report_id UUID REFERENCES reports(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_reports_team ON reports(team_id);
CREATE INDEX idx_reports_agent ON reports(agent_id);
CREATE INDEX idx_reports_created ON reports(created_at);
CREATE INDEX idx_reports_task_type ON reports(task_type);
CREATE INDEX idx_reports_quality ON reports(quality_score);

-- Improvement suggestions from the Analyst team
CREATE TABLE IF NOT EXISTS improvement_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_report_ids UUID[] NOT NULL,
    target_team_id VARCHAR(100) NOT NULL,
    target_agent_id VARCHAR(100),
    suggestion_type VARCHAR(50) NOT NULL CHECK (suggestion_type IN ('instruction', 'knowledge', 'tool', 'workflow')),
    suggestion_data JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'applied', 'rejected', 'reviewing')),
    applied_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_improvements_target_team ON improvement_suggestions(target_team_id);
CREATE INDEX idx_improvements_status ON improvement_suggestions(status);
CREATE INDEX idx_improvements_created ON improvement_suggestions(created_at);

-- Agent configuration overrides (dynamic config beyond code)
CREATE TABLE IF NOT EXISTS agent_configs (
    agent_id VARCHAR(100) PRIMARY KEY,
    team_id VARCHAR(100) NOT NULL,
    custom_instructions TEXT[],
    temperature FLOAT DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 4096,
    enabled BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}',
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agent_configs_team ON agent_configs(team_id);

-- Knowledge document registry (tracks what docs are in which agent's RAG)
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(100) NOT NULL,
    team_id VARCHAR(100) NOT NULL,
    table_name VARCHAR(200) NOT NULL,
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('pdf', 'url', 'text', 'file', 'directory')),
    source_path TEXT NOT NULL,
    title VARCHAR(500),
    description TEXT,
    chunk_count INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'processing', 'error')),
    added_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_knowledge_docs_agent ON knowledge_documents(agent_id);
CREATE INDEX idx_knowledge_docs_team ON knowledge_documents(team_id);
CREATE INDEX idx_knowledge_docs_status ON knowledge_documents(status);
