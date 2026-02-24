"""System Health page — DB status, costs, agent leaderboard."""

import streamlit as st

from src.dashboard.api_client import check_backend, get_health, get_report_stats, get_reports
from src.dashboard.pages.teams_agents import TEAMS_INFO


def render():
    st.title("🏥 System Health")
    st.markdown("Monitor system status, costs, and agent performance.")

    if not check_backend():
        st.error("Backend API is offline.")
        return

    # ─── Health check ─────────────────────────────────────────────────────
    st.subheader("System Status")
    health = get_health()
    if "error" in health:
        st.warning(f"Could not fetch health: {health['error']}")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Database", health.get("database", "?"))
        c2.metric("API", "Online")
        c3.metric(
            "Uptime",
            health.get("uptime", "?") if isinstance(health.get("uptime"), str) else "Running",
        )

    st.markdown("---")

    # ─── Aggregate stats ──────────────────────────────────────────────────
    st.subheader("Aggregate Statistics")
    stats = get_report_stats()
    if stats and "error" not in stats:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Reports", stats.get("total_reports", 0))
        c2.metric("Avg Quality", f"{stats.get('avg_quality', 0):.1f}/10")
        c3.metric("Total Cost", f"${stats.get('total_cost', 0):.4f}")
        c4.metric("Total Tokens", f"{stats.get('total_tokens', 0):,}")
    else:
        st.info("No report data available yet.")

    st.markdown("---")

    # ─── Agent leaderboard ────────────────────────────────────────────────
    st.subheader("Agent Leaderboard (by Quality Score)")

    # Fetch recent reports and compute per-agent stats
    reports = get_reports(limit=100)
    if reports:
        agent_stats: dict[str, dict] = {}
        for r in reports:
            aid = r.get("agent_id", "unknown")
            if aid not in agent_stats:
                agent_stats[aid] = {
                    "count": 0,
                    "total_quality": 0,
                    "total_cost": 0,
                }
            agent_stats[aid]["count"] += 1
            agent_stats[aid]["total_quality"] += r.get("quality_score", 0) or 0
            agent_stats[aid]["total_cost"] += r.get("cost_usd", 0) or 0

        # Sort by average quality
        leaderboard = []
        for aid, s in agent_stats.items():
            avg_q = s["total_quality"] / s["count"] if s["count"] > 0 else 0
            leaderboard.append(
                {
                    "Agent": aid,
                    "Reports": s["count"],
                    "Avg Quality": round(avg_q, 2),
                    "Total Cost": f"${s['total_cost']:.4f}",
                }
            )
        leaderboard.sort(key=lambda x: x["Avg Quality"], reverse=True)

        st.dataframe(leaderboard, use_container_width=True)
    else:
        st.info("No reports to build leaderboard. Run some agents first!")

    st.markdown("---")

    # ─── Team summary ─────────────────────────────────────────────────────
    st.subheader("Team Overview")
    for team_key, info in TEAMS_INFO.items():
        st.markdown(f"**{info['name']}** — {len(info['agents'])} agents")
