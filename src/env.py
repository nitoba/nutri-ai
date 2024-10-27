from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Env(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    ENV_MODE: Optional[str] = 'dev'

    API_KEY: str
    TELEGRAM_API_ID: str
    TELEGRAM_API_HASH: str
    TELEGRAM_TOKEN: str


env = Env()
