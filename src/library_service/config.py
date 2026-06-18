from os import getenv


class Settings:
    DB_HOST: str = getenv("DB_HOST", "localhost")
    DB_PORT: str = getenv("DB_PORT", "5434")
    DB_NAME: str = getenv("DB_NAME", "library_db")
    DB_USER: str = getenv("DB_USER", "admin")
    DB_PASSWORD: str = getenv("DB_PASSWORD", "admin")

    # SECRET_KEY: str = getenv("SECRET_KEY")
    # ALGORITHM: str = "HS256"
    # ACCESS_EXPIRE_MIN: int = 15
    # REFRESH_EXPIRE_DAYS: int = 30

    @property
    def DATABASE_URL(self) -> str:
        host = self._normalized_text(self.DB_HOST, "localhost")
        user = self._normalized_text(self.DB_USER, "admin")
        password = self._normalized_text(self.DB_PASSWORD, "admin")
        database = self._normalized_text(self.DB_NAME, "library_db")
        port = self._normalized_port()
        return (
            f"postgresql+asyncpg://{user}:{password}"
            f"@{host}:{port}/{database}"
        )

    def _normalized_port(self) -> int:
        raw_port = (self.DB_PORT or "").strip()
        if not raw_port or raw_port.lower() in {"none", "null"}:
            return 5433
        return int(raw_port)

    def _normalized_text(self, value: str | None, default: str) -> str:
        normalized = (value or "").strip()
        if not normalized or normalized.lower() in {"none", "null"}:
            return default
        return normalized


settings = Settings()
