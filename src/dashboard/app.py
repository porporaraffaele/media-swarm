"""Media Swarm Dashboard — Streamlit Entrypoint.

Launch:
    streamlit run src/dashboard/app.py
"""

import streamlit as st

st.set_page_config(
    page_title="Media Swarm",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Sidebar navigation ──────────────────────────────────────────────────────

PAGES = {
    "🏠 Home": "home",
    "👥 Teams & Agents": "teams_agents",
    "🤖 Run Agent": "run_agent",
    "🚀 Run Team": "run_team",
    "📊 Reports": "reports",
    "📚 Knowledge Base": "knowledge",
    "📁 Projects": "projects",
    "🏥 System Health": "system_health",
}

st.sidebar.title("🐝 Media Swarm")
st.sidebar.markdown("---")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")
page_key = PAGES[selection]

st.sidebar.markdown("---")
st.sidebar.caption("v0.3.0 · 14 Teams · 97 Agents")

# ─── Page routing ─────────────────────────────────────────────────────────────

if page_key == "home":
    from src.dashboard.pages.home import render

    render()
elif page_key == "teams_agents":
    from src.dashboard.pages.teams_agents import render

    render()
elif page_key == "run_agent":
    from src.dashboard.pages.run_agent import render

    render()
elif page_key == "run_team":
    from src.dashboard.pages.run_team import render

    render()
elif page_key == "reports":
    from src.dashboard.pages.reports import render

    render()
elif page_key == "knowledge":
    from src.dashboard.pages.knowledge import render

    render()
elif page_key == "projects":
    from src.dashboard.pages.projects import render

    render()
elif page_key == "system_health":
    from src.dashboard.pages.system_health import render

    render()
