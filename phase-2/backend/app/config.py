"""
Application Configuration
Handles environment variables using Pydantic v2 (pydantic-settings)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",      # Load from .env file in dev
        case_sensitive=True
    )

    # --------------------------
    # Environment
    # --------------------------
    DEBUG: bool = True  # Toggle dev mode
    CORS_ORIGINS: str = "http://localhost:3000,https://2-hackathon-ii.vercel.app,https://2-hackathon-ii-git-main.vercel.app"

    # --------------------------
    # Database
    # --------------------------
    DATABASE_URL: str  # e.g. postgresql://user:pass@host:port/db

    # --------------------------
    # JWT / Authentication
    # --------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24  # token expiry in hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # access token expiry in minutes

def get_settings() -> Settings:
    """
    Return a Settings instance. Use this to access all env variables.
    """
    return Settings()

# Global settings instance
settings = get_settings()
