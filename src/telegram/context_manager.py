"""In-memory context manager for active project per Telegram chat.

Tracks which project is currently "active" for each chat_id,
so that team/agent runs are automatically logged under that project.
"""

# chat_id (str) → project_id (str)
_active_projects: dict[str, str] = {}


def set_active_project(chat_id: str, project_id: str) -> None:
    """Set the active project for a chat."""
    _active_projects[chat_id] = project_id


def get_active_project(chat_id: str) -> str | None:
    """Get the active project ID for a chat, or None."""
    return _active_projects.get(chat_id)


def clear_active_project(chat_id: str) -> None:
    """Clear the active project for a chat."""
    _active_projects.pop(chat_id, None)
