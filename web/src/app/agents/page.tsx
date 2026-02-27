"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Bot, MessageSquare, Search } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { getAgents } from "@/lib/api";
import { TEAMS, type Agent } from "@/lib/types";

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [search, setSearch] = useState("");
  const [teamFilter, setTeamFilter] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAgents()
      .then((data) => setAgents(data.agents))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = agents.filter((a) => {
    if (teamFilter && a.team_id !== teamFilter) return false;
    if (search && !a.agent_id.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  const teamCounts = agents.reduce<Record<string, number>>((acc, a) => {
    acc[a.team_id] = (acc[a.team_id] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Agents</h2>
        <p className="text-muted-foreground">{agents.length} agents across {Object.keys(teamCounts).length} teams</p>
      </div>

      {/* Filters */}
      <div className="flex gap-3 items-center">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search agents..."
            className="pl-9"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex gap-1.5 flex-wrap">
          <Button
            size="sm"
            variant={teamFilter === null ? "default" : "outline"}
            onClick={() => setTeamFilter(null)}
          >
            All
          </Button>
          {Object.keys(teamCounts).sort().map((tid) => {
            const team = TEAMS.find((t) => t.id === tid);
            return (
              <Button
                key={tid}
                size="sm"
                variant={teamFilter === tid ? "default" : "outline"}
                onClick={() => setTeamFilter(tid)}
              >
                {team?.name || tid} ({teamCounts[tid]})
              </Button>
            );
          })}
        </div>
      </div>

      {/* Agent Grid */}
      {loading ? (
        <p className="text-muted-foreground">Loading agents...</p>
      ) : (
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filtered.map((agent) => {
            const team = TEAMS.find((t) => t.id === agent.team_id);
            return (
              <Card key={agent.agent_id} className="hover:shadow-md transition-shadow">
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <Bot className="h-4 w-4 text-muted-foreground" />
                      <CardTitle className="text-sm font-medium">
                        {agent.agent_id}
                      </CardTitle>
                    </div>
                    {!agent.enabled && <Badge variant="destructive">Disabled</Badge>}
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <Badge variant="secondary" className="text-xs mb-3">
                    {team?.name || agent.team_id}
                  </Badge>
                  <div className="flex gap-2 mt-2">
                    <Link href={`/chat?agent=${agent.agent_id}`}>
                      <Button size="sm" variant="outline" className="gap-1 text-xs h-7">
                        <MessageSquare className="h-3 w-3" />
                        Chat
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
