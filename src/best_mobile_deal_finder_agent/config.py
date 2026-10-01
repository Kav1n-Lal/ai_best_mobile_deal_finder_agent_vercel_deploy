from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ---------------------------------------------------------
    # OpenRouter
    # ---------------------------------------------------------

    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "qwen/qwen3-8b"
    openrouter_api_key: str

    # ---------------------------------------------------------
    # PostgreSQL
    # ---------------------------------------------------------

    db_host: str | None = None
    db_port: int = 5432
    db_name: str | None = None
    db_user: str | None = None
    db_password: str | None = None

    # ---------------------------------------------------------
    # Neon PostgreSQL
    # ---------------------------------------------------------

    neon_database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
