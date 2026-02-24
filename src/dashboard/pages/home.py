"""Home page — overview cards, recent activity, quick actions."""

import streamlit as st

from src.dashboard.api_client import check_backend, get_report_stats, get_root_info


def render():
    st.title("🐝 Media Swarm Dashboard")
    st.markdown("AI-powered media company with **14 teams** and **97 agents**.")

    # ─── Backend status ───────────────────────────────────────────────────
    online = check_backend()
    if online:
        st.success("Backend API is online (localhost:7777)")
    else:
        st.error("Backend API is offline. Start it with: `uv run python -m src.app`")
        return

    # ─── System info cards ────────────────────────────────────────────────
    info = get_root_info()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Teams", info.get("teams", "?"))
    c2.metric("Agents", info.get("sub_agents", "?"))
    c3.metric("Version", info.get("version", "?"))
    c4.metric("Telegram", "Active" if info.get("telegram") else "Off")

    st.markdown("---")

    # ─── Report stats ─────────────────────────────────────────────────────
    stats = get_report_stats()
    if stats and "error" not in stats:
        st.subheader("Report Statistics")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Reports", stats.get("total_reports", 0))
        s2.metric("Avg Quality", f"{stats.get('avg_quality', 0):.1f}/10")
        s3.metric("Total Cost", f"${stats.get('total_cost', 0):.4f}")
        s4.metric("Total Tokens", f"{stats.get('total_tokens', 0):,}")

    # ─── Quick actions ────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Quick Actions")
    qa1, qa2, qa3, qa4 = st.columns(4)
    with qa1:
        if st.button("🤖 Run Agent", use_container_width=True):
            st.session_state["_nav"] = "run_agent"
            st.rerun()
    with qa2:
        if st.button("🚀 Run Team", use_container_width=True):
            st.session_state["_nav"] = "run_team"
            st.rerun()
    with qa3:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state["_nav"] = "reports"
            st.rerun()
    with qa4:
        if st.button("📚 Knowledge Base", use_container_width=True):
            st.session_state["_nav"] = "knowledge"
            st.rerun()
