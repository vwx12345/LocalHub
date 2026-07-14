from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LocalHub API"
    app_env: str = "local"

    database_url: str = "sqlite:///./data/localhub.db"
    frontend_origins: str = "http://localhost:5173"
    openai_api_key: str = ""
    openai_model: str =""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.frontend_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()