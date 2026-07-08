"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for AutoMind AI."""

    APP_NAME: str = "AutoMind AI"
    APP_DESCRIPTION: str = "AI Powered Vehicle Assistant"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    AI_NAME: str = "BON"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///automind.db"
    SECRET_KEY: str = "CHANGE_ME"
    OLLAMA_MODEL: str = "gemma3:4b"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"
    OPENAPI_URL: str = "/openapi.json"
    CONTACT_NAME: str = "AutoMind AI Maintainers"
    CONTACT_URL: str = "https://github.com/placeholder/automind-ai"
    LICENSE_NAME: str = "MIT"
    LICENSE_URL: str = "https://opensource.org/licenses/MIT"
    CORS_ORIGINS: tuple[str, ...] = (
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    )
    TRUSTED_HOSTS: tuple[str, ...] = (
        "localhost",
        "127.0.0.1",
        "testserver",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
