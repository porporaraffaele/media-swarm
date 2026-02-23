"""Base agent factory for creating sub-agents with shared configuration.

All ~80 sub-agents across all teams use this factory to ensure consistent:
- LLM model selection
- Database connection
- Memory settings
- Knowledge integration
- Report tools
- History and context configuration
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge

from src.config.models import get_claude_haiku, get_claude_sonnet
from src.db.connection import db
from src.tools.reporting.report_tools import ReportTools


def create_agent(
    agent_id: str,
    name: str,
    role: str,
    team_id: str,
    instructions: list[str],
    knowledge: Knowledge | None = None,
    tools: list | None = None,
    output_model: type | None = None,
    use_haiku: bool = False,
    num_history_runs: int = 5,
) -> Agent:
    """Create a sub-agent with standardized configuration.

    Args:
        agent_id: Unique identifier (used for report tracking, not passed to Agent).
        name: Human-readable name (used as Agent identifier).
        role: Description of the agent's role within its team.
        team_id: ID of the parent team (for report tracking).
        instructions: List of instruction strings for the agent.
        knowledge: Optional Knowledge for RAG (per-agent isolated table).
        tools: Additional tools beyond the default ReportTools.
        output_model: Optional Pydantic model for structured output.
        use_haiku: Use Claude Haiku instead of Sonnet (for simple/fast tasks).
        num_history_runs: Number of previous runs to include in context.

    Returns:
        Configured Agent instance.
    """
    all_tools = [ReportTools(team_id=team_id, agent_id=agent_id)]
    if tools:
        all_tools.extend(tools)

    return Agent(
        name=name,
        role=role,
        model=get_claude_haiku() if use_haiku else get_claude_sonnet(),
        db=db,
        knowledge=knowledge,
        search_knowledge=knowledge is not None,
        tools=all_tools,
        instructions=instructions,
        output_schema=output_model,
        add_history_to_context=True,
        num_history_runs=num_history_runs,
        add_datetime_to_context=True,
        markdown=True,
    )
