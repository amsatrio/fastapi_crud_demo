from fastapi import FastAPI, HTTPException
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "MyFastAPI App"
    database_url: str
    allowed_hosts: list = ["*"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()