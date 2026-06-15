from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CORS_ORIGINS = (
    "http://localhost:4300,"
    "http://127.0.0.1:4300,"
    "http://localhost:4200,"
    "http://127.0.0.1:4200"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = DEFAULT_CORS_ORIGINS

    def get_cors_origins(self) -> list[str]:
        raw = self.CORS_ORIGINS or DEFAULT_CORS_ORIGINS
        return [origin.strip() for origin in raw.split(",") if origin.strip()]


settings = Settings()
