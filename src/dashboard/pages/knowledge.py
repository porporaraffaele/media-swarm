"""Knowledge Base page — upload files/URLs, list docs, search RAG."""

import streamlit as st

from src.dashboard.api_client import (
    add_knowledge_url,
    check_backend,
    get_knowledge_docs,
    search_knowledge,
    upload_knowledge_file,
)
from src.dashboard.pages.teams_agents import TEAMS_INFO

ALL_AGENTS = []
for info in TEAMS_INFO.values():
    ALL_AGENTS.extend(info["agents"])
ALL_AGENTS.sort()


def render():
    st.title("📚 Knowledge Base")
    st.markdown("Manage RAG knowledge for each agent.")

    if not check_backend():
        st.error("Backend API is offline.")
        return

    tab_upload, tab_url, tab_browse, tab_search = st.tabs(
        ["📤 Upload File", "🔗 Add URL", "📋 Browse Docs", "🔍 Search"]
    )

    # ─── Upload File ──────────────────────────────────────────────────────
    with tab_upload:
        st.subheader("Upload a file to an agent's knowledge base")
        agent_id = st.selectbox("Agent", ALL_AGENTS, key="kb_upload_agent")
        uploaded = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "docx", "csv"],
            key="kb_upload_file",
        )
        if st.button("Upload", disabled=not uploaded):
            with st.spinner("Uploading..."):
                result = upload_knowledge_file(agent_id, uploaded.read(), uploaded.name)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Uploaded {uploaded.name} to {agent_id}!")

    # ─── Add URL ──────────────────────────────────────────────────────────
    with tab_url:
        st.subheader("Add a URL to an agent's knowledge base")
        agent_id_url = st.selectbox("Agent", ALL_AGENTS, key="kb_url_agent")
        url = st.text_input("URL", placeholder="https://example.com/article")
        if st.button("Add URL", disabled=not url):
            with st.spinner("Loading URL..."):
                result = add_knowledge_url(agent_id_url, url)
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.success(f"Added URL to {agent_id_url}!")

    # ─── Browse Documents ─────────────────────────────────────────────────
    with tab_browse:
        st.subheader("Browse knowledge documents")
        browse_filter = st.selectbox(
            "Filter by agent",
            ["All"] + ALL_AGENTS,
            key="kb_browse_agent",
        )
        docs = get_knowledge_docs(agent_id=browse_filter if browse_filter != "All" else None)
        if not docs:
            st.info("No documents found.")
        else:
            st.markdown(f"**{len(docs)} documents**")
            for doc in docs:
                with st.expander(
                    f"**{doc.get('title', doc.get('source_path', '?'))}** "
                    f"({doc.get('agent_id', '?')})"
                ):
                    c1, c2, c3 = st.columns(3)
                    c1.write(f"**Type:** {doc.get('source_type', '?')}")
                    c2.write(f"**Chunks:** {doc.get('chunk_count', 0)}")
                    c3.write(f"**Status:** {doc.get('status', '?')}")
                    if doc.get("description"):
                        st.write(doc["description"])

    # ─── Search ───────────────────────────────────────────────────────────
    with tab_search:
        st.subheader("Search an agent's RAG knowledge")
        search_agent = st.selectbox("Agent", ALL_AGENTS, key="kb_search_agent")
        query = st.text_input("Search query", key="kb_search_query")
        if st.button("Search", disabled=not query):
            with st.spinner("Searching..."):
                results = search_knowledge(search_agent, query)
            if not results:
                st.info("No results found.")
            else:
                for i, r in enumerate(results):
                    st.markdown(f"**Result {i + 1}:**")
                    st.write(r.get("content", r.get("text", str(r))))
                    st.markdown("---")
