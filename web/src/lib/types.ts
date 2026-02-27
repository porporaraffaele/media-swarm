// ─── Team metadata (static, defined in frontend) ───────────────────────────

export interface TeamInfo {
  id: string;
  name: string;
  icon: string;
  role: string;
  agentCount: number;
  mode: string;
}

export const TEAMS: TeamInfo[] = [
  { id: "branding", name: "Branding", icon: "Palette", role: "Brand strategy, naming, visual identity, tone of voice", agentCount: 8, mode: "coordinate" },
  { id: "copywriting", name: "Copywriting", icon: "PenTool", role: "SEO copy, social media, email, ad copy, scripts, UX writing", agentCount: 7, mode: "coordinate" },
  { id: "graphic-design", name: "Graphic Design", icon: "Image", role: "Social graphics, templates, infographics, thumbnails, motion", agentCount: 6, mode: "coordinate" },
  { id: "competitors", name: "Competitors & Market", icon: "Target", role: "Competitive intelligence, SWOT, pricing, benchmarks, audience", agentCount: 6, mode: "tasks" },
  { id: "news", name: "News", icon: "Newspaper", role: "News aggregation, trend detection, fact-checking, alerts", agentCount: 6, mode: "tasks" },
  { id: "community", name: "Community", icon: "Users", role: "Engagement, UGC, growth hacking, influencer outreach, events", agentCount: 9, mode: "route" },
  { id: "content-ideation", name: "Content Ideation", icon: "Lightbulb", role: "Content ideas, hooks, formats, viral scoring, editorial calendar", agentCount: 6, mode: "coordinate" },
  { id: "content-finder", name: "Content Finder", icon: "Search", role: "Find content across social, web, and niche platforms", agentCount: 6, mode: "broadcast" },
  { id: "content-creator", name: "Content Creator", icon: "Video", role: "AI image and video generation with quality control", agentCount: 6, mode: "tasks" },
  { id: "analyst", name: "Analyst", icon: "BarChart3", role: "Performance analysis, quality auditing, self-improvement", agentCount: 9, mode: "tasks" },
  { id: "sales", name: "Sales & Leads", icon: "TrendingUp", role: "Lead generation, qualification, outreach, CRM", agentCount: 7, mode: "tasks" },
  { id: "ads-expert", name: "Ads Expert", icon: "Megaphone", role: "Paid advertising across all major platforms", agentCount: 8, mode: "tasks" },
  { id: "web-blog", name: "Web & Blog", icon: "Globe", role: "Website, blog, SEO, email marketing, analytics", agentCount: 8, mode: "tasks" },
  { id: "master-orchestrator", name: "Master Orchestrator", icon: "Brain", role: "Top-level coordinator for all teams", agentCount: 18, mode: "coordinate" },
];

export function getTeamById(id: string): TeamInfo | undefined {
  return TEAMS.find((t) => t.id === id);
}

// ─── API response types ────────────────────────────────────────────────────

export interface Agent {
  agent_id: string;
  team_id: string;
  enabled: boolean;
  has_custom_config: boolean;
  updated_at: string | null;
}

export interface AgentConfig {
  agent_id: string;
  team_id: string;
  custom_instructions: string[];
  temperature: number;
  max_tokens: number;
  enabled: boolean;
  metadata: Record<string, unknown>;
  has_custom_config: boolean;
  updated_at?: string | null;
}

export interface Report {
  id: string;
  team_id: string;
  agent_id: string;
  task_type: string;
  quality_score: number | null;
  tokens_used: number | null;
  cost_usd: number | null;
  execution_time_seconds: number | null;
  created_at: string | null;
  status: string | null;
  report_data?: Record<string, unknown>;
}

export interface ReportStats {
  team_id: string;
  total_reports: number;
  avg_quality: number;
  total_cost: number;
  total_tokens: number;
  avg_time_seconds: number;
}

export interface KnowledgeAgent {
  agent_id: string;
  table_name: string;
}

export interface KnowledgeDocument {
  id: string;
  source_type: string;
  source_path: string | null;
  title: string | null;
  description: string | null;
  chunk_count: number;
  status: string;
  added_at: string | null;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  team_ids: string[];
  status: string;
  created_at: string | null;
}

export interface ProjectSession {
  team_id: string | null;
  agent_id: string | null;
  prompt: string;
  response: string;
  created_at: string | null;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}
