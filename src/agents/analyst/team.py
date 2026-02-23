"""Analyst Team assembly (self-improvement system)."""

from agno.team import Team, TeamMode

from src.agents.analyst.agents import (
    ab_testing_manager,
    benchmark_comparator,
    learning_loop_manager,
    pattern_recognition_engine,
    performance_analyst,
    quality_auditor,
    rag_improvement_suggester,
    report_aggregator,
)
from src.config.models import get_claude_sonnet
from src.db.connection import db

analyst_team = Team(
    name="Analyst Team",
    role="Analyze all agent reports and drive continuous system improvement",
    model=get_claude_sonnet(),
    mode=TeamMode.tasks,
    max_iterations=8,
    members=[
        report_aggregator,
        performance_analyst,
        quality_auditor,
        pattern_recognition_engine,
        ab_testing_manager,
        benchmark_comparator,
        rag_improvement_suggester,
        learning_loop_manager,
    ],
    db=db,
    instructions=[
        "You are the Analyst Team Orchestrator - the self-improvement engine.",
        "Run the analysis pipeline iteratively:",
        "1. Report Aggregator collects and summarizes all incoming reports.",
        "2. Performance Analyst identifies cost/speed inefficiencies.",
        "3. Quality Auditor evaluates content quality trends.",
        "4. Pattern Recognition Engine finds recurring issues or successes.",
        "5. Benchmark Comparator compares against industry standards.",
        "6. RAG Improvement Suggester identifies knowledge gaps.",
        "7. A/B Testing Manager designs experiments for improvements.",
        "8. Learning Loop Manager synthesizes all findings into actionable improvements.",
        "",
        "Output a final AnalystReport with specific, prioritized improvement suggestions.",
        "Each suggestion must specify: target team, target agent, type, and action.",
    ],
    show_members_responses=True,
    enable_agentic_state=True,
    markdown=True,
)
