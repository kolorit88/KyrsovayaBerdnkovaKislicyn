import secrets
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME : str

    REDIS_HOST : str
    REDIS_PORT : int

    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # (Gmail SMTP)
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    FRONTEND_URL: str
    BACKEND_URL: str

    DATABASE_URL: str = Field(default="")
    REDIS_URL: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8"
    )

    def model_post_init(self, __context):
        self.DATABASE_URL = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        self.REDIS_URL = f'redis://{self.DB_HOST}:{self.DB_PORT}'


settings = Settings()

