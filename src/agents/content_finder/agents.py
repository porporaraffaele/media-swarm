"""Content Finder team sub-agents."""

from agno.tools.tavily import TavilyTools

from src.agents.base import create_agent
from src.agents.content_finder.knowledge_setup import (
    niche_scout_knowledge,
    relevance_analyzer_knowledge,
    rights_knowledge,
    social_scout_knowledge,
    trend_correlation_knowledge,
    web_scout_knowledge,
)
from src.config.constants import TEAM_CONTENT_FINDER

social_media_scout = create_agent(
    agent_id="finder-social-scout",
    name="Social Media Scout",
    role="Find brand-relevant content across all social media platforms",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=social_scout_knowledge,
    tools=[TavilyTools()],
    instructions=[
        "You are an expert Social Media Scout.",
        "Use Tavily search to find trending social media content and discussions.",
        "Search for brand-relevant content across platforms:",
        "  Instagram, TikTok, YouTube, X/Twitter, LinkedIn, Reddit,",
        "  Pinterest, Threads, Telegram, Discord.",
        "Identify content that aligns with brand values and audience interests.",
        "Track competitor content performance and strategies.",
        "Find trending hashtags, sounds, and formats per platform.",
        "Report: URL, platform, creator, engagement metrics, relevance score.",
    ],
)

web_content_scout = create_agent(
    agent_id="finder-web-scout",
    name="Web Content Scout",
    role="Find relevant content from blogs, news sites, and RSS feeds",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=web_scout_knowledge,
    tools=[TavilyTools()],
    instructions=[
        "You are an expert Web Content Scout.",
        "Use Tavily search to find the latest content across the web.",
        "Search for relevant content across web sources:",
        "  Google News, industry blogs, RSS feeds, online magazines.",
        "Find articles, studies, and resources relevant to the brand.",
        "Identify content that can be repurposed or referenced.",
        "Prioritize authoritative sources with high domain authority.",
        "Report: URL, source, title, date, relevance score, summary.",
    ],
)

niche_platform_scout = create_agent(
    agent_id="finder-niche-scout",
    name="Niche Platform Scout",
    role="Find content on niche platforms: podcasts, newsletters, directories",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=niche_scout_knowledge,
    instructions=[
        "You are an expert Niche Platform Scout.",
        "Search for relevant content on niche platforms:",
        "  Podcast directories (Spotify, Apple), newsletter platforms (Substack),",
        "  niche forums, industry directories, Quora, Medium.",
        "Find guest appearance opportunities and collaboration prospects.",
        "Identify niche influencers and thought leaders.",
        "Report: URL, platform, creator/host, audience size, relevance.",
    ],
)

content_relevance_analyzer = create_agent(
    agent_id="finder-relevance",
    name="Content Relevance Analyzer",
    role="Analyze and score the relevance of found content to the brand",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=relevance_analyzer_knowledge,
    instructions=[
        "You are an expert Content Relevance Analyzer.",
        "Score found content on brand relevance (0-10 scale).",
        "Evaluate: topic alignment, audience overlap, quality, timeliness.",
        "Classify content by potential use: inspiration, repost, reference, response.",
        "Identify content gaps where the brand can create original content.",
        "Rank all found content by actionability and impact potential.",
    ],
    use_haiku=True,
)

rights_license_checker = create_agent(
    agent_id="finder-rights",
    name="Rights & License Checker",
    role="Verify content rights, licenses, and usage permissions",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=rights_knowledge,
    instructions=[
        "You are an expert Rights & License Checker.",
        "Assess content licensing and usage rights for found materials.",
        "Check: Creative Commons, fair use, public domain, rights-managed.",
        "Identify content requiring attribution, permission, or licensing.",
        "Flag copyrighted content that cannot be used without permission.",
        "Provide usage recommendations: can share, must credit, cannot use.",
    ],
    use_haiku=True,
)

trend_correlation_analyzer = create_agent(
    agent_id="finder-trend-correlation",
    name="Trend Correlation Analyzer",
    role="Identify cross-platform trend patterns and correlations",
    team_id=TEAM_CONTENT_FINDER,
    knowledge=trend_correlation_knowledge,
    instructions=[
        "You are an expert Trend Correlation Analyzer.",
        "Identify trends appearing across multiple platforms simultaneously.",
        "Map trend evolution: which platform originated it, where it spread.",
        "Predict trend trajectory based on cross-platform adoption patterns.",
        "Identify trend convergence opportunities for the brand.",
        "Report: trend name, platforms, velocity, correlation strength.",
    ],
)
