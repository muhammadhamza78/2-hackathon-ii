# """
# Application Configuration
# Loads environment variables and provides configuration settings.
# """

# from pydantic_settings import BaseSettings
# from functools import lru_cache


# class Settings(BaseSettings):
#     """Application settings loaded from environment variables."""

#     # Database Configuration
#     DATABASE_URL: str

#     # JWT Configuration
#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str = "HS256"
#     JWT_EXPIRY_HOURS: int = 24

#     # Application Configuration
#     ENV: str = "development"
#     DEBUG: bool = True

#     # CORS Configuration
#     CORS_ORIGINS: str 

#     class Config:
#         env_file = ".env"
#         case_sensitive = True


# @lru_cache()
# def get_settings() -> Settings:
#     """Get cached settings instance."""
#     return Settings()


# # Export singleton settings instance
# settings = get_settings()





"""
Application Configuration
Loads environment variables and provides configuration settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str  # Example: sqlite:///./test.db

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24

    # Application Configuration
    ENV: str = "development"
    DEBUG: bool = True

    # CORS Configuration
    CORS_ORIGINS: str  # Comma-separated list of allowed origins

    # Cloud Storage Configuration (AWS S3 or Cloudflare R2)
    S3_BUCKET_NAME: str | None = None
    S3_REGION: str | None = "auto"  # Use "auto" for Cloudflare R2
    S3_ACCESS_KEY_ID: str | None = None
    S3_SECRET_ACCESS_KEY: str | None = None
    S3_ENDPOINT_URL: str | None = None  # Required for Cloudflare R2, optional for AWS S3
    S3_PUBLIC_URL: str | None = None  # Public CDN URL for serving images

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields in .env without validation errors

    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export singleton settings instance
settings = get_settings()
