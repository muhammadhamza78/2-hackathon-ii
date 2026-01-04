"""
Application Configuration
Loads environment variables and provides configuration settings.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ------------------
    # Database
    # ------------------
    DATABASE_URL: str

    # ------------------
    # JWT
    # ------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24

    # ------------------
    # App
    # ------------------
    ENV: str = "development"
    DEBUG: bool = True

    # ------------------
    # CORS
    # ------------------
    CORS_ORIGINS: str = Field(default="")

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
