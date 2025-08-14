from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.app import app
from src.dto.response import AppResponse
from sqlalchemy.exc import OperationalError
import logging
import time

@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, e: StarletteHTTPException):
    print(f"OMG! An HTTP error!: {repr(e)}")
    return await http_exception_handler(request, e)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, e: HTTPException):
    response_data = AppResponse[str](
        status=e.status_code,
        message=e.detail,
        data=None,
    )
    return response_data.generate_json_response()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, e: RequestValidationError):
    response_data = AppResponse[list[dict]](
        status=422,
        message="payload is invalid",
        data=[
            {
                "type": error["type"],
                "loc": error["loc"],
                # "error": error,
                "msg": error["msg"],
                "input": error.get("ctx", {}).get(
                    "value", None
                ),  # Include the input value if available
            }
            for error in e.errors()
        ],
    )
    return response_data.generate_json_response()


@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, e: OperationalError):
    print(f"OMG! An ops error!: {repr(e)}")
    response_data = AppResponse[str](
        status=500,
        message=str(e),
        data=None,
    )
    return response_data.generate_json_response()