"""Knowledge bases for each Analyst sub-agent."""

from src.knowledge.factory import create_agent_knowledge

performance_knowledge = create_agent_knowledge("analyst-performance")
quality_knowledge = create_agent_knowledge("analyst-quality")
pattern_knowledge = create_agent_knowledge("analyst-pattern")
ab_testing_knowledge = create_agent_knowledge("analyst-ab-testing")
benchmark_knowledge = create_agent_knowledge("analyst-benchmark")
learning_loop_knowledge = create_agent_knowledge("analyst-learning-loop")
report_aggregator_knowledge = create_agent_knowledge("analyst-report-aggregator")
rag_improvement_knowledge = create_agent_knowledge("analyst-rag-improvement")
