import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Dummy Sample FastAPI Application")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "")


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql+psycopg://"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    return database_url


def get_settings() -> Settings:
    settings = Settings()
    if settings.database_url:
        return Settings(
            app_name=settings.app_name,
            app_version=settings.app_version,
            debug=settings.debug,
            database_url=_normalize_database_url(settings.database_url),
        )

    base_dir = Path(__file__).resolve().parent.parent.parent
    database_path = base_dir / "test.db"
    return Settings(database_url=f"sqlite:///{database_path}")