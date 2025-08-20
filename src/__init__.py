from fastapi import FastAPI, Request
from src.hello_world.routes import hello_world_router
from src.m_biodata.routes import m_biodata_router
from src.health.routes import health_router
from src.config import logger_config
from src.app import app
from src import middleware

version = "v1"
version_prefix = f"/api/{version}"

# CONFIG
logger_config.config()

# ROUTER
app.include_router(
    hello_world_router, prefix=f"{version_prefix}/hello-world", tags=["hello_world"]
)
app.include_router(
    health_router, prefix=f"{version_prefix}/health", tags=["health"]
)
app.include_router(
    m_biodata_router, prefix=f"{version_prefix}/m-biodata", tags=["m_biodata"]
)