"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { BarChart3, FileText, Star } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getReports, getReportStats, getReport } from "@/lib/api";
import { TEAMS, type Report, type ReportStats } from "@/lib/types";

export default function ReportsPageWrapper() {
  return (
    <Suspense fallback={<div className="text-muted-foreground p-8">Loading reports...</div>}>
      <ReportsPage />
    </Suspense>
  );
}

function ReportsPage() {
  const searchParams = useSearchParams();
  const initialTeam = searchParams.get("team_id");

  const [reports, setReports] = useState<Report[]>([]);
  const [stats, setStats] = useState<ReportStats[]>([]);
  const [total, setTotal] = useState(0);
  const [teamFilter, setTeamFilter] = useState<string | null>(initialTeam);
  const [page, setPage] = useState(0);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [loading, setLoading] = useState(true);
  const LIMIT = 20;

  const loadReports = async () => {
    setLoading(true);
    try {
      const params: { team_id?: string; limit: number; offset: number } = {
        limit: LIMIT,
        offset: page * LIMIT,
      };
      if (teamFilter) params.team_id = teamFilter;

      const [reportsData, statsData] = await Promise.all([
        getReports(params),
        getReportStats(),
      ]);
      setReports(reportsData.reports);
      setTotal(reportsData.total);
      setStats(statsData.stats);
    } catch {
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, [teamFilter, page]);

  const viewReport = async (id: string) => {
    try {
      const full = await getReport(id);
      setSelectedReport(full);
    } catch {}
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Reports</h2>
        <p className="text-muted-foreground">{total} total reports across all agents</p>
      </div>

      {/* Stats Summary */}
      <div className="grid gap-3 md:grid-cols-4 lg:grid-cols-7">
        {stats.slice(0, 7).map((s) => {
          const team = TEAMS.find((t) => t.id === s.team_id);
          return (
            <Card
              key={s.team_id}
              className={`cursor-pointer transition-all ${teamFilter === s.team_id ? "ring-2 ring-primary" : ""}`}
              onClick={() => setTeamFilter(teamFilter === s.team_id ? null : s.team_id)}
            >
              <CardContent className="p-3">
                <p className="text-xs font-medium truncate">{team?.name || s.team_id}</p>
                <p className="text-lg font-bold">{s.total_reports}</p>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                  <Star className="h-3 w-3" />
                  {s.avg_quality.toFixed(1)}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Filter Chips */}
      <div className="flex gap-1.5 flex-wrap">
        <Button
          size="sm"
          variant={teamFilter === null ? "default" : "outline"}
          onClick={() => { setTeamFilter(null); setPage(0); }}
        >
          All
        </Button>
        {stats.map((s) => {
          const team = TEAMS.find((t) => t.id === s.team_id);
          return (
            <Button
              key={s.team_id}
              size="sm"
              variant={teamFilter === s.team_id ? "default" : "outline"}
              onClick={() => { setTeamFilter(s.team_id); setPage(0); }}
            >
              {team?.name || s.team_id}
            </Button>
          );
        })}
      </div>

      {/* Reports Table */}
      <Card>
        <CardContent className="p-0">
          {loading ? (
            <div className="p-8 text-center text-muted-foreground">Loading...</div>
          ) : reports.length === 0 ? (
            <div className="p-8 text-center text-muted-foreground">
              No reports found. Run a team or agent to generate reports.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b bg-muted/50">
                    <th className="text-left p-3 font-medium">Agent</th>
                    <th className="text-left p-3 font-medium">Team</th>
                    <th className="text-left p-3 font-medium">Type</th>
                    <th className="text-right p-3 font-medium">Quality</th>
                    <th className="text-right p-3 font-medium">Cost</th>
                    <th className="text-right p-3 font-medium">Time</th>
                    <th className="text-left p-3 font-medium">Date</th>
                    <th className="p-3"></th>
                  </tr>
                </thead>
                <tbody>
                  {reports.map((r) => (
                    <tr key={r.id} className="border-b hover:bg-muted/30 transition-colors">
                      <td className="p-3 font-medium">{r.agent_id}</td>
                      <td className="p-3">
                        <Badge variant="secondary" className="text-xs">
                          {TEAMS.find((t) => t.id === r.team_id)?.name || r.team_id}
                        </Badge>
                      </td>
                      <td className="p-3 text-muted-foreground">{r.task_type || "-"}</td>
                      <td className="p-3 text-right">
                        {r.quality_score != null ? (
                          <span className={r.quality_score >= 7 ? "text-green-600" : r.quality_score >= 5 ? "text-yellow-600" : "text-red-600"}>
                            {r.quality_score}/10
                          </span>
                        ) : "-"}
                      </td>
                      <td className="p-3 text-right text-muted-foreground">
                        {r.cost_usd != null ? `$${r.cost_usd.toFixed(4)}` : "-"}
                      </td>
                      <td className="p-3 text-right text-muted-foreground">
                        {r.execution_time_seconds != null ? `${r.execution_time_seconds.toFixed(1)}s` : "-"}
                      </td>
                      <td className="p-3 text-muted-foreground text-xs">
                        {r.created_at ? new Date(r.created_at).toLocaleString() : "-"}
                      </td>
                      <td className="p-3">
                        <Button size="sm" variant="ghost" onClick={() => viewReport(r.id)}>
                          View
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Pagination */}
      {total > LIMIT && (
        <div className="flex justify-center gap-2">
          <Button
            variant="outline"
            size="sm"
            disabled={page === 0}
            onClick={() => setPage((p) => p - 1)}
          >
            Previous
          </Button>
          <span className="text-sm text-muted-foreground py-2">
            Page {page + 1} of {Math.ceil(total / LIMIT)}
          </span>
          <Button
            variant="outline"
            size="sm"
            disabled={(page + 1) * LIMIT >= total}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </Button>
        </div>
      )}

      {/* Report Detail Modal */}
      {selectedReport && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Report Detail: {selectedReport.agent_id}
              </CardTitle>
              <Button variant="ghost" size="sm" onClick={() => setSelectedReport(null)}>
                Close
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <pre className="bg-muted rounded-lg p-4 text-xs overflow-auto max-h-96">
              {JSON.stringify(selectedReport.report_data || selectedReport, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
