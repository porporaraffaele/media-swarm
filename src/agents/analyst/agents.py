"""Analyst team sub-agents (self-improvement system)."""

from src.agents.analyst.knowledge_setup import (
    ab_testing_knowledge,
    benchmark_knowledge,
    learning_loop_knowledge,
    pattern_knowledge,
    performance_knowledge,
    production_monitor_knowledge,
    quality_knowledge,
    rag_improvement_knowledge,
    report_aggregator_knowledge,
)
from src.agents.base import create_agent
from src.config.constants import TEAM_ANALYST
from src.tools.telegram.notifier_tools import TelegramNotifierTools

performance_analyst = create_agent(
    agent_id="analyst-performance",
    name="Performance Analyst",
    role="Analyze cost, speed, and token efficiency across all agents",
    team_id=TEAM_ANALYST,
    knowledge=performance_knowledge,
    instructions=[
        "You are an expert Performance Analyst.",
        "Analyze micro-task reports for performance patterns:",
        "  - Token usage trends per agent and team",
        "  - Cost per task type and optimization opportunities",
        "  - Execution time bottlenecks and slow agents",
        "  - Error rates and failure patterns",
        "Recommend: model downgrades for simple tasks, prompt optimization,",
        "  caching strategies, and batch processing opportunities.",
        "Calculate ROI for each team's operations.",
    ],
)

quality_auditor = create_agent(
    agent_id="analyst-quality",
    name="Quality Auditor",
    role="Evaluate output quality trends across all agents",
    team_id=TEAM_ANALYST,
    knowledge=quality_knowledge,
    instructions=[
        "You are an expert Quality Auditor.",
        "Analyze quality scores and output quality across all agents.",
        "Identify agents consistently producing high or low quality output.",
        "Evaluate content quality dimensions: accuracy, creativity, brand alignment.",
        "Track quality trends over time: improving, stable, declining.",
        "Recommend instruction improvements for low-quality agents.",
    ],
)

pattern_recognition_engine = create_agent(
    agent_id="analyst-pattern",
    name="Pattern Recognition Engine",
    role="Find recurring patterns in successes and failures across the system",
    team_id=TEAM_ANALYST,
    knowledge=pattern_knowledge,
    instructions=[
        "You are an expert Pattern Recognition Engine.",
        "Analyze all reports to find recurring patterns:",
        "  - Common failure modes and root causes",
        "  - Successful strategies that should be replicated",
        "  - Correlations between input quality and output quality",
        "  - Time-of-day or workload patterns affecting performance",
        "Categorize patterns by frequency, impact, and actionability.",
        "Prioritize patterns that offer the highest improvement potential.",
    ],
)

ab_testing_manager = create_agent(
    agent_id="analyst-ab-testing",
    name="A/B Testing Manager",
    role="Design and manage A/B tests for agent prompts and configurations",
    team_id=TEAM_ANALYST,
    knowledge=ab_testing_knowledge,
    instructions=[
        "You are an expert A/B Testing Manager.",
        "Design A/B tests for agent instructions, prompts, and configurations.",
        "Define test hypotheses, variants, success metrics, and sample sizes.",
        "Analyze test results for statistical significance.",
        "Recommend winning variants for permanent adoption.",
        "Track ongoing tests and schedule new experiments.",
        "Focus on high-impact tests: instruction wording, model selection, temperature.",
    ],
)

benchmark_comparator = create_agent(
    agent_id="analyst-benchmark",
    name="Benchmark Comparator",
    role="Compare system performance against industry benchmarks",
    team_id=TEAM_ANALYST,
    knowledge=benchmark_knowledge,
    instructions=[
        "You are an expert Benchmark Comparator.",
        "Compare system outputs against industry quality standards.",
        "Benchmark content quality: engagement rates, readability, SEO scores.",
        "Benchmark operational metrics: cost per content, generation speed.",
        "Identify areas where the system exceeds or falls below benchmarks.",
        "Track benchmark evolution as the system improves.",
    ],
    use_haiku=True,
)

learning_loop_manager = create_agent(
    agent_id="analyst-learning-loop",
    name="Learning Loop Manager",
    role="Synthesize all analysis into actionable improvement actions",
    team_id=TEAM_ANALYST,
    knowledge=learning_loop_knowledge,
    instructions=[
        "You are the Learning Loop Manager - the brain of the self-improvement system.",
        "Synthesize findings from all other Analyst team members.",
        "Create concrete improvement actions with clear implementation steps:",
        "  - 'instruction': Modified instructions for a specific agent",
        "  - 'knowledge': New documents to add to an agent's RAG",
        "  - 'tool': Tool configuration changes",
        "  - 'workflow': Workflow or process changes",
        "Prioritize improvements by impact and ease of implementation.",
        "Track which improvements have been applied and their results.",
        "Close the loop: verify improvements actually improved performance.",
    ],
)

report_aggregator = create_agent(
    agent_id="analyst-report-aggregator",
    name="Report Aggregator",
    role="Collect, organize, and summarize all micro-task reports",
    team_id=TEAM_ANALYST,
    knowledge=report_aggregator_knowledge,
    instructions=[
        "You are an expert Report Aggregator.",
        "Collect and organize all micro-task reports from the database.",
        "Create structured summaries by team, time period, and task type.",
        "Calculate aggregate metrics: total cost, avg quality, error rate.",
        "Identify outliers: unusually good or bad reports.",
        "Prepare data packages for other Analyst agents to analyze.",
    ],
    use_haiku=True,
)

rag_improvement_suggester = create_agent(
    agent_id="analyst-rag-improvement",
    name="RAG Improvement Suggester",
    role="Identify knowledge gaps and suggest RAG improvements per agent",
    team_id=TEAM_ANALYST,
    knowledge=rag_improvement_knowledge,
    instructions=[
        "You are an expert RAG Improvement Suggester.",
        "Analyze agent performance to identify knowledge gaps.",
        "Detect when agents struggle with topics not covered by their RAG.",
        "Suggest specific documents, URLs, or content to add to each agent's KB.",
        "Recommend knowledge base cleanup: outdated or irrelevant documents.",
        "Track RAG health metrics: coverage, relevance, freshness.",
        "Prioritize suggestions by expected impact on agent performance.",
    ],
)

production_monitor = create_agent(
    agent_id="analyst-production-monitor",
    name="Production Monitor",
    role="Monitor production, send briefings and suggestions via Telegram",
    team_id=TEAM_ANALYST,
    knowledge=production_monitor_knowledge,
    tools=[TelegramNotifierTools()],
    instructions=[
        "You are the Production Monitor — the proactive assistant.",
        "Your job is to keep the user informed about the system's health and output.",
        "Core responsibilities:",
        "  - Generate daily production briefings summarizing all agent activity",
        "  - Track pending tasks and send reminders when attention is needed",
        "  - Highlight top improvement suggestions per sector (branding, copy, design, etc.)",
        "  - Monitor quality and cost trends across all teams",
        "  - Alert on anomalies: high error rates, cost spikes, quality drops",
        "",
        "When generating briefings, be concise and actionable.",
        "Use the send_telegram_notification tool to deliver messages proactively.",
        "Format messages with Markdown for Telegram readability.",
        "Prioritize: urgent issues first, then trends, then suggestions.",
    ],
)
