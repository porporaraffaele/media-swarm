"use client";

import { useEffect, useState } from "react";
import { FolderKanban, Plus, Trash2, Users } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Separator } from "@/components/ui/separator";
import {
  getProjects,
  createProject,
  archiveProject,
  updateProjectTeams,
  getProjectSessions,
} from "@/lib/api";
import { TEAMS, type Project, type ProjectSession } from "@/lib/types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [creating, setCreating] = useState(false);
  const [selectedProject, setSelectedProject] = useState<string | null>(null);
  const [sessions, setSessions] = useState<ProjectSession[]>([]);
  const [loadingSessions, setLoadingSessions] = useState(false);

  const loadProjects = () => {
    getProjects().then((d) => setProjects(d.projects)).catch(() => {});
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleCreate = async () => {
    if (!name.trim()) return;
    setCreating(true);
    try {
      await createProject(name.trim(), description.trim() || undefined);
      setName("");
      setDescription("");
      setShowCreate(false);
      loadProjects();
    } catch {
    } finally {
      setCreating(false);
    }
  };

  const handleArchive = async (id: string) => {
    await archiveProject(id);
    loadProjects();
  };

  const handleTeamToggle = async (projectId: string, teamId: string, currentTeams: string[]) => {
    const newTeams = currentTeams.includes(teamId)
      ? currentTeams.filter((t) => t !== teamId)
      : [...currentTeams, teamId];
    await updateProjectTeams(projectId, newTeams);
    loadProjects();
  };

  const loadSessions = async (projectId: string) => {
    setSelectedProject(projectId);
    setLoadingSessions(true);
    try {
      const data = await getProjectSessions(projectId, 50);
      setSessions(data.sessions);
    } catch {
      setSessions([]);
    } finally {
      setLoadingSessions(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Projects</h2>
          <p className="text-muted-foreground">Manage your media projects and assign teams</p>
        </div>
        <Button onClick={() => setShowCreate(!showCreate)} className="gap-2">
          <Plus className="h-4 w-4" />
          New Project
        </Button>
      </div>

      {/* Create Form */}
      {showCreate && (
        <Card>
          <CardHeader>
            <CardTitle>Create Project</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <Input
              placeholder="Project name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <Textarea
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
            />
            <div className="flex gap-2">
              <Button onClick={handleCreate} disabled={creating || !name.trim()}>
                {creating ? "Creating..." : "Create"}
              </Button>
              <Button variant="outline" onClick={() => setShowCreate(false)}>
                Cancel
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Project List */}
      {projects.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <FolderKanban className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">No projects yet. Create one to get started.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {projects.map((project) => (
            <Card key={project.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>{project.name}</CardTitle>
                    {project.description && (
                      <CardDescription className="mt-1">{project.description}</CardDescription>
                    )}
                  </div>
                  <Button
                    size="icon"
                    variant="ghost"
                    className="text-muted-foreground hover:text-destructive"
                    onClick={() => handleArchive(project.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                {/* Team Assignment */}
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-2 flex items-center gap-1">
                    <Users className="h-3 w-3" /> Assigned Teams
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {TEAMS.filter((t) => t.id !== "master-orchestrator").map((team) => (
                      <Badge
                        key={team.id}
                        variant={project.team_ids.includes(team.id) ? "default" : "outline"}
                        className="cursor-pointer text-xs"
                        onClick={() => handleTeamToggle(project.id, team.id, project.team_ids)}
                      >
                        {team.name}
                      </Badge>
                    ))}
                  </div>
                </div>

                <Separator />

                {/* Sessions */}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => loadSessions(project.id)}
                  className="text-xs"
                >
                  View History
                </Button>

                {selectedProject === project.id && (
                  <div className="mt-2 space-y-2">
                    {loadingSessions ? (
                      <p className="text-xs text-muted-foreground">Loading...</p>
                    ) : sessions.length === 0 ? (
                      <p className="text-xs text-muted-foreground">No interactions yet.</p>
                    ) : (
                      sessions.map((s, i) => (
                        <div key={i} className="text-xs border rounded-lg p-2">
                          <div className="flex justify-between text-muted-foreground">
                            <span>{s.team_id || s.agent_id || "?"}</span>
                            <span>{s.created_at ? new Date(s.created_at).toLocaleString() : ""}</span>
                          </div>
                          <p className="font-medium mt-1">{s.prompt}</p>
                          {s.response && (
                            <p className="text-muted-foreground mt-0.5">{s.response}</p>
                          )}
                        </div>
                      ))
                    )}
                  </div>
                )}

                <p className="text-xs text-muted-foreground">
                  Created {project.created_at ? new Date(project.created_at).toLocaleDateString() : ""}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
