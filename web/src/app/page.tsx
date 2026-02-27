"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  BarChart3,
  DollarSign,
  FileText,
  MessageSquare,
  Star,
  Users,
  Zap,
  FolderKanban,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { getReportStats, getReports, getSystemInfo } from "@/lib/api";
import type { Report, ReportStats } from "@/lib/types";
import { TEAMS } from "@/lib/types";

export default function DashboardPage() {
  const [stats, setStats] = useState<ReportStats[]>([]);
  const [recentReports, setRecentReports] = useState<Report[]>([]);
  const [systemInfo, setSystemInfo] = useState<{ teams: number; sub_agents: number; version: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      getReportStats().catch(() => ({ stats: [] })),
      getReports({ limit: 8 }).catch(() => ({ reports: [] })),
      getSystemInfo().catch(() => null),
    ]).then(([s, r, info]) => {
      setStats(s.stats);
      setRecentReports(r.reports);
      setSystemInfo(info);
    }).catch((e) => setError(e.message));
  }, []);

  const totalReports = stats.reduce((a, s) => a + s.total_reports, 0);
  const totalCost = stats.reduce((a, s) => a + s.total_cost, 0);
  const avgQuality = stats.length > 0
    ? stats.reduce((a, s) => a + s.avg_quality, 0) / stats.length
    : 0;
  const totalTokens = stats.reduce((a, s) => a + s.total_tokens, 0);

  return (
    <div className="space-y-6">
      {error && (
        <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          Backend not reachable: {error}. Make sure the FastAPI server is running on port 7777.
        </div>
      )}

      {/* Quick Actions */}
      <div className="flex gap-3">
        <Link href="/chat">
          <Button className="gap-2">
            <MessageSquare className="h-4 w-4" />
            Chat with Master Orchestrator
          </Button>
        </Link>
        <Link href="/projects">
          <Button variant="outline" className="gap-2">
            <FolderKanban className="h-4 w-4" />
            New Project
          </Button>
        </Link>
      </div>

      {/* Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reports</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalReports}</div>
            <p className="text-xs text-muted-foreground">across {stats.length} teams</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg Quality</CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgQuality.toFixed(1)}/10</div>
            <p className="text-xs text-muted-foreground">self-evaluated score</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalCost.toFixed(4)}</div>
            <p className="text-xs text-muted-foreground">API usage</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tokens Used</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{(totalTokens / 1000).toFixed(0)}K</div>
            <p className="text-xs text-muted-foreground">total tokens</p>
          </CardContent>
        </Card>
      </div>

      {/* Team Stats + Recent Reports */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Team Performance */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5" />
              Team Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            {stats.length === 0 ? (
              <p className="text-sm text-muted-foreground">No reports yet. Run a team to see data here.</p>
            ) : (
              <div className="space-y-3">
                {stats.map((s) => {
                  const team = TEAMS.find((t) => t.id === s.team_id);
                  return (
                    <div key={s.team_id} className="flex items-center justify-between text-sm">
                      <span className="font-medium">{team?.name || s.team_id}</span>
                      <div className="flex items-center gap-4">
                        <Badge variant="secondary">{s.total_reports} reports</Badge>
                        <span className="text-muted-foreground w-14 text-right">
                          {s.avg_quality.toFixed(1)}/10
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recentReports.length === 0 ? (
              <p className="text-sm text-muted-foreground">No activity yet. Start a chat to see reports here.</p>
            ) : (
              <div className="space-y-3">
                {recentReports.map((r) => (
                  <div key={r.id} className="flex items-center justify-between text-sm">
                    <div>
                      <span className="font-medium">{r.agent_id}</span>
                      <span className="text-muted-foreground ml-2">{r.task_type || "task"}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">
                      {r.created_at ? new Date(r.created_at).toLocaleString() : ""}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
