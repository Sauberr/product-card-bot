from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    TOKEN: str
    ADMIN_LIST: str

    @property
    def admin_ids(self) -> list[int]:
        if not self.ADMIN_LIST:
            return []
        return [int(x.strip()) for x in self.ADMIN_LIST.split(",") if x.strip()]


env_config = EnvConfig()


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DB_PATH: str = Path("data/bot.db")
    DB_ECHO: bool = False

    NAMING_CONVERSATION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"



db_config = DatabaseConfig()