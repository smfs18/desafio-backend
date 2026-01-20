"""Application configuration using Pydantic Settings"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/vlab_fuel"

    # Environment
    environment: str = "development"
    debug: bool = False

    # API
    api_title: str = "V-Lab Fuel Gateway API"
    api_version: str = "1.0.0"
    api_key: str = "your-secret-api-key-here"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
