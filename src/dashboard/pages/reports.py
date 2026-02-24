"""Reports page — browse, filter, and visualize agent reports."""

import streamlit as st

from src.dashboard.api_client import get_reports
from src.dashboard.pages.teams_agents import TEAMS_INFO

ALL_AGENTS = []
for info in TEAMS_INFO.values():
    ALL_AGENTS.extend(info["agents"])
ALL_AGENTS.sort()


def render():
    st.title("📊 Reports")
    st.markdown("Browse and filter reports from all agents.")

    # ─── Filters ──────────────────────────────────────────────────────────
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        team_filter = st.selectbox(
            "Team",
            ["All"] + list(TEAMS_INFO.keys()),
            key="reports_team_filter",
        )
    with fc2:
        if team_filter == "All":
            agent_options = ["All"] + ALL_AGENTS
        else:
            agent_options = ["All"] + TEAMS_INFO[team_filter]["agents"]
        agent_filter = st.selectbox("Agent", agent_options, key="reports_agent_filter")
    with fc3:
        limit = st.number_input("Limit", min_value=5, max_value=100, value=20, step=5)

    # ─── Fetch reports ────────────────────────────────────────────────────
    reports = get_reports(
        team_id=team_filter if team_filter != "All" else None,
        agent_id=agent_filter if agent_filter != "All" else None,
        limit=limit,
    )

    if not reports:
        st.info("No reports found. Run some agents to generate reports!")
        return

    st.markdown(f"**{len(reports)} reports found**")

    # ─── Reports table ────────────────────────────────────────────────────
    for r in reports:
        with st.expander(
            f"**{r.get('agent_id', '?')}** — {r.get('task_type', '?')} "
            f"(Q: {r.get('quality_score', '?')}/10, ${r.get('cost_usd', 0):.4f})"
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Quality", f"{r.get('quality_score', '?')}/10")
            c2.metric("Cost", f"${r.get('cost_usd', 0):.4f}")
            c3.metric("Tokens", f"{r.get('tokens_used', 0):,}")
            c4.metric("Time", f"{r.get('execution_time_seconds', 0):.1f}s")

            report_data = r.get("report_data", {})
            if isinstance(report_data, dict):
                if report_data.get("approach"):
                    st.markdown(f"**Approach:** {report_data['approach']}")
                if report_data.get("result_summary"):
                    st.markdown(f"**Summary:** {report_data['result_summary']}")
                if report_data.get("recommendations"):
                    st.markdown(f"**Recommendations:** {report_data['recommendations']}")

            st.caption(f"Created: {r.get('created_at', '?')} | ID: {r.get('id', '?')}")
