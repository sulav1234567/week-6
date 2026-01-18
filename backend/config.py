from pydantic import BaseSettings, AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./quiz_platform.db"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    WORKERS: int = 1
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    ENV: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()
