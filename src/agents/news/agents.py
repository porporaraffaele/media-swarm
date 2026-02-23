"""News Agent team sub-agents."""

from agno.tools.tavily import TavilyTools

from src.agents.base import create_agent
from src.agents.news.knowledge_setup import (
    aggregator_knowledge,
    alert_knowledge,
    fact_checker_knowledge,
    relevance_knowledge,
    summarizer_knowledge,
    trend_detector_knowledge,
)
from src.config.constants import TEAM_NEWS

news_aggregator = create_agent(
    agent_id="news-aggregator",
    name="RSS & News Aggregator",
    role="Collect and aggregate news from RSS feeds and web sources",
    team_id=TEAM_NEWS,
    knowledge=aggregator_knowledge,
    tools=[TavilyTools()],
    instructions=[
        "You are an expert News Aggregator.",
        "Collect news from configured RSS feeds and web sources.",
        "Use Tavily search to find the latest news articles on any topic.",
        "Parse article metadata: title, author, date, source, category.",
        "Deduplicate articles covering the same story from different sources.",
        "Categorize articles by topic, industry, and relevance.",
        "Provide a structured list of aggregated articles with metadata.",
    ],
)

trend_detector = create_agent(
    agent_id="news-trend-detector",
    name="Trend Detector",
    role="Identify emerging trends from news patterns",
    team_id=TEAM_NEWS,
    knowledge=trend_detector_knowledge,
    tools=[TavilyTools()],
    instructions=[
        "You are an expert Trend Detector.",
        "Use Tavily search to research emerging trends and validate patterns.",
        "Analyze news articles for recurring themes and emerging patterns.",
        "Identify trend signals: frequency spikes, new terminology, sentiment shifts.",
        "Classify trends: breaking, emerging, growing, peaking, declining.",
        "Connect related trends across different industries and sectors.",
        "Flag trends with high potential impact for the brand.",
    ],
)

fact_checker = create_agent(
    agent_id="news-fact-checker",
    name="Fact Checker",
    role="Verify claims and sources in news articles",
    team_id=TEAM_NEWS,
    knowledge=fact_checker_knowledge,
    instructions=[
        "You are an expert Fact Checker.",
        "Verify key claims in news articles against reliable sources.",
        "Assess source credibility and potential bias.",
        "Flag unverified claims, misleading headlines, and speculation.",
        "Rate confidence level: verified, likely, unverified, disputed.",
        "Provide source references for fact-checked claims.",
    ],
    use_haiku=True,
)

news_summarizer = create_agent(
    agent_id="news-summarizer",
    name="News Summarizer",
    role="Create concise, actionable summaries of news articles",
    team_id=TEAM_NEWS,
    knowledge=summarizer_knowledge,
    instructions=[
        "You are an expert News Summarizer.",
        "Create concise summaries preserving key facts and insights.",
        "Structure summaries: headline, key points, implications, action items.",
        "Highlight what matters most for the brand's industry.",
        "Write in clear, accessible language for quick consumption.",
        "Group related stories into thematic briefings.",
    ],
)

relevance_scorer = create_agent(
    agent_id="news-relevance",
    name="Relevance Scorer",
    role="Score news relevance to the brand's industry and interests",
    team_id=TEAM_NEWS,
    knowledge=relevance_knowledge,
    instructions=[
        "You are an expert Relevance Scorer.",
        "Score news articles on relevance to the brand (0-10 scale).",
        "Consider: industry match, audience interest, content opportunity, timing.",
        "Prioritize articles that can inspire brand content or campaigns.",
        "Flag articles requiring immediate brand response or commentary.",
        "Filter out noise and low-relevance content.",
    ],
    use_haiku=True,
)

alert_manager = create_agent(
    agent_id="news-alert",
    name="Alert Manager",
    role="Manage urgent news alerts and notifications",
    team_id=TEAM_NEWS,
    knowledge=alert_knowledge,
    instructions=[
        "You are an expert Alert Manager.",
        "Identify news requiring immediate attention or brand response.",
        "Classify alert urgency: critical, high, medium, low.",
        "Critical: brand mentions, industry crises, competitor moves.",
        "High: trending topics relevant to brand, viral content opportunities.",
        "Draft alert notifications with context and recommended actions.",
    ],
    use_haiku=True,
)
