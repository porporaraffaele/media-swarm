from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Providers
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Visual AI
    nano_banana_api_key: str = ""
    seedance_api_key: str = ""
    flux_api_key: str = ""
    runway_api_key: str = ""

    # Database
    database_url: str = "postgresql+psycopg://ai:ai@localhost:5532/ai"

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Google
    google_api_key: str = ""

    # Paths
    output_dir: str = "outputs"
    log_dir: str = "logs"

    # AgentOS
    agent_os_port: int = 7777
    agent_os_host: str = "0.0.0.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
