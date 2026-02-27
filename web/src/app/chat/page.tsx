"use client";

import { Suspense, useEffect, useRef, useState, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { Bot, Send, Users, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { cn } from "@/lib/utils";
import { runTeam, runAgent } from "@/lib/api";
import { TEAMS, type ChatMessage } from "@/lib/types";
import ReactMarkdown from "react-markdown";

export default function ChatPageWrapper() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center h-96 text-muted-foreground">Loading chat...</div>}>
      <ChatPage />
    </Suspense>
  );
}

// Agent IDs grouped by team (matches KB_TABLES from constants.py)
const AGENT_IDS: Record<string, string[]> = {
  branding: ["branding-strategist","branding-visual-identity","branding-tone-of-voice","branding-storyteller","branding-auditor","branding-naming","branding-positioning","branding-cultural-sensitivity"],
  copywriting: ["copywriting-seo","copywriting-social-media","copywriting-email","copywriting-ad-copy","copywriting-script","copywriting-ux","copywriting-proofreader"],
  "graphic-design": ["design-social-media","design-template","design-infographic","design-thumbnail","design-motion","design-photo-editor"],
  competitors: ["competitors-intelligence","competitors-trends","competitors-swot","competitors-pricing","competitors-benchmarker","competitors-segmentation"],
  news: ["news-aggregator","news-trend-detector","news-fact-checker","news-summarizer","news-relevance","news-alert"],
  community: ["community-engagement","community-responder","community-ugc","community-growth","community-analytics","community-crisis","community-influencer","community-events","community-ambassador"],
  "content-ideation": ["ideation-format","ideation-hook","ideation-trend-adapter","ideation-calendar","ideation-tone-optimizer","ideation-viral-scorer"],
  "content-finder": ["finder-social-scout","finder-web-scout","finder-niche-scout","finder-relevance","finder-rights","finder-trend-correlation"],
  "content-creator": ["creator-image-gen","creator-video-gen","creator-prompt-crafter","creator-quality-reviewer","creator-format-optimizer","creator-post-production"],
  analyst: ["analyst-performance","analyst-quality","analyst-pattern","analyst-ab-testing","analyst-benchmark","analyst-learning-loop","analyst-report-aggregator","analyst-rag-improvement","analyst-production-monitor"],
  sales: ["sales-web-scraper","sales-lead-generator","sales-lead-qualifier","sales-outreach-specialist","sales-strategist","sales-technical-consultant","sales-crm-manager"],
  "ads-expert": ["ads-fb-instagram","ads-google","ads-tiktok","ads-linkedin","ads-youtube","ads-creative","ads-ab-optimization","ads-budget-roi"],
  "web-blog": ["web-seo-technical","web-blog-writer","web-landing-page","web-cms-manager","web-analytics","web-email-marketing","web-site-performance","web-content-calendar"],
  "master-orchestrator": ["orchestrator-decomposer","orchestrator-assembler","orchestrator-workflow","orchestrator-cost","orchestrator-progress"],
};

type Target = { type: "team"; id: string } | { type: "agent"; id: string };

