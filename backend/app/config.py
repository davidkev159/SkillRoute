"""
Centralised configuration, loaded from environment variables (.env in local dev).
Nothing secret is ever hard-coded here — connection details are read from the
environment so the repo never contains the CognoDB URI/password.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    neo4j_uri: str
    neo4j_username: str = "cognodb"
    neo4j_password: str
    neo4j_database: str = "neo4j"

    cors_origins: str = "http://localhost:5173"
    debug_log_queries: bool = False

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    # lru_cache -> settings are parsed once and reused (env is read at process start)
    return Settings()
