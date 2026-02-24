"""Run Team page — execute a full team via the API."""

import streamlit as st

from src.dashboard.api_client import check_backend, run_team

# Team command keys mapped to display names and team module keys
TEAM_OPTIONS = {
    "Master Orchestrator": "ask",
    "Branding": "branding",
    "Copywriting": "copy",
    "Graphic Design": "design",
    "Competitors & Market": "competitors",
    "News": "news",
    "Community": "community",
    "Content Ideation": "ideation",
    "Content Finder": "find",
    "Content Creator": "create",
    "Analyst": "analyst",
    "Sales & Lead Gen": "sales",
    "Ads Expert": "ads",
    "Web/Blog Management": "web",
}


def render():
    st.title("🚀 Run Team")
    st.markdown("Execute a full team pipeline and see the coordinated response.")

    if not check_backend():
        st.error("Backend API is offline. Start it first.")
        return

    # Team selector
    team_name = st.selectbox("Select team", list(TEAM_OPTIONS.keys()))
    team_key = TEAM_OPTIONS[team_name]

    # Message input
    message = st.text_area(
        "Message",
        placeholder=f"Write a prompt for the {team_name} team...",
        height=150,
    )

    st.info(
        f"The **{team_name}** team will coordinate multiple agents "
        "to produce a comprehensive response. This may take 30-120 seconds."
    )

    if st.button("Run Team", type="primary", disabled=not message):
        with st.spinner(f"Running {team_name} team... This may take a while."):
            result = run_team(team_key, message)

        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success(f"{team_name} team completed!")
            content = result.get("content", result.get("response", str(result)))
            st.markdown("### Response")
            st.markdown(content)
