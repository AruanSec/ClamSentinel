from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClamSentinel"
    environment: str = "development"
    debug: bool = False
    database_url: str = "postgresql+psycopg://scanner:change_me@localhost:5432/clamsentinel"
    max_upload_size_mb: int = 100
    clamav_host: str = "localhost"
    clamav_port: int = 3310

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CLAMSENTINEL_")


settings = Settings()
