from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Annotated
from src.dto.response import AppResponse
from fastapi.responses import JSONResponse
import logging
import shutil
from pathlib import Path
from src.config import environment_config
from src.config.database_config import Base, engine

log = logging.getLogger(__name__)
health_router = APIRouter()


@health_router.get("/status", response_model=AppResponse[str])
async def root():
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data="ok",
    )
    return response_data.generate_json_response()


@health_router.get("/info", response_model=AppResponse[str])
async def info():
    settings = environment_config.get_settings()
    response_data = AppResponse[dict](
        status=200,
        message="Success",
        data={
            "app_name": settings.app_name,
            "database_url": settings.database_url[:10] + "...",  # Truncate for security
        },
    )
    return response_data.generate_json_response()

@health_router.get("/init-db", response_model=AppResponse[str])
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data="ok",
    )
    return response_data.generate_json_response()