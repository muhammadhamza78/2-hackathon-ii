"""
Application Configuration
Loads environment variables and provides configuration settings.

Spec Reference: specs/features/authentication.md (Configuration section)
"""

from pydantic_settings import BaseSettings, Field
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Add this

    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(default_factory=list)  # Add this

    # Application Configuration
    ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Uses lru_cache to create a singleton instance.
    This ensures environment variables are read only once.

    Returns:
        Settings: Application settings
    """
    return Settings()


# Export settings instance for easy import
settings = get_settings()
