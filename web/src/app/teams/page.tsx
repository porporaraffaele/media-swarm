"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Palette, PenTool, Image, Target, Newspaper, Users, Lightbulb,
  Search, Video, BarChart3, TrendingUp, Megaphone, Globe, Brain,
  ChevronRight, MessageSquare,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TEAMS, type TeamInfo } from "@/lib/types";

const ICON_MAP: Record<string, React.ElementType> = {
  Palette, PenTool, Image, Target, Newspaper, Users, Lightbulb,
  Search, Video, BarChart3, TrendingUp, Megaphone, Globe, Brain,
};

function TeamCard({ team }: { team: TeamInfo }) {
  const [expanded, setExpanded] = useState(false);
  const Icon = ICON_MAP[team.icon] || Users;

  return (
    <Card
      className="cursor-pointer transition-all hover:shadow-md"
      onClick={() => setExpanded(!expanded)}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
              <Icon className="h-5 w-5 text-primary" />
            </div>
            <div>
              <CardTitle className="text-base">{team.name}</CardTitle>
              <CardDescription className="text-xs mt-0.5">
                {team.agentCount} agents &middot; {team.mode}
              </CardDescription>
            </div>
          </div>
          <ChevronRight
            className={`h-4 w-4 text-muted-foreground transition-transform ${expanded ? "rotate-90" : ""}`}
          />
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="text-sm text-muted-foreground">{team.role}</p>
        {expanded && (
          <div className="mt-4 flex gap-2">
            <Link href={`/chat?team=${team.id}`} onClick={(e) => e.stopPropagation()}>
              <Button size="sm" className="gap-1.5">
                <MessageSquare className="h-3.5 w-3.5" />
                Chat
              </Button>
            </Link>
            <Link href={`/reports?team_id=${team.id}`} onClick={(e) => e.stopPropagation()}>
              <Button size="sm" variant="outline" className="gap-1.5">
                <BarChart3 className="h-3.5 w-3.5" />
                Reports
              </Button>
            </Link>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default function TeamsPage() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Teams</h2>
          <p className="text-muted-foreground">14 specialized teams powering your media company</p>
        </div>
        <Badge variant="secondary" className="text-sm">
          {TEAMS.reduce((a, t) => a + t.agentCount, 0)} total agents
        </Badge>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {TEAMS.filter((t) => t.id !== "master-orchestrator").map((team) => (
          <TeamCard key={team.id} team={team} />
        ))}
      </div>

      {/* Master Orchestrator separate */}
      <div>
        <h3 className="text-lg font-semibold mb-3">Orchestration</h3>
        <TeamCard team={TEAMS.find((t) => t.id === "master-orchestrator")!} />
      </div>
    </div>
  );
}
