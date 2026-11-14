"""Application configuration via pydantic-settings.

All settings are read from environment variables (or .env file).
The .env.example file is the canonical reference for all required vars.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from pydantic import AnyHttpUrl, EmailStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/evolve_dev",
        description="Async SQLAlchemy connection URL.",
    )
    supabase_url: str = Field(default="https://your-project.supabase.co")
    supabase_anon_key: str = Field(default="your-anon-key")
    supabase_service_key: str = Field(default="your-service-key")

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------
    anthropic_api_key: str = Field(default="your-anthropic-key")
    llm_provider: str = Field(default="mock", description="'mock' or 'anthropic'")
    embedding_provider: str = Field(default="mock", description="'mock' or 'openai'")
    llm_budget_usd_per_user_per_day: float = Field(default=0.10)

    # ------------------------------------------------------------------
    # App
    # ------------------------------------------------------------------
    secret_key: str = Field(default="change-me-in-production")
    environment: str = Field(default="development")
    frontend_url: Annotated[str, AnyHttpUrl] = Field(default="http://localhost:3000")
    backend_url: Annotated[str, AnyHttpUrl] = Field(default="http://localhost:8000")
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # ------------------------------------------------------------------
    # Admin
    # ------------------------------------------------------------------
    admin_email: str = Field(default="admin@example.com")

    # ------------------------------------------------------------------
    # Derived helpers
    # ------------------------------------------------------------------
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, v: str | list[str]) -> list[str]:
        """Accept comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def is_testing(self) -> bool:
        return self.environment.lower() == "test"


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings singleton."""
    return Settings()