function ChatPage() {
  const searchParams = useSearchParams();
  const [target, setTarget] = useState<Target>(() => {
    const teamParam = searchParams.get("team");
    const agentParam = searchParams.get("agent");
    if (agentParam) return { type: "agent", id: agentParam };
    if (teamParam) return { type: "team", id: teamParam };
    return { type: "team", id: "master-orchestrator" };
  });
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const sendMessage = useCallback(async () => {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    const userMsg: ChatMessage = { role: "user", content: text, timestamp: new Date() };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      let response: unknown;
      if (target.type === "team") {
        response = await runTeam(target.id, text);
      } else {
        response = await runAgent(target.id, text);
      }

      // AgentOS returns various response shapes — extract the content
      let content = "";
      if (typeof response === "string") {
        content = response;
      } else if (response && typeof response === "object") {
        const r = response as Record<string, unknown>;
        content = (r.content as string) || (r.response as string) || (r.message as string) || JSON.stringify(r, null, 2);
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content, timestamp: new Date() },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Error: ${err instanceof Error ? err.message : "Unknown error"}`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, target]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const targetLabel =
    target.type === "team"
      ? TEAMS.find((t) => t.id === target.id)?.name || target.id
      : target.id;

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4">
      {/* Sidebar — Team/Agent Selection */}
      <div className="w-64 border rounded-xl bg-card flex flex-col overflow-hidden">
        <div className="p-4 border-b">
          <h3 className="font-semibold text-sm">Select Target</h3>
        </div>
        <ScrollArea className="flex-1">
          <div className="p-2">
            {TEAMS.map((team) => (
              <div key={team.id}>
                <button
                  className={cn(
                    "w-full text-left rounded-lg px-3 py-2 text-sm font-medium transition-colors flex items-center gap-2",
                    target.type === "team" && target.id === team.id
                      ? "bg-primary text-primary-foreground"
                      : "hover:bg-accent text-muted-foreground"
                  )}
                  onClick={() => setTarget({ type: "team", id: team.id })}
                >
                  <Users className="h-3.5 w-3.5" />
                  {team.name}
                </button>
                {/* Show agents under team */}
                {AGENT_IDS[team.id]?.map((agentId) => (
                  <button
                    key={agentId}
                    className={cn(
                      "w-full text-left rounded-md px-3 py-1.5 text-xs transition-colors ml-4 flex items-center gap-1.5",
                      target.type === "agent" && target.id === agentId
                        ? "bg-primary text-primary-foreground"
                        : "hover:bg-accent text-muted-foreground"
                    )}
                    onClick={() => setTarget({ type: "agent", id: agentId })}
                  >
                    <Bot className="h-3 w-3" />
                    {agentId}
                  </button>
                ))}
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Chat Area */}
      <div className="flex-1 border rounded-xl bg-card flex flex-col overflow-hidden">
        {/* Chat Header */}
        <div className="flex items-center gap-3 px-6 py-3 border-b">
          {target.type === "team" ? (
            <Users className="h-5 w-5 text-primary" />
          ) : (
            <Bot className="h-5 w-5 text-primary" />
          )}
          <div>
            <h3 className="font-semibold">{targetLabel}</h3>
            <p className="text-xs text-muted-foreground">
              {target.type === "team" ? "Team" : "Agent"} &middot;{" "}
              {target.type === "team"
                ? TEAMS.find((t) => t.id === target.id)?.role || ""
                : `Part of ${target.id.split("-").slice(0, -1).join("-")}`}
            </p>
          </div>
          <Badge variant="secondary" className="ml-auto">
            {messages.length} messages
          </Badge>
        </div>

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4 chat-scroll">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
                <MessageSquareIcon className="h-8 w-8 text-primary" />
              </div>
              <h3 className="font-semibold text-lg mb-1">Chat with {targetLabel}</h3>
              <p className="text-muted-foreground text-sm max-w-md">
                Send a message to start working. You can ask the {target.type} to
                perform tasks, create content, analyze data, or get recommendations.
              </p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={cn(
                "flex gap-3 max-w-[85%]",
                msg.role === "user" ? "ml-auto flex-row-reverse" : ""
              )}
            >
              <div
                className={cn(
                  "h-8 w-8 rounded-full flex items-center justify-center shrink-0",
                  msg.role === "user" ? "bg-primary" : "bg-muted"
                )}
              >
                {msg.role === "user" ? (
                  <span className="text-primary-foreground text-xs font-bold">U</span>
                ) : (
                  <Bot className="h-4 w-4" />
                )}
              </div>
              <div
                className={cn(
                  "rounded-2xl px-4 py-3 text-sm",
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                )}
              >
                {msg.role === "assistant" ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                ) : (
                  msg.content
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3">
              <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
              <div className="rounded-2xl px-4 py-3 bg-muted text-sm text-muted-foreground">
                Thinking...
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t p-4">
          <div className="flex gap-3">
            <Textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Message ${targetLabel}...`}
              className="min-h-[44px] max-h-[200px] resize-none"
              rows={1}
              disabled={loading}
            />
            <Button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              size="icon"
              className="shrink-0 h-11 w-11"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

function MessageSquareIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}
