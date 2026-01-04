"""
Application Configuration
Loads environment variables and provides configuration settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24

    # Application Configuration
    ENV: str = "development"
    DEBUG: bool = True

    # CORS Configuration
    CORS_ORIGINS: str = "https://2-hackathon-ii.vercel.app,https://2-hackathon-ii-git-main.vercel.app"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export singleton settings instance
settings = get_settings()
