"""Projects page — create, browse, and manage projects."""

import streamlit as st

from src.dashboard.api_client import check_backend, create_project, get_projects


def render():
    st.title("📁 Projects")
    st.markdown("Organize your work into projects to track team interactions.")

    if not check_backend():
        st.error("Backend API is offline.")
        return

    tab_browse, tab_create = st.tabs(["📋 Browse Projects", "➕ Create Project"])

    # ─── Browse ───────────────────────────────────────────────────────────
    with tab_browse:
        projects = get_projects()
        if not projects:
            st.info("No projects yet. Create one to get started!")
        else:
            st.markdown(f"**{len(projects)} projects**")
            for p in projects:
                with st.expander(f"**{p.get('name', '?')}** — {p.get('status', '?')}"):
                    st.write(f"**ID:** `{p.get('id', '?')}`")
                    st.write(f"**Description:** {p.get('description', 'N/A')}")
                    st.write(f"**Teams:** {', '.join(p.get('team_ids', []))}")
                    st.write(f"**Status:** {p.get('status', '?')}")
                    st.write(f"**Created:** {p.get('created_at', '?')}")

    # ─── Create ───────────────────────────────────────────────────────────
    with tab_create:
        st.subheader("Create a new project")
        name = st.text_input("Project name", key="project_name")
        description = st.text_area(
            "Description (optional)",
            key="project_desc",
            height=100,
        )
        if st.button("Create Project", type="primary", disabled=not name):
            with st.spinner("Creating project..."):
                result = create_project(name, description)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Project '{name}' created!")
                st.rerun()
