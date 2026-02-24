"""HTTP client for the Media Swarm FastAPI backend (localhost:7777)."""

import httpx

BASE_URL = "http://localhost:7777"
TIMEOUT = 60.0


def _client() -> httpx.Client:
    """Return a shared HTTP client."""
    return httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)


# ─── Health / Root ────────────────────────────────────────────────────────────


def get_root_info() -> dict:
    """GET / — system info."""
    try:
        with _client() as c:
            r = c.get("/")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def get_health() -> dict:
    """GET /admin/health — detailed health check."""
    try:
        with _client() as c:
            r = c.get("/admin/health")
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


# ─── Reports ──────────────────────────────────────────────────────────────────


def get_reports(
    team_id: str | None = None,
    agent_id: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """GET /admin/reports — list reports with optional filters."""
    params: dict = {"limit": limit}
    if team_id:
        params["team_id"] = team_id
    if agent_id:
        params["agent_id"] = agent_id
    try:
        with _client() as c:
            r = c.get("/admin/reports", params=params)
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


def get_report_stats() -> dict:
    """GET /admin/reports/stats — aggregate report statistics."""
    try:
        with _client() as c:
            r = c.get("/admin/reports/stats")
            r.raise_for_status()
            return r.json()
    except Exception:
        return {}


# ─── Knowledge ────────────────────────────────────────────────────────────────


def get_knowledge_docs(agent_id: str | None = None) -> list[dict]:
    """GET /admin/knowledge/documents."""
    params = {}
    if agent_id:
        params["agent_id"] = agent_id
    try:
        with _client() as c:
            r = c.get("/admin/knowledge/documents", params=params)
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


def upload_knowledge_file(agent_id: str, file_bytes: bytes, filename: str) -> dict:
    """POST /admin/knowledge/upload — upload a file to agent's KB."""
    try:
        with _client() as c:
            r = c.post(
                "/admin/knowledge/upload",
                data={"agent_id": agent_id},
                files={"file": (filename, file_bytes)},
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def add_knowledge_url(agent_id: str, url: str) -> dict:
    """POST /admin/knowledge/url — add URL to agent's KB."""
    try:
        with _client() as c:
            r = c.post(
                "/admin/knowledge/url",
                json={"agent_id": agent_id, "url": url},
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def search_knowledge(agent_id: str, query: str) -> list[dict]:
    """GET /admin/knowledge/search."""
    try:
        with _client() as c:
            r = c.get(
                "/admin/knowledge/search",
                params={"agent_id": agent_id, "query": query},
            )
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


# ─── Agent Config ─────────────────────────────────────────────────────────────


def get_agent_configs() -> list[dict]:
    """GET /admin/agent-configs."""
    try:
        with _client() as c:
            r = c.get("/admin/agent-configs")
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


# ─── Projects ─────────────────────────────────────────────────────────────────


def get_projects() -> list[dict]:
    """GET /admin/projects (via reports router)."""
    try:
        with _client() as c:
            r = c.get("/admin/projects")
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


def create_project(name: str, description: str = "") -> dict:
    """POST /admin/projects."""
    try:
        with _client() as c:
            r = c.post(
                "/admin/projects",
                json={"name": name, "description": description},
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


# ─── Teams / Agents (Agno OS endpoints) ──────────────────────────────────────


def get_teams() -> list[dict]:
    """GET /v1/teams — list all teams from AgentOS."""
    try:
        with _client() as c:
            r = c.get("/v1/teams")
            r.raise_for_status()
            return r.json()
    except Exception:
        return []


def run_team(team_id: str, message: str) -> dict:
    """POST /v1/teams/{team_id}/run — run a team with a message."""
    try:
        with _client() as c:
            r = c.post(
                f"/v1/teams/{team_id}/run",
                json={"input": message},
                timeout=120.0,
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def run_agent_direct(agent_id: str, message: str) -> dict:
    """POST /v1/agents/{agent_id}/run — run an agent directly."""
    try:
        with _client() as c:
            r = c.post(
                f"/v1/agents/{agent_id}/run",
                json={"input": message},
                timeout=120.0,
            )
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


def check_backend() -> bool:
    """Quick check if backend is reachable."""
    try:
        with _client() as c:
            r = c.get("/", timeout=5.0)
            return r.status_code == 200
    except Exception:
        return False
