from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from typing import Annotated
from  .schemas import HelloWorld
from src.dto.response import AppResponse
from fastapi.responses import JSONResponse
import logging
import shutil
from pathlib import Path

log = logging.getLogger(__name__)
hello_world_router = APIRouter()

@hello_world_router.get("/", response_model=AppResponse[str])
async def root():
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data="Hello World!",
    )
    return response_data.generate_json_response()

@hello_world_router.get("/path/{message}", response_model=AppResponse[str])
async def path_param(message: str):
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data=message,
    )
    return response_data.generate_json_response()

@hello_world_router.get("/query", response_model=AppResponse[str])
async def query_param(message: str = ""):
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data=message,
    )
    return response_data.generate_json_response()

@hello_world_router.post("/", response_model=AppResponse[HelloWorld])
async def body_request(hello_world: HelloWorld):
    response_data = AppResponse[HelloWorld](
        status=200,
        message="Success",
        data=hello_world,
    )
    return response_data.generate_json_response()


@hello_world_router.get("/logger", response_model=AppResponse[str])
async def logger():
    log.info("logger()")
    log.warn("logger()")
    log.error("logger()")
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data="ok",
    )
    return response_data.generate_json_response()

@hello_world_router.get("/error", response_model=AppResponse[str])
async def raise_error(error_type: str = ""):
    if error_type == "400":
        raise HTTPException(status_code=400, detail="sample bad request")
    if error_type == "404":
        raise HTTPException(status_code=404, detail="sample not found")
        
    response_data = AppResponse[str](
        status=200,
        message="Success",
        data="ok",
    )
    return response_data.generate_json_response()

@hello_world_router.post("/upload-file")
def upload_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    destination = Path('/home/mos/drive_0/workspace/python/fastapi_crud/data/' + str(fileb.filename))
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(fileb.file, buffer)
    finally:
        fileb.file.close()

    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }