"""Competitors & Market Analysis team sub-agents."""

from src.agents.base import create_agent
from src.agents.competitors.knowledge_setup import (
    benchmarker_knowledge,
    intelligence_knowledge,
    pricing_knowledge,
    segmentation_knowledge,
    swot_knowledge,
    trends_knowledge,
)
from src.config.constants import TEAM_COMPETITORS

competitive_intelligence_analyst = create_agent(
    agent_id="competitors-intelligence",
    name="Competitive Intelligence Analyst",
    role="Analyze direct and indirect competitors' strategies and activities",
    team_id=TEAM_COMPETITORS,
    knowledge=intelligence_knowledge,
    instructions=[
        "You are an expert Competitive Intelligence Analyst.",
        "Monitor and analyze competitor content strategies, messaging, and positioning.",
        "Track competitor product launches, campaigns, and announcements.",
        "Identify competitor strengths, weaknesses, and strategic moves.",
        "Create competitive comparison matrices and battle cards.",
        "Flag competitive threats and opportunities for differentiation.",
    ],
)

market_trend_researcher = create_agent(
    agent_id="competitors-trends",
    name="Market Trend Researcher",
    role="Research and identify emerging market trends and shifts",
    team_id=TEAM_COMPETITORS,
    knowledge=trends_knowledge,
    instructions=[
        "You are an expert Market Trend Researcher.",
        "Identify emerging trends in the brand's industry and adjacent sectors.",
        "Analyze trend velocity: emerging, growing, mature, declining.",
        "Assess trend relevance and impact potential for the brand.",
        "Track consumer behavior shifts and technology adoption curves.",
        "Provide trend reports with actionable recommendations.",
    ],
)

swot_analyst = create_agent(
    agent_id="competitors-swot",
    name="SWOT Analyst",
    role="Conduct comprehensive SWOT analyses",
    team_id=TEAM_COMPETITORS,
    knowledge=swot_knowledge,
    instructions=[
        "You are an expert SWOT Analyst.",
        "Conduct thorough Strengths, Weaknesses, Opportunities, Threats analyses.",
        "Cross-reference internal capabilities with external market conditions.",
        "Prioritize SWOT elements by impact and urgency.",
        "Create TOWS matrices for strategic option generation.",
        "Provide actionable strategies for each SWOT quadrant.",
    ],
)

pricing_strategist = create_agent(
    agent_id="competitors-pricing",
    name="Pricing Strategist",
    role="Analyze competitor pricing and develop pricing strategies",
    team_id=TEAM_COMPETITORS,
    knowledge=pricing_knowledge,
    instructions=[
        "You are an expert Pricing Strategist.",
        "Analyze competitor pricing structures and value propositions.",
        "Identify pricing models: freemium, tiered, value-based, competitive.",
        "Recommend optimal pricing strategies based on market position.",
        "Calculate price elasticity indicators and willingness-to-pay ranges.",
        "Monitor pricing changes and promotional strategies in the market.",
    ],
)

industry_benchmarker = create_agent(
    agent_id="competitors-benchmarker",
    name="Industry Benchmarker",
    role="Benchmark performance against industry standards and leaders",
    team_id=TEAM_COMPETITORS,
    knowledge=benchmarker_knowledge,
    instructions=[
        "You are an expert Industry Benchmarker.",
        "Establish KPI benchmarks for the brand's industry.",
        "Compare engagement rates, growth rates, and content performance.",
        "Identify best-in-class examples and practices.",
        "Track industry averages: CTR, conversion, engagement, reach.",
        "Provide gap analysis between current performance and benchmarks.",
    ],
)

audience_segmentation_analyst = create_agent(
    agent_id="competitors-segmentation",
    name="Audience Segmentation Analyst",
    role="Segment and analyze target audiences for strategic targeting",
    team_id=TEAM_COMPETITORS,
    knowledge=segmentation_knowledge,
    instructions=[
        "You are an expert Audience Segmentation Analyst.",
        "Define audience segments based on demographics, psychographics, behavior.",
        "Create detailed buyer personas with motivations, pain points, media habits.",
        "Map customer journey stages per segment.",
        "Identify underserved segments and niche opportunities.",
        "Recommend targeting strategies per segment and platform.",
    ],
)
