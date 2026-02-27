/**
 * API client for Media Swarm FastAPI backend.
 *
 * All requests go through Next.js rewrite (localhost:3000/api/* → localhost:7777/*).
 * This avoids CORS issues and keeps the backend URL in one place.
 */

import type {
  Agent,
  AgentConfig,
  KnowledgeAgent,
  KnowledgeDocument,
  Project,
  ProjectSession,
  Report,
  ReportStats,
} from "./types";

const BASE = "/api";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json();
}

// ─── Health ─────────────────────────────────────────────────────────────────

export async function getHealth() {
  return fetchJSON<{ status: string }>(`${BASE}/admin/health`);
}

export async function getSystemInfo() {
  return fetchJSON<{
    name: string;
    version: string;
    status: string;
    teams: number;
    sub_agents: number;
  }>(`${BASE}/`);
}

// ─── Reports ────────────────────────────────────────────────────────────────

export async function getReports(params?: {
  team_id?: string;
  agent_id?: string;
  task_type?: string;
  min_quality?: number;
  limit?: number;
  offset?: number;
}) {
  const qs = new URLSearchParams();
  if (params?.team_id) qs.set("team_id", params.team_id);
  if (params?.agent_id) qs.set("agent_id", params.agent_id);
  if (params?.task_type) qs.set("task_type", params.task_type);
  if (params?.min_quality != null) qs.set("min_quality", String(params.min_quality));
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  return fetchJSON<{ reports: Report[]; total: number }>(`${BASE}/admin/reports?${qs}`);
}

export async function getReport(id: string) {
  return fetchJSON<Report>(`${BASE}/admin/reports/${id}`);
}

export async function getReportStats() {
  return fetchJSON<{ stats: ReportStats[] }>(`${BASE}/admin/reports/stats/summary`);
}

// ─── Agents ─────────────────────────────────────────────────────────────────

export async function getAgents() {
  return fetchJSON<{ agents: Agent[]; total: number }>(`${BASE}/admin/agents`);
}

export async function getAgentConfig(agentId: string) {
  return fetchJSON<AgentConfig>(`${BASE}/admin/agents/${agentId}/config`);
}

export async function updateAgentConfig(
  agentId: string,
  config: Partial<AgentConfig>
) {
  return fetchJSON<{ status: string }>(`${BASE}/admin/agents/${agentId}/config`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config),
  });
}

// ─── Knowledge ──────────────────────────────────────────────────────────────

export async function getKnowledgeAgents() {
  return fetchJSON<{ agents: KnowledgeAgent[]; total: number }>(
    `${BASE}/admin/knowledge/agents`
  );
}

export async function getAgentDocuments(agentId: string) {
  return fetchJSON<{ documents: KnowledgeDocument[] }>(
    `${BASE}/admin/knowledge/agents/${agentId}/documents`
  );
}

export async function uploadDocument(
  agentId: string,
  data: { url?: string; text_content?: string; title?: string; file?: File }
) {
  const formData = new FormData();
  if (data.url) formData.append("url", data.url);
  if (data.text_content) formData.append("text_content", data.text_content);
  if (data.title) formData.append("title", data.title);
  if (data.file) formData.append("file", data.file);
  return fetchJSON<{ status: string; document_id: string; chunk_count: number }>(
    `${BASE}/admin/knowledge/agents/${agentId}/documents`,
    { method: "POST", body: formData }
  );
}

export async function deleteDocument(agentId: string, docId: string) {
  return fetchJSON<{ status: string }>(
    `${BASE}/admin/knowledge/agents/${agentId}/documents/${docId}`,
    { method: "DELETE" }
  );
}

export async function searchKnowledge(agentId: string, query: string) {
  const formData = new FormData();
  formData.append("query", query);
  return fetchJSON<{ results: unknown[] }>(
    `${BASE}/admin/knowledge/agents/${agentId}/search`,
    { method: "POST", body: formData }
  );
}

// ─── Projects ───────────────────────────────────────────────────────────────

export async function getProjects(status = "active") {
  return fetchJSON<{ projects: Project[] }>(
    `${BASE}/admin/projects?status=${status}`
  );
}

export async function createProject(name: string, description?: string) {
  return fetchJSON<Project>(`${BASE}/admin/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, description }),
  });
}

export async function getProject(id: string) {
  return fetchJSON<Project>(`${BASE}/admin/projects/${id}`);
}

export async function updateProjectTeams(id: string, teamIds: string[]) {
  return fetchJSON<Project>(`${BASE}/admin/projects/${id}/teams`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ team_ids: teamIds }),
  });
}

export async function archiveProject(id: string) {
  return fetchJSON<{ status: string }>(`${BASE}/admin/projects/${id}`, {
    method: "DELETE",
  });
}

export async function getProjectSessions(id: string, limit = 20) {
  return fetchJSON<{ sessions: ProjectSession[] }>(
    `${BASE}/admin/projects/${id}/sessions?limit=${limit}`
  );
}

// ─── Team & Agent Run ───────────────────────────────────────────────────────

export async function runTeam(teamId: string, input: string) {
  return fetchJSON<{ content: string; team_id: string }>(
    `${BASE}/api/run/team/${teamId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input }),
    }
  );
}

export async function runAgent(agentId: string, input: string) {
  return fetchJSON<{ content: string; agent_id: string }>(
    `${BASE}/api/run/agent/${agentId}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input }),
    }
  );
}
