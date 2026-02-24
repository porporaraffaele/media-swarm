"""Teams & Agents browser page."""

import streamlit as st

# Team → agents mapping (static reference)
TEAMS_INFO = {
    "branding": {
        "name": "Branding",
        "agents": [
            "branding-strategist",
            "branding-visual-identity",
            "branding-tone-of-voice",
            "branding-storyteller",
            "branding-auditor",
            "branding-naming",
            "branding-positioning",
            "branding-cultural-sensitivity",
        ],
    },
    "copywriting": {
        "name": "Copywriting",
        "agents": [
            "copywriting-seo",
            "copywriting-social-media",
            "copywriting-email",
            "copywriting-ad-copy",
            "copywriting-script",
            "copywriting-ux",
            "copywriting-proofreader",
        ],
    },
    "graphic-design": {
        "name": "Graphic Design",
        "agents": [
            "design-social-media",
            "design-template",
            "design-infographic",
            "design-thumbnail",
            "design-motion",
            "design-photo-editor",
        ],
    },
    "competitors": {
        "name": "Competitors & Market",
        "agents": [
            "competitors-intelligence",
            "competitors-trends",
            "competitors-swot",
            "competitors-pricing",
            "competitors-benchmarker",
            "competitors-segmentation",
        ],
    },
    "news": {
        "name": "News",
        "agents": [
            "news-aggregator",
            "news-trend-detector",
            "news-fact-checker",
            "news-summarizer",
            "news-relevance",
            "news-alert",
        ],
    },
    "community": {
        "name": "Community",
        "agents": [
            "community-engagement",
            "community-responder",
            "community-ugc",
            "community-growth",
            "community-analytics",
            "community-crisis",
            "community-influencer",
            "community-events",
            "community-ambassador",
        ],
    },
    "content-ideation": {
        "name": "Content Ideation",
        "agents": [
            "ideation-format",
            "ideation-hook",
            "ideation-trend-adapter",
            "ideation-calendar",
            "ideation-tone-optimizer",
            "ideation-viral-scorer",
        ],
    },
    "content-finder": {
        "name": "Content Finder",
        "agents": [
            "finder-social-scout",
            "finder-web-scout",
            "finder-niche-scout",
            "finder-relevance",
            "finder-rights",
            "finder-trend-correlation",
        ],
    },
    "content-creator": {
        "name": "Content Creator",
        "agents": [
            "creator-image-gen",
            "creator-video-gen",
            "creator-prompt-crafter",
            "creator-quality-reviewer",
            "creator-format-optimizer",
            "creator-post-production",
        ],
    },
    "master-orchestrator": {
        "name": "Master Orchestrator",
        "agents": [
            "orchestrator-decomposer",
            "orchestrator-assembler",
            "orchestrator-workflow",
            "orchestrator-cost",
            "orchestrator-progress",
        ],
    },
    "analyst": {
        "name": "Analyst",
        "agents": [
            "analyst-performance",
            "analyst-quality",
            "analyst-pattern",
            "analyst-ab-testing",
            "analyst-benchmark",
            "analyst-learning-loop",
            "analyst-report-aggregator",
            "analyst-rag-improvement",
            "analyst-production-monitor",
        ],
    },
    "sales": {
        "name": "Sales & Lead Gen",
        "agents": [
            "sales-web-scraper",
            "sales-lead-generator",
            "sales-lead-qualifier",
            "sales-outreach-specialist",
            "sales-strategist",
            "sales-technical-consultant",
            "sales-crm-manager",
        ],
    },
    "ads-expert": {
        "name": "Ads Expert",
        "agents": [
            "ads-fb-instagram",
            "ads-google",
            "ads-tiktok",
            "ads-linkedin",
            "ads-youtube",
            "ads-creative",
            "ads-ab-optimization",
            "ads-budget-roi",
        ],
    },
    "web-blog": {
        "name": "Web/Blog Management",
        "agents": [
            "web-seo-technical",
            "web-blog-writer",
            "web-landing-page",
            "web-cms-manager",
            "web-analytics",
            "web-email-marketing",
            "web-site-performance",
            "web-content-calendar",
        ],
    },
}


def render():
    st.title("👥 Teams & Agents")
    st.markdown(
        f"**{len(TEAMS_INFO)} teams** with a total of "
        f"**{sum(len(t['agents']) for t in TEAMS_INFO.values())} agents**."
    )

    # Team selector
    team_keys = list(TEAMS_INFO.keys())
    team_names = [TEAMS_INFO[k]["name"] for k in team_keys]
    selected_name = st.selectbox("Select a team", team_names)
    selected_key = team_keys[team_names.index(selected_name)]
    team = TEAMS_INFO[selected_key]

    st.subheader(f"{team['name']} ({len(team['agents'])} agents)")

    # Display agents in a grid
    cols = st.columns(min(4, len(team["agents"])))
    for i, agent_id in enumerate(team["agents"]):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
            <div style="padding: 12px; border: 1px solid #ddd; border-radius: 8px;
                        margin-bottom: 8px; text-align: center;">
                <code>{agent_id}</code>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # All agents flat list
    with st.expander("View all 97 agents"):
        for team_key, info in TEAMS_INFO.items():
            st.markdown(f"**{info['name']}**: " + ", ".join(f"`{a}`" for a in info["agents"]))
