from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    supabase_url: str
    supabase_key: str
    supabase_jwt_secret: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings()->Settings:
    return Settings()
