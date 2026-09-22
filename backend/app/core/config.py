from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClamSentinel"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = False
    database_url: str = "postgresql+psycopg://scanner:change_me@localhost:5432/clamsentinel"
    max_upload_size_mb: int = 100
    clamav_host: str = "localhost"
    clamav_port: int = 3310
    cors_origins: str = "http://localhost:5173"
    jwt_secret_key: str = "development-only-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CLAMSENTINEL_")


settings = Settings()
