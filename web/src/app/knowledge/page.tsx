"use client";

import { useEffect, useState } from "react";
import {
  BookOpen,
  FileText,
  Link as LinkIcon,
  Plus,
  Search,
  Trash2,
  Upload,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  getKnowledgeAgents,
  getAgentDocuments,
  uploadDocument,
  deleteDocument,
  searchKnowledge,
} from "@/lib/api";
import type { KnowledgeAgent, KnowledgeDocument } from "@/lib/types";

export default function KnowledgePage() {
  const [agents, setAgents] = useState<KnowledgeAgent[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [documents, setDocuments] = useState<KnowledgeDocument[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<unknown[]>([]);
  const [agentSearch, setAgentSearch] = useState("");

  // Upload state
  const [showUpload, setShowUpload] = useState(false);
  const [uploadUrl, setUploadUrl] = useState("");
  const [uploadText, setUploadText] = useState("");
  const [uploadTitle, setUploadTitle] = useState("");
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    getKnowledgeAgents()
      .then((d) => setAgents(d.agents))
      .catch(() => {});
  }, []);

  const selectAgent = async (agentId: string) => {
    setSelectedAgent(agentId);
    setSearchResults([]);
    try {
      const data = await getAgentDocuments(agentId);
      setDocuments(data.documents);
    } catch {
      setDocuments([]);
    }
  };

  const handleUpload = async () => {
    if (!selectedAgent) return;
    setUploading(true);
    try {
      await uploadDocument(selectedAgent, {
        url: uploadUrl || undefined,
        text_content: uploadText || undefined,
        title: uploadTitle || undefined,
      });
      setUploadUrl("");
      setUploadText("");
      setUploadTitle("");
      setShowUpload(false);
      selectAgent(selectedAgent);
    } catch {
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId: string) => {
    if (!selectedAgent) return;
    await deleteDocument(selectedAgent, docId);
    selectAgent(selectedAgent);
  };

  const handleSearch = async () => {
    if (!selectedAgent || !searchQuery.trim()) return;
    try {
      const data = await searchKnowledge(selectedAgent, searchQuery);
      setSearchResults(data.results);
    } catch {}
  };

  const filteredAgents = agents.filter((a) =>
    a.agent_id.toLowerCase().includes(agentSearch.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold">Knowledge Base</h2>
        <p className="text-muted-foreground">
          Browse and manage knowledge bases for {agents.length} agents
        </p>
      </div>

      <div className="flex h-[calc(100vh-14rem)] gap-4">
        {/* Agent List */}
        <div className="w-72 border rounded-xl bg-card flex flex-col overflow-hidden">
          <div className="p-3 border-b">
            <Input
              placeholder="Filter agents..."
              value={agentSearch}
              onChange={(e) => setAgentSearch(e.target.value)}
              className="h-8 text-xs"
            />
          </div>
          <ScrollArea className="flex-1">
            <div className="p-1">
              {filteredAgents.map((a) => (
                <button
                  key={a.agent_id}
                  className={`w-full text-left rounded-md px-3 py-2 text-xs transition-colors ${
                    selectedAgent === a.agent_id
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent text-muted-foreground"
                  }`}
                  onClick={() => selectAgent(a.agent_id)}
                >
                  {a.agent_id}
                </button>
              ))}
            </div>
          </ScrollArea>
        </div>

        {/* Content */}
        <div className="flex-1 border rounded-xl bg-card flex flex-col overflow-hidden">
          {!selectedAgent ? (
            <div className="flex-1 flex items-center justify-center text-muted-foreground">
              <div className="text-center">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Select an agent to view its knowledge base</p>
              </div>
            </div>
          ) : (
            <>
              {/* Header */}
              <div className="flex items-center justify-between px-6 py-3 border-b">
                <div>
                  <h3 className="font-semibold">{selectedAgent}</h3>
                  <p className="text-xs text-muted-foreground">{documents.length} documents</p>
                </div>
                <div className="flex gap-2">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => setShowUpload(!showUpload)}
                    className="gap-1"
                  >
                    <Plus className="h-3.5 w-3.5" />
                    Add
                  </Button>
                </div>
              </div>

              {/* Upload Form */}
              {showUpload && (
                <div className="p-4 border-b space-y-2 bg-muted/30">
                  <Input
                    placeholder="Title"
                    value={uploadTitle}
                    onChange={(e) => setUploadTitle(e.target.value)}
                    className="h-8 text-sm"
                  />
                  <Input
                    placeholder="URL (paste a link)"
                    value={uploadUrl}
                    onChange={(e) => setUploadUrl(e.target.value)}
                    className="h-8 text-sm"
                  />
                  <Textarea
                    placeholder="Or paste text content..."
                    value={uploadText}
                    onChange={(e) => setUploadText(e.target.value)}
                    rows={3}
                    className="text-sm"
                  />
                  <div className="flex gap-2">
                    <Button size="sm" onClick={handleUpload} disabled={uploading}>
                      {uploading ? "Uploading..." : "Upload"}
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => setShowUpload(false)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              )}

              {/* Search */}
              <div className="flex gap-2 px-4 py-3 border-b">
                <Input
                  placeholder="Search knowledge..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  className="h-8 text-sm"
                />
                <Button size="sm" variant="outline" onClick={handleSearch}>
                  <Search className="h-3.5 w-3.5" />
                </Button>
              </div>

              {/* Documents */}
              <ScrollArea className="flex-1">
                <div className="p-4 space-y-2">
                  {searchResults.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium mb-2">Search Results</h4>
                      {searchResults.map((r, i) => (
                        <div key={i} className="bg-muted rounded-lg p-3 text-xs mb-2">
                          <pre className="whitespace-pre-wrap">{JSON.stringify(r, null, 2)}</pre>
                        </div>
                      ))}
                    </div>
                  )}

                  {documents.length === 0 ? (
                    <p className="text-sm text-muted-foreground text-center py-8">
                      No documents yet. Upload one to get started.
                    </p>
                  ) : (
                    documents.map((doc) => (
                      <div
                        key={doc.id}
                        className="flex items-center justify-between p-3 rounded-lg border hover:bg-muted/30 transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          {doc.source_type === "url" ? (
                            <LinkIcon className="h-4 w-4 text-muted-foreground" />
                          ) : (
                            <FileText className="h-4 w-4 text-muted-foreground" />
                          )}
                          <div>
                            <p className="text-sm font-medium">{doc.title || doc.source_path || "Untitled"}</p>
                            <div className="flex gap-2 mt-0.5">
                              <Badge variant="secondary" className="text-[10px]">{doc.source_type}</Badge>
                              <span className="text-[10px] text-muted-foreground">
                                {doc.chunk_count} chunks
                              </span>
                            </div>
                          </div>
                        </div>
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-7 w-7 text-muted-foreground hover:text-destructive"
                          onClick={() => handleDelete(doc.id)}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </Button>
                      </div>
                    ))
                  )}
                </div>
              </ScrollArea>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
