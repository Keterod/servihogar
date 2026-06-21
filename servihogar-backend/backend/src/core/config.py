from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CORS_ORIGINS = "https://servihogar-frontend.onrender.com"


def normalize_cors_origin(origin: str) -> str:
    """Strip whitespace, surrounding quotes, and trailing slashes from one origin."""
    cleaned = origin.strip()
    if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in "\"'":
        cleaned = cleaned[1:-1].strip()
    return cleaned.rstrip("/")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = DEFAULT_CORS_ORIGINS

    def get_cors_origins(self) -> list[str]:
        raw = self.CORS_ORIGINS or DEFAULT_CORS_ORIGINS
        origins: list[str] = []
        for part in raw.split(","):
            normalized = normalize_cors_origin(part)
            if normalized:
                origins.append(normalized)
        return origins


settings = Settings()
