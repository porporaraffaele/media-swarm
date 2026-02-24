"""Run Agent page — execute a single agent via the API."""

import streamlit as st

from src.dashboard.api_client import check_backend, run_agent_direct
from src.dashboard.pages.teams_agents import TEAMS_INFO

# Flatten all agent IDs
ALL_AGENTS = []
for info in TEAMS_INFO.values():
    ALL_AGENTS.extend(info["agents"])
ALL_AGENTS.sort()


def render():
    st.title("🤖 Run Agent")
    st.markdown("Execute a single agent and see the response.")

    if not check_backend():
        st.error("Backend API is offline. Start it first.")
        return

    # Agent selector with team grouping
    col1, col2 = st.columns([1, 2])
    with col1:
        team_filter = st.selectbox(
            "Filter by team",
            ["All Teams"] + [info["name"] for info in TEAMS_INFO.values()],
        )

    if team_filter == "All Teams":
        agent_list = ALL_AGENTS
    else:
        team_key = next(k for k, v in TEAMS_INFO.items() if v["name"] == team_filter)
        agent_list = TEAMS_INFO[team_key]["agents"]

    with col2:
        agent_id = st.selectbox("Select agent", agent_list)

    # Message input
    message = st.text_area(
        "Message",
        placeholder="Write your prompt here...",
        height=120,
    )

    if st.button("Run Agent", type="primary", disabled=not message):
        with st.spinner(f"Running {agent_id}..."):
            result = run_agent_direct(agent_id, message)

        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success("Agent completed!")
            # Extract response text
            content = result.get("content", result.get("response", str(result)))
            st.markdown("### Response")
            st.markdown(content)
