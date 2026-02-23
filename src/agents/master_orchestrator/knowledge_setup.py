"""Knowledge bases for Master Orchestrator sub-agents."""

from src.knowledge.factory import create_agent_knowledge

decomposer_knowledge = create_agent_knowledge("orchestrator-decomposer")
assembler_knowledge = create_agent_knowledge("orchestrator-assembler")
workflow_knowledge = create_agent_knowledge("orchestrator-workflow")
cost_knowledge = create_agent_knowledge("orchestrator-cost")
progress_knowledge = create_agent_knowledge("orchestrator-progress")
