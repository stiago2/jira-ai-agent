"""
Application configuration using Pydantic Settings.
"""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "jira-ai-agent"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: Union[List[str], str] = Field(default=["http://localhost:3000"])

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        """Parse ALLOWED_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            # Split by comma and strip whitespace
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    # Jira Configuration
    JIRA_BASE_URL: str = Field(..., description="Jira Cloud base URL")
    JIRA_EMAIL: str = Field(..., description="Jira user email")
    JIRA_API_TOKEN: str = Field(..., description="Jira API token")
    JIRA_DEFAULT_PROJECT: str = Field(default="PROJ")

    # AI/LLM Configuration (for future implementation)
    LLM_PROVIDER: str = Field(default="openai")
    LLM_API_KEY: str = Field(default="")
    LLM_MODEL: str = Field(default="gpt-4")
    LLM_TEMPERATURE: float = Field(default=0.3)
    LLM_MAX_TOKENS: int = Field(default=500)

    # Cache
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    CACHE_TTL: int = Field(default=3600)
    CACHE_ENABLED: bool = Field(default=False)

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60)

    # Retry Configuration
    MAX_RETRIES: int = Field(default=3)
    RETRY_BACKOFF_FACTOR: int = Field(default=2)


# Global settings instance
settings = Settings()
