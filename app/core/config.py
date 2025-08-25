from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "ExtortionGuard"
    ENV: str = "dev"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite:///./extortion_guard.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    PEPPER: str = "dev-only"
    HALF_LIFE_DAYS: int = 90
    BETA_PRIOR_A: float = 1.0
    BETA_PRIOR_B: float = 3.0
    MIN_REPORTS_FOR_HIGH: int = 3
    SAFE_BROWSING_KEY: str | None = None
    ALLOWED_ORIGINS: List[str] = ["*"]
    LOG_LEVEL: str = "INFO"
    API_KEY: str | None = None


    model_config = {
    "env_file": ".env",
    "env_file_encoding": "utf-8",
    "case_sensitive": True,
}


settings = Settings()