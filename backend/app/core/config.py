import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "CPA Adaptive Exam Platform"
    SECRET_KEY: str = "cpa-secret-key-super-secure-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    DATABASE_URL: str = "sqlite:///./cpa_prep.db"
    NVIDIA_API_KEY: str = ""
    CORS_ORIGINS: list[str] = [
        "https://demo.i-te.am",
        "http://localhost:8005",
        "http://127.0.0.1:8005"
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
