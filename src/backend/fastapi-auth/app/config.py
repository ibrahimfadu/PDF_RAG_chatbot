from pydantic_settings import BaseSettings
from functools import lru_cache


class Setting(BaseSettings):
    DATABASE_URL: str = "////...//"
    google_gemini: str = "////...//"
    discord: str = "////...//"
    webhooks: str = "////...//"
    openai: str = "////...//"

    class Config:
        env_file = ".env"

@lru_cache
def get_setting():
    return Setting();
