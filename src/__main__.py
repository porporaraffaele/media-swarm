"""Allow running with: python -m src"""

from src.app import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    from src.config.settings import settings

    uvicorn.run(
        "src.app:app",
        host=settings.agent_os_host,
        port=settings.agent_os_port,
        reload=True,
    )
