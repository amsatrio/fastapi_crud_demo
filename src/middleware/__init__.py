from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from src.app import app
from src.dto.response import AppResponse
import logging
import time

from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.middleware import global_exception

# app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com", "localhost"]
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8989",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)


log = logging.getLogger(__name__)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log.info(
        "add_process_time_header(), url: "
        + str(request.url)
        + ", status code: "
        + str(response.status_code)
    )
    return response
