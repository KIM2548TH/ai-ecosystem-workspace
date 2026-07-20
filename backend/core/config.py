"""Configuration settings for the Backend service."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate .env dynamically (check root first, then backend/)
ROOT_DIR: Path = Path(__file__).resolve().parents[2]
ENV_FILE: Path = ROOT_DIR / ".env"
if not ENV_FILE.exists():
    ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    """Application Settings loaded from environment variables or .env file."""

    redis_host: str = Field(..., description="Redis host address")
    redis_port: int = Field(6379, description="Redis port number")
    postgres_host: str = Field(..., description="PostgreSQL host address")
    postgres_port: int = Field(5432, description="PostgreSQL port number")
    postgres_user: str = Field(..., description="PostgreSQL database user")
    postgres_password: str = Field(..., description="PostgreSQL user password")
    postgres_db: str = Field(..., description="PostgreSQL database name")
    label_studio_url: str = Field(..., description="Label Studio service URL")
    label_studio_api_key: str = Field(..., description="Label Studio API access token")

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings: Settings = Settings()
