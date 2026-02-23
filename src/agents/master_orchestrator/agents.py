"""Master Orchestrator sub-agents."""

from src.agents.base import create_agent
from src.agents.master_orchestrator.knowledge_setup import (
    assembler_knowledge,
    cost_knowledge,
    decomposer_knowledge,
    progress_knowledge,
    workflow_knowledge,
)
from src.config.constants import TEAM_MASTER_ORCHESTRATOR

task_decomposer = create_agent(
    agent_id="orchestrator-decomposer",
    name="Task Decomposer",
    role="Break down complex user requests into discrete, actionable sub-tasks",
    team_id=TEAM_MASTER_ORCHESTRATOR,
    knowledge=decomposer_knowledge,
    instructions=[
        "You are an expert Task Decomposer.",
        "Analyze user requests and break them into discrete sub-tasks.",
        "Each sub-task must have: description, required team, priority, dependencies.",
        "Identify which tasks can run in parallel vs. sequentially.",
        "Estimate complexity and token cost for each sub-task.",
        "Output a structured task breakdown with dependency graph.",
    ],
)

team_assembler = create_agent(
    agent_id="orchestrator-assembler",
    name="Team Assembler",
    role="Select and assign the right teams for each sub-task",
    team_id=TEAM_MASTER_ORCHESTRATOR,
    knowledge=assembler_knowledge,
    instructions=[
        "You are an expert Team Assembler.",
        "Given a task breakdown, assign the optimal team for each sub-task.",
        "Available teams: Branding, Copywriting, Graphic Design, Competitors,",
        "  News, Community, Content Ideation, Content Finder, Content Creator, Analyst.",
        "Consider team strengths and current workload.",
        "Identify cross-team dependencies and coordination needs.",
        "Flag tasks requiring multiple teams to collaborate.",
    ],
)

workflow_manager = create_agent(
    agent_id="orchestrator-workflow",
    name="Workflow Manager",
    role="Manage task execution flow and coordinate between teams",
    team_id=TEAM_MASTER_ORCHESTRATOR,
    knowledge=workflow_knowledge,
    instructions=[
        "You are an expert Workflow Manager.",
        "Orchestrate the execution flow of sub-tasks across teams.",
        "Ensure tasks execute in the correct order respecting dependencies.",
        "Track which tasks are pending, in-progress, and completed.",
        "Handle task failures: retry, reassign, or escalate.",
        "Provide real-time status updates on the overall workflow.",
    ],
)

cost_controller = create_agent(
    agent_id="orchestrator-cost",
    name="Cost Controller",
    role="Monitor and optimize token usage and API costs across all operations",
    team_id=TEAM_MASTER_ORCHESTRATOR,
    knowledge=cost_knowledge,
    instructions=[
        "You are an expert Cost Controller.",
        "Track token usage and API costs for each sub-task and team.",
        "Flag operations exceeding cost thresholds.",
        "Recommend cost optimizations: use Haiku for simple tasks, batch operations.",
        "Calculate running totals and project final cost for the operation.",
        "Provide cost-benefit analysis for expensive operations.",
    ],
    use_haiku=True,
)

progress_tracker = create_agent(
    agent_id="orchestrator-progress",
    name="Progress Tracker",
    role="Track and report on overall task completion progress",
    team_id=TEAM_MASTER_ORCHESTRATOR,
    knowledge=progress_knowledge,
    instructions=[
        "You are an expert Progress Tracker.",
        "Monitor completion status of all sub-tasks in the workflow.",
        "Calculate overall progress percentage.",
        "Identify bottlenecks and delayed tasks.",
        "Generate progress reports with ETA estimates.",
        "Compile final summary reports when all tasks complete.",
    ],
    use_haiku=True,
)
