"""Configuration management for Kalshi Trader.

Centralized configuration using Pydantic BaseSettings with environment
variable overrides for production deployment flexibility.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration with environment variable overrides."""

    # region Kalshi API Configuration
    kalshi_api_key: str = Field(..., env="KALSHI_API_KEY")
    kalshi_api_url: str = Field("https://trading-api.kalshi.com/trade-api/v2", env="KALSHI_API_URL")
    # endregion

    # region Google ADK Configuration
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    google_project_id: str = Field(..., env="GOOGLE_PROJECT_ID")
    google_credentials_path: Optional[str] = Field(None, env="GOOGLE_CREDENTIALS_PATH")
    gemini_model: str = Field("gemini-1.5-pro", env="GEMINI_MODEL")
    # endregion

    # region Database Configuration
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    postgres_url: Optional[str] = Field(None, env="POSTGRES_URL")
    weaviate_url: str = Field("http://localhost:8080", env="WEAVIATE_URL")
    # endregion

    # region Service Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    max_workers: int = Field(4, env="MAX_WORKERS")
    bet_size_limit: float = Field(100.0, env="BET_SIZE_LIMIT")
    # endregion

    # region Observability
    prometheus_port: int = Field(8000, env="PROMETHEUS_PORT")
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    # endregion

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# TODO: Add validation for API keys and URLs
# TODO: Implement configuration hot-reloading
# TODO: Add encryption for sensitive configuration values 